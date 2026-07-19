`timescale 1ns / 1ps

// Unit testbench for the 4-bit ALU.
//
// Carry/borrow convention (matches rtl/alu_4bit.v and docs/isa.md):
//   ADD/INC : carry = 1 when the result overflows bit 4 (a+b >= 16).
//   SUB/DEC : carry = 1 when there is NO borrow (a >= b);
//             carry = 0 when a borrow occurs   (a <  b).
//
// Every check funnels through check_alu(), which counts failures so the
// final banner reports the true PASS/FAIL state instead of unconditionally
// printing "passed".

module tb_alu_4bit;

    logic [3:0] a, b;
    logic [2:0] op;
    logic [3:0] result;
    logic       zero, negative, carry;

    integer errors = 0;
    integer checks = 0;

    alu_4bit uut (
        .a       (a),
        .b       (b),
        .op      (op),
        .result  (result),
        .zero    (zero),
        .negative(negative),
        .carry   (carry)
    );

    // Drive one operation, wait for the combinational output to settle, then
    // compare result + all three flags against the expected values.
    task automatic check_alu(input string        name,
                             input logic [3:0]    ta,
                             input logic [3:0]    tb_,
                             input logic [2:0]    top,
                             input logic [3:0]    exp_result,
                             input logic          exp_zero,
                             input logic          exp_neg,
                             input logic          exp_carry);
        begin
            a = ta; b = tb_; op = top;
            #10;
            checks = checks + 1;
            if (result === exp_result && zero === exp_zero &&
                negative === exp_neg && carry === exp_carry) begin
                $display("[PASS] %-14s a=%0d b=%0d -> res=%0d Z=%b N=%b C=%b",
                         name, ta, tb_, result, zero, negative, carry);
            end else begin
                errors = errors + 1;
                $display("[FAIL] %-14s a=%0d b=%0d op=%b", name, ta, tb_, top);
                $display("        got  res=%0d Z=%b N=%b C=%b",
                         result, zero, negative, carry);
                $display("        want res=%0d Z=%b N=%b C=%b",
                         exp_result, exp_zero, exp_neg, exp_carry);
            end
        end
    endtask

    initial begin
        $dumpfile("tb_alu_4bit.vcd");
        $dumpvars(0, tb_alu_4bit);

        // op codes: 000 ADD, 001 SUB, 010 AND, 011 OR,
        //           100 XOR, 101 INC, 110 DEC, 111 PASSTHRU

        //          name           a       b       op       res      Z N C
        check_alu("ADD",          4'd5,  4'd7,  3'b000,  4'd12,  0,1,0); // 5+7=12 (0b1100, N=1)
        check_alu("ADD carry",    4'd8,  4'd9,  3'b000,  4'd1,   0,0,1); // 17 -> 1, C=1
        check_alu("ADD zero",     4'd8,  4'd8,  3'b000,  4'd0,   1,0,1); // 16 -> 0, C=1
        check_alu("SUB",          4'd10, 4'd3,  3'b001,  4'd7,   0,0,1); // 10-3=7, no borrow
        // 3-10 = -7 -> 2's-comp 9. a<b => borrow => C=0 (N=1: bit3 set).
        check_alu("SUB borrow",   4'd3,  4'd10, 3'b001,  4'd9,   0,1,0);
        check_alu("SUB zero",     4'd6,  4'd6,  3'b001,  4'd0,   1,0,1); // equal, no borrow
        check_alu("AND",          4'd12, 4'd10, 3'b010,  4'd8,   0,1,0); // 1100&1010=1000
        check_alu("OR",           4'd5,  4'd10, 3'b011,  4'd15,  0,1,0); // 0101|1010=1111
        check_alu("XOR",          4'd12, 4'd10, 3'b100,  4'd6,   0,0,0); // 1100^1010=0110
        check_alu("INC",          4'd15, 4'd0,  3'b101,  4'd0,   1,0,1); // 15+1=0, C=1
        check_alu("INC mid",      4'd7,  4'd0,  3'b101,  4'd8,   0,1,0); // 7+1=8, N=1
        // DEC 0 -> 15. a=0 => borrow => C=0 (N=1: bit3 set).
        check_alu("DEC borrow",   4'd0,  4'd0,  3'b110,  4'd15,  0,1,0);
        check_alu("DEC",          4'd1,  4'd0,  3'b110,  4'd0,   1,0,1); // 1-1=0, no borrow
        check_alu("PASSTHRU",     4'd0,  4'd9,  3'b111,  4'd9,   0,1,0); // MOV: result=b

        $display("========================================");
        $display("ALU RESULT: %0d/%0d checks passed, %0d failed",
                 checks - errors, checks, errors);
        $display("========================================");
        if (errors == 0)
            $display("ALL ALU TESTS PASSED");
        else
            $display("SOME ALU TESTS FAILED");

        $finish;
    end

endmodule
