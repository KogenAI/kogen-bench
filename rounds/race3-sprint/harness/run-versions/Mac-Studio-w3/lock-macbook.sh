#!/bin/bash
# lock-macbook.sh — chmod 000 every Kogen implementation/clone, race dir (with earlier arms' code), export archive and Quint tool on the MacBook;
# record modes in this harness dir's locks.tsv for exact restore by unlock.sh. The race3 kit stays readable (agents need its docs/env).
set -e; R=$(cd "$(dirname "$0")" && pwd); L=$R/locks.tsv; : > $L
if [ "$1" = --test-dir ]; then exec "$R/lock.sh" "$2"; fi
K=~/Areas/Kogen; S=~/Scratch.noindex
cand=( $K/kogen $K/kogen-try $K/quint-connect-go $K/kogen-rs $K/kogen-rs-wt $K/kogen-core $K/kogen-spec $K/kogen-spec-wt $K/kogen-conformance $K/kogen-bare $K/kogen-live $K/kogen-loop $K/kogen-desperate $K/kogen-release-v0 $K/codegen_rewrite
       $S/kogen-core $S/kogen-research $S/kogen-remote $S/verify $S/conf-final $S/quint-cli $S/race $S/race-gleam $S/race-export $S/race3-stack-guides ~/.kogen )
for d in $K/codegen-core* $K/kogen-codex* $K/kogen-compare-* $K/kogen-build-* $K/kogen-next-* $K/kogen-direct-* $K/kogen-compact-* $K/kogen-b027-* $K/kogen-context-* $K/kogen-custody-* $K/kogen-local-* $K/kogen-c01-* $K/kogen-opening-* $S/race2* $S/race3-*; do cand+=("$d"); done
for d in "${cand[@]}"; do [ -d "$d" ] || continue; grep -qF "	$d" $L 2>/dev/null && continue;   # dedupe: never record an already-locked dir (its mode would read 000)
  [ "$(stat -f %Lp "$d")" = 0 ] && { echo "refusing: $d already at mode 000 before locking" >&2; exit 3; }; case "$d" in "$R"|"$R"/*|$S/race3-kit|$S/race3-kit/*|$S/race3-harness|$S/race3-harness/*) continue;; esac; "$R/lock.sh" --append "$d"; done
wc -l < $L
