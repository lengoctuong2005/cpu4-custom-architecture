#!/usr/bin/env python3
"""Two deliberately faulty temporary RTL variants MUST be rejected.
No mutated source is written to rtl/. This is detection evidence, not formal proof.
"""
import subprocess,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'build/verification';out.mkdir(parents=True,exist_ok=True)
results={}
with tempfile.TemporaryDirectory() as d:
    tmp=Path(d)
    for name in ('xor_to_or','unconditional_flags'):
        source=ROOT/'rtl'/('alu_4bit.v' if name=='xor_to_or' else 'cpu_top.v')
        text=source.read_text()
        old,new=('result = a ^ b;','result = a | b;') if name=='xor_to_or' else ('end else if (clk_en && flag_write)','end else if (clk_en)')
        assert old in text
        mutated=tmp/source.name;mutated.write_text(text.replace(old,new,1))
        if name=='xor_to_or':files=[ROOT/'tb/tb_alu_4bit.v',mutated];top='tb_alu_4bit'
        else:
            files=[ROOT/'tb/tb_cpu_top.v',*[p for p in sorted((ROOT/'rtl').glob('*.v')) if p.name!='cpu_top.v'],mutated];top='tb_cpu_top'
        binary=tmp/f'{name}.out'
        compile=subprocess.run(['iverilog','-g2012','-s',top,'-o',str(binary),*map(str,files)],text=True,capture_output=True,timeout=60)
        if compile.returncode:raise RuntimeError('Mutation compile error, not a valid detection: '+compile.stderr)
        run=subprocess.run(['vvp',str(binary)],cwd=ROOT,text=True,capture_output=True,timeout=60)
        (out/f'mutation_{name}.log').write_text(run.stdout+run.stderr)
        if run.returncode==0:raise AssertionError(f'Fault escaped tests: {name}')
        results[name]={'status':'DETECTED','exit_code':run.returncode}
(out/'mutation_summary.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
