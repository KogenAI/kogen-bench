#!/bin/bash
# priority.sh RACE_DIR — FINAL first, then binary search for the first 5-min snapshot with scored >= target (one arm-snapshot at a time)
R=$1; cd $R || exit 1; T=$(sed -n 's/^target=//p' COUNTS.txt); P=$R/out/priority.tsv; : > $P
LABELS=($(ls snapshots | grep '^T+' | sort)); n=${#LABELS[@]}
score(){ SCORE_TAG=prio ./score-arm.sh "$1" "$2" >/dev/null 2>&1; l=$(tail -1 out/scores-prio.tsv); s=$(echo "$l" | cut -f4 | awk '{print $2}' | cut -d/ -f1); a=$(echo "$l" | cut -f3); printf '%s\t%s\t%s\t%s\t%s\n' "$2" "$1" "$s" "$a" "$(date -u +%T)" >> $P; echo $s; }
for A in $(cat ARMS); do
  f=$(score FINAL $A)
  if [ "${f:-0}" -lt "$T" ]; then printf '%s\tRESULT\tnot reached (FINAL %s/56)\n' $A "$f" >> $P; continue; fi
  lo=0; hi=$n; first=FINAL   # invariant: LABELS[hi] (or FINAL) >= T
  while [ $lo -lt $hi ]; do mid=$(( (lo+hi)/2 )); s=$(score ${LABELS[$mid]} $A); if [ "${s:-0}" -ge "$T" ]; then hi=$mid; first=${LABELS[$mid]}; else lo=$((mid+1)); fi; done
  printf '%s\tRESULT\tfirst>=%s at %s\n' $A "$T" "$first" >> $P
done
echo "priority done $(date -u +%T)" >> $P
