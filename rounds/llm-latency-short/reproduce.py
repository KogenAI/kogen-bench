#!/usr/bin/env python3
"""Recalculate short-probe arm counts and quantiles from text-free event logs."""
import collections
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def quantile(values, p):
    values = sorted(value for value in values if value is not None)
    if not values:
        return None
    position = (len(values) - 1) * p
    low, high = math.floor(position), math.ceil(position)
    return values[low] + (values[high] - values[low]) * (position - low)


rows = []
for path in sorted((HERE / "raw").glob("*.jsonl")):
    with path.open() as stream:
        rows.extend(json.loads(line) for line in stream if line.strip())
ends = [row for row in rows if row.get("kind") == "request_end"]
arms = collections.defaultdict(list)
for row in ends:
    arms[(row["model"], row["effort"])].append(row)
completed = lambda row: row.get("completed") and not row.get("aborted") and row.get("returncode") == 0
summary = {
    "attempts": len(ends),
    "uncensored_completed": sum(completed(row) for row in ends),
    "arms": {},
    "errors": dict(collections.Counter(error for row in ends for error in row.get("errors", []))),
    "raw_sha256": {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((HERE / "raw").glob("*.jsonl"))
    },
}
for (model, effort), group in sorted(arms.items()):
    eligible = [row for row in group if completed(row)]
    summary["arms"][f"{model}/{effort}"] = {
        "attempts": len(group),
        "uncensored_completed": len(eligible),
        "first_byte_p50_s": quantile([row.get("first_byte_s") for row in eligible], 0.5),
        "first_byte_p90_s": quantile([row.get("first_byte_s") for row in eligible], 0.9),
        "total_wall_p50_s": quantile([row.get("total_s") for row in eligible], 0.5),
        "total_wall_p90_s": quantile([row.get("total_s") for row in eligible], 0.9),
    }
print(json.dumps(summary, indent=2))
