const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Antigravity AI';
pres.title = 'Premium 4-Bit CPU Presentation';

// Premium Design System Colors (No '#' prefix)
const COLOR_BG_DARK = "0F172A";       // Deep Slate (Dark Mode)
const COLOR_BG_LIGHT = "F8FAFC";      // Cream Off-White (Light Mode)
const COLOR_PRIMARY = "1E293B";       // Slate 800
const COLOR_SECONDARY = "475569";     // Slate 600
const COLOR_ACCENT = "0D9488";        // Vibrant Teal
const COLOR_ACCENT_BG = "CCFBF1";     // Soft Teal Tint
const COLOR_CARD_BG = "FFFFFF";       // Pure White for Cards
const COLOR_CARD_BORDER = "E2E8F0";   // Border Slate 200
const COLOR_SECONDARY_LIGHT = "94A3B8"; // Light Slate 400
const COLOR_WHITE = "FFFFFF";

// Fonts
const FONT_HEADER = "Georgia";
const FONT_BODY = "Calibri";

// Helper to make shadow configuration
const makeShadow = () => ({
    type: "outer",
    color: "0F172A",
    blur: 8,
    offset: 2,
    angle: 135,
    opacity: 0.08
});

// Helper for slide titles
function addSlideHeader(slide, category, title, isDark = false) {
    // Small Category/Section Tracker
    slide.addText(category.toUpperCase(), {
        x: 0.8, y: 0.4, w: 8.0, h: 0.25,
        fontSize: 10, fontFace: FONT_BODY,
        color: isDark ? COLOR_ACCENT : COLOR_ACCENT,
        bold: true, charSpacing: 3, margin: 0
    });
    
    // Main Title
    slide.addText(title, {
        x: 0.8, y: 0.65, w: 8.0, h: 0.5,
        fontSize: 26, fontFace: FONT_HEADER,
        color: isDark ? COLOR_WHITE : COLOR_PRIMARY,
        bold: true, margin: 0
    });
}

// -------------------------------------------------------------
// SLIDE 1: Title Slide (Dark Premium Mode)
// -------------------------------------------------------------
let slide1 = pres.addSlide();
slide1.background = { color: COLOR_BG_DARK };

// Subtle background design elements
slide1.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.3, h: 5.625,
    fill: { color: COLOR_ACCENT }
});

slide1.addText("ĐỒ ÁN MÔN HỌC THIẾT KẾ VI MẠCH ĐIỆN TỬ", {
    x: 1.0, y: 1.6, w: 8.5, h: 0.3,
    fontSize: 12, fontFace: FONT_BODY,
    color: COLOR_ACCENT, bold: true, charSpacing: 4, margin: 0
});

slide1.addText("Thiết Kế CPU 4-Bit\nDùng Quy Trình RTL Flow", {
    x: 1.0, y: 2.0, w: 8.5, h: 1.4,
    fontSize: 42, fontFace: FONT_HEADER,
    color: COLOR_WHITE, bold: true, margin: 0
});

slide1.addText("Quy trình thiết kế mạch số trên ngôn ngữ Verilog | Mô phỏng kiểm thử chuyên sâu", {
    x: 1.0, y: 3.5, w: 8.5, h: 0.4,
    fontSize: 14, fontFace: FONT_BODY,
    color: "94A3B8", margin: 0
});

slide1.addShape(pres.shapes.LINE, {
    x: 1.0, y: 4.1, w: 2.5, h: 0,
    line: { color: COLOR_ACCENT, width: 2 }
});

slide1.addText("Học kỳ 3 (2025-2026) | Topic số 7", {
    x: 1.0, y: 4.3, w: 5.0, h: 0.3,
    fontSize: 12, fontFace: FONT_BODY,
    color: "64748B", italic: true, margin: 0
});


// -------------------------------------------------------------
// SLIDE 2: Tổng quan & Đề tài (Light Background)
// -------------------------------------------------------------
let slide2 = pres.addSlide();
slide2.background = { color: COLOR_BG_LIGHT };
addSlideHeader(slide2, "Tổng Quan Đề Tài", "Đặc Tả Kiến Trúc CPU 4-Bit");

// We'll create 3 distinct visual cards representing the 3 core pillars of this CPU
const cardWidth = 2.6;
const cardHeight = 3.6;
const cardY = 1.4;

