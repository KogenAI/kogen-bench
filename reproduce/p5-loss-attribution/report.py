import csv,sys,math
# usage: report.py <data dir>
d=sys.argv[1]
cells=list(csv.DictReader(open(d+"/p5-loss-attribution_cells.tsv"),delimiter="\t"))
aa=list(csv.DictReader(open(d+"/p5-loss-attribution_aa.tsv"),delimiter="\t"))
k={r["key"]:int(r["value"]) for r in csv.DictReader(open(d+"/p5-loss-attribution_counts.tsv"),delimiter="\t")}
def wl(rs): return sum(r["pair_result"]=="p5_win" for r in rs),sum(r["pair_result"]=="p5_loss" for r in rs)
print("1. Recorded figure: every pair except the one lost to a service timeout (class d)")
rec=[r for r in cells if r["cause_class"]!="d"]
w,l=wl(rec); print("pairs %d, patched wins %d, losses %d, net %+d"%(len(rec),w,l,w-l))
print(); print("2. Cause of each patched loss")
loss=[r for r in cells if r["pair_result"]=="p5_loss"]
for c in sorted({r["cause_class"] for r in loss}): print("class %s: %d  (%s)"%(c,sum(r["cause_class"]==c for r in loss),", ".join(r["task"]+r["rep"] for r in loss if r["cause_class"]==c)))
print("class a (builder stopped with its own work wrong or unchecked): %d"%sum(r["cause_class"]=="a" for r in loss))
print(); print("3. Recount: pairs where both arms reached Build with a sound Intent")
inn=[r for r in cells if r["in_recount"]=="yes"]
for rep in ("r1","r3","r4"):
    w,l=wl([r for r in inn if r["rep"]==rep]); print("%s: %d pairs, wins %d, losses %d"%(rep,sum(r["rep"]==rep for r in inn),w,l))
w,l=wl(inn); print("pooled: %d pairs, wins %d, losses %d, net %+d"%(len(inn),w,l,w-l))
l2=sum(r["pair_result"]=="p5_loss" and r["cause_class"]!="e" for r in inn); print("net %d if the one ambiguous-request loss (class e) is also left out"%(-l2))
print(); print("4. Shape-time defects by arm (identical shaping in both arms)")
p=sum(r["shape_defect_arm"]=="p5" for r in cells); b=sum(r["shape_defect_arm"]=="b0" for r in cells)
print("patched arm %d, unpatched arm %d"%(p,b))
n=p+b; m=max(p,b); pr=2*sum(math.comb(n,i) for i in range(m,n+1))/2**n
print("chance of a split at least this lopsided with %d defects (two-sided): %.1f%%"%(n,100*pr))
print(); print("5. How often the patched and unpatched arms differ on the hidden result")
ni=[r for r in cells if r["cause_class"]!="d"]
fl=sum(r["pair_result"] in("p5_win","p5_loss") for r in ni); print("patched against unpatched: %d of %d pairs (%.0f%%)"%(fl,len(ni),100*fl/len(ni)))
print("unpatched against unpatched (partial, %d finished pairs): outcome differs in %d, hidden result flips in %d to %d (%.0f%% to %.0f%%)"%(k["aa_finished_pairs"],k["aa_pairs_outcome_differs"],k["aa_hidden_flips_low"],k["aa_hidden_flips_high"],100*k["aa_hidden_flips_low"]/k["aa_finished_pairs"],100*k["aa_hidden_flips_high"]/k["aa_finished_pairs"]))
print("rows in the unpatched-against-unpatched file: %d, all build_blocked: %s"%(len(aa),all(r["outcome"]=="build_blocked" for r in aa)))
print(); print("6. Shape-time acceptance contradicting the Intent or the request")
t=k["screen_cells_with_shape_defect"]+k["aa_cells_with_shape_defect"]; c=k["screen_cells"]+k["aa_finished_cells"]
print("%d of %d cells (%d of %d patched-test cells, %d of %d finished unpatched-pair cells)"%(t,c,k["screen_cells_with_shape_defect"],k["screen_cells"],k["aa_cells_with_shape_defect"],k["aa_finished_cells"]))
