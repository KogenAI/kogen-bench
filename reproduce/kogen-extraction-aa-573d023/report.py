#!/usr/bin/env python3
"""report.py <pairs.tsv>: per-task paired outcomes of the Kogen A/A block (standard library only)."""
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
def s(k): return sum(int(r[k]) for r in rows)
print(f"pairs {len(rows)}")
print(f"valid Intent: g0 {s('g0_valid_intent')}/{len(rows)}, g1 {s('g1_valid_intent')}/{len(rows)}")
print(f"input tokens: g0 {s('g0_input_tokens')}, g1 {s('g1_input_tokens')}; output tokens: g0 {s('g0_output_tokens')}, g1 {s('g1_output_tokens')}")
print("\nPer pair: task g0_outcome g1_outcome g0_hidden/expected g1_hidden/expected")
for r in rows:
    print(f"{r['task']}\t{r['g0_outcome']}\t{r['g1_outcome']}\t{r['g0_hidden_passed']}/{r['hidden_expected']}\t{r['g1_hidden_passed']}/{r['hidden_expected']}")
same = sum(1 for r in rows if r["g0_outcome"] == r["g1_outcome"])
print(f"\nSame outcome class in both arms: {same} of {len(rows)} pairs; hidden all-pass: g0 0/{len(rows)}, g1 0/{len(rows)}")
