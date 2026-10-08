`timescale 1ns/1ps
// Reproducible vector protocol: cycles, PC/Z/N/OUT, RF[4], RAM[16], ROM[16], EN[cycles].
// Hierarchical state injection is testbench-only. Sample after NBA settles.
module tb_differential;
    reg clk=0; always #5 clk=~clk;
    reg rst_n=0,clk_en=1;
    wire [3:0] out_port,debug_r0;wire halt_out;
    cpu_top uut(.clk(clk),.clk_en(clk_en),.rst_n(rst_n),
        .out_port(out_port),.halt_out(halt_out),.debug_r0(debug_r0));
    integer fd,trace_fd,rc,ncycles,tmp,index=0;
    reg [3:0] initial_pc,initial_out,rf[0:3];reg initial_z,initial_n;
    string vectors,trace_file;
    task read_value;
        begin rc=$fscanf(fd,"%h",tmp);if(rc!=1)$fatal(1,"Malformed vector at case %0d",index);end
    endtask
    initial begin
        if(!$value$plusargs("VECTORS=%s",vectors) || !$value$plusargs("TRACE=%s",trace_file))
            $fatal(1,"Missing vectors/trace args");
        fd=$fopen(vectors,"r");trace_fd=$fopen(trace_file,"w");
        if(!fd || !trace_fd)$fatal(1,"Cannot open vector/trace files");
        while(!$feof(fd)) begin
            rc=$fscanf(fd,"%h",ncycles);
            if(rc==1) begin
                @(negedge clk);rst_n=0;clk_en=0;
                @(negedge clk);
                read_value;initial_pc=tmp;read_value;initial_z=tmp;
                read_value;initial_n=tmp;read_value;initial_out=tmp;
                for(integer j=0;j<4;j=j+1)begin read_value;rf[j]=tmp;end
                for(integer j=0;j<16;j=j+1)begin read_value;uut.dmem.ram[j]=tmp;end
                for(integer j=0;j<16;j=j+1)begin read_value;uut.imem.rom[j]=tmp;end
                rst_n=1;
                uut.pc_inst.pc=initial_pc;uut.zero_r=initial_z;uut.negative_r=initial_n;
                uut.rf.r0=rf[0];uut.rf.r1=rf[1];uut.rf.r2=rf[2];uut.rf.r3=rf[3];uut.out_reg=initial_out;
                for(integer cyc=0;cyc<ncycles;cyc=cyc+1)begin
                    read_value;clk_en=tmp;
                    @(posedge clk);#1;
                    $fwrite(trace_fd,"%0d %0d %h %h %h %h %h %h %h %h",index,cyc,
                        uut.pc,uut.rf.r0,uut.rf.r1,uut.rf.r2,uut.rf.r3,
                        uut.zero_r,uut.negative_r,out_port);
                    for(integer j=0;j<16;j=j+1)$fwrite(trace_fd," %h",uut.dmem.ram[j]);
                    $fwrite(trace_fd," %h\n",halt_out);
                    @(negedge clk);
                end
                index=index+1;
            end
        end
        $fclose(fd);$fclose(trace_fd);$display("TRACE CASES: %0d",index);$finish;
    end
endmodule
