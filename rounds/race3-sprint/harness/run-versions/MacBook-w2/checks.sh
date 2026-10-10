#!/bin/bash
# checks.sh — pre-clock equality gates; log every PASS/FAIL and return failure to start.sh.
R=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$R/out"
/usr/bin/python3 "$R/checks.py" 2>&1 | tee "$R/out/checks.txt"
exit ${PIPESTATUS[0]}
