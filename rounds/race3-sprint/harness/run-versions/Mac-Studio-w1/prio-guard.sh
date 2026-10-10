#!/bin/bash
# prio-guard.sh RACE_DIR — after priority.sh: for each arm's first>=target snapshot S, also score S-5m and S-10m (if not yet scored); result stays provisional
R=$1; cd $R || exit 1; P=$R/out/priority.tsv; T=$(sed -n 's/^target=//p' COUNTS.txt)
until grep -q '^priority done' $P; do sleep 15; done
score(){ SCORE_TAG=prio ./score-arm.sh "$1" "$2" >/dev/null 2>&1; l=$(tail -1 out/scores-prio.tsv); s=$(echo "$l" | cut -f4 | awk '{print $2}' | cut -d/ -f1); printf '%s\t%s\t%s\t%s\t%s\tguard\n' "$2" "$1" "$s" "$(echo "$l" | cut -f3)" "$(date -u +%T)" >> $P; }
for A in $(cat ARMS); do
  S=$(awk -F'\t' -v a=$A '$1==a && $2=="RESULT" {print $3}' $P | sed -n 's/.* at T+0*\([0-9]*\)m$/\1/p'); [ -z "$S" ] && continue
  for d in 5 10; do m=$((S-d)); [ $m -lt 5 ] && continue; L=$(printf 'T+%03dm' $m); awk -F'\t' -v a=$A -v l=$L '$1==a && $2==l' $P | grep -q . || score $L $A; done
done
echo "guard done $(date -u +%T)" >> $P