const pillars = [
    {
        num: "01",
        title: "Kiến trúc Harvard",
        desc: "Bộ nhớ dữ liệu (RAM) và Bộ nhớ chỉ lệnh (ROM) được tách biệt hoàn toàn về đường truyền vật lý.\n\nCho phép nạp lệnh từ ROM và đọc/ghi RAM dữ liệu trong cùng một thời điểm mà không xảy ra xung đột bus."
    },
    {
        num: "02",
        title: "Single-Cycle Core",
        desc: "Mỗi chu kỳ xung nhịp (clock edge) thực thi hoàn chỉnh đúng một lệnh.\n\nĐơn giản hóa khối điều khiển điều hướng, tối ưu hóa quá trình kiểm tra chức năng logic của mạch xử lý."
    },
    {
        num: "03",
        title: "Lõi Dữ Liệu 4-bit",
        desc: "Các thanh ghi đa năng R0-R3 có độ rộng 4-bit.\n\nALU tính toán toán số học/logic trên dữ liệu 4-bit.\n\nTập lệnh tối giản với độ rộng từ lệnh cố định 8-bit (Opcode 4-bit + Operand 4-bit)."
    }
];

pillars.forEach((p, idx) => {
    let xPos = 0.8 + idx * 3.0;
    
    // Draw Card Background with Shadow
    slide2.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: cardY, w: cardWidth, h: cardHeight,
        fill: { color: COLOR_CARD_BG },
        line: { color: COLOR_CARD_BORDER, width: 1 },
        shadow: makeShadow()
    });

    // Top color strip on card
    slide2.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: cardY, w: cardWidth, h: 0.15,
        fill: { color: idx === 1 ? COLOR_ACCENT : COLOR_PRIMARY }
    });

    // Number
    slide2.addText(p.num, {
        x: xPos + 0.2, y: cardY + 0.3, w: 1.0, h: 0.4,
        fontSize: 24, fontFace: FONT_HEADER,
        color: COLOR_ACCENT, bold: true, margin: 0
    });

    // Card Title
    slide2.addText(p.title, {
        x: xPos + 0.2, y: cardY + 0.8, w: cardWidth - 0.4, h: 0.4,
        fontSize: 16, fontFace: FONT_HEADER,
        color: COLOR_PRIMARY, bold: true, margin: 0
    });

    // Card Desc
    slide2.addText(p.desc, {
        x: xPos + 0.2, y: cardY + 1.3, w: cardWidth - 0.4, h: 2.0,
        fontSize: 12, fontFace: FONT_BODY,
        color: COLOR_SECONDARY, margin: 0
    });
});


// -------------------------------------------------------------
// SLIDE 3: Tập lệnh ISA (Light Background with Custom Layout)
// -------------------------------------------------------------
let slide3 = pres.addSlide();
slide3.background = { color: COLOR_BG_LIGHT };
addSlideHeader(slide3, "Kiến trúc Tập lệnh", "Định Dạng Chỉ Lệnh & Tập Lệnh Tối Giản");

// Left Card: Instruction Format Visualisation
slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 1.4, w: 3.2, h: 3.6,
    fill: { color: COLOR_PRIMARY },
    shadow: makeShadow()
});

slide3.addText("ĐỊNH DẠNG TỪ LỆNH (8-BIT)", {
    x: 1.0, y: 1.7, w: 2.8, h: 0.3,
    fontSize: 11, fontFace: FONT_BODY,
    color: COLOR_ACCENT, bold: true, charSpacing: 2, margin: 0
});

// Opcode box
slide3.addShape(pres.shapes.RECTANGLE, {
    x: 1.1, y: 2.2, w: 1.3, h: 0.8,
    fill: { color: COLOR_ACCENT }
});
slide3.addText("OPCODE\n[7:4]", {
    x: 1.1, y: 2.3, w: 1.3, h: 0.6,
    fontSize: 12, fontFace: FONT_BODY, color: COLOR_WHITE, bold: true, align: "center", margin: 0
});

// Operand box
slide3.addShape(pres.shapes.RECTANGLE, {
    x: 2.5, y: 2.2, w: 1.3, h: 0.8,
    fill: { color: COLOR_SECONDARY }
});
slide3.addText("OPERAND\n[3:0]", {
    x: 2.5, y: 2.3, w: 1.3, h: 0.6,
    fontSize: 12, fontFace: FONT_BODY, color: COLOR_WHITE, bold: true, align: "center", margin: 0
});

