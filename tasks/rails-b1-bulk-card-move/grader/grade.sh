#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/share/mise/installs/ruby/3.4.8/bin:$PATH"
export GEM_HOME="$HOME/.local/share/mise/installs/ruby/3.4.8/lib/ruby/gems/3.4.0"
export RAILS_ENV=test
export BUNDLE_WITHOUT=production
export BUNDLE_FROZEN=true
export DATABASE_ADAPTER=sqlite
export SAAS=false
export TZ=UTC
export CI_PROGRESS_BAR=0

test -f "$TASK_DIR/sealed/verification_test.rb"
bin/rails db:test:prepare
bundle exec ruby -Itest "$TASK_DIR/sealed/verification_test.rb"
