#!/usr/bin/env python3
"""Quint arm package CLI; stages follow bridge/fv-cli.md."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from check import check, environment


def main():
    root=Path.cwd()
    if sys.argv[1:]!=['check']:
        print('usage: ./fv check');return 2
    total=0;passed=0;tests=False;digest='none';status=2
    env=environment()
    env['PATH']='/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:'+env['PATH']
    env['ERL_FLAGS']='+S 1:1 +A 1'
    try:
        laws=json.loads((root/'laws.json').read_text());total=len(laws['laws'])
        hashes=root/'fixed.sha256'
        if not hashes.exists():raise RuntimeError('missing fixed.sha256')
        verified=set()
        for line in hashes.read_text().splitlines():
            expected,rel=line.split(maxsplit=1);rel=rel.lstrip('*')
            target=(root/rel).resolve()
            if not target.is_relative_to(root):raise RuntimeError('invalid fixed path')
            if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise RuntimeError('changed fixed law: '+rel)
            verified.add(rel)
        if not {'laws.json','verification/laws.qnt'}.issubset(verified):raise RuntimeError('fixed hashes must include laws.json and verification/laws.qnt')
        out=root/'verification';ir=out/'ir.json'
        r=subprocess.run(['nice','-n','10','elixir',str(root/'bridge/frontend/main.exs'),str(root/'app'),str(ir)],env=env)
        if r.returncode:raise RuntimeError('frontend rejected current source')
        r=subprocess.run(['nice','-n','10','python3',str(root/'bridge/quint/emit.py'),str(ir),str(root/'laws.json'),str(out)],env=env)
        if r.returncode:raise RuntimeError('emitter rejected current source')
        digest=hashlib.sha256(ir.read_bytes()+(out/'app.qnt').read_bytes()).hexdigest()
        status,passed,_=check(out,laws)
        sys.stdout.flush()
        r=subprocess.run(['nice','-n','10','mix','test'],cwd=root/'app',env=env)
        tests=r.returncode==0
        if status==0 and not tests:status=1
    except (RuntimeError,OSError,ValueError,KeyError) as ex:
        print('FV-ERROR '+str(ex));status=2
    print(f'FV-SUMMARY arm=quint laws_ok={passed}/{total} tests_ok={str(tests).lower()} regenerated={digest}')
    return status
if __name__=='__main__':sys.exit(main())
