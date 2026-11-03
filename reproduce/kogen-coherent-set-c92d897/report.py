#!/usr/bin/env python3
"""Recompute the descriptive outcomes and registered sensitivity checks from data.json."""
from pathlib import Path
import sys,json
d=json.loads(Path(sys.argv[1]).read_text());m=d['metadata'];rows=d['rows'];phase=d['phase_scores']
print('E2E assigned/observed:',m['assigned_e2e'],len(rows))
print('Valid Intents / landed / hidden all-pass:',sum(r['valid_intent'] for r in rows),sum(r['landed'] for r in rows),sum(r['hidden_all_pass'] is True for r in rows))
for r in sorted(rows,key=lambda x:x['task']):print(r['task'],r['outcome'],'valid='+str(int(r['valid_intent'])),'hidden='+str(int(r['hidden_all_pass'] is True)))
print('Shape-only Intents:',sum(r['intent_valid'] for r in phase),'/',len(phase))
print('Shape-only coverage:',','.join(str(r['coverage']) for r in phase))
for key in ['include_approval_timeouts','exclude_approval_timeouts']:
 calc={}
 for metric in ['valid','landed','hidden']:
  deltas=[]
  for r in rows:
   s=r['stored']
   if not s:continue
   n=s['graded'] if metric=='hidden' else s['n']-(s['timeouts'] if key.startswith('exclude') else 0)
   new=r[{'valid':'valid_intent','landed':'landed','hidden':'hidden_all_pass'}[metric]]
   if n:deltas.append(float(new)-s[metric]/n)
  mean=sum(deltas)/len(deltas);worse=mean<=-.15 or any(v<=-.34 for v in deltas)
  assert abs(mean-m['metric_readings'][key][metric]['mean_delta'])<1e-12
  assert worse==m['metric_readings'][key][metric]['worse']
  calc[metric]=dict(mean_delta=round(mean,6),worse=worse)
 print(key,json.dumps(calc,sort_keys=True))
tokens={k:sum(r['tokens'].get(k,0) or 0 for r in [*rows,*phase]) for k in ['input_tokens','cached_input_tokens','output_tokens','reasoning_tokens','requests']}
assert tokens==m['tokens'];print('Tokens:',json.dumps(tokens,sort_keys=True))
print('Cell wall seconds including failures:',f"{sum(r['wall_s'] for r in [*rows,*phase]):.3f}")
print('Verdict:',m['verdict'],'qualified='+str(m['qualified']))
