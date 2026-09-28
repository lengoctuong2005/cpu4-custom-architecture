# CPU4: Synthesizable 4-Bit Harvard Microprocessor & Complete Synopsys 32nm ASIC Implementation Flow

[![HDL](https://img.shields.io/badge/HDL-Verilog--2001-blue.svg)](https://en.wikipedia.org/wiki/Verilog)
[![Synthesis](https://img.shields.io/badge/Synthesis-Synopsys%20Design%20Compiler-red.svg)](https://www.synopsys.com)
[![PnR](https://img.shields.io/badge/P%26R-Synopsys%20IC%20Compiler%20II-orange.svg)](https://www.synopsys.com)
[![Formal](https://img.shields.io/badge/Formal-Synopsys%20Formality-purple.svg)](https://www.synopsys.com)
[![Simulation](https://img.shields.io/badge/Simulation-Icarus%20Verilog%20%7C%20VCS-green.svg)](https://steveicarus.github.io/iverilog/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade digital IC design project implementing a custom **4-bit single-cycle Harvard microprocessor** from architectural specification to full ASIC implementation (RTL to GDSII) using the **Synopsys SAED 32nm EDK PDK**.

This repository contains the complete synthesizable RTL core, a custom 2-pass Python assembler, cycle-accurate architectural emulator, exhaustive self-checking testbenches, SDC timing constraints, Design Compiler logic synthesis scripts, Formality logic equivalence checking (LEC) suites, and IC Compiler II physical design scripts.

---

## 1. Architectural Highlights

- **Harvard Memory Architecture**: Physically separated 16x9-bit Instruction Memory (IMEM) and 16x4-bit Data Memory (DMEM) eliminating structural bus conflicts in single-cycle execution.
- **Register File**: 4 general-purpose registers (`R0` to `R3`, 4-bit wide) featuring dual asynchronous read ports and single synchronous write port. `R0` serves as the architectural accumulator for memory transfers (`LOAD`, `STORE`) and immediate value loading (`LDI`).
- **Arithmetic Logic Unit (ALU)**: 4-bit ALU supporting 8 distinct operations (ADD, SUB, AND, OR, XOR, INC, DEC, PASS-THROUGH).
- **Conditional Flag Latching**: Zero (`Z`), Negative (`N`), and Carry (`C`) flags are conditionally latched via a dedicated `flag_write` control line. Non-arithmetic operations (`MOV`, `LOAD`, `STORE`, `NOP`, `OUT`) preserve flag states, allowing instruction scheduling between flag generation and conditional branch targets (`JZ`, `JN`).
- **Timing & Performance**: Constrained for 100 MHz clock frequency ($\tau_{clk} = 10.0\text{ ns}$) with 0.2 ns clock uncertainty under typical operating conditions.

---

## 2. Technical Specifications

| Parameter | Specification | Details |
| :--- | :--- | :--- |
| **Architecture** | Single-Cycle RISC Harvard | Fixed 1-cycle execution per instruction |
| **Data Bus Width** | 4-bit | Nibble-wide datapath and internal bus interconnect |
| **Instruction Word Width** | 9-bit | `[8] imm_mode` \| `[7:4] opcode` \| `[3:0] operand` |
| **Instruction Memory (ROM)**| 16 words x 9-bit | Parameterized simulation model & synthesizable case ROM |
| **Data Memory (RAM)** | 16 words x 4-bit | Asynchronous read, positive edge synchronous write |
| **General Purpose Registers**| 4 x 4-bit (`R0`–`R3`) | 2 read ports, 1 write port; `R0` accumulator |
| **Program Counter (PC)** | 4-bit | Sequential increment, synchronous branch target load, halt freeze |
| **Target Technology** | Synopsys SAED 32nm EDK | Nominal 1.05V, 25°C, typical-typical corner |
| **Target Frequency** | 100 MHz | Constrained via Synopsys SDC (`cpu4.sdc`) |

---

## 3. Instruction Set Architecture (ISA)

The processor implements a fixed 9-bit instruction word:
```text
 8             7             4 3             0
+---------------+---------------+---------------+
|   imm_mode    |    opcode     |    operand    |
|    (1 bit)    |   (4 bit)     |    (4 bit)    |
+---------------+---------------+---------------+
```

### Complete Opcode Table

| Opcode | Mnemonic | Format | RTL Micro-operations | Flags | Description |
| :---: | :--- | :--- | :--- | :---: | :--- |
| `0000` | `NOP` | `NOP` | None | - | No operation. PC increments. |
| `0001` | `LOAD` | `LOAD addr` | `R0 <= DMEM[addr]` | - | Load 4-bit data from RAM address into R0. |
| `0010` | `STORE` | `STORE addr` | `DMEM[addr] <= R0` | - | Store R0 content into RAM address. |
| `0011` | `LDI` | `LDI #imm4` (`imm_mode=1`) | `R0 <= imm4` | Z, N | Load 4-bit immediate constant into R0. |
| `0011` | `MOV` | `MOV Rd, Rs` (`imm_mode=0`)| `R[Rd] <= R[Rs]` | - | Copy value from source register Rs to Rd. |
| `0100` | `ADD` | `ADD Rd, Rs` | `R[Rd] <= R[Rd] + R[Rs]` | Z, N, C | Add Rs to Rd, write result to Rd. |
| `0101` | `SUB` | `SUB Rd, Rs` | `R[Rd] <= R[Rd] - R[Rs]` | Z, N, C | Subtract Rs from Rd, write result to Rd. |
| `0110` | `AND` | `AND Rd, Rs` | `R[Rd] <= R[Rd] & R[Rs]` | Z, N | Bitwise AND of Rd and Rs. |
| `0111` | `OR` | `OR Rd, Rs` | `R[Rd] <= R[Rd] \| R[Rs]` | Z, N | Bitwise OR of Rd and Rs. |
| `1000` | `XOR` | `XOR Rd, Rs` | `R[Rd] <= R[Rd] ^ R[Rs]` | Z, N | Bitwise XOR of Rd and Rs. |
| `1001` | `INC` | `INC Rd` | `R[Rd] <= R[Rd] + 1` | Z, N, C | Increment destination register Rd by 1. |
| `1010` | `DEC` | `DEC Rd` | `R[Rd] <= R[Rd] - 1` | Z, N, C | Decrement destination register Rd by 1. |
| `1011` | `JMP` | `JMP target` | `PC <= target` | - | Unconditional branch to 4-bit target address. |
| `1100` | `JZ` | `JZ target` | `PC <= (Z ? target : PC + 1)` | - | Branch to target if Zero flag is set. |
| `1101` | `JN` | `JN target` | `PC <= (N ? target : PC + 1)` | - | Branch to target if Negative flag is set. |
| `1110` | `OUT` | `OUT Rs` | `out_port <= R[Rs]` | - | Latch source register value to output port. |
| `1111` | `HALT` | `HALT` | `halt <= 1; PC <= PC` | - | Freeze program counter and stop execution. |

---

## 4. Synopsys Commercial ASIC Implementation Flow

The design includes full commercial EDA scripts targeting standard cell library deployment:

```text
[ RTL Source: Verilog-2001 ]
            │
            ▼
[ Simulation & Verification ] ───► VCS / Icarus Verilog + GTKWave
            │
            ▼
[ Logic Synthesis ] ──────────────► Synopsys Design Compiler (dc_shell)
   ├── SDC Timing Constraints     Target: SAED 32nm EDK Standard Cells
   └── Wire Load Models           Outputs: Gate-level Netlist, Area/Timing/Power Reports
            │
            ▼
[ Formal Equivalence (LEC) ] ────► Synopsys Formality (fm_shell)
                                  Verification: RTL vs Gate Netlist (verify_rtl_gate.fms)
            │
            ▼
[ Physical Design (PnR) ] ───────► Synopsys IC Compiler II (icc2_shell)
   ├── Floorplanning & Power Mesh (`scripts/power.tcl`)
   ├── Standard Cell Placement & Optimization
   ├── Clock Tree Synthesis (CTS) with NDR (`scripts/ndr.tcl`)
   ├── Detailed Routing & DRC/LVS Verification
   └── GDSII Streaming (`cpu4.gds`)
            │
            ▼
[ Post-PnR Verification ] ───────► Synopsys Formality (Post-PnR Netlist vs Synthesis Netlist)
```

### EDA Configuration Files
- `cons/cpu4.sdc`: Primary timing constraints setting clock definition (100 MHz), clock latency, uncertainty (0.2 ns), input/output delays (2.0 ns), and output capacitive load (0.05 pF).
- `syn/run_dc.tcl`: Synthesis automation script for `dc_shell` with clock gating, boundary optimization, and report generation.
- `PnR/run_icc2.tcl`: Complete physical design script covering floorplanning, power rings, cell placement, CTS, route optimization, and GDSII generation.
- `Formal/RTL_vs_Gate/verify_rtl_gate.fms`: Formality script verifying functional equivalence between RTL and post-synthesis gate-level netlist.
- `Formal/Post_PnR/verify_post_pnr.fms`: Formality script verifying post-routing netlist against post-synthesis netlist.

---

## 5. Software Toolchain

### Custom 2-Pass Python Assembler (`tools/assembler.py`)
Converts custom assembly language (`.asm`) into 9-bit hex machine code (`.hex`) and commented memory initialization files (`.mem`).
- **Pass 1**: Resolves symbol labels and calculates 4-bit PC offsets.
- **Pass 2**: Emits machine code words with validation against 16-instruction memory bounds.

```bash
# Assemble assembly program to machine code
python3 tools/assembler.py prog/fib.asm -o sim/fib.hex
```

### Cycle-Accurate Python Reference Model (`tools/sim_cpu.py`)
An independent software emulator that mimics register states, ALU operations, flag updates, and memory cycles bit-for-bit against the hardware RTL. Used for golden-reference regression verification.

```bash
# Run cycle-by-cycle behavioral execution
python3 tools/sim_cpu.py sim/fib.hex --trace
```

---

## 6. Verified Demonstration Programs

| Routine | Source | Algorithm | Expected Verification Output |
| :--- | :--- | :--- | :--- |
| **Multiplication** | [`prog/mul.asm`](prog/mul.asm) | Software multiplication via repeated addition ($3 \times 4 = 12$) | `out_port = 12 (0xC)`, `DMEM[12] = 12` |
| **Memory Addition**| [`prog/add.asm`](prog/add.asm) | Load two operands from RAM, compute sum, store to RAM ($5 + 7 = 12$) | `out_port = 12 (0xC)`, `DMEM[12] = 12` |
| **Fibonacci** | [`prog/fib.asm`](prog/fib.asm) | Compute sequence until value exceeds 4-bit saturation limit | Sequence `1, 1, 2, 3, 5, 8` on `out_port` |
| **Flag Isolation** | [`prog/flag_test.asm`](prog/flag_test.asm) | Interleave non-arithmetic `MOV` between arithmetic operation and `JZ` | Verifies conditional jump with preserved flags |

---

## 7. Quickstart & Verification Guide

### Prerequisites
- **Simulation**: [Icarus Verilog](https://steveicarus.github.io/iverilog/) (`iverilog`, `vvp`) and [GTKWave](https://gtkwave.sourceforge.net/).
- **Software**: Python 3.8+ (for assembler and golden model).
- **Commercial EDA (Optional)**: Synopsys VCS, Design Compiler, Formality, IC Compiler II (2020.09+).

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y iverilog gtkwave python3 build-essential
```

### Running Simulations

```bash
# 1. Run full end-to-end CPU verification (all 4 demo programs)
make test

# 2. Run ALU unit verification (14 corner cases)
make alu

# 3. Run Python golden reference model simulation
make pysim

# 4. Re-assemble all assembly test programs
make asm

# 5. Open simulation waveform in GTKWave
make wave

# 6. Clean generated simulation artifacts
make clean
```

### Expected Simulation Output (`make test`)

```text
======================================================================
                  CPU4 REGRESSION VERIFICATION SUITE
======================================================================
---- RUNNING: MUL (3 x 4) ----
[PASS] MUL : halt after 23 cycles, out_port=12 (0xc)
MUL value check OK: OUT=12, Mem[12]=12

---- RUNNING: ADD (5 + 7) ----
[PASS] ADD : halt after 8 cycles, out_port=12 (0xc)
ADD value check OK: OUT=12, Mem[12]=12

---- RUNNING: FIBONACCI ----
[PASS] FIB : halt after 36 cycles, out_port=8 (0x8)
FIB OUT sequence captured (6 values):
  OUT[0] = 1, OUT[1] = 1, OUT[2] = 2, OUT[3] = 3, OUT[4] = 5, OUT[5] = 8
FIB sequence OK: 1,1,2,3,5,8 (full match)

---- RUNNING: FLAG PRESERVATION ----
[PASS] FLAG : halt after 9 cycles, out_port=12 (0xc)
FLAG value check OK: OUT=12
======================================================================
RESULT: 4 PASS, 0 FAIL
ALL TESTS PASSED
======================================================================
```

---

## 8. Repository Structure

```text
.
├── cons/
│   └── cpu4.sdc                    # Synopsys SDC timing constraints (100MHz clock, I/O delays)
├── docs/
│   ├── isa.md                      # Detailed Instruction Set Architecture specification
│   ├── setup.md                    # Environment and simulation setup manual
│   └── audit-report.md             # Verification and code audit post-mortem
├── Formal/
│   ├── RTL_vs_Gate/
│   │   └── verify_rtl_gate.fms     # Formality LEC script (RTL vs DC Netlist)
│   └── Post_PnR/
│       └── verify_post_pnr.fms     # Formality LEC script (DC Netlist vs ICC2 Netlist)
├── imem/
│   ├── instruction_memory_sim.v    # Parameterized ROM for VCS / Icarus simulation
│   └── instruction_memory_rom.v    # Hardwired case-statement ROM for synthesis & Formality
├── PnR/
│   ├── run_icc2.tcl                # IC Compiler II automated physical design flow
│   └── scripts/
│       ├── power.tcl               # Power ring and strap creation script
│       └── ndr.tcl                 # Non-Default Routing rules for CTS
├── prog/
│   ├── add.asm                     # Assembly program: memory addition
│   ├── fib.asm                     # Assembly program: Fibonacci sequence
│   ├── flag_test.asm               # Assembly program: flag preservation test
│   └── mul.asm                     # Assembly program: software multiplication
├── report_assets/
│   ├── alu_schematic.svg           # Gate-level schematic of the 4-bit ALU
│   ├── cpu_top_schematic.svg       # Full processor datapath interconnect diagram
│   ├── gate_level_schematic.svg    # Synthesized gate-level netlist view
│   ├── anhGDS.jpg                  # Post-routing layout capture (GDSII preview)
│   └── waveform_*.png              # Annotated simulation waveforms
├── rtl/
│   ├── alu_4bit.v                  # 4-bit 8-operation Arithmetic Logic Unit
│   ├── control_unit.v              # Opcode decoder and flag-latch control FSM
│   ├── cpu_top.v                   # Top-level datapath module (module cpu_top)
│   ├── data_memory.v               # 16x4-bit synchronous RAM (DMEM)
│   ├── instruction_memory.v        # Default instruction ROM wrapper
│   ├── program_counter.v           # 4-bit Program Counter with halt and branch logic
│   └── register_file.v             # 4x4-bit dual-read single-write general register bank
├── sim/
│   ├── prog.hex, fib.hex, mul.hex  # Machine code hex files
│   ├── prog.mem, data.mem          # Memory initialization images
│   ├── gate_level_netlist.v        # Synthesized gate netlist
│   └── yosys_script.ys             # Open-source gate synthesis script
├── syn/
│   └── run_dc.tcl                  # Synopsys Design Compiler synthesis script (SAED 32nm)
├── tb/
│   ├── tb_alu_4bit.v               # Exhaustive ALU unit testbench (14 boundary cases)
│   └── tb_cpu_top.v                # End-to-end self-checking system testbench
├── tools/
│   ├── assembler.py                # Custom 2-pass Python assembler
│   ├── sim_cpu.py                  # Cycle-accurate golden Python CPU emulator
│   ├── synth.ys                    # Yosys RTL synthesis flow
│   └── plot_*_waveform.py          # Waveform visualization scripts
├── .gitignore                      # Ignore simulation outputs, EDA database caches
├── LICENSE                         # MIT License
├── Makefile                        # Project automation driver
└── README.md                       # Main technical documentation
```

---

## 9. Author & Contact

**Le Ngoc Tuong**  
Faculty of Electrical & Electronics Engineering  
Ho Chi Minh City University of Technology and Education (HCMUTE)  
GitHub: [@lengoctuong2005](https://github.com/lengoctuong2005)  
Email: [lengoctuong.work@gmail.com](mailto:lengoctuong.work@gmail.com)

---

## 10. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
