#!/usr/bin/env python3
"""Recalculate the original R70 RvE outcome counts from public ledgers."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream if line.strip()]


grades = [
    row for row in read_jsonl(ROOT / "results/test-counts.jsonl")
    if row.get("cohort") == "r70-original-rve"
]
resources = [
    row for row in read_jsonl(ROOT / "results/cost-time.jsonl")
    if row.get("cohort") == "r70-original-rve"
]
by_stack = collections.defaultdict(list)
for row in grades:
    by_stack[row["stack"]].append(row)

print(json.dumps({
    "cohort": "r70-original-rve",
    "graded_n": len(grades),
    "outcomes": {
        stack: {
            "pass": sum(row["outcome"] == "pass" for row in rows),
            "n": len(rows),
            "cell_ids": sorted(row["cell_id"] for row in rows),
        }
        for stack, rows in sorted(by_stack.items())
    },
    "resource_rows": len(resources),
    "resource_stacks": sorted({row["stack"] for row in resources}),
}, indent=2))
