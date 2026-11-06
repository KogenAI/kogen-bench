#!/usr/bin/env python3
"""report.py: print the tables of this Lab from the data files next to it. No model, no network.
usage: python3 -I report.py [dir containing data/]"""
import json, os, sys
d = os.path.join(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)), "data")
def load(n): return json.load(open(os.path.join(d, n)))
BOUND = 524288
print("== bytes per class of the scope estimate (recorded attempt-1 package of each tree)")
bd = load("breakdown.json")
for t, r in bd.items():
    print(t, "estimate", r["estimate"], "(gate measured: %s)" % r["gate_measured_estimate"], "| package", r["package_bytes"], "%.1f%%" % (100 * r["package_share"]),
          "| named files", r["named_files"], r["named_bytes"], "%.1f%%" % (100 * r["named_share"]))
    for k, v in sorted(r["classes"].items(), key=lambda x: -x[1]):
        print("    %-24s %8d  %5.1f%%" % (k, v, 100 * v / r["estimate"]))
    print("    largest class:", r["largest_class"], "%.1f%%" % (100 * r["largest_share"]), "| repeated package lines", r["package_repeat_line_bytes"],
          "| package lines also in the tree", r["package_lines_also_in_head_bytes"], "| package gzip", r["package_gzip_bytes"])
print("== what remains if a class is measured once (bound %d)" % BOUND)
for t, r in bd.items():
    print(t, {k: (v, "fits" if v <= BOUND else "over") for k, v in r["remaining"].items()}, "| gate estimate:", "fits" if r["estimate"] <= BOUND else "over")
print("== reach replay (attempt-1 package repeated by a stub shaper; stub checkers; real tree; no model)")
reach = load("reach.json")
for arm, rows in reach.items():
    for t, r in rows.items():
        g = []
        for x in r["gates"]:
            if x not in g: g.append(x)
        print(arm, t, "first gate:", ",".join(g), "| problems:", r["problems_by_gate"], "| readiness_ms:", r["readiness_ms"], "| acceptance executions:", r["acceptance_executions"], "| model calls:", r["model_calls"])
    print(arm, "trees where readiness ran:", sum(1 for r in rows.values() if r["acceptance_executions"] > 0 or r["readiness_ms"] > 0), "of", len(rows),
          "| trees past the scope gate:", sum(1 for r in rows.values() if r["gates"] and r["gates"][0] not in ("decision_record", "scope")), "of", len(rows))
print("== synthetic packages through the scope gate")
for arm, rows in load("synthetic.json").items():
    for r in rows: print(arm, "%-40s refused=%s package=%d" % (r["Case"], r["Refused"], r["PackageB"]))
for n in ("suite-counts.tsv",):
    p = os.path.join(d, n)
    if os.path.exists(p): print("==", n); print(open(p).read())
