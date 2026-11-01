# Rebuild every count in the README from data/firsts.tsv and data/cells.tsv (standard library only).
# Usage: python3 -I report.py <data dir>
import csv,sys,os,statistics as st,math,collections
D=sys.argv[1]
def read(n): return list(csv.DictReader(open(os.path.join(D,n)),delimiter="\t"))
F=read("firsts.tsv"); C=read("cells.tsv")
I=lambda x:int(float(x)) if x not in ("",None) else 0
def bucket(v):
    v=I(v)
    if v==0: return "0"
    if v==4096: return "4096"
    if v<4096: return "1-4095"
    return ">4096"
print("== Conversation starts (first request of each model conversation)")
for study in ("baseline","screen"):
    for arm in ("g0","g1"):
        rows=[r for r in F if r["study"]==study and r["arm"]==arm]
        if not rows: continue
        by=collections.defaultdict(list)
        for r in rows: by[r["role"]].append(r)
        for role in sorted(by):
            rs=by[role]; b=collections.Counter(bucket(r["cached"]) for r in rs)
            fr=sorted({(r["instructions_bytes"],r["tools_bytes"]) for r in rs})
            print(f"{study} {arm} {role}: n={len(rs)} cached " + " ".join(f"{k}:{b[k]}" for k in ("0","1-4095","4096",">4096")) +
                  f" | median input {int(st.median(I(r['input']) for r in rs))} | instructions+tools bytes {fr}")
print()
print("== Cells")
for study in ("baseline","screen"):
    cs=[c for c in C if c["study"]==study]
    if not cs: continue
    fs=[r for r in F if r["study"]==study]
    inp=sum(I(c["input"]) for c in cs); cac=sum(I(c["cached"]) for c in cs)
    first_inp=sum(I(r["input"]) for r in fs); first_cold=sum(I(r["input"]) for r in fs if I(r["cached"])==0)
    req=sum(I(c["requests"]) for c in cs); later=sum(I(c["later_requests"]) for c in cs); later0=sum(I(c["later_cold"]) for c in cs)
    print(f"{study}: cells {len(cs)}, requests {req}, conversation starts {len(fs)} (cold {sum(1 for r in fs if I(r['cached'])==0)}), later requests {later} (cold {later0})")
    print(f"{study}: cached share of input {100*cac/inp:.1f}%, input of cold conversation starts {100*first_cold/inp:.1f}% of all input")
print()
print("== Screen pairs (same run, same task, g1 - g0)")
cells={(c["run"],c["task"],c["arm"]):c for c in C if c["study"]=="screen"}
pairs=[(cells[(r,t,"g0")],cells[(r,t,"g1")]) for (r,t,a) in cells if a=="g0" and (r,t,"g1") in cells]
def share(c): return I(c["cached"])/I(c["input"]) if I(c["input"]) else None
def cost(c): return (I(c["input"])-I(c["cached"]))+0.1*I(c["cached"])+8*I(c["output"])
def ci(v):
    m=st.mean(v); se=st.stdev(v)/math.sqrt(len(v)) if len(v)>1 else float("nan"); return f"{m:+.3f} (95% CI {m-1.96*se:+.3f} to {m+1.96*se:+.3f}, n={len(v)})"
ok=[(a,b) for a,b in pairs if share(a) is not None and share(b) is not None]
if ok:
    print("pairs", len(ok), "runs", sorted({a["run"] for a,b in ok}))
    print("cached share difference, percentage points:", ci([100*(share(b)-share(a)) for a,b in ok]))
    print("cost index ratio g1/g0 (uncached 1, cached 0.1, output 8):", ci([cost(b)/cost(a) for a,b in ok]))
    print("requests difference:", ci([I(b["requests"])-I(a["requests"]) for a,b in ok]))
    graded=[(a,b) for a,b in ok if a["hidden_pass"]!="" and b["hidden_pass"]!=""]
    print("graded pairs (hidden grader ran on both cells):", len(graded))
    for arm,k in (("g0",0),("g1",1)):
        xs=[p[k] for p in ok]; gs=[p[k] for p in graded]
        print(f"{arm}: cached share {100*sum(I(c['cached']) for c in xs)/sum(I(c['input']) for c in xs):.1f}%, hidden pass {sum(I(c['hidden_pass']) for c in gs)}/{len(gs)} graded, "
              f"outcomes {dict(collections.Counter(c['outcome'] for c in xs))}, wall s median {st.median(float(c['wall_s']) for c in xs):.0f}")
    w=sum(1 for a,b in graded if I(b["hidden_pass"]) and not I(a["hidden_pass"])); l=sum(1 for a,b in graded if I(a["hidden_pass"]) and not I(b["hidden_pass"]))
    print(f"hidden pass discordant pairs: lever wins {w}, lever losses {l}")
    for a,b in sorted(graded,key=lambda p:(p[0]["run"],p[0]["task"])):
        if I(a["hidden_pass"])!=I(b["hidden_pass"]): print(f"  {a['run']} {a['task']}: g0 {a['outcome']} pass={a['hidden_pass']} | g1 {b['outcome']} pass={b['hidden_pass']}")
