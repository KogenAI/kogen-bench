#!/bin/bash
# wave-plan.sh T0_EPOCH MINUTES SNAP_MIN [GAP_MIN] — on THIS host: prepare race3-<host>-w1 and -w2 from this harness, start wave 1 at T0 and
# wave 2 at T0 + MINUTES + GAP (default 10) — the same epochs on both hosts, so each wave starts at the same moment everywhere.
H=$(cd "$(dirname "$0")" && pwd); T0=$1; M=${2:-180}; I=${3:-5}; G=${4:-10}; S=~/Scratch.noindex
host=st; case "$(hostname)" in *MacBook*) host=mb;; esac; ARMS="rust go ts gleam ex"
for w in 1 2; do D=$S/race3-$host-w$w; [ -e "$D" ] && { echo "$D exists"; exit 1; }; mkdir -p $D; cp -c -R $H/. $D/; rm -rf "$D/out" "$D/snapshots" "$D/score-wd"; if [ $host = st ]; then echo ~/.codex-almir > $D/CODEX_HOME; else echo ~/.codex > $D/CODEX_HOME; fi; done
T2=$((T0 + M*60 + G*60)); echo "$(hostname -s) wave1 $(date -u -r $T0 +%T) wave2 $(date -u -r $T2 +%T)" > $S/race3-$host-waves.txt
$S/race3-$host-w1/start.sh $M "$ARMS" $I LOCK $T0 > $S/race3-$host-w1.start.log 2>&1
until [ -f $S/race3-$host-w1/DONE ]; do sleep 5; done
du -sh $S/race3-$host-w1 >> $S/race3-$host-waves.txt; df -h /Users | tail -1 >> $S/race3-$host-waves.txt
$S/race3-$host-w2/start.sh $M "$ARMS" $I LOCK $T2 > $S/race3-$host-w2.start.log 2>&1
until [ -f $S/race3-$host-w2/DONE ]; do sleep 5; done
du -sh $S/race3-$host-w2 >> $S/race3-$host-waves.txt; df -h /Users | tail -1 >> $S/race3-$host-waves.txt
echo "both waves done $(date -u +%T); score with race3-$host-w1/score-all.sh then -w2" >> $S/race3-$host-waves.txt
