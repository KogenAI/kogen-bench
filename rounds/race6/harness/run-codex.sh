#!/bin/bash
set -euo pipefail
R=$1; A=$2; shift 2
if [ "$(uname -s)" = Darwin ]; then
  CORES=${RACE6_SOFT_CORES:-1.25}
  case "$(cat "$R/CODEX_HOME")" in */.codex) CORES=${RACE6_SOFT_CORES:-1.5};; esac
  exec python3 "$R/soft-cpu.py" "$CORES" codex "$@"
fi
# Linux has one Elixir arm; all other wave roots are locked before launch.
exec codex "$@"
