#!/usr/bin/env bash
set -u

HOST=${1:?host required}
TASK_ID=${2:?task id required}
shift 2
[ "$#" -eq 4 ] || { echo 'exactly four arms required' >&2; exit 2; }
STATE_DIR=${SPOT1_STATE_DIR:-spot1-state}
LOG="$STATE_DIR/logs/launcher.log"
mkdir -p "$STATE_DIR/logs"

log() { printf '%s\n' "$1" >> "$LOG"; }
utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
reject_packets() {
  nft list table inet rve2_egress 2>/dev/null | awk '
    /meta skuid 1001 counter packets [0-9]+/ {
      for (i = 1; i <= NF; i++) if ($i == "packets") { print $(i+1); exit }
    }
  '
}

for arm in "$@"; do
  task="$TASK_ID-$arm"
  run_id="spot1-$HOST-$TASK_ID-$arm"
  if [ -e $STATE_DIR/logs/ROUND-STOP ]; then
    log "STOP utc=$(utc) pair=spot run_id=$run_id reason=ROUND-STOP"
    exit 0
  fi

  KIT=${KIT_ROOT:?KIT_ROOT must identify the active kit}
  expected=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prompt_sha256_original"])' "$KIT/tasks/$task/task.json" 2>/dev/null || true)
  actual=$(sha256sum "$KIT/tasks/$task/prompt.md" 2>/dev/null | awk '{print $1}')
  if [ -z "$expected" ] || [ -z "$actual" ] || [ "$expected" != "$actual" ]; then
    log "PREFLIGHT-FAIL utc=$(utc) pair=spot run_id=$run_id task=$task expected=${expected:-missing} actual=${actual:-missing}"
    exit 1
  fi
  log "PREFLIGHT-PASS utc=$(utc) pair=spot run_id=$run_id task=$task expected=$expected actual=$actual"

  before=$(reject_packets)
  before=${before:-0}
  log "START utc=$(utc) pair=spot run_id=$run_id"
  sudo -n /usr/local/bin/bench-run-lane "$task" "$run_id" gpt-6-luna max </dev/null >"$STATE_DIR/logs/$run_id.stdout" 2>"$STATE_DIR/logs/$run_id.stderr" &
  pid=$!
  started=$(date +%s)
  timed_out=0
  while kill -0 "$pid" 2>/dev/null; do
    now=$(date +%s)
    if [ $((now - started)) -ge 1200 ]; then
      systemctl stop "bench-$run_id" >/dev/null 2>&1 || true
      timed_out=1
      break
    fi
    sleep 10
  done

  if [ "$timed_out" -eq 1 ]; then
    wait "$pid" 2>/dev/null || true
    rc=124
    log "TIMEOUT utc=$(utc) pair=spot run_id=$run_id"
  else
    wait "$pid"
    rc=$?
  fi
  log "END utc=$(utc) rc=$rc pair=spot run_id=$run_id"
  after=$(reject_packets)
  after=${after:-0}
  log "REJECTS utc=$(utc) pair=spot run_id=$run_id before=$before after=$after"
done
