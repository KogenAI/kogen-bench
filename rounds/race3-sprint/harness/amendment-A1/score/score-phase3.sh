#!/bin/bash
# score-phase3.sh HOST — full /56 curves: every T+ snapshot of every arm in w1..w3 (cached ones skipped), 5 concurrent, jobs 2
H=$1; X=$(dirname "$0"); S=~/Scratch.noindex; export SCORE_JOBS=2
for W in w1 w2 w3; do for L in $(ls $S/race3-$H-$W/snapshots | grep '^T+'); do for A in rust go ts gleam ex; do echo "$H $W $L $A"; done; done; done | xargs -P 5 -L 1 bash $X/score-one.sh > /dev/null
echo "phase3 done $(date -u +%T)" >> $S/race3-$H-score.log
