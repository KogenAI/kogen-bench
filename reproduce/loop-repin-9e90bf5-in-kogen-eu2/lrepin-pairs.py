#!/usr/bin/env python3
"""lrepin-pairs.py RUNSROOT RUNID... : hidden pass per cell (evaluation.json all_passed and complete), paired g0 vs g1 per task per run.
Prints per-cell TSV rows, then pair classes (both pass, both fail, g1 wins, g1 loses), wall/requests sums, last result.json mtime per run."""
import json,glob,os,sys,datetime
root=sys.argv[1]; runs=sys.argv[2:]
cells={}
for run in runs:
    last=0
    for d in sorted(glob.glob(f"{root}/{run}/cells/*/*/*")):
        t,rep,arm=d.split("/")[-3:]
        r={}; e={}
        try: r=json.load(open(d+"/result.json")); last=max(last,os.path.getmtime(d+"/result.json"))
        except Exception: pass
        try: e=json.load(open(d+"/evaluation.json"))
        except Exception: pass
        p=bool(e.get("all_passed") and e.get("complete"))
        reqs=sum((s.get("requests") or 0) for s in r.get("stages",[])); wall=r.get("wall_s")
        cells[(run,t,rep,arm)]=dict(outcome=r.get("outcome"),pass_=p,graded=bool(e),wall=wall,reqs=reqs,failed=[x if isinstance(x,str) else json.dumps(x)[:80] for x in e.get("failed",[])][:4])
    print(f"#last_result_mtime {run} {datetime.datetime.utcfromtimestamp(last).isoformat()}Z" if last else f"#last_result_mtime {run} none")
print("run\ttask\trep\tarm\toutcome\tpass\tgraded\twall_s\trequests")
for k,v in sorted(cells.items()): print("\t".join(map(str,list(k)+[v["outcome"],int(v["pass_"]),int(v["graded"]),round(v["wall"] or 0),v["reqs"]])))
cls={"both_pass":[],"both_fail":[],"g1_wins":[],"g1_loses":[]}
for (run,t,rep,arm),v in sorted(cells.items()):
    if arm!="g0": continue
    w=cells.get((run,t,rep,"g1"))
    if not w: continue
    a,b=v["pass_"],w["pass_"]
    cls["both_pass" if a and b else "both_fail" if not a and not b else "g1_wins" if b else "g1_loses"].append((run,t,rep,v["outcome"],w["outcome"]))
print("#PAIRS", {k:len(x) for k,x in cls.items()})
for k in ("g1_wins","g1_loses","both_fail"):
    for x in cls[k]: print("#",k,*x)
for arm in ("g0","g1"):
    A=[v for k,v in cells.items() if k[3]==arm]
    print("#",arm,"pass",sum(v["pass_"] for v in A),"of",len(A),"wall_sum",round(sum(v["wall"] or 0 for v in A)),"requests",sum(v["reqs"] for v in A))
