#!/bin/bash
# score-fast2.sh HOST — 5 concurrent arm-snapshots (one per arm), --jobs 2 each: phase 1 FINALs, phase 2 time-to-target; curves later
H=$1; X=$(dirname "$0"); S=~/Scratch.noindex; ARMS="rust go ts gleam ex"; export SCORE_JOBS=2
for W in w1 w2 w3; do for A in $ARMS; do echo "$H $W FINAL $A"; done; done | xargs -P 5 -L 1 bash $X/score-one.sh > /dev/null
echo "phase1 done $(date -u +%T) (P5 jobs2)" >> $S/race3-$H-score.log
for W in w1 w2 w3; do : > $S/race3-$H-$W/out/ttt.tsv; done
for A in $ARMS; do echo "$H $A"; done | xargs -P 5 -L 1 bash -c 'for W in w1 w2 w3; do bash '"$X"'/bsearch.sh $0 $W $1; done'
echo "phase2 done $(date -u +%T) (P5 jobs2)" >> $S/race3-$H-score.log
