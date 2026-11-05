#!/bin/bash
# run-linux.sh [setup]: the Linux conditions of Lab L1, from an empty work directory on a 4-core Linux host (needs go, git, python3).
# Arms A and B (B = the clock-at-setup-1 test change, see README), quiet then fixed load, 10 rounds x 30 runs per arm each; then the pre-setup probe.
set -u
W=${W:-$PWD}; cd "$W" || exit 1
R=https://github.com/KogenAI
if [ "${1:-}" = setup ]; then
  git clone -q $R/kogen-verification kv && git -C kv checkout -q ec39831718deb42a60af26e1e8a9b06a763e1258
  cp -R kv kv-b   # now change kv-b/verify/wall_time_test.go as described under Arms (B)
  cp -R kv kv-p   # now add the probe log line described under Arms (probe)
  git clone -q $R/kogen-build kb && git -C kb checkout -q 956b151a6564
  exit 0
fi
for i in $(seq 1 60); do awk '{exit !($2<1)}' /proc/loadavg && break; sleep 10; done
bash chunks.sh linuxquiet 10 30 out-quiet kv kv-b
( cd kv-p && go test -v -run '^TestWallTimeDeadlineAndNeverStarted$' -count=300 ./verify ) > probe-quiet.out 2>&1
( while [ ! -e STOPLOAD ]; do (cd kb && go test -count=1 ./... >/dev/null 2>&1); done ) & lp=$!
sleep 240
bash chunks.sh linuxload 10 30 out-load kv kv-b
( cd kv-p && go test -v -run '^TestWallTimeDeadlineAndNeverStarted$' -count=300 ./verify ) > probe-load.out 2>&1
touch STOPLOAD; wait $lp
