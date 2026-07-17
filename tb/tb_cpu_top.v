`timescale 1ns / 1ps

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

    initial begin
        $display("TB INITIAL START");
        $fflush;

        // Xuat waveform de xem bang GTKWave
        $dumpfile("cpu_top.vcd");
        $dumpvars(0, tb_cpu_top);

        rst_n = 0;
        #12;
        // Nap chuong trinh vao ROM va du lieu dau vao vao RAM TRUOC khi giai phong reset.
        // mul.asm: Mem[10]=3 (so lan), Mem[11]=4 (so cong) -> tich = 12 = 0xC.
        uut.load_program("sim/mul.hex");
        uut.preload_ram(4'd3, 4'd4);
        rst_n = 1;

        // MUL loop = 3 vong lap x 5 lenh ~ 23 chu ky; chay 60 cho du phong.
        repeat (60) @(posedge clk);

        // Kiem tra ket qua truc tiep tu bo nho du lieu
        // Chuong trinh: Mem[10]=3, Mem[11]=4 -> tich 12 luu Mem[12]
        $display("Simulation finished:");
        $display("  out_port = %d (0x%h)", out_port, out_port);
        $display("  halt_out = %b", halt_out);
        $display("  Mem[12]  = %d (0x%h) [expected 12]",
                  uut.dmem.ram[12], uut.dmem.ram[12]);

        if (out_port == 4'd12 && uut.dmem.ram[12] == 4'd12) begin
            $display("TEST PASSED: OUT = 12, Mem[12] = 12 as expected");
        end else begin
            $error("TEST FAILED: OUT = %d, Mem[12] = %d, expected 12",
                    out_port, uut.dmem.ram[12]);
        end

        $finish;
    end

    // Monitor tung chu ky de hieu single-cycle datapath
    always @(posedge clk) begin
        $display("Time=%0t | PC=%d | Opcode=%b | Operand=%b | R0=%d R1=%d R2=%d R3=%d | OUT=%d | HALT=%b",
                 $time, uut.pc, uut.opcode, uut.operand,
                 uut.rf.r0, uut.rf.r1, uut.rf.r2, uut.rf.r3,
                 out_port, halt_out);
    end

endmodule
