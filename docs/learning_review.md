# CPU4 learning material — technical correction checklist

This review covers all ten pages and fifteen interview questions of the supplied
CPU4_LEARNING_ROADMAP.pdf. It is not a company-certified syllabus.

## Flags and architecture

No ISA-independent rule requires four flags. Z/N/C/V is common, not universal.
ISA v1 stores Z/N only; carry is combinational in the ALU, not architectural.
Carry for SUB uses no-borrow. JN tests result[3], not general signed less-than.
For 4-bit SUB, signed comparison conventionally uses N XOR V; V is absent in v1.
Example: 7−(−8)=15 wraps to 1111: N=1, V=1, N XOR V=0. JN taking the branch is
correct JN behavior, but interpreting it as 7<−8 is wrong. ADD/SUB wrap modulo16.
Flags must be defined per instruction; logical C/V update policy is not universal.

Harvard lets instruction/data widths differ and avoids a shared-memory structural
conflict; it does not remove every hazard. "Bus contention" in the electrical
multiple-driver sense is not the correct explanation here. Bit8 is not a global
immediate mode. Four opcode bits mean sixteen opcode values, not necessarily
sixteen instruction names (MOV/LDI share opcode3). RF async read has nonzero delay.
LOAD/LDI using R0 is an ISA choice, not a universal 4-bit CPU rule.

## RTL and measurement

`flag_write` is a functional repair, not evidence of a timing optimization.
Do not call the ripple-carry ALU the measured critical path without STA. LOAD,
branch/control, MUX and net delay may dominate. For a 4-bit adder CLA benefits
are technology-dependent, and synthesis maps `+` according to its libraries.
Pipeline changes require hazard/control verification, not only a timing claim.

A constant ROM is generally combinational logic/IP, not automatically flip-flops.
16×4 RAM needs 64 storage bits if FF-mapped, but final cell counts can change.
The original generic ROM was initialized to NOP and loaded only in a simulation
helper. The patch supplies a constant synthesizable Fibonacci boot image and
checks it against assembled source; boot without helper loading is simulated.
RAM initialization remains a simulation/FPGA contract; CPU reset preserves RAM.
There is no ASIC power-up-zero guarantee from `initial`.

## STA and exceptions

For same-clock, same-edge, single-cycle paths with skew=K−L:

- setup slack = T + skew − tcq_max − Dmax − tsetup − Usetup;
- hold slack = tcq_min + Dmin − skew − thold − Uhold.

Positive skew helps setup and hurts hold on that path. Delaying clock at B in
A→B→C helps setup A→B, hurts hold A→B, and hurts setup B→C. LVT/upsizing can
reduce both min and max delay, so every ECO needs setup/hold/DRV rechecks.
Hold normally cannot be fixed by lowering frequency; "always scrap the chip"
is too absolute. Voltage workarounds must stay within reliability limits.

A same-clock multicycle setup2/hold1 example restores hold to the original
same-launch-edge relation, not "cycle1". There must be a real enable/protocol;
other clock relationships require explicit edge analysis. CPU4 is single-cycle.
Do not false-path all asynchronous reset: recovery/removal for deassertion and
pulse-width constraints remain relevant. CDC exceptions do not construct safe
hardware; single-bit controls and coherent buses/pulses need different protocols.
Gray-pointer FIFO routing may need max delay/bus-skew limits. In Vivado, blanket
clock groups override max-delay: inspect exception precedence/coverage.

## PVT, variation, SI and PDN

Cold often increases mobility and |Vth| simultaneously; at low Vdd, increased
threshold can dominate and make cold slower. Temperature inversion is not tied
to a hard <28nm cutoff. Use characterized PVT/RC/mode corners rather than a
universal SS/hot setup and FF/cold hold formula. Synopsys uses POCV, LVF supplies
variation data; "all AI chips require SOCV" is unsupported. Correlated/systematic
variation does not disappear by averaging logic stages. Include MCMM and CPPR.

Crosstalk effects depend on timing windows and driver/slew; not every glitch
causes failure. IR=I×R differs from inductive supply droop L×di/dt. AI activity
can create large peaks but does not imply exponential current growth. Decap
is not a universal solution for static IR. Verify EM separately.

## Physical design, memory IP and scripts

Use PDK-qualified tap/endcap rules, post-CTS hold repair, route extraction/SPEF,
post-route STA and final ECO rechecks. Metal stack, tap names, utilization and
macro placement are PDK/flow-dependent; neither M1–M6 nor die-edge SRAM placement
is mandatory. SRAM MBIST/repair is an IP/DFT option, not automatic. Synchronous
SRAM may change CPU read latency. Foundry/library views and qualified decks matter.

Antenna damage relates to plasma processing such as etch, not photolithography
alone. Clock cells are characterized, not perfectly symmetric by definition.
LVS is connectivity/device matching, not necessarily literal one-to-one cell
comparison. GDS export and in-tool connectivity checks are not full foundry signoff.
Liberty contains more than two-dimensional delay tables; CCS is not just NLDM
under another name. Include sequential timing arcs, pulse-width checks, power,
limits and variation. .lib does not replace SPEF/LEF/GDS.

Do not assume `num_pins` is a PrimeTime fanout attribute; use tool help and
`list_attributes`. Diagnose max capacitance via constraints/load reports, not
only fanout count. Verify units and Vt naming. Tcl APIs differ across tools.
ASIC PnR script late=max/early=min assignment is repaired, but unrun vendor
scripts and incomplete PDK tap/signoff setup remain explicitly unverified.

## Evidence policy

All measured claims live in verification_2026-10-08.md and generated test logs.
Historical reports/presentations are not current verification evidence. No FPT
job-specific requirement is asserted without the actual JD. Educational
one-corner cell-delay STA is not post-route MCMM/SI/IR signoff or measured Fmax.
