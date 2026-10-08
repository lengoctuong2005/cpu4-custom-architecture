#!/usr/bin/env python3
"""Educational netlist-only drive-strength ECO, not a physical/timing closure flow.
Run STA first. Each requested instance must occur exactly once; library must
contain both old/new cells and same base family (e.g. NOR4_X1 -> NOR4_X4).
Re-run STA/gate model afterwards. No tracked RTL/netlist is overwritten.
"""
import argparse,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
p.add_argument('--liberty',type=Path,required=True);p.add_argument('--resize',action='append',required=True)
a=p.parse_args();text=a.input.read_text();lib=a.liberty.read_text()
if a.input.resolve()==a.output.resolve():p.error('Use a distinct output; preserve baseline')
for item in a.resize:
    instance,new=item.split('=',1)
    pat=re.compile(r'\b([A-Za-z0-9_]+)\s+'+re.escape(instance)+r'\s*\(')
    matches=list(pat.finditer(text))
    if len(matches)!=1:p.error(f'Expected unique instance {instance}')
    old=matches[0].group(1)
    if old.rsplit('_X',1)[0]!=new.rsplit('_X',1)[0]:p.error('Only same-family strength swaps permitted')
    for cell in (old,new):
        if not re.search(r'cell\s*\(\s*'+re.escape(cell)+r'\s*\)',lib):p.error(f'Missing library cell {cell}')
    text=pat.sub(lambda m:f'{new} {instance} (',text,count=1)
    print(f'{instance}: {old} -> {new}')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
