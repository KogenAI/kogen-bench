#!/bin/sh
R=${LANES_RUNS:-$HOME/bare-runs}
sh lanes/bare/lanes-bare.sh batch h2h-28-dry.json --run-dir $R/h2h-28-dry --slots 1 > $R/h2h-28-dry.log 2>&1
[ "$(find $R/h2h-28-dry -name evaluation.json | wc -l | tr -d " ")" = 1 ] || exit 1
exec sh lanes/bare/lanes-bare.sh batch h2h-28.json --run-dir $R/h2h-28 --slots 1 > $R/h2h-28.log 2>&1
