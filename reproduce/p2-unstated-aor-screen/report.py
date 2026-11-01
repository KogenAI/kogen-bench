import csv,sys,collections
# usage: report.py <data dir> <data file stem> <patch arm name>
d,stem,pa=sys.argv[1],sys.argv[2],sys.argv[3]
rows=list(csv.DictReader(open("%s/%s_cells.tsv"%(d,stem)),delimiter="\t"))
P=collections.defaultdict(dict)
for r in rows: P[r["task"]][r["arm"]]=r
print("1. AoR task cells (6 tasks x repetitions; hidden pass = every hidden check passed; not every cell finished)")
print("arm  cells  hidden_pass  wall_s")
for a in ("b0",pa):
    x=[r for r in rows if r["arm"]==a]
    print("%-4s %3d  %3d  %9d"%(a,len(x),sum(int(r["hidden_pass"]) for r in x),sum(int(r["wall_s"]) for r in x)))
print(); print("2. Complete pairs (both arms have a cell) and pairs where the hidden result differs")
n=w=l=0
for t in sorted(P):
    if "b0" in P[t] and pa in P[t]:
        n+=1; b,p=int(P[t]["b0"]["hidden_pass"]),int(P[t][pa]["hidden_pass"])
        w+=p>b; l+=b>p
print("complete pairs %d, %s wins %d, loses %d, wins-losses %+d (keep rule: >= +3)"%(n,pa,w,l,w-l))
print(); print("3. Outcome per arm")
for a in ("b0",pa): print(a,dict(sorted(collections.Counter(r["outcome"] for r in rows if r["arm"]==a).items())))
