# Build the pack data from copied run directories (model-free).
# Usage: python3 -I build_data.py <out dir> <study>=<runs root>:<run>[,<run>...] ...
#   study "baseline" = earlier eu2 runs (characterisation), study "screen" = lcache runs.
# Writes <out>/firsts.tsv (one row per conversation start) and <out>/cells.tsv (one row per cell).
# Task names are replaced by T01..T13 (alphabetical); hidden suites are not read.
import json,glob,os,sys,csv
# T01..T13 = the task directory names of the given runs in alphabetical order (names are not stored here)
SPECS=[(x.split("=",1)[0],)+tuple(x.split("=",1)[1].split(":",1)) for x in sys.argv[2:]]
TASKS=sorted({os.path.basename(d) for _,root,runs in SPECS for run in runs.split(",") for d in glob.glob(f"{root}/{run}/cells/*")})
TID={t:"T%02d"%(i+1) for i,t in enumerate(TASKS)}
def lines(p):
    try:
        for l in open(p):
            try: yield json.loads(l)
            except Exception: pass
    except FileNotFoundError: return
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
F=[]; C=[]
for spec in sys.argv[2:]:
    study,rest=spec.split("=",1); root,runs=rest.split(":",1)
    for run in runs.split(","):
        for d in sorted(glob.glob(f"{root}/{run}/cells/*/r1/g[01]")):
            task=d.split("/")[-3]; arm=d.split("/")[-1]
            if not os.path.exists(d+"/result.json"): continue
            base=dict(study=study,run=run,task=TID[task],arm=arm)
            req=inp=cac=out_=0; seen=set(); conv=None; later=later0=0
            for e in lines(d+"/shaping-events.ndjson"):
                if e.get("event")!="provider_call" or e.get("status")!="completed": continue
                p=e.get("provider") or {}; cv=p.get("conversation_id"); u=e.get("usage") or {}; fp=p.get("fingerprints") or {}
                req+=1; inp+=u.get("input") or 0; cac+=u.get("cached") or 0; out_+=u.get("output") or 0
                if cv not in seen:
                    seen.add(cv); F.append(dict(base,role="shape:"+("main" if e.get("scope")=="main shaping" else "example_check" if e.get("scope")=="example check" else str(e.get("scope"))),
                        at=p.get("timestamp") or "",input=u.get("input") or 0,cached=u.get("cached") or 0,
                        instructions_bytes=(fp.get("policy") or {}).get("bytes"),tools_bytes=(fp.get("tools") or {}).get("bytes")))
                else:
                    later+=1; later0+=(u.get("cached") or 0)==0
            pa=None
            for e in lines(d+"/run-log/log.jsonl"):
                ev=e.get("event")
                if ev=="provider_attempt": pa=e.get("provider") or {}; conv=pa.get("conversation_id")
                if ev!="request": continue
                u=e.get("usage") or {}
                req+=1; inp+=u.get("input") or 0; cac+=u.get("cached") or 0; out_+=u.get("output") or 0
                if conv not in seen:
                    seen.add(conv); fp=(pa or {}).get("fingerprints") or {}
                    F.append(dict(base,role=e.get("role"),at=e.get("at",""),input=u.get("input") or 0,cached=u.get("cached") or 0,
                        instructions_bytes=(fp.get("policy") or {}).get("bytes"),tools_bytes=(fp.get("tools") or {}).get("bytes")))
                else:
                    later+=1; later0+=(u.get("cached") or 0)==0
            try: ev=json.load(open(d+"/evaluation.json")); hp=int(bool(ev.get("all_passed") and ev.get("complete")))
            except Exception: hp=""
            r=json.load(open(d+"/result.json"))
            C.append(dict(base,outcome=r.get("outcome"),hidden_pass=hp,requests=req,input=inp,cached=cac,output=out_,
                later_requests=later,later_cold=later0,wall_s=r.get("wall_s")))
def w(name,rows):
    if not rows: return
    with open(os.path.join(out,name),"w",newline="") as f:
        cw=csv.DictWriter(f,fieldnames=list(rows[0].keys()),delimiter="\t",lineterminator="\n"); cw.writeheader()
        for r in sorted(rows,key=lambda r:tuple(str(r[k]) for k in ("study","run","task","arm")+(("role","at") if "role" in r else ()))): cw.writerow(r)
w("firsts.tsv",F); w("cells.tsv",C); print(len(F),"conversation starts,",len(C),"cells")
