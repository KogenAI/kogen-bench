#!/usr/bin/env python3
"""E2 orchestrator (runs on EU as lanes). Replays 4 concurrent Build streams through heavy-lab.sh under one lock policy arm.
usage: e2.py <arm A|B|C> <schedule.json> <outdir>   env: W (work root), no model, no network except module fetch already cached."""
import json,os,subprocess,sys,threading,time
arm,sched,out=sys.argv[1:4]
W=os.environ['W']; S=json.load(open(sched)); os.makedirs(out,exist_ok=True)
lockdir=f"{W}/lock-{arm}-{int(time.time())}"
env=dict(os.environ,LAB_ARM=arm,LAB_LOCKDIR=lockdir,LAB_CAP='2',GOCACHE=f"{W}/gocache",GOMODCACHE=f"{W}/gomod",TMPDIR=f"{W}/tmp",
         GOTOOLCHAIN='local',PATH=os.path.expanduser("~/.local/share/mise/installs/node/24.21.0/bin:")+os.path.expanduser("~/.local/share/mise/installs/go/1.27.2/bin:")+"/usr/local/bin:/usr/bin:/bin")
recs=[]; lk=threading.Lock(); t0=time.time()
def one(sid,i,item):
    cf=f"{out}/cmd-{sid}-{i}/cmd.sh"; os.makedirs(os.path.dirname(cf),exist_ok=True)
    open(cf,'w').write(f"# lab-class: {item['class']}\n{item['cmd']}\n")
    e=dict(env,LAB_CLASS=item['class'])
    ts=time.time()
    p=subprocess.Popen(['sh',f'{W}/bin/heavy-lab.sh',cf],cwd=f"{W}/trees/{item['tree']}",env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,start_new_session=True)
    open(f"{out}/pids.txt",'a').write(f"{p.pid}\n")
    o,_=p.communicate(); te=time.time()
    open(f"{out}/cmd-{sid}-{i}/out.txt",'w').write(o)
    with lk: recs.append(dict(stream=sid,i=i,kind=item['kind'],suite=item['suite'],cls=item['class'],pid=p.pid,t_submit=ts-t0,t_end=te-t0,total=te-ts,rc=p.returncode))
def stream(sid,items):
    time.sleep(S['stagger'][sid])
    n=0
    while True:
        for i,item in enumerate(items):
            if os.path.exists(f"{out}/STOP"): return
            one(sid,f"{n}-{i}",item); time.sleep(S['think'])
        n+=1
        if not os.environ.get('LOOP'): return
th=[threading.Thread(target=stream,args=(sid,items)) for sid,items in enumerate(S['streams'])]
[t.start() for t in th]; [t.join() for t in th]
makespan=time.time()-t0
# join wrapper log (run/end stamps) to split wait vs run
log={}
for l in open(f"{lockdir}/kogen-heavy.log"):
    f=l.split(); 
    if len(f)<5: continue
    log.setdefault(int(f[1]),{})[f[2].split('-')[0] if f[2].startswith('wait') else f[2].split(' ')[0]]=(float(f[0]),l.strip())
for r in recs:
    d=log.get(r['pid'],{}); w=d.get('wait'); ru=d.get('run'); en=d.get('end')
    r['wait']=(ru[0]-w[0]) if (w and ru) else None; r['run']=(en[0]-ru[0]) if (ru and en) else None
json.dump(dict(arm=arm,makespan=makespan,recs=sorted(recs,key=lambda r:r['t_submit'])),open(f"{out}/result.json",'w'),indent=1)
print(json.dumps(dict(arm=arm,makespan=round(makespan),n=len(recs),suites=sum(1 for r in recs if r['kind']=='suite'),red=sum(1 for r in recs if r['rc']))))
