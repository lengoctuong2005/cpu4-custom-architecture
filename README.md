# CPU4 — verified 4-bit Harvard CPU learning project

CPU4 v1 is a single-cycle, 4-bit Harvard CPU with a 9-bit instruction word,
16-word boot ROM, 16-nibble data RAM, four registers, and **two architectural
flags: Z and N**. The ALU also computes an **internal combinational carry**;
that signal is not a CPU status register, and v1 has no JC/ADC/V instructions.

This repository includes RTL, a strict assembler, a cycle-stepped reference
model, reproducible tests, FPGA wrappers, and **ASIC flow templates**.
It is not evidence of fabricated silicon, completed SAED32 signoff, or tested
Cyclone V/MAX 10 boards. See [verification evidence](docs/verification_2026-10-08.md).

## Quick start

Required: Python 3.10+, Icarus Verilog with SystemVerilog-2012 support, make.
Optional: native Yosys/ABC for synthesis; OpenSTA and a compatible Liberty file
for the educational STA experiment. Do not substitute a successful exit code
for checking that all expected artifacts/reports exist.

```sh
make verify   # assemble + module tests + ALU + demos + Python + extra + differential + mutations
make synth    # generic synthesis and check; not PDK signoff
```

`make verify` fails on mismatches. CI additionally compares regenerated demo HEX
files to the tracked files and uploads evidence from `build/`.

## Architecture and interface

| Item | CPU4 v1 |
|---|---|
| Core top | `cpu_top` |
| Language | SystemVerilog-2012; existing `.v` files must be read in SV mode |
| Inputs | `clk`, asynchronous active-low `rst_n`, synchronous `clk_en` |
| Outputs | `out_port[3:0]`, `halt_out`, `debug_r0[3:0]` |
| Registers | R0–R3, each 4-bit; async read/sync write |
| PC | 4-bit, modulo 16; reset to 0; stable on HALT or `clk_en=0` |
| Flags | Registered Z/N; reset both to 0; conditional `flag_write` |
| ROM | 16×9, async read; default synthesizable constant Fibonacci program |
| RAM | 16×4, async read/sync write; CPU reset does not clear RAM |
| OUT | Registered 4-bit value; updated only by enabled OUT instruction |

**Interface change in the verification patch:** connect `clk_en=1'b1` for a
free-running core. It gates every architectural write, not the physical clock.
FPGA wrappers use CLOCK_50 directly plus instruction-enable pulses.

RAM `initial` initialization/preload is a simulation/FPGA contract, not a claim
that ASIC SRAM/FF powers up at zero. ASIC implementation needs explicit boot,
reset, valid-bit initialization or a qualified memory IP. Testbench helper tasks
are excluded from synthesis. ROM contents used in hardware must be present
at synthesis; a `$readmemh` call in a simulation-only task does not load hardware.

## ISA and encoding

`imm_mode[8] | opcode[7:4] | operand[3:0]`.
Bit8 distinguishes MOV/LDI at opcode 3; it is not a universal immediate mode.
Other ignored fields have their RTL-defined behavior; assembler emits canonical
encodings only. `tools/isa.py` is the shared Python encoding/ALU specification.

| Opcode | Instruction | Operand | Flags |
|---|---|---|---|
| 0 | NOP | none | preserve |
| 1 / 2 | LOAD / STORE | address 0..15; implicit R0 | preserve |
| 3, bit8=0 | MOV Rd,Rs | `{Rd,Rs}` | preserve |
| 3, bit8=1 | LDI #imm | nibble; implicit R0 | Z,N |
| 4 / 5 | ADD / SUB Rd,Rs | `{Rd,Rs}` | Z,N |
| 6 / 7 / 8 | AND / OR / XOR Rd,Rs | `{Rd,Rs}` | Z,N |
| 9 / A | INC / DEC Rd | `{Rd,00}` | Z,N |
| B / C / D | JMP / JZ / JN | absolute ROM address | preserve |
| E | OUT Rs | `{00,Rs}` | preserve |
| F | HALT | none | preserve |

Z is result==0; N is result bit3. JN tests N, **not general signed less-than**:
7−(−8) wraps to `1111`, N=1 despite 7 being greater than −8. A conventional
signed SUB comparison uses N XOR V; v1 does not implement V.