slide3.addText("Opcode (4-bit): Định nghĩa 9 phép toán xử lý cơ bản.\n\nOperand (4-bit): Chứa địa chỉ bộ nhớ (RAM/ROM) hoặc chỉ số của tập thanh ghi nguồn/đích.", {
    x: 1.0, y: 3.3, w: 2.8, h: 1.4,
    fontSize: 12, fontFace: FONT_BODY, color: COLOR_SECONDARY_LIGHT, margin: 0
});

// Right Table: Styled and modern
slide3.addTable([
    [
        { text: "Lệnh (ASM)", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "Opcode", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY }, align: "center" } },
        { text: "Chức năng thực thi", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } }
    ],
    ["LOAD addr", "0001", "Nạp dữ liệu từ RAM[addr] vào R0"],
    ["STORE addr", "0010", "Lưu dữ liệu từ R0 vào RAM[addr]"],
    ["ADD Rd, Rs", "0011", "Cộng thanh ghi: R[Rd] = R[Rd] + R[Rs]"],
    ["SUB Rd, Rs", "0100", "Trừ thanh ghi: R[Rd] = R[Rd] - R[Rs]"],
    ["MOV Rd, Rs", "0101", "Sao chép dữ liệu giữa các thanh ghi"],
    ["JMP addr", "0110", "Nhảy không điều kiện tới địa chỉ ROM"],
    ["JZ addr", "0111", "Nhảy nếu cờ Zero Z = 1"],
    ["OUT Rs", "1000", "Xuất giá trị của Rs ra cổng ngoài"],
    ["HALT", "1111", "Dừng chạy chương trình"]
], {
    x: 4.3, y: 1.4, w: 4.9, h: 3.6,
    colW: [1.2, 0.9, 2.8],
    border: { pt: 1, color: COLOR_CARD_BORDER },
    valign: "middle",
    fontSize: 10,
    fontFace: FONT_BODY
});


// -------------------------------------------------------------
// SLIDE 4: Sơ đồ khối Datapath (Light Background Layout)
// -------------------------------------------------------------
let slide4 = pres.addSlide();
slide4.background = { color: COLOR_BG_LIGHT };
addSlideHeader(slide4, "Sơ Đồ Kiến Trúc", "Đường Đi Dữ Liệu (Datapath) Tối Ưu");

// Draw Flow Nodes with Soft Cards and Connectors
const flowNodes = [
    { name: "Program Counter", x: 0.8, y: 1.8, w: 2.4, h: 1.0, t: "FETCH", desc: "Tăng địa chỉ PC qua từng cạnh clock" },
    { name: "Instruction Memory", x: 3.6, y: 1.8, w: 2.4, h: 1.0, t: "DECODE", desc: "ROM nạp mã máy 8-bit tương ứng" },
    { name: "Register File", x: 6.4, y: 1.8, w: 2.8, h: 1.0, t: "REG READ", desc: "Lấy dữ liệu từ R0-R3 cho toán hạng" },
    
    { name: "ALU 4-bit", x: 6.4, y: 3.6, w: 2.8, h: 1.0, t: "EXECUTE", desc: "Thực hiện ADD/SUB/Pass qua opcode" },
    { name: "Data Memory (RAM)", x: 3.6, y: 3.6, w: 2.4, h: 1.0, t: "WRITEBACK", desc: "Đọc/ghi kết quả tính toán vào RAM" }
];

flowNodes.forEach((node, idx) => {
    // Background Card
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: node.x, y: node.y, w: node.w, h: node.h,
        fill: { color: COLOR_CARD_BG },
        line: { color: COLOR_CARD_BORDER, width: 1 },
        shadow: makeShadow()
    });

    // Accent line on side of card
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: node.x, y: node.y, w: 0.08, h: node.h,
        fill: { color: COLOR_ACCENT }
    });

    // Badge
    slide4.addShape(pres.shapes.RECTANGLE, {
        x: node.x + 0.15, y: node.y + 0.12, w: 0.9, h: 0.22,
        fill: { color: COLOR_ACCENT_BG },
        line: { style: "none" }
    });
    slide4.addText(node.t, {
        x: node.x + 0.15, y: node.y + 0.12, w: 0.9, h: 0.22,
        fontSize: 8, fontFace: FONT_BODY, color: COLOR_ACCENT, bold: true, align: "center", margin: 0
    });

    // Title
    slide4.addText(node.name, {
        x: node.x + 0.15, y: node.y + 0.38, w: node.w - 0.25, h: 0.25,
        fontSize: 12, fontFace: FONT_HEADER, color: COLOR_PRIMARY, bold: true, margin: 0
    });

    // Desc
    slide4.addText(node.desc, {
        x: node.x + 0.15, y: node.y + 0.62, w: node.w - 0.25, h: 0.35,
        fontSize: 9, fontFace: FONT_BODY, color: COLOR_SECONDARY, margin: 0
    });
});

