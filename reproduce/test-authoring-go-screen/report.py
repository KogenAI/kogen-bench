import csv,sys,collections
# usage: report.py <data dir> <data file stem> <patch arm name>
d,stem,pa=sys.argv[1],sys.argv[2],sys.argv[3]
rows=list(csv.DictReader(open("%s/%s_cells.tsv"%(d,stem)),delimiter="\t"))
P=collections.defaultdict(dict)
for r in rows: P[r["task"]][r["arm"]]=r
print("1. Go tasks (4 tasks, 1 trial per arm; hidden pass = every hidden check passed)")
print("arm  hidden_pass  wall_s  build_s  tokens  requests")
for a in ("b0",pa):
    x=[r for r in rows if r["arm"]==a]
    print("%-4s %2d/%d  %7d %7d %9d %5d"%(a,sum(int(r["hidden_pass"]) for r in x),len(x),sum(int(r["wall_s"]) for r in x),sum(int(r["build_s"]) for r in x),sum(int(r["tokens"]) for r in x),sum(int(r["requests"]) for r in x)))
print(); print("2. Pairs where the hidden result differs")
w=l=0
for t in sorted(P):
    b,p=int(P[t]["b0"]["hidden_pass"]),int(P[t][pa]["hidden_pass"]); w+=p>b; l+=b>p
print("%s wins %d, loses %d"%(pa,w,l))
print(); print("3. Build-stage wall per task (patched vs unpatched)")
n15=0
for t in sorted(P):
    b,p=int(P[t]["b0"]["build_s"]),int(P[t][pa]["build_s"]); ch=100.0*(p-b)/b; n15+=ch<=-15
    print("%s: b0 %d s, %s %d s (%+.0f%%)"%(t,b,pa,p,ch))
print("tasks with build wall >= 15%% lower: %d of %d (bar: >= 3 of 5, or fewer waits / shorter authored tests, not measured here)"%(n15,len(P)))
print(); print("4. Outcome per arm")
for a in ("b0",pa): print(a,dict(sorted(collections.Counter(r["outcome"] for r in rows if r["arm"]==a).items())))
