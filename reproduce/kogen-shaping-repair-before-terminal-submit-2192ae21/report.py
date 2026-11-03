#!/usr/bin/env python3
"""Recompute the paired-screen summary from sanitized cell-level results."""
import csv
from pathlib import Path
p=Path(__file__).parent/'data'/'paired-results.tsv'
rows=list(csv.DictReader(p.open(), delimiter='\t'))
complete=[r for r in rows if r['control_intent']!='not_run']
print('task	control intent/outcome/hidden	candidate intent/outcome/hidden')
for r in complete:
    print(f"{r['task']}\t{r['control_intent']}/{r['control_outcome']}/{r['control_hidden']}\t{r['candidate_intent']}/{r['candidate_outcome']}/{r['candidate_hidden']}")
for a in ('control','candidate'):
    print(f"{a}: valid Intent {sum(r[a+'_intent']=='yes' for r in complete)}/{len(complete)}; landed {sum(r[a+'_outcome']=='landed' for r in complete)}/{len(complete)}; hidden all-pass {sum(r[a+'_all_pass']=='yes' for r in complete)}/{len(complete)}")
print('unrun pairs:', ', '.join(r['task'] for r in rows if r['control_intent']=='not_run'))
print('acceptance separation: unknown for every pair')
