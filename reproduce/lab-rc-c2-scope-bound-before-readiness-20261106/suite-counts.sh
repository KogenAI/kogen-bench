#!/bin/sh
# suite-counts.sh <go test -v output file>: pass, fail and skip lines (subtests included) and the failing test names
f="$1"
echo "pass $(grep -cE '^[[:space:]]*--- PASS' "$f") fail $(grep -cE '^[[:space:]]*--- FAIL' "$f") skip $(grep -cE '^[[:space:]]*--- SKIP' "$f")"
grep -E '^--- FAIL' "$f" | sed 's/ (.*//'
