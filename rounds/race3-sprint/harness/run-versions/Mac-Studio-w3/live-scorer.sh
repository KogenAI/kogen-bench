#!/bin/bash
# live-scorer.sh TARGET PLATEAU_MIN — during the race: score each new arm-snapshot ONE at a time at nice 20 (tag "live", jobs 2) only to decide
# per-arm stops: target reached (excl >= TARGET) or no improvement for PLATEAU_MIN minutes. Official scores are recomputed after the stop.
R=$(cd "$(dirname "$0")" && pwd); TG=${1:-$(sed -n 's/^target=//p' "$R/COUNTS.txt")}; NS=$(sed -n 's/^N_scored=//p' "$R/COUNTS.txt"); PL=${2:-45}; export SCORE_TAG=live SCORE_JOBS=2
done_f=$R/out/live-done.txt; touch $done_f
while [ ! -f $R/STOP ]; do
  for L in $(ls $R/snapshots 2>/dev/null | grep '^T+' | sort); do for A in $(cat $R/ARMS); do
    grep -qx "$L $A" $done_f && continue; [ -f $R/STOP-$A ] && { echo "$L $A" >> $done_f; continue; }
    nice -n 20 $R/score-arm.sh $L $A; echo "$L $A" >> $done_f
    ex=$(awk -F'\t' -v l="$L" -v a="$A" '$1==l && $2==a {split($4,x," "); split(x[2],y,"/"); print y[1]}' $R/out/scores-live.tsv | tail -1)
    m=$((10#$(echo $L | tr -dc 0-9)))
    if [ "${ex:-0}" -ge $TG ]; then echo "$(date -u +%T) $A reached target $ex/$NS at snapshot $L (T+${m}m)" >> $R/out/arms.log; touch $R/STOP-$A; fi
    best=$(awk -F'\t' -v a="$A" -v m=$m '$2==a {n=$1; gsub(/[^0-9]/,"",n); split($4,x," "); split(x[2],y,"/"); if (n+0<=m-'$PL' && y[1]+0>b) b=y[1]+0} END{print b+0}' $R/out/scores-live.tsv)
    cur=$(awk -F'\t' -v a="$A" '$2==a {split($4,x," "); split(x[2],y,"/"); if (y[1]+0>b) b=y[1]+0} END{print b+0}' $R/out/scores-live.tsv)
    if [ $m -ge $PL ] && [ "$cur" -le "$best" ] && [ ! -f $R/STOP-$A ]; then echo "$(date -u +%T) $A plateau: best $cur/$NS not above $best (T+$((m-PL))m) for ${PL}m at $L" >> $R/out/arms.log; touch $R/STOP-$A; fi
  done; done; sleep 20
done
