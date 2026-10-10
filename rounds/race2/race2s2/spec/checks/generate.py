#!/usr/bin/env python3
"""Retain representative model traces without executing their effects."""
import concurrent.futures,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
seeds={'approve':7000000,'build':8000000,'check':9000000,'cli':1000000,'config':6104101,'git':2000000,'init':12000000,'intent':5000000,'kogen':20261009,'landing':10000000,'process':3000000,'provider_login':20261009,'queue':11000000,'recovery':14010004,'shape':6000000,'status':13010000,'version':20261009}
def generate(item):
 module,seed=item;out=Path('quint/traces')/(module+'-{seq}.itf.json')
 cmd=['../../../quint-cli/quint.sh','run','quint/'+module+'.qnt','--main',module,'--backend','typescript','--seed',str(seed),'--invariant','invariant','--max-samples','1','--max-steps','20','--out-itf',str(out),'--n-traces','1','--verbosity','1']
 if module=='status':cmd+=['--init','initRich']
 if module=='recovery':cmd+=['--init','initFreshGreen']
 p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (ROOT/'checks'/(module+'-generation.log')).write_text('$ '+' '.join(cmd)+'\n'+p.stdout)
 record={'module':module,'seed':str(seed),'max_steps':20,'command':cmd,'exit':p.returncode,'replayed':False}
 trace=ROOT/'quint/traces'/(module+'-0.itf.json')
 if p.returncode==0:
  data=json.loads(trace.read_text());steps=[step for state in data['states'] for step in state.get('lastStep',[])]
  record.update(states=len(data['states']),actions=len(steps),executable_witness=bool(steps),itf=str(trace.relative_to(ROOT)),itf_sha256=hashlib.sha256(trace.read_bytes()).hexdigest())
 print(module,'PASS' if p.returncode==0 else 'FAIL',flush=True);return record
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(generate,seeds.items()))
 (ROOT/'quint/traces/generation.json').write_text(json.dumps(records,indent=2)+'\n')
 raise SystemExit(any(r['exit'] for r in records))
