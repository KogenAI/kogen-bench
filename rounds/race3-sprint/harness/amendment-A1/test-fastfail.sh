#!/bin/bash
# No network or model calls. All temporary files stay beside this script.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp -d "$HERE/.test-fastfail.XXXXXX") || exit 1
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
cat > "$TMP/bin/codex" <<'EOF'
#!/bin/bash
if [ "$1" = exec ] && [ "${2:-}" = resume ]; then
  date +%s >> "$ATTEMPTS"
  if [ "$MODE" = fail ]; then
    echo 'error: unexpected argument' >&2
    exit 2
  fi
  echo '{"type":"turn.completed"}'
  sleep 3
  exit 0
fi
echo '{"type":"thread.started","thread_id":"fake-thread"}'
echo '{"type":"turn.completed"}'
EOF
chmod +x "$TMP/bin/codex"

prepare() {
  local race=$1
  mkdir -p "$race/rust" "$race/out/rust"
  : > "$race/env.sh"
  : > "$race/BRIEF-rust.md"
  : > "$race/alerts.md"
  : > "$race/attempts"
  : > "$race/out/rust/stalls.log"
  cat > "$race/stamp.py" <<'EOF'
import sys, time
with open(sys.argv[1], "w") as output:
    for line in sys.stdin:
        output.write(line)
        output.flush()
        with open(sys.argv[2], "w") as stamp:
            stamp.write(str(int(time.time())) + "\n")
EOF
}

# Run the success cases concurrently to keep total runtime near 75 seconds.
# Also exercise the continuation entry point with an already saved turn 0.
names=(); pids=(); deadlines=(); statuses=()
for script in arm.sh arm-cont.sh; do
  for mode in fail success; do
    name="${script%.sh}-$mode"
    race="$TMP/$name"
    prepare "$race"
    if [ "$script" = arm-cont.sh ]; then
      echo 'fake-thread' > "$race/out/rust/thread"
      echo 2147483647 > "$race/out/rust/pid"
      echo '{"type":"turn.completed"}' > "$race/out/rust/turn-0.jsonl"
      : > "$race/out/rust/turn-0.err"
    fi
    duration=75
    [ "$mode" = success ] && duration=8
    deadline=$(( $(date +%s) + duration ))
    (
      PATH="$TMP/bin:$PATH" MODE="$mode" ATTEMPTS="$race/attempts" \
        ALERT_FILE="$race/alerts.md" FASTFAIL_BASE=2 \
        bash "$HERE/$script" "$race" rust "$deadline" > "$race/run.log" 2>&1
      status=$?
      date +%s > "$race/ended"
      exit "$status"
    ) &
    names+=("$name"); pids+=("$!"); deadlines+=("$deadline")
  done
done
for pid in "${pids[@]}"; do
  wait "$pid"
  statuses+=("$?")
done

failures=0
check() {
  local label=$1
  shift
  if "$@"; then
    printf 'PASS %s\n' "$label"
  else
    printf 'FAIL %s\n' "$label"
    failures=$((failures + 1))
  fi
}
for ((i=0; i<${#names[@]}; i++)); do
  name=${names[$i]}; race="$TMP/$name"
  count=$(wc -l < "$race/attempts" | tr -d ' ')
  ended=$(cat "$race/ended")
  if [[ "$name" = *-fail ]]; then
    fastfails=0
    [ ! -f "$race/out/rust/fastfail.log" ] || fastfails=$(wc -l < "$race/out/rust/fastfail.log" | tr -d ' ')
    check "$name: at least 2 fast-fails ($fastfails)" test "$fastfails" -ge 2
    check "$name: FAST-FAIL alert includes first error" grep -qE \
      '^- [0-9-]+T[0-9:]+Z [^:]+: [^:]+: arm rust resume FAST-FAIL after turn [0-9]+ \(error: unexpected argument\)$' "$race/alerts.md"
    alerts=$(wc -l < "$race/alerts.md" | tr -d ' ')
    check "$name: one alert per fast-fail ($alerts)" test "$alerts" -eq "$fastfails"
    check "$name: at most 8 resumes in 75 seconds ($count)" test "$count" -le 8
    check "$name: retries continue toward deadline" test "$ended" -ge "${deadlines[$i]}"
  else
    check "$name: successful resume exercised ($count)" test "$count" -ge 1
    check "$name: no fast-fail" test ! -s "$race/out/rust/fastfail.log"
    check "$name: no alert" test ! -s "$race/alerts.md"
  fi
  check "$name: no stalls" test ! -s "$race/out/rust/stalls.log"
  check "$name: exits successfully by itself" test "${statuses[$i]}" -eq 0
  check "$name: arms.log ending line" grep -qE '^arm rust ended turns=[0-9]+ [0-9:]+$' "$race/out/arms.log"
  check "$name: ends within 5 seconds after DL" test "$ended" -le "$((deadlines[$i] + 5))"
done
printf 'Assertions failed: %s\n' "$failures"
[ "$failures" -eq 0 ]
