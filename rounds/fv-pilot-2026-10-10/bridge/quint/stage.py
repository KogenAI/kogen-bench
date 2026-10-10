#!/usr/bin/env python3
"""Harness adapter for immutable backend plans: regenerate/check/starter."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

scriptdir=Path(__file__).resolve().parent
root=scriptdir.parent
embedded=(scriptdir/'bridge/quint').is_dir()
backend=scriptdir if embedded else root/'verification'
bridge=scriptdir/'bridge' if embedded else root/'bridge'
hashfile=scriptdir/'fixed.sha256' if embedded else root/'fixed.sha256'
lawpath='backend/laws.qnt' if embedded else 'verification/laws.qnt'
sys.path.insert(0,str(bridge/'quint'))
from check import check, environment
statefile=backend/'.fv-stage.json'

def save(s):statefile.write_text(json.dumps(s)+'\n')
def env():
    e=environment();e['PATH']='/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:'+e['PATH'];e['ERL_FLAGS']='+S 1:1 +A 1';return e

def fixed():
    verified=set()
    for line in hashfile.read_text().splitlines():
        expected,relative=line.split(maxsplit=1);target=(root/relative.lstrip('*')).resolve()
        if not target.is_relative_to(root) or hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise RuntimeError('changed fixed laws: '+relative)
        verified.add(relative.lstrip('*'))
    if not {'laws.json',lawpath}.issubset(verified):raise RuntimeError('incomplete fixed law hashes')

def main():
    action=sys.argv[1] if len(sys.argv)==2 else ''
    if action not in {'regenerate','check','starter'}:print('invalid backend stage');return 2
    s={'regenerated':'none','laws_ok':0,'laws_total':0,'translated':False,'status':2}
    if action!='regenerate' and statefile.exists():s=json.loads(statefile.read_text())
    try:
        fixed();laws=json.loads((root/'laws.json').read_text());s['laws_total']=len(laws['laws'])
        if action=='regenerate':
            r=subprocess.run(['nice','-n','10','elixir',str(bridge/'frontend/main.exs'),str(root/'app'),str(backend/'ir.json')],env=env())
            if r.returncode:raise RuntimeError('frontend rejected source')
            r=subprocess.run(['nice','-n','10','python3',str(bridge/'quint/emit.py'),str(backend/'ir.json'),str(root/'laws.json'),str(backend)],env=env())
            if r.returncode:raise RuntimeError('emitter rejected source')
            s.update(translated=True,status=0,regenerated=hashlib.sha256((backend/'ir.json').read_bytes()+(backend/'app.qnt').read_bytes()).hexdigest());save(s);return 0
        if action=='check':
            if not s['translated']:raise RuntimeError('regeneration incomplete')
            status,passed,_=check(backend,laws);s.update(status=status,laws_ok=passed);save(s);return status
        tests=False
        if s['translated']:
            r=subprocess.run(['nice','-n','10','mix','test'],cwd=root/'app',env=env());tests=r.returncode==0
        status=s['status'] if s['status'] else (0 if tests else 1)
        print(f'FV-SUMMARY arm=quint laws_ok={s["laws_ok"]}/{s["laws_total"]} tests_ok={str(tests).lower()} regenerated={s["regenerated"]}')
        return status
    except (OSError,ValueError,RuntimeError,KeyError) as ex:
        print('FV-ERROR '+str(ex));s['status']=2;save(s)
        if action=='starter':print(f'FV-SUMMARY arm=quint laws_ok=0/{s["laws_total"]} tests_ok=false regenerated={s["regenerated"]}')
        return 2
if __name__=='__main__':sys.exit(main())
