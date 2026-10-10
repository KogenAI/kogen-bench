#!/bin/bash
# gate-dry.sh HOST — exact w2/w3 pre-start gate (setup-arms.sh + checks.sh) on a scratch copy with the v2 files applied; no lock, no agents
H=$1; S=~/Scratch.noindex; G=$S/r3-gate-dry-$H; V=$S/r3armfix
[ -e "$G" ] && { echo "$G exists"; exit 1; }
rsync -a --exclude '/rust' --exclude '/go' --exclude '/ts' --exclude '/gleam' --exclude '/ex' --exclude '/out' --exclude '/snapshots' --exclude '/score-wd' \
  --exclude '/START' --exclude '/DEADLINE' --exclude '/DONE' --exclude '/STOP*' --exclude '/locks.tsv' --exclude '/arm.sh.fixed' --exclude '/arm-cont.sh' --exclude '/deploy.sh' \
  $S/race3-$H-w1/ $G/
cp $S/r3-armfix-v2/arm.sh $S/r3-armfix-v2/arm-cont.sh $S/r3-armfix-v2/DECISION-RULE-A1.md $G/
cd $G && mkdir -p out && echo "rust go ts gleam ex" > ARMS && ./setup-arms.sh > out/setup.txt && ./checks.sh; rc=$?
echo "GATE rc=$rc host=$(hostname -s)"; grep -E "^(PASS|FAIL)" out/checks.txt 2>/dev/null | tr '\n' ' '; echo
