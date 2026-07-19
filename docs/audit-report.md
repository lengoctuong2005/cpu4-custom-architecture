# Báo cáo Audit & Cleanup — CPU 4-bit (PR #1)

> Tài liệu này giải thích các thay đổi trong [PR #1](https://github.com/lengoctuong2005/CPU-4Bit/pull/1).
> Đối tượng đọc: từ người mới đến người đã quen dự án.

## Bối cảnh

Đồ án là một **CPU 4-bit single-cycle** mô tả bằng Verilog RTL cho môn *Thiết kế
vi mạch điện tử*. "Single-cycle" nghĩa là mỗi lệnh hoàn tất trọn vẹn trong đúng
**một cạnh xung clock**: nạp lệnh, giải mã, thực thi và ghi kết quả xảy ra trong
cùng một chu kỳ, không có pipeline. Kiến trúc theo mô hình *Harvard* — bộ nhớ
lệnh (ROM 16×9-bit) và bộ nhớ dữ liệu (RAM 16×4-bit) tách rời.

Datapath gồm các khối quen thuộc: `program_counter` (PC 4-bit) trỏ vào
`instruction_memory`; `control_unit` giải mã 4 bit opcode thành các tín hiệu điều
khiển; `register_file` chứa R0–R3; `alu_4bit` thực hiện 8 phép toán;
`data_memory` cho LOAD/STORE. Tất cả được nối trong `cpu_top.v`.

Một chi tiết cốt lõi cho phần audit này là **quy ước cờ Carry**. Với phép cộng,
`C=1` khi kết quả tràn (a+b ≥ 16) — trực giác thông thường. Nhưng với phép trừ,
dự án chọn quy ước kiểu "không mượn": `C=1` nghĩa là **KHÔNG có mượn** (a ≥ b) và
`C=0` nghĩa là **CÓ mượn** (a < b). Quy ước này được ghi rõ trong `docs/isa.md` và
cài đặt trong `alu_4bit.v` bằng phép cộng bù-2: `{carry,result} = a + (~b) + 1`.

> **Vì sao nó quan trọng?** Nếu một bài kiểm thử hiểu sai quy ước Carry, nó sẽ "tố
> cáo" ALU sai trong khi ALU thực ra đúng — hoặc tệ hơn, che giấu lỗi thật. Đây
> chính là mấu chốt của PR này.

Ngoài phần kỹ thuật, repo còn vô tình bị commit một thư mục `.agents/` (bộ khung
AI coding-agent, 2609 file ~35MB) cùng nhiều artifact tái tạo được
(`node_modules/`, output mô phỏng, cache). Chúng làm repo phình to và gây nhiễu
khi review.

## Ý tưởng cốt lõi

PR chia làm hai mạch việc độc lập.

**1. Dọn dẹp repo.** Gỡ khỏi git mọi thứ không phải mã nguồn: `.agents/`,
`node_modules/`, `.manifest_cache.json`, các file `*.vcd/*.vvp/*.out`, và bản
trùng `data.mem`/`prog.mem` ở gốc. Điểm tinh tế: `.gitignore` *đã* liệt kê
`.agents/` nhưng git vẫn track nó, vì **gitignore chỉ chặn file mới, không gỡ file
đã được track**. Do đó phải `git rm --cached` tường minh.

**2. Sửa bug testbench ALU.** Xét ca `SUB` với a=3, b=10:

```
3 - 10 = -7  → biểu diễn bù-2 4-bit = 9 (1001)
a < b  → CÓ mượn  → theo quy ước: C = 0
```

Testbench cũ lại khẳng định `carry==1`, tức mâu thuẫn với chính tài liệu. Tương tự
ca `DEC` từ 0 → 15. Nhưng vì trong Verilog câu lệnh `assert ... else $error(...)`
**không dừng mô phỏng và không đếm lỗi**, nên cuối cùng testbench vẫn in
`"ALU all tests passed!"` — một lời khẳng định sai sự thật.

Ý tưởng sửa: (a) chỉnh 2 kỳ vọng cho đúng quy ước, (b) gom mọi ca kiểm thử qua một
task `check_alu` có **đếm số lỗi** và so cả ba cờ Z/N/C, (c) chỉ in "passed" khi
`errors == 0`.

## Mã

Các thay đổi nhóm theo hai commit.

**Commit dọn dẹp** (`chore: remove accidentally-committed .agents ...`)
- `git rm -r .agents` + `git rm --cached` cho `node_modules/`,
  `.manifest_cache.json`, `sim/*.vcd|vvp|out`, `sim/_debug.txt`, `cpu_top.vcd`.
- Xóa `data.mem`, `prog.mem` ở gốc (bản trùng, RTL không đọc).
- `.gitignore` bổ sung `node_modules/`, `__pycache__/`, `*.pyc`,
  `.manifest_cache.json`.

**Commit audit** (`fix+docs: correct ALU testbench ...`)
- `tb/tb_alu_4bit.v`: viết lại quanh task
  `check_alu(name, a, b, op, exp_result, exp_Z, exp_N, exp_C)`; 14 ca phủ đủ
  ADD/SUB/AND/OR/XOR/INC/DEC/PASSTHRU kèm ca biên (carry, zero, borrow); banner in
  `errors` thật.
- `Makefile`: `clean` phân nhánh theo `$(OS)` (Windows dùng `del`, Unix dùng
  `rm`); thêm target `alu`, `test`, `asm`, `pysim`.
- `README.md`: thay file lỗi encoding bằng bản tổng quan đầy đủ (kiến trúc, cây
  thư mục, cách chạy, 3 demo, ràng buộc flag-pipeline).
- `docs/isa.md`, `docs/setup.md`, `sim/prog.mem`: chỉnh cho khớp định dạng lệnh
  **9-bit** thật (trước lẫn lộn với 8-bit); sửa lỗi chính tả.
- `tools/sim_cpu.py`: bỏ dòng chết `imm_val = operand & 0x3` (LDI nạp imm 4-bit,
  không phải 2-bit).

> Lưu ý: **không sửa RTL** trong `rtl/`. RTL vốn đã đúng; vấn đề nằm ở bài kiểm thử
> và tài liệu.

## Xác minh

- `make test` → `RESULT: 3 PASS, 0 FAIL` + `ALL TESTS PASSED` (CPU: MUL=12,
  ADD=12, FIB=1,1,2,3,5,8) và `ALU RESULT: 14/14 checks passed, 0 failed`.
- `make asm` sinh lại `sim/*.hex` **giống hệt từng byte** với file đã commit →
  assembler ↔ hex nhất quán.
- Chạy `tools/sim_cpu.py` (mô hình tham chiếu Python) cho **cùng** kết quả với RTL
  trên cả 3 demo → tăng độ tin cậy chéo.
- Kiểm tra `git ls-files` sau cùng: 42 file được track, không còn `.agents/`,
  `node_modules/`, cache hay output.

**QA thủ công từng bước:**
1. `git fetch && git switch claude/cpu-4bit-audit-01SwmMs8LVwnbbKsBy9ZJHzo`
2. Cài Icarus Verilog (`sudo apt install iverilog` hoặc bản Windows).
3. Chạy `make test` → phải thấy cả hai dòng "ALL ... PASSED".
4. Thử phá để chắc chắn test *thực sự* bắt lỗi: sửa tạm một kỳ vọng trong
   `tb/tb_alu_4bit.v` (ví dụ đổi `C` của ca SUB borrow về `1`) rồi chạy lại
   `make alu` → phải thấy `[FAIL]` và `SOME ALU TESTS FAILED`. Hoàn tác sau khi thử.
5. `git ls-files | wc -l` → 42.

## Phương án thay thế

**Phương án A — Đổi quy ước Carry của ALU cho khớp testbench cũ** (thay vì sửa
testbench).

| Ưu điểm | Nhược điểm |
| :--- | :--- |
| Không phải chỉnh file test | Phá vỡ quy ước đã ghi rõ trong `docs/isa.md` |
| | Phải sửa cả RTL + Python model + tài liệu |
| | Quy ước ngược thông lệ mượn/không-mượn của đề |

**Phương án B — Dùng Git LFS / xóa hẳn lịch sử `.agents` bằng filter-repo.**

| Ưu điểm | Nhược điểm |
| :--- | :--- |
| Repo nhẹ thật sự (giảm cả dung lượng .git) | Viết lại lịch sử, buộc force-push, rủi ro cao |
| Phù hợp nếu cần đưa PDF lớn vào | Phức tạp, dễ hỏng với người mới |

PR chọn cách an toàn: chỉ gỡ khỏi track ở commit mới, giữ nguyên lịch sử.

## Đề xuất người để trao đổi

Lịch sử git cho thấy gần như toàn bộ mã do **ngTwg (taikhoanpubg200@gmail.com)** —
chủ repo — viết (commit `73f1b2c "Thêm toàn bộ file dự án"`, `8d03dfe` chỉnh
testbench, `b5e4f4a` thêm ràng buộc flag-pipeline vào ISA). Vì đây là đồ án cá
nhân, người nắm rõ bối cảnh ALU/ISA và nên review PR này chính là **bạn (chủ
repo)**. Không có cộng tác viên nào khác trong lịch sử để đề xuất thêm.

## Trắc nghiệm

<details>
<summary>Câu 1: Vì sao testbench ALU cũ vẫn in "passed" dù có ca sai?</summary>

- A. Vì Icarus bỏ qua module test
- B. Vì `assert ... else $error` chỉ in lỗi, không dừng và không đếm lỗi, còn dòng `$display("...passed")` chạy vô điều kiện ✅
- C. Vì ALU thực ra đúng hết
- D. Vì thiếu `$finish`

**Giải thích:** Đáp án B. Trong Verilog, `$error` trong nhánh `else` của `assert`
chỉ ghi thông báo; nó không ảnh hưởng luồng chạy. Câu `$display` cuối vẫn được thực
thi nên luôn báo "passed". Sửa bằng cách đếm `errors` và in có điều kiện.
</details>

<details>
<summary>Câu 2: Với SUB a=3, b=10, giá trị đúng của result và cờ C là gì?</summary>

- A. result=7, C=1
- B. result=9, C=1
- C. result=9, C=0 ✅
- D. result=13, C=0

**Giải thích:** Đáp án C. 3−10=−7, bù-2 4-bit là 9 (1001). Vì a<b nên CÓ mượn,
theo quy ước dự án `C=0`. (N=1 vì bit3 của 1001 bật.)
</details>

<details>
<summary>Câu 3: Tại sao `.gitignore` liệt kê `.agents/` mà git vẫn track nó?</summary>

- A. `.gitignore` viết sai cú pháp
- B. gitignore chỉ chặn file *chưa* được track; file đã track vẫn cần `git rm --cached` để gỡ ✅
- C. Do `.agents` nằm trong `node_modules`
- D. Do phân quyền file

**Giải thích:** Đáp án B. Quy tắc ignore không tự động gỡ những gì đã nằm trong chỉ
mục. Phải chủ động `git rm --cached` (hoặc `git rm -r`).
</details>

<details>
<summary>Câu 4: Vì sao `git add -A` không đủ để untrack `node_modules/`?</summary>

- A. Vì `node_modules` quá lớn
- B. Vì các file đó đang gitignored VÀ vẫn còn trên đĩa nên git coi là không đổi → không stage việc gỡ ✅
- C. Vì cần quyền root
- D. Vì `-A` chỉ thêm file mới

**Giải thích:** Đáp án B. Khi file đã track còn tồn tại trên đĩa và khớp HEAD,
`git add -A` không thấy thay đổi; gitignore lại chặn thao tác thêm. Chỉ
`git rm --cached` mới stage được việc gỡ khỏi track (vẫn giữ file trên đĩa).
</details>

<details>
<summary>Câu 5: Ràng buộc "flag-pipeline" của CPU này nói gì?</summary>

- A. Không được dùng lệnh JMP
- B. Cờ Z/N được latch tại cạnh clock nên `JZ`/`JN` phải nằm ngay sau lệnh set-flag, không chèn lệnh ALU khác vào giữa ✅
- C. Phải luôn có NOP sau mỗi lệnh
- D. Chỉ R0 mới cập nhật cờ

**Giải thích:** Đáp án B. Vì thiết kế single-cycle latch cờ một nhịp, lệnh nhánh
đọc cờ của lệnh *trước đó*. Nếu chèn một lệnh ALU giữa lệnh set-flag và lệnh nhánh,
cờ bị lệnh chen ghi đè. Đây là quy ước lập trình bắt buộc, không phải lỗi.
</details>
