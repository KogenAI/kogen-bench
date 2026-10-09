#!/usr/bin/env python3
"""Write rounds/rz1/data/cells.csv: one analysis row per scored rz1 cell, from committed public records."""
from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIELDS = [
    "cell_id", "plan_index", "pair_order", "task", "stack", "rep", "outcome", "tests_passed", "tests_total",
    "uncached_input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens", "wall_s",
    "model", "effort", "cli_version", "host", "grade_route", "base_sha",
]


def main() -> int:
    plan = json.loads((HERE / "receipts/PLAN.json").read_text())
    with gzip.open(ROOT / "data/mined/rz1.jsonl.gz", "rt", encoding="utf-8") as stream:
        records = {row["cell_id"]: row for row in (json.loads(line) for line in stream if line.strip())}
    rows = []
    for cell in sorted(plan["cells"], key=lambda c: c["index"]):
        rec = records[cell["cell_id"]]
        grade = rec["official_grade"]
        usage = rec["usage"]
        rows.append({
            "cell_id": cell["cell_id"], "plan_index": cell["index"], "pair_order": cell["pair_order"] + 1,
            "task": rec["task"], "stack": cell["stack"], "rep": rec["rep"], "outcome": grade["outcome"],
            "tests_passed": grade["test_counts"]["tests_passed"], "tests_total": grade["test_counts"]["tests_total"],
            "uncached_input_tokens": usage["input_tokens"], "cached_input_tokens": usage["cached_input_tokens"],
            "output_tokens": usage["output_tokens"], "reasoning_tokens": usage["reasoning_tokens"],
            "wall_s": rec["wall_s"], "model": rec["model"], "effort": rec["effort"], "cli_version": rec["versions"]["cli"],
            "host": "kogen-bench-eu", "grade_route": "r70-macbook-window-v1",
            "base_sha": rec["base_sha"]["base_sha"],
        })
    out = HERE / "data/cells.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
