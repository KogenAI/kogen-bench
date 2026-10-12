#!/usr/bin/env python3
"""Probe compiled public skeletons in the official grade profile."""
import importlib.util
import json
from pathlib import Path
import subprocess
ROOT=Path('<ROOT>')
spec=importlib.util.spec_from_file_location('validation',ROOT/'<SERVER_ID>.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[]
for lang in ('rust','go','ts-bun'):
 for argv in ([],['unknown-command'],['status','--unknown','value']):
  p=subprocess.run([v.PROFILE,'grade',str(ROOT/f'work-base-{lang}-100'),str(ROOT/f'taskdir-{lang}'),'--','/work/bin/app',*argv],env=v.ENV,capture_output=True,text=True,timeout=10)
  obj=json.loads(p.stderr)
  valid=p.returncode==70 and p.stdout=='' and p.stderr.endswith('\n') and p.stderr.count('\n')==1 and set(obj)=={'error'} and set(obj['error'])=={'code','message'} and obj['error']['code']=='NOT_IMPLEMENTED' and isinstance(obj['error']['message'],str) and bool(obj['error']['message'])
  rows.append({'lang':lang,'case':argv[0] if argv else 'no-command','rc':p.returncode,'valid':bool(valid)})
  if not valid:raise RuntimeError('base smoke failure')
(ROOT/'BASE-SMOKE-FIX1.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'base_argv_cases':len(rows),'valid':sum(r['valid'] for r in rows),'expected_rc':70}))
