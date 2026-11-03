#!/usr/bin/env python3
"""report.py <review_counts.tsv> <path_table.tsv>: recompute the counts and checks behind the finding (standard library only)."""
import csv, sys
c = {r["measure"]: int(r["value"]) for r in csv.DictReader(open(sys.argv[1]), delimiter="\t")}
paths = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
print(f"reviews {c['reviews']}: approve {c['verdict_approve']}, changes {c['verdict_changes']}, sum {c['verdict_approve'] + c['verdict_changes']}")
print(f"findings {c['findings']}, blocking {c['findings_blocking']}")
print(f"blocking findings matching the no-defect pattern: old check {c['blocking_matching_no_defect_pattern_old']}, new check {c['blocking_matching_no_defect_pattern_new']}")
print(f"blocking findings where old and new differ: {c['blocking_where_old_and_new_differ']} of {c['findings_blocking']}")
print(f"review-material events in parts mode: {c['review_material_mode_parts']} of {c['review_material_events']}")
print(f"rejected verdicts: {c['rejected_verdicts_total']} of {c['reviews']} reviews (allowance events {c['review_allowance_events']}, rejected in them {c['review_allowance_rejected_verdicts']}, invalid outcomes {c['review_invalid_outcomes']})")
print(f"paths that change behaviour: {sum(r['changed'] == 'yes' for r in paths)} of {len(paths)}; in parts mode (the default): {sum(r['changed'] == 'yes' and r['mode'] == 'parts' for r in paths)}")
ok = c["verdict_approve"] + c["verdict_changes"] == c["reviews"] and c["blocking_where_old_and_new_differ"] == 0
print("verdict: SAME on the retained data" if ok else "verdict: CHECK")
