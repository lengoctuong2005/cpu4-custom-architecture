`timescale 1ns / 1ps

module cpu_top (
    input  logic        clk,
    input  logic        rst_n,
    output logic [3:0]  out_port,
    output logic        halt_out,
    output logic [3:0]  debug_r0
);

    // PC
    logic [3:0] pc, pc_next;
    logic       pc_write;
    logic       halt;

    // Decode
    logic [3:0] opcode;
    logic [3:0] operand;
    logic       imm_mode;
    logic [3:0] imm_val;

    // Control
    logic        reg_write, mem_read, mem_write, mem_to_reg, alu_src, pc_src;
    logic [2:0]  alu_op;
    logic [1:0]  reg_sel;
    logic        flag_write;

    // Register File
    logic [3:0] read_data1, read_data2;
    logic [3:0] write_data;
    logic [1:0] write_reg;

    // ALU
    logic [3:0] alu_result;
    // ALU flags (combinational, from ALU each cycle)
    logic       zero, negative, carry;
    // ALU flags registered at the clock edge so branch/jump instructions
    // (JZ/JN) read the result of the *previous* executed instruction rather
    // than the (meaningless) ALU output of the branch cycle itself.
    logic       zero_r, negative_r;

    // Data Memory
    logic [3:0] mem_read_data;

    // Output register
    logic [3:0] out_reg;

    // Decoded instruction bus (9-bit). Declared explicitly to avoid
    // Icarus inferring a 1-bit scalar from the imem port connection.
    logic [8:0] instruction;

    // PC register
    program_counter pc_inst (
        .clk       (clk),
        .rst_n     (rst_n),
        .pc_write  (pc_write),
        .halt      (halt),
        .pc_next   (pc_next),
        .pc        (pc)
    );

    instruction_memory imem (
        .addr        (pc),
        .instruction (instruction)
    );

    // Decode instruction 9-bit
    //   [8]   = imm_mode (1: LDI #imm, 0: reg-reg / others)
    //   [7:4] = opcode
    //   [3:0] = operand:
    //           - MOV Rd, Rs : {Rd[3:2], Rs[1:0]}
    //           - LDI #imm   : imm[3:0] (ghi vao R0 ngam dinh, bo qua Rd)
    //           - LOAD/STORE : dia chi RAM [3:0]
    assign opcode    = instruction[7:4];
    assign operand   = instruction[3:0];
    assign imm_mode  = instruction[8];
    assign imm_val   = operand[3:0]; // imm 4-bit zero-extended (LDI)

    // Control Unit
    control_unit ctrl (
        .opcode      (opcode),
        .imm_mode    (imm_mode),
        .zero        (zero_r),
        .negative    (negative_r),
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

    // Register file write register selection
    assign write_reg = (reg_sel == 2'b01) ? operand[3:2] : 2'b00;

    logic [1:0] read_reg1_mux;
    assign read_reg1_mux = (opcode == 4'b0010) ? 2'b00 : // STORE reads R0
                           (opcode == 4'b1110) ? operand[1:0] : // OUT reads Rs
                           operand[3:2]; // Default reads Rd

    // Register File
    register_file rf (
        .clk         (clk),
        .rst_n       (rst_n),
        .reg_write   (reg_write),
        .read_reg1   (read_reg1_mux),
        .read_reg2   (operand[1:0]),
        .write_reg   (write_reg),
        .write_data  (write_data),
        .read_data1  (read_data1),
        .read_data2  (read_data2)
    );

    // ALU input mux
    logic [3:0] alu_b;
    // alu_src=1: chon operand. Neu LDI (imm_mode) thi chon imm_val (imm 4-bit),
    //            nguoc lai chon operand (dia chi cho LOAD/STORE).
    // alu_src=0: chon read_data2 (reg-reg).
    assign alu_b = alu_src ? (imm_mode ? imm_val : operand) : read_data2;

    // ALU
    alu_4bit alu (
        .a       (read_data1),
        .b       (alu_b),
        .op      (alu_op),
        .result  (alu_result),
        .zero    (zero),
        .negative(negative),
        .carry   (carry)
    );

    // Flag register: latch ALU flags at the clock edge so that branch
    // instructions (JZ/JN) in the next cycle read the result of the
    // *previous* executed arithmetic/logic instruction, not their own
    // (meaningless) ALU output. Cleared on reset.
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            zero_r    <= 1'b0;
            negative_r <= 1'b0;
        end else if (flag_write) begin
            zero_r    <= zero;
            negative_r <= negative;
        end
    end

    // Data Memory
    data_memory dmem (
        .clk        (clk),
        .mem_read   (mem_read),
        .mem_write  (mem_write),
        .addr       (operand),
        .write_data (read_data1),
        .read_data  (mem_read_data)
    );

    // Write-back mux
    assign write_data = mem_to_reg ? mem_read_data : alu_result;

    // PC next select
    assign pc_next = pc_src ? operand : pc + 1;

    // HALT logic
    assign halt = (opcode == 4'b1111);

    // PC write enable (not on HALT)
    assign pc_write = ~halt;

    // OUT port register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            out_reg <= 4'b0;
        else if (opcode == 4'b1110) // OUT
            out_reg <= read_data1;
    end

    assign out_port  = out_reg;
    assign halt_out  = halt;

    // Expose R0 for testbench inspection without hierarchical cross-module
    // references (Icarus 12.0 blocks cpu.rf.r0 access from the TB).
    // cpu_top instantiates rf directly, so rf.r0 is visible here.
    assign debug_r0 = rf.r0;

    // ---- Testbench helper tasks (keep $readmemh / RAM writes inside cpu_top) ----
    /* synthesis translate_off */
    // Load a hex program into the instruction ROM.
    task load_program(input string hex_path);
        $readmemh(hex_path, imem.rom);
    endtask

    // Preload data RAM locations 10 and 11 (operands for ADD/MUL demos).
    task preload_ram(input logic [3:0] a, input logic [3:0] b);
        dmem.ram[10] = a;
        dmem.ram[11] = b;
    endtask

    // Clear data RAM locations 10 and 11.
    task clear_ram;
        dmem.ram[10] = 4'h0;
        dmem.ram[11] = 4'h0;
    endtask
    /* synthesis translate_on */

endmodule
