#!/bin/bash
R=~/Scratch.noindex/race3-st-w2
while [ $(date +%s) -lt 1791633667 ] && [ ! -f $R/STOP ]; do sleep 0.5; done
$R/snap.sh FINAL > $R/out/final-snap.txt 2>&1
touch $R/STOP; echo "snapshot FINAL then STOP at $(date -u +%T)" >> $R/out/arms.log
pkill -f "$R/snap-loop.sh"; sleep 10; pkill -TERM -f "$R/arm.sh"
for p in $(pgrep -f "codex exec"); do c=$(/usr/sbin/lsof -a -p $p -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); a=$(ps -o args= -p $p); case "$c $a" in *$R/*) kill -TERM $p && echo "stopped codex $p";; esac; done >> $R/out/arms.log
echo "agents stopped at $(date -u +%T)" >> $R/out/arms.log
[ -s $R/locks.tsv ] && $R/unlock.sh > $R/out/unlock.txt 2>&1
left=$(find ~/Areas/Kogen ~/Scratch.noindex -maxdepth 1 -perm 000 2>/dev/null | wc -l | tr -d ' '); echo "dirs left at mode 000 after unlock: $left" >> $R/out/arms.log
/usr/bin/python3 $R/audit.py > $R/out/audit.txt 2>&1
for A in rust go ts gleam ex; do case "$R/$A/target" in "$R/"?*) rm -rf "$R/$A/target";; esac; done
touch $R/DONE; echo "finished at $(date -u +%T) (scoring deferred: run score-all.sh)" >> $R/out/arms.log
