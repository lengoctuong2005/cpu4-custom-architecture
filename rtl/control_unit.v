`timescale 1ns / 1ps

module control_unit (
    input  logic [3:0]  opcode,
    input  logic        zero,
    input  logic        negative,
    input  logic        imm_mode,
    output logic        reg_write,
    output logic        mem_read,
    output logic        mem_write,
    output logic        mem_to_reg,
    output logic        alu_src,
    output logic [2:0]  alu_op,
    output logic        pc_src,
    output logic [1:0]  reg_sel,
    output logic        flag_write
);

    always @(opcode, imm_mode) begin
        // defaults
        reg_write  = 1'b0;
        mem_read   = 1'b0;
        mem_write  = 1'b0;
        mem_to_reg = 1'b0;
        alu_src    = 1'b0;
        alu_op     = 3'b000;
        reg_sel    = 2'b00;
        flag_write = 1'b0;

        case (opcode)
            4'b0000: begin // NOP
                alu_op = 3'b000; // ADD (passthru)
            end
            4'b0001: begin // LOAD
                reg_write  = 1'b1;
                mem_read   = 1'b1;
                mem_to_reg = 1'b1;
                alu_src    = 1'b1; // use immediate addr
                alu_op     = 3'b000; // ADD (addr calc)
                reg_sel    = 2'b00; // R0
            end
            4'b0010: begin // STORE
                mem_write  = 1'b1;
                alu_src    = 1'b1; // use immediate addr
                alu_op     = 3'b000; // ADD (addr calc)
            end
            4'b0011: begin
                if (imm_mode) begin // LDI #imm -> load immediate into R0 (implicit)
                    reg_write  = 1'b1;
                    mem_to_reg = 1'b0;
                    alu_src    = 1'b1;    // chọn imm_val
                    alu_op     = 3'b111;  // PASSTHRU (giữ nguyên imm)
                    reg_sel    = 2'b00;   // R0 (implicit register)
                    flag_write = 1'b1;
                end else begin // MOV Rd, Rs (reg-reg)
                    reg_write  = 1'b1;
                    mem_to_reg = 1'b0;
                    alu_src    = 1'b0;    // chọn read_data2 (Rs)
                    alu_op     = 3'b111;  // PASSTHRU
                    reg_sel    = 2'b01;   // Rd = operand[3:2]
                end
            end
            4'b0100: begin // ADD
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b000; // ADD
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b0101: begin // SUB
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b001; // SUB
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b0110: begin // AND
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b010; // AND
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b0111: begin // OR
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b011; // OR
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b1000: begin // XOR
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b100; // XOR
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b1001: begin // INC
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b101; // INC
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b1010: begin // DEC
                reg_write  = 1'b1;
                mem_to_reg = 1'b0;
                alu_src    = 1'b0;
                alu_op     = 3'b110; // DEC
                reg_sel    = 2'b01; // Rd
                flag_write = 1'b1;
            end
            4'b1011: begin // JMP
                // Handled continuously
            end
            4'b1100: begin // JZ
                // Handled continuously
            end
            4'b1101: begin // JN
                // Handled continuously
            end
            4'b1110: begin // OUT
                // no reg write, just output
                alu_op = 3'b000;
            end
            4'b1111: begin // HALT
                // pc_src = 0 (freeze PC by not updating in cpu_top)
            end
            default: begin
                alu_op = 3'b000;
            end
        endcase
    end

    assign pc_src = (opcode == 4'b1011) ? 1'b1 :
                    (opcode == 4'b1100) ? zero :
                    (opcode == 4'b1101) ? negative :
                    1'b0;

endmodule
