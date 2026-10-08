#!/usr/bin/env python3
"""Compare PC/RF/Z/N/OUT/all RAM on every edge, including enable holds/HALT.
Run tests/test_software.py first: it independently checks mathematical ALU values.
Use --baseline against unmodified RTL (no clk_en) to isolate functional baseline.
"""
import argparse,random,subprocess,sys,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from sim_cpu import CPU,load_hex
from assembler import assemble

def cases():
    rng=random.Random(0xC4)
    # All raw words, including ignored fields, with all 4 initial flag combinations.
    for word in range(512):
        for flags in range(4):
            c=CPU([word]+[0]*15);c.r=[rng.randrange(16) for _ in range(4)]
            c.ram=[rng.randrange(16) for _ in range(16)];c.z=flags&1;c.n=flags>>1;c.out=rng.randrange(16)
            yield f'raw_{word:03x}_flags{flags}',c,[1]
    # Demo algorithm validity for every nibble input pair, plus post-HALT stability.
    for name,path in [('add','prog'),('mul','mul')]:
        for a in range(16):
            for b in range(16):
                c=CPU(load_hex(ROOT/f'sim/{path}.hex'),{10:a,11:b})
                yield f'{name}_{a}_{b}',c,[1]*100
    for name in ('fib','flag_test'):
        yield name,CPU(load_hex(ROOT/f'sim/{name}.hex')),[1]*100
    # Directed corner cases: signed overflow behavior, flags, wrap, branches, RAM edges.
    directed=[('overflow','LDI #7\nMOV R1,R0\nLDI #8\nSUB R1,R0\nJN done\nLDI #0\ndone: OUT R1\nHALT'),
      ('flag_keep','LDI #0\nMOV R1,R0\nSTORE 15\nLOAD 15\nNOP\nOUT R0\nJZ end\nLDI #9\nend: HALT'),
      ('ram_boundary','LDI #15\nSTORE 0\nSTORE 15\nLDI #0\nLOAD 0\nOUT R0\nLOAD 15\nOUT R0\nHALT'),
      ('repeated_out','LDI #4\nOUT R0\nOUT R0\nHALT')]
    for name,text in directed:yield name,CPU(assemble(text)),[1]*64
    c=CPU([0]*16);c.pc=15;yield 'pc_wrap',c,[1]*20
    # Random ROM/state/enable patterns: no claim of exhaustive program coverage.
    for seed in range(200):
        r=random.Random(seed);c=CPU([r.randrange(512) for _ in range(16)])
        c.r=[r.randrange(16) for _ in range(4)];c.ram=[r.randrange(16) for _ in range(16)]
        c.z=r.randrange(2);c.n=r.randrange(2);c.out=r.randrange(16)
        yield f'random_seed_{seed}',c,[r.randrange(2) for _ in range(128)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path);p.add_argument('--out',type=Path,default=ROOT/'build/verification');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True);src=a.baseline.resolve() if a.baseline else ROOT
    vectors=a.out/'vectors.txt';expected=[];names=[]
    with vectors.open('w') as f:
        for idx,(name,c,enables) in enumerate(cases()):
            if a.baseline:enables=[1]*len(enables)
            names.append(name)
            vals=[len(enables),c.pc,c.z,c.n,c.out,*c.r,*c.ram,*c.rom,*enables]
            f.write(' '.join(f'{v:x}' for v in vals)+'\n')
            for cycle,en in enumerate(enables):
                if en:c.step()
                expected.append((idx,cycle,c.state(),int(((c.rom[c.pc]>>4)&15)==15)))
    tb=(ROOT/'tb/system/tb_differential.sv').read_text()
    if a.baseline:tb=tb.replace('.clk_en(clk_en),','')
    tbpath=a.out/'tb_run.sv';tbpath.write_text(tb)
    files=[str(src/'rtl'/f'{name}.v') for name in ('alu_4bit','control_unit','data_memory','instruction_memory','program_counter','register_file','cpu_top')]
    binary=a.out/'diff.out';trace=a.out/'trace.txt'
    for cmd in (['iverilog','-g2012','-s','tb_differential','-o',str(binary),str(tbpath),*files],['vvp',str(binary),f'+VECTORS={vectors}',f'+TRACE={trace}']):
        r=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
        (a.out/('compile.log' if cmd[0]=='iverilog' else 'run.log')).write_text(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    rows=trace.read_text().splitlines()
    if len(rows)!=len(expected):raise AssertionError(f'Trace length {len(rows)} != {len(expected)}')
    for line,(idx,cyc,state,halt) in zip(rows,expected):
        tokens=line.split();got_id,got_cyc=map(int,tokens[:2])
        try:values=tuple(int(t,16) for t in tokens[2:])
        except ValueError:raise AssertionError(f'X/Z output: {names[idx]} cycle {cyc}: {line}') from None
        if (got_id,got_cyc,values)!=(idx,cyc,(*state,halt)):
            raise AssertionError(f'{names[idx]} cycle {cyc}\n got={line}\n want={state} halt={halt}')
    summary={'status':'PASS','scenarios':len(names),'compared_edges':len(rows),'seed_range':'0..199','raw_instruction_cases':2048,'add_mul_input_cases':512,'baseline':bool(a.baseline),'state_fields':'PC,R0..R3,Z,N,OUT,RAM[0..15],halt_out','protocol':'state injection in testbench only'}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
if __name__=='__main__':main()
