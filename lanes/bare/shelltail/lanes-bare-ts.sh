#!/bin/sh
# lanes-bare.sh: head-to-head cells (kogen loop vs codex exec vs claude -p), graded by the lanes grader.
# Runs on the lanes host as its lanes user (on macOS, the runner account). Usage: lanes-bare.sh cell|batch|summary ... (see lanes_bare_ts.py -h)
# Environment: LANES_ENV (default $LANES_PRIVATE/lanes.env: PATH with the refusing shims, mise toolchain,
# KOGEN_LANES_HOME, LANES_DIR), CLAUDE_BIN, CODEX_BIN are picked up by the options' defaults.
HERE=$(cd "$(dirname "$0")" && pwd)
LE=${LANES_ENV:-${LANES_PRIVATE:-$HOME/lanes-work}/lanes.env}
[ -f "$LE" ] && . "$LE"
export MISE_TRUSTED_CONFIG_PATHS=${MISE_TRUSTED_CONFIG_PATHS:-/}
exec python3 "$HERE/lanes_bare_ts.py" "$@"
