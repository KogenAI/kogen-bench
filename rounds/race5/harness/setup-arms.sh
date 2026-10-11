#!/bin/bash
# Fresh arms with private, writable, repository-local copies of kit caches.
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
source "$R/mode-env.sh" "$R"
KIT=${RACE3_KIT_DIR:-$HOME/retained-run/race3-kit}
PYKIT=${RACE5_PY_KIT_DIR:-$(dirname "$R")/race5-py-kit}
case " $(cat "$R/ARMS") " in
  *" py "*)
    [ "$(uname -s)" = Darwin ] || { echo 'Python is registered on Macs only' >&2; exit 2; }
    [ -d "$PYKIT/templates/py" ] && [ -f "$PYKIT/env-py.sh" ] || { echo 'Python kit pending: templates/py and env-py.sh required' >&2; exit 2; }
    ;;
esac
for L in $(cat "$R/ARMS"); do
  case "$L" in rust|go|ts|ex|py) ;; *) echo "unknown arm: $L" >&2; exit 2;; esac
  TEMPLATE=$KIT/templates/$L
  if [ "$L" = py ]; then
    [ "$(uname -s)" = Darwin ] || { echo 'Python is registered on Macs only' >&2; exit 2; }
    TEMPLATE=$PYKIT/templates/py
    [ -d "$TEMPLATE" ] && [ -f "$PYKIT/env-py.sh" ] || { echo 'Python kit pending: templates/py and env-py.sh required' >&2; exit 2; }
  fi
  rm -rf "$R/$L" "$R/out/$L"
  if [ "$(uname -s)" = Darwin ]; then cp -c -p -R "$TEMPLATE" "$R/$L"; else cp -p -R "$TEMPLATE" "$R/$L"; fi
  cd "$R/$L"
  git init -q
  # Both local config and a private global config cover clones outside this repo.
  export GIT_CONFIG_GLOBAL="$PWD/.gitconfig-global"
  : > "$GIT_CONFIG_GLOBAL"
  for prefix in https://github.com/KogenAI/ http://github.com/KogenAI/ git@github.com:KogenAI/ ssh://git@github.com/KogenAI/; do
    git config --local --add url.https://invalid.invalid/blocked/.insteadOf "$prefix"
    git config --file "$GIT_CONFIG_GLOBAL" --add url.https://invalid.invalid/blocked/.insteadOf "$prefix"
  done
  cp -R "$R/inputs/spec" "$R/inputs/conformance" .
  cp "$R/TARGET.md" .
  mkdir -p .kitcache
  for c in cargo go-build go go-telemetry golangci gopls mix hex xdg config data npm bun bun-transpiler; do
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
echo arms-ready