// Draw Connective Flow Lines
// Node 0 -> Node 1
slide4.addShape(pres.shapes.LINE, { x: 3.2, y: 2.3, w: 0.4, h: 0, line: { color: COLOR_SECONDARY, width: 1.5 } });
// Node 1 -> Node 2
slide4.addShape(pres.shapes.LINE, { x: 6.0, y: 2.3, w: 0.4, h: 0, line: { color: COLOR_SECONDARY, width: 1.5 } });
// Node 2 -> Node 3 (Vertical Down)
slide4.addShape(pres.shapes.LINE, { x: 7.8, y: 2.8, w: 0, h: 0.8, line: { color: COLOR_SECONDARY, width: 1.5 } });
// Node 3 -> Node 4
slide4.addShape(pres.shapes.LINE, { x: 6.4, y: 4.1, w: -0.4, h: 0, line: { color: COLOR_SECONDARY, width: 1.5 } });


// -------------------------------------------------------------
// SLIDE 5: Khối điều khiển Control Unit (Light Background)
// -------------------------------------------------------------
let slide5 = pres.addSlide();
slide5.background = { color: COLOR_BG_LIGHT };
addSlideHeader(slide5, "Khối Điều Khiển", "Logic Giải Mã Trực Quan (Control Unit)");

// Left Panel Card
slide5.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 1.4, w: 3.0, h: 3.6,
    fill: { color: COLOR_CARD_BG },
    line: { color: COLOR_CARD_BORDER, width: 1 },
    shadow: makeShadow()
});

slide5.addText("GIẢI MÃ LỆNH TỔ HỢP", {
    x: 1.0, y: 1.7, w: 2.6, h: 0.3,
    fontSize: 11, fontFace: FONT_BODY,
    color: COLOR_ACCENT, bold: true, charSpacing: 2, margin: 0
});

slide5.addText([
    { text: "Control Unit đóng vai trò bộ não của CPU:\n\n", options: { bold: true, fontSize: 13, color: COLOR_PRIMARY } },
    { text: "• Mạch Tổ Hợp: ", options: { bold: true, color: COLOR_PRIMARY } },
    { text: "Nhận opcode 4-bit đầu vào và chuyển đổi tức thời sang các tín hiệu điều khiển mà không tốn chu kỳ clock.\n\n", options: { color: COLOR_SECONDARY } },
    { text: "• Tránh Vòng Phản Hồi: ", options: { bold: true, color: COLOR_PRIMARY } },
    { text: "Cấu trúc độc lập của cờ Z và N tách rời khỏi tổ hợp khối điều khiển giúp mạch mô phỏng tránh được lỗi zero-delay loop.", options: { color: COLOR_SECONDARY } }
], {
    x: 1.0, y: 2.1, w: 2.6, h: 2.6,
    fontSize: 11, fontFace: FONT_BODY, margin: 0
});

