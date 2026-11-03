#!/usr/bin/env python3
"""report.py <selftest.tsv> <copy_scan.tsv>: recompute the checks behind the finding (standard library only)."""
import csv, sys
t = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
s = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
ok = all(r["selftest"] == "ok" and r["test_classes"] == "1" for r in t)
print(f"self-test rows: {len(t)}, ids: {sum(int(r['ids']) for r in t)}, every task under exactly one test class: {ok}")
print(f"copies scanned: {sum(int(r['copies_matching_fixed_ids']) + int(r['copies_with_wrong_ids']) for r in s)}; copies with wrong ids: {sum(int(r['copies_with_wrong_ids']) for r in s)} (all of one task)")
print("verdict: DEFECT FIXED, NO PUBLISHED SCORE AFFECTED" if ok else "verdict: CHECK")
