#!/bin/bash
# lock-studio.sh — chmod 000 agreed Studio candidates; record modes for exact restore.
set -e
R=$(cd "$(dirname "$0")" && pwd); L=$R/locks.tsv
list=false
case "${1:-}" in
  --list) list=true; shift ;;
  --test-dir) exec "$R/lock.sh" "$2" ;;
  "") ;;
  *) echo "usage: lock-studio.sh [--list | --test-dir DIR]" >&2; exit 2 ;;
esac
[ "$#" -eq 0 ] || { echo "usage: lock-studio.sh [--list | --test-dir DIR]" >&2; exit 2; }
K=$HOME/Areas/Kogen; S=$HOME/retained-run
PYKIT=${RACE5_PY_KIT_DIR:-$S/race5-py-kit}
cand=( "$K/kogen" "$K/kogen-rs" "$K/kogen-spec" "$K/bench-held" "$K/research-2026-10-08" "$K/webstack-bench" "$S/build-research" "$S/worktrees" "$S/shared" "$S/race3-inputs-check" $HOME/.kogen )
B=$K/bench-manager
for d in "$B/core4" "$B/core4b" "$B/ksub" "$B/shape1" "$B/rz1-pack" "$B/b7" "$B/b9-deps" "$B/rounds" "$B/maclane" "$B/us-rebuild" "$B/vms"; do cand+=("$d"); done
# Include hidden immediate directories too; publishing names match exactly.
shopt -s nullglob dotglob
for d in "$B/cx-jobs"/*; do
  [ -d "$d" ] || continue
  case "${d##*/}" in
    PUB-PUSH|PUB-RTG1-STUDIO-1|CF-FIX|CF-CHECK-STUDIO-1|PUB-RTG1B|PUB-RTG1B-STUDIO-1) continue ;;
  esac
  cand+=("$d")
done
shopt -u dotglob
for d in "$K"/kogen-bench-* "$K"/quint-connect* "$S"/race3-* "$S"/race4-* "$S"/race5-* "$S"/r3-* "$S/suite-v3" "$S/spec-v2" "$S/spec-fast" "$S/race3-v2"; do cand+=("$d"); done
# Deduplicate before locking, so a repeated candidate never reads its new 000 mode.
unique=()
for d in "${cand[@]}"; do
  [ -d "$d" ] || continue
  case "$d" in
    "$B/cx-jobs"|"$B/cx-live"|"$B/cx-live"/*|"$R"|"$R"/*|"$PYKIT"|"$PYKIT"/*|"$S/race5-py-kit"|"$S/race5-py-kit"/*|"$S/race5-harness"|"$S/race5-harness"/*|"$S/race4-harness"|"$S/race4-harness"/*|"$S/race3-kit"|"$S/race3-kit"/*|"$S/race3-harness"|"$S/race3-harness"/*|"$S"/race3-*-waves.txt) continue ;;
  esac
  seen=false
  for prior in "${unique[@]}"; do [ "$d" != "$prior" ] || { seen=true; break; }; done
  $seen || unique+=("$d")
done
# Listing must not truncate the receipt or change any modes.
if $list; then
  for d in "${unique[@]}"; do printf '%s\n' "$d"; done
  exit 0
fi
: > "$L"
for d in "${unique[@]}"; do
  [ "$(stat -f %Lp "$d")" = 0 ] && { echo "refusing: $d already at mode 000 before locking" >&2; exit 3; }
  "$R/lock.sh" --append "$d"
done
wc -l < "$L"
