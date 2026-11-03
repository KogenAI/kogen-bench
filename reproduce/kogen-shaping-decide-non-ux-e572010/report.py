#!/usr/bin/env python3
"""report.py <compared_tasks.tsv> <stops.tsv>: recompute the per-task differences and the registered reading (standard library only)."""
import csv, sys
t = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
s = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
d1, d2 = [], []
for r in t:
    c, v = int(r["candidate_cells"]), int(r["valid_intents"])
    ok, n, to = int(r["stored_ok"]), int(r["stored_cells"]), int(r["stored_approval_timeouts"])
    a = v / c - ok / n
    b = v / c - ok / (n - to)
    d1.append(a); d2.append(b)
    print(f"task {r['task']}: candidate {v}/{c}, stored {ok}/{n}, d {a:+.2f}, d without stored approval timeouts {b:+.2f}")
m1, m2 = sum(d1) / len(d1), sum(d2) / len(d2)
print(f"mean d {m1:+.2f}; without stored approval timeouts {m2:+.2f}; lowest task d {min(d1):+.2f}")
rule = "BETTER" if m1 >= 0.15 and m2 >= 0.15 and min(d1) > -0.34 else "other"
print(f"registered rule reading: {rule}")
h = [r for r in s if r["group"] == "held_out_tasks"][0]
print(f"held-out tasks: {h['cells']} cells, {h['valid_intents']} valid Intents")
print("published verdict: TENTATIVE (effect of the change unresolved)")
