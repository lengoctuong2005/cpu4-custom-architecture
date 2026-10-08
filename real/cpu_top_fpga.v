`timescale 1ns / 1ps
// One real clock domain. Buttons/mode are synchronized; execution uses clk_en.
module cpu_top_fpga #(
    parameter integer AUTO_CYCLES = 50_000_000,
    parameter integer DEBOUNCE_CYCLES = 500_000
)(
    input logic CLOCK_50,
    input logic [1:0] KEY,
    input logic [0:0] SW,
    output logic [9:0] LEDR,
    output logic [6:0] HEX0, HEX1
);
    localparam integer AW = (AUTO_CYCLES < 2) ? 1 : $clog2(AUTO_CYCLES);
    localparam integer DW = (DEBOUNCE_CYCLES < 2) ? 1 : $clog2(DEBOUNCE_CYCLES);
    (* async_reg = "true" *) logic [1:0] reset_sync;
    (* async_reg = "true" *) logic [1:0] key_sync, mode_sync;
    wire rst_n = reset_sync[1];
    always_ff @(posedge CLOCK_50 or negedge KEY[0])
        if (!KEY[0]) reset_sync <= 2'b00;
        else reset_sync <= {reset_sync[0],1'b1};
    always_ff @(posedge CLOCK_50 or negedge rst_n)
        if (!rst_n) begin key_sync<=2'b11; mode_sync<=2'b00; end
        else begin key_sync<={key_sync[0],KEY[1]}; mode_sync<={mode_sync[0],SW[0]}; end
    logic [DW-1:0] debounce_count;
    logic key_clean, key_previous;
    always_ff @(posedge CLOCK_50 or negedge rst_n) begin
        if (!rst_n) begin debounce_count<='0; key_clean<=1'b1; key_previous<=1'b1; end
        else begin
            key_previous<=key_clean;
            if (key_sync[1]==key_clean) debounce_count<='0;
            else if (debounce_count==DEBOUNCE_CYCLES-1) begin
                key_clean<=key_sync[1]; debounce_count<='0;
            end else debounce_count<=debounce_count+1'b1;
        end
    end
    logic [AW-1:0] auto_count;
    wire auto_tick = (auto_count==AUTO_CYCLES-1);
    always_ff @(posedge CLOCK_50 or negedge rst_n)
        if (!rst_n) auto_count<='0;
        else if (!mode_sync[1] || auto_tick) auto_count<='0;
        else auto_count<=auto_count+1'b1;
    wire cpu_enable = rst_n && (mode_sync[1] ? auto_tick : (key_previous && !key_clean));
    wire [3:0] cpu_out, cpu_r0;
    wire cpu_halt;
    cpu_top cpu_inst(.clk(CLOCK_50),.clk_en(cpu_enable),.rst_n(rst_n),
        .out_port(cpu_out),.halt_out(cpu_halt),.debug_r0(cpu_r0));
    assign LEDR={cpu_enable,cpu_r0,cpu_halt,cpu_out};
    hex_decoder_fpga h0(.in(cpu_out),.out(HEX0));
    hex_decoder_fpga h1(.in(cpu_r0),.out(HEX1));
endmodule
module hex_decoder_fpga(input logic [3:0] in,output logic [6:0] out);
    always @* case(in)
        0:out=7'b1000000; 1:out=7'b1111001; 2:out=7'b0100100; 3:out=7'b0110000;
        4:out=7'b0011001; 5:out=7'b0010010; 6:out=7'b0000010; 7:out=7'b1111000;
        8:out=7'b0000000; 9:out=7'b0010000; 10:out=7'b0001000; 11:out=7'b0000011;
        12:out=7'b1000110; 13:out=7'b0100001; 14:out=7'b0000110; 15:out=7'b0001110;
        default:out=7'b1111111;
    endcase
endmodule
