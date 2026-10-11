#!/bin/bash
# Local snapshot helper; conditional double scoring, at most SCORE_CONCURRENCY arms.
set -e
set -o pipefail
R=$(cd "$(dirname "$0")" && pwd); L=${1:?label required}
source "$R/scoring-common.sh"
[ -f "$R/DONE" ] || { echo 'wave must be DONE before scoring' >&2; exit 1; }
for A in $(cat "$R/ARMS"); do
  [ ! -d "$R/snapshots/$L/$A" ] || printf '%s\n' "$A"
done | xargs -P "$SCORE_CONCURRENCY" -n 1 /bin/bash -c '
  "$1/score-one.sh" "$2" "$3"
' score-snapshot "$R" "$L"
