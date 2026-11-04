#!/usr/bin/env python3
"""Recount the per-task screen data without model calls."""
import json
from collections import Counter
from pathlib import Path
rows=json.loads((Path(__file__).parent/'data'/'results.json').read_text())
for arm in ('baseline-1','baseline-2','candidate'):
 for group in ('intent','questions'):
  r=[x for x in rows if x['arm']==arm and x['group']==group]
  valid=sum(x['valid_intent'] for x in r); landed=sum(x['landed'] for x in r)
  graded=sum(x['grade_complete'] for x in r); passed=sum(x['hidden_all_pass'] is True for x in r)
  print(f'{arm:10s} {group:9s} n={len(r)} valid={valid} landed={landed} hidden_all_pass={passed}/{graded} stops={dict(Counter(x["outcome"] for x in r))}')
