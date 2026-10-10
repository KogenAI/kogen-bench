#!/usr/bin/env python3
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rows=[]
for filename,module in [('intent','lifeArtifacts'),('check','checkArtifacts')]:
 for operation in ['test','run']:
  cmd=['../../../quint-cli/quint.sh',operation,'quint/'+filename+'.qnt','--main',module,'--backend','typescript','--seed','20261009','--max-samples','1' if operation=='test' else '300']
  if operation=='run':cmd+=['--max-steps','20','--invariant','invariant','--verbosity','1']
  started=time.time();p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  label=module+'-'+operation
  (ROOT/'checks'/(label+'.log')).write_text('$ '+' '.join(cmd)+'\n'+p.stdout)
  rows.append({'file':'quint/'+filename+'.qnt','model':module,'check':operation,'command':cmd,'exit':p.returncode,'seconds':round(time.time()-started,2)})
  print(label,'PASS' if p.returncode==0 else 'FAIL',flush=True)
(ROOT/'checks/helper-results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(any(r['exit'] for r in rows))
