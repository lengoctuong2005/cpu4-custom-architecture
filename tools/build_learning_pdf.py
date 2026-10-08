from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
from pathlib import Path
import json
import os, subprocess
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'build/documentation'
D.mkdir(parents=True,exist_ok=True)
METRICS=json.loads((ROOT/'docs/verification_metrics.json').read_text())
for n,f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Mono','cour.ttf')]:
    candidate=Path('/usr/share/fonts/msttcore')/f
    if not candidate.exists():
        family={'Arial':'Arial','Arial-Bold':'Arial:style=Bold','Mono':'Courier New'}[n]
        candidate=Path(subprocess.check_output(['fc-match','-f','%{file}',family],text=True).strip())
    pdfmetrics.registerFont(TTFont(n,str(candidate)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
styles={
'p':ParagraphStyle('p',fontName='Arial',fontSize=11,leading=15,textColor=HexColor('#2C2C2B'),spaceAfter=6),
'h':ParagraphStyle('h',fontName='Arial-Bold',fontSize=19,leading=24,textColor=HexColor('#146492'),spaceAfter=16),
'h2':ParagraphStyle('h2',fontName='Arial-Bold',fontSize=12.5,leading=17,spaceBefore=7,spaceAfter=5,textColor=HexColor('#146492')),
'small':ParagraphStyle('small',fontName='Arial',fontSize=9,leading=12.5,spaceAfter=5,textColor=HexColor('#61676E')),
'cell':ParagraphStyle('cell',fontName='Arial',fontSize=10,leading=13,spaceAfter=0),
'code':ParagraphStyle('code',fontName='Mono',fontSize=9.2,leading=12.3,textColor=HexColor('#172A3C')),
'cover':ParagraphStyle('cover',fontName='Arial-Bold',fontSize=28,leading=34,textColor=HexColor('#123C59'),spaceAfter=18)
}
story=[]; titles=[]
def p(t,sty='p'): story.append(Paragraph(t,styles[sty]))
def h(t):p(t,'h2')
def bullet(t):p('• '+t)
def code(t):
    story.append(Preformatted(t,styles['code'],maxLineLength=83));story.append(Spacer(1,9))
def box(t):
    tb=Table([[Paragraph(t,styles['p'])]],colWidths=[487]);tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#E5F2FC')),('BOX',(0,0),(-1,-1),.5,HexColor('#C6DCEC')),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(tb);story.append(Spacer(1,10))
def table(headers,rows,widths):
    data=[[Paragraph('<b>'+escape(x)+'</b>',styles['cell']) for x in headers]]+[[Paragraph(escape(str(x)),styles['cell']) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#E5F2FC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F9F8F7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,HexColor('#B4CDD9')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,10))
def page(t):
    if titles:story.append(PageBreak())
    titles.append(t);p(t,'h')

page('CPU4 • Physical Design & STA')
p('Tài liệu học tập<br/>đã hiệu đính','cover')
p('Dành cho Lê Ngọc Tường • Bản hiệu đính + kiểm thử thực tế • 08/10/2026')
box('<b>Kết luận:</b> bản PDF cũ có kiến thức nền đúng, nhưng còn lỗi kỹ thuật và nhiều câu khẳng định quá mức. Bản này có kết quả kiểm thử RTL thực tế và bằng chứng tái tạo; không phải chứng nhận ASIC đã signoff hoặc silicon đã hoạt động.')
h('Phạm vi và mức độ xác minh')
bullet('<b>Đã làm:</b> rà soát đủ 10 trang PDF gốc và 15 câu phỏng vấn; đối chiếu đặc tả, tải repo baseline <b>5f2e19d</b>, chạy test thực tế và sửa trên nhánh riêng. Kết quả chi tiết ở trang 19–24. [S1–S6]')
bullet('<b>Đã chạy:</b> RTL ALU exhaustive, unit/demos, decoder, boot ROM, FPGA logic; differential 2.767 kịch bản / 79.324 cạnh clock; kiểm tra công thức cờ, test âm và formal ALU. Xem trang 19–24.')
bullet('<b>Giới hạn:</b> synthesis và STA minh họa được ghi riêng theo tool/library. Chưa chạy Synopsys, Quartus/board, P&amp;R, post-route/SPEF, signoff DRC/LVS/IR/EM; không có PDK SAED32/JD FPT hợp lệ để xác minh.')
p('Bỏ nhãn “chuẩn FPT AI Chip” và các câu “FPT yêu cầu…” chưa có nguồn. Mục tiêu ứng tuyển vẫn có thể giữ, nhưng nội dung ở đây là kiến thức PD/STA phổ quát, cần đối chiếu JD thực tế.')
h('Mục lục')
table(['Trang','Nội dung'],[
('2–3','Kiến trúc/ISA CPU4; RTL, reset và flag_write'),
('4–5','Cờ Z/N/C/V; tràn số, ví dụ và kiểm thử'),
('6–7','Critical path; lộ trình 5 tuần và tiêu chí bằng chứng'),
('8–10','Setup/hold/skew; DRV; SDC, CDC và reset'),
('11–13','PVT/variation; crosstalk/IR; bộ nhớ và Liberty'),
('14','Tcl theo công cụ; điều kiện chạy và giới hạn'),
('15–16','15 câu phỏng vấn đã sửa'),
('17–18','Nhật ký hiệu đính; nguồn và cách kiểm chứng tiếp'),
('19–24','Kết quả test thực tế, lỗi/sửa, synthesis/STA và GitHub')],[52,435])
p('Cách đọc: phân biệt “theo RTL đã đọc”, “kiến thức chung” và “cần báo cáo đo”. Không biến giả thuyết tối ưu hay kế hoạch tương lai thành thành tích đã thực hiện. [S1]','small')

page('1.1 • Kiến trúc và ISA CPU4 v1')
p('CPU4 là CPU Harvard single-cycle: bộ nhớ lệnh và dữ liệu có đường truy cập độc lập. Điều này tránh tranh chấp tài nguyên giữa fetch và data access của chính hai bộ nhớ; không đồng nghĩa loại bỏ mọi hazard hay đảm bảo throughput cao. Thuật ngữ phù hợp là <b>von Neumann bottleneck / structural hazard</b>, không phải mặc định “bus contention” theo nghĩa hai driver cùng lái một net. [S1,S2]')
table(['Thành phần','Đặc tả'],[
('Datapath','4-bit; unsigned 0…15 hoặc signed bù 2 −8…7'),('PC / R0–R3','PC 4-bit, tăng modulo 16; 4 thanh ghi × 4-bit'),('IMEM / DMEM','16 × 9-bit, đọc tổ hợp / 16 × 4-bit, đọc tổ hợp, ghi cạnh lên'),('OUT / cờ','OUT 4-bit; chỉ lưu Z và N khi flag_write=1'),('Từ lệnh','[8] imm_mode | [7:4] opcode | [3:0] operand')],[100,387])
p('<b>Điểm cần sửa:</b> imm_mode không phải cờ trạng thái và không biến mọi lệnh thành immediate. RTL chỉ dùng bit này để phân biệt MOV/LDI ở opcode 3. Opcode 4-bit có 16 giá trị mã; MOV và LDI dùng chung một mã nên số tên lệnh không nhất thiết chỉ là 16. [S2,S4]')
table(['Mã','Lệnh / operand','Hiệu ứng; cập nhật cờ?'],[
('0','NOP','Không thay đổi trạng thái'),('1 / 2','LOAD addr / STORE addr','R0 ← RAM[addr] / RAM[addr] ← R0; không đổi cờ'),('3, bit8=0','MOV Rd, Rs; {Rd,Rs}','Rd ← Rs; không đổi cờ'),('3, bit8=1','LDI #imm; imm[3:0]','R0 ← imm; ghi Z,N'),('4 / 5','ADD / SUB Rd,Rs','Rd ← Rd ± Rs modulo 16; ghi Z,N'),('6 / 7 / 8','AND / OR / XOR Rd,Rs','Rd ← phép logic; ghi Z,N'),('9 / A','INC / DEC Rd; {Rd,00}','Rd ← Rd ± 1; ghi Z,N'),('B / C / D','JMP / JZ / JN addr','Nhảy luôn / khi Z=1 / khi N=1; không đổi cờ'),('E / F','OUT Rs; {00,Rs} / HALT','OUT ← Rs / giữ PC và trạng thái; không đổi cờ')],[48,200,239])
p('Harvard cho phép độ rộng từ lệnh độc lập với bus dữ liệu; 9-bit là lựa chọn encoding, không phải điều kiện bắt buộc của single-cycle. LOAD/LDI dùng R0 ngầm định là quyết định ISA này, không phải luật chung. JNZ, JC, ADC, CMP, JLT trong các ví dụ lý thuyết ở trang sau <b>không phải lệnh CPU4 v1</b>. [S1,S4]','small')

page('1.2–1.3 • RTL và trạng thái kiến trúc')
h('ALU và register file')
p('ALU hiện có op 000 ADD, 001 SUB, 010 AND, 011 OR, 100 XOR, 101 INC, 110 DEC, 111 PASS B. Output là result, zero, negative và carry. Chưa có output overflow V. Z=(result==0), N=result[3]. [S3]')
p('Register file theo đặc tả: 2 cổng đọc tổ hợp, 1 cổng ghi đồng bộ. “Đọc ngay” nghĩa là không thêm một chu kỳ, nhưng vẫn có trễ MUX/cell/dây. Đọc tổ hợp phù hợp datapath single-cycle này; không phải mọi CPU đều bắt buộc dùng nó. [S1]')
h('Ghi cờ có điều kiện là sửa chức năng')
p('Theo control_unit, ADD/SUB/AND/OR/XOR/INC/DEC/LDI ghi Z,N; MOV/LOAD/STORE/NOP/branch/OUT/HALT giữ cờ. CPU chốt cờ ở cạnh lên và branch đọc cờ đã lưu, không dùng cờ tổ hợp của chính chu kỳ branch. [S2,S4]')
code("// Minh hoa, khong phai thay the nguyen file RTL\nalways_ff @(posedge clk or negedge rst_n) begin\n  if (!rst_n) begin\n    zero_r     <= 1'b0;\n    negative_r <= 1'b0;\n  end else if (flag_write) begin\n    zero_r     <= zero;\n    negative_r <= negative;\n  end\nend")
p('<b>Reset Z=0 dù register file về 0 vẫn hợp lệ</b> nếu ISA định nghĩa như vậy: cờ không tự phản ánh R0 liên tục. Cần test SUB → MOV/STORE → JZ/JN, và test LDI vì LDI chủ động ghi đè cờ. flag_write không phải bằng chứng timing nhanh hơn. [S2]')
h('Control, PC và reset')
bullet('Gán default đầy đủ trong always_comb cho các output do khối đó điều khiển; mỗi tín hiệu một driver. pc_src trong code được assign riêng; HALT được decode ở cpu_top, không phải output halt của control_unit như PDF cũ. [S2,S4]')
bullet('PC reset về 0; HALT giữ PC; còn lại chọn branch hoặc PC+1 modulo 16. Bản sửa thêm clk_en: mức 0 giữ mọi trạng thái kiến trúc, không gate clock. HALT cũng phải không phát write-enable cho RF/RAM/flags/OUT. [S1,S2]')
bullet('Async assert / sync deassert giúp giảm rủi ro metastability, không xóa nó tuyệt đối. Mỗi clock domain cần reset-release strategy phù hợp; phải kiểm tra recovery/removal và độ rộng xung reset.')
box('<b>Finding khi đọc code:</b> cpu_top nối .zero(zero), .negative(negative), .carry(carry) nhưng không khai báo tường minh ba net này. Bản sửa đã khai báo tường minh và chạy strict-net elaboration PASS. Đây là lỗi cảnh báo trong baseline, không phải bằng chứng demo gốc FAIL. Xem trang 20. [S2]')

page('1.5 • Có bắt buộc phải có bốn cờ?')
box('<b>Không.</b> CPU có thể có 0, 1, 2, 3, 4 hoặc nhiều cờ hơn. Số cờ và ý nghĩa do ISA quyết định. Khi đã chốt ISA, RTL, assembler, emulator và tài liệu phải cùng tuân thủ; không tùy ý thay đổi từng chỗ.')
p('Z/N/C/V là bộ cờ số học thường gặp, không phải chuẩn bắt buộc cho mọi CPU. Ví dụ ARM có NZCV; kiến trúc khác có thể thêm parity/auxiliary carry, hoặc dùng lệnh branch-compare mà không lưu cờ toàn cục. [S7]')
table(['Cờ','Ý nghĩa (r = kết quả 4-bit)','Ứng dụng / giới hạn'],[
('Z','r == 0','JZ; sau SUB, Z=1 nghĩa là hai bit-pattern bằng nhau'),('N','r[3]','JN kiểm tra dấu của kết quả đã cắt 4-bit; không đủ cho signed a<b khi SUB tràn'),('C','ADD: carry-out bit thứ 5','Unsigned overflow; ADC; so sánh unsigned sau SUB theo quy ước borrow'),('V','Kết quả signed thật vượt −8…7','Signed overflow; sau SUB, signed less-than = N XOR V')],[35,224,228])
h('C và V là hai khái niệm khác nhau')
p('Đặt a3, b3, r3 là bit dấu; r=(a±b) mod 16. Với phép toán 4-bit thuần ADD/SUB:')
code('Z = (r == 0)                  N = r[3]\nADD: C = ((unsigned(a) + unsigned(b)) >= 16)\nADD: V = (~(a3 ^ b3)) & (a3 ^ r3)\nSUB: V = (a3 ^ b3) & (a3 ^ r3)\nSUB: C_no_borrow = (unsigned(a) >= unsigned(b))')
p('ALU CPU4 đang dùng <b>C=1 nghĩa là không mượn</b> cho SUB/DEC: cộng mở rộng a + (~b trên 4-bit) + 1 rồi lấy bit 4. Nếu chọn quy ước C=borrow thì điều kiện so sánh đảo lại. Không được trộn hai quy ước. Carry hiện chỉ là output nội bộ, chưa được lưu trong CPU. [S3]')
h('Chọn 2, 3 hay 4 cờ như thế nào?')
bullet('<b>Z,N:</b> hợp lệ và đúng CPU4 v1; JN chỉ là “bit dấu kết quả bằng 1”. Không quảng bá JN là signed less-than tổng quát.')
bullet('<b>Z,N,C:</b> hỗ trợ carry/unsigned comparison/multi-nibble arithmetic nếu thêm ISA và datapath; vẫn thiếu V cho cách so sánh signed bằng N XOR V.')
bullet('<b>Z,N,C,V:</b> tiện cho cả signed và unsigned. Phải định nghĩa lệnh nào ghi/giữ từng cờ, giá trị reset và encoding mới; không chỉ thêm hai flip-flop.')
p('“Mỗi cờ chỉ đáng có nếu có lệnh dùng nó” là nguyên tắc thiết kế tối giản, không phải luật: cờ còn có thể đọc qua status register hoặc dùng cho trap/debug. Riêng CPU4, thêm JC/ADC cần giải quyết không gian opcode và tương thích toolchain. [S1]','small')

page('1.6 • Ví dụ cờ và kiểm tra toàn miền 4-bit')
p('C trong bảng dưới dùng quy ước <b>no-borrow</b> cho SUB. N luôn là bit 3 của kết quả, bất kể bạn đang diễn giải số signed hay unsigned. V là cờ giả định để học, <b>không tồn tại trong RTL CPU4 đã đọc</b>.')
table(['Phép toán / diễn giải','r','Z','N','C','V'],[
('7 + 1 = 8; signed vượt +7','1000',0,1,0,1),('15 + 1 = 16; unsigned carry','0000',1,0,1,0),('7 − (−8) = 15; signed overflow','1111',0,1,0,1),('−8 − 1 = −9; signed overflow','0111',0,0,1,1),('3 − 5 = −2; unsigned borrow','1110',0,1,0,0),('5 − 3 = 2','0010',0,0,1,0),('5 − 5 = 0','0000',1,0,1,0)],[287,60,35,35,35,35])
box('<b>Vì sao JN không thay được JLT?</b> 7−(−8) cho r=1111 nên N=1. JN nhảy là đúng semantics của JN, nhưng suy ra 7&lt;−8 là sai. V=1 nên N XOR V=0, khôi phục đúng phép so sánh signed.')
h('Điều kiện sau SUB/CMP, nếu ISA có đủ cờ')
code('Equal:       Z == 1      Not equal: Z == 0\nUnsigned < : C == 0      Unsigned >= : C == 1\nUnsigned > : C == 1 && Z == 0\nUnsigned <=: C == 0 || Z == 1\nSigned <   : N != V      Signed >= : N == V\nSigned >   : Z == 0 && N == V\nSigned <=  : Z == 1 || N != V')
p('Các điều kiện này phụ thuộc việc cờ được sinh từ đúng phép SUB so sánh và chưa bị lệnh khác ghi đè. CPU4 v1 không có CMP: SUB ghi đè thanh ghi đích, nên cần giữ operand nếu chương trình còn dùng nó. [S1,S7]')
h('Kiểm tra đã chạy cho bản tài liệu')
p('Python kiểm tra 16×16 = 256 cặp A,B cho ADD và 256 cặp cho SUB; so V với kết quả signed thật vượt miền −8…7. Kiểm tra 10 điều kiện equality/unsigned/signed trên cả 256 cặp SUB. <b>Kết quả: 512 phép toán và 2.560 kiểm tra điều kiện đều PASS.</b> Đây không chứng minh RTL PASS; script kiểm tra được lưu cùng quá trình tạo tài liệu.')
h('Test RTL đã chạy và lớp kiểm tra cần duy trì')
bullet('ALU exhaustive: 8 op × 16 A × 16 B = 2.048 vector, kiểm tra result/Z/N/C theo op; V chỉ khi nâng phiên bản.')
bullet('Kiểm tra flag preservation, reset, branch taken/not-taken, LDI ghi cờ, HALT; so state mỗi chu kỳ với emulator. Dùng $fatal(1) khi mismatch để CI fail, không chỉ in “ERROR” rồi tiếp tục. [S1]')

page('1.4 / 2 • Critical path và tuần 1–3')
h('Không đo thì chưa được gọi là điểm nghẽn')
p('Một đường ứng viên là PC → ROM → chọn/giải mã toán hạng → RF read/MUX → ALU → writeback → RF D. LOAD còn có PC → ROM → địa chỉ/enable RAM → RAM read → writeback → RF D. Branch có đường cờ đã lưu/ROM → điều khiển → PC D. Cần so cả đường data và control; không cộng tuần tự mọi khối nếu chúng chạy song song. [S2]')
code('Tmin >= tcq_max + tcomb_max + tsetup + Usetup - skew\n// Mo hinh cung clock, single-cycle; can xet tung path.')
p('Carry ripple trên 4-bit chưa chắc chi phối. Công cụ ánh xạ toán tử + theo thư viện/mục tiêu; CLA viết tay có thể không cải thiện PPA. flag_write sửa chức năng, không phải chứng cứ giảm delay. Pipeline là thay đổi microarchitecture: phải xử lý branch, dependency/hazard và verification lại.')
h('Tuần 1 • Chốt ISA và mô phỏng')
bullet('Thống nhất cpu_top; chuẩn SystemVerilog-2012 (.sv hoặc đọc -sv; Icarus -g2012). File hiện dùng logic/always_ff/always_comb dù tên .v. [S1–S4]')
bullet('Lint implicit net, latch, loop, multi-driver, width/signedness; test PC wrap/HALT, đủ địa chỉ RAM, OUT và flag preservation. Không sửa loop bằng false-path.')
bullet('Assembler/emulator cùng nguồn opcode; reject >16 lệnh, label trùng/thiếu, operand sai. Differential test state từng chu kỳ và seed tái tạo.')
p('<b>Đầu ra:</b> test log, waveform cho case cần debug, cấu hình/lệnh chạy; không dùng waveform thay self-checking tests.')
h('Tuần 2 • Synthesis và tính tương đương')
bullet('Dùng Yosys/DC với thư viện .lib phù hợp; lưu mapped netlist, cell area, cell count, FF/MUX, latch/loop warnings và timing sơ bộ. Formal RTL→gate khi có flow phù hợp.')
bullet('NAND-equivalent chỉ có nghĩa khi xác định cell NAND chuẩn và thư viện; cell area không phải die area. Fanout là chỉ báo, capacitance/slew và RC mới xác định tải/timing.')
bullet('Kiểm tra ROM chương trình thật còn tồn tại sau tổng hợp; đừng dùng testbench preload để thay cho implementation ROM/RAM của hardware.')
h('Tuần 3 • SDC và STA trước layout')
bullet('Ràng buộc clock, waveform, uncertainty, input/output delay <b>cả min/max</b>, drive/load, generated clock nếu có; kiểm tra unconstrained paths và exceptions.')
bullet('Đọc report_checks min/max (OpenSTA) hoặc report_timing (PrimeTime): start/end, logic, cell/net delay, clock path, slew/load. Chỉ tối ưu sau khi xác định nguyên nhân.')
p('Quét chu kỳ để ước lượng Fmax tại corner/mô hình RC đang dùng; đổi target rồi tái tổng hợp/P&amp;R có thể đổi netlist. Fmax pre-layout không phải tần số silicon đã được đảm bảo. [S9,S10]','small')

page('2 • Tuần 4–5 và tiêu chí hoàn thành')
h('Tuần 4 • Floorplan → CTS → routing')
table(['Bước','Công việc và điểm cần kiểm tra'],[
('Floorplan','Aspect ratio theo nhu cầu; utilization 50–60% chỉ là điểm khởi đầu cho bài tập, không phải ngưỡng an toàn chung. Đặt macro, pin, halo, channel.'),('Physical cells','Tap cells / well ties và endcaps theo PDK; xử lý rows/keepout. Không chờ tới cuối routing mới thêm tapcells.'),('PDN','Power ring/strap/rail theo stack kim loại, dòng tải và pin macro; kiểm tra connectivity, IR/EM.'),('Placement','Global: tối ưu wirelength, density, congestion, timing. Detailed: legalize đúng site/row; không tự đảm bảo hết congestion.'),('CTS','Cây clock đáp ứng skew, latency, slew, pulse width, công suất. Propagate clock; kiểm tra và sửa hold sau CTS, đồng thời giữ setup.'),('Routing','Global guides → detailed routes theo PDK; lớp kim loại không mặc định M1–M6. Repair antenna/DRV/timing và route lại ECO.')],[86,401])
p('CTS không chỉ “giảm insertion delay tối đa”; cần trade-off skew/latency/power/variation. Useful skew có thể có chủ đích. Tapcell, CTS, repair timing và extraction có trong flow OpenROAD, nhưng thứ tự cụ thể tùy flow/PDK. [S9,S10]')
h('Tuần 5 • STA post-route và physical verification')
bullet('<b>RC extraction → SPEF → STA:</b> đọc SPEF tương ứng netlist/layout, kiểm tra annotation coverage; propagated clocks, nhiều mode/corner với .lib và RC corner đúng. Báo cáo setup, hold, recovery/removal, pulse width, slew/cap và unconstrained paths.')
bullet('<b>Physical checks:</b> DRC bằng deck phù hợp; LVS so connectivity/device với reference netlist, không phải “so 1–1 cell” tuyệt đối. Thêm antenna, density/fill, ERC/connectivity nguồn, IR/EM theo yêu cầu.')
bullet('<b>ECO loop:</b> sửa → route lại → extract lại → STA/DRV/physical checks lại. Metal fill có thể đổi RC; dùng parasitic cuối phù hợp.')
bullet('<b>Packaging:</b> GDSII/OASIS, final netlist, SDC, SPEF, reports, tool/PDK version, commit và checksum. Formal gate→post-P&amp;R khi có flow.')
box('<b>Xuất GDS không đồng nghĩa signoff/tape-out.</b> DRC/LVS sạch không chứng minh chức năng hay timing đúng. Flow open-source phục vụ học tập; không tự tương đương signoff sản xuất nếu thiếu bộ deck/thư viện/corner được phê duyệt.')
p('Mốc 5 tuần là kế hoạch học tập, không phải bảo đảm hoàn tất ASIC. License, PDK, setup tool và lỗi thiết kế có thể kéo dài thời gian. [S1]','small')

page('3.1 • Setup, hold và clock skew')
p('Mô hình dưới đây dành cho hai FF cùng clock, cùng cạnh lên, single-cycle. L và K là latency clock tới launch/capture, không gồm chu kỳ T; Dmax/Dmin gồm cell và net delay. Signoff cần early/late, variation, SI và CPPR/CRPR theo công cụ.')
h('Setup • dữ liệu cũ phải đến trước cạnh capture')
code('Arrival_setup  = L + tcq_max + Dmax\nRequired_setup = K + T - tsetup - Usetup\nSlack_setup    = Required_setup - Arrival_setup\n               = T + (K-L) - tcq_max - Dmax\n                 - tsetup - Usetup')
h('Hold • dữ liệu mới không được đến quá sớm')
code('Arrival_hold  = L + tcq_min + Dmin\nRequired_hold = K + thold + Uhold\nSlack_hold    = Arrival_hold - Required_hold\n              = tcq_min + Dmin - (K-L) - thold - Uhold')
p('<b>skew = K−L:</b> positive skew giúp setup và làm xấu hold của chính đường launch→capture; negative skew ngược lại. Usetup và Uhold có thể khác nhau. Hold “không có T” là kết quả cho quan hệ same-edge này, không phải công thức duy nhất cho mọi generated/multiphase clock. [S8]')
h('Ví dụ số để tự kiểm tra dấu')
p('Cho T=10 ns, L=0,5 ns, K=0,8 ns; tcq_max=0,2 ns, Dmax=8 ns, tsetup=0,4 ns, Usetup=0,1 ns. Setup arrival=8,7 ns; required=10,3 ns; <b>slack=+1,6 ns</b>.')
p('Cho tcq_min=0,1 ns, Dmin=0,35 ns, thold=0,1 ns, Uhold=0,05 ns. Hold arrival=0,95 ns; required=0,95 ns; <b>slack=0 ns</b>. Tăng K thêm 0,2 ns giúp setup +0,2 ns nhưng hold thành −0,2 ns.')
h('Sửa vi phạm mà không nói quá')
bullet('Setup: giảm cell/net delay, resize/Vt swap có kiểm soát, cải thiện placement/logic hoặc pipeline. Giảm tần số có thể giúp nếu lỗi đúng là single-cycle setup; tăng Vdd chỉ trong operating range và kiểm tra reliability/power/hold lại.')
bullet('Hold: tăng min data delay bằng delay cells/buffer, route detour hoặc điều chỉnh skew phù hợp. Chèn buffer có thể làm xấu setup và thêm load; phải kiểm tra mọi corner.')
bullet('Sau chế tạo, hold thường không cứu được bằng hạ tần số; có thể cần re-spin. Workaround clock/operating-mode chỉ khả thi khi thiết kế có hỗ trợ và được đo xác nhận; không kết luận mọi chip đều “phải vứt bỏ”.')

page('3.2 • DRV và sửa timing có kiểm soát')
p('Phân biệt <b>electrical design-rule violations</b> trong STA (slew, cap, fanout…) với DRC hình học của layout. Min pulse width là timing check của cell; công cụ có thể nhóm nó khác DRV.')
table(['Loại','Nguyên nhân và hướng xử lý'],[
('Max transition','Transition time quá lớn (sườn chậm): load/RC lớn, drive yếu. Buffer, resize, giảm wirelength/fanout. Transition time không đồng nghĩa slew-rate V/s; “max transition” giới hạn thời gian cạnh.'),('Max capacitance','Tổng pin+wire capacitance vượt giới hạn driver. Phân tải/buffer/clone, cải thiện placement/routing; resize nếu library cho phép. Fanout cao không tự chứng minh cap vi phạm.'),('Max fanout','Giới hạn số tải hoặc fanout load theo tool/library. Dùng cùng cap/slew, không thay chúng.'),('Min pulse width','Xung high/low quá hẹp do waveform nguồn, generated-clock sai, duty-cycle distortion, gating/glitch hoặc rise/fall delay lệch. Kiểm tra cả clock và async control nếu .lib có check.')],[105,382])
p('Clock buffer/inverter chuyên dụng được characterized cho clock, nhưng không “đối xứng tuyệt đối”. Sửa pulse width phải tìm nguyên nhân; thay buffer không chữa được input clock/gating sai. Dùng integrated clock-gating cell hoặc primitive được hỗ trợ, tránh clock mux tổ hợp tự chế.')
h('Useful skew: phải xem cả hai chặng')
box('Với đường <b>A → B → C</b>, làm clock tại B trễ hơn δ (giữ clock A,C):<br/>• A→B: setup tăng δ; hold giảm δ.<br/>• B→C: setup giảm δ; hold tăng δ.<br/>B vừa là capture của chặng trước, vừa là launch của chặng sau. Đây là điểm PDF cũ nói nhầm.')
p('LVT/upsizing/rút ngắn dây thường làm nhanh cả max và min delay. Vì vậy có thể giúp setup nhưng phá hold; LVT còn tăng leakage, upsizing tăng area/input cap và có thể làm chậm cell phía trước. Không có lựa chọn nào “tự bảo đảm không hỏng hold”.')
h('Vòng ECO đáng tin cậy')
bullet('Xác nhận constraints/corner/clock/RC đúng, rồi đọc path đầy đủ; phân biệt cell delay, net delay, slew/load và clock contribution.')
bullet('Chọn thay đổi có ngân sách setup/hold; kiểm tra fan-in/fan-out và path lân cận. Sau ECO, cập nhật RC và chạy MCMM setup/hold/DRV/physical verification lại.')
p('OpenROAD repair_timing được sử dụng sau CTS với propagated clock trong tutorial; tùy chọn và giới hạn buffer/ECO cần đọc help theo phiên bản. [S10]','small')

page('3.3 • SDC, CDC, reset và multicycle')
h('CPU4 v1 không cần tự thêm multi-clock exceptions')
p('Core đã đọc chỉ có một clock. Ví dụ hai clock dưới đây là kiến thức mở rộng, không phải constraint bắt buộc cho CPU4. Hai clock cùng nguồn có quan hệ pha cần generated-clock đúng, không cắt async tùy tiện.')
code('set_clock_groups -asynchronous \\\n  -group [get_clocks clk_core] -group [get_clocks clk_axi]')
p('SDC này cắt timing giữa hai group, <b>không tạo synchronizer và không chứng minh CDC an toàn</b>. 2-FF phù hợp tín hiệu control đơn-bit đủ ổn định; pulse cần handshake/toggle, bus nhiều bit cần protocol/FIFO đảm bảo coherence, không đồng bộ từng bit tùy tiện.')
p('Async FIFO Gray-pointer còn cần giới hạn physical delay/skew theo tốc độ clock và protocol (ví dụ max-delay datapath-only/bus-skew theo tool). <b>Không chồng lệnh một cách máy móc:</b> trong Vivado, set_clock_groups ưu tiên cao hơn set_max_delay và có thể vô hiệu hóa check mong muốn. Chọn exceptions có mục tiêu, kiểm tra report constraints/exception coverage. [S11]')
h('False path và reset')
bullet('False path phải được chứng minh không cần timing trong mode đó. Mode register “chỉ ghi lúc boot” vẫn cần protocol và timing cho quá trình chuyển mode; không mặc định false-path.')
bullet('Reset bất đồng bộ: assertion không theo cạnh clock nhưng vẫn có pulse-width/physical requirements. <b>Deassertion có recovery/removal</b>; không false-path toàn reset rồi coi an toàn. Xác định đường external reset→reset synchronizer và synchronized reset→FF để giữ các check cần thiết.')
bullet('RDC cũng cần kiểm tra: hai miền reset có thể khác nhau dù cùng clock. Synchronizer giảm xác suất metastability, không cho bảo đảm tuyệt đối.')
h('Multicycle N=2 • chỉ khi chức năng thật cho phép')
code('# Cung clock/canh, capture cho phep sau 2 chu ky\nset_multicycle_path 2 -setup \\\n  -from [get_cells reg_a] -to [get_cells reg_b]\n# Khoi phuc hold ve quan he cung canh launch goc\nset_multicycle_path 1 -hold \\\n  -from [get_cells reg_a] -to [get_cells reg_b]')
p('Trong trường hợp này, setup chuyển capture từ T sang 2T; hold mặc định liên quan cạnh T. -hold 1 đưa quan hệ hold về cạnh 0 (cùng cạnh launch gốc), không phải “về chu kỳ 1”. N setup thường đi cùng N−1 hold cho ví dụ cùng clock này. [S8]')
p('Phải có enable/protocol bảo đảm capture trung gian không cần dữ liệu và source giữ đúng dữ liệu. Không dùng multicycle để che path single-cycle chậm. Với khác tần số/pha, -start/-end có thể cần thiết; đọc edge report, không áp N−1 vô điều kiện.','small')

page('3.4 • PVT và mô hình variation')
h('PVT corners không có một cặp worst/best cố định')
p('SS/Vmin/Tmax thường là ứng viên chậm; FF/Vmax/Tmin thường là ứng viên nhanh. Nhưng <b>corner thật phải theo characterized library/PDK</b>, RC corner, mode và đường cụ thể. Worst setup/hold có thể ở nhiệt độ khác; skew/variation/net RC cũng ảnh hưởng. Không dùng tên SS/FF thay cho việc đọc report.')
h('Temperature inversion: sửa đúng cơ chế vật lý')
p('Khi nhiệt độ giảm, mobility thường tăng (giúp nhanh), đồng thời độ lớn threshold voltage |Vth| thường tăng (giảm overdrive, làm chậm). Ở Vdd thấp, hiệu ứng Vth có thể thắng nên lạnh lại chậm hơn nóng. “Điện động giảm theo nhiệt độ thấp” trong PDF cũ là sai thuật ngữ và sai cơ chế. [S12]')
p('Mô hình trực giác: Id phụ thuộc mobility và (Vdd−|Vth|); không dùng công thức đơn giản này để tính delay chính xác cho FinFET. Temperature inversion không bị ràng buộc bởi mốc <28 nm tuyệt đối; phụ thuộc process, cell và Vdd. Kiểm tra các nhiệt độ/corner mà signoff methodology yêu cầu, không chỉ hai cực nếu có corner trung gian xấu hơn.')
table(['Mô hình','Hiểu đúng'],[
('OCV','Early/late derate cố định cho cell/net theo flow; ±5% chỉ ví dụ, không lấy làm số chuẩn. Flat derate có thể bảo thủ nhưng không tự bảo đảm đủ chính xác.'),('AOCV','Derate phụ thuộc path depth và có thể distance. Tính trung bình giảm phần variation ngẫu nhiên độc lập; tương quan/systematic variation không “triệt tiêu” hoàn toàn.'),('POCV / SOCV','Mô hình variation thống kê/parametric theo công cụ. Synopsys gọi POCV; SOCV là tên gặp ở hệ sinh thái khác. Hai tên không có nghĩa mọi triển khai giống nhau.'),('LVF','Liberty Variation Format: dữ liệu variation trong thư viện, không phải tên thuật toán signoff. Có early/late và moment-based LVF theo tool/library.')],[100,387])
p('Tài liệu Synopsys mô tả POCV cho 14/16 nm và nhỏ hơn; các flow tiên tiến dùng LVF/moments để tăng độ chính xác. <b>Không có luật “chip AI bắt buộc SOCV”</b>; yêu cầu do foundry, library, node và dự án phê duyệt. Không giả định mọi phân phối đều Gaussian đúng μ±3σ. [S13]')
h('MCMM và common-path pessimism')
p('MCMM bao phủ nhiều mode/corner (functional, test, voltage/frequency…). Setup thường bất lợi khi launch clock late/capture early và data late; hold ngược lại. Phần clock path chung không thể đồng thời nhanh/chậm độc lập như một giả định cực đoan; CPPR/CRPR giảm pessimism đó theo tool. Phải xem report, không chỉ cộng một derate chung.')

page('3.5–3.6 • Crosstalk, IR-drop và EM')
h('Crosstalk delay và noise là hai tình huống khác nhau')
p('Điện dung coupling Cc giữa aggressor/victim tạo tương tác. Trong mô hình chuyển mạch đồng thời đơn giản: cùng chiều giảm tải coupling hiệu dụng → có thể nhanh hơn, bất lợi hold; ngược chiều tăng tải → có thể chậm hơn, bất lợi setup. Nhưng độ thay đổi còn phụ thuộc timing window, slew, nhiều aggressor và driver; không mặc định mọi lần đều xảy ra cực trị.')
p('Victim đứng yên có thể nhận noise glitch khi aggressor chuyển mạch. Có gây lỗi hay không phụ thuộc biên độ, độ rộng, ngưỡng cell và khả năng lan truyền; không nói mọi glitch đều “lật sai toàn chip”. Clock/reset/gating net cần bảo vệ kỹ hơn.')
bullet('Giải pháp: spacing, shielding nối nguồn/đất đúng, layer assignment, reroute, buffering/driver phù hợp. Shielding cũng thêm capacitance và tốn routing; cần kiểm tra timing/RC lại.')
p('STA/SI dùng coupling parasitics và timing windows; không thể suy ra crosstalk chính xác từ RTL hay wirelength tổng. PrimeTime SI hỗ trợ phân tích SI/noise trong timing context. [S13]')
h('Phân biệt IR-drop với L·di/dt')
code('Resistive drop:  DeltaV_R = I * R\nInductive droop: DeltaV_L = L * di/dt\nDynamic power (gan dung): P = alpha * Csw * Vdd^2 * f')
p('Static IR dùng dòng trung bình/steady-state; dynamic IR xét dòng thay đổi theo thời gian và đáp ứng PDN. L·di/dt là thành phần inductive voltage droop (thường cả package/board), không gọi tất cả là “I×R”. PDN thực tế có R/L/C và resonances.')
p('AI accelerator có thể có mật độ chuyển mạch cao và activity đồng thời, gây dòng đỉnh lớn. Dòng không tự tăng “theo cấp số nhân”; phụ thuộc số khối hoạt động, switched capacitance, voltage, clock gating và workload. MCU có PDN yếu vẫn có thể gặp droop nghiêm trọng; không so chỉ theo nhãn chip.')
bullet('Droop giảm điện áp cell và có thể làm xấu timing. STA dùng một điện áp nominal không tự bao phủ mọi dynamic waveform; cần IR-aware timing hoặc margins/methodology được phê duyệt. [S13]')
bullet('Giải pháp: PDN tốt, thêm vias/straps theo rule, decap có mục tiêu, power/clock gating hoặc scheduling giảm đồng thời, kiểm tra package supply. Decap không sửa được mọi static IR problem.')
h('Đừng bỏ qua electromigration (EM)')
p('EM là độ tin cậy liên quan mật độ dòng, nhiệt độ và thời gian ở dây/via; khác IR-drop. Cần kiểm tra giới hạn DC/RMS/peak theo quy định PDK. Nguồn mạnh và nhiều vias chỉ là hướng thiết kế; vẫn cần report đo, không đủ để tuyên bố signoff.')

page('3.7 / Q14 • Bộ nhớ, Liberty và ASIC')
h('Behavioral array không quyết định loại phần cứng')
p('ROM nội dung cố định, đọc tổ hợp thường tối ưu thành logic hằng/decode/MUX, hoặc map ROM/LUT/IP phù hợp target; không mặc định thành FF. RAM 16×4 ghi đồng bộ, đọc tổ hợp có thể map sang 64 bit lưu trữ FF kèm enable/MUX nếu không có primitive/macro phù hợp; số cell sau tối ưu phải đọc synthesis report. FPGA có LUTRAM/BRAM theo pattern và device. [S14]')
box('<b>Finding và sửa đã kiểm tra:</b> baseline ROM chỉ có NOP, nạp chương trình qua task simulation-only; flatten synthesis loại bỏ toàn bộ logic chức năng. Bản sửa có ROM Fibonacci cố định, đối chiếu đủ 16 từ với assembler và boot test không dùng load_program PASS. Task preload không nạp ROM phần cứng. [S2,S5]')
p('data_memory cũng initial tất cả ô về 0 và preload bằng task testbench. FPGA có thể hỗ trợ power-up initialization theo tool/device; ASIC FF/SRAM không tự có trạng thái 0 nhờ initial. Cần reset/boot initialization/valid-bit strategy hoặc memory IP có đặc tính rõ. RAM code hiện không có reset port; reset CPU không đồng nghĩa xóa RAM. [S6]')
h('SRAM macro: thường hợp lý cho bộ nhớ lớn, không bắt buộc mọi nơi')
bullet('Macro cần views phù hợp: .lib timing, LEF abstract, GDS/OASIS physical, functional model và CDL/SPICE/LVS view theo nhà cung cấp. Xác nhận port, latency, read/write collision, power/test pins.')
bullet('Macro thường có clock cho giao tiếp synchronous, không có nghĩa phải ở clock domain riêng. Thay async RAM bằng synchronous-read SRAM có thể thêm chu kỳ: phải sửa microarchitecture/control và test lại.')
bullet('MBIST/repair thường là DFT logic bổ sung hoặc option của IP/compiler; không mặc định mọi SRAM có BIST tích hợp.')
bullet('Vị trí macro tùy connectivity, pin orientation, PDN, congestion và timing. Đặt ở biên core có thể hữu ích nhưng không bắt buộc ở rìa die; halo/channel theo PDK/flow.')
h('Liberty .lib: nhiều hơn bảng delay hai chiều')
p('Liberty chứa logic function, timing arcs, setup/hold, recovery/removal, pulse width, pin caps, điện giới hạn, power/leakage và mô hình variation nếu có. NLDM thường tra delay/slew theo input transition/output load; sequential constraint tables dùng index khác. CCS là current-source model phong phú hơn, không chỉ cùng bảng 2D như NLDM. [S13]')
p('.lib mô tả cell tại corner; không thay SPEF của dây hay LEF/GDS của hình học. “Chính xác” bị giới hạn bởi characterization, mô hình, interpolation và dữ liệu RC; không dùng .lib một góc để kết luận mọi điều kiện silicon.','small')

page('3.8 • Tcl và báo cáo theo từng công cụ')
p('Các đoạn dưới là mẫu học tập, <b>PrimeTime chưa chạy</b>; OpenSTA chỉ chạy mẫu educational trong trang 23, không phải xác nhận mọi lệnh/vendor option dưới đây. Đối chiếu help/man theo phiên bản, xác nhận collection không rỗng và units. Tcl collection API của Synopsys không tự chạy trên mọi tool.')
h('PrimeTime • top đường max delay')
code('set paths [get_timing_paths -delay_type max -max_paths 10]\nforeach_in_collection path $paths {\n  set sp [get_object_name [get_attribute $path startpoint]]\n  set ep [get_object_name [get_attribute $path endpoint]]\n  set sl [get_attribute $path slack]\n  puts "Path: $sp -> $ep | Slack: $sl (design time unit)"\n}\n# Xem timing path day du, ca min va max\nreport_timing -delay_type max -max_paths 10\nreport_timing -delay_type min -max_paths 10')
p('Không hardcode “ns” khi chưa xác nhận library/design units. -max_paths và -nworst/group behavior tùy tool/config; cần xác nhận phạm vi báo cáo để không bỏ sót nhóm path.')
h('PrimeTime • kiểm tra tải, không đoán tên attribute')
code('list_attributes -application -class net\nreport_constraints -max_capacitance -all_violators\nreport_constraints -max_transition -all_violators\n# report_net <net_name> de xem driver/load theo tool help')
p('Bỏ filter "num_pins &gt; 20" chưa xác minh. Nếu cần đếm fanout, đếm sink pin đúng chiều/kể port load và tránh double count hierarchical net; pin count gồm cả driver không đồng nghĩa fanout. Max cap dùng báo cáo điện dung, không thay bằng đếm fanout.')
h('OpenSTA / OpenROAD • khác API')
code('# Khi design, clock, library va parasitics da duoc doc\nreport_checks -path_delay max -group_path_count 10\nreport_checks -path_delay min -group_path_count 10\n# Post-CTS/post-route: dung propagated clock theo flow.\n# read_spef <extracted.spef> va kiem tra annotation coverage.')
p('Tên/options có thể đổi theo phiên bản. OpenSTA không phải PrimeTime; không copy foreach_in_collection/get_attribute của Synopsys sang mà coi chạy được. Ví dụ repair_timing thuộc OpenROAD resizer, không phải mọi phiên bản standalone OpenSTA. [S9,S10]')
h('Vt, WNS/TNS và tự động hóa')
p('Filter ref_name =~ *HVT* chỉ là naming heuristic nếu thư viện thực dùng chuỗi HVT. Vt class không thể suy ra chắc chắn từ mọi tên cell. Tự động xuất WNS/TNS theo từng setup/hold, mode/corner/group; units và số endpoint cần thống nhất. WNS=0 không chứng minh không có unconstrained paths.')
p('Script ECO nên có dry-run, log thay đổi, equivalence và kiểm tra MCMM/DRV/DRC sau sửa. Không quảng bá “tự động hóa hoàn toàn” hay phân loại root cause tuyệt đối chỉ từ regex log.')

page('4 • Phỏng vấn: câu 1–8 đã sửa')
h('Q1 • Vì sao chọn Harvard?')
p('IMEM và DMEM tách đường truy cập nên có thể fetch và truy cập data trong cùng chu kỳ của datapath này, tránh structural conflict trên một memory port dùng chung. Đó là lựa chọn cho CPU học tập, không chứng minh mọi Harvard nhanh hơn mọi von Neumann.')
h('Q2 • Vì sao lệnh 9-bit nhưng dữ liệu 4-bit?')
p('Harvard cho phép độ rộng độc lập. 9-bit dùng bit8, opcode 4-bit và operand 4-bit; imm_mode chỉ phân biệt MOV/LDI ở mã 3 trong ISA này. Dữ liệu ALU/RF là 4-bit. Đây là quyết định encoding, không phải đòi hỏi single-cycle.')
h('Q3 • RF đọc đồng bộ hay tổ hợp?')
p('Theo đặc tả CPU4, đọc tổ hợp và ghi cạnh lên. Nhờ không có thêm chu kỳ read, operand đi qua ALU rồi writeback trong một chu kỳ; vẫn có trễ đọc MUX/dây. Nếu chuyển sang RF synchronous-read thì phải đổi schedule/microarchitecture.')
h('Q4 • Vì sao LOAD/LDI ghi R0?')
p('Với encoding đang chọn, 4-bit operand dành cho toàn bộ địa chỉ 0…15 hoặc immediate 0…15; register đích là R0 ngầm định. Có thể thiết kế encoding khác hoặc lệnh dài hơn, nên không phải giới hạn toán học bắt buộc của CPU 4-bit.')
h('Q5 • Critical path ở đâu, đã tối ưu gì?')
p('Đã có STA minh họa TT trên netlist ROM Fibonacci, nhưng chưa có report SAED32/post-route. Em phân tích start/end, cell/net/clock contribution và không dùng nó để khẳng định critical path của mọi chương trình. flag_write sửa chức năng giữ cờ. CLA 4-bit/pipeline chỉ là phương án khảo sát; chỉ tuyên bố cải thiện khi có report trước/sau cùng constraints/corner.')
h('Q6 • Có sửa hold ở synthesis không?')
p('Không có luật cấm. Có flow sửa hold sớm nếu clock model đủ tin cậy, nhưng thường tập trung sau CTS vì clock skew và RC thực tế rõ hơn. Hold fix sớm có thể cần điều chỉnh lại, tăng area/power hoặc làm xấu setup; phải kiểm tra post-CTS/post-route. [S10]')
h('Q7 • Setup hay hold sau chế tạo nguy hiểm hơn?')
p('Cả hai gây lỗi. Setup single-cycle có thể có workaround giảm tần số trong phạm vi đặc tả. Hold same-edge thường không sửa được bằng hạ tần số và khó cứu hơn, có thể cần re-spin. Không nói “mọi lỗi hold chỉ vứt bỏ”; workaround phụ thuộc khả năng phần cứng và đo silicon.')
h('Q8 • Positive/negative skew?')
p('skew = clock_capture − clock_launch. Positive skew giúp setup nhưng làm xấu hold cùng đường; negative skew ngược lại trong mô hình same-clock/same-edge. Phải xem early/late, common-path correction và các chặng lân cận khi chỉnh clock.')
p('Q1–Q5 dựa trên đặc tả và RTL đã đọc [S1–S4]; không biến câu trả lời mẫu thành thành tích “em đã làm” khi chưa có artifact.','small')

page('4 • Phỏng vấn: câu 9–15 đã sửa')
h('Q9 • Core utilization nghĩa là gì?')
p('Utilization = diện tích standard cells / core hoặc placeable area theo định nghĩa tool. Có macro/blockage phải ghi mẫu số rõ. Quá cao dễ congestion/thiếu chỗ CTS-ECO; quá thấp có thể lãng phí diện tích/dây dài, nhưng tool có thể cluster cell. 40/80% không phải ngưỡng vật lý phổ quát.')
h('Q10 • Antenna effect là gì?')
p('Trong các bước plasma processing như etch, conductor nối gate có thể tích điện làm hỏng gate oxide. Rule theo PDK xét exposed conductor/gate area, layer/stage và diode protection. Layer hopping/jumper giảm antenna ratio hiệu dụng theo trình tự chế tạo; không có nghĩa cắt đứt kết nối cuối. Antenna diode là cell bảo vệ theo PDK, không mặc định mọi diode luôn nối trực tiếp GND.')
h('Q11 • Sửa setup mà giữ hold thế nào?')
p('Chọn ECO từ report: resize/Vt swap, giảm net delay, chỉnh placement/logic; chúng có thể giảm cả min delay nên kiểm tra hold mọi corner. Useful skew delay clock ở B giúp setup A→B nhưng hại hold A→B và setup B→C. Chỉ chấp nhận khi đủ margin và đã chạy lại MCMM/DRV/physical checks.')
h('Q12 • Vì sao phải nhiều corners?')
p('Delay phụ thuộc process, Vdd, temperature, RC, variation và mode. SS/Vmin/hot và FF/Vmax/cold chỉ là ứng viên thường gặp; inversion có thể làm cold chậm ở Vdd thấp. Chọn corners theo library/PDK và signoff methodology, không thuộc lòng một “worst corner” cho mọi đường.')
h('Q13 • Vì sao AI accelerator có thể droop lớn?')
p('Activity song song và switched capacitance lớn tạo dòng đỉnh; phụ thuộc workload/gating/PDN, không tăng theo cấp số nhân mặc định. Tách resistive IR=I×R khỏi inductive droop=L×di/dt. Kiểm tra dynamic supply và timing impact, không chỉ STA nominal-voltage.')
h('Q14 • .lib làm gì trong STA?')
p('Cung cấp timing/power/electrical models của cell tại corner, gồm arcs, setup/hold, recovery/removal, pulse-width… NLDM tra delay/slew; CCS là current-source model phong phú hơn; LVF thêm variation. Cần netlist/SDC và RC/SPEF để STA thiết kế, không chỉ .lib. [S13]')
h('Q15 • Ứng dụng Tcl hàng ngày thế nào?')
p('Em sẽ chuẩn hóa setup chạy/report, kiểm tra clocks/exceptions/unconstrained paths, thống kê WNS/TNS và DRV theo scenario, tạo báo cáo diff giữa các run. ECO tự động cần review/dry-run, equivalence và verify lại. Lệnh/attributes theo PrimeTime, ICC2 hay Innovus không hoàn toàn giống nhau.')
box('<b>Câu nói an toàn khi phỏng vấn:</b> “Đây là đặc tả/giả thuyết hiện tại; em sẽ xác nhận bằng test hoặc report này.” Ghi rõ commit/tool/PDK và corner; không viện “FPT yêu cầu” khi chưa có JD.')

page('5 • Nhật ký hiệu đính và giới hạn')
table(['Vị trí PDF cũ','Điều đã sửa / bổ sung'],[
('1.1 / Q1–Q2','Bus contention → bottleneck/structural hazard; Harvard cho độ rộng độc lập; bit8 không phải immediate mode toàn ISA.'),('1.2 / 1.3','ALU có carry nội bộ; CPU chỉ lưu Z/N; HALT ở cpu_top. Thêm reset semantics, latch/implicit-net và flag_write là chức năng.'),('1.4 / Q5','Bỏ khẳng định carry-chain là critical path; thêm LOAD/branch candidates, MUX/wire/clock và cần STA chứng minh.'),('3.1 / Q7–Q8','Bổ sung tcq_min/max, uncertainty riêng, phạm vi same-edge; bỏ “hold luôn vứt bỏ”, tăng Vdd chỉ trong giới hạn.'),('3.2 / Q11','Clock cells không đối xứng tuyệt đối; LVT/upsizing có thể phá hold; sửa useful-skew cùng đường/chặng sau.'),('3.3','Multicycle hold về cùng cạnh gốc; false-path reset không được xóa check deassert; CDC multi-bit và exception precedence.'),('3.4 / Q12','Mobility và |Vth| cạnh tranh; không có mốc node/PVT tuyệt đối; POCV/SOCV/LVF và MCMM/CPPR.'),('3.5 / 3.6 / Q13','Crosstalk phụ thuộc timing window; bỏ “mọi glitch phá chip”; bỏ cấp số nhân, tách IR với inductive droop và thêm EM.'),('3.7 / Q14','ROM hằng vs RAM FF/IP; macro không bắt buộc ở rìa, MBIST không mặc định; initial/ROM preload ASIC; NLDM khác CCS.'),('3.8 / Q15','Bỏ num_pins chưa xác minh; max cap phải report; units/Vt naming theo library; PrimeTime chưa chạy; OpenSTA educational ghi riêng.'),('Lộ trình / Q6/Q9/Q10','Tap/endcap; sửa hold sau CTS; SPEF/post-route MCMM; DRC/LVS không đủ signoff; utilization theo tool/PDK; plasma etch.'),('Tiêu đề / toàn file','Bỏ tuyên bố “chuẩn FPT” chưa có JD; thêm phần cờ, test toán học, nguồn và mức xác minh.')],[100,387])
h('Nhận xét bạn gửi cũng cần hiểu có điều kiện')
p('Z/N/C/V là bộ phổ biến, không phải “bộ chuẩn” bắt buộc. ROM không <i>luôn</i> thành logic: mapping tùy implementation/target. “Thêm max_delay bên cạnh clock_groups” không đúng nếu exception ưu tiên cao đã cắt mất check. N−1 hold chỉ là mẫu thông dụng trong trường hợp clock/edge phù hợp.')
p('Bản sửa giữ CPU4 v1 là Z/N; C/V, ADC, signed comparisons là kiến thức/mở rộng có nhãn. Repository đã được sửa trên nhánh audit; ISA vẫn là Z/N. Kết quả chạy và giới hạn ở trang 19–24. Code địa phương của bạn có thể khác baseline GitHub; đối chiếu trước khi học như hành vi hardware hiện tại.','small')

page('6 • Nguồn và bước xác minh tiếp')
p('Nguồn tra cứu ngày 08/10/2026. [S2–S6] đã đọc nguyên văn file qua GitHub MCP tại commit cố định. Nguồn web dùng excerpt được trả về; trang Yosys/OpenROAD tutorial tải toàn trang gặp lỗi nên không coi đã kiểm tra đầy đủ mọi option/version. Nguồn baseline khác bản sửa; kiểm thử bổ sung và nhánh GitHub được nêu ở trang 19–24. Lệnh vendor/PDK phải xác nhận trong môi trường thật.','small')
base='https://github.com/lengoctuong2005/cpu4-custom-architecture/blob/5f2e19d687a3b77410542dc3828f8fbe8a98f3bd/'
sources=[
('S1','CPU4 ISA v1 — đặc tả và verification revision trong repo', 'https://github.com/lengoctuong2005/cpu4-custom-architecture/blob/audit/cpu4-v1-verified-2026-10-08/docs/isa.md'),
('S2','RTL top: cờ lưu, HALT, datapath, task mô phỏng',base+'rtl/cpu_top.v'),
('S3','ALU: result/Z/N/carry, no-borrow SUB/DEC',base+'rtl/alu_4bit.v'),
('S4','Control unit: opcode, flag_write và branch',base+'rtl/control_unit.v'),
('S5','Instruction memory: initial 0 và read tổ hợp',base+'rtl/instruction_memory.v'),
('S6','Data memory: initial 0, synchronous write, async read',base+'rtl/data_memory.v'),
('S7','Arm: Condition Codes 1 — flags and comparison conditions','https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/condition-codes-1-condition-flags-and-codes'),
('S8','Altera/Intel: Multicycle Path Analysis','https://docs.altera.com/r/docs/683068/18.1/intel-quartus-prime-standard-edition-user-guide/multicycle-path-analysis'),
('S9','OpenROAD: flow overview, timing/extraction/final checks','https://openroad.readthedocs.io/en/latest/main/README.html'),
('S10','OpenROAD Flow Scripts Tutorial: repair_timing after CTS','https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html'),
('S11','AMD UG903: clock groups override set_max_delay','https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Recommended-Asynchronous-Clock-Groups-Constraints'),
('S12','Embedded Computing: temperature inversion / mobility / Vth','https://embeddedcomputing.com/technology/analog-and-power/power-semiconductors-wireless-charging/effect-of-temperature-inversion-on-lower-nodes'),
('S13','Synopsys: PrimeTime datasheet — POCV/LVF/CCS/SI','https://www.synopsys.com/content/dam/synopsys/implementation&signoff/datasheets/primetime-ds.pdf'),
('S14','Yosys: memory handling and mapping patterns','https://yosyshq.readthedocs.io/projects/yosys/en/v0.49/using_yosys/synthesis/memory.html')]
for sid,label,url in sources:
    p(f'<b>[{sid}] {escape(label)}</b><br/><link href="{escape(url)}" color="#146492">Mở nguồn</link>','small')
h('Trước khi coi CPU4/flow là “đã xác minh”')
bullet('Chốt commit của code địa phương; chạy unit + differential tests và strict lint. Xác minh ROM program/initialization khi synthesis; lưu mapped netlist và memory report.')
bullet('Chạy STA có SDC/.lib/RC đúng và không bỏ sót path; post-route với SPEF/propagated clocks; lưu reports và artifact provenance. JD FPT cần bản thật để chỉnh nội dung ứng tuyển.')
p('Quy tắc học: hiểu điều kiện áp dụng → làm ví dụ → chạy test/report → mới khẳng định. Không dùng PDF này để thay thế datasheet/PDK/tool manual hoặc kết quả đo.','small')


page('7.1 • Kết quả kiểm thử thực tế')
p('Baseline repo: 5f2e19d687a3b77410542dc3828f8fbe8a98f3bd. Kết quả dưới đây là lệnh đã chạy trong sandbox Linux, không phải PASS banner chép từ README. Log, vectors, trace, manifest và source patch có trong gói bằng chứng.')
table(['Hạng mục','Kết quả và phạm vi'],[
('Baseline make verify','PASS: 4 module unit benches; 4 demos; 14 directed + 2.048 exhaustive ALU vector.'),
('Python regression','PASS: 10 test methods; parser/HEX/timeout/reset; đủ 512 raw decodings; mọi cặp ADD/MUL 4-bit.'),
('Decoder RTL','PASS: 512 từ lệnh × 4 tổ hợp Z/N = 2.048 kiểm tra; toàn bộ output control.'),
('Differential CPU','PASS: 2.767 scenario, 79.324 cạnh clock; cả trước/sau sửa. Sau sửa có clk_en/stall.'),
('Boot ROM','PASS: boot Fibonacci không nạp chương trình bằng task; OUT=8, HALT=1.'),
('FPGA logic','PASS: reset, bounce, giữ nút, mỗi press một pulse, chuyển mode, auto boot. Không phải board test.'),
('Strict net / legacy','PASS: default_nettype none elaboration core; wrapper legacy elaborate được.'),
('Negative tests','DETECTED: XOR→OR và ghi cờ vô điều kiện; simulator exit=1 cho cả hai.'),
('Formal ALU','PASS: 7/7 equivalence bit cells proven, 0 unproven; ALU baseline và bản width-explicit.'),
('C/V toán học','PASS: 512 ADD/SUB; 2.560 điều kiện compare. V là lý thuyết, không thêm vào CPU ISA.')],[103,384])
h('Công cụ và môi trường')
p('Icarus Verilog 12.0 (v12_0), Python '+METRICS['python_version']+'. '+METRICS['yosys_version']+'; '+METRICS['sta_version']+'. Icarus/Yosys/OpenSTA được build native khi package hệ thống không có; formal ALU còn được kiểm tra bằng Yosys WASM 0.69. Phiên bản và hash file nằm trong manifest.')
box('<b>PASS có phạm vi:</b> simulation so sánh trạng thái logic; formal ở đây chỉ cho ALU; không có xác nhận bộ CPU bằng Formality, FPGA hardware timing hoặc ASIC signoff.')

page('7.2 • Lỗi tái tạo được và bản sửa')
table(['Baseline đã quan sát','Sửa và test hồi quy'],[
('Icarus -Wall: 3 implicit-net warnings','Khai báo zero/negative/carry tường minh; strict-net elaboration không còn warning.'),
('LDI\t#5 bị từ chối; label có comment không resolve','Tokenizer theo whitespace, bỏ ; và // trước pass1/pass2; label-only/inline label đều được kiểm tra.'),
('HEX có comment/dòng trống bị lệch địa chỉ','Đếm các word hợp lệ, không đếm dòng vật lý; 131 đặt ở ROM[0], không phải ROM[2].'),
('HEX 200 bị mask âm thầm thành 000','Reject >9-bit, ảnh >16 words, syntax sai và ảnh rỗng; tests xác nhận ValueError.'),
('Timeout đặt halted=True và CLI thành công','TimeoutError, không đổi HALT; CLI trả lỗi khác 0.'),
('Emulator báo saved C nhưng core chỉ lưu Z/N','CPU model chỉ có Z/N; carry vẫn nằm trong helper ALU cho unit tests.'),
('ROM generic là NOP hằng','Default ROM Fibonacci chứa chương trình khi synthesis; đủ16 từ khớp assembler; boot without helper PASS.'),
('FPGA dùng generated/button-controlled clock','Core thêm clk_en; toàn bộ side effects gated. CLOCK_50 duy nhất; sync/debounce inputs; one press/one enable.'),
('README/SDC/ICC2 nói quá hoặc sai mapping','README phân biệt verified/template; bỏ blanket false-path reset; min/max I/O; late=maxTLU, early=minTLU.')],[209,278])
p('Bốn demo gốc đã PASS; bản sửa không được mô tả như vừa cứu một ALU sai. Lỗi chính nằm ở toolchain edge cases, mức bằng chứng, ROM synthesis và interface clock wrapper. Một số chỗ đã có sửa ở baseline mới hơn kế hoạch cũ, nên audit này dùng code hiện tại làm chuẩn.')
p('load_program helper nay báo lỗi mở file và xóa ROM trước khi nạp ảnh ngắn, tránh instruction cũ còn sót. Helper vẫn bị loại khi synthesis. RAM reset/ASIC power-up và PDK tap insertion vẫn chưa được giải quyết bằng các test logic này.')

page('7.3 • Differential: kiểm gì ở mỗi cạnh?')
box('<b>State compared:</b> PC, R0, R1, R2, R3, Z, N, OUT, RAM[0]…RAM[15] và halt_out. Lấy mẫu sau NBA settle, không so tại cạnh clock đang cập nhật.')
table(['Nhóm scenario','Số / nội dung'],[
('Raw instruction universe','2.048: 512 word × 4 initial flags. RF/RAM/OUT khởi tạo giả ngẫu nhiên bằng seed0xC4; thực thi1 cạnh mỗi case.'),
('ADD + MUL algorithms','512: 256 input pairs cho ADD và 256 cho MUL. Mỗi scenario100 cạnh, gồm ổn định sau HALT.'),
('FIB + FLAG demos','2 scenario ×100 cạnh; Python còn assert toàn sequence Fibonacci 1,1,2,3,5,8.'),
('Directed / PC wrap','5: overflow/JN, flag preservation, RAM0/15, repeated OUT, PC15→0.'),
('Random programs','200 seed0…199; 16 raw words/ROM, random RF/RAM/flags/OUT, 128 cạnh và pattern clk_en có hold.')],[133,354])
p('Tổng 2.767 scenario / 79.324 cạnh. Baseline được chạy cùng harness nhưng mọi enable=1 vì core cũ không có cổng clk_en; bản sau sửa mới kiểm tra stall/enable. Không nói baseline đã kiểm tra một interface chưa tồn tại.')
h('Oracle và giới hạn')
bullet('Python import ISA chung để tránh opcode drift; ALU được đối chiếu thêm bằng số nguyên độc lập, không chỉ copy cùng biểu thức cắt 4-bit. Hai deliberate mutants chứng minh test có khả năng báo lỗi.')
bullet('State injection vào DUT là testbench-only để mở rộng đầu vào; không khẳng định các state đó đều reachable từ reset. Random pass không chứng minh mọi chương trình/trajectory.')
bullet('HALT output là combinational decode của lệnh tại PC hiện tại. Emulator halted là trạng thái dừng sau step; harness đối chiếu halt_out theo decode ROM, tránh so hai khái niệm khác nhau.')
h('Tái tạo / debug failure')
code('make verify\npython tests/differential.py --out build/verification\n# Fail in ten scenario/seed/cycle va state got/want.\n# vectors.txt va trace.txt duoc luu de tai lap.')
p('Timeout, mismatch hoặc X/Z trong state đều làm test fail. Đây là kiểm tra chức năng zero-delay RTL, không mô phỏng gate-delay/SDF hay metastability analog.')

page('7.4 • Synthesis và formal đã chạy')
p(METRICS['synthesis_intro'])
table(['Đo / kiểm tra','Kết quả thực tế'],[
('Baseline flatten ROM=NOP','0 functional cells; 6 scopeinfo metadata cells. Outputs bị tối ưu thành hằng. Có JSON/log thật.'),
('Generic Yosys/ABC',METRICS['generic_result']),
('Mapped educational netlist',METRICS['mapped_result']),
('Cell area',METRICS['area_result']),
('Gate boot simulation',METRICS['gate_result']),
('Formal ALU',METRICS['formal_result'])],[142,345])
h('Diễn giải đúng số cell')
p('ROM fixed-program cho phép synthesis bỏ opcode/path/RAM/cờ không dùng bởi chương trình đó. Vì vậy số FF của netlist Fibonacci không bắt buộc bằng PC4 + RF16 + RAM64 + flags2 + OUT4 =90 bit trạng thái mô phỏng tổng quát. Không dùng FF count sau tối ưu để suy ra ISA đã thêm/bớt cờ.')
p('ROM là logic hằng/decode/IP tùy target; RAM có thể FF-map hoặc macro-map. Generic cell count không phải physical area; mapped standard-cell area không phải core/die area. Nangate45 không phải SAED32, nên không chuyển kết quả PPA giữa hai thư viện.')
h('Phạm vi formal')
p('equiv_make + equiv_simple + equiv_status -assert chứng minh 4 result bits + Z + N + carry =7 output bit tương đương giữa ALU baseline và ALU sửa width. Đây là proof combinational cho ALU, không phải formal proof toàn CPU, ROM boot, clock wrapper hoặc gate→PnR.')
h('Artifact bắt buộc')
code('make synth\nLIBERTY=/path/to/Nangate_typical.lib \\\n  python tests/run_synthesis.py\n# Logs + JSON + netlist phai ton tai; khong chi xem exit0.')
p('Warnings còn lại: translate_off và scan/gating models không dùng. Gate test xác nhận mọi cell instantiated có model. Lần thử WASM ABC không tạo đủ artifact nên không tính PASS; native mapping, baseline no-ABC và formal ALU có output/proof riêng.','small')

page('7.5 • STA minh họa: kết quả và giới hạn')
p(METRICS['sta_intro'])
table(['Điều kiện / kết quả','Giá trị'],[
('Library','NangateOpenCellLibrary typical: 1,10V /25°C; time_unit=1ns; capacitance_unit=1fF.'),
('Clock / I/O giả định','Ideal clock T=10ns; Usetup0,2ns/Uhold0,05ns; I/O max1ns/min0,1ns; output load10fF.'),
('Setup worst slack',METRICS['setup_slack']),
('Min / hold / removal',METRICS['hold_slack']),
('TNS / electrical checks',METRICS['tns_drv']),
('Đường max xấu nhất trong report',METRICS['critical_path']),
('STA run status',METRICS['sta_run_status'])],[146,341])
box('<b>Không suy ra “100MHz silicon PASS”.</b> Chưa có placement/routing, SPEF, CTS/propagated clocks, RC corners, MCMM/OCV/SI, supply droop, foundry/library approval hoặc board I/O constraints. STA này là bài tập cell-delay một góc, không signoff.')
p('Netlist đã specialize cho ROM Fibonacci; đường báo cáo không đại diện mọi chương trình hay generic Harvard datapath. Không áp kết quả này cho LOAD nếu LOAD/RAM đã bị ROM-specific optimization bỏ đi.')
h('Cách đọc và kiểm chứng tiếp')
bullet('Slack âm là finding của mô hình đang dùng, không tự chứng minh silicon lỗi; slack dương cũng không chứng minh signoff. Xác nhận constraints, corner, launch/capture clock, arc và parasitic trước khi ECO.')
bullet('Hold với clock ideal và không có wire RC chỉ mang tính sơ bộ. Sau CTS/post-route phải chạy lại; không sửa hold bằng hạ tần số, không dùng false-path/multicycle để giấu vi phạm.')
code('LIBERTY=/path/to/Nangate_typical.lib \\\n  sta -exit tools/sta_educational.tcl\n# Kiem tra Error/Warning, path coverage va report units.\n# PDK/SAED32 + SPEF + real SDC can cho ket luan ASIC.')
p('SHA256 library: 8d540a4d4cf6d09d27c87ad067857a9c0c2eeb023ab7a56e058cd3113db4e9b1. File library không phân phối trong gói bằng chứng; URL/provenance được lưu.','small')

page('7.6 • GitHub, tái tạo và phần chưa hoàn tất')
p('<b>Nhánh:</b> audit/cpu4-v1-verified-2026-10-08. Không merge vào main trong lần audit này. Source, tests, CI, ROM/wrapper và tài liệu được giao qua pull request để review.')
p('<b>Pull request:</b> <link href="'+METRICS['pr_url']+'" color="#146492">'+escape(METRICS['pr_url'])+'</link>')
p('<b>RTL/test commit kiểm thử:</b> '+METRICS['source_commit']+'. Source SHA256 và log trong evidence manifest giúp phân biệt code đã test với thay đổi sau này.')
h('Một pipeline, fail thật')
code('git checkout audit/cpu4-v1-verified-2026-10-08\nmake verify\nmake synth\npip install -r requirements-docs.txt\npython tools/build_learning_pdf.py')
p('CI được cập nhật để assemble, chạy test sâu, kiểm tra generated HEX và synthesis smoke; <b>local PASS không đồng nghĩa GitHub Actions đã xanh</b>. Xem trạng thái Actions ở PR và rerun theo runner/tool phiên bản đó.')
table(['Chưa chạy / còn cần','Điều kiện hoàn tất'],[
('Quartus + FPGA board','Compile/TimeQuest, I/O timing, synchronizer recognition, reset release, resource usage, bitstream + board test/video/log.'),
('Synopsys ASIC / formal CPU','Tool/license/PDK hợp lệ; DC + Formality setup; memory init strategy; equivalent reference/implementation ROM.'),
('Physical/signoff','Qualified tap/endcaps, PDN/EM/IR, CTS hold fix, routing/SPEF, MCMM/variation/SI, foundry DRC/LVS/ERC/antenna/density.'),
('Nội dung ứng tuyển FPT','Đối chiếu JD thật; không coi lộ trình/tài liệu là chứng nhận yêu cầu tuyển dụng.')],[140,347])
box('<b>Đã hoàn tất:</b> bản học tập hiệu đính + functional audit có bằng chứng + patch GitHub. <b>Chưa hoàn tất:</b> FPGA hardware validation và ASIC signoff. Không đổi ISA thành 4 cờ chỉ để giống một bộ cờ phổ biến.')
p('Gói bằng chứng kèm PDF chứa log, summaries, trace/vectors và hash/source patch; không chứa proprietary PDK hay license credentials. Học từ trang4–5 trước, rồi tái tạo các test trang19–24.','small')

class NumberedCanvas(canvas.Canvas):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.states=[]
    def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
    def save(self):
        n=len(self.states)
        for s in self.states:
            self.__dict__.update(s)
            self.setStrokeColor(HexColor('#D8E3E9'));self.setLineWidth(.5);self.line(54,48,541,48)
            self.setFont('Arial',9);self.setFillColor(HexColor('#61676E'))
            self.drawString(54,33,'CPU4 • Bản hiệu đính học tập | 08/10/2026')
            self.drawRightString(541,33,f'{self._pageNumber} / {n}')
            self.setFont('Arial',9);self.drawString(54,809,'CPU4 / PHYSICAL DESIGN / STATIC TIMING ANALYSIS')
            super().showPage()
        super().save()
doc=SimpleDocTemplate(str(D/'CPU4_LEARNING_ROADMAP_VERIFIED.pdf'),pagesize=(595.28,841.89),leftMargin=54,rightMargin=54.28,topMargin=55,bottomMargin=63,title='CPU4 — Physical Design & STA | Bản hiệu đính',author='Lê Ngọc Tường | Bản rà soát hỗ trợ học tập')
doc.build(story,canvasmaker=NumberedCanvas)
(D/'page_titles.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2))
print('PDF created; intended pages:',len(titles))
