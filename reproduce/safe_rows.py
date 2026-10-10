#!/usr/bin/env python3
"""Print grade/result rows with hidden-suite content removed.

Standing rule (2026-10-08, after the env-blocks exposure, see
kogen-bench-sot/tasks/CONTAMINATION-LOG.md): any inspection of grade rows,
grade windows, run records or COMPLETE/manifest JSON that may carry hidden-suite
fields goes through this helper (CLI) or sanitize() (import). Never cat, grep,
jq, head or tail those files directly.

CLI:   python3 levers/lib/safe_rows.py FILE.jsonl|FILE.json [--keys k1,k2] [--last N]
Import: sys.path.insert(0, ".../levers/lib"); from safe_rows import sanitize, load_rows
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Keys whose values can carry hidden test names, test output or grader text.
HIDDEN_KEY = re.compile(
    r"(test_names|failing|^tail$|_tail$|failure_summary|stdout|stderr|hidden_output|test_output|failed_tests|passed_tests)",
    re.IGNORECASE,
)
REDACTED = "<hidden-suite field removed by safe_rows>"


def sanitize(obj):
    """Return a deep copy with every hidden-suite key's value replaced."""
    if isinstance(obj, dict):
        return {k: (REDACTED if HIDDEN_KEY.search(str(k)) else sanitize(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return obj


def load_rows(path: str) -> list:
    with open(path, errors="replace") as fh:
        text = fh.read()
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    rows.append({"unparsed_line_chars": len(line)})
        return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path")
    ap.add_argument("--keys", help="comma-separated top-level keys to keep (after sanitizing)")
    ap.add_argument("--last", type=int, help="only the last N rows")
    a = ap.parse_args()
    rows = load_rows(a.path)
    if a.last:
        rows = rows[-a.last:]
    keep = [k for k in (a.keys or "").split(",") if k]
    for row in rows:
        row = sanitize(row)
        if keep and isinstance(row, dict):
            row = {k: row.get(k) for k in keep}
        print(json.dumps(row, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
