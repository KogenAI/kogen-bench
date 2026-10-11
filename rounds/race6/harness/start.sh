#!/bin/bash
# start.sh 60 "CONDITIONS" 5 LOCK EPOCH; next gated whole-minute epoch, no live dry cells.
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd); cd "$R"
M=${1:-60}; ARMS=${2:-"ex-a ex-b ex-c ex-d go-a go-b go-c go-d"}; I=${3:-5}; LK=${4:-LOCK}; AT=${5:-}
[ "$M" = 60 ] || { echo "race6 requires a 60-minute cap" >&2; exit 2; }
[ "$I" = 5 ] && [ "$LK" = LOCK ] || { echo 'five-minute snapshots and LOCK are mandatory' >&2; exit 2; }
case "$AT" in ''|*[!0-9]*) echo 'explicit start epoch required' >&2; exit 2;; esac
case "$(uname -s):$ARMS" in Darwin:'ex-a ex-b ex-c ex-d go-a go-b go-c go-d'|Linux:ex-a|Linux:ex-d) ;; *) echo 'Macs: ex-a ex-b ex-c ex-d go-a go-b go-c go-d; Linux EU: a, US: d' >&2; exit 2;; esac
if [ "$(uname -s)" = Linux ]; then
  case "$(basename "$R"):$ARMS:$(cat CODEX_HOME)" in
    race6-eu-*:ex-a:"$HOME"/.codex|race6-us-*:ex-d:"$HOME"/.codex-billing) ;;
    *) echo 'Linux EU=A with $HOME/.codex; US=D with $HOME/.codex-billing' >&2; exit 2 ;;
  esac
fi
[ ! -e START ] && [ ! -e DONE ] || { echo 'fresh wave directory required' >&2; exit 1; }
export PYTHONDONTWRITEBYTECODE=1 RACE_CAP_MIN="$M" RACE_SNAPSHOT_MIN="$I"
printf '%s\n' "$ARMS" > ARMS; printf '%s\n' "$M" > CAP_MIN
mkdir -p out snapshots
python3 "$R/freeze.py" --check
python3 "$R/checks.py" --disk-only
./setup-arms.sh > out/setup.txt
./checks.sh
python3 - <<'PY'
from processes import table,cwd_table
assert table() and cwd_table(), 'host process observation required'
PY
# Supervisor launch-only client pin; build gates never execute Codex.
source "$R/env.sh"
export CODEX_HOME=$(cat "$R/CODEX_HOME")
CLIENT=$(codex --version)
[ "$CLIENT" = "$(cat CODEX-VERSION)" ] || { echo 'Codex client version differs from pin' >&2; exit 1; }

L=./lock-studio.sh; case "$(hostname)" in *MacBook*) L=./lock-macbook.sh;; esac
$L > out/lock.txt 2>&1
# On Macs probe all real protected roots as the arm user before any arm starts.
# Linux admin-owned 0700 suite is probed by bench as part of the same gate.
if ! ./probe-hidden.sh --live > out/hidden-probe.txt 2>&1; then ./unlock.sh; echo 'hidden suite exposure: abort before launch' >&2; exit 1; fi
REQUESTED=$AT; S=$(( ($(date +%s)/60+1)*60 )); echo "requested_epoch=$REQUESTED gated_epoch=$S" > out/epoch-receipt.txt; AT=$S; DL=$((S+M*60)); echo "$S" > START; echo "$DL" > DEADLINE
: > out/arms.log
python3 - "$R" "$S" <<'PYCODE'
import json,os,sys
from pathlib import Path
r=Path(sys.argv[1]);s=int(sys.argv[2]);go=int(os.environ.get('RACE6_GO_EPOCH',s+int(os.environ.get('RACE6_GO_DELAY_MINUTES','0'))*60))
assert s<=go<=s+900,'Go epoch must be gated epoch or at most 15 minutes later'
starts={a:(go if a.startswith('go-') else s) for a in (r/'ARMS').read_text().split()}
(r/'LANGUAGE-EPOCHS.json').write_text(json.dumps(starts,sort_keys=True)+'\n')
cores=float(os.environ.get('RACE6_SOFT_CORES','1.5' if (r/'CODEX_HOME').read_text().strip().endswith('/.codex') else '1.25'))
assert 0<cores<=2
(r/'out/cpu-caps.json').write_text(json.dumps({'soft_cores_per_arm':cores,'arms':list(starts),'method':'process-tree duty-cycle; one-second soft bursts'})+'\n')
for a,t in starts.items():
    (r/'out'/a).mkdir(exist_ok=True);(r/'out'/a/'START').write_text(str(t));(r/'out'/a/'DEADLINE').write_text(str(t+3600))
(r/'DEADLINE').write_text(str(max(starts.values())+3600))
PYCODE
while [ "$(date +%s)" -lt "$AT" ]; do sleep .5; done
# Stopper starts before arms; any subsequent launch failure requests STOP.
trap 'touch "$R/STOP"' ERR
python3 "$R/detach.py" "$R/out/stopper.log" python3 "$R/stop-wave.py"
for A in $ARMS; do
  python3 "$R/detach.py" "$R/out/arm-$A.log" "$R/arm.sh" "$R" "$A" "$(cat "$R/out/$A/DEADLINE")"
done
python3 "$R/detach.py" "$R/out/cpu-sampler.out" "$R/cpu-sampler.sh" "$R"
python3 "$R/detach.py" "$R/out/snap-loop.out" "$R/snap-loop.sh" "$I"
python3 "$R/detach.py" "$R/out/guard.out" "$R/guard.sh"
python3 "$R/detach.py" "$R/out/pruner.log" python3 "$R/prune-snapshots.py" --root "$R" --loop
printf 'launched %s: cap=%sm, snapshots=%sm, epoch=%s, scoring detached after DONE\n' "$ARMS" "$M" "$I" "$AT"
