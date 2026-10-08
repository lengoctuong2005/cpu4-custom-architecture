# Executed verification audit — 2026-10-08

Baseline: `5f2e19d687a3b77410542dc3828f8fbe8a98f3bd`.
Patch branch: `audit/cpu4-v1-verified-2026-10-08`.
[Pull request #1](https://github.com/lengoctuong2005/cpu4-custom-architecture/pull/1).
RTL/test source commit: `1ed737eec51ea5223f9868a485b161d9b44c97b6`;
subsequent commits update publication metadata/PDF layout, not tested RTL. See
[metrics](verification_metrics.json), [source hashes](verification_source_manifest.json),
and [technical learning corrections](learning_review.md).

## Outcome

Local `make verify` and `make synth` completed successfully. This means the
specified functional tests and generic synthesis passed, **not** that GitHub
Actions has run, FPGA boards were validated, or an ASIC has been signed off.
The baseline's existing demo/ALU tests already passed; this audit does not claim
that the original arithmetic core was broken.

| Check | Measured result |
|---|---|
| Baseline and final demos | ADD/MUL/FIB/FLAG PASS; full FIB sequence 1,1,2,3,5,8 |
| Module unit benches | PC/RF/control/RAM PASS |
| RTL ALU | 14 directed + 2,048 exhaustive = 2,062 checks PASS |
| Python tests | 10 test methods PASS; all 256 ADD/256 MUL input pairs, parser/HEX failures, reset/HALT/timeout |
| Decoder | 512 words ×4 flag combinations =2,048 combinations PASS |
| Differential CPU | 2,767 scenarios /79,324 compared edges PASS; PC, RF, Z/N, OUT, all RAM, HALT |
| Raw single-instruction CPU | All512 raw words ×4 initial flag combinations within differential suite |
| Random CPU | 200 deterministic seeds0..199, 128 edges each; final suite includes enable/stall patterns |
| Boot/FPGA logic | Default ROM boot; reset, bounce, press/hold/mode/auto PASS (simulation only) |
| Strict-net core | Default-nettype-none elaboration PASS; original3 implicit-net warnings fixed |
| Negative mutants | XOR→OR and unconditional flags detected; both vvp exit1 |
| Learning C/V formulas | 512 arithmetic cases +2,560 comparison assertions PASS; V is not implemented in v1 |
| Formal ALU | 7 output-bit equivalences proved, 0 unproven; native Yosys0.40 and WASM0.69 |
| Generic synthesis | PASS with artifact/check assertion; hierarchy top49 cells, not physical total |
| Nangate45 mapping | PASS;361 standard cells,65 FF (40 DFF +25 DFFR), cell-area sum646.646 library units |
| Gate/reference interface | Before/after ECO100 edges each PASS; OUT/debug_r0/HALT with enables/stalls; no SDF |

## Actual reproduced failures and repairs

- Tabs and label/comment forms fail in the old assembler. Normalize comments
  and whitespace before both passes; inline labels supported, strict validation.
- Old HEX reader counts physical lines, so comments/blanks shift program words.
  It also silently masks an overwide word `200` to `000`. New reader validates
  capacity/syntax/range and uses instruction count.
- Old emulator turns timeout into HALT and prints architectural C absent in RTL.
  New model has only Z/N and raises TimeoutError with nonzero CLI exit.
- Default generic ROM contains only NOP; flatten synthesis yields **no functional
  cells** (WASM adds six scope-info metadata cells). New boot ROM contains FIB,
  is checked against assembled source and tested without helper loading.
- Add synchronous `clk_en` to every architectural side effect. Connect high for
  free-running cores; FPGA uses one CLOCK_50 domain plus synchronized/debounced
  inputs and enable pulses. Legacy wrapper delegates to the canonical one.
- Missing program files now trigger `$fatal`; loading a short program first
  clears the simulation ROM so no prior program words remain.
- Correct ICC2 late/max and early/min RC association; do not pretend a filler
  is a validated well-tap. Vendor flow templates still need qualified PDK work.
- Synthesis mapping initially failed `check -assert` because library cells had
  not been loaded as definitions. Adding `read_liberty -lib` fixes the flow;
  initial failure logs are retained. Artifact presence is checked explicitly.

## Educational STA — finding, not blanket PASS

Library: external Nangate45 TT (nominal1.10V,25°C), **not SAED32**. Time1ns,
capacitance1fF. Ideal clock10ns, setup uncertainty0.2ns/hold0.05ns; I/O max1ns,
min0.1ns; input transition0.1ns; output load10fF. No SPEF, routing or CTS.

Before ECO:
- Worst max-delay slack **+8.39ns**, max TNS0.
- Worst min-delay slack **−0.26ns**, specifically `rst_n` **removal**, not data hold.
-1 max-slew and3 max-cap violations: instances `_459_`, `_460_`, `_461_`.

Netlist-copy experiment: NOR3_X1→NOR3_X4, NOR4_X1→NOR4_X4,
AOI221_X1→AOI221_X4. After re-running STA:
- Worst max slack **+8.38ns** (upsizing does not guarantee every path improves).
- No slew/cap/pulse violations reported in this constrained educational run.
- Aggregate min remains **−0.26ns reset removal**. Reported FF/data min paths
  have lowest slack **+0.05ns**. Reset timing is not closed and is **not hidden**
  with a blanket false path. Real release protocol/constraints and physical
  recovery/removal must be resolved in the qualified implementation environment.
- Gate/reference100-edge public-interface tests PASS before and after ECO.

Do not label +8.38ns positive worst slack as measured silicon Fmax or SAED32
performance. Fixed-program ROM can specialize away unused datapath/state.
The first worst max path is a PC-flop/ROM-decode path to HALT output, not proof
that LOAD or ALU dominates the generic CPU. Mapping/import warnings include
legacy translate_off and unsupported unused scan/gating models; used gate-cell
models are verified present before simulation.

## Reproduce

```sh
make verify
make synth
LIBERTY=/path/to/NangateOpenCellLibrary_typical.lib python tests/run_synthesis.py
LIBERTY=/path/to/NangateOpenCellLibrary_typical.lib sta -exit tools/sta_educational.tcl
LIBERTY=/path/to/NangateOpenCellLibrary_typical.lib python tests/gate_smoke.py
python tests/educational_eco.py --input build/synthesis/cpu_top_mapped.v \
  --output build/synthesis/cpu_top_eco.v --liberty /path/to/library.lib \
  --resize _459_=NOR3_X4 --resize _460_=NOR4_X4 --resize _461_=AOI221_X4
LIBERTY=/path/to/library.lib NETLIST=build/synthesis/cpu_top_eco.v \
  sta -exit tools/sta_educational.tcl
LIBERTY=/path/to/library.lib NETLIST=build/synthesis/cpu_top_eco.v \
  python tests/gate_smoke.py
pip install -r requirements-docs.txt
python tools/build_learning_pdf.py
```

ECO instance names belong to the recorded mapping; if mapping changes, inspect
STA anew rather than copying these names. External library URL and SHA256 are
in the metrics/evidence package; comply with its upstream license. No external
library/PDK data is redistributed by this patch.

## Remaining BLOCKED / NOT RUN

- Quartus compilation/TimeQuest/bitstream/board tests; pin maps not newly validated.
- Synopsys DC, PrimeTime, Formality full CPU, ICC2 with licensed qualified SAED32.
- ASIC RAM power-up/boot/reset strategy; approved tap/endcap insertion, DFT/MBIST.
- Post-route SPEF, MCMM/variation/SI, propagated clocks, physical hold closure,
  IR/EM, foundry DRC/LVS/ERC/density/antenna and tapeout packaging.
- Job-specific FPT requirements without the actual JD.

A complete learning/audit PDF is deliverable; a fabricated/signoff-certified
chip is not. Historical reports and slide decks remain legacy, unverified
artifacts until regenerated against this maintained source/evidence.
