#!/usr/bin/env python3
"""report.py <pairs.tsv>: paired counts for the Kogen data-stores follow-up (standard library only)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
def clean(rs): return [r for r in rs if r["pair_status"] == "clean"]
def hid(r, k): return None if r[k] == "NA" else int(r[k])
print(f"pairs {len(rows)}: clean {len(clean(rows))}, void (first-arm gate timeout) {len(rows) - len(clean(rows))}")
groups = [("first pack (eu2, laptop)", [r for r in rows if r["block"] == "first-pack"]),
          ("Studio, first run", [r for r in rows if r["block"] == "studio-st2"]),
          ("Studio, rerun of the two voids", [r for r in rows if r["block"] == "studio-st2-rerun"]),
          ("Studio, all", [r for r in rows if r["block"].startswith("studio")]),
          ("pooled (all hosts)", rows)]
for name, rs in groups:
    c = clean(rs)
    print(f"\n{name}: clean pairs {len(c)}")
    print(f"  valid Intent g0 {sum(int(r['g0_valid_intent']) for r in c)}/{len(c)}, g1 {sum(int(r['g1_valid_intent']) for r in c)}/{len(c)}")
    print("  g0 outcomes:", dict(sorted(collections.Counter(r["g0_outcome"] for r in rs).items())))
    print("  g1 outcomes (every g1 cell, voided pairs included):", dict(sorted(collections.Counter(r["g1_outcome"] for r in rs).items())))
    h0 = [hid(r, "g0_hidden_passed") for r in c]; g = [x for x in h0 if x is not None]
    print(f"  hidden all-pass g0 {sum(x == int(c[i]['hidden_expected']) for i, x in enumerate(h0) if x is not None)}/{len(g)} graded (not graded {len(h0) - len(g)}), g1 {sum(int(r['g1_hidden_passed']) == int(r['hidden_expected']) for r in c)}/{len(c)}")
    k = sum(1 for r in c if r["g0_valid_intent"] == "1" and r["g1_valid_intent"] == "0")
    print(f"  pairs where g0 had a valid Intent and g1 did not: {k} of {len(c)}; one-sided exact sign p = {0.5 ** len(c) if k == len(c) and c else float('nan'):.4f}")
print("\nPer pair: pair status g0_outcome g1_outcome g0_hidden g1_hidden (of expected) g0_requested g1_requested")
for r in rows:
    print(f"{r['pair']}\t{r['pair_status']}\t{r['g0_outcome']}\t{r['g1_outcome']}\t{r['g0_hidden_passed']}\t{r['g1_hidden_passed']}/{r['hidden_expected']}\t{r['g0_requested_passed']}\t{r['g1_requested_passed']}")
s = [r for r in rows if r["block"].startswith("studio")]
print(f"\nStudio input tokens (every cell, voids included): g0 {sum(int(r['g0_input_tokens']) for r in s)}, g1 {sum(int(r['g1_input_tokens']) for r in s)}")
