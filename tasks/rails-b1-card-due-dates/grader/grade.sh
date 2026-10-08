#!/usr/bin/env bash
set -euo pipefail
[ -n "${GRADEBOX:-}" ] || exec "$HOME/bench/tools/gradebox" "$0" "$@"

RUBYV=3.4.8
RUBY_ROOT="$HOME/.local/share/mise/installs/ruby/$RUBYV"
export PATH="$RUBY_ROOT/bin:$PATH"
export GEM_HOME="$RUBY_ROOT/lib/ruby/gems/3.4.0"
export RAILS_ENV=test BUNDLE_WITHOUT=production BUNDLE_FROZEN=true TZ=UTC
export DATABASE_ADAPTER=sqlite SAAS=false CI_PROGRESS_BAR=0 PARALLEL_WORKERS=2
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1

TASK_DIR="${TASK_DIR:?}"
# v5 verifier submits through each rendered editor form and checks published JSON plus draft Card#due_on.
VERIFY="$TASK_DIR/sealed/hidden_verification_test.rb"
[ -s "$VERIFY" ] || { echo "GRADER_ERROR: hidden verifier missing or empty"; exit 99; }

bin/rails db:test:prepare
echo "== hidden checks"
ruby -Itest "$VERIFY"
