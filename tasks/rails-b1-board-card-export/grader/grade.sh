#!/usr/bin/env bash
set -euo pipefail
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
[ -n "${GRADEBOX:-}" ] || exec "$HOME/bench/tools/gradebox" "$0" "$@"

RUBYV=3.4.8
LIB="$HOME/bench/tasks/rails-_lib"
export PATH="$HOME/.local/share/mise/installs/ruby/$RUBYV/bin:$PATH"
export GEM_HOME="$HOME/.local/share/mise/installs/ruby/$RUBYV/lib/ruby/gems/3.4.0"
export RAILS_ENV=test BUNDLE_WITHOUT=production BUNDLE_FROZEN=true
export TZ=UTC SAAS=false DATABASE_ADAPTER=sqlite CI_PROGRESS_BAR=0 PARALLEL_WORKERS=2
export RUBYOPT="-rcsv -r$LIB/no_egress_ip.rb -r$LIB/uuid_v7_monotonic.rb ${RUBYOPT:-}"

TASK_DIR="${TASK_DIR:?}"
G="${TMPDIR:?}/rails-board-card-export"
TESTS="$G/tests"
LOGS="$G/logs"
export TESTS LOGS
mkdir -p "$TESTS" "$LOGS"
[ -s "$TASK_DIR/sealed/verification_test.rb" ] || { echo "GRADER_ERROR: sealed verifier missing"; exit 99; }
VERIFIER="$TASK_DIR/sealed/verification_test.rb"
RUN_VERIFIER="$TESTS/verification_test.rb"
cp "$VERIFIER" "$RUN_VERIFIER"

bin/rails db:test:prepare
bin/rails db:migrate
ruby -Itest -I"$LIB" -report-lemans "$RUN_VERIFIER"
python3 "$LIB/protect.py" receipt "$LOGS/checks.json" "$VERIFIER"
