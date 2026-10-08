#!/usr/bin/env bash
# Admission check used immediately before every lane or control.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
LOCK=${BENCH_PINS_LOCK:-$HERE/host-pins.lock}
# shellcheck disable=SC1090,SC1091
source "$LOCK"
path=${1:-/srv/bh/bench}
free=$(df -PB1 --output=avail "$path" | tail -n 1 | tr -d ' ')
floor=$((DISK_FLOOR_GIB * 1024 * 1024 * 1024))
if (( free < floor )); then
  printf 'Disk floor: %s bytes free at %s, requires %s bytes\n' "$free" "$path" "$floor" >&2
  exit 1
fi
printf 'Disk floor: %s bytes free at %s (>= %s)\n' "$free" "$path" "$floor"
