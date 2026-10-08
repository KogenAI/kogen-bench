#!/usr/bin/env python3
"""Recalculate long-probe request summaries from a text-free event log."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = []
for path in sorted((HERE / "raw").glob("round2-eu-*.jsonl")):
    with path.open() as stream:
        rows.extend(json.loads(line) for line in stream if line.strip())
ends = [row for row in rows if row.get("kind") == "request_end"]
completed = [
    row for row in ends
    if row.get("completed") and not row.get("aborted") and row.get("returncode") == 0
]
idles_over_90 = sum(any(gap > 90 for gap in row.get("idle_gaps_s", [])) for row in ends)
walls = [row["total_s"] for row in completed]
first_bytes = [row.get("first_byte_s") for row in ends if row.get("first_byte_s") is not None]
first_items = [row.get("first_model_event_s") for row in completed if row.get("first_model_event_s") is not None]
summary = {
    "attempts": len(ends),
    "uncensored_completed": len(completed),
    "errors": dict(collections.Counter(error for row in ends for error in row.get("errors", []))),
    "completed_wall_min_s": min(walls) if walls else None,
    "completed_wall_max_s": max(walls) if walls else None,
    "completed_requests_with_idle_gap_over_90s": sum(
        any(gap > 90 for gap in row.get("idle_gaps_s", [])) for row in completed
    ),
    "all_attempts_with_idle_gap_over_90s": idles_over_90,
    "first_stdout_byte_max_s": max(first_bytes) if first_bytes else None,
    "first_model_visible_item_min_s": min(first_items) if first_items else None,
    "first_model_visible_item_max_s": max(first_items) if first_items else None,
    "completed_walls_at_least_600s": sum(value >= 600 for value in walls),
    "completed_walls_at_least_1200s": sum(value >= 1200 for value in walls),
    "raw_sha256": {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((HERE / "raw").glob("round2-eu-*.jsonl"))
    },
}
print(json.dumps(summary, indent=2))
