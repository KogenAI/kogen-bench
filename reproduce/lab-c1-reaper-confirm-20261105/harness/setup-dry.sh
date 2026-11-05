#!/bin/bash
# Lab C1 confirmation: setup + warm compile + one dry run per arm (run under the lm host lock). usage: setup-dry.sh <work> <cfg> <runs>
W=$1; cfg=$2; runs=$3
G=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["gobin"])' $cfg); N=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["nodebin"])' $cfg)
export PATH=$G:$N:/usr/local/bin:/usr/bin:/bin GOTOOLCHAIN=local GOCACHE=$W/gocache TMPDIR=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tmp"])' $cfg) npm_config_cache=$W/npmcache
unset GOFLAGS
echo "$(date -u +%FT%TZ) setup start"
for r in kogen-shaping kogen-verification; do (cd $W/src/$r && npm ci --prefix testdata/tools/cucumber >/dev/null 2>&1 && npm ci --prefix testdata/tools/quint >/dev/null 2>&1 && echo "$r npm ok" || echo "$r npm FAILED"); done
(cd $W/src/kogen-loop && go mod download && echo "loop mod ok")
for r in kogen-shaping kogen-verification; do (cd $W/src/$r && GOFLAGS=-trimpath go test -count=1 -run '^$' ./... >/dev/null 2>&1; echo "$r warm rc=$?"); done
(cd $W/src/kogen-loop && go test -count=1 -run '^$' ./... >/dev/null 2>&1; echo "loop warm rc=$?")
for d in kv-a kv-b; do (cd $W/src/$d && go test -count=1 -run '^$' ./verify/ >/dev/null 2>&1; echo "$d warm rc=$?"); done
echo "$(date -u +%FT%TZ) setup done"
bash $W/harness/driver-confirm.sh $cfg $W/plan-dry.txt $runs
echo "$(date -u +%FT%TZ) dry done" 
