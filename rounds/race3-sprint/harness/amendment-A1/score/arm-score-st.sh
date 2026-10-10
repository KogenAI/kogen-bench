#!/bin/bash
S=~/Scratch.noindex; until [ -f $S/race3-st-w3/DONE ]; do sleep 10; done; sleep 5; echo "start $(date -u +%T)" >> $S/race3-st-score.log; bash $S/r3-armfix-v2/score/score-fast.sh st
