#!/bin/bash
# score-phase2.sh HOST — wait for phase-1 xargs to finish, then time-to-target per wave (w2, w3, w1), 5 arms concurrently, jobs 2
H=$1; X=$(dirname "$0"); S=~/Scratch.noindex; export SCORE_JOBS=2
while pgrep -f "xargs -P 5 -L 1 bash $X/score-one.sh" >/dev/null; do sleep 5; done
echo "phase1 done $(date -u +%T) (P5 jobs2)" >> $S/race3-$H-score.log
for W in w2 w3 w1; do : > $S/race3-$H-$W/out/ttt.tsv
  for A in rust go ts gleam ex; do echo "$H $W $A"; done | xargs -P 5 -L 1 bash $X/bsearch.sh
  echo "phase2 $W done $(date -u +%T)" >> $S/race3-$H-score.log
done