The internal ALU carry is 1 for ADD carry-out and for SUB/DEC **no borrow**.
Logical/PASS ALU operations produce internal C=0. There is no saved C in the
architectural emulator. Arithmetic wraps modulo 16.

Assembler accepts spaces/tabs, `;` or `//` comments, and `label:` optionally
before an instruction. Labels are case-sensitive. It rejects oversized programs,
duplicate/unknown labels, invalid operands, unsupported mnemonics and addresses.
The HEX reader validates 9-bit words and capacity instead of silently truncating.
Simulator timeout is a nonzero error, never a successful HALT.

## Verification layers

- Four module unit testbenches (PC, register file, decoder, RAM).
- 14 directed + 2,048 exhaustive ALU vectors; independent integer oracle.
- ADD/MUL/Fibonacci/flag-preservation RTL demos and full Fibonacci OUT sequence.
- 10 Python test methods including all 512 raw decodings, HEX/parser failures,
  timeout exit semantics, all 256 ADD and 256 MUL inputs, and boot-ROM consistency.
- 2,048 instruction/flag decoder combinations.
- Default boot-ROM execution without testbench program loading.
- Single-clock FPGA logic tests: reset, bounce, one instruction per press,
  held-button suppression, mode change, automatic boot; not board validation.
- Differential comparison of PC, R0–R3, Z/N, OUT, every RAM nibble and HALT on
  79,324 sampled edges across 2,767 scenarios. Includes all 512 raw words × four
  initial flag states, all ADD/MUL nibble input pairs, directed programs,
  PC wrap, 200 deterministic random seeds and enabled/stalled cycles.
- Two intentionally faulty **temporary copies** must fail tests: XOR→OR and
  unconditional flag writes. Mutated source never replaces tracked RTL.

Hierarchical arbitrary-state injection is testbench-only and expands behavioral
coverage; it does not prove every possible program/hardware trajectory. The
Python reference shares the ISA module, so separate integer ALU checks and
directed expectations are retained to reduce correlated-model errors.

## FPGA scope

`real/cpu_top_fpga.v` is the canonical Cyclone V wrapper. It synchronizes reset
release, button and mode signals, debounces the button, and generates `clk_en`
pulses. No pushbutton/divided clock is used as the CPU clock. `cpu4_de10` delegates
to this implementation. The QSFs include source assignments; `cpu_top_fpga.sdc`
is intentionally incomplete for board signoff. Verify I/O timing, synchronizer
recognition, recovery/removal and all TimeQuest paths in Quartus.

No Quartus compile/timing report, bitstream or physical board test was produced
by the 2026-10-08 audit. Existing pin maps are not newly validated. MAX 10 is not
an audited target. Simulator pass does not substitute for FPGA timing closure.

## ASIC and timing scope

Synopsys scripts target `cpu_top` and require licensed DC/Formality/ICC2 plus
qualified SAED32 assets. They remain **templates, not a completed ASIC flow**.
The patch corrects late/max vs early/min RC association and stops identifying an
arbitrary filler as a well-tap cell. PDK-approved taps/endcaps, MCMM libraries,
reset strategy, formal setup/SVF, DFT, PDN/EM/IR, extracted STA and foundry
DRC/LVS decks still require validation in the real tool environment.

`cons/cpu_top.sdc` is an I/O timing template with min/max values. It does not
blanket-false-path reset. Finish reset synchronization/release constraints and
check recovery/removal; numbers/library cell names are not board/system specs.
100 MHz is a target in this template, not a silicon performance guarantee.

The optional [educational STA script](tools/sta_educational.tcl) uses externally
supplied Liberty data. No SPEF/layout, CTS, multi-corner variation/SI or IR analysis
is implied. A clean generic synthesis or one-corner STA does not prove signoff.

## Documentation policy

- [ISA](docs/isa.md), [audit evidence](docs/verification_2026-10-08.md), and
  [learning corrections](docs/learning_review.md) are the maintained sources.
- The learning PDF supplied with this audit combines corrected lessons with
  measured results and explicit BLOCKED/NOT RUN items.
- Historical `Bao_cao_CPU_4bit.*`, presentations and layout images are not
  regenerated by this patch and **must not be used as current verified evidence**.
  A screenshot or prewritten PASS banner is not proof of a reproducible flow.
- PDK/library and large generated artifacts are not redistributed as source.

## License

Project code uses MIT as recorded in LICENSE. External technology libraries,
EDA tools and historical reference documents have their own licenses.
