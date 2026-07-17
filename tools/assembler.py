#!/usr/bin/env python3
"""
# TKVM 4-bit CPU Assembler
=======================
Chuyen file assembly (.asm) thanh file hex (.hex) de nap vao ROM ($readmemh).

Dinh dang instruction word 9-bit: [imm_mode 1][opcode 4][operand 4]
  Opcode map (4-bit):
    0x0 NOP   0x1 LOAD  0x2 STORE 0x3 MOV   0x4 ADD   0x5 SUB
    0x6 AND   0x7 OR    0x8 XOR   0x9 INC   0xA DEC   0xB JMP
    0xC JZ    0xD JN    0xE OUT   0xF HALT
    LDI is MOV with imm_mode=1 (opcode still 0011)

  Field encoding (operand 4-bit):
  LOAD/STORE:     operand = {addr[3:0]}            (RAM address 0..15)
  JMP/JZ/JN:      operand = {addr[3:0]}            (jump to label/address)
  RR_OPS (ADD/SUB/AND/OR/XOR/MOV):
                   operand = {Rd[1:0], Rs[1:0]}      (reg-reg only)
  LDI (bit8=1):   opcode = 0011, operand = imm[3:0] (0..15)
                   Cu phap: LDI #imm  (always loads into R0)
                   De nap vao R1/R2/R3: LDI #imm roi MOV Rx, R0
  INC/DEC:        operand = {Rd[2 bit], 00}
  OUT:            operand = {00, Rs[2 bit]}
  NOP/HALT:       operand = 0000

Cach dung:
  python tools/assembler.py prog/add.asm -o sim/prog.hex
  python tools/assembler.py prog/fib.asm --run     # sinh hex roi in ra
"""

import sys
import os

# Opcode mapping
OPCODES = {
    "NOP": 0x0, "LOAD": 0x1, "STORE": 0x2, "MOV": 0x3,
    "ADD": 0x4, "SUB": 0x5, "AND": 0x6, "OR": 0x7,
    "XOR": 0x8, "INC": 0x9, "DEC": 0xA, "JMP": 0xB,
    "JZ": 0xC, "JN": 0xD, "OUT": 0xE, "HALT": 0xF,
    "LDI": 0x3,   # immediate load: shares opcode 0011 with MOV, imm_mode=1
}

REG_NAMES = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}

# Loai lenh
ADDR_OPS = ("LOAD", "STORE", "JMP", "JZ", "JN")   # can dia chi (hoac label)
RR_OPS = ("ADD", "SUB", "AND", "OR", "XOR", "MOV")  # can 2 thanh ghi (reg-reg only)
LDI_OPS = ("LDI",)                                # 1 toan hang: LDI #imm
ONE_REG_OPS = ("INC", "DEC", "OUT")                 # can 1 thanh ghi


def parse_int(s):
    """Parse so hex (0x..) hoac dec."""
    s = s.strip()
    if s.lower().startswith("0x"):
        return int(s, 16)
    return int(s, 10)


