#!/bin/bash
# Phase 2 batch m2a (run as the runner user in the scratch root). run-cell2.sh <name> <mode> <reserve> <K> <P> <Q> <drive> <tools>
cd "${ROOT:?set ROOT}" || exit 1
export KH=${KH:?set KH} CC_VER=${CC_VER:-2.1.312}
./run-cell2.sh m2-hash-a       hash      0 4 2 2 resume 0 &
./run-cell2.sh m2-hash-b       hash      0 4 2 2 resume 0 &
./run-cell2.sh m2-nonce-a      nonce     0 4 2 2 resume 0 &
./run-cell2.sh m2-nonce-b      nonce     0 4 2 2 resume 0 &
./run-cell2.sh m2-rolling-a    rolling   0 4 2 2 resume 0 &
./run-cell2.sh m2-rolling-b    rolling   0 4 2 2 resume 0 &
./run-cell2.sh m2-self-a       selfcheck 0 4 2 2 resume 0 &
./run-cell2.sh m2-self-b       selfcheck 0 4 2 2 resume 0 &
./run-cell2.sh m2-self-live    selfcheck 0 4 2 2 live   0 &
./run-cell2.sh m2-self-steady  selfcheck 0 2 10 2 resume 0 &   # 10 steady calls before the first compaction (false alarms)
PERM=bypassPermissions ./run-cell2.sh p2dry-gs-byp      guide-short 0 1 1 1 resume 1 &
PERM=bypassPermissions ./run-cell2.sh p2dry-ge-byp-live guide-exact 0 1 1 1 live   1 &
wait
echo ALLDONE > m2a.done
