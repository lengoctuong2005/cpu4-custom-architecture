# ─────────────────────────────────────────────────────────────
# Makefile — CPU 4-bit (TKVM) simulation
# Tools: Icarus Verilog (iverilog + vvp) + GTKWave, Python 3.
#
#   make            compile + run the full-CPU testbench
#   make alu        compile + run the ALU unit testbench
#   make test       run BOTH RTL testbenches (CPU + ALU)
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

.PHONY: all compile run test alu wave wave-alu asm pysim clean

all: run

compile:
	$(IVERILOG) -o $(OUT) $(CPU_SRC)

run: compile
	$(VVP) $(OUT)

alu:
	$(IVERILOG) -o $(ALU_OUT) $(ALU_SRC)
	$(VVP) $(ALU_OUT)

test: run alu

wave: run
	$(GTKWAVE) $(VCD)

wave-alu: alu
	$(GTKWAVE) $(ALU_VCD)

asm:
	$(PYTHON) tools/assembler.py prog/add.asm -o sim/prog.hex
	$(PYTHON) tools/assembler.py prog/mul.asm -o sim/mul.hex
	$(PYTHON) tools/assembler.py prog/fib.asm -o sim/fib.hex

pysim:
	$(PYTHON) tools/sim_cpu.py sim/prog.hex --ram 10=5,11=7
	$(PYTHON) tools/sim_cpu.py sim/mul.hex  --ram 10=3,11=4
	$(PYTHON) tools/sim_cpu.py sim/fib.hex

CLEANFILES = $(OUT) $(VCD) $(ALU_OUT) $(ALU_VCD)

clean:
ifeq ($(OS),Windows_NT)
	-del /Q /F $(CLEANFILES) 2>NUL
else
	-rm -f $(CLEANFILES)
endif
