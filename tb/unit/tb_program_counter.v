`timescale 1ns / 1ps

module tb_program_counter;

    logic       clk;
    logic       rst_n;
    logic       pc_write;
    logic       halt;
    logic [3:0] pc_next;
    logic [3:0] pc;

    integer errors = 0;

    program_counter uut (
        .clk     (clk),
        .rst_n   (rst_n),
        .pc_write(pc_write),
        .halt    (halt),
        .pc_next (pc_next),
        .pc      (pc)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        // 1. Reset check
        rst_n = 0;
        pc_write = 1;
        halt = 0;
        pc_next = 4'hA;
        #15;
        if (pc !== 4'h0) begin
            $display("[FAIL] PC after reset: got %h, expected 0", pc);
            errors = errors + 1;
        end else begin
            $display("[PASS] PC reset to 0");
        end

        // 2. Normal load
        rst_n = 1;
        pc_next = 4'h5;
        #10;
        if (pc !== 4'h5) begin
            $display("[FAIL] PC load 5: got %h, expected 5", pc);
            errors = errors + 1;
        end else begin
            $display("[PASS] PC loaded 5");
        end

        // 3. pc_write disabled
        pc_write = 0;
        pc_next = 4'h9;
        #10;
        if (pc !== 4'h5) begin
            $display("[FAIL] PC write disabled: got %h, expected 5", pc);
            errors = errors + 1;
        end else begin
            $display("[PASS] PC retained value when pc_write=0");
        end

        // 4. Halt freezes PC even if pc_write=1
        pc_write = 1;
        halt = 1;
        pc_next = 4'hC;
        #10;
        if (pc !== 4'h5) begin
            $display("[FAIL] PC halt freeze: got %h, expected 5", pc);
            errors = errors + 1;
        end else begin
            $display("[PASS] PC frozen when halt=1");
        end

        // 5. Unfreeze and modulo 16 wraparound
        halt = 0;
        pc_next = 4'hF;
        #10;
        if (pc !== 4'hF) begin
            $display("[FAIL] PC load 15: got %h", pc);
            errors = errors + 1;
        end
        pc_next = 4'h0;
        #10;
        if (pc !== 4'h0) begin
            $display("[FAIL] PC wraparound to 0: got %h", pc);
            errors = errors + 1;
        end else begin
            $display("[PASS] PC wraparound 15 -> 0 verified");
        end

        if (errors == 0) begin
            $display("ALL PROGRAM COUNTER UNIT TESTS PASSED");
            $finish;
        end else begin
            $fatal(1, "PROGRAM COUNTER UNIT TESTS FAILED");
        end
    end

endmodule
