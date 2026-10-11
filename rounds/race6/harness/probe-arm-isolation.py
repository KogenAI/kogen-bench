#!/usr/bin/env python3
"""Launch-only macOS gate, with the exact inherited arm deny profile."""
import importlib.util,json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('isolation',r/'arm-isolation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
arms=(r/'ARMS').read_text().split()
for arm in arms:
    p=r/'out'/arm/'arm-isolation.sb';p.parent.mkdir(exist_ok=True);p.write_text(m.profile(r,arm))
    targets=[str(r/a) for a in arms if a!=arm]
    script="""import json,sys,os
for p in json.loads(sys.argv[1]):
 for read in (lambda:os.listdir(p),lambda:open(p+'/AGENTS.md').read()):
  try:read()
  except PermissionError:continue
  raise SystemExit('EXPOSED other arm: '+p)
print('PASS other-arm list/read denied')
"""
    subprocess.run(['/usr/bin/sandbox-exec','-f',str(p),'/usr/bin/python3','-c',script,json.dumps(targets)],check=True)
print('PASS inherited isolation profiles for '+str(len(arms))+' arms')
