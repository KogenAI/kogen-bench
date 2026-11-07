#!/bin/bash
# runs ON eu2 as lanes: l4-run.sh <outdir>
O=$1; mkdir -p $O/src $O/json $O/log; cd $O
export PATH=/usr/local/bin:/usr/bin:/bin GOFLAGS=-mod=mod CI=1
for r in kogen-loop kogen-verification kogen-coordinator kogen-setup kogen-executor kogen-review kogen-shaping kogen-build kogen; do
  [ -e $O/STOP ] && break
  l=$(cut -d' ' -f1 /proc/loadavg); echo "$(date -u +%T) $r start load1=$l" >> $O/log/progress.txt
  rm -rf $O/src/$r; git clone -q --depth 1 https://github.com/KogenAI/$r $O/src/$r || { echo "$r clone failed" >> $O/log/progress.txt; continue; }
  sha=$(git -C $O/src/$r rev-parse HEAD); echo $sha > $O/json/$r.sha
  export GOCACHE=$O/gocache-$r GOMODCACHE=$O/gomod; mkdir -p $GOMODCACHE
  s=$(date +%s.%N)
  ( cd $O/src/$r && timeout 2400 go test -json -count=1 ./... > $O/json/$r.json 2> $O/log/$r.err ); rc=$?
  e=$(date +%s.%N); echo "$r rc=$rc wall=$(echo "$e - $s" | bc) sha=$sha" >> $O/log/progress.txt
  rm -rf $O/gocache-$r $O/src/$r
done
echo "$(date -u +%T) ALL DONE" >> $O/log/progress.txt
