# Tài liệu ISA chính thức — CPU 4-bit (TKVM)

> Môn: Thiết kế vi mạch điện tử (TKVM), HK3 2025-2026.
> Đề tài: Thiết kế CPU 4-bit dùng quy trình thiết kế mạch số (Topic 7).
> Quyết định đã chốt: **chỉ mô phỏng RTL (Verilog)**, **không vẽ layout**.
> Kiến trúc: **single-cycle**, lõi 4-bit, bộ nhớ chỉ lệnh + bộ nhớ dữ liệu tách biệt (Harvard).

---

## 1. Tổng quan kiến trúc

| Hạng mục | Thông số |
| :--- | :--- |
| Độ rộng từ lệnh | 9 bit |
| Độ rộng dữ liệu | 4 bit |
| Thanh ghi | 4 thanh ghi đa dụng R0–R3 (4 bit mỗi thanh ghi) |
| Thanh ghi cờ | Zero (Z), Negative (N), Carry (C) |
| Bộ nhớ chỉ lệnh (ROM) | 16 × 9 bit (địa chỉ 4 bit) |
| Bộ nhớ dữ liệu (RAM) | 16 × 4 bit (địa chỉ 4 bit) |
| Bộ đếm chương trình PC | 4 bit (0–15) |
| Cổng ra (OUT) | 4 bit |
| Chu kỳ | Single-cycle (1 lệnh = 1 cạnh xung CLK) |
| Tín hiệu dừng | HALT (đóng băng PC) |

### Mô hình lập trình
- **R0 đóng vai trò accumulator** cho các lệnh truy cập bộ nhớ (LOAD/STORE).
- **R1–R3 là thanh ghi đa dụng** dùng cho các phép toán thanh ghi – thanh ghi.
- Các lệnh ALU/MOV/INC/DEC/OUT dùng toán hạng là **2 chỉ số thanh ghi 2 bit** (`[Rd:Rs]`).
- Các lệnh LOAD/STORE/JMP/JZ/JN dùng toán hạng là **địa chỉ 4 bit**.
- Lệnh **LDI #imm** nạp hằng số lập tức vào **R0** (thanh ghi ngầm định), dùng để khởi tạo hằng số.

---

## 2. Định dạng từ lệnh (9 bit)

```
+-----------+-----------------------+
| imm_mode  |  Opcode (4 bit)      |  Operand (4 bit)     |
|  bit [8]  |   bit [7:4]          |      bit [3:0]       |
+-----------+-----------------------+
```

- `imm_mode = 0`: lệnh thanh ghi – thanh ghi hoặc nhảy/nhớ.
- `imm_mode = 1`: lệnh nạp hằng (LDI), opcode vẫn là `0011` (chung với MOV).

**Giải nghĩa trường Operand theo nhóm lệnh:**

| Nhóm | Operand[3:0] | Ý nghĩa |
| :--- | :--- | :--- |
| Thanh ghi – thanh ghi (MOV/ADD/SUB/AND/OR/XOR) | `[Rd:Rs]` = `{operand[3:2], operand[1:0]}` | Rd, Rs ∈ {0,1,2,3} |
| LDI (imm_mode=1) | `imm[3:0]` | hằng số 0–15, nạp vào R0 |
| Truy cập bộ nhớ (LOAD/STORE) | `addr` = `operand[3:0]` | địa chỉ 0–15 (RAM) |
| Nhảy (JMP/JZ/JN) | `addr` = `operand[3:0]` | địa chỉ 0–15 (ROM) |
| INC/DEC | `Rd` = `operand[3:2]` | Rs bỏ qua |
| OUT | `Rs` = `operand[1:0]` | Rd bỏ qua |
| NOP / HALT | — | toán hạng bị bỏ qua |

---

## 3. Tập lệnh (16 opcode)

| Opcode | Mnemonic | Toán hạng | Hoạt động | Cập nhật cờ |
| :--- | :--- | :--- | :--- | :--- |
| `0000` | `NOP` | — | Không làm gì | không |
| `0001` | `LOAD addr` | addr | `R0 ← Mem[addr]` | không |
| `0010` | `STORE addr` | addr | `Mem[addr] ← R0` | không |
| `0011` | `MOV Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rs]` | không |
| `0011` | `LDI #imm` | imm (imm_mode=1) | `R0 ← imm` (imm 0–15) | Z, N (C=0) |
| `0100` | `ADD Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rd] + R[Rs]` | Z, N, C |
| `0101` | `SUB Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rd] - R[Rs]` | Z, N, C |
| `0110` | `AND Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rd] & R[Rs]` | Z, N |
| `0111` | `OR Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rd] \| R[Rs]` | Z, N |
| `1000` | `XOR Rd, Rs` | `[Rd:Rs]` | `R[Rd] ← R[Rd] ^ R[Rs]` | Z, N |
| `1001` | `INC Rd` | `Rd` | `R[Rd] ← R[Rd] + 1` | Z, N, C |
| `1010` | `DEC Rd` | `Rd` | `R[Rd] ← R[Rd] - 1` | Z, N, C |
| `1011` | `JMP addr` | addr | `PC ← addr` | không |
| `1100` | `JZ addr` | addr | `if Z=1: PC ← addr` | không |
| `1101` | `JN addr` | addr | `if N=1: PC ← addr` | không |
| `1110` | `OUT Rs` | `Rs` | `OUT ← R[Rs]` | không |
| `1111` | `HALT` | — | Đóng băng PC, dừng thực thi | không |

