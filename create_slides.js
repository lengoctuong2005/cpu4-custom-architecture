const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Antigravity AI';
pres.title = 'Thiet ke CPU 4-Bit dung Quy trinh Thiet ke Mach so';

// Theme Colors (no # prefix)
const COLOR_PRIMARY_DARK = "1E2761";   // Midnight Navy
const COLOR_SECONDARY_LIGHT = "CADCFC"; // Ice Blue
const COLOR_WHITE = "FFFFFF";
const COLOR_TEXT_DARK = "1A1A1A";
const COLOR_TEXT_MUTED = "4A4A4A";
const COLOR_ACCENT = "39A78E";          // Mint/Teal accent
const COLOR_CARD_BG = "F4F7FC";         // Light gray-blue for cards

// Helper to create slides with consistent styles
function addSlideHeader(slide, titleText, isDark = false) {
    slide.addText(titleText, {
        x: 0.6,
        y: 0.4,
        w: 8.8,
        h: 0.6,
        fontSize: 24,
        fontFace: "Georgia",
        color: isDark ? COLOR_WHITE : COLOR_PRIMARY_DARK,
        bold: true,
        margin: 0
    });
}

// -------------------------------------------------------------
// SLIDE 1: Title Slide (Dark Background)
// -------------------------------------------------------------
let slide1 = pres.addSlide();
slide1.background = { color: COLOR_PRIMARY_DARK };

// Accent shapes
slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0.6,
    y: 1.8,
    w: 0.1,
    h: 2.2,
    fill: { color: COLOR_ACCENT }
});

slide1.addText("THIẾT KẾ CPU 4-BIT", {
    x: 0.8,
    y: 1.8,
    w: 8.5,
    h: 0.8,
    fontSize: 40,
    fontFace: "Georgia",
    color: COLOR_WHITE,
    bold: true,
    margin: 0
});

slide1.addText("Dùng Quy trình Thiết kế Mạch số (RTL Flow)", {
    x: 0.8,
    y: 2.7,
    w: 8.5,
    h: 0.6,
    fontSize: 20,
    fontFace: "Calibri",
    color: COLOR_SECONDARY_LIGHT,
    bold: false,
    margin: 0
});

slide1.addText("Báo cáo Đồ án Môn học: Thiết kế Vi mạch Điện tử\nĐề tài số 7 — Mô phỏng kiểm thử RTL (Verilog)", {
    x: 0.8,
    y: 3.8,
    w: 8.5,
    h: 1.0,
    fontSize: 14,
    fontFace: "Calibri",
    color: COLOR_WHITE,
    italic: true,
    margin: 0
});


// -------------------------------------------------------------
// SLIDE 2: Tổng quan & Đề tài (Light Background)
// -------------------------------------------------------------
let slide2 = pres.addSlide();
slide2.background = { color: COLOR_WHITE };
addSlideHeader(slide2, "1. Tổng quan Kiến trúc CPU 4-bit");

// Left Column: Key Features Cards
slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.3, w: 4.2, h: 3.8,
    fill: { color: COLOR_CARD_BG },
    line: { color: COLOR_SECONDARY_LIGHT, width: 1 }
});

