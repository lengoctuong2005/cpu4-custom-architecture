`timescale 1ns / 1ps

module tb_cpu;
    logic        clk;
    logic        rst_n;
    logic [3:0] out_port;
    logic        halt_out;
    logic [3:0] debug_r0;

    // DUT
    cpu_top cpu (
        .clk      (clk),
        .rst_n    (rst_n),
        .out_port (out_port),
        .halt_out (halt_out),
        .debug_r0 (debug_r0)
    );

    // Clock: 10ns period
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    int pass_count = 0;
    int fail_count = 0;

    // Run DUT until halt, return cycle count
    task run_until_halt(output int cyc);
        cyc = 0;
        while (!halt_out && cyc < 300) begin
            @(posedge clk);
            cyc++;
        end
    endtask

    task check(input string nm, input logic [3:0] exp_r0, input bit chk);
        int       cyc;
        logic [3:0] got_r0;
        begin
            run_until_halt(cyc);
            got_r0 = debug_r0;
            if (!halt_out) begin
                $display("[FAIL] %-4s : timeout after %0d cycles", nm, cyc);
                fail_count++;
            end else if (chk && got_r0 !== exp_r0) begin
                $display("[FAIL] %-4s : R0=0x%h, expected 0x%h", nm, got_r0, exp_r0);
                fail_count++;
            end else begin
                $display("[PASS] %-4s : R0=0x%h, cycles=%0d%s",
                         nm, got_r0, cyc, chk ? "" : " (HALT ok)");
                pass_count++;
            end
        end
    endtask

    task reset_pulse;
        rst_n = 0;
        @(posedge clk);
        @(posedge clk);
        rst_n = 1;
    endtask

    initial begin
        $dumpfile("sim/tb.vcd");
        $dumpvars(0, tb_cpu);

        // ---- Test 1: ADD (5 + 7 = 12) ----
        cpu.load_program("sim/prog.hex");
        cpu.preload_ram(4'h5, 4'h7);
        reset_pulse;
        check("ADD", 4'hC, 1'b1);

        // ---- Test 2: MUL (3 x 4 = 12) ----
        cpu.load_program("sim/mul.hex");
        cpu.preload_ram(4'h3, 4'h4);
        reset_pulse;
        check("MUL", 4'hC, 1'b1);

        // ---- Test 3: FIB (1,1,2,3,5,8 -> HALT) ----
        cpu.load_program("sim/fib.hex");
        cpu.clear_ram;
        reset_pulse;
        check("FIB", 4'h8, 1'b0);

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
