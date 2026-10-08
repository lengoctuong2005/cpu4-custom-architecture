`timescale 1ns/1ps
module tb_control_exhaustive;
    reg [3:0] opcode;reg z,n,imm;
    wire rw,mr,mw,mtr,src,pcs,fw;wire [2:0] op;wire [1:0] sel;
    reg erw,emr,emw,emtr,esrc,epcs,efw;reg [2:0] eop;reg [1:0] esel;
    integer checks=0;
    control_unit uut(.opcode(opcode),.flag_zero_in(z),.flag_neg_in(n),.imm_mode(imm),
        .reg_write(rw),.mem_read(mr),.mem_write(mw),.mem_to_reg(mtr),.alu_src(src),
        .alu_op(op),.pc_src(pcs),.reg_sel(sel),.flag_write(fw));
    initial begin
      for(integer word=0;word<512;word=word+1)
        for(integer fl=0;fl<4;fl=fl+1)begin
          opcode=(word>>4)&15;imm=(word>>8)&1;z=fl&1;n=(fl>>1)&1;
          erw=0;emr=0;emw=0;emtr=0;esrc=0;epcs=0;efw=0;eop=0;esel=0;
          case(opcode)
            1:begin erw=1;emr=1;emtr=1;esrc=1;end
            2:begin emw=1;esrc=1;end
            3:begin erw=1;eop=7;if(imm)begin esrc=1;efw=1;end else esel=1;end
            4,5,6,7,8:begin erw=1;esel=1;efw=1;eop=opcode-4;end
            9,10:begin erw=1;esel=1;efw=1;eop=opcode-4;end
            11:epcs=1;12:epcs=z;13:epcs=n;
          endcase
          #1;checks=checks+1;
          if({rw,mr,mw,mtr,src,pcs,fw,op,sel} !== {erw,emr,emw,emtr,esrc,epcs,efw,eop,esel})
            $fatal(1,"Decode mismatch word=%h flags=%d",word,fl);
        end
      $display("CONTROL EXHAUSTIVE PASS: %0d instruction/flag combinations",checks);$finish;
    end
endmodule
