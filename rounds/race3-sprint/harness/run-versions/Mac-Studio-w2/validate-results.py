#!/usr/bin/python3
# A partial result file is a harness failure, not a legitimate zero score.
import json
import sys
from pathlib import Path
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R / 'inputs/conformance'))
from kogen_conformance.runner import load_cases

rows = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
rows = [row for row in rows if row.get('id')]
ids = [row['id'] for row in rows]
expected = {row['id'] for row in load_cases()}
if len(ids) != len(set(ids)) or set(ids) != expected or any(row.get('status') not in ('pass', 'fail', 'error', 'blocked') for row in rows):
    raise SystemExit('FAIL scorer result inventory/status differs from frozen suite')
