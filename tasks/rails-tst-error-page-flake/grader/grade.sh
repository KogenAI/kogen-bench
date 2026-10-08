#!/usr/bin/env bash
# Rails Foundation verify protocol, natively (no Docker). Runs in the work dir under the grading Seatbelt profile (bench grade / tools/gradebox), only inside a sealed grade window.
# 0 protected paths (Gemfile*, boot/test env config, test_helper, shared test helpers: rails-_lib/protect.py) must equal the pre-agent snapshot (else fail),
# 1 restore graded surfaces from the pre-agent snapshot (base + environment.patch), 2 preverify: app suite (bin/rails test) must pass,
# 3 hidden checks: ruby -Itest -report-lemans sealed/verification_test.rb, 4 receipt: every hidden check recorded and passing (skips veto via exported TESTS).
# Exit status = reward (0 pass); 99 = grader/infrastructure error (missing verifier, failed snapshot or restore), never a pass.
set -uo pipefail
[ -n "${GRADEBOX:-}" ] || exec "$HOME/bench/tools/gradebox" "$0" "$@"   # contestant code must run sandboxed (tools/gradebox; bench grade sets GRADEBOX=1)
APP=writebook; RUBYV=3.4.8; GEMV=3.4.7
TASK_DIR="${TASK_DIR:?}"; BASE="$HOME/bench/tasks/rails-_base/$APP"; LIB="$HOME/bench/tasks/rails-_lib"
export PATH="$HOME/.local/share/mise/installs/ruby/$RUBYV/bin:$PATH" GEM_HOME="$HOME/.local/share/mise/installs/ruby/${GEMV:-$RUBYV}/lib/ruby/gems/3.4.0"
G="${TMPDIR:-$HOME/bench/work}/rails-grade"; mkdir -p "$G" || exit 99   # TMPDIR = the grader private scratch (deleted after every grade)
export RUBYOPT="-r$LIB/no_egress_ip.rb -r$LIB/uuid_v7_monotonic.rb ${RUBYOPT:-}"   # Selenium's local-IP probe (UDP connect to 8.8.8.8) is refused by the no-network grade sandbox
export SE_BROWSER_PATH="$HOME/bench/rails/chromewrap/chrome"   # same Chrome + --no-sandbox/--disable-crash-reporter: Chrome cannot nest its sandbox inside the grade Seatbelt
export SE_CACHE_PATH="$G/selenium" SE_OFFLINE=true SE_AVOID_STATS=true   # Selenium Manager must not touch $HOME or the network (sandboxed grading)
SNAP="$(mktemp -d "$G/s.XXXXXX")"; TESTS="$(mktemp -d "$G/t.XXXXXX")"; export TESTS   # export: the reporter's skip veto reads ENV["TESTS"]
[ -n "${LOGS:-}" ] || { LOGS="$(mktemp -d "$G/l.XXXXXX")"; OWNLOGS="$LOGS"; }
export TZ=UTC CI_PROGRESS_BAR=0 PARALLEL_WORKERS=2 LOGS
trap 'rm -rf "$SNAP" "$TESTS" "${OWNLOGS:-}"' EXIT
[ -s "$TASK_DIR/sealed/verification_test.rb" ] || { echo "GRADER_ERROR: hidden verifier missing or empty"; exit 99; }
# the official sandbox keeps the app at /app; natively that is the work dir (only affects tests that hard-code "/app/...")
perl -pe "s#\"/app/#\"$PWD/#g" "$TASK_DIR/sealed/verification_test.rb" > "$TESTS/verification_test.rb" && [ -s "$TESTS/verification_test.rb" ] || { echo "GRADER_ERROR: verifier staging failed"; exit 99; }
cp -c -R "$BASE/." "$SNAP/" && (cd "$SNAP" && git init -q && { [ ! -s "$TASK_DIR/environment.patch" ] || git apply --whitespace=nowarn "$TASK_DIR/environment.patch"; }) || { echo "GRADER_ERROR: snapshot failed"; exit 99; }
restore_surfaces() { for p in bin config/environments/test.rb; do rm -rf "./$p"; if [ -e "$SNAP/$p" ]; then mkdir -p "$(dirname "./$p")" && cp -R "$SNAP/$p" "./$p" || { echo "GRADER_ERROR: restore $p failed"; exit 99; }; fi; done; }
python3 "$LIB/protect.py" check "$PWD" "$SNAP" "$(basename "$TASK_DIR")" || { echo "PROTECTED_PATHS_FAIL"; exit 1; }
restore_surfaces
rm -rf tmp/cache
S=$(date +%s)
echo "== preverify: bin/rails test"; perl "$LIB/pgrun.pl" 900 bin/rails test || { echo "PREVERIFY_FAIL"; exit 1; }
M=$(date +%s); echo "== hidden checks"
python3 "$LIB/protect.py" check "$PWD" "$SNAP" "$(basename "$TASK_DIR")" >/dev/null || { echo "PROTECTED_PATHS_FAIL (changed by the test run)"; exit 1; }   # app suite must not have rewritten them
restore_surfaces; rm -f "$LOGS/checks.json"
perl "$LIB/pgrun.pl" 600 ruby -Itest -I"$LIB" -report-lemans "$TESTS/verification_test.rb"; rc=$?
E=$(date +%s); echo "GRADE_TIMING preverify=$((M-S))s hidden=$((E-M))s rc=$rc"
[ $rc -eq 0 ] || exit $rc
python3 "$LIB/protect.py" receipt "$LOGS/checks.json" "$TESTS/verification_test.rb" || { echo "RECEIPT_FAIL"; exit 1; }
exit 0
