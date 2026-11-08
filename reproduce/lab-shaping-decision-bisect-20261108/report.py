#!/usr/bin/env python3
import collections,json,pathlib
print('Commit inventory and prior-stage ranking: history.md')
x=json.loads((pathlib.Path(__file__).parent/'data.json').read_text())
rows=x['cells']; pairs=collections.defaultdict(dict)
for r in rows: pairs[(r['task'],r['rep'])][r['arm']]=r
for arm in ('old','new','baseline'):
 a=[r for r in rows if r['arm']==arm]
 if a: print(arm,'ready',sum(r['ready'] for r in a),'/',len(a),'wall_s',round(sum(r['wall_s'] for r in a),2))
for a,b in (('old','new'),('baseline','old')):
 both=[v for v in pairs.values() if a in v and b in v]
 if both:
  print(a,'to',b, 'paired',len(both),'not-ready to ready',sum(not p[a]['ready'] and p[b]['ready'] for p in both),'ready to not-ready',sum(p[a]['ready'] and not p[b]['ready'] for p in both))
  for task,rep in sorted(pairs):
   p=pairs[(task,rep)]
   if a in p and b in p: print(task,rep,int(p[a]['ready']),int(p[b]['ready']))
