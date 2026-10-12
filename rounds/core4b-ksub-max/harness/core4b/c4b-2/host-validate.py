#!/usr/bin/env python3
"""Private <SERVER_ID>; execute only via the authorized eu wrappers."""
import json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path('<ROOT>')
PROFILE='/benchmark-root/kits/current/reproduce/sandbox-profile.sh'
ENV={**os.environ,'HOME':'/tmp/bench-home','PYTHONDONTWRITEBYTECODE':'1',
'PATH':'/benchmark-root/toolchains/go-1.27.1/bin:/benchmark-root/toolchains/rust-1.97.1/bin:/benchmark-root/toolchains/bun-1.4.2/bin:/benchmark-root/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/elixir/1.20.2-otp-29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/opt/bench/mise/installs/node/24.20.0/bin:/opt/bench/mise/installs/ruby/3.4.8/bin:/benchmark-root/toolchains/python-3.14.7/bin:/usr/bin:/bin',
'PYTHONPATH':'/benchmark-root/toolchains/python-3.14.7/lib/python3.14/site-packages','RUSTUP_HOME':'/opt/bench/rustup','CARGO_NET_OFFLINE':'true','GOTOOLCHAIN':'local','GOPROXY':'off'}
def run(lang,variant,command,label):
 task=ROOT/('taskdir-'+lang);task.mkdir(exist_ok=True)
 proc=subprocess.run([PROFILE,'grade',str(ROOT/variant/lang),str(task),'--','/bin/bash','-c',command],env=ENV,capture_output=True,text=True,timeout=600)
 (ROOT/(variant+'-'+lang+'-'+label+'.log')).write_text(proc.stdout+'\n'+proc.stderr)
 return proc
if __name__=='__main__':
 mode=sys.argv[1]
 for lang in ['rust','go','ts-bun']:
  if mode=='format':
   command={'rust':'cargo fmt','go':'gofmt -w .','ts-bun':'./setup.sh && bun ./node_modules/@biomejs/biome/bin/biome check --write .'}[lang]
   for variant in ['bases','reference']:
    p=run(lang,variant,command,'format');print(json.dumps({'lang':lang,'variant':variant,'format_rc':p.returncode}),flush=True)
  elif mode=='harness':
   p=run(lang,'reference','python3 /task/hidden/suite/harness_check.py /work/bin/app','harness');print(json.dumps({'lang':lang,'rc':p.returncode,'counts':json.loads(p.stdout.splitlines()[-1]) if p.stdout else {}}),flush=True)
  elif mode=='validate':
   for variant,count in [('bases',1),('reference',3)]:
    p=run(lang,variant,'make check','check');print(json.dumps({'lang':lang,'variant':variant,'check_rc':p.returncode}),flush=True)
    for i in range(count):
     start=time.monotonic();p=run(lang,variant,'/bin/bash /task/grader-entrypoint /work','grade-'+str(i));lines=p.stdout.splitlines();record=json.loads(lines[-1]) if lines else {};print(json.dumps({'lang':lang,'variant':variant,'run':i,'rc':p.returncode,'seconds':round(time.monotonic()-start,3),'grade':record,'suite_seconds':json.loads(lines[-2]).get('suite_seconds') if len(lines)>1 and lines[-2].startswith('{') else None}),flush=True)