slide2.addText([
    { text: "Đặc tả Kiến trúc (Specifications):\n\n", options: { bold: true, fontSize: 16, color: COLOR_PRIMARY_DARK } },
    { text: "• Kiến trúc Harvard: ", options: { bold: true, fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "ROM (Chỉ lệnh) & RAM (Dữ liệu) tách biệt.\n", options: { fontSize: 13, color: COLOR_TEXT_MUTED } },
    { text: "• Chu kỳ Đơn (Single-cycle): ", options: { bold: true, fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "Mỗi lệnh thực thi hoàn tất trong đúng 1 chu kỳ xung clock.\n", options: { fontSize: 13, color: COLOR_TEXT_MUTED } },
    { text: "• Lõi dữ liệu 4-bit: ", options: { bold: true, fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "Độ rộng thanh ghi, ALU và RAM dữ liệu là 4-bit.\n", options: { fontSize: 13, color: COLOR_TEXT_MUTED } },
    { text: "• Từ lệnh 8-bit: ", options: { bold: true, fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "Opcode 4-bit + Toán hạng 4-bit.\n", options: { fontSize: 13, color: COLOR_TEXT_MUTED } },
    { text: "• Tập thanh ghi: ", options: { bold: true, fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "4 thanh ghi đa năng R0–R3 (4-bit). R0 dùng làm accumulator cho LOAD/STORE.", options: { fontSize: 13, color: COLOR_TEXT_MUTED } }
], { x: 0.8, y: 1.5, w: 3.8, h: 3.4, margin: 0 });

// Right Column: Program Model card
slide2.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.3, w: 4.2, h: 3.8,
    fill: { color: COLOR_PRIMARY_DARK }
});

slide2.addText([
    { text: "Mô hình Lập trình & Tài nguyên:\n\n", options: { bold: true, fontSize: 16, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Program Counter (PC): ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "4-bit, trỏ đến 16 địa chỉ ô nhớ ROM.\n\n", options: { fontSize: 13, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Bộ nhớ ROM chỉ lệnh: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Kích thước 16 x 8-bit.\n\n", options: { fontSize: 13, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Bộ nhớ RAM dữ liệu: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Kích thước 16 x 4-bit.\n\n", options: { fontSize: 13, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Các cờ trạng thái ALU: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Cờ Zero (Z) báo kết quả bằng 0; cờ Negative (N) báo kết quả âm.", options: { fontSize: 13, color: COLOR_SECONDARY_LIGHT } }
], { x: 5.4, y: 1.5, w: 3.8, h: 3.4, margin: 0 });


// -------------------------------------------------------------
// SLIDE 3: Tập lệnh ISA (Light Background)
// -------------------------------------------------------------
let slide3 = pres.addSlide();
slide3.background = { color: COLOR_WHITE };
addSlideHeader(slide3, "2. Tập lệnh (Instruction Set Architecture - ISA)");

slide3.addText("Từ lệnh 8-bit được chia thành: Opcode [7:4] (4-bit) và Operand [3:0] (4-bit).", {
    x: 0.6, y: 1.0, w: 8.8, h: 0.4, fontSize: 13, color: COLOR_TEXT_MUTED, italic: true
});

// ISA Table
slide3.addTable([
    [
        { text: "Lệnh", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY_DARK } } },
        { text: "Mã máy (Bin)", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY_DARK } } },
        { text: "Toán hạng", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY_DARK } } },
        { text: "Mô tả chức năng", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY_DARK } } }
    ],
    ["LOAD addr", "0001", "addr (4-bit)", "Nạp giá trị từ RAM[addr] vào thanh ghi tích lũy R0"],
    ["STORE addr", "0010", "addr (4-bit)", "Lưu giá trị từ thanh ghi R0 vào RAM[addr]"],
    ["ADD Rd, Rs", "0011", "Rd (2-bit), Rs (2-bit)", "Cộng thanh ghi: R[Rd] = R[Rd] + R[Rs]"],
    ["SUB Rd, Rs", "0100", "Rd (2-bit), Rs (2-bit)", "Trừ thanh ghi: R[Rd] = R[Rd] - R[Rs]"],
    ["MOV Rd, Rs", "0101", "Rd (2-bit), Rs (2-bit)", "Copy dữ liệu: R[Rd] = R[Rs]"],
    ["JMP addr", "0110", "addr (4-bit)", "Nhảy không điều kiện: PC = addr"],
    ["JZ addr", "0111", "addr (4-bit)", "Nhảy nếu cờ Zero bật (Z=1): PC = addr"],
    ["OUT Rs", "1000", "Rs (2-bit)", "Xuất giá trị của thanh ghi Rs ra cổng OUT"],
    ["HALT", "1111", "Không có", "Dừng chương trình (đóng băng PC)"]
], {
    x: 0.6, y: 1.5, w: 8.8, h: 3.6,
    colW: [1.2, 1.2, 1.6, 4.8],
    border: { pt: 1, color: COLOR_SECONDARY_LIGHT },
    valign: "middle",
    align: "left",
    fontSize: 11
});


