#!/bin/sh
# 1-task dry (both arms) first; the round starts only if both dry cells reached grading. Timestamped harness copy: events-arrival.jsonl per cell.
R=${LANES_PRIVATE:-$HOME/lanes-work}/bare-runs
sh lanes-bare-ts.sh batch shelltail-dry.json --run-dir $R/shelltail-dry --slots 1 > $R/shelltail-dry.log 2>&1
n=$(find $R/shelltail-dry -name evaluation.json | wc -l | tr -d " ")
[ "$n" = 2 ] || { echo "dry incomplete: $n/2 graded" >> $R/shelltail-dry.log; exit 1; }
sh lanes-bare-ts.sh batch shelltail-hard.json --run-dir $R/shelltail-hard --slots 1 > $R/shelltail-hard.log 2>&1
exec sh lanes-bare-ts.sh batch shelltail-broad.json --run-dir $R/shelltail-broad --slots 1 > $R/shelltail-broad.log 2>&1
