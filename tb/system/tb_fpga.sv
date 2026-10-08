`timescale 1ns/1ps
module tb_fpga;
 reg clk=0;always #5 clk=~clk;
 reg [1:0] key=2'b10;reg [0:0] sw=0;
 wire [9:0] led;wire [6:0] hex0,hex1;
 integer pulses=0,before_auto;
 cpu_top_fpga #(.AUTO_CYCLES(4),.DEBOUNCE_CYCLES(3)) dut(.CLOCK_50(clk),.KEY(key),.SW(sw),.LEDR(led),.HEX0(hex0),.HEX1(hex1));
 always @(posedge clk)if(dut.rst_n && dut.cpu_enable)pulses=pulses+1;
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 initial begin
   ticks(3);key[0]=1;ticks(10);
   if(pulses!=0)$fatal(1,"Unexpected step after reset");
   key[1]=0;ticks(1);key[1]=1;ticks(1);key[1]=0;ticks(1);key[1]=1;ticks(10);
   if(pulses!=0)$fatal(1,"Short button bounce executed an instruction");
   key[1]=0;ticks(20);
   if(pulses!=1)$fatal(1,"One press must generate one pulse, got %0d",pulses);
   ticks(20);if(pulses!=1)$fatal(1,"Held key retriggered");
   key[1]=1;ticks(12);key[1]=0;ticks(12);
   if(pulses!=2)$fatal(1,"Second press failed");
   key[1]=1;ticks(12);before_auto=pulses;sw=1;ticks(160);
   if(pulses-before_auto<30 || led[3:0]!==4'd8 || led[4]!==1'b1)
     $fatal(1,"Auto/default boot failed");
   sw=0;ticks(10);before_auto=pulses;ticks(20);
   if(pulses!=before_auto)$fatal(1,"Auto continued in manual mode");
   key[0]=0;ticks(2);if(dut.cpu_inst.pc!==4'd0)$fatal(1,"Reset did not clear PC");
   $display("FPGA LOGIC PASS: reset, bounce, single press, held key, mode switch, auto boot");$finish;
 end
endmodule
