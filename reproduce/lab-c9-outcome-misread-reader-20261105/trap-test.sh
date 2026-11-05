#!/bin/sh
# trap-test.sh <dir> <reader>: six scenarios with a fake 3 s "build" that prints a step line and, at the end, "landed".
D=$1; R=$2; cd "$D" || exit 1
FAKE='echo "step build 00:00:00Z"; sleep 3; echo "landed fake-slug 1224076f (Build x)"; exit 0'
FAILING='echo "step build 00:00:00Z"; sleep 1; echo "candidate/build_blocked: x"; exit 1'
rm -f A.log B.log C.log D.log E.log F.log
# A: current wrapper, no signal (success)
( sh -c "$FAKE" > A.log 2>&1; echo EXIT=$? >> A.log ) </dev/null & wait
# B: current wrapper, TERM to the subshell mid-build: EXIT lost, child survives and lands
( sh -c "$FAKE" > B.log 2>&1; echo EXIT=$? >> B.log ) </dev/null & p=$!; sleep 1; kill -s TERM $p; sleep 4
# C: new wrapper, success
sh ./run-with-exit.sh C.log sh -c "$FAKE" </dev/null & wait
# D: new wrapper, TERM mid-build: EXIT=143 written, child stopped (no landed line)
sh ./run-with-exit.sh D.log sh -c "$FAKE" </dev/null & p=$!; sleep 1; kill -s TERM $p; wait $p 2>/dev/null; sleep 3
# E: new wrapper, KILL mid-build (untrappable): no EXIT; child survives and lands -> reader (b)
sh ./run-with-exit.sh E.log sh -c "$FAKE" </dev/null & p=$!; sleep 1; kill -s KILL $p; sleep 4
# F: new wrapper, failing build: EXIT=1 and a structured stop
sh ./run-with-exit.sh F.log sh -c "$FAILING" </dev/null & wait
for f in A B C D E F; do printf '%s: ' $f; python3 -I "$R" $f.log | cut -f2-4,6; done
for f in A B C D E F; do printf '%s EXIT lines: ' $f; grep -c '^EXIT=' $f.log; done
