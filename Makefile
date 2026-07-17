# Makefile - CPU 4-bit (TKVM) simulation with Icarus Verilog + GTKWave
# Cách dùng:
#   make          -> compile + run simulation
#   make compile  -> chỉ compile (tạo cpu_tb.out)
#   make run      -> chạy simulation (tạo cpu_top.vcd)
#   make wave     -> mở GTKWave xem sóng
#   make clean    -> xóa file trung gian

IVERILOG = iverilog -g2012
VVP      = vvp
GTKWAVE  = gtkwave
OUT      = cpu_tb.out
VCD      = cpu_top.vcd

SRC = tb/tb_cpu_top.v rtl/alu_4bit.v rtl/control_unit.v rtl/cpu_top.v \
      rtl/data_memory.v rtl/instruction_memory.v rtl/program_counter.v \
      rtl/register_file.v

.PHONY: all compile run wave clean

all: compile run

compile:
	$(IVERILOG) -o $(OUT) $(SRC)

run: compile
	$(VVP) $(OUT)

wave: run
	$(GTKWAVE) $(VCD)

clean:
	powershell -Command "Remove-Item -ErrorAction SilentlyContinue -Force $(OUT), $(VCD); exit 0"

