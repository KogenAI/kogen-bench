#!/bin/sh
# drive.sh: unattended E2 (arms A,B,C) then E3 on EU as lanes. Every batch waits for a quiet host (gate.sh) and NEVER starts on a busy host:
# the gate is retried until it passes or the deadline (epoch in $R/deadline) is reached, in which case that batch is skipped and logged.
W=$HOME/work.noindex/scratch/research/work/build-speed-e2e3; R=$HOME/work.noindex/scratch/research/runs/build-speed-e2e3
export W; B=$W/bin; mkdir -p $R/e2 $R/e3; echo $$ > $R/drive.pid
log() { echo "$(date +%s) $(date -u +%T) $*" >> $R/drive.log; }
waitq() { # waitq <label> <deadline_epoch>
  while :; do
    [ "$(date +%s)" -gt "$2" ] && { log "deadline-$1"; return 1; }
    g=$(sh $B/gate.sh quiet 300) && { log "gate-$1 $g"; return 0; }
  done; }
DL_E2=$(cat $R/deadline-e2); DL_E3=$(cat $R/deadline-e3)
while pgrep -f "bin/calib.sh" >/dev/null; do sleep 10; done; log calib-finished
rm -f $R/mon.stop; sh $B/mon.sh $R/overlap.log $R/mon.stop & mpid=$!
cat > $B/calib2.sh <<'EOS'
export PATH=$HOME/.local/share/mise/installs/node/24.21.0/bin:$HOME/.local/share/mise/installs/go/1.27.2/bin:/usr/local/bin:/usr/bin:/bin
export GOCACHE=$W/gocache GOMODCACHE=$W/gomod TMPDIR=$W/tmp GOTOOLCHAIN=local
for r in "$@"; do
  cd $W/trees/$r; d0=$(sh $W/bin/gate.sh count); s=$(date +%s.%N); GOFLAGS="-trimpath -count=1" go test ./... > $W/calib/$r.solo.out 2>&1; rc=$?; e=$(date +%s.%N)
  echo "$r timed rc=$rc secs=$(echo "$e - $s" | bc) load=$(cut -d' ' -f1 /proc/loadavg) deliv_before=$d0 deliv_after=$(sh $W/bin/gate.sh count)" >> $W/calib/calib2.log
done
EOS
# solo recalibration of the small suites and verification (shaping excluded: red solo on EU, E3 uses -skip)
if waitq calib2 $DL_E2; then log start-calib2; sh $B/calib2.sh kogen-review kogen-setup kogen-executor kogen-coordinator kogen-loop kogen-verification; log end-calib2; fi
A_OK=
for arm in A B C; do
  [ "$arm" != A ] && [ -z "$A_OK" ] && continue
  case $arm in A) DL=$DL_E2;; B) DL=$((DL_E2+720));; C) DL=$((DL_E2+1440));; esac
  if waitq $arm $DL; then log "start-$arm"; python3 $B/e2.py $arm $B/sched.json $R/e2/$arm > $R/e2/$arm.stdout 2>&1; log "end-$arm rc=$? $(tail -1 $R/e2/$arm.stdout)"; [ "$arm" = A ] && A_OK=1; fi
done
log e2-finished
if [ -z "$NO_E3" ]; then if waitq e3 $DL_E3; then python3 $B/e3.py $B/e3-items.json $B/sched.json $R/e3 3 0 > $R/e3.stdout 2>&1; log "e3-finished rc=$?"; fi; fi
touch $R/mon.stop; log all-finished; touch $R/DRIVE-DONE
