#!/usr/bin/env python3
"""100-edge public-interface gate/reference test for the fixed boot image.
Cell models come from the caller's Liberty; simulation is zero-delay, not SDF.
Any skipped unsupported library cells must be UNUSED by the mapped netlist.
"""
import os,re,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from sim_cpu import CPU,load_hex
out=ROOT/'build/synthesis';lib=Path(os.environ['LIBERTY']).resolve()
netlist=Path(os.environ.get('NETLIST',str(out/'cpu_top_mapped.v'))).resolve()
model=out/'library_simulation.v'
r=subprocess.run(['yosys','-Q','-T','-p',f'read_liberty -ignore_miss_func -ignore_miss_data_latch {lib}; write_verilog -noattr {model}'],text=True,capture_output=True,timeout=60)
(out/'libmodel.log').write_text(r.stdout+r.stderr)
if r.returncode:raise RuntimeError(r.stdout+r.stderr)
# Reject unresolved instances rather than silently simulating black boxes.
celltypes=set(re.findall(r'^\s+([A-Z][A-Za-z0-9_]+)\s+_[0-9]+_\s*\(',netlist.read_text(),re.M))
models=set(re.findall(r'^module\s+([A-Za-z0-9_]+)',model.read_text(),re.M))
if not celltypes<=models:raise AssertionError('Unmodelled used cells: '+str(celltypes-models))
c=CPU(load_hex(ROOT/'sim/fib.hex'));rows=[]
for i in range(100):
    en=0 if i%5==1 else 1
    if en:c.step()
    rows.append(f'{en:x} {c.out:x} {c.r[0]:x} {int(((c.rom[c.pc]>>4)&15)==15):x}\n')
vector=out/'gate_vectors.txt';vector.write_text(''.join(rows))
tb=out/'tb_gate_edges.sv';tb.write_text('''`timescale 1ns/1ps
module tb_gate_edges;
reg clk=0,rst_n=0,clk_en=0;always #5 clk=~clk;
wire[3:0]out_port,debug_r0;wire halt_out;integer f,rc,en,eo,er,eh;
cpu_top uut(.clk(clk),.clk_en(clk_en),.rst_n(rst_n),.out_port(out_port),.halt_out(halt_out),.debug_r0(debug_r0));
initial begin
 f=$fopen("'''+str(vector)+'''","r");if(!f)$fatal(1,"no vectors");
 #12;rst_n=1;
 for(integer i=0;i<100;i=i+1)begin
  rc=$fscanf(f,"%h %h %h %h",en,eo,er,eh);if(rc!=4)$fatal(1,"bad gate vector");
  clk_en=en;@(posedge clk);#1;
  if(out_port!==eo[3:0] || debug_r0!==er[3:0] || halt_out!==eh[0])
   $fatal(1,"gate/reference mismatch edge %0d got out/r0/halt=%h/%h/%h",i,out_port,debug_r0,halt_out);
  @(negedge clk);
 end
 $display("GATE INTERFACE PASS: 100 edges OUT/debug_r0/halt, includes enable stalls/HALT");$finish;
end
endmodule
''')
binary=out/'gate_edges.out'
subprocess.run(['iverilog','-g2012','-s','tb_gate_edges','-o',str(binary),str(tb),str(netlist),str(model)],check=True,timeout=60)
r=subprocess.run(['vvp',str(binary)],capture_output=True,text=True,timeout=60)
(out/('gate_eco_edges.log' if 'eco' in netlist.name else 'gate_edges.log')).write_text(r.stdout+r.stderr)
if r.returncode:raise AssertionError(r.stdout+r.stderr)
print(r.stdout,end='')
