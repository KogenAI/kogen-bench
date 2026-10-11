#!/usr/bin/env python3
"""Supervisor post-DONE dry-cell verification; never starts arms or repeats scoring."""
import json,os,subprocess,sys
from pathlib import Path
if len(sys.argv)!=2:raise SystemExit('usage: test-gates.sh DONE_DRY_CELL_ROOT')
root=Path(sys.argv[1]).resolve()
if root.name=='out':root=root.parent
assert (root/'DONE').is_file() and (root/'CAP_MIN').read_text().strip()=='10','completed 10-minute supervisor dry cell required'
assert (root/'snapshots/FINAL/SNAPSHOT_COMPLETE').is_file()
assert (root/'snapshots/T+005m/SNAPSHOT_COMPLETE').is_file()
assert not (root/'locks.tsv').read_text().strip(),'unrestored locks'
arms=(root/'ARMS').read_text().split();assert set(arms)<=set('abcd')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',RACE3_KIT_DIR=str(root.parent/'race3-kit'),RACE6_KIT_DIR=str(root.parent/'race6-kit'))
for script in ('checks.py','audit.py'):
    subprocess.run(['python3',str(root/script)],cwd=root,env=env,check=True)
for arm in arms:
    receipt=json.loads((root/f'out/results/FINAL-{arm}-score.json').read_text())
    assert receipt['N_scored']==106
    assert receipt['double_scored']==(103<=receipt['first_scored']<=109)
    for tag in ('official','repeat') if receipt['double_scored'] else ('official',):
        subprocess.run(['python3',str(root/'validate-results.py'),str(root/f'out/results/FINAL-{arm}-{tag}.jsonl')],cwd=root,env=env,check=True)
    assert not (root/arm/'conformance').exists()
print('PASS post-DONE dry cell: model/effort, audit, inputs/kits/specs/briefs, snapshots, restored locks, complete scoring and repeat band')
