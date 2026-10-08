#!/bin/bash
set -euo pipefail
W="$1"; D=$(cd "$(dirname "$0")" && pwd)
cd "$W"
export PATH="$HOME/.local/share/mise/installs/elixir/1.20.2-otp-29/bin:$HOME/.local/share/mise/installs/erlang/29.0.3/bin:$PATH" MIX_ENV=test TRACKLINE_DB="$W/port-grade.db"
# Revert protected framework/test configuration to this task's public base.
rm -rf test
git checkout HEAD -- mix.exs mix.lock config test
mix compile --force --warnings-as-errors
mix ecto.create --quiet
mix ecto.migrate --quiet
mix test --seed 17
# Contestant tests cannot replace hidden behavior checks.
find test -type f -name '*_test.exs' -delete
cp "$D/sealed/port_test.exs" test/port_test.exs
echo '== hidden checks'
mix test test/port_test.exs --seed 0 | tee .port-hidden.log
python3 - "$D/sealed/port_test.exs" .port-hidden.log <<'CHECK'
import re,sys
from pathlib import Path
expected=len(re.findall(r'^  test ',Path(sys.argv[1]).read_text(),re.M))
out=Path(sys.argv[2]).read_text()
assert expected >= 6 and expected <= 15
assert re.search(r'Result: '+str(expected)+r' passed(?:\s|$)',out), 'hidden tests skipped, excluded or not all run'
CHECK
