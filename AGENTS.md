# TKVM — 4-bit CPU Verilog

University project: single-cycle 4-bit CPU in Verilog (RTL simulation only).

## Quick commands

```sh
make              # compile + simulate tb/tb_cpu_top.v (MUL only)
make wave         # open GTKWave on cpu_top.vcd
make clean        # rm -f cpu_tb.out cpu_top.vcd

# Assemble .asm → .hex
python tools/assembler.py prog/add.asm -o sim/prog.hex

# Python reference simulator
python tools/sim_cpu.py sim/prog.hex --trace

# Run ALL tests (ADD, MUL, FIB) via SystemVerilog testbench
iverilog -o sim/tb.vvp rtl/tb_cpu.sv rtl/*.v
vvp sim/tb.vvp
```

## Key files

| Path | Role |
|------|------|
| `rtl/*.v` | CPU modules (ALU, control, regfile, memory, top) |
| `rtl/tb_cpu.sv` | **Preferred testbench** — runs ADD, MUL, FIB programs |
| `tb/tb_cpu_top.v` | Simple testbench — only runs MUL |
| `tb/tb_alu_4bit.v` | ALU unit test |
| `tools/assembler.py` | `.asm` → 9-bit `.hex` (3 hex digits/line) |
| `tools/sim_cpu.py` | Python behavioral reference model |
| `prog/*.asm` | Assembly programs |
| `sim/*.hex` | Compiled machine code |
| `docs/isa.md` | ISA reference (16 opcodes, 9-bit word) |

## Architecture essentials

- **Harvard**: 16x9 ROM (instructions), 16x4 RAM (data)
- **4 registers**: R0 (accumulator for LOAD/STORE), R1-R3 (general)
- **Flags**: Z, N, C — registered (latched at clock edge). Branches read flags from *previous* ALU op.
- **HALT**: freezes PC, stops execution
- **MOV/LDI share opcode `0011`**: distinguished by `imm_mode` bit[8]. LDI always loads into R0.

## Gotchas

- `make` / `make run` = only `tb/tb_cpu_top.v` (MUL). Run `rtl/tb_cpu.sv` for full suite.
- Testbench uses `cpu_top.load_program()` and `cpu_top.preload_ram()` via hierarchical refs — works in Icarus.
- Assembler outputs 9-bit values as 3 hex digits (`%03X`), compatible with `$readmemh`.
- No `.gitignore` — don't commit `.vcd`, `.vvp`, `.out` files.
- `package.json` is for slide generation (`create_slides.js`), unrelated to simulation.

## Workflow

1. Edit `.asm` → `tools/assembler.py` → `.hex`
2. Verify with `tools/sim_cpu.py --trace`
3. Simulate RTL via `rtl/tb_cpu.sv` or `tb/tb_cpu_top.v`
4. Debug with `make wave` (GTKWave)
