#!/bin/bash
# driver.sh <setup_min> <quiet_min> <load_min>   (Lab C6, Linux host as lanes, detached; pid file W/out/driver.pid)
# Phases, each with its own deadline so a short host window still yields a balanced prefix:
#   1 setup  : load prep (clones + warm of the E2 load trees), then one test binary per tree in priority order R01 G01 R02 G02 ...
#   2 quiet  : wait for no delivery process (<= 10 min, then go on and record it), probes at level quiet, then the mutation tree
#   3 load   : E2 replay started, 120 s ramp, probes at level load, then the mutation tree, load stopped
. "$(dirname "$0")/env.sh"; H=$(cd "$(dirname "$0")" && pwd); SM=$1; QM=$2; LM=$3; S=$(date +%s); O=$W/out; echo $$ > $O/driver.pid
log() { echo "$(date -u +%FT%TZ) $*" >> $O/driver.log; }
order="R01 G01 R02 G02 R03 G03 R04 G04 R05 G05 R06 G06 R07 G07 R08 G08 R09 G09 R10 G10 R11 G11 R12 G12 G13 G14 G15 G16 G17 G18 G19 G20"
log "start setup=${SM}m quiet=${QM}m load=${LM}m"
bash $H/load.sh prep >> $O/load-prep.log 2>&1; log "load prep done"
for l in $order; do [ $(date +%s) -gt $((S+SM*60)) ] && { log "setup deadline at $l"; break; }; bash $H/host-setup.sh $H/trees.tsv $H/budget_allow_test.go $l; done
built=""; for l in $order; do awk -F'\t' -v l=$l '$1==l && ($8=="OK"||$8=="NO_ARM_A"){f=1} END{exit !f}' $O/setup.tsv 2>/dev/null && built="$built $l"; done
log "built:$built"
g1=$(echo $built | tr " " "\n" | grep "^G" | head -1); M=""
if [ -n "$g1" ]; then bash $H/mutate.sh $g1 >> $O/mutate.log 2>&1 && M=$g1-M01; fi; log "mutation tree: ${M:-none}"
t1=$(date +%s)
sh $H/gate.sh quiet 600 >> $O/gate.log 2>&1; log "gate: $(tail -1 $O/gate.log)"
python3 $H/run-probes.py $W quiet 3 $((t1+QM*60)) $built >> $O/probes.log 2>&1; log "quiet probes: $(tail -1 $O/probes.log)"
[ -n "$M" ] && python3 $H/run-probes.py $W quiet 3 $(( $(date +%s)+300 )) $M >> $O/probes.log 2>&1
bash $H/load.sh start >> $O/load.log 2>&1; sleep 120; log "load running, load1 $(cut -d' ' -f1 /proc/loadavg)"
python3 $H/run-probes.py $W load 3 $(( $(date +%s)+LM*60 )) $built >> $O/probes.log 2>&1; log "load probes: $(tail -1 $O/probes.log)"
[ -n "$M" ] && python3 $H/run-probes.py $W load 3 $(( $(date +%s)+300 )) $M >> $O/probes.log 2>&1
bash $H/load.sh stop >> $O/load.log 2>&1; log "load stopped"; touch $O/DRIVER-DONE; log done
