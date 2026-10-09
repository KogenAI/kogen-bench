#!/usr/bin/env python3
"""Sanitize one instrumented grade stream before any row is retained."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "bench/hc01-grade-counts"))
from safe_rows import sanitize  # noqa: E402

KEEP = ("id", "task", "outcome", "pass_", "counts", "grader", "started")


def main() -> int:
    if len(sys.argv) != 3:
        return 2
    src, dst = map(Path, sys.argv[1:])
    with src.open("r", errors="replace") as source, dst.open("w") as target:
        for line in source:
            if not line.strip():
                continue
            try:
                row = sanitize(json.loads(line))
            except Exception:
                sys.stderr.write("instrumented grade row could not be parsed\n")
                return 3
            target.write(json.dumps({key: row[key] for key in KEEP if key in row}, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
