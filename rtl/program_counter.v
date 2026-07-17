`timescale 1ns / 1ps

module program_counter (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        pc_write,
    input  logic        halt,
    input  logic [3:0]  pc_next,
    output logic [3:0]  pc
);


    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            pc <= 4'b0;
        else if (!halt && pc_write)
            pc <= pc_next;
    end

endmodule
