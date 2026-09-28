`timescale 1ns / 1ps

module cpu_top_fpga (
    input  logic       CLOCK_50,       // Xung clock 50MHz onboard
    input  logic [1:0] KEY,            // KEY[0] = Reset (active low), KEY[1] = Step Clock (active low)
    input  logic [0:0] SW,             // SW[0] = Mode Select (1: Auto clock 1Hz, 0: Manual step clock)
    output logic [9:0] LEDR,           // LEDR[3:0] = Out Port, LEDR[4] = Halt, LEDR[8:5] = Debug R0, LEDR[9] = Current Clock
    output logic [6:0] HEX0,           // HEX0 = Hien thi out_port tren Led 7 doan (active low)
    output logic [6:0] HEX1            // HEX1 = Hien thi debug_r0 tren Led 7 doan (active low)
);

    // Day cac tin hieu dieu khien va reset
    logic fpga_clk;
    logic fpga_rst_n;
    logic fpga_step_clk;
    logic fpga_mode_select;

    assign fpga_clk         = CLOCK_50;
    assign fpga_rst_n       = KEY[0];
    assign fpga_step_clk     = KEY[1];
    assign fpga_mode_select = SW[0];

    // 1. Bo chia tan so (Clock Divider): 50MHz -> 1Hz
    logic [25:0] clk_div;
    logic        clk_1hz;
    always_ff @(posedge fpga_clk or negedge fpga_rst_n) begin
        if (!fpga_rst_n) begin
            clk_div <= 26'd0;
            clk_1hz <= 1'b0;
        end else begin
            if (clk_div == 26'd24_999_999) begin
                clk_div <= 26'd0;
                clk_1hz <= ~clk_1hz;
            end else begin
                clk_div <= clk_div + 1;
            end
        end
    end

    // 2. Mach loc nhieu nut nhan (Debouncer) cho KEY[1] (step clock)
    // Lay mau o tan so 1kHz (50MHz / 50_000)
    logic [15:0] debounce_div;
    logic        sample_tick;
    always_ff @(posedge fpga_clk or negedge fpga_rst_n) begin
        if (!fpga_rst_n) begin
            debounce_div <= 16'd0;
            sample_tick  <= 1'b0;
        end else begin
            if (debounce_div == 16'd49_999) begin
                debounce_div <= 16'd0;
                sample_tick  <= 1'b1;
            end else begin
                debounce_div <= debounce_div + 1;
                sample_tick  <= 1'b0;
            end
        end
    end

    logic [2:0] button_shift;
    always_ff @(posedge fpga_clk or negedge fpga_rst_n) begin
        if (!fpga_rst_n) begin
            button_shift <= 3'b111;
        end else if (sample_tick) begin
            button_shift <= {button_shift[1:0], fpga_step_clk};
        end
    end

    // Phat hien canh xuong cua nut nhan (Key pressed)
    logic step_clk_pressed;
    assign step_clk_pressed = (button_shift[2:1] == 2'b10);

    // 3. Mux chon xung clock cho CPU
    logic cpu_clk;
    assign cpu_clk = fpga_mode_select ? clk_1hz : step_clk_pressed;

    // Duong truyen tin hieu tu CPU
    logic [3:0] cpu_out_port;
    logic       cpu_halt_out;
    logic [3:0] cpu_debug_r0;

    // Instantiation cua CPU top
    cpu_top cpu_inst (
        .clk      (cpu_clk),
        .rst_n    (fpga_rst_n),
        .out_port (cpu_out_port),
        .halt_out (cpu_halt_out),
        .debug_r0 (cpu_debug_r0)
    );

    // 4. Anh xa sang LED
    assign LEDR[3:0] = cpu_out_port;
    assign LEDR[4]   = cpu_halt_out;
    assign LEDR[8:5] = cpu_debug_r0;
    assign LEDR[9]   = cpu_clk;

    // 5. Giai ma LED 7 doan (Active Low)
    hex_decoder_fpga hex0_dec (
        .in  (cpu_out_port),
        .out (HEX0)
    );

    hex_decoder_fpga hex1_dec (
        .in  (cpu_debug_r0),
        .out (HEX1)
    );

endmodule

// Module giai ma LED 7 doan tu 0 den F
module hex_decoder_fpga (
    input  logic [3:0] in,
    output logic [6:0] out
);
    always_comb begin
        case (in)
            4'h0: out = 7'b1000000;
            4'h1: out = 7'b1111001;
            4'h2: out = 7'b0100100;
            4'h3: out = 7'b0110000;
            4'h4: out = 7'b0011001;
            4'h5: out = 7'b0010010;
            4'h6: out = 7'b0000010;
            4'h7: out = 7'b1111000;
            4'h8: out = 7'b0000000;
            4'h9: out = 7'b0010000;
            4'hA: out = 7'b0001000;
            4'hB: out = 7'b0000011;
            4'hC: out = 7'b1000110;
            4'hD: out = 7'b0100001;
            4'hE: out = 7'b0000110;
            4'hF: out = 7'b0001110;
            default: out = 7'b1111111;
        endcase
    end
endmodule
