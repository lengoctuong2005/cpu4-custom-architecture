#!/usr/bin/env python3
"""
TKVM 4-bit CPU Behavioral Simulator (Python reference model)
============================================================
Muc dich:
  - Mo phong datapath single-cycle cua CPU 4-bit theo docs/isa.md.
  - Doc chuong trinh tu file .hex (do tools/assembler.py sinh ra, dang $readmemh).
  - In trace tung chu ky (PC, opcode, operand, thanh ghi, OUT, flags) de nhom hieu ro.
  - Kiem tra ket qua cuoi cung (OUT, Mem[12], v.v.).

Kien truc (theo ISA):
  - 4 thanh ghi R0..R3 (4-bit), R0 la accumulator cho LOAD/STORE.
  - ROM 16x9 (instruction), RAM 16x4 (data).
  - Flags: Z (result==0), N (bit3==1), C (carry/borrow bit4 cua phep +,-).
  - Single-cycle: 1 lenh / 1 chu ky. HALT dong bang PC.

Instruction word 9-bit: [imm_mode 1][opcode 4][operand 4]
  - MOV reg-reg: imm_mode=0, operand = {Rd[1:0], Rs[1:0]}
  - LDI #imm:  imm_mode=1, opcode=0011, operand = imm[3:0] (0..15)
                Loads immediate into R0 (implicit register). C=0.

Quy uoc C (chuan, da chot voi user):
  - ADD:  C = 1 khi co nho bit 4 (a+b >= 16)
  - SUB:  C = 1 khi KHONG co muon (a >= b), C = 0 khi a < b (co muon)
  - INC:  C = 1 khi rollover (15 -> 0)
  - DEC:  C = 1 khi KHONG co muon (a >= 1), C = 0 khi a == 0 (co muon)

Usage:
  python tools/sim_cpu.py sim/prog.hex
  python tools/sim_cpu.py sim/mul.hex --trace
  python tools/sim_cpu.py sim/fib.hex --max-cycles 200
"""

import sys
import os


# Opcode mapping (4-bit high nibble)
OPCODES = {
    0x0: "NOP",
    0x1: "LOAD",
    0x2: "STORE",
    0x3: "MOV",
    0x4: "ADD",
    0x5: "SUB",
    0x6: "AND",
    0x7: "OR",
    0x8: "XOR",
    0x9: "INC",
    0xA: "DEC",
    0xB: "JMP",
    0xC: "JZ",
    0xD: "JN",
    0xE: "OUT",
    0xF: "HALT",
}


def mask4(x):
    return x & 0xF


def load_hex(path):
    """Doc file .hex: moi dong 1 word (3 ky tu hex 9-bit). Giong $readmemh."""
    rom = [0] * 16
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith("//") or line.startswith(";"):
                continue
            if i >= 16:
                break
            rom[i] = int(line, 16) & 0x1FF
    return rom


