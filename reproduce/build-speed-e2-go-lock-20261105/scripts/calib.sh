#!/bin/sh
# solo calibration on a quiet EU: warm run (build cache) then timed run per repo. usage: calib.sh <repo>...  (W set)
export PATH=$HOME/.local/share/mise/installs/node/24.21.0/bin:$HOME/.local/share/mise/installs/go/1.27.2/bin:/usr/local/bin:/usr/bin:/bin
export GOCACHE=$W/gocache GOMODCACHE=$W/gomod TMPDIR=$W/tmp GOTOOLCHAIN=local
mkdir -p $W/calib
for r in "$@"; do
  cd $W/trees/$r || exit 1
  for rep in warm timed; do
    d0=$(sh $W/bin/gate.sh count); s=$(date +%s.%N); GOFLAGS="-trimpath -count=1" go test ./... > $W/calib/$r.$rep.out 2>&1; rc=$?; e=$(date +%s.%N)
    echo "$r $rep rc=$rc secs=$(echo "$e - $s" | bc) load=$(cut -d' ' -f1 /proc/loadavg) deliv_before=$d0 deliv_after=$(sh $W/bin/gate.sh count)" | tee -a $W/calib/calib.log
    [ $rc -ne 0 ] && [ $rep = warm ] && { echo "$r red on warm run, skipping timed" | tee -a $W/calib/calib.log; break; }
  done
done
