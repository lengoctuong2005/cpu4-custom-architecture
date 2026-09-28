`timescale 1ns / 1ps

module instruction_memory (
    input  logic [3:0]  addr,
    output logic [8:0]  instruction
);

    logic [8:0] rom [0:15];

    initial begin
        // Fibonacci program hardcoded for FPGA synthesis
        rom[4'h0] = 9'h131; // LDI   #1
        rom[4'h1] = 9'h034; // MOV   R1, R0
        rom[4'h2] = 9'h038; // MOV   R2, R0
        rom[4'h3] = 9'h0E1; // OUT   R1
        rom[4'h4] = 9'h0E2; // OUT   R2
        rom[4'h5] = 9'h03D; // MOV   R3, R1
        rom[4'h6] = 9'h046; // ADD   R1, R2
        rom[4'h7] = 9'h0E1; // OUT   R1
        rom[4'h8] = 9'h031; // MOV   R0, R1
        rom[4'h9] = 9'h060; // AND   R0, R0
        rom[4'hA] = 9'h0DD; // JN    END
        rom[4'hB] = 9'h03B; // MOV   R2, R3
        rom[4'hC] = 9'h0B5; // JMP   LOOP
        rom[4'hD] = 9'h0F0; // HALT
        rom[4'hE] = 9'h000;
        rom[4'hF] = 9'h000;
    end

    assign instruction = rom[addr];

endmodule
