#!/usr/bin/env python3
"""lrepin-count.py RUNSROOT RUNID... : model-free loop-side classes per cell (registered in lrepin.md, 1 Nov 2026).
Per cell (arm dir with run-log/log.jsonl): shell calls; refusal46 = shell result 46 bytes sha 79a88ff9 ('supply exactly one of command or handle');
refusal39 ('handle must be a nonempty string'), refusal27 ('unknown shell handle'), refusal_cmd ('argument command must be a string'): matched by result size only
for 39/27, by sha prefix for the rest; yields = 76-byte shell results; retrievals = shell calls with 45-byte arguments (handle only);
net_end = provider_attempt errors with a network text or stdout/stderr 'did not answer after N attempts' / 'network error'; unavailable = outcome 'unavailable';
polls = yields + retrievals (shell calls beyond the first of each command); small-result signatures (<=120 B) for the new-refusal-class check.
Output: TSV to stdout (cell rows) + a per-arm summary to stderr-free second block."""
import json,sys,os,glob,re,collections
root=sys.argv[1]; runs=sys.argv[2:]
rows=[]; sig=collections.defaultdict(collections.Counter)
for run in runs:
    for d in sorted(glob.glob(f"{root}/{run}/cells/*/*/*")):
        p=d.split("/"); task,rep,arm=p[-3],p[-2],p[-1]
        r={}
        if os.path.exists(d+"/result.json"):
            try: r=json.load(open(d+"/result.json"))
            except Exception: r={"outcome":"BADRESULT"}
        c=collections.Counter(); hasLog=os.path.exists(d+"/run-log/log.jsonl")
        if hasLog:
            for l in open(d+"/run-log/log.jsonl"):
                try:o=json.loads(l)
                except Exception: continue
                e=o.get("event")
                if e=="tool_call":
                    res=o.get("result"); rb=res if isinstance(res,int) else (res or {}).get("bytes") if isinstance(res,dict) else None
                    rs=(res or {}).get("sha256","")[:8] if isinstance(res,dict) else ""
                    ab=(o.get("arguments") or {}).get("bytes")
                    c["tool_calls"]+=1
                    if rb is not None and rb<=120: sig[arm][(o.get("name"),rb,rs)]+=1
                    if o.get("name")=="shell":
                        c["shell"]+=1
                        if ab==45: c["retrievals"]+=1
                        if rb==76: c["yields"]+=1
                        if rb==46 and rs=="79a88ff9": c["refusal46"]+=1
                        elif rb==39: c["refusal39"]+=1
                        elif rb==27: c["refusal27"]+=1
                elif e=="provider_attempt":
                    pr=o.get("provider") or {}; er=pr.get("error")
                    if er and re.search(r"network|dial|i/o timeout|connection|dns|transport",json.dumps(er),re.I): c["net_attempt_err"]+=1
                elif e=="request": c["requests"]+=1
        txt=""
        for f in ("stdout.txt","stderr.txt"):
            try: txt+=open(f"{d}/{f}",errors="replace").read()
            except Exception: pass
        c["net_end"]=len(re.findall(r"did not answer after \d+ attempts: network error|network failure",txt))
        c["connect_wait"]=len(re.findall(r"response wait exceeded|accept connections|connect wait",txt))
        refus=sorted(set(re.findall(r"\b(?:intent|controller|provider|build|review)/[a-z_]+",txt)))
        rows.append([run,task,rep,arm,r.get("outcome"),int(hasLog),c["requests"],c["shell"],c["yields"],c["retrievals"],c["yields"]+c["retrievals"],c["refusal46"],c["refusal39"],c["refusal27"],c["net_attempt_err"],c["net_end"],c["connect_wait"],int(r.get("outcome")=="unavailable"),",".join(refus)])
H="run task rep arm outcome has_log requests shell yields retrievals polls refusal46 refusal39 refusal27 net_attempt_err net_end connect_wait unavailable stdout_classes".split()
print("\t".join(H))
for x in rows: print("\t".join(str(v) for v in x))
print("#SUMMARY by arm: cells, cells_with_log, shell, polls, refusal46, cells_with_refusal46, net_end cells, unavailable")
for a in sorted({x[3] for x in rows}):
    R=[x for x in rows if x[3]==a]; L=[x for x in R if x[5]]
    print("#",a,len(R),len(L),sum(x[7] for x in L),sum(x[10] for x in L),sum(x[11] for x in L),sum(1 for x in L if x[11]),sum(1 for x in R if x[15]),sum(x[17] for x in R))
print("#SIGNATURES (tool,bytes,sha8) count by arm")
for a in sorted(sig):
    for k,v in sorted(sig[a].items(),key=lambda kv:-kv[1])[:25]: print("#",a,k,v)
