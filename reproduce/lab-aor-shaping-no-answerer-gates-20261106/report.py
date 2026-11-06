#!/usr/bin/env python3
"""report.py: print the tables of this Lab from the data files next to it. No model, no network.
usage: python3 -I report.py [dir containing data/]"""
import json, os, sys
d = os.path.join(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)), "data")
def load(n): return json.load(open(os.path.join(d, n)))
ARMS = ["A", "B1", "B2", "B3", "B"]
print("== recorded refusals replayed through each arm (refused/problems; the recorded count in the last column)")
for r in load("recorded-refusals-replay.json"):
    if "A" not in r: print("%s a%d %-18s (kogen-coordinator lint, not replayed) recorded %d" % (r["tree"], r["attempt"], r["gate"], r["recorded_problems"])); continue
    print("%s a%d %-18s" % (r["tree"], r["attempt"], r["gate"]), " ".join("%s=%s/%d" % (a, "REF" if r[a]["refused"] else "pass", r[a]["problems"]) for a in ARMS), "recorded", r["recorded_problems"])
c = load("refusal-classes.json")
print("== refusal problem lines by gate:class", c["problem_classes"], "totals", c["totals"])
n = load("negative-cases.json")
print("== synthetic cases (refused / accepted per arm)")
for kind, v in n["negative_cases"].items(): print(kind, {a: "%d refused, %d accepted" % (v[a]["refused"], v[a]["accepted"]) for a in ARMS})
for k, v in n["change_cases"].items(): print("  ", k, v)
h = load("heldout.json")
print("== held-out stored Intents:", h["packages"], "packages")
for kind, v in h["by_kind"].items():
    print(kind, "cases", v["cases"], "A accepts", v["A_accepted"], {a: (v[a]["accepted"], "A-accepted-now-refused %d" % v[a]["A_accepted_now_refused"], "A-refused-now-accepted %d" % v[a]["A_refused_now_accepted"]) for a in ARMS[1:]})
print("== fixture", json.dumps(load("fixture.json")))
print("== suite-counts.tsv"); print(open(os.path.join(d, "suite-counts.tsv")).read())
