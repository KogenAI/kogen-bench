#!/bin/bash
# load.sh prep|start|stop   (Lab C6, Linux host as lanes). The load is Lab E2's replay, reused as written:
# notes-harness/lab-build-speed/e2e3/{e2.py,sched.json,heavy-lab.sh}: 4 concurrent Build streams (stagger 0/15/30/45 s, seeded mix of
# kogen-setup/executor/review/loop/coordinator/verification/shaping suites, each preceded by a go-shim style targeted go test), policy
# arm C (all shared lock, cap 2 large suites = the most concurrent of E2's three policies), looped until stopped (LOOP=1).
. "$(dirname "$0")/env.sh"; E=${E2DIR:-$(cd "$(dirname "$0")" && pwd)}; MIR=$HOME/work.noindex/mirrors; O=$W/out/load
case $1 in
prep) mkdir -p $W/bin; cp $E/e2.py $E/sched.json $E/heavy-lab.sh $W/bin/
  for r in kogen-setup kogen-executor kogen-review kogen-loop kogen-coordinator kogen-verification kogen-shaping; do
    [ -d $W/trees/$r ] || { git clone -q $MIR/$r.git $W/trees/$r && git -C $W/trees/$r checkout -q --detach main 2>/dev/null; }
    (cd $W/trees/$r && go test -count=1 -run XXX_NONE ./... >/dev/null 2>&1; echo "$r warm rc=$?"); done;;
start) mkdir -p $O; rm -f $O/STOP $O/pids.txt; cd $W
  LOOP=1 W=$W setsid nohup python3 $W/bin/e2.py C $W/bin/sched.json $O > $W/out/load.stdout 2>&1 < /dev/null &
  echo $! > $W/out/load.pid; echo "load started pid $(cat $W/out/load.pid)";;
stop) touch $O/STOP
  for p in $(cat $O/pids.txt 2>/dev/null); do ps -o user= -p $p 2>/dev/null | grep -qx "$(id -un)" && kill -s TERM -- -$p 2>/dev/null; done
  [ -f $W/out/load.pid ] && kill -s TERM -- -$(cat $W/out/load.pid) 2>/dev/null; echo stopped;;
esac
