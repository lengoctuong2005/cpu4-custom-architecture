`timescale 1ns / 1ps

module instruction_memory (
    input  logic [3:0]  addr,
    output logic [8:0]  instruction
);

    logic [8:0] rom [0:15];

    integer i;
    initial begin
        for (i = 0; i < 16; i++) rom[i] = 9'h000;
    end

    assign instruction = rom[addr];

endmodule
