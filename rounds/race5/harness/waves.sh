#!/bin/bash
# waves.sh A_EPOCH B_EPOCH [GAP_MIN] — fresh Mac waves, scoring between them.
set -euo pipefail
H=$(cd "$(dirname "$0")" && pwd)
[ "$#" -ge 2 ] && [ "$#" -le 3 ] || { echo 'usage: waves.sh A_EPOCH B_EPOCH [GAP_MIN=10]' >&2; exit 2; }
T0=$1; T1=$2; GAP=${3:-10}
for value in "$T0" "$T1" "$GAP"; do
  case "$value" in ''|*[!0-9]*) echo 'epochs and gap must be nonnegative integers' >&2; exit 2;; esac
done
# Force decimal parsing, including inputs with leading zeroes.
T0=$((10#$T0)); T1=$((10#$T1)); GAP=$((10#$GAP))
[ "$T1" -ge "$((T0 + 180*60 + GAP*60))" ] || { echo 'B must be at least A + 3 hours + gap' >&2; exit 2; }
[ "$(uname -s)" = Darwin ] || { echo 'waves.sh runs the Macs; Linux uses one Rust or Go arm per start.sh invocation' >&2; exit 2; }
S=$(dirname "$H"); HOST=st
case "$(hostname)" in *MacBook*) HOST=mb;; esac
ARMS='rust go ts ex py'
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$H/prepare-inputs.py"
for W in a b; do
  D=$S/race5-$HOST-$W
  [ ! -e "$D" ] || { echo "$D exists; use a fresh destination" >&2; exit 1; }
done
for W in a b; do
  D=$S/race5-$HOST-$W
  mkdir "$D"; cp -c -R "$H/." "$D/"
  rm -rf "$D/out" "$D/snapshots" "$D/score-wd" "$D/score-cases"
  rm -f "$D/STOP" "$D/DONE" "$D"/STOP-* "$D/START" "$D/DEADLINE" "$D/locks.tsv" "$D/stopper.sh"
  if [ "$HOST" = st ]; then printf '%s\n' $HOME/.codex-shared > "$D/CODEX_HOME"
  else printf '%s\n' $HOME/.codex > "$D/CODEX_HOME"; fi
done
LOG=$S/race5-$HOST-waves.txt
printf '%s A=%s B=%s cap=180m gap=%sm arms=%s\n' "$(hostname -s)" "$T0" "$T1" "$GAP" "$ARMS" > "$LOG"
for W in a b; do
  D=$S/race5-$HOST-$W; AT=$T0; [ "$W" != b ] || AT=$T1
  "$D/start.sh" 180 "$ARMS" 5 LOCK "$AT" > "$D.start.log" 2>&1
  until [ -f "$D/DONE" ]; do sleep 5; done
  echo "$W done $(date -u +%FT%TZ)" >> "$LOG"
  # Synchronous scoring must finish before the next wave's start.sh runs.
  "$D/score-wave.sh" >> "$D.score.log" 2>&1
  echo "$W scored $(date -u +%FT%TZ)" >> "$LOG"
done
