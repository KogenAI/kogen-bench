#!/bin/bash
# score-one.sh LABEL ARM [official|repeat] — raw first + conditional second; return both-pass official count.
set -e
set -o pipefail
R=$(cd "$(dirname "$0")" && pwd); cd "$R"
L=${1:?label required}; A=${2:?arm required}; TAG=${3:-official}
case "$L $A" in *[!A-Za-z0-9+_\ -]*) echo 'invalid score arguments' >&2; exit 2;; esac
case "$TAG" in official|repeat) ;; *) echo 'tag must be official or repeat' >&2; exit 2;; esac
source "$R/scoring-common.sh"
export PYTHONDONTWRITEBYTECODE=1
T=$(/usr/bin/python3 "$R/scoring_config.py" | sed -n 's/^target=//p')
mkdir -p "$R/out"
LOCK=$R/out/score-lock-$L-$A
until mkdir "$LOCK" 2>/dev/null; do sleep 0.1; done
trap 'score_pool_release; rmdir "$LOCK"' EXIT
score_pool_acquire
cached() {
  if [ -f "$R/out/scores-$1.tsv" ]; then
    awk -F'\t' -v l="$L" -v a="$A" -v t="$1" '$1==l && $2==a && $6==t' "$R/out/scores-$1.tsv" | tail -1
  fi
}
run_raw() {
  local row
  row=$(cached "$1")
  if [ -z "$row" ]; then
    export SCORE_TAG=$1
    if [ "$L" != FINAL ]; then
      SCORE_CASES=$(/usr/bin/python3 "$R/scoring_config.py" --cases); export SCORE_CASES
    else unset SCORE_CASES; fi
    "$R/score-arm.sh" "$L" "$A" > "$R/out/score-$L-$A-$1.log" 2>&1 || return "$?"
    row=$(cached "$1")
  fi
  [ -n "$row" ] || { echo 'scorer produced no score row' >&2; exit 1; }
  echo "$row" | cut -f4 | awk '{print $2}' | cut -d/ -f1
}
first=$(run_raw official)
near=0
if [ "$first" -ge "$((T-3))" ] && [ "$first" -le "$((T+3))" ]; then
  near=1
  second=$(run_raw repeat)
fi
if [ "$TAG" = repeat ] && [ "$near" = 0 ]; then
  echo 'second scoring is only required within target±3' >&2; exit 2
fi
combined=$(/usr/bin/python3 "$R/combined_score.py" "$R" "$L" "$A")
if [ "$TAG" = repeat ]; then echo "$second"; else echo "$combined"; fi
