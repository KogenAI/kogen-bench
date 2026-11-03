#!/usr/bin/env python3
"""Recompute the recorded golden-output changes from public commits; no source is saved."""
from pathlib import Path
import argparse,json,urllib.request
p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');a=p.parse_args()
b=Path(__file__).resolve().parent;r=json.loads((b/'model-free.json').read_text())
if a.offline:
 changes=r['golden_changes']
else:
 def get(sha):
  u='https://raw.githubusercontent.com/KogenAI/kogen-coordinator/'+sha+'/project/testdata/golden.json'
  with urllib.request.urlopen(u,timeout=30) as f:return json.load(f)
 old,new=get(r['base']),get(r['head']);changes=[]
 for section in old:
  if old[section]==new[section]:continue
  if not isinstance(old[section],list):raise SystemExit('Unexpected non-list golden change')
  if len(old[section])!=len(new[section]):raise SystemExit('Golden case count changed')
  for i,(x,y) in enumerate(zip(old[section],new[section])):
   if x!=y:changes.append(dict(section=section,index=i,label=x.get('label'),before=x.get('result'),after=y.get('result')))
 if changes!=r['golden_changes']:raise SystemExit('REFUSED: public source differs from recorded comparison')
print(json.dumps(dict(changed_golden_outputs=len(changes),changes=changes),indent=2))