// -------------------------------------------------------------
// SLIDE 4: Sơ đồ khối Datapath (Light Background)
// -------------------------------------------------------------
let slide4 = pres.addSlide();
slide4.background = { color: COLOR_WHITE };
addSlideHeader(slide4, "3. Thiết kế Datapath (Đường đi dữ liệu)");

// Visual representation using shapes to mimic a flow/architecture
// PC -> ROM -> Register File -> ALU -> RAM
const blockY = 2.2;
const blockH = 1.2;
const blockW = 1.4;

const blocks = [
    { name: "Program Counter", x: 0.6, desc: "Trỏ địa chỉ lệnh (4-bit)" },
    { name: "Instruction ROM", x: 2.4, desc: "Chứa chương trình (8-bit)" },
    { name: "Register File", x: 4.2, desc: "4 thanh ghi R0-R3 (4-bit)" },
    { name: "ALU 4-bit", x: 6.0, desc: "Cộng, trừ & tính cờ Z, N" },
    { name: "Data Memory", x: 7.8, desc: "RAM lưu dữ liệu (16x4)" }
];

blocks.forEach((b, idx) => {
    // Draw Box
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: b.x, y: blockY, w: blockW, h: blockH,
        fill: { color: COLOR_CARD_BG },
        line: { color: COLOR_PRIMARY_DARK, width: 1.5 }
    });
    
    // Title inside box
    slide4.addText(b.name, {
        x: b.x + 0.05, y: blockY + 0.1, w: blockW - 0.1, h: 0.4,
        fontSize: 12, fontFace: "Calibri", color: COLOR_PRIMARY_DARK, bold: true, align: "center"
    });
    
    // Description inside box
    slide4.addText(b.desc, {
        x: b.x + 0.05, y: blockY + 0.5, w: blockW - 0.1, h: 0.6,
        fontSize: 10, fontFace: "Calibri", color: COLOR_TEXT_MUTED, align: "center"
    });

    // Arrow to next (except last)
    if (idx < blocks.length - 1) {
        slide4.addShape(pres.shapes.LINE, {
            x: b.x + blockW, y: blockY + (blockH/2), w: 0.4, h: 0,
            line: { color: COLOR_ACCENT, width: 2 }
        });
    }
});

// Out Port indicator
slide4.addShape(pres.shapes.OVAL, {
    x: 6.2, y: 3.8, w: 1.0, h: 1.0,
    fill: { color: COLOR_ACCENT },
    line: { color: COLOR_WHITE, width: 1 }
});
slide4.addText("Cổng OUT", {
    x: 6.2, y: 4.1, w: 1.0, h: 0.4,
    fontSize: 11, fontFace: "Calibri", color: COLOR_WHITE, bold: true, align: "center"
});
// Arrow from ALU to OUT
slide4.addShape(pres.shapes.LINE, {
    x: 6.7, y: blockY + blockH, w: 0, h: 0.4,
    line: { color: COLOR_ACCENT, width: 2 }
});

slide4.addText("Mạch thiết kế theo mô hình Single-cycle: trong 1 chu kỳ xung clock, lệnh được nạp từ ROM, giải mã tại Control Unit, đọc dữ liệu từ thanh ghi, tính toán qua ALU, ghi ngược lại thanh ghi hoặc RAM, và PC tăng lên 1.", {
    x: 0.6, y: 4.8, w: 8.8, h: 0.6, fontSize: 11, color: COLOR_TEXT_MUTED, italic: true
});


// -------------------------------------------------------------
// SLIDE 5: Khối điều khiển Control Unit (Light Background)
// -------------------------------------------------------------
let slide5 = pres.addSlide();
slide5.background = { color: COLOR_WHITE };
addSlideHeader(slide5, "4. Khối điều khiển (Control Unit)");

// Left panel: Description
slide5.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.3, w: 3.0, h: 3.8,
    fill: { color: COLOR_PRIMARY_DARK }
});

