#!/usr/bin/python3
# A partial result file is a harness failure, not a legitimate zero score.
import json
import os
import sys
from pathlib import Path
from scoring_config import inventory, scored_ids
R = Path(__file__).resolve().parent
rows = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
rows = [row for row in rows if isinstance(row, dict) and row.get('id')]
ids = [row['id'] for row in rows]
selected = os.environ.get('SCORE_CASES')
expected = set(scored_ids(R) if selected else inventory(R))
if selected and set(selected.split(',')) != expected:
    raise SystemExit('FAIL SCORE_CASES must equal the exact frozen scored IDs')
if len(ids) != len(set(ids)) or set(ids) != expected or any(row.get('status') not in ('pass', 'fail', 'error', 'blocked') for row in rows):
    raise SystemExit('FAIL scorer result inventory/status differs from frozen selection')
