#!/bin/bash
# lock-macbook.sh — chmod 000 every Kogen implementation/clone, race dir (with earlier arms' code), export archive and Quint tool on the MacBook;
# record modes in this harness dir's locks.tsv for exact restore by unlock.sh. The race3 kit stays readable (agents need its docs/env).
set -e; R=$(cd "$(dirname "$0")" && pwd); L=$R/locks.tsv
if [ "${1:-}" = --test-dir ]; then exec "$R/lock.sh" "$2"; fi
K=$HOME/Areas/Kogen; S=$HOME/retained-run
PYKIT=${RACE5_PY_KIT_DIR:-$S/race5-py-kit}
cand=( $K/kogen $K/kogen-try $K/quint-connect-go $K/kogen-rs $K/kogen-rs-wt $K/kogen-core $K/kogen-spec $K/kogen-spec-wt $K/kogen-conformance $K/kogen-bare $K/kogen-live $K/kogen-loop $K/kogen-desperate $K/kogen-release-v0 $K/codegen_rewrite
       $S/kogen-core $S/kogen-research $S/kogen-remote $S/verify $S/conf-final $S/quint-cli $S/race $S/race-gleam $S/race-export $S/race3-stack-guides $HOME/.kogen )
shopt -s nullglob
for d in $K/codegen-core* $K/kogen-codex* $K/kogen-compare-* $K/kogen-build-* $K/kogen-next-* $K/kogen-direct-* $K/kogen-compact-* $K/kogen-b027-* $K/kogen-context-* $K/kogen-custody-* $K/kogen-local-* $K/kogen-c01-* $K/kogen-opening-* $S/race2* $S/race3-* $S/race4-* $S/race5-* $S/r3-* "$S/suite-v3" "$S/spec-v2" "$S/spec-fast" "$S/race3-v2"; do cand+=("$d"); done
# Same publishing/benchmark exclusions as Studio; skip before checking modes.
B=$K/bench-manager
unique=()
for d in "${cand[@]}"; do
  [ -d "$d" ] || continue
  case "$d" in
    "$R"|"$R"/*|"$PYKIT"|"$PYKIT"/*|"$S/race5-py-kit"|"$S/race5-py-kit"/*|"$S/race5-harness"|"$S/race5-harness"/*|"$S/race4-harness"|"$S/race4-harness"/*|"$S/race3-kit"|"$S/race3-kit"/*|"$S/race3-harness"|"$S/race3-harness"/*|"$B/cx-live"|"$B/cx-live"/*|"$B/cx-jobs/PUB-PUSH"|"$B/cx-jobs/PUB-RTG1-STUDIO-1"|"$B/cx-jobs/CF-FIX"|"$B/cx-jobs/CF-CHECK-STUDIO-1"|"$B/cx-jobs/PUB-RTG1B"|"$B/cx-jobs/PUB-RTG1B-STUDIO-1") continue;;
  esac
  seen=false
  for prior in "${unique[@]}"; do [ "$d" != "$prior" ] || { seen=true; break; }; done
  $seen || unique+=("$d")
done
if [ "${1:-}" = --list ]; then printf '%s\n' "${unique[@]}"; exit 0; fi
[ "$#" -eq 0 ] || { echo 'usage: lock-macbook.sh [--list | --test-dir DIR]' >&2; exit 2; }
: > "$L"
for d in "${unique[@]}"; do
  [ "$(stat -f %Lp "$d")" = 0 ] && { echo "refusing: $d already at mode 000 before locking" >&2; exit 3; }
  "$R/lock.sh" --append "$d"
done
wc -l < "$L"
