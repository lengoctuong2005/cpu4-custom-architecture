# imem/instruction_memory_sim.v — TKVM mo phong ($readmemh)
module instruction_memory #(
    parameter PROG = "programs/fib.hex"
)(
    input  wire [3:0] addr,
    output wire [8:0] instr
);
    reg [8:0] rom [0:15];
    integer k;
    initial begin
        for (k = 0; k < 16; k = k + 1) rom[k] = 9'h000; // mac dinh NOP
        $readmemh(PROG, rom);   // doc file hex 9-bit
    end
    assign instr = rom[addr];
endmodule
