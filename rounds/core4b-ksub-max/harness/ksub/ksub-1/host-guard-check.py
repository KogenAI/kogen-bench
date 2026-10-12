#!/usr/bin/env python3
"""Run planted custody positives inside the official grade profile."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
ROOT = Path('<ROOT>')
spec = importlib.util.spec_from_file_location('validation', ROOT/'<SERVER_ID>.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
task = ROOT/'taskdir-go'
shutil.copytree(ROOT/'hidden', task/'hidden', dirs_exist_ok=True)
units = subprocess.run(['systemctl','list-units','--state=running','bench-c4*','--no-legend','--plain','--no-pager'],capture_output=True,text=True,check=True)
print(json.dumps({'running_bench_units':len(units.stdout.splitlines()),'cpu_burners':0,'loaded_runs':'deferred by ORDERS.md'}))
results=[]
for case in ('custody','timeout','app-leak'):
 p=subprocess.run([v.PROFILE,'grade',str(ROOT/'format-go-fix1'),str(task),'--','python3','/task/hidden/runner.py','/work','--'+case+'-selftest'],env=v.ENV,capture_output=True,text=True,timeout=30)
 (ROOT/'validation-logs'/('guard-fix1-'+case+'.log')).write_text(p.stdout+'\n'+p.stderr)
 rows=[]
 for line in (p.stdout+'\n'+p.stderr).splitlines():
  try: rows.append(json.loads(line))
  except ValueError: pass
 final=json.loads(p.stdout.splitlines()[-1])
 item={'case':case,'sandbox_rc':p.returncode,'summary':final,'before_leftovers':max((r.get('before_leftovers',0) for r in rows),default=0),'before_zombies':max((r.get('before_zombies',0) for r in rows),default=0)}
 results.append(item); print(json.dumps(item),flush=True)
 if p.returncode or not final['pass_']: raise RuntimeError('planted guard selftest failed')
(ROOT/'GUARD-FIX1-COUNTS.json').write_text(json.dumps(results,indent=2)+'\n')
