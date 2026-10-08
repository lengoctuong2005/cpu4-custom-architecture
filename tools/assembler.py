#!/usr/bin/env python3
"""Strict two-pass assembler for CPU4 v1; 16 words, 9 bits per word.
Comments: ; or //. Labels: identifier:, optionally before an instruction.
Bit8 is set only for LDI. No MVI/JC/CMP/ADC pseudo-instructions.
"""
import argparse
import re
from pathlib import Path
from isa import OPCODES,REG_NAMES,ADDR_OPS,RR_OPS,ONE_REG_OPS

LABEL = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$')

def parse_int(text):
    text=text.strip()
    return int(text,16 if text.lower().startswith(('0x','-0x','+0x')) else 10)

def strip_comment(line):
    return re.split(r';|//',line,maxsplit=1)[0].strip()

def assemble_line(line, labels, line_no):
    line=strip_comment(line)
    if not line: return None,'EMPTY'
    parts=line.split(None,1); mnem=parts[0].upper()
    operands=parts[1].strip() if len(parts)>1 else ''
    try:
        if mnem not in OPCODES: raise ValueError(f'unknown mnemonic {mnem}')
        imm=0
        if mnem in ('NOP','HALT'):
            if operands: raise ValueError(f'{mnem} takes no operands')
            operand=0
        elif mnem in ADDR_OPS:
            if not operands: raise ValueError(f'{mnem} needs an address')
            if operands in labels: operand=labels[operands]
            else:
                try: operand=parse_int(operands)
                except ValueError: raise ValueError(f'unknown label/address {operands}') from None
            if not 0 <= operand <= 15: raise ValueError('address outside 0..15')
        elif mnem in RR_OPS:
            regs=[r.strip().upper() for r in operands.split(',')]
            if len(regs)!=2 or any(r not in REG_NAMES for r in regs):
                raise ValueError(f'{mnem} needs Rd,Rs in R0..R3')
            operand=REG_NAMES[regs[0]]*4+REG_NAMES[regs[1]]
        elif mnem=='LDI':
            if not operands.startswith('#'): raise ValueError('LDI needs #imm')
            operand=parse_int(operands[1:])
            if not 0 <= operand <= 15: raise ValueError('immediate outside 0..15')
            imm=1
        elif mnem in ONE_REG_OPS:
            reg=operands.upper()
            if reg not in REG_NAMES: raise ValueError(f'{mnem} needs one R0..R3')
            operand=REG_NAMES[reg] if mnem=='OUT' else REG_NAMES[reg]*4
        return (imm<<8)|(OPCODES[mnem]<<4)|operand,None
    except ValueError as e:
        raise ValueError(f'Line {line_no}: {e}') from None

def assemble(text):
    labels={}; instructions=[]
    for line_no,raw in enumerate(text.splitlines(),1):
        line=strip_comment(raw)
        match=LABEL.match(line)
        if match:
            name,line=match.groups()
            if name in labels: raise ValueError(f'Line {line_no}: duplicate label {name}')
            labels[name]=len(instructions)
        if line:
            instructions.append((line_no,line))
            if len(instructions)>16: raise ValueError('Program exceeds ROM capacity 16')
    return [assemble_line(line,labels,n)[0] for n,line in instructions]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('-o','--output',type=Path)
    parser.add_argument('--run',action='store_true',help='show encoding preview (not CPU execution)')
    args=parser.parse_args()
    try: words=assemble(args.source.read_text(encoding='utf-8'))
    except (ValueError,OSError) as e: parser.exit(1,f'[ERROR] {e}\n')
    text=''.join(f'{w:03X}\n' for w in words)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
        print(f'[OK] Created {args.output} ({len(words)} instructions)')
    else: print(text,end='')
    if args.run:
        for i,w in enumerate(words): print(f'[{i:02d}] {w:03X}')
if __name__=='__main__': main()
