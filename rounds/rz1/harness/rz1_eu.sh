#!/usr/bin/env bash
set -euo pipefail

ROOT=public-source-location-withheld
LANE="$ROOT/levers/rz1"
R70="$ROOT/levers/r70"
PY=/opt/bench/mise/installs/python/3.14.7/bin/python3
DISPATCH="$LANE/lane_dispatch.py"
PLAN="$LANE/PLAN.json"
mode=dry-run
scope=all
simulate_stop_after=0
from_pair=0
through_pair=0

usage() {
  printf '%s\n' 'usage: rz1_eu.sh [--dry-run | --smoke-only | --launch] [--plan FILE] [--simulate-stop-after N] [--from-pair N] [--through-pair N]'
}

while (($#)); do
  case "$1" in
    --dry-run) mode=dry-run; shift ;;
    --smoke-only) mode=launch; scope=smoke; shift ;;
    --launch) mode=launch; scope=bulk; shift ;;
    --plan) (($# >= 2)) || { usage >&2; exit 2; }; PLAN="$2"; shift 2 ;;
    --from-pair) (($# >= 2)) || { usage >&2; exit 2; }; from_pair="$2"; shift 2 ;;
    --through-pair) (($# >= 2)) || { usage >&2; exit 2; }; through_pair="$2"; shift 2 ;;
    --simulate-stop-after) (($# >= 2)) || { usage >&2; exit 2; }; simulate_stop_after="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done

if [[ "$PLAN" != /* ]]; then PLAN="$LANE/$PLAN"; fi
if [[ "$simulate_stop_after" != 0 && "$mode" != dry-run ]]; then
  echo 'STOP simulation is available only with --dry-run' >&2
  exit 2
fi
if ! [[ "$simulate_stop_after" =~ ^[0-9]+$ ]]; then
  echo '--simulate-stop-after must be a non-negative integer' >&2
  exit 2
fi

plan_summary=$("$PY" "$DISPATCH" verify-plan --plan "$PLAN")
plan_sha=$("$PY" -c 'import json,sys; print(json.loads(sys.argv[1])["plan_sha256"])' "$plan_summary")
cell_count=$("$PY" -c 'import json,sys; print(json.loads(sys.argv[1])["cells"])' "$plan_summary")
provisional=$("$PY" -c 'import json,sys; print(str(json.loads(sys.argv[1])["provisional"]).lower())' "$plan_summary")
[[ "$provisional" == false || "$mode" == dry-run ]] || { echo 'provisional plan cannot launch' >&2; exit 2; }

disk_free() {
  df -B1 --output=avail /srv | awk 'NR==2 {print $1}'
}
active_cells() {
  PYTHONPATH="$ROOT/levers/lib" "$PY" -c 'from count_cells import count_cells; print(count_cells())'
}
stop_reason() {
  local marker
  for marker in "$ROOT/STOP-eu" "$ROOT/levers/STOP-eu" "$R70/STOP-eu" "$LANE/STOP"; do
    if [[ -e "$marker" ]]; then printf '%s' "$marker"; return 0; fi
  done
  return 1
}
release_flag() {
  "$PY" - "$LANE/gate/release-receipt.json" "$plan_sha" "$1" <<'PY'
import json, pathlib, sys
p=pathlib.Path(sys.argv[1])
if not p.is_file():
    print("missing")
    raise SystemExit(0)
try:
    d=json.loads(p.read_text())
except Exception:
    print("invalid")
    raise SystemExit(0)
flag=sys.argv[3]
print("true" if d.get("plan_sha256")==sys.argv[2] and d.get(flag) is True else "false")
PY
}

preflight() {
  local bytes running marker
  marker=$(stop_reason || true)
  [[ -z "$marker" ]] || { echo "STOP marker present: $marker" >&2; return 1; }
  bytes=$(disk_free)
  [[ "$bytes" =~ ^[0-9]+$ ]] && ((bytes >= 6 * 1024 * 1024 * 1024)) || {
    echo "disk floor failed: available_bytes=${bytes:-unknown}" >&2; return 1;
  }
  running=$(active_cells)
  [[ "$running" == 0 ]] || { echo "benchmark cells already running: $running" >&2; return 1; }
  printf 'PREFLIGHT host=%s free_bytes=%s active_cells=%s plan_sha256=%s\n' "$(hostname)" "$bytes" "$running" "$plan_sha"
}

if [[ "$mode" == launch ]]; then
  if [[ "$scope" == smoke ]]; then flag=allows_smoke_launch; else flag=allows_scored_launch; fi
  allowed=$(release_flag "$flag")
  [[ "$allowed" == true ]] || { echo "release receipt denies $scope launch (flag=$allowed)" >&2; exit 2; }
fi

preflight
if [[ "$scope" == smoke ]]; then flag=allows_smoke_launch; else flag=allows_scored_launch; fi
printf 'PLAN lane=rz1-eu cells=%s plan_sha256=%s mode=%s scope=%s release=%s\n' \
  "$cell_count" "$plan_sha" "$mode" "$scope" "$(release_flag "$flag")"

if [[ "$scope" == smoke ]]; then
  run_from=0
  run_to=2
elif [[ "$scope" == bulk ]]; then
  run_from=2
  run_to=$cell_count
else
  run_from=0
  run_to=$cell_count
fi
if ! [[ "$from_pair" =~ ^[0-9]+$ && "$through_pair" =~ ^[0-9]+$ ]]; then echo '--from-pair/--through-pair must be non-negative integers' >&2; exit 2; fi
# Pre-registered interim (rz1 DECISION-RULE): pair k (1-based) occupies plan indices 2(k-1) and 2(k-1)+1.
if (( from_pair > 0 && 2 * (from_pair - 1) > run_from )); then run_from=$((2 * (from_pair - 1))); fi
if (( through_pair > 0 && 2 * through_pair < run_to )); then run_to=$((2 * through_pair)); fi
if (( run_to > cell_count )); then run_to=$cell_count; fi
printf 'RANGE from_index=%s to_index_exclusive=%s from_pair=%s through_pair=%s\n' "$run_from" "$run_to" "$from_pair" "$through_pair"

monitor_disk() {
  local watched_pid=$1 bytes
  while kill -0 "$watched_pid" 2>/dev/null; do
    sleep 15
    kill -0 "$watched_pid" 2>/dev/null || break
    bytes=$(disk_free)
    printf 'DISK utc=%s free_bytes=%s pid=%s\n' "$(date -u +%FT%TZ)" "$bytes" "$watched_pid"
    if ! [[ "$bytes" =~ ^[0-9]+$ ]] || ((bytes < 6 * 1024 * 1024 * 1024)); then
      touch "$LANE/STOP"
      printf 'DISK_FLOOR_BREACH utc=%s free_bytes=%s; lane STOP set\n' "$(date -u +%FT%TZ)" "$bytes"
      kill -TERM "$watched_pid" 2>/dev/null || true
      break
    fi
  done
}

launched=0
for ((index=run_from; index<run_to; index++)); do
  if (( simulate_stop_after > 0 && launched >= simulate_stop_after )); then
    printf 'STOP-SIMULATION before_index=%s completed_dry_run_rows=%s\n' "$index" "$launched"
    break
  fi
  preflight
  cell_json=$("$PY" "$DISPATCH" describe --plan "$PLAN" --index "$index")
  cell_id=$("$PY" -c 'import json,sys; print(json.loads(sys.argv[1])["cell_id"])' "$cell_json")
  argv_sha=$("$PY" -c 'import json,sys; print(json.loads(sys.argv[1])["argv_sha256"])' "$cell_json")
  argv_json=$("$PY" -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1])["argv"],separators=(",",":")))' "$cell_json")
  if [[ "$mode" == dry-run ]]; then
    printf 'DRY-RUN index=%s cell_id=%s argv_sha256=%s argv=%s\n' "$index" "$cell_id" "$argv_sha" "$argv_json"
    launched=$((launched + 1))
    continue
  fi

  printf 'START utc=%s index=%s cell_id=%s argv_sha256=%s\n' "$(date -u +%FT%TZ)" "$index" "$cell_id" "$argv_sha"
  "$PY" "$DISPATCH" launch-one --plan "$PLAN" --index "$index" --scope "$scope" &
  runner_pid=$!
  monitor_disk "$runner_pid" &
  sampler_pid=$!
  set +e
  wait "$runner_pid"
  rc=$?
  set -e
  kill "$sampler_pid" 2>/dev/null || true
  wait "$sampler_pid" 2>/dev/null || true
  printf 'END utc=%s index=%s cell_id=%s argv_sha256=%s rc=%s\n' "$(date -u +%FT%TZ)" "$index" "$cell_id" "$argv_sha" "$rc"
  # ITT: a failed or errored cell is a measured outcome; continue. Transport replacement is decided later from receipts.
  [[ "$rc" == 0 ]] || printf 'NONZERO utc=%s index=%s cell_id=%s rc=%s (continuing)\n' "$(date -u +%FT%TZ)" "$index" "$cell_id" "$rc"
  launched=$((launched + 1))
done

if [[ "$mode" == dry-run ]]; then
  printf 'RZ1 DONE mode=dry-run launched=0 printed=%s plan_sha256=%s\n' "$launched" "$plan_sha"
else
  printf 'RZ1 DONE mode=launch scope=%s launched=%s plan_sha256=%s\n' "$scope" "$launched" "$plan_sha"
fi
