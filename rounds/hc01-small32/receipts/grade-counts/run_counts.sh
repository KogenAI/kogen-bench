#!/bin/bash
set -uo pipefail
if [ "$#" -ne 3 ]; then
  echo "usage: run_counts.sh JOBS.json FIFO SAFE.jsonl" >&2
  exit 2
fi
JOBS="$1"; FIFO="$2"; SAFE="$3"
D="$HOME/bench/hc01-grade-counts"
rm -f "$FIFO" "$SAFE"
mkfifo -m 600 "$FIFO" || exit 3
python3 "$D/filter_stream.py" "$FIFO" "$SAFE" &
FILTER_PID=$!
python3 "$D/night_grade_counts.py" "$JOBS" "$FIFO"
GRADE_RC=$?
if [ "$GRADE_RC" -ne 0 ]; then
  kill "$FILTER_PID" >/dev/null 2>&1 || true
fi
wait "$FILTER_PID"
FILTER_RC=$?
rm -f "$FIFO"
if [ "$GRADE_RC" -ne 0 ]; then exit "$GRADE_RC"; fi
exit "$FILTER_RC"
