`timescale 1ns / 1ps

module tb_alu_4bit;

    logic [3:0] a, b;
    logic [2:0] op;
    logic [3:0] result;
    logic       zero, negative, carry;

    alu_4bit uut (
        .a       (a),
        .b       (b),
        .op      (op),
        .result  (result),
        .zero    (zero),
        .negative(negative),
        .carry   (carry)
    );

    initial begin
        $dumpfile("tb_alu_4bit.vcd");
        $dumpvars(0, tb_alu_4bit);

        // Test ADD: 5 + 7 = 12 (0xC), carry=0
        a=4'd5; b=4'd7; op=3'b000; #10;
        assert(result==4'd12 && carry==0) else $error("ADD fail: %d+%d=%d c=%b", a,b,result,carry);

        // Test ADD with carry: 8 + 9 = 17 -> 1 (carry=1)
        a=4'd8; b=4'd9; op=3'b000; #10;
        assert(result==4'd1 && carry==1) else $error("ADD carry fail");

        // Test SUB: 10 - 3 = 7
        a=4'd10; b=4'd3; op=3'b001; #10;
        assert(result==4'd7) else $error("SUB fail");

        // Test SUB borrow: 3 - 10 = -7 (2's comp = 9), borrow=1
        a=4'd3; b=4'd10; op=3'b001; #10;
        assert(result==4'd9 && carry==1) else $error("SUB borrow fail");

        // Test AND: 12 & 10 = 8
        a=4'd12; b=4'd10; op=3'b010; #10;
        assert(result==4'd8) else $error("AND fail");

        // Test OR: 5 | 10 = 15
        a=4'd5; b=4'd10; op=3'b011; #10;
        assert(result==4'd15) else $error("OR fail");

        // Test XOR: 12 ^ 10 = 6
        a=4'd12; b=4'd10; op=3'b100; #10;
        assert(result==4'd6) else $error("XOR fail");

        // Test INC: 15 + 1 = 0 (carry=1)
        a=4'd15; b=4'd0; op=3'b101; #10;
        assert(result==4'd0 && carry==1) else $error("INC fail");

        // Test DEC: 0 - 1 = 15 (borrow=1)
        a=4'd0; b=4'd0; op=3'b110; #10;
        assert(result==4'd15 && carry==1) else $error("DEC fail");

        // Test PASSTHRU (MOV)
        a=4'd0; b=4'd9; op=3'b111; #10;
        assert(result==4'd9) else $error("PASSTHRU fail");

        $display("ALU all tests passed!");
        $finish;
    end

endmodule