> Quy ước cờ: **Z** = 1 khi kết quả = 0; **N** = 1 khi bit cao nhất của kết quả = 1
> (số có dấu bù 2, bit 3); **C** = 1 khi phép cộng/trừ sinh bit nhớ (bit 4 của kết quả 5 bit).

> LDI dùng chung opcode `0011` với MOV, phân biệt bằng `imm_mode` (bit 8). LDI luôn
> nạp vào R0; muốn đưa hằng số vào R1/R2/R3, dùng `LDI #imm` rồi `MOV Rx, R0`.

---

## 4. Tín hiệu điều khiển (Control Unit)

Bảng chân trị tóm tắt (cho `cpu_top`):

| Opcode | RegWrite | MemRead | MemWrite | MemtoReg | ALUSrcB | ALUOp | PCSrc | RegSel |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NOP | 0 | 0 | 0 | X | X | ADD | PC+1 | X |
| LOAD | 1 | 1 | 0 | MEM | X | ADD | PC+1 | R0 |
| STORE | 0 | 0 | 1 | X | X | ADD | PC+1 | R0 |
| MOV | 1 | 0 | 0 | ALU | REG | ADD(passthru) | PC+1 | Rd |
| LDI | 1 | 0 | 0 | ALU | IMM | ADD(passthru) | PC+1 | R0 |
| ADD/SUB/AND/OR/XOR | 1 | 0 | 0 | ALU | REG | theo opcode | PC+1 | Rd |
| INC/DEC | 1 | 0 | 0 | ALU | REG | ADD/SUB(+1/-1) | PC+1 | Rd |
| JMP | 0 | 0 | 0 | X | X | ADD | addr | X |
| JZ | 0 | 0 | 0 | X | X | ADD | addr nếu Z | X |
| JN | 0 | 0 | 0 | X | X | ADD | addr nếu N | X |
| OUT | 0 | 0 | 0 | X | X | ADD | PC+1 | X |
| HALT | 0 | 0 | 0 | X | X | ADD | giữ nguyên | X |

- `RegSel = R0`: thanh ghi đích/nguồn là R0 (lệnh bộ nhớ, LDI).
- `RegSel = Rd`: thanh ghi đích là `operand[3:2]`, nguồn 2 là `operand[1:0]`.
- `MemtoReg = MEM`: kết quả ghi vào thanh ghi lấy từ bộ nhớ (LOAD).
- `MemtoReg = ALU`: kết quả ghi vào thanh ghi lấy từ ALU.
- `ALUSrcB`: chọn toán hạng B của ALU (REG = R[Rs], MEM cho LOAD, IMM cho LDI).

---

## 5. Ví dụ chương trình (kiểm thử)

Cộng hai số đặt tại `Mem[10]` và `Mem[11]`, lưu tổng vào `Mem[12]`:

```asm
; Mem[10] = 5, Mem[11] = 7  (khởi tạo bởi file .mem)
0x00: LOAD  10      ; R0 = Mem[10]  = 5
0x01: MOV   R1, R0  ; R1 = R0      = 5
0x02: LOAD  11      ; R0 = Mem[11]  = 7
0x03: ADD   R1, R0  ; R1 = R1 + R0 = 12
0x04: MOV   R0, R1  ; R0 = R1      = 12
0x05: STORE 12      ; Mem[12] = R0 = 12
0x06: OUT   R0      ; OUT = 12
0x07: HALT
```

Kết quả đúng: `Mem[12] = 12 = 0xC`, cờ Z = 0, N = 0 (12 < 16).

---

## 6. Tệp liên quan

- `rtl/alu_4bit.v` — khối ALU 4 bit.
- `rtl/register_file.v` — file thanh ghi 4×4 bit.
- `rtl/instruction_memory.v` — ROM chỉ lệnh 16×9.
- `rtl/data_memory.v` — RAM dữ liệu 16×4.
- `rtl/control_unit.v` — giải mã opcode → tín hiệu điều khiển.
- `rtl/program_counter.v` — bộ đếm PC 4 bit.
- `rtl/cpu_top.v` — liên kết datapath single-cycle.
- `tools/assembler.py` — bộ hợp dịchch .asm → .hex (9-bit, 3 ký tự hex/dòng).
- `tools/sim_cpu.py` — mô phỏng hành vi tham chiếu (Python).
- `sim/*.hex` — chương trình mã máy + dữ liệu khởi tạo.
- `tb/tb_*.v` — testbench từng module và toàn bộ CPU.
