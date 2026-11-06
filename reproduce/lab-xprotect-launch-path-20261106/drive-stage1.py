#!/usr/bin/env python3
# XProtect lab driver (Studio side). Every remote command runs as <build-host> over ssh. Model-free.
import subprocess, json, time, re, sys, statistics, os
HOST="<build-host>"; XP="<scratch>"; N=int(os.environ.get("N","5"))
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"xplab-results.json")
def mb(cmd, tty=False, timeout=300):
    a=["ssh"]+(["-tt"] if tty else ["-n"])+["-o","BatchMode=yes","-o","ConnectTimeout=15",HOST,cmd]
    r=subprocess.run(a,capture_output=True,text=True,timeout=timeout); return r.returncode, r.stdout
def secs(t):
    p=t.split(":"); s=0.0
    for x in p: s=s*60+float(x)
    return s
NAMES=["XprotectService","XProtectBridgeService","syspolicyd","endpointsecurityd","amfid"]
def sample():
    rc,o=mb("ps -axo pid=,time=,comm=; vm_stat | egrep 'Pages wired|Pages free|File-backed'; sysctl -n kern.num_vnodes; uptime")
    cpu={n:0.0 for n in NAMES}; pids={n:set() for n in NAMES}; extra={}
    for l in o.splitlines():
        m=re.match(r"\s*(\d+)\s+([\d:.]+)\s+(\S.*)$",l)
        if m:
            for n in NAMES:
                if m.group(3).endswith("/"+n) or m.group(3)==n or ("/"+n) in m.group(3):
                    cpu[n]+=secs(m.group(2)); pids[n].add(int(m.group(1)))
        elif "Pages wired" in l: extra["wired_pages"]=int(re.search(r"(\d+)\.",l).group(1))
        elif "Pages free" in l: extra["free_pages"]=int(re.search(r"(\d+)\.",l).group(1))
        elif "load averages" in l: extra["load"]=l.split("load averages:")[1].strip()
        elif re.fullmatch(r"\d+",l.strip()): extra["vnodes"]=int(l.strip())
    return {"t":time.time(),"cpu":cpu,"pids":{n:sorted(v) for n,v in pids.items()},**extra}
def busy():
    rc,o=mb("sh <hostbin>/heavy.sh --held; echo held=$?; ps -axo args= | egrep -c '[k]build.sh|[l]anes-run|[g]o test'")
    held="held=0" in o; n=int(o.strip().splitlines()[-1]); return held or n>0, o.strip().replace("\n"," ")
def wait_quiet(tag):
    waited=0
    while True:
        b,o=busy()
        if not b: return waited
        if waited==0: print("  busy before",tag,o,flush=True)
        time.sleep(30); waited+=30
        if waited>900: raise SystemExit("mb busy > 15 min: stop")
def settle(prev):
    stable=0; cur=prev
    for _ in range(12):
        time.sleep(3); cur=sample()
        d=sum(cur["cpu"][n]-prev["cpu"][n] for n in ("XprotectService","XProtectBridgeService"))
        stable = stable+1 if d<0.02 else 0
        prev=cur
        if stable>=2: break
    return cur
RUN=("cd %s/loop && export PATH=<go 1.27.2 bin>:$PATH GOCACHE=%s/gocache GOFLAGS=-mod=mod && "
     "s=$(perl -MTime::HiRes=time -e 'printf \"%%.2f\",time') && %s; rc=$?; e=$(perl -MTime::HiRes=time -e 'printf \"%%.2f\",time'); "
     "echo \"$rc $s $e\" > %s/%s.done; exit $rc")
def script(tag,core):
    body=RUN%(XP,XP,core,XP,tag)
    mb("cat > %s/%s.sh <<'EOS'\n%s\nEOS"%(XP,tag,body)); mb("rm -f %s/%s.done"%(XP,tag))
def read_done(tag):
    for _ in range(120):
        rc,o=mb("cat %s/%s.done 2>/dev/null"%(XP,tag))
        if o.strip(): r,s,e=o.split(); return int(r),float(e)-float(s)
        time.sleep(2)
    return None,None