def assemble_line(line, labels, line_no):
    """Tra ve (word_9bit, None) hoac (None, 'LABEL_DEF') neu la dong nhan.

    Word 9-bit: [imm_mode 1][opcode 4][operand 4]
    """
    # bo comment
    if ";" in line:
        line = line[:line.index(";")]
    line = line.strip()
    if not line:
        return None, "EMPTY"

    # Nhan:  LABEL:
    if line.endswith(":") and " " not in line and not line.startswith("."):
        name = line[:-1].strip()
        return None, "LABEL_DEF"

    # Tach mnemonic va operand
    if " " in line:
        parts = line.split(" ", 1)
    else:
        parts = [line]
    mnem = parts[0].strip().upper()
    if mnem not in OPCODES:
        raise ValueError(f"Dong {line_no}: mnemonic khong hop le '{parts[0]}'")
    opc = OPCODES[mnem]
    imm_mode = 0  # mac dinh (chi MOV immediate moi set = 1)

    operand_field = ""
    if len(parts) > 1:
        operand_field = parts[1].strip()

    if mnem in ("NOP", "HALT"):
        if operand_field:
            raise ValueError(f"Dong {line_no}: {mnem} khong nhan toan hang")
        operand = 0
    elif mnem in ADDR_OPS:
        if not operand_field:
            raise ValueError(f"Dong {line_no}: {mnem} can dia chi")
        # co the la nhan hoac so
        if operand_field in labels:
            addr = labels[operand_field]
            if addr is None:
                raise ValueError(f"Dong {line_no}: nhan '{operand_field}' chua duoc gan dia chi (nhay tien/lui chua quet)")
            val = addr
        else:
            val = parse_int(operand_field)
        if not (0 <= val <= 15):
            raise ValueError(f"Dong {line_no}: dia chi {val} ngoai 0..15")
        operand = val & 0xF
    elif mnem in RR_OPS:
        regs = [r.strip().upper() for r in operand_field.split(",")]
        if len(regs) != 2:
            raise ValueError(f"Dong {line_no}: {mnem} can 2 thanh ghi (Rd, Rs)")
        if regs[0] not in REG_NAMES or regs[1] not in REG_NAMES:
            raise ValueError(f"Dong {line_no}: thanh ghi phai la R0..R3")
        rd = REG_NAMES[regs[0]]
        rs = REG_NAMES[regs[1]]
        imm_mode = 0
        operand = ((rd & 0x3) << 2) | (rs & 0x3)
    elif mnem in LDI_OPS:
        # LDI #imm  ->  bit8=1, opcode=0011, operand = imm[3:0] (0..15)
        # Luon nap vao R0 (implicit register)
        if not operand_field or not operand_field.startswith("#"):
            raise ValueError(f"Dong {line_no}: LDI can 1 toan hang dang #imm (vi du: LDI #5)")
        imm = parse_int(operand_field[1:])
        if not (0 <= imm <= 15):
            raise ValueError(f"Dong {line_no}: LDI immediate {imm} ngoai 0..15")
        imm_mode = 1
        operand = imm & 0xF
    elif mnem in ONE_REG_OPS:
        reg = operand_field.strip().upper()
        if reg not in REG_NAMES:
            raise ValueError(f"Dong {line_no}: {mnem} can 1 thanh ghi R0..R3")
        r = REG_NAMES[reg]
        if mnem == "OUT":
            operand = (0 << 2) | (r & 0x3)  # Rs o bits [1:0]
        else:  # INC/DEC: Rd o bits [3:2]
            operand = ((r & 0x3) << 2)
    else:
        raise ValueError(f"Dong {line_no}: khong xu ly duoc {mnem}")

    return (imm_mode << 8) | (opc << 4) | (operand & 0xF), None


def assemble(text):
    """Tra ve list cac word 9-bit (toi da 16)."""
    # Pass 1: tim dia chi cac nhan
    labels = {}
    pc = 0
    lines = text.splitlines()
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith(";") or line.startswith("//"):
            continue
        # nhan
        if line.endswith(":") and " " not in line and not line.startswith("."):
            name = line[:-1].strip()
            labels[name] = pc
            continue
        pc += 1
        if pc >= 16:
            break

    # Pass 2: sinh code
    program = []
    pc = 0
    for i, raw in enumerate(lines):
        line_no = i + 1
        line = raw.strip()
        if not line or line.startswith(";") or line.startswith("//"):
            continue
        if line.endswith(":") and " " not in line and not line.startswith("."):
            continue  # nhan da xu ly
        word, kind = assemble_line(line, labels, line_no)
        if kind in ("EMPTY", "LABEL_DEF"):
            continue
        if word is None:
            raise ValueError(f"Dong {line_no}: loi assemble")
        program.append(word)
        pc += 1
        if pc >= 16:
            print(f"[WARN] Vuot qua 16 lenh, cat bo phan con lai.")
            break
    return program


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/assembler.py <file.asm> [-o out.hex] [--run]")
        sys.exit(1)
    asm_path = sys.argv[1]
    out_path = None
    do_run = False
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            out_path = sys.argv[idx + 1]
    if "--run" in sys.argv:
        do_run = True

    if not os.path.exists(asm_path):
        print(f"[ERROR] File not found: {asm_path}")
        sys.exit(1)

    with open(asm_path, "r", encoding="utf-8") as f:
        src = f.read()

    try:
        program = assemble(src)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            for b in program:
                f.write(f"{b:03X}\n")
        print(f"[OK] Created {out_path} ({len(program)} instructions)")
    else:
        for b in program:
            print(f"{b:03X}")

    if do_run or not out_path:
        # In disassembly de kiem tra
        print("\n--- Disassembly preview ---")
        for addr, w in enumerate(program):
            imm_mode = (w >> 8) & 1
            opc = (w >> 4) & 0xF
            operand = w & 0xF
            print(f"[{addr:02d}] {w:03X}  opc={opc:01X} opnd={operand:01X} imm={imm_mode}")


if __name__ == "__main__":
    main()
