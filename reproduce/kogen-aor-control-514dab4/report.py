#!/usr/bin/env python3
"""report.py <cells.tsv>: per-task table for the Kogen AoR control cohort (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
def s(rs, k): return sum(int(r[k]) for r in rs)
print(f"cells {len(rows)}: Studio {sum(r['host']=='Studio' for r in rows)}, eu2 {sum(r['host']=='eu2' for r in rows)}, laptop {sum(r['host']=='laptop' for r in rows)}")
print("\ntask\tcells\tvalid_intent\treached_build\tlanded\thidden_all_pass\trequested_all_pass")
for t in sorted({r["task"] for r in rows}):
    rs = [r for r in rows if r["task"] == t]
    print(f"{t}\t{len(rs)}\t{s(rs,'valid_intent')}\t{s(rs,'reached_build')}\t{s(rs,'landed')}\t{s(rs,'hidden_all_pass')}\t{sum(r['requested_passed']==r['requested_total'] for r in rs)}")
print(f"all\t{len(rows)}\t{s(rows,'valid_intent')}\t{s(rows,'reached_build')}\t{s(rows,'landed')}\t{s(rows,'hidden_all_pass')}\t{sum(r['requested_passed']==r['requested_total'] for r in rows)}")
print("\noutcomes:", dict(sorted(collections.Counter(r["outcome"] for r in rows).items())))
for h in ("Studio", "eu2", "laptop"):
    rs = [r for r in rows if r["host"] == h]
    print(f"{h}: valid Intent {s(rs,'valid_intent')}/{len(rs)}, landed {s(rs,'landed')}, hidden all-pass {s(rs,'hidden_all_pass')}")
print(f"\ntokens: input {s(rows,'input_tokens')} (cached {s(rows,'cached_tokens')}), output {s(rows,'output_tokens')}")
print("\nFirst mistake per cell: task host first_mistake")
for r in rows: print(f"{r['task']}\t{r['host']}\t{r['first_mistake']}")
print("\nPer cell: task host hidden requested input output wall_s")
for r in rows: print(f"{r['task']}\t{r['host']}\t{r['hidden_passed']}/{r['hidden_expected']}\t{r['requested_passed']}/{r['requested_total']}\t{r['input_tokens']}\t{r['output_tokens']}\t{r['wall_s']}")
