#!/bin/sh
# dry cell per arm first; the screen starts only if every dry cell reached grading
R=${LANES_RUNS:-$HOME/bare-runs}
sh lanes/bare/lanes-bare.sh batch h2h-25-dry.json --run-dir $R/h2h-25-dry --slots 3 > $R/h2h-25-dry.log 2>&1
n=$(find $R/h2h-25-dry -name evaluation.json | wc -l | tr -d " ")
[ "$n" = 6 ] || { echo "dry incomplete: $n/6 graded" >> $R/h2h-25-dry.log; exit 1; }
exec sh lanes/bare/lanes-bare.sh batch h2h-25.json --run-dir $R/h2h-25 --slots 4 > $R/h2h-25.log 2>&1