class CPU:
    def __init__(self, rom, ram_init=None):
        self.rom = list(rom)
        self.ram = [0] * 16
        if ram_init:
            for a, v in ram_init.items():
                self.ram[a] = mask4(v)
        self.r = [0, 0, 0, 0]          # R0..R3
        self.pc = 0
        self.out = 0
        self.z = 0
        self.n = 0
        self.c = 0
        self.halted = False
        self.cycle = 0

    def set_flags(self, result, carry=None):
        """Cap nhat Z, N. Carry do caller truyen (vi SUB/DEC co quy uoc rieng)."""
        result = mask4(result)
        self.z = 1 if result == 0 else 0
        self.n = 1 if (result & 0x8) else 0
        if carry is not None:
            self.c = 1 if carry else 0

    def step(self):
        if self.halted:
            return False
        instr = self.rom[self.pc]
        opcode = (instr >> 4) & 0xF
        operand = instr & 0xF
        imm_mode = (instr >> 8) & 1    # 1 => LDI (immediate load into R0)
        mnem = OPCODES[opcode]
        next_pc = mask4(self.pc + 1)

        # snapshot cho trace
        pre = (self.pc, mnem, operand, list(self.r), self.out,
               (self.z, self.n, self.c))

        if mnem == "NOP":
            pass

        elif mnem == "LOAD":
            addr = operand
            self.r[0] = mask4(self.ram[addr])

        elif mnem == "STORE":
            addr = operand
            self.ram[addr] = mask4(self.r[0])

        elif opcode == 0x3 and imm_mode:
            # LDI #imm: opcode=0011, imm_mode=1, operand = imm[3:0]
            # Loads immediate into R0 (implicit register), C=0
            self.r[0] = mask4(operand)
            self.set_flags(self.r[0], carry=0)

        elif mnem == "MOV":
            # MOV reg-reg: imm_mode=0, operand = {Rd[1:0], Rs[1:0]}
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            self.r[rd] = mask4(self.r[rs])

        elif mnem == "ADD":
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            a = self.r[rd]
            b = self.r[rs]
            s = a + b
            self.r[rd] = mask4(s)
            self.set_flags(self.r[rd], carry=(s >= 16))

        elif mnem == "SUB":
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            a = self.r[rd]
            b = self.r[rs]
            # C = 1 khi KHONG co muon (a >= b)
            diff = a - b
            borrow = a < b
            self.r[rd] = mask4(diff)
            self.set_flags(self.r[rd], carry=(not borrow))

        elif mnem == "AND":
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            self.r[rd] = mask4(self.r[rd] & self.r[rs])
            self.set_flags(self.r[rd])

        elif mnem == "OR":
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            self.r[rd] = mask4(self.r[rd] | self.r[rs])
            self.set_flags(self.r[rd])

        elif mnem == "XOR":
            rd = (operand >> 2) & 0x3
            rs = operand & 0x3
            self.r[rd] = mask4(self.r[rd] ^ self.r[rs])
            self.set_flags(self.r[rd])

        elif mnem == "INC":
            rd = (operand >> 2) & 0x3
            v = self.r[rd] + 1
            self.r[rd] = mask4(v)
            self.set_flags(self.r[rd], carry=(v >= 16))

        elif mnem == "DEC":
            rd = (operand >> 2) & 0x3
            v = self.r[rd]
            # C = 1 khi KHONG co muon (v >= 1)
            borrow = (v == 0)
            self.r[rd] = mask4(v - 1)
            self.set_flags(self.r[rd], carry=(not borrow))

        elif mnem == "JMP":
            next_pc = operand

        elif mnem == "JZ":
            if self.z:
                next_pc = operand

        elif mnem == "JN":
            if self.n:
                next_pc = operand

        elif mnem == "OUT":
            rs = operand & 0x3
            self.out = mask4(self.r[rs])

        elif mnem == "HALT":
            self.halted = True
            # PC dong bang (giu nguyen)

        if not self.halted:
            self.pc = next_pc
        self.cycle += 1
        return pre, mnem, operand

    def run(self, max_cycles=200, trace=False):
        print(f"=== TKVM CPU SIM START (ROM={len([x for x in self.rom if x])} instr) ===")
        if trace:
            print(f"{'cyc':>3} | {'PC':>2} | {'OP':<6} | {'opnd':>4} | "
                  f"R0 R1 R2 R3 | OUT | Z N C")
            print("-" * 52)
        while not self.halted and self.cycle < max_cycles:
            snap = self.step()
            if trace:
                pc, mnem, operand, r, out, fl = snap[0]
                z, n, c = fl
                print(f"{self.cycle-1:>3} | {pc:>2} | {mnem:<6} | "
                      f"0x{operand:X} | {r[0]} {r[1]} {r[2]} {r[3]} | "
                      f"{out} | {z} {n} {c}")
        if self.cycle >= max_cycles and not self.halted:
            print(f"[WARN] Reached max_cycles={max_cycles}, halted forcibly.")
            self.halted = True
        print("=== SIM DONE ===")
        print(f"OUT port = {self.out} (0x{self.out:X})")
        print(f"Registers: R0={self.r[0]} R1={self.r[1]} R2={self.r[2]} R3={self.r[3]}")
        print(f"Flags: Z={self.z} N={self.n} C={self.c}")
        print(f"RAM[10]={self.ram[10]} RAM[11]={self.ram[11]} RAM[12]={self.ram[12]} "
              f"RAM[13]={self.ram[13]} RAM[14]={self.ram[14]} RAM[15]={self.ram[15]}")
        return self


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/sim_cpu.py <prog.hex> [--trace] [--max-cycles N]")
        sys.exit(1)
    hex_path = sys.argv[1]
    trace = "--trace" in sys.argv
    max_cycles = 200
    if "--max-cycles" in sys.argv:
        idx = sys.argv.index("--max-cycles")
        if idx + 1 < len(sys.argv):
            max_cycles = int(sys.argv[idx + 1])

    if not os.path.exists(hex_path):
        print(f"[ERROR] File not found: {hex_path}")
        sys.exit(1)

    # RAM init linh hoat qua --ram a=v,b=v (vi du: --ram 10=3,11=4).
    # Mac dinh khong preload (RAM = 0). Moi chuong trinh truyen rieng.
    ram_init = {}
    if "--ram" in sys.argv:
        idx = sys.argv.index("--ram")
        if idx + 1 < len(sys.argv):
            for pair in sys.argv[idx + 1].split(","):
                if "=" in pair:
                    a, v = pair.split("=", 1)
                    ram_init[int(a)] = int(v) & 0xF

    rom = load_hex(hex_path)
    cpu = CPU(rom, ram_init)
    cpu.run(max_cycles=max_cycles, trace=trace)


if __name__ == "__main__":
    main()
