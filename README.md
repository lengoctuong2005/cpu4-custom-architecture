# CPU4: Synthesizable 4-Bit Microprocessor & Complete Synopsys 32nm ASIC Implementation Flow

[![HDL](https://img.shields.io/badge/HDL-Verilog--2001-blue.svg)](https://en.wikipedia.org/wiki/Verilog)
[![Synthesis](https://img.shields.io/badge/Synthesis-Synopsys%20Design%20Compiler-red.svg)](https://www.synopsys.com)
[![PnR](https://img.shields.io/badge/P%26R-Synopsys%20IC%20Compiler%20II-orange.svg)](https://www.synopsys.com)
[![Formal](https://img.shields.io/badge/Formal-Synopsys%20Formality-purple.svg)](https://www.synopsys.com)
[![FPGA](https://img.shields.io/badge/FPGA-Intel%20Quartus%20Prime-0071C5.svg)](https://www.intel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

CPU4 is a synthesizable 4-bit single-cycle Harvard microprocessor designed and implemented across the complete digital ASIC design cycle, from architectural specification and RTL coding to Synopsys 32nm physical implementation (GDSII) and FPGA validation on Intel hardware.

Designed for production-grade engineering rigor, this repository includes synthesizable Verilog-2001 RTL, SDC timing constraints, Synopsys Design Compiler synthesis scripts, Synopsys IC Compiler II physical design recipes, Synopsys Formality logic equivalence checking suites, Intel Quartus Prime FPGA deployment wrappers, a 2-pass Python assembler, and a cycle-accurate architectural emulator.

---

## 1. Executive Summary

This project demonstrates practical competence across front-end logic design, functional verification, logical synthesis, formal verification, physical design, and hardware prototyping. The CPU4 design targets digital IC design and semiconductor engineering roles (such as digital design, ASIC synthesis, STA, physical design, and verification engineering):

- **Synthesizable Microarchitecture**: Clean, single-cycle Harvard architecture written in standard Verilog-2001 without proprietary IP dependencies or vendor-locked primitives.
- **Front-End & Verification Rigor**: Exhaustive corner-case testbenches verified under Icarus Verilog and Synopsys VCS, supplemented by a cycle-accurate Python golden reference model.
- **Commercial Synthesis Flow**: Synopsys Design Compiler automation targeting the Synopsys SAED 32nm EDK standard cell library (`saed32rvt_tt1p05v25c.db`), constrained under industrial SDC specifications at 100 MHz.
- **Formal Verification (LEC)**: Two-stage Synopsys Formality verification verifying structural and logical equivalence across RTL vs. Synthesis Netlist and Synthesis Netlist vs. Post-PnR Netlist.
- **Physical Implementation (PnR)**: Complete IC Compiler II flow executing floorplanning, power grid routing, cell placement, Clock Tree Synthesis (CTS) with Non-Default Routing (NDR) rules, detailed routing, and GDSII generation.
- **Silicon-Level Prototyping**: Complete board-level FPGA wrapper with debounced clock controls, frequency dividers, and 7-segment display drivers running on Intel Cyclone V / MAX 10 hardware.

---

## 2. Microarchitecture Specifications

```text
               +-------------------------------------------------------------+
               |                     INSTRUCTION MEMORY                      |
               |                     16 words x 9-bit (ROM)                  |
               +------------------------------+------------------------------+
                                              |
                                     instr [8:0]
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
                 imm_mode [8]            opcode [7:4]            operand [3:0]
                     |                        |                        |
                     |                        v                        |
                     |               +-----------------+               |
                     |               |  CONTROL UNIT   |               |
                     |               | (Decoder & FSM) |               |
                     |               +--------+--------+               |
                     |                        |                        |
                     |       +----------------+----------------+       |
                     |       |                |                |       |
                     |       v                v                v       |
                     |   reg_write        flag_write        alu_op     |
                     |       |                |             mem_ctrl   |
                     |       |                |                |       |
                     v       v                |                |       v
               +---------------+              |                |   +-------+
       addr -> | REGISTER FILE |              |                |   | PC    |
               |  4 x 4-bit    |              |                |   | 4-bit |
               |  (R0 to R3)   |              |                |   +-------+
               +-------+-------+              |                |       ^
                       |                      |                |       |
                 read_data1/2                 |                |    pc_src
                       |                      |                |       |
                       v                      v                v       |
               +---------------+      +---------------+   +------------+---+
               |  4-BIT ALU    | ---> | FLAG REGISTERS| ->| BRANCH CONTROL |
               | (8 Operations)|      | (Z, N, C)     |   +----------------+
               +-------+-------+      +---------------+
                       |
                  alu_result
                       |
                       +----------------------+
                       |                      |
                       v                      v
               +---------------+      +---------------+
               |  DATA MEMORY  |      |   OUT PORT    |
               | 16 x 4-bit RAM|      |    (4-bit)    |
               +---------------+      +---------------+
```

### Architectural Parameters

| Module | Dimension | Characteristics |
| :--- | :--- | :--- |
| **Architecture** | Single-Cycle Harvard | Non-multiplexed instruction and data buses |
| **Datapath Width** | 4-bit | Nibble-wide ALU, register bank, and data memory |
| **Instruction Word** | 9-bit | `[8]` imm_mode, `[7:4]` opcode, `[3:0]` operand |
| **Instruction ROM** | 16 words x 9-bit | Dual-target: simulation model (`$readmemh`) and synthesizable case ROM |
| **Data RAM** | 16 words x 4-bit | Asynchronous read, synchronous positive-edge write |
| **Register File** | 4 x 4-bit (`R0` to `R3`) | 2 asynchronous read ports, 1 synchronous write port; `R0` is accumulator |
| **ALU Operations** | 8 operations | ADD, SUB, AND, OR, XOR, INC, DEC, PASSTHRU |
| **Status Flags** | Zero (Z), Negative (N), Carry (C) | Conditionally updated via `flag_write` control line |
| **Target PDK** | Synopsys SAED 32nm EDK | Nominal 1.05V, 25 deg C, typical-typical corner |
| **Target Clock** | 100 MHz (10.0 ns) | Constrained via Synopsys SDC |

### Flag Preservation Pipeline
Arithmetic operations update condition flags. Non-arithmetic operations (`MOV`, `LOAD`, `STORE`, `NOP`, `OUT`) do not assert `flag_write`. This design decision decouples flag generation from branch instruction evaluation (`JZ`, `JN`), allowing compilers or assembly programmers to insert register movements without corrupting branch evaluation states.

---

## 3. Instruction Set Architecture (ISA)

The processor instruction word is formatted as:
```text
 8             7             4 3             0
+---------------+---------------+---------------+
|   imm_mode    |    opcode     |    operand    |
|    (1 bit)    |   (4 bit)     |    (4 bit)    |
+---------------+---------------+---------------+
```

Operand field decoding:
- **Register-Register Operations**: `operand = {Rd[1:0], Rs[1:0]}` (bits `[3:2]` select destination register, bits `[1:0]` select source register).
- **Immediate Operations (`MVI` / `LDI`)**: `imm_mode = 1`, `operand = imm[3:0]` (loads 4-bit immediate into accumulator `R0`).
- **Memory Addressing (`LOAD` / `STORE`)**: `operand = addr[3:0]` (4-bit RAM address).
- **Branch Operations (`JMP` / `JZ` / `JC` / `JN`)**: `operand = target[3:0]` (4-bit ROM address).
- **Single-Register Operations (`INC` / `DEC` / `OUT`)**: bits `[3:2]` or `[1:0]` select target register.

### Core Instruction Set Table

| Opcode | Mnemonic | Instruction Format | RTL Micro-operations | Affected Flags | Functional Description |
| :---: | :--- | :--- | :--- | :---: | :--- |
| `0000` | `NOP` | `NOP` | None | None | No operation; advances PC. |
| `0001` | `LOAD` | `LOAD addr` | `R0 <= DMEM[addr]` | None | Load 4-bit data from RAM address into accumulator R0. |
| `0010` | `STORE` | `STORE addr` | `DMEM[addr] <= R0` | None | Store accumulator R0 data into RAM address. |
| `0011` | `MOV` | `MOV Rd, Rs` | `R[Rd] <= R[Rs]` | None | Copy content of source register Rs to destination Rd. |
| `0011` | `MVI` | `MVI #imm4` (`LDI`) | `R0 <= imm4` | Z, N | Load 4-bit immediate constant into R0 (`imm_mode=1`). |
| `0100` | `ADD` | `ADD Rd, Rs` | `R[Rd] <= R[Rd] + R[Rs]` | Z, N, C | Add Rs to Rd; updates Zero, Negative, Carry. |
| `0101` | `SUB` | `SUB Rd, Rs` | `R[Rd] <= R[Rd] - R[Rs]` | Z, N, C | Subtract Rs from Rd; updates Zero, Negative, Carry. |
| `0110` | `AND` | `AND Rd, Rs` | `R[Rd] <= R[Rd] & R[Rs]` | Z, N | Bitwise logical AND between Rd and Rs. |
| `0111` | `OR` | `OR Rd, Rs` | `R[Rd] <= R[Rd] \| R[Rs]`| Z, N | Bitwise logical OR between Rd and Rs. |
| `1000` | `XOR` | `XOR Rd, Rs` | `R[Rd] <= R[Rd] ^ R[Rs]` | Z, N | Bitwise logical XOR between Rd and Rs. |
| `1001` | `INC` | `INC Rd` | `R[Rd] <= R[Rd] + 1` | Z, N, C | Increment destination register Rd by 1. |
| `1010` | `DEC` | `DEC Rd` | `R[Rd] <= R[Rd] - 1` | Z, N, C | Decrement destination register Rd by 1. |
| `1011` | `JMP` | `JMP addr` | `PC <= addr` | None | Unconditional jump to target ROM address. |
| `1100` | `JZ` | `JZ addr` | `PC <= (Z ? addr : PC+1)`| None | Conditional jump to target address if Zero flag is 1. |
| `1101` | `JN` / `JC` | `JN addr` | `PC <= (N ? addr : PC+1)`| None | Conditional jump if Negative (or Carry) condition is met. |
| `1110` | `OUT` | `OUT Rs` | `out_port <= R[Rs]` | None | Drive register data to CPU external output port. |
| `1111` | `HALT` | `HALT` | `halt <= 1; PC <= PC` | None | Freeze Program Counter and halt pipeline execution. |

*Extended microcode aliases supported via software toolchain:*
- `NOT Rd`: Implemented via `XOR Rd, R_all_ones` or `SUB R0, Rd`.
- `SHL Rd`: Implemented via `ADD Rd, Rd` (arithmetic/logical shift left by 1).
- `SHR Rd`: Implemented via software rotation and masking sequence.

---

## 4. Software Toolchain & Verification Infrastructure

### Custom 2-Pass Assembler (`tools/assembler.py`)
A self-contained Python assembler converts `.asm` source files into 9-bit hex representations compatible with Verilog `$readmemh`:
- **Pass 1**: Parses source files, strips comments, builds symbol tables for labels, and computes 4-bit PC addresses.
- **Pass 2**: Resolves forward and backward label references, validates operand bounds (`0` to `15`), packs instruction bits, and formats output `.hex` and `.mem` files.

```bash
# Assemble assembly source into hex image
python3 tools/assembler.py prog/fib.asm -o sim/fib.hex
```

### Cycle-Accurate Software Emulator (`tools/sim_cpu.py`)
A software reference model written in Python acts as an architectural oracle. It mirrors hardware register transitions, RAM state, output pins, and condition flags cycle-by-cycle:

```bash
# Execute behavioral emulation with execution trace
python3 tools/sim_cpu.py sim/mul.hex --trace
```

---

## 5. Verified Assembly Test Suites

Four verified application routines test the processor microarchitecture and flag evaluation:

| Benchmark | Source File | Algorithm Details | Expected Verified Output |
| :--- | :--- | :--- | :--- |
| **4-Bit Multiplication** | [`prog/mul.asm`](prog/mul.asm) | Software multiplication via repeated addition ($3 \times 4$) with zero-operand early-exit check | `out_port = 12 (0xC)`, `DMEM[12] = 12` |
| **Fibonacci Sequence** | [`prog/fib.asm`](prog/fib.asm) | Computes sequence terms ($F_n = F_{n-1} + F_{n-2}$) until 4-bit saturation ($N=1$ when value >= 8) | Output sequence: `1, 1, 2, 3, 5, 8` |
| **Memory Arithmetic** | [`prog/add.asm`](prog/add.asm) | Loads operands from RAM, computes sum, and writes result back ($5 + 7 = 12$) | `out_port = 12 (0xC)`, `DMEM[12] = 12` |
| **Flag Isolation Test** | [`prog/flag_test.asm`](prog/flag_test.asm) | Interleaves a non-flag-modifying `MOV` between `DEC` ($Z=1$) and `JZ` target jump | Verified flag persistence across non-ALU operations |

---

## 6. Synopsys 32nm Commercial ASIC Implementation Flow

The design includes automation scripts targeting the Synopsys SAED 32nm standard cell library:

```text
  +-----------------------+
  | Verilog-2001 Core RTL |
  +-----------+-----------+
              |
              v
  +-----------------------+      +-----------------------+
  | Functional Simulation | ---> | VCS / Icarus Verilog  |
  +-----------+-----------+      +-----------------------+
              |
              v
  +-----------------------+      +-----------------------+
  |   Logic Synthesis     | <--- | SDC Constraints       |
  | (Design Compiler)     |      | (100 MHz, I/O delays) |
  +-----------+-----------+      +-----------------------+
              |
              +--------------------------+
              |                          |
              v                          v
  +-----------------------+  +-----------------------+
  | Formal LEC (Stage 1)  |  |   Physical Design     |
  | Synopsys Formality    |  | (IC Compiler II)      |
  | (RTL vs. DC Netlist)  |  +-----------+-----------+
  +-----------------------+              |
                                         v
                             +-----------------------+
                             | Formal LEC (Stage 2)  |
                             | Synopsys Formality    |
                             | (DC vs. ICC2 Netlist) |
                             +-----------+-----------+
                                         |
                                         v
                             +-----------------------+
                             | Final Tape-Out GDSII  |
                             | (`output/cpu4.gds`)   |
                             +-----------------------+
```

### 1. SDC Timing Constraints (`cons/cpu4.sdc`)
- **Clock Definition**: 100 MHz operating target (`period 10.0ns`) on port `clk`.
- **Clock Quality**: 0.2 ns clock uncertainty, 0.1 ns clock transition.
- **Port Budgeting**: 2.0 ns input delay, 2.0 ns output delay relative to clock edge.
- **Drive and Load**: Input transition driven by `INVX1_RVT` library cell, 0.05 pF output capacitive load.
- **False Paths**: Asynchronous reset line `rst_n` marked as false path for static timing analysis.

### 2. Logic Synthesis (`syn/run_dc.tcl`)
- Tool: Synopsys Design Compiler (`dc_shell`).
- Target Library: `saed32rvt_tt1p05v25c.db` (Nominal 1.05V, 25 deg C).
- Optimization: `compile_ultra` with boundary optimization and auto-uniquification.
- Artifacts: Gate-level netlist (`output/design_mapped.v`), synthesized SDC constraints, and timing/area/power reports.

### 3. Formal Verification (`Formal/`)
Two verification suites eliminate functional discrepancies introduced during translation:
- **RTL vs. Synthesis Gate Netlist** ([`Formal/RTL_vs_Gate/verify_rtl_gate.fms`](Formal/RTL_vs_Gate/verify_rtl_gate.fms)): Verifies that logic synthesis preserves the original RTL behavior.
- **Synthesis Netlist vs. Post-PnR Netlist** ([`Formal/Post_PnR/verify_post_pnr.fms`](Formal/Post_PnR/verify_post_pnr.fms)): Verifies that clock tree insertion, physical cell legalization, and optimization steps do not alter functionality.

### 4. Physical Design and Place & Route (`PnR/run_icc2.tcl`)
- Tool: Synopsys IC Compiler II (`icc2_shell`).
- Floorplanning: 60% core utilization with 5 um core margins.
- Power Grid Network ([`PnR/scripts/power.tcl`](PnR/scripts/power.tcl)): Power and ground rings on top metal layers (M8/M9) with regular vertical and horizontal straps to minimize IR drop.
- Placement & Legalization: `place_opt` for timing-driven placement, congestion mitigation, and high-fanout net synthesis.
- Clock Tree Synthesis (CTS): Target skew <= 50 ps with Non-Default Routing ([`PnR/scripts/ndr.tcl`](PnR/scripts/ndr.tcl)) shielding for clock nets.
- Detailed Routing & Sign-off: Antenna prevention routing, automatic filler cell insertion (`SHFILL*`), layout versus schematic (LVS) verification, parasitic extraction (`cpu4.spef`), and GDSII export (`cpu4.gds`).

---

## 7. FPGA Prototyping & Board Deployment

Hardware validation is provided for Intel FPGA development boards (Terasic DE10-Lite / Cyclone V hardware platforms):

- **Target FPGA**: Intel MAX 10 (10M50DAF484C7G) / Cyclone V SE (5CSXFC6D6F31C6).
- **Top-Level Wrappers**: [`real/cpu_top_fpga.v`](real/cpu_top_fpga.v) and [`real/cpu4_de10.v`](real/cpu4_de10.v).
- **Clock Management**:
  - 50 MHz onboard oscillator input (`CLOCK_50`).
  - Frequency divider generating 1 Hz clock for visible step-by-step program inspection.
  - Hardware button debouncer on `KEY[1]` for manual single-step execution.
  - Toggle switch `SW[0]` to select between automatic 1 Hz execution and manual step mode.
- **Board Peripherals**:
  - `HEX0`: Decodes 4-bit `out_port` onto 7-segment display.
  - `HEX1`: Decodes accumulator `R0` content onto 7-segment display.
  - `LEDR[3:0]`: Real-time status of `out_port` data bus.
  - `LEDR[4]`: CPU execution halt status.
  - `LEDR[8:5]`: Real-time status of debug `R0` bus.
  - `LEDR[9]`: Current CPU clock toggle state.

---

## 8. Quickstart & Simulation Guide

### Dependencies
- **Simulation**: Icarus Verilog (`iverilog`, `vvp`) and GTKWave.
- **Software**: Python 3.8+.
- **EDA Suites (Optional)**: Synopsys VCS, Design Compiler, Formality, IC Compiler II, Intel Quartus Prime Lite.

```bash
# Ubuntu / Debian package installation
sudo apt-get update && sudo apt-get install -y iverilog gtkwave python3 build-essential
```

### Simulation Commands

```bash
# 1. Run full CPU regression test suite across all 4 programs
make test

# 2. Run ALU unit verification (14 corner cases including overflow and borrow)
make alu

# 3. Run Python cycle-accurate golden reference model
make pysim

# 4. Re-assemble all assembly test programs
make asm

# 5. Open simulation waveform in GTKWave
make wave

# 6. Clean generated test files
make clean
```

### Regression Verification Log (`make test`)

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

## 9. Project Directory Structure

```text
.
├── cons/
│   └── cpu4.sdc                    # Synopsys SDC timing constraints (100 MHz, I/O delays)
├── docs/
│   ├── isa.md                      # Complete ISA specification and control matrix
│   ├── setup.md                    # Toolchain setup and environment manual
│   └── audit-report.md             # Microarchitecture verification report
├── Formal/
│   ├── RTL_vs_Gate/
│   │   └── verify_rtl_gate.fms     # Synopsys Formality LEC: RTL vs Synthesis Netlist
│   └── Post_PnR/
│       └── verify_post_pnr.fms     # Synopsys Formality LEC: DC Netlist vs ICC2 Netlist
├── imem/
│   ├── instruction_memory_sim.v    # Parameterized ROM model for RTL simulation
│   └── instruction_memory_rom.v    # Synthesizable case-statement ROM for ASIC flow
├── PnR/
│   ├── run_icc2.tcl                # Synopsys IC Compiler II physical design recipe
│   └── scripts/
│       ├── power.tcl               # Power ring and strap generation script
│       └── ndr.tcl                 # Non-Default Routing rules for CTS clock shielding
├── prog/
│   ├── add.asm                     # Assembly program: memory addition
│   ├── fib.asm                     # Assembly program: Fibonacci sequence calculation
│   ├── flag_test.asm               # Assembly program: conditional flag isolation test
│   └── mul.asm                     # Assembly program: 4-bit software multiplication
├── real/
│   ├── cpu_top_fpga.v              # FPGA top-level wrapper with debouncer and display
│   ├── cpu4_de10.v                 # Alternative DE10 pinout interface module
│   ├── cpu_top_fpga.qsf            # Quartus Prime board pin assignments
│   └── output_files/
│       └── cpu_top_fpga.sof        # Compiled Intel FPGA bitstream file
├── report_assets/
│   ├── alu_schematic.svg           # Gate-level schematic of the 4-bit ALU
│   ├── cpu_top_schematic.svg       # Full processor datapath interconnect diagram
│   ├── gate_level_schematic.svg    # Synthesized gate-level netlist schematic
│   ├── anhGDS.jpg                  # Post-routing layout capture (GDSII preview)
│   └── waveform_*.png              # Annotated simulation waveforms
├── rtl/
│   ├── alu_4bit.v                  # 4-bit 8-operation Arithmetic Logic Unit
│   ├── control_unit.v              # Opcode decoder and flag latch control logic
│   ├── cpu_top.v                   # Microprocessor top-level datapath module
│   ├── data_memory.v               # 16x4-bit synchronous RAM (DMEM)
│   ├── instruction_memory.v        # Default instruction ROM wrapper
│   ├── program_counter.v           # 4-bit Program Counter with halt freeze logic
│   └── register_file.v             # 4x4-bit dual-read single-write register bank
├── sim/
│   ├── prog.hex, fib.hex, mul.hex  # 9-bit assembled machine code images
│   ├── gate_level_netlist.v        # Synthesized gate netlist
│   └── yosys_script.ys             # Open-source gate synthesis script
├── syn/
│   └── run_dc.tcl                  # Synopsys Design Compiler synthesis flow (SAED 32nm)
├── tb/
│   ├── tb_alu_4bit.v               # Exhaustive ALU unit testbench (14 boundary cases)
│   └── tb_cpu_top.v                # End-to-end self-checking system regression testbench
├── tools/
│   ├── assembler.py                # Custom 2-pass Python assembler
│   ├── sim_cpu.py                  # Cycle-accurate golden Python CPU emulator
│   └── synth.ys                    # Open-source synthesis definition
├── .gitignore                      # Clean ignore rules for simulation dumps and EDA caches
├── LICENSE                         # MIT License
├── Makefile                        # Project simulation and build driver
└── README.md                       # Main technical documentation
```

---

## 10. Author & Contact

**Le Ngoc Tuong**  
Faculty of Electrical and Electronics Engineering  
Ho Chi Minh City University of Technology and Education (HCMUTE)  
GitHub: [@lengoctuong2005](https://github.com/lengoctuong2005)  
Email: [lengoctuong.work@gmail.com](mailto:lengoctuong.work@gmail.com)

---

## 11. License

This project is open-source under the terms of the [MIT License](LICENSE).
