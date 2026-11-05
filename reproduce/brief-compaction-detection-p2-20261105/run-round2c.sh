#!/bin/bash
# Phase 2 batch m2c: self-check with re-serve, so every compaction (not only the first) can be flagged.
cd "${ROOT:?set ROOT}" || exit 1
export KH=${KH:?set KH} CC_VER=${CC_VER:-2.1.312}
./run-cell2.sh m2-self2-rs-a      selfcheck2 1 4 2 2 resume 0 &
./run-cell2.sh m2-self2-rs-b      selfcheck2 1 4 2 2 resume 0 &
./run-cell2.sh m2-self2-rs-live   selfcheck2 1 4 2 2 live   0 &
./run-cell2.sh m2-self-rs-a       selfcheck  1 4 2 2 resume 0 &
./run-cell2.sh m2-self2-rs-steady selfcheck2 1 2 10 2 resume 0 &
wait
echo ALLDONE > m2c.done
