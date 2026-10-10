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
  printf 'START utc=%s pair=%s run_id=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$pair" "$run_id" >>"$logdir/launcher.log"
  sudo -n /usr/local/bin/bench-run-lane "$task_id" "$run_id" gpt-6-luna max </dev/null >"$logdir/$run_id.stdout" 2>"$logdir/$run_id.stderr" &
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
