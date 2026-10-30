# Provenance copy of the fault test as run on 30 October 2026. Paths are parameters: set the environment variables named below to a scratch
# directory, your lanes release and your task-kit directory. It needs pinned Kogen artifacts; it is not runnable standalone.
# usage: python3 npm-stall-preflight.py old|new     (old = unpatched harness, new = patched harness)
from pathlib import Path
import hashlib,json,os,shlex,shutil,subprocess,sys,time
ROOT=Path(os.environ['FAULT_ROOT'])           # scratch dir holding repo/ (patched lanes) and proof/
P=Path(os.environ['LANES_PRIVATE'])            # holds runs/ (with the pinned-Kogen run dirs) and lc-tasks/ (task kits)
OLD_HARNESS=Path(os.environ['OLD_LANES_RELEASE'])  # the unpatched lanes release (mode old)
mode=sys.argv[1]
sys.path.insert(0,str(OLD_HARNESS if mode=='old' else ROOT/'repo/lanes'))
from lanes import cell,experiment,preflight
proof=ROOT/'proof'
shim=proof/('npm-fault-'+mode);shim.mkdir(exist_ok=True)
calls=proof/(mode+'-npm.calls')
(shim/'npm').write_text('#!/bin/sh\necho "npm $*" >> '+shlex.quote(str(calls))+'\necho \"$$ $(ps -o pgid= -p $$)\" >> '+shlex.quote(str(proof/(mode+'-npm-processes.txt')))+'\nexec /bin/sleep 600\n')
(shim/'npm').chmod(0o755)
os.environ['PATH']=str(shim)+os.pathsep+os.environ['PATH']
checks=[('goose-labels-go','q-brief-st-dry','capped')] if mode=='goose' else [('task-tags-go','q-prefix-st.aside-preflight-refused-20261030T0518Z','a0'),('bytefmt-go','q-nudge-st-dry','reminder')]

def snapshot(root):
    entries=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():e=[rel,'symlink',os.readlink(p)]
        elif p.is_file():e=[rel,'file',p.stat().st_mode&0o777,hashlib.sha256(p.read_bytes()).hexdigest()]
        else:e=[rel,'directory']
        entries.append(e)
    return entries

original=cell.Cell.invoke
current={}
def observed(self,*args,**kwargs):
    result=original(self,*args,**kwargs)
    ws=Path(self.ws)
    if (ws/'node_modules').is_dir():
        files=snapshot(ws/'node_modules')
        (proof/(mode+'-'+current['task']+'-cell-files.json')).write_text(json.dumps(files,indent=2)+'\n')
        current['cell_lock_sha256']=hashlib.sha256((ws/'package-lock.json').read_bytes()).hexdigest()
        current['entries']=len(files)
    return result
cell.Cell.invoke=observed
results=[]
for task,run,name in checks:
    current.clear();current['task']=task
    rd=P/'runs'/run
    exp=experiment.load(rd/'experiment.json')
    lane=next(l for l in exp['lanes'] if l['name']==name)
    config=cell.tomllib.load(open(P/'lc-tasks'/task/'task.toml','rb'))
    artifact=cell.resolve_kogen(str(rd),name,None)
    t=time.monotonic()
    ok,message=preflight.check_one(exp,str(rd),str(P/'lc-tasks'),task,lane)
    row=dict(current,mode=mode,ok=ok,elapsed_s=round(time.monotonic()-t,3),message=message,deadline_s=cell.approve_timeout(config,preflight.DEADLINE_S),kogen=artifact,kogen_sha256=hashlib.sha256(Path(artifact).read_bytes()).hexdigest(),npm_calls=calls.read_text().splitlines() if calls.exists() else [])
    results.append(row)
    print(json.dumps(row),flush=True)
    (proof/(mode+'.json')).write_text(json.dumps(results,indent=2)+'\n')
if mode=='old':assert all(not r['ok'] and r['npm_calls'] for r in results),results
elif mode=='new':assert all(r['ok'] and not r['npm_calls'] and r.get('entries') for r in results),results
