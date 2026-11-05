import json,os
d=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","results.json")))
rows=[r for r in d["rows"] if r.get("graded")]; tasks=sorted({r["task"] for r in rows})
print("| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome | refused g0 / g1 |"); print("| --- | --- | --- | --- | --- | --- |")
for t in tasks:
    c={a:next(r for r in rows if r["task"]==t and r["arm"]==a) for a in ("g0","g1")}
    print("| %s | %d/%d | %d/%d | %s | %s | %s / %s |"%(t,c["g0"]["hidden_passed"],c["g0"]["hidden_total"],c["g1"]["hidden_passed"],c["g1"]["hidden_total"],c["g0"]["outcome"],c["g1"]["outcome"],c["g0"]["refused_submissions"],c["g1"]["refused_submissions"]))
print()
for a,m in sorted(d["climb_metrics"].items()):
    w=sum(s["wall_s"] for r in rows if r["arm"]==a for s in r["stages"])
    print("%s: cells %d, hidden %d/%d (mean %s), landed %d, valid Intents %d, all-pass %d, wall %d s"%(a,m["cells"],m["hidden_passed"],m["hidden_total"],m["hidden_frac_mean"],m["landed"],m["valid_intent"],m["all_pass"],w))
