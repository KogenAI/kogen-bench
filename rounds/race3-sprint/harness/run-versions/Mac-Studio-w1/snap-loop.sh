#!/bin/bash
# snap-loop.sh INTERVAL_MIN — snapshots only (no scoring during the race) every INTERVAL minutes until the deadline
R=$(cd "$(dirname "$0")" && pwd); I=$1; S=$(cat $R/START); DL=$(cat $R/DEADLINE); m=$I
while :; do t=$((S+m*60)); [ $t -ge $DL ] && break; while [ $(date +%s) -lt $t ]; do sleep 1; [ -f $R/STOP ] && exit 0; done; $R/snap.sh "T+$(printf %03d $m)m" >> $R/out/snap-loop.log 2>&1; m=$((m+I)); done
