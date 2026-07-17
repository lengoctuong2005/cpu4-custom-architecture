`timescale 1ns / 1ps

module register_file (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        reg_write,
    input  logic [1:0]  read_reg1,
    input  logic [1:0]  read_reg2,
    input  logic [1:0]  write_reg,
    input  logic [3:0]  write_data,
    output logic [3:0]  read_data1,
    output logic [3:0]  read_data2
);

    logic [3:0] r0, r1, r2, r3;


    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r0 <= 4'b0;
            r1 <= 4'b0;
            r2 <= 4'b0;
            r3 <= 4'b0;
        end else if (reg_write) begin
            case (write_reg)
                2'b00: r0 <= write_data;
                2'b01: r1 <= write_data;
                2'b10: r2 <= write_data;
                2'b11: r3 <= write_data;
            endcase
        end
    end

    always @(read_reg1, read_reg2, r0, r1, r2, r3) begin
        case (read_reg1)
            2'b00: read_data1 = r0;
            2'b01: read_data1 = r1;
            2'b10: read_data1 = r2;
            2'b11: read_data1 = r3;
            default: read_data1 = 4'b0;
        endcase

        case (read_reg2)
            2'b00: read_data2 = r0;
            2'b01: read_data2 = r1;
            2'b10: read_data2 = r2;
            2'b11: read_data2 = r3;
            default: read_data2 = 4'b0;
        endcase
    end

endmodule
