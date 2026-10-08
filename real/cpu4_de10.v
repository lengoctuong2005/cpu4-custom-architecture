// Compatibility wrapper; use the canonical single-clock clk_en implementation.
module cpu4_de10(input wire CLOCK_50,input wire [1:0] KEY,input wire mode_sw,
    output wire [9:0] LEDR,output wire [6:0] HEX0,HEX1);
    cpu_top_fpga wrapper(.CLOCK_50(CLOCK_50),.KEY(KEY),.SW(mode_sw),
        .LEDR(LEDR),.HEX0(HEX0),.HEX1(HEX1));
endmodule