// Right Table: Control signals truth table
slide5.addTable([
    [
        { text: "Opcode", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "Lệnh", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "RegWrite", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "ALUSrc", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "ALUOp", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "MemWrite", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } },
        { text: "MemtoReg", options: { bold: true, color: COLOR_WHITE, fill: { color: COLOR_PRIMARY } } }
    ],
    ["0001", "LOAD", "1", "1 (Mem)", "000 (Pass)", "0", "1 (Mem)"],
    ["0010", "STORE", "0", "1 (Mem)", "000 (Pass)", "1", "x"],
    ["0011", "ADD", "1", "0 (Reg)", "001 (Add)", "0", "0 (ALU)"],
    ["0100", "SUB", "1", "0 (Reg)", "010 (Sub)", "0", "0 (ALU)"],
    ["0101", "MOV", "1", "0 (Reg)", "011 (Pass)", "0", "0 (ALU)"],
    ["0110", "JMP", "0", "x", "xxx", "0", "x"],
    ["0111", "JZ", "0", "x", "xxx", "0", "x"],
    ["1000", "OUT", "0", "0 (Reg)", "011 (Pass)", "0", "x"],
    ["1111", "HALT", "0", "x", "xxx", "0", "x"]
], {
    x: 4.0, y: 1.4, w: 5.2, h: 3.6,
    colW: [0.7, 0.7, 0.8, 0.8, 1.0, 0.8, 0.8],
    border: { pt: 1, color: COLOR_CARD_BORDER },
    valign: "middle",
    align: "center",
    fontSize: 9,
    fontFace: FONT_BODY
});


// -------------------------------------------------------------
// SLIDE 6: Kết quả mô phỏng & Đánh giá (Light Background)
// -------------------------------------------------------------
let slide6 = pres.addSlide();
slide6.background = { color: COLOR_BG_LIGHT };
addSlideHeader(slide6, "Kiểm Thử Đồ Án", "Kiểm Thử Chương Trình & Kết Quả Mô Phỏng");

// Left Column: Modern Dark Terminal
slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 1.4, w: 3.6, h: 3.6,
    fill: { color: "1E1E2E" }, // Dark terminal background
    shadow: makeShadow()
});

slide6.addText("TERMINAL - CODE MÃ MÁY (PROG.MEM)", {
    x: 1.0, y: 1.6, w: 3.2, h: 0.25,
    fontSize: 10, fontFace: "Consolas",
    color: COLOR_ACCENT, bold: true, margin: 0
});

slide6.addText([
    { text: "1A ; PC=0 | LOAD RAM[10] -> R0 (5)\n", options: { color: "A6E22E" } },
    { text: "54 ; PC=1 | MOV  R1, R0    -> R1 (5)\n", options: { color: "F8F8F2" } },
    { text: "1B ; PC=2 | LOAD RAM[11] -> R0 (7)\n", options: { color: "A6E22E" } },
    { text: "34 ; PC=3 | ADD  R1, R0    -> R1 (12)\n", options: { color: "F92672" } },
    { text: "50 ; PC=4 | MOV  R0, R1    -> R0 (12)\n", options: { color: "F8F8F2" } },
    { text: "2C ; PC=5 | STORE R0       -> RAM[12]\n", options: { color: "66D9EF" } },
    { text: "80 ; PC=6 | OUT  R0        -> OUT=12\n", options: { color: "E6DB74" } },
    { text: "F0 ; PC=7 | HALT           -> STOP", options: { color: "F92672" } }
], {
    x: 1.0, y: 2.0, w: 3.2, h: 2.8,
    fontSize: 11, fontFace: "Consolas", margin: 0
});

// Right Column: Simulation Trace steps
slide6.addShape(pres.shapes.RECTANGLE, {
    x: 4.7, y: 1.4, w: 4.5, h: 3.6,
    fill: { color: COLOR_CARD_BG },
    line: { color: COLOR_CARD_BORDER, width: 1 },
    shadow: makeShadow()
});

slide6.addText("TRÌNH TỰ MÔ PHỎNG (WAVEFORM LOG)", {
    x: 4.9, y: 1.6, w: 4.1, h: 0.25,
    fontSize: 11, fontFace: FONT_BODY,
    color: COLOR_PRIMARY, bold: true, charSpacing: 1, margin: 0
});

const steps = [
    { time: "t = 10ns", desc: "Reset (rst_n) được kích hoạt lên mức 1, CPU bắt đầu hoạt động." },
    { time: "t = 30ns", desc: "PC=0, đọc lệnh 1A: Nạp giá trị 5 từ RAM[10] vào R0 thành công." },
    { time: "t = 90ns", desc: "PC=3, lệnh 34: Thực hiện R1 = R1 (5) + R0 (7). Kết quả R1 = 12." },
    { time: "t = 130ns", desc: "PC=5, lệnh 2C: Ghi giá trị 12 từ R0 vào ô nhớ RAM[12]." },
    { time: "t = 150ns", desc: "PC=6, lệnh OUT: Giá trị 12 xuất ra cổng ngoài. Nhận tín hiệu HALT dừng máy." }
];

