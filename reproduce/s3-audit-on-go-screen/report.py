import csv,sys,collections
# usage: report.py <data dir> <data file stem> <patch arm name>
d,stem,pa=sys.argv[1],sys.argv[2],sys.argv[3]
rows=list(csv.DictReader(open("%s/%s_cells.tsv"%(d,stem)),delimiter="\t"))
P=collections.defaultdict(dict)
for r in rows: P[r["task"]][r["arm"]]=r
print("1. Go tasks (13 tasks, 1 trial per arm; hidden pass = every hidden check of the task passed)")
print("arm  hidden_pass  wall_s  tokens  requests")
for a in ("b0",pa):
    x=[r for r in rows if r["arm"]==a]
    print("%-4s %2d/%d  %9d %9d %6d"%(a,sum(int(r["hidden_pass"]) for r in x),len(x),sum(int(r["wall_s"]) for r in x),sum(int(r["tokens"]) for r in x),sum(int(r["requests"]) for r in x)))
print("wall, tokens and requests include cells that ended refused or build_blocked")
print(); print("2. Pairs where the hidden result differs")
w=l=0
for t in sorted(P):
    b,p=int(P[t]["b0"]["hidden_pass"]),int(P[t][pa]["hidden_pass"])
    if b!=p:
        print("%s: b0 %s (%s) vs %s %s (%s)"%(t,"pass" if b else "fail",P[t]["b0"]["outcome"],pa,"pass" if p else "fail",P[t][pa]["outcome"])); w+=p>b; l+=b>p
print("%s wins %d, loses %d, wins-losses %+d (keep rule: >= +3)"%(pa,w,l,w-l))
print(); print("3. Outcome per arm")
for a in ("b0",pa): print(a,dict(sorted(collections.Counter(r["outcome"] for r in rows if r["arm"]==a).items())))
