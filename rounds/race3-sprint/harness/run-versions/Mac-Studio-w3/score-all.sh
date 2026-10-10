#!/bin/bash
# score-all.sh — after the race: score every snapshot of this race dir, one arm-snapshot at a time (warm-up + race 2 scorer config), then metrics and stalls
set -e
R=$(cd "$(dirname "$0")" && pwd); s0=$(date +%s)
mkdir -p "$R/out"
: > "$R/out/scores.tsv"; : > "$R/out/scores-official.tsv"; : > "$R/out/scores-repeat.tsv"; : > "$R/out/scores-regrade.tsv"
for D in "$R"/snapshots/*; do
  [ -d "$D" ] || continue; L=$(basename "$D"); [ "$L" = FINAL ] && continue
  for A in $(cat "$R/ARMS"); do
    SCORE_TAG= "$R/score-arm.sh" "$L" "$A"
    if PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - "$R" <<'PYCODE'
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from scoring_config import counts
root=Path(sys.argv[1]);values,_=counts(root)
fields=(root/'out/scores.tsv').read_text().splitlines()[-1].split('\t')
passed=int(fields[3].split()[1].split('/')[0])
sys.exit(not (values['target']-3 <= passed <= values['target']+3))
PYCODE
    then SCORE_TAG=repeat "$R/score-arm.sh" "$L" "$A"; fi
  done
done
cp "$R/out/scores.tsv" "$R/out/scores-checkpoints.tsv"
for A in $(cat "$R/ARMS"); do
  SCORE_TAG=official "$R/score-arm.sh" FINAL "$A"
  SCORE_TAG=repeat "$R/score-arm.sh" FINAL "$A"
  T=$(mktemp -d "$R/.regrade.XXXXXX")
  /usr/bin/python3 "$R/clean-copy.py" "$R/snapshots/FINAL/$A" "$T/$A"
  SCORE_SOURCE="$T/$A" SCORE_TAG=regrade "$R/score-arm.sh" FINAL "$A"
  rm -rf "$T"
done
/usr/bin/python3 "$R/compare-scores.py"
echo "scoring took $(( $(date +%s)-s0 ))s" >> $R/out/arms.log
/usr/bin/python3 $R/stalls.py > $R/out/stalls-summary.txt 2>&1; /usr/bin/python3 $R/metrics.py > $R/out/metrics-print.txt 2>&1
echo "scored at $(date -u +%T)" >> $R/out/arms.log
