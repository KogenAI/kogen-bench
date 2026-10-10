#!/bin/bash
# bsearch.sh HOST W ARM — first snapshot >= target (binary search + S-5/S-10 guard; repeat-score S and S-5 when within target±3)
H=$1; W=$2; A=$3; X=$(dirname "$0"); R=~/Scratch.noindex/race3-$H-$W; T=$(sed -n 's/^target=//p' $R/COUNTS.txt); O=$R/out/ttt.tsv
f=$($X/score-one.sh $H $W FINAL $A)
if [ "${f:-0}" -lt "$T" ]; then printf '%s\t%s\tnot reached\tFINAL=%s\n' $W $A "$f" >> $O; exit 0; fi
LABELS=($(ls $R/snapshots | grep '^T+' | sort)); lo=0; hi=${#LABELS[@]}; first=FINAL
while [ $lo -lt $hi ]; do mid=$(( (lo+hi)/2 )); s=$($X/score-one.sh $H $W ${LABELS[$mid]} $A); if [ "${s:-0}" -ge "$T" ]; then hi=$mid; first=${LABELS[$mid]}; else lo=$((mid+1)); fi; done
m=$(echo $first | sed -n 's/^T+0*\([0-9]*\)m$/\1/p'); guard=""
if [ -n "$m" ]; then for d in 5; do k=$((m-d)); [ $k -lt 5 ] && continue; L=$(printf 'T+%03dm' $k); s=$($X/score-one.sh $H $W $L $A); guard="$guard $L=$s"; [ "${s:-0}" -ge "$T" ] && first=$L; done; fi
rep=""; for L in $(case $first in (T+*) echo $first;; esac) $( [ -n "$m" ] && printf 'T+%03dm' $(( $(echo $first | sed -n 's/^T+0*\([0-9]*\)m$/\1/p')-5 )) ); do s=$($X/score-one.sh $H $W $L $A); [ "${s:-0}" -ge $((T-3)) ] && [ "${s:-0}" -le $((T+3)) ] && rep="$rep $L:$s/$($X/score-one.sh $H $W $L $A rep)"; done
printf '%s\t%s\tfirst>=%s at %s\tFINAL=%s\tguard:%s\trepeat:%s\n' $W $A $T "$first" "$f" "$guard" "$rep" >> $O
