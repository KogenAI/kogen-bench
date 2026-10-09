#!/usr/bin/env python3
"""Classify kept control grader logs by error class without printing any log content.

Usage: classify-control-logs.py KEEP_DIR
Reads KEEP_DIR/<task>/<variant>/grader.log (written when KOGEN_CONTROLS_KEEP is set) and prints one JSON line
per log with error-class line counts and the class of the first error line. Raw lines, test names and
test output are never printed: grader logs can contain hidden-suite content.
"""
import json
import re
import sys
from pathlib import Path

CLASSES = [  # order matters for first-error classification: most specific first
    ("dependency_resolution", r"failed to download|no matching package|offline|could not resolve|unable to fetch|"
                              r"failed to fetch|missing go\.sum|cannot find module|could not find dependency|"
                              r"enotfound|eai_again|failed to select a version|registry|hex\.pm|dependency .* not"),
    ("toolchain_missing", r"command not found|no such file or directory.*\b(cargo|go|mix|bun|node|elixir|erl|gleam|zig|python3?)\b|"
                          r"toolchain .* (not installed|is not installed)|rustup could not"),
    ("permission", r"permission denied|eacces|operation not permitted|read-only file system"),
    ("infra", r"timed? ?out|killed|out of memory|no space left|cannot allocate|bwrap:"),
    ("build", r"error\[e\d{4}\]|could not compile|compilation error|compileerror|build failed|syntaxerror|"
              r"cannot find (type|value|function)|undefined (function|variable|reference)"),
    ("test", r"\bfailed\b|failures?:|assertionerror|assert(ion)? (error|failed)|\bfail\b"),
]
COMPILED = [(name, re.compile(rx, re.IGNORECASE)) for name, rx in CLASSES]


def classify(path: Path) -> dict:
    counts = {name: 0 for name, _ in CLASSES}
    first = None
    for line in path.read_text(errors="replace").splitlines():
        for name, rx in COMPILED:
            if rx.search(line):
                counts[name] += 1
                first = first or name
                break
    return {"counts": counts, "first_error_class": first or "none"}


def main() -> int:
    keep = Path(sys.argv[1])
    for log in sorted(keep.glob("*/*/grader.log")):
        task, variant = log.parent.parent.name, log.parent.name
        print(json.dumps({"task": task, "variant": variant, **classify(log)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
