#!/usr/bin/env python3
"""report.py <cells.tsv> [<first-cohort cells.tsv>]: per-task table for the second Kogen AoR Claude Code ceiling block, and the pool with the first block (standard library only)."""
import csv, sys, collections
def load(p): return list(csv.DictReader(open(p), delimiter="\t"))
def s(rs, k): return sum(int(r[k]) for r in rs)
def table(rows, title):
    print(f"{title}: cells {len(rows)}, H1 {sum(r['host']=='H1' for r in rows)}, H2 {sum(r['host']=='H2' for r in rows)}")
    print("task\tcells\tvalid_intent\treached_build\tlanded\thidden_all_pass\trequested_all_pass")
    for t in sorted({r["task"] for r in rows}):
        rs = [r for r in rows if r["task"] == t]
        print(f"{t}\t{len(rs)}\t{s(rs,'valid_intent')}\t{s(rs,'reached_build')}\t{s(rs,'landed')}\t{s(rs,'hidden_all_pass')}\t{sum(r['requested_passed']==r['requested_total'] for r in rs)}")
    print(f"all\t{len(rows)}\t{s(rows,'valid_intent')}\t{s(rows,'reached_build')}\t{s(rows,'landed')}\t{s(rows,'hidden_all_pass')}\t{sum(r['requested_passed']==r['requested_total'] for r in rows)}")
    print("outcomes:", dict(sorted(collections.Counter(r["outcome"] for r in rows).items())))
    print()
rows = load(sys.argv[1])
table(rows, "second block (r2)")
for h in ("H1", "H2"):
    rs = [r for r in rows if r["host"] == h]
    print(f"{h}: valid Intent {s(rs,'valid_intent')}/{len(rs)}, landed {s(rs,'landed')}, hidden all-pass {s(rs,'hidden_all_pass')}")
print(f"\ntokens: input {s(rows,'input_tokens')} (cached {s(rows,'cached_tokens')}), output {s(rows,'output_tokens')} (the timed-out cell has no token totals and counts 0)")
print("\nFirst mistake per cell: task host first_mistake")
for r in rows: print(f"{r['task']}\t{r['host']}\t{r['first_mistake']}")
print("\nPer cell: task host hidden requested input output wall_s")
for r in rows: print(f"{r['task']}\t{r['host']}\t{r['hidden_passed']}/{r['hidden_expected']}\t{r['requested_passed']}/{r['requested_total']}\t{r['input_tokens']}\t{r['output_tokens']}\t{r['wall_s']}")
if len(sys.argv) > 2:
    print()
    table(load(sys.argv[2]) + rows, "pooled with the first block (dd593dd3), two hosts, EU's separate run not included")