slide5.addText([
    { text: "Nhiệm vụ của CU:\n\n", options: { bold: true, fontSize: 16, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Giải mã Opcode: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Nhận 4 bit cao của lệnh [7:4] đưa vào mạch giải mã tổ hợp.\n\n", options: { fontSize: 12, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Sinh tín hiệu điều khiển: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Sinh các tín hiệu chọn đường multiplexer, cho phép ghi RAM (mem_write), ghi thanh ghi (reg_write).\n\n", options: { fontSize: 12, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Điều khiển rẽ nhánh: ", options: { bold: true, fontSize: 13, color: COLOR_WHITE } },
    { text: "Phối hợp với cờ Z từ ALU để sinh tín hiệu nhảy PC (pc_src).", options: { fontSize: 12, color: COLOR_SECONDARY_LIGHT } }
], { x: 0.8, y: 1.5, w: 2.6, h: 3.4, margin: 0 });

// Right table: Control Signals table
slide5.addTable([
    [
        { text: "Lệnh", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "RegWr", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "ALUSrc", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "ALUOp", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "MemRd", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "MemWr", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } },
        { text: "MemToReg", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_ACCENT } } }
    ],
    ["LOAD", "1", "1 (Mem)", "000 (Pass)", "1", "0", "1 (Mem)"],
    ["STORE", "0", "1 (Mem)", "000 (Pass)", "0", "1", "x"],
    ["ADD", "1", "0 (Reg)", "001 (Add)", "0", "0", "0 (ALU)"],
    ["SUB", "1", "0 (Reg)", "010 (Sub)", "0", "0", "0 (ALU)"],
    ["MOV", "1", "0 (Reg)", "011 (Mov)", "0", "0", "0 (ALU)"],
    ["JMP / JZ", "0", "x", "xxx", "0", "0", "x"],
    ["OUT", "0", "0", "011 (Pass)", "0", "0", "x"]
], {
    x: 3.8, y: 1.3, w: 5.6, h: 3.8,
    colW: [1.1, 0.7, 0.8, 1.0, 0.7, 0.7, 0.6],
    border: { pt: 1, color: COLOR_SECONDARY_LIGHT },
    valign: "middle",
    align: "center",
    fontSize: 10
});


// -------------------------------------------------------------
// SLIDE 6: Kết quả mô phỏng & Đánh giá (Light Background)
// -------------------------------------------------------------
let slide6 = pres.addSlide();
slide6.background = { color: COLOR_WHITE };
addSlideHeader(slide6, "5. Kết quả mô phỏng trên Icarus Verilog");

// Left Column: Test Program
slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.3, w: 4.2, h: 3.8,
    fill: { color: COLOR_CARD_BG },
    line: { color: COLOR_SECONDARY_LIGHT, width: 1 }
});

slide6.addText([
    { text: "Chương trình kiểm thử (Program.mem):\n\n", options: { bold: true, fontSize: 16, color: COLOR_PRIMARY_DARK } },
    { text: "Chương trình thực hiện phép tính:\n", options: { fontSize: 13, color: COLOR_TEXT_DARK } },
    { text: "Cộng hai số tại RAM[10] = 5 và RAM[11] = 7. Kết quả ghi vào RAM[12].\n\n", options: { fontSize: 13, color: COLOR_TEXT_MUTED } },
    { text: "0x0: LOAD 10      ; R0 = RAM[10] (5)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x1: MOV  R1, R0  ; R1 = R0 (5)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x2: LOAD 11      ; R0 = RAM[11] (7)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x3: ADD  R1, R0  ; R1 = R1 + R0 (12)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x4: MOV  R0, R1  ; R0 = R1 (12)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x5: STORE 12     ; RAM[12] = R0 (12)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x6: OUT  R0      ; OUT = 12 (0xC)\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } },
    { text: "0x7: HALT         ; Dừng chương trình", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_PRIMARY_DARK } }
], { x: 0.8, y: 1.5, w: 3.8, h: 3.4, margin: 0 });

