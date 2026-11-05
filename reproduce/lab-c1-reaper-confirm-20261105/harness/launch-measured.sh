#!/bin/bash
# Lab C1 confirmation: measured plan, then DRIVER-DONE. usage: launch-measured.sh <work> <cfg> <runs>
W=$1; cfg=$2; runs=$3
G=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["gobin"])' $cfg); N=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["nodebin"])' $cfg)
export PATH=$G:$N:/usr/local/bin:/usr/bin:/bin GOTOOLCHAIN=local GOCACHE=$W/gocache TMPDIR=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tmp"])' $cfg) npm_config_cache=$W/npmcache
unset GOFLAGS
echo "$(date -u +%FT%TZ) measured start"
bash $W/harness/driver-confirm.sh $cfg $W/plan-measured.txt $runs
echo "$(date -u +%FT%TZ) measured end" 
date -u +%FT%TZ > $runs/DRIVER-DONE
