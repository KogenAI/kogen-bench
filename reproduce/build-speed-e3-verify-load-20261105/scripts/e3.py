#!/usr/bin/env python3
"""E3 runner (EU, lanes). usage: e3.py <items.json> <e2-sched.json> <outdir> <reps> [shaping_reps]
Phase A solo / phase B under looped E2 arm-B load, per rep. No model, no network beyond Go module fetch into the private GOMODCACHE."""
import json,os,subprocess,sys,time,signal
items=json.load(open(sys.argv[1])); sched=sys.argv[2]; out=sys.argv[3]; reps=int(sys.argv[4]); sreps=int(sys.argv[5]) if len(sys.argv)>5 else reps
W=os.environ['W']; os.makedirs(out,exist_ok=True)
env=dict(os.environ,GOCACHE=f"{W}/gocache",GOMODCACHE=f"{W}/gomod",TMPDIR=f"{W}/tmp",GOTOOLCHAIN='local',
         PATH=os.path.expanduser("~/.local/share/mise/installs/node/24.21.0/bin:")+os.path.expanduser("~/.local/share/mise/installs/go/1.27.2/bin:")+"/usr/local/bin:/usr/bin:/bin")
def sh(c,cwd=None,e=env,t=None): return subprocess.run(c,shell=True,cwd=cwd,env=e,capture_output=True,text=True,timeout=t)
os.makedirs(f"{W}/wt",exist_ok=True)
trees={}
for it in items:
    r=it['repo']; base=f"{W}/trees/{r}"
    sha=sh(f"git rev-list -1 --before='{it['at']}' HEAD",cwd=base).stdout.strip()
    d=f"{W}/wt/{r}-{sha[:8]}"
    if not os.path.isdir(d): sh(f"git worktree add --detach {d} {sha}",cwd=base)
    for t in ('cucumber','quint'):
        src=f"{base}/testdata/tools/{t}/node_modules"; dst=f"{d}/testdata/tools/{t}/node_modules"
        if os.path.isdir(src) and os.path.isdir(os.path.dirname(dst)) and not os.path.isdir(dst): sh(f"cp -a {src} {dst}")
    it['sha']=sha[:8]; it['tree']=d
checks={}
for it in items: checks.setdefault((it['tree'],it['check']),[]).append(it['id'])
keys=sorted(checks,key=lambda k:('./...' in k[1] and 'shaping' in k[0], k))
log=open(f"{out}/runs.jsonl",'a')
def run(k,arm,rep):
    t=time.time(); p=sh(k[1],cwd=k[0],t=1500) if True else None
    d=time.time()-t
    rec=dict(tree=k[0].rsplit('/',1)[-1],check=k[1],arm=arm,rep=rep,rc=p.returncode,secs=round(d,1),load1=open('/proc/loadavg').read().split()[0],
             timeout='test timed out' in p.stdout+p.stderr,tail=(p.stdout+p.stderr)[-300:],items=checks[k])
    log.write(json.dumps(rec)+'\n'); log.flush(); return rec
def quiet():
    ps=sh("ps -eo user:12,args | grep -E 'kogen intent|kbuild\\.sh|heavy\\.sh' | grep -v -E 'grep|heavy-lab' | head -3").stdout.strip()
    return ps==''
for rep in range(1,reps+1):
    sel=[k for k in keys if rep<=(sreps if 'shaping' in k[0] else reps)]
    g=sh(f"sh {W}/bin/gate.sh quiet 1200").stdout.strip(); open(f"{out}/gate.log",'a').write(f"{time.time():.0f} rep{rep}A {g}\n")
    for k in sel: run(k,'A',rep)
    ld=f"{out}/load-{rep}"; os.makedirs(ld,exist_ok=True)
    lp=subprocess.Popen(['python3',f"{W}/bin/e2.py",'B',sched,ld],env=dict(env,LOOP='1',W=W),stdout=open(f"{ld}/stdout",'w'),stderr=subprocess.STDOUT,start_new_session=True)
    open(f"{out}/loadpgid.txt",'a').write(f"{lp.pid}\n")
    g=sh(f"sh {W}/bin/gate.sh quiet 1200").stdout.strip(); open(f"{out}/gate.log",'a').write(f"{time.time():.0f} rep{rep}B {g}\n")
    time.sleep(40)
    for k in sel: run(k,'B',rep)
    open(f"{ld}/STOP",'w').close()
    try: lp.wait(timeout=600)
    except subprocess.TimeoutExpired:
        for l in open(f"{ld}/pids.txt"):
            try: os.killpg(int(l),signal.SIGTERM)
            except OSError: pass
        try: os.killpg(lp.pid,signal.SIGTERM)
        except OSError: pass
    time.sleep(10)
json.dump(items,open(f"{out}/items-resolved.json",'w'),indent=1)
print('E3 done')
