#!/bin/bash
# arm.sh R LANG DEADLINE_EPOCH — one continuing Codex session (gpt-6.1-sol high) in $R/LANG, auto-continued until deadline, STOP or STOP-LANG; each turn wrapped in /usr/bin/time -l (CPU incl. waited children)
R=$1; L=$2; DL=$3; W=$R/$L; O=$R/out/$L; mkdir -p $O; echo $$ > "$O/driver.pid"; /usr/bin/python3 -c 'import os;print(os.getpgrp())' > "$O/pgid"
source "$R/env.sh" || exit 2
[ ! -f "$W/.kit-env.sh" ] || source "$W/.kit-env.sh" || exit 2
source "$R/mode-env.sh" "$R" || exit 2
[ -s $R/CODEX_HOME ] && export CODEX_HOME=$(cat $R/CODEX_HOME)   # e.g. $HOME/.codex-shared on the Studio ([account omitted] on both hosts)
FLAGS=(-m gpt-6.1-sol -c 'model_reasoning_effort="high"' -c features.unified_exec=false -s workspace-write -c "sandbox_workspace_write.network_access=$RACE_NETWORK_ACCESS" -c "web_search=\"$CODEX_WEB_SEARCH\"" --skip-git-repo-check --json)
RFLAGS=(-m gpt-6.1-sol -c 'model_reasoning_effort="high"' -c features.unified_exec=false -c 'sandbox_mode="workspace-write"' -c "sandbox_workspace_write.network_access=$RACE_NETWORK_ACCESS" -c "web_search=\"$CODEX_WEB_SEARCH\"" --skip-git-repo-check --json)
while [ "$(date +%s)" -lt "$(cat "$O/START" 2>/dev/null || echo 0)" ]; do [ ! -f "$R/STOP" ] || exit 0; sleep .5; done
ALERT_FILE=${ALERT_FILE:-$R/out/HEALTH-EVENT.md}
FASTFAIL_BASE=${FASTFAIL_BASE:-30}
case "$FASTFAIL_BASE" in ''|*[!0-9]*) echo "FASTFAIL_BASE must be a positive integer" >&2; exit 1;; esac
FASTFAIL_BASE=$((10#$FASTFAIL_BASE))
[ "$FASTFAIL_BASE" -gt 0 ] || { echo "FASTFAIL_BASE must be positive" >&2; exit 1; }
[ "$FASTFAIL_BASE" -le 300 ] || FASTFAIL_BASE=300
backoff=$FASTFAIL_BASE
stopped() { [ $(date +%s) -ge $DL ] || [ -f $R/STOP ] || [ -f $R/STOP-$L ]; }
# Sleep in small steps so retries and backoff honor the deadline and STOP files.
pause_arm() {
  local until=$(( $(date +%s) + $1 ))
  while ! stopped && [ "$(date +%s)" -lt "$until" ]; do sleep 1; done
}
kill_arm() { for p in $(pgrep -f "codex exec"); do c=$("${RACE_LSOF:-lsof}" -a -p $p -d cwd -Fn 2>/dev/null | sed -n 's/^n//p'); a=$(ps -o args= -p $p); case "$c $a" in "$W"*|*"-C $W "*) kill -TERM $p;; esac; done; }
n=0
python3 "$R/symlink-alert.py" "$R" "$L"
(cd $W && "$R/time-run.sh" "$R/run-codex.sh" "$R" "$L" exec "${FLAGS[@]}" -C $W - < $R/BRIEF-$L.md 2> $O/turn-$n.err | /usr/bin/python3 $R/stamp.py $O/turn-$n.jsonl $O/turn-$n.ts) &
pid=$!; echo $pid > $O/pid; while kill -0 $pid 2>/dev/null; do if stopped; then kill_arm; sleep 1; else pause_arm 5; fi; done
TID=$(grep -m1 -o '"thread_id":"[^"]*"' $O/turn-0.jsonl | cut -d'"' -f4); echo "$TID" > $O/thread
QP='(^|[^0-9])429([^0-9]|$)|\brate.?limit\b|\bquota\b|\busage limit\b|\btoo many requests\b'
fastfail=0
while ! stopped && [ -n "$TID" ]; do
  # stall handling: if the last turn ended on a quota/rate-limit error, log it and wait 60 s before resuming (no tight retry loop)
  if [ "$fastfail" -eq 0 ] && { grep -vE '^[[:space:]]+[0-9]+[[:space:]]|^[[:space:]]*[0-9]+([.][0-9]+)?[[:space:]]+real[[:space:]]' $O/turn-$n.err 2>/dev/null | grep -qiE "$QP" || tail -3 $O/turn-$n.jsonl 2>/dev/null | grep -qiE "$QP"; }; then
    echo "$(date -u +%T) $(date +%s) stall after turn $n" >> $O/stalls.log; touch $O/QUOTA-REFUSAL; pause_arm 60; continue_stall=1
  fi
  stopped && break
  echo "$(date -u +%T) $(date +%s) turn $n ended" >> $O/turns.log
  n=$((n+1))
  python3 "$R/symlink-alert.py" "$R" "$L"
  started_at=$(date +%s)
  (cd $W && "$R/time-run.sh" "$R/run-codex.sh" "$R" "$L" exec resume "${RFLAGS[@]}" "$TID" "Keep implementing Kogen from the supplied spec and writing your own tests until the 60-minute cap. Deliver a prebuilt, offline ./kogen using relative paths." 2> $O/turn-$n.err | /usr/bin/python3 $R/stamp.py $O/turn-$n.jsonl $O/turn-$n.ts) &
  pid=$!; echo $pid > $O/pid; while kill -0 $pid 2>/dev/null; do if stopped; then kill_arm; sleep 1; else pause_arm 5; fi; done
  elapsed=$(( $(date +%s) - started_at ))
  fastfail=0
  if grep -qE '"type"[[:space:]]*:[[:space:]]*"turn[.]completed"' "$O/turn-$n.jsonl" 2>/dev/null; then
    backoff=$FASTFAIL_BASE
  elif [ "$elapsed" -lt 15 ]; then
    echo "$(date -u +%T) $(date +%s) fast-fail after turn $n" >> "$O/fastfail.log"
    first_error=$(head -n 1 "$O/turn-$n.err" | cut -c 1-160)
    printf -- '- %s %s: %s: arm %s resume FAST-FAIL after turn %s (%s)\n' \
      "$(date -u +%FT%TZ)" "$(hostname -s)" "$(basename "$R")" "$L" "$n" "$first_error" >> "$ALERT_FILE"
    fastfail=1
    pause_arm "$backoff"
    backoff=$((backoff * 2))
    [ "$backoff" -le 300 ] || backoff=300
  fi
done
echo "arm $L ended turns=$n $(date -u +%T)" >> $R/out/arms.log
