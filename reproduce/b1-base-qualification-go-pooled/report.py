import csv,sys,collections
# usage: report.py <data dir> <data file stem>
d,stem=sys.argv[1],sys.argv[2]
rows=list(csv.DictReader(open("%s/%s_cells.tsv"%(d,stem)),delimiter="\t"))
INFRA={"unavailable","provider"}
runs=sorted(set(r["run"] for r in rows))
P=collections.defaultdict(dict)
for r in rows: P[(r["run"],r["task"])][r["arm"]]=r
print("1. Per repetition (13 Go tasks, 1 trial per arm; hidden pass = every hidden check passed)")
print("run  arm  hidden_pass  wall_s  tokens  requests")
for run in runs+["all"]:
    for a in ("b0","b1"):
        x=[r for r in rows if r["arm"]==a and (run=="all" or r["run"]==run)]
        print("%-4s %-3s %2d/%d %9d %9d %6d"%(run,a,sum(int(r["hidden_pass"]) for r in x),len(x),sum(int(r["wall_s"]) for r in x),sum(int(r["tokens"]) for r in x),sum(int(r["requests"]) for r in x)))
print("wall, tokens and requests include cells that ended refused, build_blocked, review_blocked or unavailable")
print(); print("2. Pairs where the hidden result differs")
W=L=0
for k in sorted(P):
    b,p=P[k]["b0"],P[k]["b1"]
    if b["hidden_pass"]!=p["hidden_pass"]:
        print("%s %s: b0 %s (%s) vs b1 %s (%s)"%(k[0],k[1],"pass" if b["hidden_pass"]=="1" else "fail",b["outcome"],"pass" if p["hidden_pass"]=="1" else "fail",p["outcome"]))
        W+=p["hidden_pass"]>b["hidden_pass"]; L+=b["hidden_pass"]>p["hidden_pass"]
print("b1 wins %d, loses %d, wins-losses %+d over %d pairs"%(W,L,W-L,len(P)))
ex=[k for k in P if P[k]["b0"]["outcome"] in INFRA or P[k]["b1"]["outcome"] in INFRA]
print("pairs with a provider/availability stop in either cell (both cells failed the hidden checks): %d (%s)"%(len(ex),", ".join("%s %s"%k for k in sorted(ex))))
print(); print("3. Hidden passes per task over the %d repetitions (b0 / b1)"%len(runs))
T=collections.defaultdict(lambda:[0,0])
for k in P:
    T[k[1]][0]+=int(P[k]["b0"]["hidden_pass"]); T[k[1]][1]+=int(P[k]["b1"]["hidden_pass"])
for t in sorted(T): print(t,T[t][0],T[t][1])
print(); print("4. Outcome per arm")
for a in ("b0","b1"): print(a,dict(sorted(collections.Counter(r["outcome"] for r in rows if r["arm"]==a).items())))
print(); print("5. Without task G08 (the task that ends review_blocked or refused in both arms)")
for a in ("b0","b1"):
    x=[r for r in rows if r["arm"]==a and r["task"]!="G08"]
    print("%-3s wall_s %d requests %d tokens %d"%(a,sum(int(r["wall_s"]) for r in x),sum(int(r["requests"]) for r in x),sum(int(r["tokens"]) for r in x)))
