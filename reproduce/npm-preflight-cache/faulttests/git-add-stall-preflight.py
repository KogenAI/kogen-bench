# Provenance copy of the fault test as run on 30 October 2026. Paths are parameters: set the environment variables named below to a scratch
# directory, your lanes release and your task-kit directory. It needs pinned Kogen artifacts; it is not runnable standalone.
from pathlib import Path
import json,os,shlex,sys,time,hashlib
ROOT=Path(os.environ['FAULT_ROOT'])
P=Path(os.environ['LANES_PRIVATE']);proof=ROOT/'proof'
sys.path.insert(0,str(ROOT/'repo/lanes'))
from lanes import cell,experiment,preflight
shim=proof/'git-fault';shim.mkdir(exist_ok=True)
shim.joinpath('git').write_text('''#!/usr/bin/env python3
import os,sys
if sys.argv[1:] == ['add','-A','--','.'] and os.environ.get('GIT_INDEX_FILE'):
    with open(os.environ['FAULT_ROOT']+'/proof/git-processes.txt','a') as f:
        f.write(str(os.getpid())+' '+str(os.getpgrp())+' '+os.getcwd()+'\\n')
    os.execv('/bin/sleep',['sleep','600'])
os.execv('/usr/bin/git',['git',*sys.argv[1:]])
''')
shim.joinpath('git').chmod(0o755)
os.environ['PATH']=str(shim)+os.pathsep+os.environ['PATH']
rd=P/'runs/q-brief-st-dry';exp=experiment.load(rd/'experiment.json');lane=next(l for l in exp['lanes'] if l['name']=='capped')
kogen=cell.resolve_kogen(str(rd),'capped',None)
t=time.monotonic();ok,message=preflight.check_one(exp,str(rd),str(P/'lc-tasks'),'goose-labels-go',lane)
r=dict(task='goose-labels-go',ok=ok,message=message,elapsed_s=round(time.monotonic()-t,3),deadline_s=preflight.DEADLINE_S,kogen=kogen,kogen_sha256=hashlib.sha256(Path(kogen).read_bytes()).hexdigest(),fault='sleep 600 only for git add -A -- . with a temporary GIT_INDEX_FILE; no index mutation')
(proof/'git-fault.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
assert not ok and 'timed out' in message and 'status 143' in message,r
