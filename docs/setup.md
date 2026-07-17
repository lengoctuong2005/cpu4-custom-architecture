# Hướng dẫn cài đặt môi trường mô phỏng (Windows)

Đồ án dùng **Verilog (RTL)** mô phỏng functional, không cần FPGA.
Tool cần: **Icarus Verilog** (compiler) + **GTKWave** (xem sóng). Cả hai đều miễn phí, open-source.

---

## 1. Cài Icarus Verilog + GTKWave

### Cách A: Bản cài đặt Windows (khuyên dùng)
1. Tải **Icarus Verilog** bản Windows tại:
   https://bleyer.org/icarus/ (file `iverilog-*.exe` mới nhất)
2. Tải **GTKWave** tại:
   https://gtkwave.sourceforge.net/ (hoặc bản mingw trong cùng trang trên)
3. Cài như phần mềm bình thường, **giữ nguyên** tùy chọn "Add to PATH".
4. Mở PowerShell, kiểm tra:
   ```powershell
   iverilog -V
   vvp -V
   gtkwave -V
   ```
   Nếu hiện version là thành công.

### Cách B: Dùng WSL (nếu máy có WSL)
```bash
sudo apt update
sudo apt install -y iverilog gtkwave
```

### Cách C (fallback không cài): EDAPlayground
- Vào https://www.edaplayground.com, dán code, chọn Icarus Verilog, tick "Open EPWave".

---

## 2. Chạy mô phỏng dự án

Tại thư mục gốc `TKVM/`:

```powershell
make            # compile + chạy, in kết quả TEST PASSED
make wave       # mở GTKWave xem cpu_top.vcd
make clean      # xóa file trung gian
```

Hoặc chạy tay từng bước:
```powershell
iverilog -o cpu_tb.out tb/tb_cpu_top.v rtl/*.v
vvp cpu_tb.out
gtkwave cpu_top.vcd
```

---

## 3. Cấu trúc file cần biết

| File | Vai trò |
| :--- | :--- |
| `rtl/*.v` | Code RTL các module CPU |
| `sim/prog.hex` | Chương trình mã máy (1 byte hex/dòng) nạp vào ROM |
| `sim/prog.mem` | Bản có chú thích, để người đọc hiểu (ROM không đọc file này) |
| `tb/tb_cpu_top.v` | Testbench toàn CPU, xuất waveform `cpu_top.vcd` |
| `tools/assembler.py` | (Phase 2) dịch `.asm` → `prog.hex` |

---

## 4. Khi sửa chương trình

1. Sửa `sim/prog.hex` (hoặc dùng assembler sinh ra).
2. Chạy `make run`.
3. Xem `out_port` và `Mem[12]` in ra có đúng không.
4. Mở `make wave` để xem từng chu kỳ PC, opcode, thanh ghi.
