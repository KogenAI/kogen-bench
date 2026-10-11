#!/bin/bash
# target-watch.sh ARM [--once] — inspect the arm's own results every 10 s; no live scoring; record cumulative tokens at STOP.
set -e
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec /usr/bin/python3 "$R/target_watch.py" --root "${TARGET_WATCH_ROOT:-$R}" "$@"
