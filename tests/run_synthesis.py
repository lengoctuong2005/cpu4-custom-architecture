#!/usr/bin/env python3
"""Native Yosys generic + optional external-library educational synthesis.
Never treat process success as artifact success; verify cell/FF counts and files.
"""
import json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'build/synthesis';out.mkdir(parents=True,exist_ok=True)
subprocess.run(['yosys','-l',str(out/'yosys.log'),'tools/synth.ys'],cwd=ROOT,check=True,timeout=180)
net=json.loads((out/'cpu_top.json').read_text());top=net['modules']['cpu_top']
# Hierarchical generic report preserves ROM + datapath; not physical cell area.
summary={'generic':'PASS','top_cells':len(top['cells']),'modules':list(net['modules'])}
if os.environ.get('LIBERTY'):
    lib=Path(os.environ['LIBERTY']).resolve()
    if not lib.is_file():raise FileNotFoundError(lib)
    script=(ROOT/'tools/synth_mapped.ys').read_text().replace('@LIBERTY@',str(lib))
    run=out/'mapped_run.ys';run.write_text(script)
    subprocess.run(['yosys','-l',str(out/'mapped_yosys.log'),str(run)],cwd=ROOT,check=True,timeout=180)
    mapped=json.loads((out/'cpu_top_mapped.json').read_text())['modules']['cpu_top']
    types={}
    for c in mapped['cells'].values():types[c['type']]=types.get(c['type'],0)+1
    if not any('DFF' in t for t in types):raise AssertionError('Mapped design lost all sequential state')
    summary.update(mapped='PASS',mapped_cells=len(mapped['cells']),mapped_cell_types=types)
(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
