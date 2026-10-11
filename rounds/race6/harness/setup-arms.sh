#!/bin/bash
# Fresh arms with private, writable, repository-local copies of kit caches.
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
source "$R/mode-env.sh" "$R"
KIT=${RACE3_KIT_DIR:-$(dirname "$R")/race3-kit}
PYKIT=${RACE5_PY_KIT_DIR:-$(dirname "$R")/race5-py-kit}
for L in $(cat "$R/ARMS"); do
  LANGID=$(/usr/bin/python3 -c 'import sys; sys.path.insert(0,sys.argv[1]); from condition import language; print(language(sys.argv[2]))' "$R" "$L")
  TEMPLATE=$KIT/templates/$LANGID
  /usr/bin/python3 "$R/reset-arm.py" "$L"
  if [ "$(uname -s)" = Darwin ]; then cp -c -p -R "$TEMPLATE" "$R/$L"; else cp -p -R "$TEMPLATE" "$R/$L"; fi
  cd "$R/$L"
  git init -q
  # Both local config and a private global config cover clones outside this repo.
  export GIT_CONFIG_GLOBAL="$PWD/.gitconfig-global"
  : > "$GIT_CONFIG_GLOBAL"
  for prefix in https://github.com/KogenAI/ http://github.com/KogenAI/ [email omitted]:KogenAI/ ssh://[email omitted]/KogenAI/; do
    git config --local --add url.https://invalid.invalid/blocked/.insteadOf "$prefix"
    git config --file "$GIT_CONFIG_GLOBAL" --add url.https://invalid.invalid/blocked/.insteadOf "$prefix"
  done
  /usr/bin/python3 - "$R" "$L" "$PWD/spec" <<'PYCODE'
import sys
sys.path.insert(0,sys.argv[1])
from spec_split import copy_spec
copy_spec(*sys.argv[1:])
PYCODE
  cp "$R/INTERFACE.md" .
  chmod 444 INTERFACE.md
  cp "$R/TARGET.md" .
  mkdir -p .kitcache
  case "$LANGID" in ex) CACHES="mix hex xdg config data";; go) CACHES="go-build go go-telemetry golangci gopls xdg config data";; *) exit 2;; esac
  for c in cargo go-build go go-telemetry golangci gopls mix hex xdg config data npm bun bun-transpiler; do
    case " $CACHES " in *" $c "*) ;; *) mkdir -p ".kitcache/$c"; continue;; esac
    if [ -d "$KIT/cache/$c" ]; then
      if [ "$(uname -s)" = Darwin ]; then cp -c -p -R -L "$KIT/cache/$c" ".kitcache/$c"; else cp -p -R -L "$KIT/cache/$c" ".kitcache/$c"; fi
    fi
    mkdir -p ".kitcache/$c"
  done
  mkdir -p .kitcache/tmp
  chmod -R u+rwX .kitcache
  if [ "$L" = py ]; then
    mkdir -p .kitcache/py
    for c in uv xdg config data mypy ruff; do
      if [ -d "$PYKIT/cache/$c" ]; then cp -c -p -R -L "$PYKIT/cache/$c" ".kitcache/py/$c"; fi
      mkdir -p ".kitcache/py/$c"
    done
    mkdir -p .kitcache/py/tmp
    /usr/bin/python3 "$R/setup-arm-internet.py" "$PWD" "$KIT" "$PYKIT"
  else
    /usr/bin/python3 "$R/setup-arm-internet.py" "$PWD" "$KIT"
  fi
  printf 'target/\n_build/\ndeps/\nnode_modules/\n.cache/\nbuild/\n.kitcache/\n' >> .gitignore
done
echo race6-arms-ready
