#!/usr/bin/env python3
import subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'build/verification';out.mkdir(parents=True,exist_ok=True)
core=[str(ROOT/'rtl'/f'{n}.v') for n in ('alu_4bit','control_unit','data_memory','instruction_memory','program_counter','register_file','cpu_top')]
results={}
for name,tb,files in [('decode',ROOT/'tb/unit/tb_control_exhaustive.sv',[ROOT/'rtl/control_unit.v']),
 ('boot',ROOT/'tb/system/tb_boot.sv',core),('fpga',ROOT/'tb/system/tb_fpga.sv',core+[ROOT/'real/cpu_top_fpga.v'])]:
 binary=out/f'{name}.out';r=subprocess.run(['iverilog','-g2012','-s',f'tb_{"control_exhaustive" if name=="decode" else name}','-o',str(binary),str(tb),*map(str,files)],capture_output=True,text=True,timeout=60)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 r=subprocess.run(['vvp',str(binary)],capture_output=True,text=True,timeout=60)
 (out/f'{name}.log').write_text(r.stdout+r.stderr);print(r.stdout,end='')
 if r.returncode:raise RuntimeError(f'{name} failed: {r.stderr}')
 results[name]='PASS'
# Explicit-net elaboration; a real warning/error is a failure.
strict=out/'strict.v';strict.write_text('`default_nettype none\n'+'\n'.join(Path(p).read_text() for p in core)+'\n`default_nettype wire\n')
r=subprocess.run(['iverilog','-g2012','-Wall','-s','cpu_top','-o',str(out/'lint.out'),str(strict)],capture_output=True,text=True,timeout=60)
(out/'lint.log').write_text(r.stdout+r.stderr)
if r.returncode or 'warning:' in r.stderr or 'error:' in r.stderr:raise RuntimeError(r.stdout+r.stderr)
results['strict_net_elaboration']='PASS'
# Legacy wrapper compilation, without competing instruction_memory definitions.
r=subprocess.run(['iverilog','-g2012','-Wall','-s','cpu4_de10','-o',str(out/'legacy.out'),*core,str(ROOT/'real/cpu_top_fpga.v'),str(ROOT/'real/cpu4_de10.v')],capture_output=True,text=True,timeout=60)
(out/'legacy_compile.log').write_text(r.stdout+r.stderr)
if r.returncode:raise RuntimeError(r.stdout+r.stderr)
results['legacy_wrapper_elaboration']='PASS'
(out/'extra_summary.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
