#!/bin/bash
# Phase 2 batch m2d: the recommended brief text (guide-final: exact hook install + always-on brief_seen self-check, re-serve on).
cd "${ROOT:?set ROOT}" || exit 1
export KH=${KH:?set KH} CC_VER=${CC_VER:-2.1.312}
for x in a b c; do ./run-cell2.sh m2-gf-def-$x guide-final 1 4 2 2 resume 1 & done
./run-cell2.sh m2-gf-def-live guide-final 1 4 2 2 live 1 &
for x in a b; do PERM=bypassPermissions ./run-cell2.sh m2-gf-byp-$x guide-final 1 2 1 2 resume 1 & done
PERM=bypassPermissions ./run-cell2.sh m2-gf-byp-live guide-final 1 2 1 2 live 1 &
wait; echo ALLDONE > m2d.done