def one(arm,i,core):
    tag="%s-%d-%d"%(arm,i,int(time.time())); script(tag,core.replace("@N",str(i)+str(int(time.time())%100000)))
    w=wait_quiet(tag); b0=sample()
    if arm.startswith("b"): rc,_=mb("sh %s/%s.sh"%(XP,tag))
    elif arm.startswith("d1"): rc,_=mb("sh %s/%s.sh"%(XP,tag),tty=True)
    elif arm.startswith("d2"):
        mb("launchctl submit -l xp.%s -- sh %s/%s.sh"%(tag,XP,tag)); rc,_=read_done(tag); mb("launchctl remove xp.%s"%tag)
    else: mb("nohup sh %s/%s.sh </dev/null >/dev/null 2>&1 &"%(XP,tag))   # a, c-detached: launched over ssh as the delivery Builds are
    rc,wall=read_done(tag); b1=sample(); b2=settle(b1)
    b,o=busy()
    r={"arm":arm,"i":i,"rc":rc,"wall_s":round(wall,2) if wall else None,"waited_s":w,"intruded_after":b,
       "xprotect_cpu_s":round(b2["cpu"]["XprotectService"]-b0["cpu"]["XprotectService"],2),
       "bridge_cpu_s":round(b2["cpu"]["XProtectBridgeService"]-b0["cpu"]["XProtectBridgeService"],2),
       "syspolicyd_cpu_s":round(b2["cpu"]["syspolicyd"]-b0["cpu"]["syspolicyd"],2),
       "pid_changed":b0["pids"]["XprotectService"]!=b2["pids"]["XprotectService"],
       "wired_gb_before":round(b0.get("wired_pages",0)*16384/2**30,2),"wired_gb_after":round(b2.get("wired_pages",0)*16384/2**30,2),
       "vnodes_before":b0.get("vnodes"),"vnodes_after":b2.get("vnodes"),"load_before":b0.get("load")}
    print(json.dumps(r),flush=True); return r
def baseline(i,secs_=20):
    b0=sample(); time.sleep(secs_); b1=sample()
    r={"arm":"idle","i":i,"xprotect_cpu_s":round(b1["cpu"]["XprotectService"]-b0["cpu"]["XprotectService"],2),
       "bridge_cpu_s":round(b1["cpu"]["XProtectBridgeService"]-b0["cpu"]["XProtectBridgeService"],2),"window_s":secs_,
       "wired_gb":round(b0.get("wired_pages",0)*16384/2**30,2),"vnodes":b0.get("vnodes"),"load":b0.get("load")}
    print(json.dumps(r),flush=True); return r
TEST="go test -count=1 -ldflags='-X main.xplab=@N' ./tools"
res=[]; t0=time.time()
for i in range(3): wait_quiet("idle"); res.append(baseline(i))
order=["a","b","c1","d1","d2"]
for i in range(N):
    for arm in order:
        if arm=="c1":
            if i==0:
                wait_quiet("cbuild"); tag="cbuild"; script(tag,"mkdir -p %s/stable && go test -c -o %s/stable/tools.test ./tools"%(XP,XP)); b0=sample()
                mb("sh %s/%s.sh"%(XP,tag)); rc,wall=read_done(tag); b2=settle(sample())
                res.append({"arm":"c-build-once","i":0,"rc":rc,"wall_s":round(wall,2),"xprotect_cpu_s":round(b2["cpu"]["XprotectService"]-b0["cpu"]["XprotectService"],2),"bridge_cpu_s":round(b2["cpu"]["XProtectBridgeService"]-b0["cpu"]["XProtectBridgeService"],2)}); print(res[-1],flush=True)
            res.append(one("c-reuse-detached",i,"cd %s/loop/tools && %s/stable/tools.test -test.count=1"%(XP,XP)))
        else:
            core=TEST
            res.append(one({"a":"a-detached","b":"b-attached","d1":"d1-attached-pty","d2":"d2-launchd-submit"}[arm],i,core))
    json.dump(res,open(OUT,"w"),indent=1)
    if time.time()-t0>1500: print("time budget 25 min reached, stopping"); break
for i in range(3,5): wait_quiet("idle"); res.append(baseline(i))
json.dump(res,open(OUT,"w"),indent=1); print("DONE",time.time()-t0)
