#!/bin/bash
# Single wave; never waits for scoring or another wave.
set -euo pipefail
H=$(cd "$(dirname "$0")" && pwd)
[ "$#" = 1 ] || { echo 'usage: race6-wave.sh EPOCH' >&2; exit 2; }
case "$1" in ''|*[!0-9]*) exit 2;; esac
EPOCH=$1; S=$(dirname "$H"); HOST=${RACE6_HOST:-st}
case "$(hostname)" in *MacBook*) HOST=${RACE6_HOST:-mb};; esac
case "$HOST" in
  st) ARMS='ex-a ex-b ex-c ex-d go-a go-b go-c go-d'; C=$HOME/.codex-shared ;;
  mb) ARMS='ex-a ex-b ex-c ex-d go-a go-b go-c go-d'; C=$HOME/.codex ;;
  eu) ARMS=ex-a; C=${HOME}/.codex ;;
  us) ARMS=ex-d; C=${HOME}/.codex-billing ;;
  *) exit 2 ;;
esac
W=${RACE6_WAVE_NUMBER:-1}; case "$W" in 1) ;; *) exit 2;; esac
D=$S/race6-$HOST-$W; M=60
[ "${RACE6_DRY:-0}" = 0 ] || { echo "live dry cells waived by frozen rule" >&2; exit 2; }
[ ! -e "$D" ] || { echo "$D exists; fresh destination required" >&2; exit 1; }
if [ "$(uname -s)" = Linux ]; then
  echo 'Linux supervisor must provision benchadmin-owned suite before start.sh; follow LINUX-RACE6.md' >&2; exit 2
fi
mkdir "$D"; cp -c -R "$H/." "$D/"
python3 - "$D" <<'PY'
from pathlib import Path
import shutil,sys
root=Path(sys.argv[1])
for name in ('out','snapshots','score-wd','score-cases','evidence'):
    p=root/name
    if p.exists():shutil.rmtree(p)
for name in ('STOP','DONE','START','DEADLINE','CAP_MIN','locks.tsv'):
    (root/name).unlink(missing_ok=True)
PY
printf '%s\n' "$C" > "$D/CODEX_HOME"
exec "$D/start.sh" "$M" "$ARMS" 5 LOCK "$EPOCH"
