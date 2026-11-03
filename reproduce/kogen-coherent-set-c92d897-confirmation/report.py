"""Model-free replay of recorded outcomes; no model or benchmark execution."""
import json
from pathlib import Path

def readings(rows):
 out={}
 for exclude in (False,True):
  by={}
  for metric in ('valid','landed','hidden'):
   pairs=[]
   for r in rows:
    s=r.get('stored')
    if not s: continue
    n=s['graded'] if metric=='hidden' else s['n']-(s['timeouts'] if exclude else 0)
    new=r['hidden_all_pass'] if metric=='hidden' else r[metric]
    if not n or new is None:continue
    pairs.append({'task':r['task'],'delta':float(new)-s[metric]/n,'stored_denominator':n})
   mean=sum(x['delta'] for x in pairs)/len(pairs) if pairs else None
   by[metric]={'mean_delta':mean,'per_task':pairs,'worse':bool(pairs) and (mean<=-.15 or any(x['delta']<=-.34 for x in pairs))}
  out['exclude_approval_timeouts' if exclude else 'include_approval_timeouts']=by
 return out

def main():
 d=json.loads(Path(__file__).with_name('data.json').read_text())
 for name in ('original','confirmation'):
  rows=d[name]
  print(name,'attempts',len(rows),'valid',sum(x['valid'] for x in rows),'landed',sum(x['landed'] for x in rows),'hidden_all_pass',sum(x['hidden_all_pass'] is True for x in rows))
  for x in rows: print(x['task'],x['outcome'],'Intent',int(x['valid']),'hidden',x['hidden_all_pass'],'acceptance',x['acceptance_separation'])
  print(name,'readings',json.dumps(readings(rows),sort_keys=True))
 print('combined_by_task_readings',json.dumps(readings(d['combined_by_task']),sort_keys=True))
 print('combined_timeout_sensitivity_agrees',d['metadata']['combined_timeout_sensitivity_agrees'])
 print('verdict',d['metadata']['verdict'])
 print('tokens',json.dumps(d['metadata']['tokens'],sort_keys=True))
 print('cell_wall_s',d['metadata']['cell_wall_s'])
 print('disposition',d['metadata']['disposition'])
 print('qualified',d['metadata']['qualified'])
if __name__=='__main__': main()
