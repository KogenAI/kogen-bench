#!/bin/bash
# waves.sh T0_EPOCH — fresh A/B copies on this host; identical epochs on both hosts.
set -e
H=$(cd "$(dirname "$0")" && pwd); T0=${1:?usage: waves.sh T0_EPOCH}
case "$T0" in ''|*[!0-9]*) echo 'T0_EPOCH must be an integer' >&2; exit 2;; esac
S=$(dirname "$H"); HOST=st
case "$(hostname)" in *MacBook*) HOST=mb;; esac
ARMS='rust go ts gleam ex'; T1=$((T0 + 60*60 + 5*60))
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$H/prepare-inputs.py"
for W in a b; do
  D=$S/race4-$HOST-$W
  [ ! -e "$D" ] || { echo "$D exists; use a fresh destination" >&2; exit 1; }
done
for W in a b; do
  D=$S/race4-$HOST-$W
  mkdir "$D"; cp -c -R "$H/." "$D/"
  rm -rf "$D/out" "$D/snapshots" "$D/score-wd" "$D/score-cases"
  rm -f "$D/STOP" "$D/DONE" "$D"/STOP-* "$D/START" "$D/DEADLINE" "$D/locks.tsv" "$D/stopper.sh"
  if [ "$HOST" = st ]; then printf '%s\n' $HOME/.codex-shared > "$D/CODEX_HOME"
  else printf '%s\n' $HOME/.codex > "$D/CODEX_HOME"; fi
done
LOG=$S/race4-$HOST-waves.txt
printf '%s A=%s B=%s cap=60m gap=5m\n' "$(hostname -s)" "$T0" "$T1" > "$LOG"
for W in a b; do
  D=$S/race4-$HOST-$W; AT=$T0; [ "$W" != b ] || AT=$T1
  "$D/start.sh" 60 "$ARMS" 5 LOCK "$AT" > "$D.start.log" 2>&1
  until [ -f "$D/DONE" ]; do sleep 5; done
  echo "$W done $(date -u +%FT%TZ)" >> "$LOG"
done
# Scoring cannot compete with any live wave. Score each completed wave separately.
for W in a b; do
  "$S/race4-$HOST-$W/score-wave.sh" >> "$S/race4-$HOST-$W.score.log" 2>&1
  echo "$W scored $(date -u +%FT%TZ)" >> "$LOG"
done
