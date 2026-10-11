#!/bin/bash
# score-wave.sh — all FINALs, then official time-to-target; SCORE_CONCURRENCY=3, --jobs 2.
set -e
set -o pipefail
R=$(cd "$(dirname "$0")" && pwd); cd "$R"
source "$R/scoring-common.sh"
[ -f DONE ] || { echo 'wave must be DONE before scoring' >&2; exit 1; }
mkdir -p out
LOCK=$R/out/score-wave.lock
mkdir "$LOCK" 2>/dev/null || { echo 'score-wave already running' >&2; exit 1; }
trap 'rmdir "$LOCK"' EXIT
export PYTHONDONTWRITEBYTECODE=1
/usr/bin/python3 "$R/scoring_config.py" --cases > "$R/out/SCORE_CASES.csv"
# Every FINAL (including a required second scoring) completes before the searches.
if ! printf '%s\n' $(cat ARMS) | xargs -P "$SCORE_CONCURRENCY" -n 1 /bin/bash -c '
  "$1/score-one.sh" FINAL "$2" > "$1/out/final-$2.txt"
' score-final "$R"; then echo 'FAIL FINAL scoring' >&2; exit 1; fi
: > out/ttt.tsv
if ! printf '%s\n' $(cat ARMS) | xargs -P "$SCORE_CONCURRENCY" -n 1 /bin/bash -c '
  "$1/bsearch.sh" "$2" > "$1/out/bsearch-$2.log" 2>&1
' score-search "$R"; then echo 'FAIL boundary scoring' >&2; exit 1; fi
/usr/bin/python3 "$R/compare-scores.py"
/usr/bin/python3 "$R/stalls.py" > out/stalls-summary.txt
/usr/bin/python3 "$R/metrics.py" > out/metrics-print.txt
printf 'PASS wave scoring completed %s (concurrency=%s, jobs=2)\n' "$(date -u +%FT%TZ)" "$SCORE_CONCURRENCY"
