#!/usr/bin/env python3
"""Per-run outcome table from the three measured runs' ledger.jsonl files (arm / fixture / outcome x count)."""
import collections, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = [
    ("measure (network denied)", "evidence/measure-20261015T110330Z-b54eb3"),
    ("measure-net (network open)", "evidence/net/measure-net-20261015T114336Z-fe90bc"),
    ("measure-native3 (network open)", "evidence/net/measure-native3-20261015T121425Z-3cb851"),
]
for label, run in RUNS:
    cells = collections.defaultdict(collections.Counter)
    for line in open(os.path.join(HERE, run, "ledger.jsonl"), encoding="utf-8"):
        e = json.loads(line)
        if e["event"] != "complete" or e["outcome"] == "SAMPLE":
            continue
        arm, fixture, _rep = e["key"].split("/")
        cells[(arm, fixture)][e["outcome"]] += 1
    print(f"== {label}: {run}")
    for (arm, fixture), c in sorted(cells.items()):
        print(f"{arm:42s} {fixture:22s} " + ", ".join(f"{o} x{n}" for o, n in sorted(c.items())))
    total = collections.Counter(o for c in cells.values() for o in c.elements())
    print("total " + ", ".join(f"{o} {n}" for o, n in sorted(total.items())) + "\n")
