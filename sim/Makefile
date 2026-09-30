# ─────────────────────────────────────────────────────────────
# Makefile — CPU 4-bit simulation executed inside sim/ directory
# Tools: Icarus Verilog (iverilog + vvp), Python 3.
# ─────────────────────────────────────────────────────────────

IVERILOG = iverilog -g2012
VVP      = vvp
PYTHON   = python3

OUT      = cpu_tb.out
VCD      = cpu_top.vcd
CPU_SRC  = ../tb/tb_cpu_top.v \
           ../rtl/alu_4bit.v ../rtl/control_unit.v ../rtl/cpu_top.v \
           ../rtl/data_memory.v ../rtl/instruction_memory.v ../rtl/program_counter.v \
           ../rtl/register_file.v

ALU_OUT  = alu_tb.out
ALU_VCD  = tb_alu_4bit.vcd
ALU_SRC  = ../tb/tb_alu_4bit.v ../rtl/alu_4bit.v

.PHONY: all compile run test alu clean

all: run

compile:
	$(IVERILOG) -o $(OUT) $(CPU_SRC)

run: compile
	$(VVP) $(OUT)

alu:
	$(IVERILOG) -o $(ALU_OUT) $(ALU_SRC)
	$(VVP) $(ALU_OUT)

test: run alu

CLEANFILES = $(OUT) $(VCD) $(ALU_OUT) $(ALU_VCD) cpu_sim

clean:
ifeq ($(OS),Windows_NT)
	-del /Q /F $(CLEANFILES) 2>NUL
else
	-rm -f $(CLEANFILES)
endif
