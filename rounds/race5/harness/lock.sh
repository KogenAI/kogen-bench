#!/bin/bash
# lock.sh [--append] DIR... — record exact modes in this harness and chmod 000.
# Host scripts choose the agreed candidates; explicit dirs also permit safe tests.
set -e
R=$(cd "$(dirname "$0")" && pwd); L=$R/locks.tsv
if [ "$1" = --append ]; then shift; else : > "$L"; fi
[ "$#" -gt 0 ] || { echo "usage: lock.sh [--append] DIR..."; exit 2; }
for d in "$@"; do
  [ -d "$d" ] || continue
  grep -qF "$(printf '\t')$d" "$L" && continue
  [ "$(stat -f %Lp "$d")" = 0 ] && { echo "refusing: $d already at mode 000 before locking" >&2; exit 3; }
  printf '%s\t%s\n' "$(stat -f %Lp "$d")" "$d" >> "$L"
  chmod 000 "$d"
done
