#!/usr/bin/env bash
set -u

if [[ $# -ne 3 || ( "$2" != eu && "$2" != us ) ]]; then
  echo "Usage: launch_host.sh PLAN.json eu|us LOGDIR" >&2
  exit 2
fi
plan=$1
host=$2
logdir=$3
mkdir -p "$logdir"

while IFS=$'\t' read -r pair task_id run_id; do
  [[ -n "$run_id" ]] || continue
  if [[ -e "$logdir/ROUND-STOP" ]]; then
    break
  fi

  # Fail closed before every cell if the installed prompt differs from its recorded original.
  KIT=$(readlink -f "<private-path>" 2>/dev/null || true)
  if [[ -z "$KIT" ]] || ! preflight=$(python3 - "$KIT" "$task_id" <<'PY'
import hashlib
import json
import os
import sys

kit, task = sys.argv[1:]
task_dir = os.path.join(kit, "tasks", task)
try:
    with open(os.path.join(task_dir, "task.json"), encoding="utf-8") as f:
        metadata = json.load(f)
    with open(os.path.join(task_dir, "prompt.md"), "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    expected = metadata["prompt_sha256_original"]
except (OSError, ValueError, KeyError, TypeError) as exc:
    print(f"task={task} error={type(exc).__name__}:{exc}")
    raise SystemExit(1)
print(f"task={task} expected={expected} actual={actual}")
raise SystemExit(0 if actual == expected else 1)
PY
  ); then
    printf 'PREFLIGHT-FAIL utc=%s pair=%s run_id=%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pair" "$run_id" "${preflight:-kit-resolution-failed}" >>"$logdir/launcher.log"
    break
  fi
  printf 'PREFLIGHT-PASS utc=%s pair=%s run_id=%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pair" "$run_id" "$preflight" >>"$logdir/launcher.log"
  printf 'START utc=%s pair=%s run_id=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pair" "$run_id" >>"$logdir/launcher.log"
  sudo -n task-runner "$task_id" "$run_id" gpt-6-luna max </dev/null >"$logdir/$run_id.stdout" 2>"$logdir/$run_id.stderr" &
  pid=$!
  start=$(date +%s)
  timed_out=0
  while kill -0 "$pid" 2>/dev/null; do
    now=$(date +%s)
    if (( now - start >= 3600 )); then
      systemctl stop "bench-$run_id" </dev/null >>"$logdir/launcher.log" 2>&1 || true
      timed_out=1
      printf 'TIMEOUT utc=%s pair=%s run_id=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pair" "$run_id" >>"$logdir/launcher.log"
      break
    fi
    sleep 10 </dev/null
  done
  wait "$pid"
  rc=$?
  if (( timed_out )); then rc=124; fi
  printf 'END utc=%s rc=%s pair=%s run_id=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$rc" "$pair" "$run_id" >>"$logdir/launcher.log"
done < <(python3 -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); [print(p["pair_order"],c["task_id"],c["run_id"],sep="\t") for p in d["pairs"] if p["host"]==sys.argv[2] for c in p["cells"]]' "$plan" "$host" </dev/null)
