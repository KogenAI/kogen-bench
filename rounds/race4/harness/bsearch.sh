#!/bin/bash
# bsearch.sh ARM — local binary search + S−5 guard using per-snapshot both-pass scores.
set -e
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec /usr/bin/python3 "$R/bsearch.py" "$1"
