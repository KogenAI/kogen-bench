#!/usr/bin/env python3
import json
from pathlib import Path
d=json.loads((Path(__file__).resolve().parent/'data/results.json').read_text())['cells']
tasks=sorted({c['task'] for c in d})
print('task rep g0(hidden passed/total, outcome) g1(...)')
tot={'g0':0,'g1':0}
for t in tasks:
    for rep in ('r1','r2'):
        row=[]
        for a in ('g0','g1'):
            c=[x for x in d if (x['task'],x['rep'],x['arm'])==(t,rep,a)][0]
            tot[a]+=c['hidden_passed']; row.append('%d/%d %s'%(c['hidden_passed'],c['hidden_total'],c['outcome']))
        print(t,rep,*row)
print('hidden checks passed, all cells:',tot)
for a in ('g0','g1'):
    print(a,'landed',sum(c['outcome']=='landed' for c in d if c['arm']==a),'all-pass',sum(c['all_pass'] for c in d if c['arm']==a),'wall s',round(sum(c['wall_s'] for c in d if c['arm']==a),1))
