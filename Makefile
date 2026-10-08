# ─────────────────────────────────────────────────────────────
# Makefile — CPU 4-bit (TKVM) simulation
# Tools: Icarus Verilog (iverilog + vvp) + GTKWave, Python 3.
#
#   make            compile + run the full-CPU testbench
#   make alu        compile + run the ALU unit testbench
#   make unit       run unit testbenches for all CPU submodules
#   make test       run BOTH RTL testbenches (CPU + ALU)
#   make verify     complete pipeline: asm + unit + test + pysim
#   make wave       open the CPU waveform in GTKWave
#   make wave-alu   open the ALU waveform in GTKWave
#   make asm        (re)assemble prog/*.asm -> sim/*.hex
#   make pysim      run the Python reference model on all demos
#   make clean      delete generated files
#
# Cross-platform: `clean` picks the right delete command on Windows vs Unix.
# ─────────────────────────────────────────────────────────────

IVERILOG = iverilog -g2012
VVP      = vvp
GTKWAVE  = gtkwave
PYTHON   = python3

# Full-CPU testbench
OUT      = cpu_tb.out
VCD      = cpu_top.vcd
CPU_SRC  = tb/tb_cpu_top.v \
           rtl/alu_4bit.v rtl/control_unit.v rtl/cpu_top.v \
           rtl/data_memory.v rtl/instruction_memory.v rtl/program_counter.v \
           rtl/register_file.v

# ALU unit testbench
ALU_OUT  = alu_tb.out
ALU_VCD  = tb_alu_4bit.vcd
ALU_SRC  = tb/tb_alu_4bit.v rtl/alu_4bit.v

# Unit testbenches
UNIT_PC_OUT = unit_pc_tb.out
UNIT_RF_OUT = unit_rf_tb.out
UNIT_CU_OUT = unit_cu_tb.out
UNIT_DM_OUT = unit_dm_tb.out

.PHONY: all compile run test alu unit verify synth learning-flags software extra differential mutation wave wave-alu asm pysim clean sim

all: run
sim: run

synth:
	mkdir -p build/synthesis
	yosys -l build/synthesis/yosys.log tools/synth.ys

compile:
	$(IVERILOG) -o $(OUT) $(CPU_SRC)

run: compile
	$(VVP) $(OUT)

alu:
	$(IVERILOG) -o $(ALU_OUT) $(ALU_SRC)
	$(VVP) $(ALU_OUT)

unit:
	$(IVERILOG) -o $(UNIT_PC_OUT) tb/unit/tb_program_counter.v rtl/program_counter.v
	$(VVP) $(UNIT_PC_OUT)
	$(IVERILOG) -o $(UNIT_RF_OUT) tb/unit/tb_register_file.v rtl/register_file.v
	$(VVP) $(UNIT_RF_OUT)
	$(IVERILOG) -o $(UNIT_CU_OUT) tb/unit/tb_control_unit.v rtl/control_unit.v
	$(VVP) $(UNIT_CU_OUT)
	$(IVERILOG) -o $(UNIT_DM_OUT) tb/unit/tb_data_memory.v rtl/data_memory.v
	$(VVP) $(UNIT_DM_OUT)

test: run alu

verify: asm unit test pysim software extra differential mutation learning-flags

wave: run
	$(GTKWAVE) $(VCD)

wave-alu: alu
	$(GTKWAVE) $(ALU_VCD)

asm:
	$(PYTHON) tools/assembler.py prog/add.asm -o sim/prog.hex
	$(PYTHON) tools/assembler.py prog/mul.asm -o sim/mul.hex
	$(PYTHON) tools/assembler.py prog/fib.asm -o sim/fib.hex
	$(PYTHON) tools/assembler.py prog/flag_test.asm -o sim/flag_test.hex

pysim:
	$(PYTHON) tools/sim_cpu.py sim/prog.hex --ram 10=5,11=7
	$(PYTHON) tools/sim_cpu.py sim/mul.hex  --ram 10=3,11=4
	$(PYTHON) tools/sim_cpu.py sim/fib.hex
	$(PYTHON) tools/sim_cpu.py sim/flag_test.hex

CLEANFILES = $(OUT) $(VCD) $(ALU_OUT) $(ALU_VCD) $(UNIT_PC_OUT) $(UNIT_RF_OUT) $(UNIT_CU_OUT) $(UNIT_DM_OUT) sim/cpu_sim sim/alu_sim sim/cpu_top.vcd

clean:
ifeq ($(OS),Windows_NT)
	-del /Q /F $(CLEANFILES) 2>NUL
else
	-rm -f $(CLEANFILES)
endif

# Deterministic deep verification. Any mismatch/nonzero command fails make.
software:
	$(PYTHON) -m unittest discover -s tests -v

extra:
	$(PYTHON) tests/run_extra_rtl.py

differential:
	$(PYTHON) tests/differential.py

mutation:
	$(PYTHON) tests/mutation_smoke.py

learning-flags:
	mkdir -p build/verification
	$(PYTHON) tests/flags_math.py
