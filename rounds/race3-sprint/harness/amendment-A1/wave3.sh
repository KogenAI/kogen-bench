#!/bin/bash
# wave3.sh T3_EPOCH MINUTES SNAP_MIN — prepare from a pristine HARNESS_SRC,
# wait for this host's wave 2 DONE, then launch wave 3 at the shared epoch.
set -euo pipefail
[ "$#" -eq 3 ] || { echo "usage: HARNESS_SRC=/pristine/template $0 T3_EPOCH MINUTES SNAP_MIN" >&2; exit 1; }
: "${HARNESS_SRC:?HARNESS_SRC must name a pristine harness template directory}"
[ -d "$HARNESS_SRC" ] && [ -x "$HARNESS_SRC/start.sh" ] || { echo "HARNESS_SRC must contain executable start.sh" >&2; exit 1; }
T3=$1; M=$2; I=$3
for value in "$T3" "$M" "$I"; do
  case "$value" in ''|*[!0-9]*) echo "arguments must be positive integers" >&2; exit 1;; esac
  [ "$((10#$value))" -gt 0 ] || { echo "arguments must be positive integers" >&2; exit 1; }
done
T3=$((10#$T3)); M=$((10#$M)); I=$((10#$I))
S=~/Scratch.noindex
host=st; case "$(hostname)" in *MacBook*) host=mb;; esac
D="$S/race3-$host-w3"; W2="$S/race3-$host-w2"
[ ! -e "$D" ] && [ ! -L "$D" ] || { echo "$D exists" >&2; exit 1; }
[ -d "$W2" ] || { echo "$W2 must be prepared first" >&2; exit 1; }
# A non-recursive mkdir also refuses a competing launch that creates w3.
mkdir "$D"
cp -c -R "$HARNESS_SRC"/. "$D"/
rm -rf "$D/out" "$D/snapshots" "$D/score-wd"
if [ "$host" = st ]; then
  echo ~/.codex-almir > "$D/CODEX_HOME"
else
  echo ~/.codex > "$D/CODEX_HOME"
fi
TIMES="$S/race3-$host-waves.txt"
printf '%s wave3 scheduled %s epoch=%s minutes=%s snap_min=%s prepared=%s\n' \
  "$(hostname -s)" "$(date -u -r "$T3" +%FT%TZ)" "$T3" "$M" "$I" "$(date -u +%FT%TZ)" >> "$TIMES"
until [ -f "$W2/DONE" ]; do sleep 5; done
printf '%s wave2 DONE observed %s; wave3 launcher invoked\n' "$(hostname -s)" "$(date -u +%FT%TZ)" >> "$TIMES"
if "$D/start.sh" "$M" "rust go ts gleam ex" "$I" LOCK "$T3" > "$S/race3-$host-w3.start.log" 2>&1; then
  printf '%s wave3 launcher returned %s\n' "$(hostname -s)" "$(date -u +%FT%TZ)" >> "$TIMES"
else
  status=$?
  printf '%s wave3 launcher failed %s status=%s\n' "$(hostname -s)" "$(date -u +%FT%TZ)" "$status" >> "$TIMES"
  exit "$status"
fi
until [ -f "$D/DONE" ]; do sleep 5; done
printf '%s wave3 done %s start_epoch=%s deadline_epoch=%s\n' \
  "$(hostname -s)" "$(date -u +%FT%TZ)" "$(cat "$D/START")" "$(cat "$D/DEADLINE")" >> "$TIMES"
du -sh "$D" >> "$TIMES"
df -h /Users | tail -1 >> "$TIMES"
