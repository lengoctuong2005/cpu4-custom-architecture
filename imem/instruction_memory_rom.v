# imem/instruction_memory_rom.v — THTKVM tong hop (bang case, khong $readmemh)
module instruction_memory (
    input  wire [3:0] addr,
    output reg  [8:0] instr
);
    // Chuong trinh demo: 5 + 7 = 12, xuat ra OUT
    always @(*) begin
        case (addr)
            4'd0 : instr = 9'h135; // LDI #5     -> R0 = 5
            4'd1 : instr = 9'h034; // MOV R1,R0  -> R1 = 5
            4'd2 : instr = 9'h137; // LDI #7     -> R0 = 7
            4'd3 : instr = 9'h044; // ADD R1,R0  -> R1 = 12
            4'd4 : instr = 9'h0E1; // OUT R1     -> OUT = 12
            4'd5 : instr = 9'h0F0; // HALT
            default: instr = 9'h000; // NOP
        endcase
    end
endmodule
