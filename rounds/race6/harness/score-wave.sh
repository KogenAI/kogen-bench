#!/bin/bash
# Deferred offline FINALs and hourly curves; no boundary search.
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd); cd "$R"
source "$R/scoring-common.sh"
[ -f DONE ] && [ -f snapshots/FINAL/SNAPSHOT_COMPLETE ] || { echo 'wave must be DONE with FINAL before scoring' >&2; exit 1; }
python3 "$R/score-admission.py"
mkdir -p out
mkdir out/score-wave.lock || exit 1
trap 'rmdir out/score-wave.lock' EXIT
export PYTHONDONTWRITEBYTECODE=1
python3 "$R/freeze.py" --check
python3 "$R/scoring_config.py" --cases > out/SCORE_CASES.csv
for label in FINAL T+030m; do
  if [ ! -f "snapshots/$label/SNAPSHOT_COMPLETE" ] || find "snapshots/$label" -name PRUNED_BUILD_OUTPUT 2>/dev/null | rg -q .; then
    printf '%s\tunavailable: missing/incomplete/source-only checkpoint\n' "$label" >> out/score-unavailable.tsv
    continue
  fi
  printf '%s\n' $(cat ARMS) | xargs -P "$SCORE_CONCURRENCY" -n 1 /bin/bash -c '
    "$1/score-one.sh" "$2" "$3" > "$1/out/curve-$2-$3.txt"
  ' score "$R" "$label"
done
cp out/scores-combined.tsv out/scores.tsv
python3 "$R/stalls.py" > out/stalls-summary.txt
python3 "$R/metrics.py" > out/metrics-print.txt
printf 'PASS race6 scoring: FINAL, T+030m; concurrency=%s jobs=2\n' "$SCORE_CONCURRENCY"