steps.forEach((step, idx) => {
    let yPos = 2.0 + idx * 0.58;
    
    // Time badge
    slide6.addShape(pres.shapes.RECTANGLE, {
        x: 4.9, y: yPos, w: 0.8, h: 0.35,
        fill: { color: COLOR_ACCENT_BG },
        line: { style: "none" }
    });
    slide6.addText(step.time, {
        x: 4.9, y: yPos + 0.05, w: 0.8, h: 0.25,
        fontSize: 10, fontFace: FONT_BODY, color: COLOR_ACCENT, bold: true, align: "center", margin: 0
    });

    // Description text
    slide6.addText(step.desc, {
        x: 5.8, y: yPos - 0.05, w: 3.2, h: 0.5,
        fontSize: 10.5, fontFace: FONT_BODY, color: COLOR_SECONDARY, margin: 0
    });
});


// -------------------------------------------------------------
// SLIDE 7: Kết luận & Đánh giá (Dark Premium Mode)
// -------------------------------------------------------------
let slide7 = pres.addSlide();
slide7.background = { color: COLOR_BG_DARK };

slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.3, h: 5.625,
    fill: { color: COLOR_ACCENT }
});

addSlideHeader(slide7, "Tổng Kết Đồ Án", "Kết Luận & Hướng Phát Triển Đề Tài", true);

// Left Stat Block
slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 1.5, w: 3.2, h: 3.4,
    fill: { color: "1E293B" }
});

slide7.addText("CHẤT LƯỢNG MÔ PHỎNG", {
    x: 1.0, y: 1.8, w: 2.8, h: 0.3,
    fontSize: 11, fontFace: FONT_BODY,
    color: COLOR_ACCENT, bold: true, charSpacing: 2, margin: 0
});

slide7.addText("100%", {
    x: 1.0, y: 2.2, w: 2.8, h: 0.9,
    fontSize: 72, fontFace: FONT_HEADER,
    color: COLOR_WHITE, bold: true, margin: 0
});

slide7.addText("Các chức năng tính toán số học, rẽ nhánh điều kiện và ghi dữ liệu bộ nhớ đều đạt độ chính xác hoàn đối đối chứng trực tiếp qua giản đồ xung sóng (waveform).", {
    x: 1.0, y: 3.2, w: 2.8, h: 1.4,
    fontSize: 12, fontFace: FONT_BODY, color: "94A3B8", margin: 0
});

// Right List Cards
const achievements = [
    { title: "Hoàn thiện RTL Flow", text: "Thiết kế thành công toàn bộ kiến trúc lõi CPU bằng Verilog chuẩn hóa." },
    { title: "Sửa lỗi treo Simulator", text: "Loại bỏ hoàn toàn combinational feedback loop tại Control Unit giúp mạch chạy ổn định." },
    { title: "Hướng phát triển tương lai", text: "Mở rộng tập lệnh lên 16-bit, bổ sung bộ nhân chuyên dụng (multiplier) và tổng hợp ASIC." }
];

achievements.forEach((ach, idx) => {
    let yPos = 1.5 + idx * 1.15;
    
    slide7.addShape(pres.shapes.RECTANGLE, {
        x: 4.3, y: yPos, w: 4.9, h: 1.0,
        fill: { color: "1E293B" }
    });

    // Vertical line indicator
    slide7.addShape(pres.shapes.RECTANGLE, {
        x: 4.3, y: yPos, w: 0.06, h: 1.0,
        fill: { color: COLOR_ACCENT }
    });

    slide7.addText(ach.title, {
        x: 4.5, y: yPos + 0.15, w: 4.5, h: 0.3,
        fontSize: 14, fontFace: FONT_HEADER, color: COLOR_WHITE, bold: true, margin: 0
    });

    slide7.addText(ach.text, {
        x: 4.5, y: yPos + 0.45, w: 4.5, h: 0.45,
        fontSize: 12, fontFace: FONT_BODY, color: "94A3B8", margin: 0
    });
});

// Save Presentation
pres.writeFile({ fileName: "CPU_4Bit_Presentation_Premium.pptx" }).then(fileName => {
    console.log(`Successfully created: ${fileName}`);
}).catch(err => {
    console.error("Error writing pptx:", err);
});
