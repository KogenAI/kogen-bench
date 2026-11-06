#!/usr/bin/env python3
"""report.py: print the tables of this Lab from the data files next to it. No model, no network.
usage: python3 -I report.py [dir containing data/]"""
import json, os, sys
d = os.path.join(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)), "data")
def load(n): return json.load(open(os.path.join(d, n)))
print("== gate replay (recorded decisions of each tree through the decision record gate)")
for arm in "AB":
    rows = load("replay-%s.json" % arm)
    a1 = [r for r in rows if r["Round"] == 1]
    print(arm, "attempt-1 submissions refused:", sum(r["Refused"] for r in a1), "of", len(a1), "| problem lines:", sum(r["Problems"] for r in a1),
          "| refused at any attempt:", sum(r["Refused"] for r in rows), "of", len(rows))
    for r in rows:
        if r["Refused"]: print("   ", r["Slug"], "attempt", r["Round"], dict(r["Kinds"]))
print("== reach replay (attempt-1 package repeated by a stub shaper; stub checkers; real tree)")
for arm in "AB":
    rows = load("reach-%s.json" % arm)
    for r in rows:
        print(arm, r["Slug"], "gates:", ",".join(r["Gates"]), "| readiness_ms:", r["ReadinessMs"], "| acceptance executions:", r["AcceptanceExecs"], "| model calls:", r["ModelCalls"])
    print(arm, "trees where readiness ran:", sum(1 for r in rows if r["AcceptanceExecs"] > 0 or r["ReadinessMs"] > 0), "of", len(rows))
print("== fixture (external shaper, decision cites a URL)")
print(json.dumps(load("fixture.json")))
for n in ("gate-classification.tsv", "approve.tsv", "suite-counts.tsv"):
    print("==", n); print(open(os.path.join(d, n)).read())
