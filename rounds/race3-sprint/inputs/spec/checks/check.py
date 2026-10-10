#!/usr/bin/env python3
"""Offline pinned Quint checks, invoked from spec/. Logs include exact commands."""
import concurrent.futures,json,re,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WRAPPER='../../../quint-cli/quint.sh'
OUT=ROOT/'checks';OUT.mkdir(exist_ok=True)
def check_file(path):
 name=path.stem;source=path.read_text();records=[]
 commands=[('typecheck',[WRAPPER,'typecheck',str(path.relative_to(ROOT))]),('test',[WRAPPER,'test',str(path.relative_to(ROOT)),'--main',name,'--backend','typescript','--seed','20261009','--max-samples','1'])]
 # Pure IO library has no init/step; every runnable model is explored.
 if re.search(r'^  action init\s*=',source,re.M):
  invs=list(dict.fromkeys(re.findall(r'^  val ((?:invariant|\w*Invariant))\s*=',source,re.M)))
  for inv in invs:
   commands.append(('run-'+inv,[WRAPPER,'run',str(path.relative_to(ROOT)),'--main',name,'--backend','typescript','--seed','20261009','--invariant',inv,'--max-samples','300','--max-steps','20','--verbosity','1'] + (['--out-itf', str(Path('quint/traces')/(name+'-{seq}.itf.json')), '--n-traces','1'] if inv == 'invariant' else [])))
 # Secondary fixture-export models have their own init/step/invariant.
 for match in re.finditer(r'^module (\w+) \{(.*?)(?=^module |\Z)',source,re.M|re.S):
  secondary,body=match.groups()
  if secondary == name or not re.search(r'^  action init\s*=',body,re.M):continue
  commands.append((secondary+'-test',[WRAPPER,'test',str(path.relative_to(ROOT)),'--main',secondary,'--backend','typescript','--seed','20261009','--max-samples','1']))
  for inv in dict.fromkeys(re.findall(r'^  val ((?:invariant|\w*Invariant))\s*=',body,re.M)):
   commands.append((secondary+'-run-'+inv,[WRAPPER,'run',str(path.relative_to(ROOT)),'--main',secondary,'--backend','typescript','--seed','20261009','--invariant',inv,'--max-samples','300','--max-steps','20','--verbosity','1']))
 for label,cmd in commands:
  start=time.time();proc=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (OUT/(name+'-'+label+'.log')).write_text('$ '+' '.join(cmd)+'\n'+proc.stdout)
  rec=dict(file=str(path.relative_to(ROOT)),check=label,command=cmd,exit=proc.returncode,seconds=round(time.time()-start,2));records.append(rec)
  print(name,label,'PASS' if proc.returncode==0 else 'FAIL',flush=True)
  if proc.returncode: print(proc.stdout[-2500:],flush=True);break
 (OUT/(name+'-results.json')).write_text(json.dumps(records,indent=2)+'\n')
 return records
if __name__=='__main__':
 import sys
 targets = [ROOT/'quint'/(n+'.qnt') for n in sys.argv[1:]] if sys.argv[1:] else sorted((ROOT/'quint').glob('*.qnt'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  results=sum(pool.map(check_file,targets),[])
 results=sum((json.loads((OUT/(p.stem+'-results.json')).read_text()) for p in sorted((ROOT/'quint').glob('*.qnt')) if (OUT/(p.stem+'-results.json')).exists()),[])
 if (OUT/'helper-results.json').exists():
  for helper in json.loads((OUT/'helper-results.json').read_text()):
   label=helper['model']+'-'+('test' if helper['check']=='test' else 'run-invariant')
   if not any(r['file']==helper['file'] and r['check']==label for r in results):results.append(helper)
 (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 raise SystemExit(any(r['exit'] for r in results))
