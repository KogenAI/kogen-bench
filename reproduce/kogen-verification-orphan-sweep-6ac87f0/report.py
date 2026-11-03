#!/usr/bin/env python3
"""report.py <data dir>: rebuilds every count of the orphan-sweep landing check from the three tables (standard library only)."""
import csv, sys, os
d = sys.argv[1]
rd = lambda n: list(csv.DictReader(open(os.path.join(d, n)), delimiter="\t"))
cases, exits, diag = rd("orphan_sweep_cases.tsv"), rd("orphan_sweep_exit_output.tsv"), rd("orphan_sweep_diagnostic.tsv")
for arm in ("control_587f67d", "candidate_6ac87f0"):
    print(f"{arm}: swept {sum(r[arm] == 'swept' for r in cases)} of {len(cases)}")
print("survivors (control / candidate): " + ", ".join(f"{r['case']}" for r in cases if r["control_587f67d"] == "survives" and r["candidate_6ac87f0"] == "survives"))
print(f"cases where the arms differ: {sum(r['control_587f67d'] != r['candidate_6ac87f0'] for r in cases)}")
print(f"exit status and output identical between arms: {sum(r['control_equals_candidate'] == 'yes' for r in exits)} of {len(exits)} commands")
for r in diag:
    print(f"diagnostic ({r['launcher']}): control {r['control_587f67d']}, candidate {r['candidate_6ac87f0']}")
print("pass condition (6 of 6 swept on Linux): " + ("met" if all(r["candidate_6ac87f0"] == "swept" for r in cases) else "NOT met"))
