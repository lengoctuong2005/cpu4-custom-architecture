`timescale 1ns / 1ps

module tb_control_unit;

    logic [3:0] opcode;
    logic       flag_zero_in;
    logic       flag_neg_in;
    logic       imm_mode;
    logic       reg_write;
    logic       mem_read;
    logic       mem_write;
    logic       mem_to_reg;
    logic       alu_src;
    logic [2:0] alu_op;
    logic       pc_src;
    logic [1:0] reg_sel;
    logic       flag_write;

    integer errors = 0;

    control_unit uut (
        .opcode      (opcode),
        .flag_zero_in(flag_zero_in),
        .flag_neg_in (flag_neg_in),
        .imm_mode    (imm_mode),
        .reg_write   (reg_write),
        .mem_read    (mem_read),
        .mem_write   (mem_write),
        .mem_to_reg  (mem_to_reg),
        .alu_src     (alu_src),
        .alu_op      (alu_op),
        .pc_src      (pc_src),
        .reg_sel     (reg_sel),
        .flag_write  (flag_write)
    );

    initial begin
        flag_zero_in = 0;
        flag_neg_in = 0;
        imm_mode = 0;

        // 1. NOP (0x0)
        opcode = 4'h0; #1;
        if (reg_write || mem_read || mem_write || pc_src || flag_write) begin
            $display("[FAIL] NOP generated active control signals");
            errors = errors + 1;
        end else begin
            $display("[PASS] NOP control decoded");
        end

        // 2. LOAD (0x1): reg_write=1, mem_read=1, mem_to_reg=1, reg_sel=00 (R0)
        opcode = 4'h1; #1;
        if (!reg_write || !mem_read || !mem_to_reg || reg_sel !== 2'b00 || mem_write) begin
            $display("[FAIL] LOAD control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] LOAD control decoded");
        end

        // 3. STORE (0x2): mem_write=1, reg_write=0, mem_read=0
        opcode = 4'h2; #1;
        if (!mem_write || reg_write || mem_read) begin
            $display("[FAIL] STORE control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] STORE control decoded");
        end

        // 4. MOV (0x3, imm_mode=0): reg_write=1, mem_to_reg=0, alu_src=0 (Rs), reg_sel=01 (Rd), flag_write=0
        opcode = 4'h3; imm_mode = 0; #1;
        if (!reg_write || mem_to_reg || alu_src || reg_sel !== 2'b01 || flag_write) begin
            $display("[FAIL] MOV reg-reg control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] MOV reg-reg control decoded");
        end

        // 5. LDI (0x3, imm_mode=1): reg_write=1, alu_src=1 (imm), reg_sel=00 (R0), flag_write=1
        opcode = 4'h3; imm_mode = 1; #1;
        if (!reg_write || !alu_src || reg_sel !== 2'b00 || !flag_write) begin
            $display("[FAIL] LDI immediate control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] LDI immediate control decoded");
        end
        imm_mode = 0;

        // 6. ADD (0x4): reg_write=1, alu_op=000, reg_sel=01, flag_write=1
        opcode = 4'h4; #1;
        if (!reg_write || alu_op !== 3'b000 || reg_sel !== 2'b01 || !flag_write) begin
            $display("[FAIL] ADD control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] ADD control decoded");
        end

        // 7. SUB (0x5): reg_write=1, alu_op=001, reg_sel=01, flag_write=1
        opcode = 4'h5; #1;
        if (!reg_write || alu_op !== 3'b001 || !flag_write) begin
            $display("[FAIL] SUB control signals incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] SUB control decoded");
        end

        // 8. JMP (0xB): unconditional branch pc_src=1
        opcode = 4'hB; #1;
        if (!pc_src) begin
            $display("[FAIL] JMP pc_src is 0");
            errors = errors + 1;
        end else begin
            $display("[PASS] JMP unconditional jump decoded");
        end

        // 9. JZ (0xC): pc_src follows flag_zero_in
        opcode = 4'hC; flag_zero_in = 0; #1;
        if (pc_src !== 1'b0) begin
            $display("[FAIL] JZ taken when Z=0");
            errors = errors + 1;
        end
        flag_zero_in = 1; #1;
        if (pc_src !== 1'b1) begin
            $display("[FAIL] JZ not taken when Z=1");
            errors = errors + 1;
        end else begin
            $display("[PASS] JZ conditional jump verified for Z=0 and Z=1");
        end
        flag_zero_in = 0;

        // 10. JN (0xD): pc_src follows flag_neg_in
        opcode = 4'hD; flag_neg_in = 0; #1;
        if (pc_src !== 1'b0) begin
            $display("[FAIL] JN taken when N=0");
            errors = errors + 1;
        end
        flag_neg_in = 1; #1;
        if (pc_src !== 1'b1) begin
            $display("[FAIL] JN not taken when N=1");
            errors = errors + 1;
        end else begin
            $display("[PASS] JN conditional jump verified for N=0 and N=1");
        end
        flag_neg_in = 0;

        // 11. OUT (0xE): reg_write=0, mem_write=0
        opcode = 4'hE; #1;
        if (reg_write || mem_write || pc_src) begin
            $display("[FAIL] OUT wrote state");
            errors = errors + 1;
        end else begin
            $display("[PASS] OUT control decoded");
        end

        // 12. HALT (0xF): pc_src=0, reg_write=0, mem_write=0
        opcode = 4'hF; #1;
        if (reg_write || mem_write || pc_src) begin
            $display("[FAIL] HALT control incorrect");
            errors = errors + 1;
        end else begin
            $display("[PASS] HALT control decoded");
        end

        if (errors == 0) begin
            $display("ALL CONTROL UNIT UNIT TESTS PASSED");
            $finish;
        end else begin
            $fatal(1, "CONTROL UNIT UNIT TESTS FAILED");
        end
    end

endmodule
