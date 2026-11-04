#!/usr/bin/env python3
"""report.py [cells.json]: recompute the screen tables and the registered verdict from the published cells."""
import json, statistics, sys
c = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cells.json"))["cells"]
arms = ("no-context", "context-packet")
print("case | rep | no-context outcome, s, input | context-packet outcome, s, input, recall")
for case in dict.fromkeys(x["case"] for x in c):
    for rep in (1, 2):
        a, b = ({x["arm"]: x for x in c if x["case"] == case and x["rep"] == rep}[k] for k in arms)
        print(f"{case} | {rep} | {a['outcome']}, {a['model_seconds']}, {a['input_tokens_uncached']} | {b['outcome']}, {b['model_seconds']}, {b['input_tokens_uncached']}, {b['packet_recall']}")
d = [x for x in c if x["decision"]]
med = {k: statistics.median(x["model_seconds"] for x in d if x["arm"] == k) for k in arms}
tok = {k: sum(x["input_tokens_uncached"] for x in d if x["arm"] == k) for k in arms}
green = lambda o: o.startswith("green")
worse = any(not green(b["outcome"]) and green(a["outcome"]) for case in {x["case"] for x in d} for rep in (1, 2)
            for a in [x for x in d if x["case"] == case and x["rep"] == rep and x["arm"] == arms[0]] for b in [x for x in d if x["case"] == case and x["rep"] == rep and x["arm"] == arms[1]])
loss = any(all(not green(b["outcome"]) and green(a["outcome"]) for rep in (1, 2)
               for a in [x for x in d if x["case"] == case and x["rep"] == rep and x["arm"] == arms[0]] for b in [x for x in d if x["case"] == case and x["rep"] == rep and x["arm"] == arms[1]])
           for case in {x["case"] for x in d})
dt = (med[arms[1]] - med[arms[0]]) / med[arms[0]]; dk = (tok[arms[1]] - tok[arms[0]]) / tok[arms[0]]
print(f"decision cells: median model seconds {med[arms[0]]} -> {med[arms[1]]} ({dt:+.1%}); uncached input tokens {tok[arms[0]]} -> {tok[arms[1]]} ({dk:+.1%})")
print(f"models seen: {sorted({m for x in c for m in x['models']})}; list cost ${sum(x['list_usd'] for x in c):.2f}")
v = "CLEAR LOSS" if loss else ("PROMISING" if not worse and (dt <= -0.15 or dk <= -0.15) else "UNRESOLVED")
print("registered screen rule:", v)
