# CPU 4-bit (TKVM)

Đồ án môn **Thiết kế vi mạch điện tử (TKVM)** — thiết kế một CPU 4-bit
**single-cycle** theo quy trình thiết kế mạch số, mô tả bằng **Verilog RTL** và
kiểm chứng bằng mô phỏng functional (Icarus Verilog). Đề tài chốt phương án
**chỉ mô phỏng RTL, không vẽ layout**.

> Tài liệu ISA đầy đủ: [`docs/isa.md`](docs/isa.md) · Hướng dẫn cài đặt & chạy:
> [`docs/setup.md`](docs/setup.md)

---

## 1. Tổng quan kiến trúc

| Hạng mục | Thông số |
| :--- | :--- |
| Kiến trúc | Single-cycle, Harvard (ROM lệnh + RAM dữ liệu tách biệt) |
| Độ rộng dữ liệu | 4 bit |
| Độ rộng từ lệnh | 9 bit — `[8] imm_mode · [7:4] opcode · [3:0] operand` |
| Thanh ghi | R0–R3 (4 bit); R0 là accumulator cho LOAD/STORE |
| Cờ trạng thái | Zero (Z), Negative (N) |
| Bộ nhớ lệnh (ROM) | 16 × 9 bit |
| Bộ nhớ dữ liệu (RAM) | 16 × 4 bit |
| Tập lệnh | 16 opcode (NOP, LOAD, STORE, MOV/LDI, ADD, SUB, AND, OR, XOR, INC, DEC, JMP, JZ, JN, OUT, HALT) |

---

## 2. Cấu trúc thư mục

```
rtl/            Mã RTL các module
  alu_4bit.v            ALU 4-bit (8 phép: ADD/SUB/AND/OR/XOR/INC/DEC/PASSTHRU)
  register_file.v       4 thanh ghi R0–R3, 2 cổng đọc / 1 cổng ghi
  instruction_memory.v  ROM 16×9
  data_memory.v         RAM 16×4
  control_unit.v        Giải mã opcode -> tín hiệu điều khiển
  program_counter.v     PC 4-bit (đóng băng khi HALT)
  cpu_top.v             Liên kết datapath single-cycle
tb/             Testbench
  tb_alu_4bit.v         Unit test ALU (14 ca, kiểm cả Z/N/C)
  tb_cpu_top.v          Test toàn CPU (3 demo: MUL, ADD, FIB)
prog/           Chương trình nguồn assembly (.asm)
sim/            Mã máy (.hex nạp vào ROM) + bản chú thích (.mem)
tools/
  assembler.py          Hợp dịch .asm -> .hex (9-bit)
  sim_cpu.py            Mô hình tham chiếu Python (trace từng chu kỳ)
docs/           isa.md (ISA), setup.md (cài đặt)
```

---

## 3. Yêu cầu công cụ

- [Icarus Verilog](https://bleyer.org/icarus/) (`iverilog` + `vvp`) — biên dịch & chạy mô phỏng.
- [GTKWave](https://gtkwave.sourceforge.net/) — xem dạng sóng (tuỳ chọn).
- Python 3 — cho assembler và mô hình tham chiếu.

Linux/WSL: `sudo apt install iverilog gtkwave`. Windows: xem [`docs/setup.md`](docs/setup.md).

---

## 4. Chạy nhanh

```bash
make            # biên dịch + chạy testbench toàn CPU
make alu        # chạy unit test ALU
make test       # chạy CẢ hai testbench RTL
make pysim      # chạy mô hình tham chiếu Python trên cả 3 demo
make asm        # hợp dịch lại prog/*.asm -> sim/*.hex
make wave       # mở GTKWave xem cpu_top.vcd
make clean      # xoá file sinh ra (chạy được trên Windows lẫn Unix)
```

Kết quả mong đợi của `make test`: `ALL TESTS PASSED` (CPU) và
`ALL ALU TESTS PASSED` (ALU).

---

## 5. Ba chương trình demo

| Demo | Nguồn | Ý nghĩa | Kết quả đúng |
| :--- | :--- | :--- | :--- |
| ADD | [`prog/add.asm`](prog/add.asm) | `Mem[10] + Mem[11] -> Mem[12]` | OUT = 12, Mem[12] = 12 |
| MUL | [`prog/mul.asm`](prog/mul.asm) | Nhân bằng cộng lặp `3 × 4` | OUT = 12, Mem[12] = 12 |
| FIB | [`prog/fib.asm`](prog/fib.asm) | Dãy Fibonacci 4-bit, dừng khi > 7 | OUT: 1, 1, 2, 3, 5, 8 |

Ví dụ hợp dịch và mô phỏng tham chiếu một chương trình:

```bash
python3 tools/assembler.py prog/fib.asm -o sim/fib.hex --run
python3 tools/sim_cpu.py   sim/fib.hex --trace
```

---

## 6. Ràng buộc thiết kế cần biết

Cờ Z/N được chốt có điều kiện qua `flag_write`; chỉ lệnh sinh cờ (ADD/SUB/AND/OR/XOR/INC/DEC/LDI) mới ghi đè. Có thể chèn lệnh không sinh cờ (MOV/LOAD/STORE/NOP/OUT) giữa lệnh set-flag và JZ/JN.
