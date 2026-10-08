#!/usr/bin/env python3
"""Rebuild the three published L3b pilot records from sanitized source records."""

from __future__ import annotations

import json
from pathlib import Path

from missing_reasons import compact_value, load_marker_to_code


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reproduce/inputs/l3b-pilot-records.jsonl"
OUTPUT = ROOT / "rounds/l3b-repair-vs-continue/records.jsonl"
ROUND = "l3b-repair-vs-continue"


def main() -> None:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [row.get("cell_id") for row in rows]
    if (len(rows) != 3 or len(set(ids)) != 3 or any(not isinstance(cid, str) or not cid for cid in ids)
            or any(row.get("round_id") != ROUND or row.get("audit_round") != ROUND
                   or row.get("schema_version") != "1.1" for row in rows)):
        raise ValueError("Expected three distinct L3b schema 1.1 pilot source records")
    marker_to_code = load_marker_to_code()
    for row in rows:
        row["schema_version"] = "1.2"
    compact = [compact_value(row, marker_to_code) for row in rows]
    OUTPUT.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in compact),
        encoding="utf-8",
    )
    print(f"{ROUND}: wrote {len(compact)} Standard 1.2 records")


if __name__ == "__main__":
    main()