// Right Column: Output logs
slide6.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.3, w: 4.2, h: 3.8,
    fill: { color: COLOR_PRIMARY_DARK }
});

slide6.addText([
    { text: "Kết quả mô phỏng (Simulation Output):\n\n", options: { bold: true, fontSize: 16, color: COLOR_SECONDARY_LIGHT } },
    { text: "Biên dịch & mô phỏng thành công trên Icarus Verilog v12:\n\n", options: { fontSize: 13, color: COLOR_WHITE } },
    { text: "[TIME: 10] Reset released\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 30] PC: 0, Instruction: 1A (LOAD 10)  -> R0: 5\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 50] PC: 1, Instruction: 54 (MOV R1,R0) -> R1: 5\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 70] PC: 2, Instruction: 1B (LOAD 11)  -> R0: 7\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 90] PC: 3, Instruction: 34 (ADD R1,R0) -> R1: 12\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 130] PC: 5, Instruction: 2C (STORE 12) -> RAM[12]: 12\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "[TIME: 150] PC: 6, Instruction: 80 (OUT R0)    -> Cổng OUT: 12\n\n", options: { fontFace: "Consolas", fontSize: 11, color: COLOR_SECONDARY_LIGHT } },
    { text: "=> Đạt yêu cầu: Giá trị tại RAM[12] ghi nhận đúng 12 (0xC), cổng OUT xuất đúng giá trị 12, chương trình kết thúc tại lệnh HALT.", options: { fontSize: 12, color: COLOR_WHITE, italic: true } }
], { x: 5.4, y: 1.5, w: 3.8, h: 3.4, margin: 0 });


// -------------------------------------------------------------
// SLIDE 7: Kết luận & Đánh giá (Dark Background)
// -------------------------------------------------------------
let slide7 = pres.addSlide();
slide7.background = { color: COLOR_PRIMARY_DARK };

slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0.6,
    y: 1.8,
    w: 0.1,
    h: 2.2,
    fill: { color: COLOR_ACCENT }
});

slide7.addText("KẾT LUẬN & ĐÁNH GIÁ ĐỒ ÁN", {
    x: 0.8,
    y: 1.8,
    w: 8.5,
    h: 0.6,
    fontSize: 32,
    fontFace: "Georgia",
    color: COLOR_WHITE,
    bold: true,
    margin: 0
});

slide7.addText([
    { text: "• Hoàn thành thiết kế mức RTL: ", options: { bold: true, fontSize: 14, color: COLOR_WHITE } },
    { text: "Đã thiết kế toàn bộ các khối chức năng bằng ngôn ngữ Verilog chuẩn tắc.\n", options: { fontSize: 14, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Khắc phục lỗi zero-delay loop: ", options: { bold: true, fontSize: 14, color: COLOR_WHITE } },
    { text: "Đã sửa thành công lỗi phản hồi vòng kín tại thời điểm khởi tạo trong Control Unit.\n", options: { fontSize: 14, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Kiểm tra đúng chức năng: ", options: { bold: true, fontSize: 14, color: COLOR_WHITE } },
    { text: "Chương trình chạy chính xác trên bộ mô phỏng Icarus Verilog và xuất kết quả đúng dạng sóng.\n", options: { fontSize: 14, color: COLOR_SECONDARY_LIGHT } },
    { text: "• Hướng phát triển: ", options: { bold: true, fontSize: 14, color: COLOR_WHITE } },
    { text: "Tích hợp thêm bộ giải mã hiển thị LED 7 thanh hoặc thực hiện tổng hợp mạch (Synthesis) mức cổng.", options: { fontSize: 14, color: COLOR_SECONDARY_LIGHT } }
], { x: 0.8, y: 2.6, w: 8.5, h: 2.0, margin: 0 });


// Write presentation to file
pres.writeFile({ fileName: "CPU_4Bit_Presentation.pptx" }).then(fileName => {
    console.log(`Successfully created: ${fileName}`);
}).catch(err => {
    console.error("Error writing pptx:", err);
});
