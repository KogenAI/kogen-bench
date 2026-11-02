#!/usr/bin/env python3
"""report.py <pairs.tsv>: counters and per-task paired outcomes for the Kogen data-stores screen (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
prim = [r for r in rows if r["task"] == "T1"]; guard = [r for r in rows if r["task"] != "T1"]
def s(rs, k): return sum(int(r[k]) for r in rs)
print(f"pairs {len(rows)}: primary T1 {len(prim)}, guards {len(guard)} on {len({r['task'] for r in guard})} tasks")
for name, rs in (("primary T1", prim), ("guards", guard)):
    print(f"\n{name}: valid Intent g0 {s(rs,'g0_valid_intent')}/{len(rs)}, g1 {s(rs,'g1_valid_intent')}/{len(rs)}")
    print("  g0 outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rs).items())))
    print("  g1 outcomes:", dict(sorted(collections.Counter(r["g1_outcome"] for r in rs).items())))
    print(f"  requested checks passed g0 {s(rs,'g0_requested_passed')}, g1 {s(rs,'g1_requested_passed')}; input tokens g0 {s(rs,'g0_input_tokens')}, g1 {s(rs,'g1_input_tokens')}")
print("\nPer pair: task rep host g0_hidden/expected g1_hidden/expected g0_req g1_req")
for r in rows:
    print(f"{r['task']}\tr{r['rep']}\t{r['host']}\t{r['g0_hidden_passed']}/{r['hidden_expected']}\t{r['g1_hidden_passed']}/{r['hidden_expected']}\t{r['g0_requested_passed']}\t{r['g1_requested_passed']}")
from math import comb
n = len(prim); k = s(prim, "g0_valid_intent") - s(prim, "g1_valid_intent")
print(f"\nPrimary pairs where g0 had a valid Intent and g1 did not: {sum(1 for r in prim if r['g0_valid_intent']=='1' and r['g1_valid_intent']=='0')} of {n}; one-sided exact sign p = {0.5**n:.4f}")
