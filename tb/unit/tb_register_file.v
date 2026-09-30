`timescale 1ns / 1ps

module tb_register_file;

    logic       clk;
    logic       rst_n;
    logic       reg_write;
    logic [1:0] read_reg1;
    logic [1:0] read_reg2;
    logic [1:0] write_reg;
    logic [3:0] write_data;
    logic [3:0] read_data1;
    logic [3:0] read_data2;
    logic [3:0] r0_out;

    integer errors = 0;

    register_file uut (
        .clk       (clk),
        .rst_n     (rst_n),
        .reg_write (reg_write),
        .read_reg1 (read_reg1),
        .read_reg2 (read_reg2),
        .write_reg (write_reg),
        .write_data(write_data),
        .read_data1(read_data1),
        .read_data2(read_data2),
        .r0_out    (r0_out)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        // 1. Reset check
        rst_n = 0;
        reg_write = 0;
        read_reg1 = 2'b00;
        read_reg2 = 2'b01;
        write_reg = 2'b00;
        write_data = 4'hF;
        #15;
        rst_n = 1;
        #1;
        if (read_data1 !== 4'h0 || read_data2 !== 4'h0 || r0_out !== 4'h0) begin
            $display("[FAIL] RF reset: got r1=%h r2=%h r0=%h", read_data1, read_data2, r0_out);
            errors = errors + 1;
        end else begin
            $display("[PASS] RF reset to 0");
        end

        // 2. Sequential writes to R0..R3
        reg_write = 1;
        // Write R0 = 4'hA
        write_reg = 2'b00; write_data = 4'hA; #10;
        // Write R1 = 4'hB
        write_reg = 2'b01; write_data = 4'hB; #10;
        // Write R2 = 4'hC
        write_reg = 2'b10; write_data = 4'hC; #10;
        // Write R3 = 4'hD
        write_reg = 2'b11; write_data = 4'hD; #10;

        reg_write = 0;
        #1;

        // 3. Read back all registers & verify dual asynchronous read ports
        read_reg1 = 2'b00; read_reg2 = 2'b01; #1;
        if (read_data1 !== 4'hA || read_data2 !== 4'hB || r0_out !== 4'hA) begin
            $display("[FAIL] Read R0/R1: got %h / %h", read_data1, read_data2);
            errors = errors + 1;
        end else begin
            $display("[PASS] Write & read R0=0xA, R1=0xB verified");
        end

        read_reg1 = 2'b10; read_reg2 = 2'b11; #1;
        if (read_data1 !== 4'hC || read_data2 !== 4'hD) begin
            $display("[FAIL] Read R2/R3: got %h / %h", read_data1, read_data2);
            errors = errors + 1;
        end else begin
            $display("[PASS] Write & read R2=0xC, R3=0xD verified");
        end

        // 4. Verify reg_write = 0 prevents modification
        write_reg = 2'b00; write_data = 4'h7; reg_write = 0;
        #10;
        read_reg1 = 2'b00; #1;
        if (read_data1 !== 4'hA) begin
            $display("[FAIL] Write disable failed: R0 was overwritten with %h", read_data1);
            errors = errors + 1;
        end else begin
            $display("[PASS] Write disable verified");
        end

        if (errors == 0) begin
            $display("ALL REGISTER FILE UNIT TESTS PASSED");
            $finish;
        end else begin
            $fatal(1, "REGISTER FILE UNIT TESTS FAILED");
        end
    end

endmodule
