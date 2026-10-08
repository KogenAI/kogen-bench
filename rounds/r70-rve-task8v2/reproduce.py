#!/usr/bin/env python3
"""Extract R70 task 8 v2 smoke and control rows from public ledgers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream if line.strip()]


smokes = [
    row for row in read_jsonl(ROOT / "results/test-counts.jsonl")
    if row.get("cohort") == "r70-task8-v2-smoke"
]
controls = [
    row for row in read_jsonl(ROOT / "results/controls.jsonl")
    if row.get("cohort") == "r70-task8-v2"
]
print(json.dumps({
    "smokes": [{key: row.get(key) for key in (
        "cell_id", "task", "stack", "outcome", "tests_passed", "tests_total", "scored"
    )} for row in smokes],
    "controls": [{key: row.get(key) for key in (
        "cell_id", "control_type", "outcome", "tests_passed", "tests_total"
    )} for row in controls],
}, indent=2))
