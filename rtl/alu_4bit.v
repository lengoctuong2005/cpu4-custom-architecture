`timescale 1ns / 1ps

module alu_4bit (
    input  logic [3:0] a,
    input  logic [3:0] b,
    input  logic [2:0] op,
    output logic [3:0] result,
    output logic       zero,
    output logic       negative,
    output logic       carry
);

    always @(a, b, op) begin
        result  = 4'b0;
        carry   = 1'b0;

        case (op)
            3'b000: begin // ADD
                {carry, result} = a + b;
            end
            3'b001: begin // SUB (a - b)
                // Chuẩn hóa cờ Carry: carry = 1  -> KHÔNG mượn (a >= b)
                //                     carry = 0  -> CÓ mượn    (a < b)
                {carry, result} = {1'b0, a} + {1'b0, ~b} + 5'b00001;
            end
            3'b010: begin // AND
                result = a & b;
            end
            3'b011: begin // OR
                result = a | b;
            end
            3'b100: begin // XOR
                result = a ^ b;
            end
            3'b101: begin // INC (a + 1)
                {carry, result} = a + 1'b1;
            end
            3'b110: begin // DEC (a - 1)
                // Chuẩn hóa cờ Carry: carry = 1  -> KHÔNG mượn (a >= 1)
                //                     carry = 0  -> CÓ mượn    (a = 0)
                {carry, result} = {1'b0, a} + {1'b0, ~4'b0001} + 5'b00001;
            end
            default: begin // MOV / PASSTHRU (b)
                result = b;
            end
        endcase
    end

    assign zero     = (result == 4'b0);
    assign negative = result[3]; // MSB = sign bit trong bù 2

endmodule
