`timescale 1ns / 1ps

module tb_data_memory;

    logic       clk;
    logic       mem_read;
    logic       mem_write;
    logic [3:0] addr;
    logic [3:0] write_data;
    logic [3:0] read_data;

    logic [3:0] exp;
    integer errors = 0;

    data_memory uut (
        .clk       (clk),
        .mem_read  (mem_read),
        .mem_write (mem_write),
        .addr      (addr),
        .write_data(write_data),
        .read_data (read_data)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        mem_read = 0;
        mem_write = 0;
        addr = 0;
        write_data = 0;
        #10;

        // 1. Check all 16 locations read 0 initially
        mem_read = 1;
        for (int i = 0; i < 16; i++) begin
            addr = i[3:0];
            #1;
            if (read_data !== 4'h0) begin
                $display("[FAIL] Initial RAM[%0d] = %h, expected 0", i, read_data);
                errors = errors + 1;
            end
        end
        if (errors == 0) $display("[PASS] Initial RAM cleared to 0");

        // 2. Write all 16 addresses with distinct patterns
        mem_read = 0;
        mem_write = 1;
        for (int i = 0; i < 16; i++) begin
            addr = i[3:0];
            write_data = (i ^ 4'hA) & 4'hF;
            #10;
        end
        mem_write = 0;

        // 3. Read back all 16 locations
        mem_read = 1;
        for (int i = 0; i < 16; i++) begin
            addr = i[3:0];
            #1;
            exp = (i ^ 4'hA) & 4'hF;
            if (read_data !== exp) begin
                $display("[FAIL] RAM[%0d] read = %h, expected %h", i, read_data, exp);
                errors = errors + 1;
            end
        end
        if (errors == 0) $display("[PASS] All 16 RAM addresses read/write verified");

        // 4. mem_read = 0 disables output (returns 0)
        mem_read = 0;
        addr = 4'h5; #1;
        if (read_data !== 4'h0) begin
            $display("[FAIL] mem_read=0 did not gate output to 0");
            errors = errors + 1;
        end else begin
            $display("[PASS] mem_read=0 gates output correctly");
        end

        // 5. mem_write = 0 prevents modification
        mem_read = 0;
        mem_write = 0;
        addr = 4'h0;
        write_data = 4'hF; // was 0 ^ 0xA = 0xA
        #10;
        mem_read = 1; #1;
        if (read_data !== 4'hA) begin
            $display("[FAIL] mem_write=0 failed to protect RAM[0]");
            errors = errors + 1;
        end else begin
            $display("[PASS] mem_write=0 prevents unintended write");
        end

        if (errors == 0) begin
            $display("ALL DATA MEMORY UNIT TESTS PASSED");
            $finish;
        end else begin
            $fatal(1, "DATA MEMORY UNIT TESTS FAILED");
        end
    end

endmodule
