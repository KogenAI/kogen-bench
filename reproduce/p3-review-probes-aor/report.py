import csv,sys,collections
d=sys.argv[1]
go=list(csv.DictReader(open(d+"/go_cells.tsv"),delimiter="\t"))
aor=list(csv.DictReader(open(d+"/aor_cells.tsv"),delimiter="\t"))
def pairs(rows):
    t=collections.defaultdict(dict)
    for r in rows: t[r["task"]][r["arm"]]=r
    return t
print("1. Go tasks (13 tasks, 1 trial per arm; hidden pass = every hidden check of the task passed)")
print("arm  hidden_pass  wall_s  tokens")
for a in ("b0","p3"):
    x=[r for r in go if r["arm"]==a]
    print("%-4s %2d/%d  %9d %9d"%(a,sum(int(r["hidden_pass"]) for r in x),len(x),sum(int(r["wall_s"]) for r in x),sum(int(r["tokens"]) for r in x)))
print("wall and tokens include cells that ended build_blocked, review_blocked or no_progress")
P=pairs(go); w=l=0
print(); print("2. Go pairs where the hidden result differs")
for t in sorted(P):
    b,p=int(P[t]["b0"]["hidden_pass"]),int(P[t]["p3"]["hidden_pass"])
    if b!=p:
        print("%s: b0 %s (%s) vs p3 %s (%s)"%(t,"pass" if b else "fail",P[t]["b0"]["outcome"],"pass" if p else "fail",P[t]["p3"]["outcome"])); w+=p>b; l+=b>p
print("p3 wins %d, loses %d, wins-losses %+d (keep rule: >= +3)"%(w,l,w-l))
print(); print("3. Outcome per arm")
for a in ("b0","p3"): print("Go",a,dict(sorted(collections.Counter(r["outcome"] for r in go if r["arm"]==a).items())))
for a in ("b0","p3"): print("AoR",a,dict(sorted(collections.Counter(r["outcome"] for r in aor if r["arm"]==a).items())))
print(); print("4. AoR tasks (6 tasks, 1 trial per arm); 'ungraded' = the grader had not run when this result was written")
print("task  arm  outcome            graded hidden_pass ids_passed/expected")
for r in aor: print("%-5s %-4s %-18s %-6s %-11s %s/%s"%(r["task"],r["arm"],r["outcome"],r["graded"],r["hidden_pass"] or "-",r["ids_passed"] or "-",r["ids_expected"] or "-"))
g=[r for r in aor if r["graded"]=="yes"]
print("graded AoR cells: %d of %d; passed: %d"%(len(g),len(aor),sum(r["hidden_pass"]=="1" for r in g)))
print(); print("5. AoR pairs (a cell that did not land has no implementation and counts as no pass; a landed cell not yet graded leaves its pair open)")
def res(r):
    if r["outcome"]!="landed": return "no-pass"
    return {"1":"pass","0":"fail"}.get(r["hidden_pass"],"ungraded")
P=pairs(aor); w=l=same=op=0
for t in sorted(P):
    b,p=res(P[t]["b0"]),res(P[t][[k for k in P[t] if k!="b0"][0]])
    pk=[k for k in P[t] if k!="b0"][0]
    print("%s: b0 %s | %s %s"%(t,b,pk,p))
    if "ungraded" in (b,p): op+=1
    elif b==p or (b!="pass" and p!="pass"): same+=1
    else: w+=p=="pass"; l+=b=="pass"
print("AoR pairs: patch wins %d, loses %d, no difference %d, open (ungraded) %d"%(w,l,same,op))
