#!/bin/bash
# Phase 2 batch m2b: guidance arms (run as the runner user in the scratch root). run-cell2.sh <name> <mode> <reserve> <K> <P> <Q> <drive> <tools>
cd "${ROOT:?set ROOT}" || exit 1
export KH=${KH:?set KH} CC_VER=${CC_VER:-2.1.312}
B=bypassPermissions
for x in a b c; do
  PERM=$B ./run-cell2.sh m2-gs-byp-$x      guide-short 0 2 1 2 resume 1 &
  PERM=$B ./run-cell2.sh m2-ge-byp-$x      guide-exact 0 2 1 2 resume 1 &
done
for x in a b; do
  PERM=$B ./run-cell2.sh m2-gs-byp-live-$x guide-short 0 2 1 2 live 1 &
  PERM=$B ./run-cell2.sh m2-ge-byp-live-$x guide-exact 0 2 1 2 live 1 &
  ./run-cell2.sh m2-gs-def-$x guide-short 0 2 1 2 resume 1 &      # client default permissions: the install is denied
done
wait
echo ALLDONE > m2b.done
