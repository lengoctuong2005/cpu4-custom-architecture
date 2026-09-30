// Loi CPU dung chung (module cpu4 o Muc 2.7) + lop I/O cho DE10-Standard.
// IMEM: dung ban ROM bang `case` (instruction_memory_rom.v) vi FPGA cung can tong hop duoc.
module cpu4_de10 (
    input  wire       CLOCK_50,  // PIN_AF14, 50 MHz
    input  wire [1:0] KEY,       // KEY[0]=reset, KEY[1]=buoc-clock (tich cuc muc THAP)
    input  wire       mode_sw,   // = SW[9]: 1 = tu dong ~1.5Hz, 0 = buoc tay bang KEY[1]
    output wire [9:0] LEDR,
    output wire [6:0] HEX0,      // out_port dang hex
    output wire [6:0] HEX1       // luon hien '0'
);
    wire rst_n = KEY[0];         // nhan KEY0 = reset (tich cuc thap)

    // 1) Chia 50MHz -> ~1.49 Hz de mat nguoi kip nhin
    reg [24:0] div;
    always @(posedge CLOCK_50 or negedge rst_n)
        if (!rst_n) div <= 25'd0; else div <= div + 25'd1;
    wire clk_slow = div[24];

    // 2) Debounce KEY[1] cho che do buoc tay
    reg [19:0] cnt; reg s0, s1, key1_clean;
    always @(posedge CLOCK_50 or negedge rst_n)
        if (!rst_n) begin s0<=1'b1; s1<=1'b1; cnt<=20'd0; key1_clean<=1'b1; end
        else begin
            s0 <= KEY[1]; s1 <= s0;
            if (s1 == key1_clean)      cnt <= 20'd0;
            else if (cnt == 20'hFFFFF) begin key1_clean <= s1; cnt <= 20'd0; end
            else                       cnt <= cnt + 20'd1;
        end

    // 3) Chon clock CPU (dat mode_sw TRUOC khi tha reset de tranh xung thua)
    wire cpu_clk = mode_sw ? clk_slow : key1_clean;
    // Che do buoc tay: moi lan NHAN-THA KEY[1] = 1 nhip lenh.

    // 4) Loi CPU dung chung (cpu_top)
    wire [3:0] out_port; wire halt;
    cpu_top u_cpu (
        .clk      (cpu_clk),
        .rst_n    (rst_n),
        .out_port (out_port),
        .halt_out (halt),
        .debug_r0 ()
    );

    // 5) Hien thi
    assign LEDR[3:0] = out_port;   // ket qua 4-bit
    assign LEDR[8:4] = 5'd0;
    assign LEDR[9]   = halt;       // sang khi CPU da HALT
    seg7 h0 (.v(out_port), .seg(HEX0));
    assign HEX1 = 7'b1000000;      // hien so '0'
endmodule

// Giai ma 7 doan, tich cuc muc THAP, thu tu HEX[6:0] = {g,f,e,d,c,b,a}
module seg7 (input wire [3:0] v, output reg [6:0] seg);
    always @(*) case (v)
        4'h0: seg=7'b1000000; 4'h1: seg=7'b1111001;
        4'h2: seg=7'b0100100; 4'h3: seg=7'b0110000;
        4'h4: seg=7'b0011001; 4'h5: seg=7'b0010010;
        4'h6: seg=7'b0000010; 4'h7: seg=7'b1111000;
        4'h8: seg=7'b0000000; 4'h9: seg=7'b0010000;
        4'hA: seg=7'b0001000; 4'hB: seg=7'b0000011;
        4'hC: seg=7'b1000110; 4'hD: seg=7'b0100001;
        4'hE: seg=7'b0000110; 4'hF: seg=7'b0001110;
        default: seg=7'b1111111;
    endcase
endmodule
