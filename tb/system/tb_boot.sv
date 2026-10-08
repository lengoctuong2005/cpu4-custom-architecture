`timescale 1ns/1ps
module tb_boot;
 reg clk=0,rst_n=0;always #5 clk=~clk;
 wire [3:0] out_port;wire halt_out;
 cpu_top uut(.clk(clk),.clk_en(1'b1),.rst_n(rst_n),.out_port(out_port),.halt_out(halt_out),.debug_r0());
 initial begin
   #12;rst_n=1;
   repeat(100)@(negedge clk);
   if(out_port!==4'd8 || halt_out!==1'b1)$fatal(1,"Default synthesized ROM boot failed");
   $display("BOOT PASS: default Fibonacci ROM OUT=8, HALT=1");$finish;
 end
endmodule
