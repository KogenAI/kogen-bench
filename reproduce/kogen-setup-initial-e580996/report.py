#!/usr/bin/env python3
"""report.py <init_source_hashes.tsv> <file_compare.tsv>: recompute the checks behind the finding (standard library only)."""
import csv, sys
h = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
f = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
same = all(r["adopted_94eabe5"] == r["head_d69a0a3"] == h[0]["adopted_94eabe5"] for r in h)
print(f"init source hashes: {len(h)} rows, all equal: {same}, lines {h[0]['lines']}")
logic = [r for r in f if r["model_visible"].startswith("yes")]
print(f"model-visible files compared: {len(logic)}; identical to adopted: {sum(r['vs_adopted_94eabe5'] == 'identical' for r in logic)}")
tests = [r for r in f if r["model_visible"].startswith("no")]
print(f"test-only files: {len(tests)}; differing from adopted: {sum(r['vs_adopted_94eabe5'] != 'identical' for r in tests)} (all test fixtures, never sent to a model)")
print("verdict: SAME (pure move)" if same and all(r["vs_adopted_94eabe5"] == "identical" for r in logic) else "verdict: CHECK")
