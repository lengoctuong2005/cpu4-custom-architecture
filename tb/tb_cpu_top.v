`timescale 1ns / 1ps

// CANONICAL testbench for the TKVM 4-bit CPU.
// Runs three demos: MUL (3x4=12), ADD (5+7=12), FIB (1,1,2,3,5,8 -> HALT).
// For FIB it records the FULL OUT sequence (not just the final register)
// to exclude off-by-one / coincidental-final-value bugs like the old MUL bug.
//
// NOTE: rtl/tb_cpu.sv is archived (rtl/tb_cpu.sv.bak) and no longer used.
// This file is the only active testbench; Makefile points here.

module tb_cpu_top;

    logic        clk;
    logic        rst_n;
    logic [3:0]  out_port;
    logic        halt_out;

    cpu_top uut (
        .clk      (clk),
        .rst_n    (rst_n),
        .out_port (out_port),
        .halt_out (halt_out)
    );

    // Clock generation: 10ns period
    initial clk = 0;
    always #5 clk = ~clk;

    // FIB OUT capture
    logic [3:0] fib_seq [0:7];
    int         fib_cnt;
    bit         capturing_fib;

    // Counts
    int pass_count;
    int fail_count;

    // Capture OUT whenever the OUT opcode (1110) executes.
    logic [3:0] prev_opcode;
    always @(posedge clk) begin
        prev_opcode <= uut.opcode;
        if (capturing_fib && prev_opcode == 4'b1110) begin
            if (fib_cnt < 8) begin
                fib_seq[fib_cnt] = out_port;
                fib_cnt = fib_cnt + 1;
            end
        end
    end

    // Run a demo: load program, set RAM, reset, run until HALT (or timeout).
    task run_demo(input string name,
                  input string hex_path,
                  input logic [3:0] ram_a,
                  input logic [3:0] ram_b,
                  input bit use_ram);
        int cyc;
        begin
            $display("---- %s ----", name);
            rst_n = 0;
            #12;
            uut.load_program(hex_path);
            if (use_ram)
                uut.preload_ram(ram_a, ram_b);
            else
                uut.clear_ram;
            rst_n = 1;

            cyc = 0;
            while (!halt_out && cyc < 300) begin
                @(posedge clk);
                cyc = cyc + 1;
            end

            if (!halt_out) begin
                $display("[FAIL] %s : timeout after %0d cycles", name, cyc);
                fail_count = fail_count + 1;
            end else begin
                $display("[PASS] %s : halt after %0d cycles, out_port=%0d (0x%h)",
                         name, cyc, out_port, out_port);
                pass_count = pass_count + 1;
            end
        end
    endtask

    initial begin
        $display("TB INITIAL START");
        $fflush;

        $dumpfile("cpu_top.vcd");
        $dumpvars(0, tb_cpu_top);

        pass_count = 0;
        fail_count = 0;
        fib_cnt    = 0;
        capturing_fib = 1'b0;

        // ---- MUL: 3 x 4 = 12, stored Mem[12]=12 ----
        run_demo("MUL", "sim/mul.hex", 4'd3, 4'd4, 1'b1);
        if (!(out_port == 4'd12 && uut.dmem.ram[12] == 4'd12)) begin
            $error("MUL VALUE CHECK FAILED: out_port=%0d Mem[12]=%0d",
                   out_port, uut.dmem.ram[12]);
            fail_count = fail_count + 1;
        end else begin
            $display("MUL value check OK: OUT=12, Mem[12]=12");
        end

        // ---- ADD: 5 + 7 = 12, stored Mem[12]=12 ----
        run_demo("ADD", "sim/prog.hex", 4'd5, 4'd7, 1'b1);
        if (!(out_port == 4'd12 && uut.dmem.ram[12] == 4'd12)) begin
            $error("ADD VALUE CHECK FAILED: out_port=%0d Mem[12]=%0d",
                   out_port, uut.dmem.ram[12]);
            fail_count = fail_count + 1;
        end else begin
            $display("ADD value check OK: OUT=12, Mem[12]=12");
        end

        // ---- FIB: full OUT sequence must be 1,1,2,3,5,8 ----
        fib_cnt = 0;
        capturing_fib = 1'b1;
        run_demo("FIB", "sim/fib.hex", 4'd0, 4'd0, 1'b0);
        capturing_fib = 1'b0;

        $display("FIB OUT sequence captured (%0d values):", fib_cnt);
        for (int i = 0; i < fib_cnt; i = i + 1)
            $display("  OUT[%0d] = %0d", i, fib_seq[i]);

        // Expected full sequence 1,1,2,3,5,8
        if (fib_cnt != 6) begin
            $error("FIB SEQUENCE LENGTH FAILED: got %0d, expected 6", fib_cnt);
            fail_count = fail_count + 1;
        end else begin
            bit seq_ok;
            seq_ok = (fib_seq[0]==4'd1) && (fib_seq[1]==4'd1) &&
                     (fib_seq[2]==4'd2) && (fib_seq[3]==4'd3) &&
                     (fib_seq[4]==4'd5) && (fib_seq[5]==4'd8);
            if (!seq_ok) begin
                $error("FIB SEQUENCE MISMATCH: expected 1,1,2,3,5,8");
                fail_count = fail_count + 1;
            end else begin
                $display("FIB sequence OK: 1,1,2,3,5,8 (full match, no off-by-one)");
            end
        end

        // ---- FLAG: test flag_write with MOV in between ----
        run_demo("FLAG", "sim/flag_test.hex", 4'd0, 4'd0, 1'b0);
        if (out_port != 4'd12) begin
            $error("FLAG VALUE CHECK FAILED: out_port=%0d, expected 12", out_port);
            fail_count = fail_count + 1;
        end else begin
            $display("FLAG value check OK: OUT=12");
        end

        $display("========================================");
        $display("RESULT: %0d PASS, %0d FAIL", pass_count, fail_count);
        $display("========================================");
        if (fail_count == 0)
            $display("ALL TESTS PASSED");
        else
            $display("SOME TESTS FAILED");

        $finish;
    end

endmodule
