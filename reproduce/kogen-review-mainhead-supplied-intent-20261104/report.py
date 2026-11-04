#!/usr/bin/env python3
"""Summarize the recorded per-cell results without rerunning models."""
import json
from pathlib import Path
rows=json.loads((Path(__file__).parent/'data'/'cells.json').read_text())
for r in rows:
 g=r['grade']
 grade=(str(g['passed'])+'/'+str(g['expected'])+' (errors '+str(g['errored'])+')') if g else 'ungraded'
 t=r['totals']
 print(r['task'],r['arm'],'approval='+str(r['approval']),'outcome='+r['outcome'],'hidden='+grade,'all-pass='+str(g['all_passed'] if g else None),'wall_s='+str(r['wall_s']),'input='+str(t['input_tokens']),'cached='+str(t['cached_input_tokens']),'output='+str(t['output_tokens']))
for arm in ('g0','g1'):
 a=[r for r in rows if r['arm']==arm]; print(arm, 'cells',len(a),'landed',sum(r['outcome']=='landed' for r in a),'all-pass',sum(bool(r['grade'] and r['grade']['all_passed']) for r in a),'input',sum(r['totals']['input_tokens'] for r in a),'output',sum(r['totals']['output_tokens'] for r in a),'wall_s',round(sum(r['wall_s'] for r in a),3))
