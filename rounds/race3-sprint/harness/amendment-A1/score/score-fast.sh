#!/bin/bash
# score-fast.sh HOST — phase 1: all FINALs (3 concurrent); phase 2: time-to-target per arm per wave (3 concurrent); phase 3: full curves (3 concurrent)
H=$1; X=$(dirname "$0"); S=~/Scratch.noindex; ARMS="rust go ts gleam ex"
for W in w1 w2 w3; do : > $S/race3-$H-$W/out/ttt.tsv; done
for W in w1 w2 w3; do for A in $ARMS; do echo "$H $W FINAL $A"; done; done | xargs -P 3 -L 1 bash $X/score-one.sh > /dev/null
echo "phase1 done $(date -u +%T)" >> $S/race3-$H-score.log
for W in w1 w2 w3; do for A in $ARMS; do echo "$H $W $A"; done; done | xargs -P 3 -L 1 bash $X/bsearch.sh
echo "phase2 done $(date -u +%T)" >> $S/race3-$H-score.log
for W in w1 w2 w3; do for L in $(ls $S/race3-$H-$W/snapshots | grep '^T+'); do for A in $ARMS; do echo "$H $W $L $A"; done; done; done | xargs -P 3 -L 1 bash $X/score-one.sh > /dev/null
echo "phase3 done $(date -u +%T)" >> $S/race3-$H-score.log
