import json,os
d=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","results.json")))
rows=d["rows"]; tasks=sorted({r["task"] for r in rows})
def cell(r):
    if r is None: return "not run","-"
    h="%s/%s"%(r["hidden_passed"],r["hidden_total"]) if "hidden_total" in r else "ungraded"
    return h,r["outcome"]
print("| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome |"); print("| --- | --- | --- | --- | --- |")
for t in tasks:
    c={a:next((r for r in rows if r["task"]==t and r["arm"]==a),None) for a in ("g0","g1")}
    a0,o0=cell(c["g0"]); a1,o1=cell(c["g1"]); print("| %s | %s | %s | %s | %s |"%(t,a0,a1,o0,o1))
print()
for a,m in sorted(d["climb_metrics"].items()):
    w=sum(s["wall_s"] or 0 for r in rows if r["arm"]==a for s in r["stages"])
    print("%s: cells %d, hidden %d/%d (mean %s), landed %d, valid Intents %d, all-pass %d, wall %d s"%(a,m["cells"],m["hidden_passed"],m["hidden_total"],m["hidden_frac_mean"],m["landed"],m["valid_intent"],m["all_pass"],w))
