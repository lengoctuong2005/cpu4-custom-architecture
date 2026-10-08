#!/usr/bin/env python3
"""Cycle-stepped CPU4 v1 reference. Architectural state includes Z/N, not C/V.
RAM initialization is a simulation/boot contract; CPU reset preserves RAM.
Timeout is an error, never HALT. OUT events are captured even if value repeats.
"""
import argparse
import re
from pathlib import Path
from isa import decode,alu

def mask4(value): return value & 15

def load_hex(path):
    words=[]
    for n,raw in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        line=re.split(r';|//',raw,maxsplit=1)[0].strip()
        if not line: continue
        if not re.fullmatch(r'[0-9a-fA-F]{1,3}',line):
            raise ValueError(f'Line {n}: expected one hexadecimal instruction')
        w=int(line,16)
        if w>511: raise ValueError(f'Line {n}: word exceeds 9 bits')
        words.append(w)
        if len(words)>16: raise ValueError('ROM image exceeds 16 words')
    if not words: raise ValueError('Empty ROM image')
    return words+[0]*(16-len(words))

class CPU:
    def __init__(self,rom,ram_init=None):
        if not 1<=len(rom)<=16 or any(not isinstance(w,int) or not 0<=w<=511 for w in rom):
            raise ValueError('Invalid ROM image')
        self.rom=list(rom)+[0]*(16-len(rom));self.ram=[0]*16
        for a,v in (ram_init or {}).items():
            if not 0<=a<=15 or not 0<=v<=15: raise ValueError('RAM init outside 0..15')
            self.ram[a]=v
        self.reset()
    def reset(self):
        self.r=[0]*4;self.pc=0;self.out=0;self.z=0;self.n=0
        self.halted=False;self.cycle=0;self.out_events=[]
    def state(self): return (self.pc,*self.r,self.z,self.n,self.out,*self.ram)
    def step(self):
        if self.halted: return False
        word=self.rom[self.pc];name,operand=decode(word)
        rd=(operand>>2)&3;rs=operand&3;next_pc=(self.pc+1)&15
        pre=(self.pc,name,operand,list(self.r),self.out,(self.z,self.n))
        if name=='LOAD': self.r[0]=self.ram[operand]
        elif name=='STORE': self.ram[operand]=self.r[0]
        elif name=='MOV': self.r[rd]=self.r[rs]
        elif name=='LDI':
            self.r[0]=operand;self.z=int(operand==0);self.n=operand>>3
        elif name in ('ADD','SUB','AND','OR','XOR','INC','DEC'):
            op={'ADD':0,'SUB':1,'AND':2,'OR':3,'XOR':4,'INC':5,'DEC':6}[name]
            result,z,n,_=alu(op,self.r[rd],self.r[rs])
            self.r[rd]=result;self.z=z;self.n=n
        elif name=='JMP': next_pc=operand
        elif name=='JZ' and self.z: next_pc=operand
        elif name=='JN' and self.n: next_pc=operand
        elif name=='OUT': self.out=self.r[rs];self.out_events.append(self.out)
        elif name=='HALT': self.halted=True
        if not self.halted: self.pc=next_pc
        self.cycle+=1
        return pre,name,operand
    def run(self,max_cycles=200,trace=False):
        if max_cycles<1: raise ValueError('max_cycles must be positive')
        while not self.halted and self.cycle<max_cycles:
            snapshot=self.step()
            if trace: print(self.cycle-1,snapshot[0],'=>',self.state())
        if not self.halted: raise TimeoutError(f'No HALT within {max_cycles} cycles')
        print(f'OUT={self.out}; R={self.r}; Z={self.z}; N={self.n}; cycles={self.cycle}')
        print(f'OUT sequence={self.out_events}; RAM={self.ram}')
        return self

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('hex_path',type=Path);p.add_argument('--trace',action='store_true')
    p.add_argument('--max-cycles',type=int,default=200);p.add_argument('--ram',default='')
    args=p.parse_args()
    try:
        ram={int(a):int(v) for a,v in (item.split('=') for item in args.ram.split(',') if item)}
        CPU(load_hex(args.hex_path),ram).run(args.max_cycles,args.trace)
    except (ValueError,OSError,TimeoutError) as e: p.exit(1,f'[ERROR] {e}\n')
if __name__=='__main__': main()
