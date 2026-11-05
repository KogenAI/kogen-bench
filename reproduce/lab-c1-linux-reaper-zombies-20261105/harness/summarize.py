#!/usr/bin/env python3
"""Lab C1 summary: reads results/<host>/<tag>/<unit>-<arm>-r<rep>/result.json, prints markdown tables and summary.json."""
import json, os, statistics, sys
root = sys.argv[1]
rows = []
for dp, _, fs in os.walk(root):
    if "result.json" in fs:
        r = json.load(open(os.path.join(dp, "result.json")))
        r["tag"] = os.path.basename(os.path.dirname(dp))
        rows.append(r)
meas = [r for r in rows if r["tag"] == "measured"]
GOT = ("shaping", "verification", "loop")
def cell(rs):
    if not rs: return None
    w = [r["wall_s"] for r in rs]
    return dict(n=len(rs), passed=sum(r["passed"] for r in rs), median_s=round(statistics.median(w), 1), min_s=round(min(w), 1), max_s=round(max(w), 1),
                orphans_alive=sum(r["orphans_alive"] for r in rs), orphans_zombie=sum(r["orphans_zombie"] for r in rs),
                timeouts=sum(r["timeout_panic"] for r in rs), fails=sorted({t for r in rs for t in r["fail_tests"]})[:8])
out = {"cells": {}, "arms": {}}
hosts = sorted({r["host"] for r in meas})
print("| unit | host | arm | n | pass | median s (min-max) | orphans alive/zombie | 10m timeouts | failing tests |")
print("|---|---|---|---|---|---|---|---|---|")
for u in GOT + ("sweep", "fixture"):
    for h in hosts:
        for a in "ABC":
            c = cell([r for r in meas if r["unit"] == u and r["host"] == h and r["arm"] == a])
            if not c: continue
            out["cells"]["%s/%s/%s" % (u, h, a)] = c
            extra = ""
            if u == "fixture":
                zp = [r["zprobe"] or "" for r in meas if r["unit"] == u and r["host"] == h and r["arm"] == a]
                extra = "zprobe pass %d/%d" % (sum(z.startswith("ZPROBE PASS") for z in zp), len(zp))
            if u == "sweep":
                xs = [r.get("xv1") or [] for r in meas if r["unit"] == u and r["host"] == h and r["arm"] == a]
                surv = sorted({k for x in xs for k, v in x if v == "SURVIVED"})
                extra = "X-V1 survivors: %s" % (",".join(surv) or "none")
            print("| %s | %s | %s | %d | %d/%d | %.1f (%.1f-%.1f) | %d/%d | %d | %s %s |" % (u, h, a, c["n"], c["passed"], c["n"], c["median_s"], c["min_s"], c["max_s"],
                  c["orphans_alive"], c["orphans_zombie"], c["timeouts"], " ".join(c["fails"]), extra))
for a in "ABC":
    g = [r for r in meas if r["arm"] == a and r["unit"] in GOT]
    out["arms"][a] = dict(gotest_runs=len(g), gotest_passed=sum(r["passed"] for r in g), gotest_wall_s=round(sum(r["wall_s"] for r in g), 1),
                          orphans_alive=sum(r["orphans_alive"] for r in g), orphans_zombie=sum(r["orphans_zombie"] for r in g),
                          fixture_runs=sum(1 for r in meas if r["arm"] == a and r["unit"] == "fixture"),
                          fixture_orphans=sum(r["orphans_alive"] for r in meas if r["arm"] == a and r["unit"] == "fixture"),
                          sweep_runs=sum(1 for r in meas if r["arm"] == a and r["unit"] == "sweep"),
                          sweep_passed=sum(r["passed"] for r in meas if r["arm"] == a and r["unit"] == "sweep"))
print()
for a, v in out["arms"].items(): print("arm", a, json.dumps(v))
# B vs C duration per repo and host (medians of all runs)
for u in GOT:
    for h in hosts:
        b, c = out["cells"].get("%s/%s/B" % (u, h)), out["cells"].get("%s/%s/C" % (u, h))
        if b and c: print("B/C median %s %s: %.1f / %.1f = %+.1f%%" % (u, h, b["median_s"], c["median_s"], 100 * (b["median_s"] / c["median_s"] - 1)))
dry = [r for r in rows if r["tag"] == "dry"]
print("\ndry runs:", " ".join("%s/%s/%s:%s:%.0fs:orph%d" % (r["host"], r["unit"], r["arm"], "pass" if r["passed"] else "FAIL", r["wall_s"], r["orphans_alive"]) for r in sorted(dry, key=lambda r: r["start"])))
out["last_end"] = max((r["end"] for r in meas), default=None)
json.dump(out, open(os.path.join(root, "summary.json"), "w"), indent=1)
