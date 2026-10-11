#!/bin/bash
# Fresh arms with private, writable, repository-local copies of kit caches.
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
KIT=${RACE3_KIT_DIR:-$HOME/retained-run/race3-kit}
for L in $(cat "$R/ARMS"); do
  case "$L" in rust|go|ts|gleam|ex) ;; *) echo "unknown arm: $L" >&2; exit 2;; esac
  rm -rf "$R/$L" "$R/out/$L"
  cp -c -p -R "$KIT/templates/$L" "$R/$L"
  cd "$R/$L"
  git init -q
  cp -R "$R/inputs/spec" "$R/inputs/conformance" .
  cp "$R/TARGET.md" .
  mkdir -p .kitcache
  for c in cargo go-build go go-telemetry golangci gopls mix hex xdg config data npm bun bun-transpiler; do
    if [ -d "$KIT/cache/$c" ]; then
      cp -c -p -R -L "$KIT/cache/$c" ".kitcache/$c"
    fi
    mkdir -p ".kitcache/$c"
  done
  mkdir -p .kitcache/tmp
  chmod -R u+rwX .kitcache
  /usr/bin/python3 "$R/setup-arm-internet.py" "$PWD" "$KIT"
  printf 'target/\n_build/\ndeps/\nnode_modules/\n.cache/\nbuild/\n.kitcache/\n' >> .gitignore
done
echo arms-ready
