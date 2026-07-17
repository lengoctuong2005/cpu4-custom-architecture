`timescale 1ns / 1ps

module data_memory (
    input  logic        clk,
    input  logic        mem_read,
    input  logic        mem_write,
    input  logic [3:0]  addr,
    input  logic [3:0]  write_data,
    output logic [3:0]  read_data
);

    logic [3:0] ram [0:15];

    // RAM khoi tao 0. Testbench se nap du lieu dau vao (preload) tuy tung chuong trinh.
    initial begin
        for (int i = 0; i < 16; i = i + 1)
            ram[i] = 4'h0;
    end

    always @(posedge clk) begin
        if (mem_write)
            ram[addr] <= write_data;
    end

    assign read_data = mem_read ? ram[addr] : 4'b0;

endmodule
