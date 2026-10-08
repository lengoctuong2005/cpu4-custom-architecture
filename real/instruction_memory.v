`timescale 1ns / 1ps
// Default boot ROM is the assembled Fibonacci demo. Testbench task loading is
// simulation-only; this initial data is a constant ROM, NOT an ASIC RAM reset.
module instruction_memory (
    input  logic [3:0] addr,
    output logic [8:0] instruction
);
    logic [8:0] rom [0:15];
    initial begin
        rom[0] = 9'h131; rom[1] = 9'h034; rom[2] = 9'h038;
        rom[3] = 9'h0E1; rom[4] = 9'h0E2; rom[5] = 9'h03D;
        rom[6] = 9'h046; rom[7] = 9'h0E1; rom[8] = 9'h031;
        rom[9] = 9'h060; rom[10] = 9'h0DD; rom[11] = 9'h03B;
        rom[12] = 9'h0B5; rom[13] = 9'h0F0;
        rom[14] = 9'h000; rom[15] = 9'h000;
    end
    assign instruction = rom[addr];
endmodule
