#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
APPEND=()
if [ "${1:-}" = --append ]; then APPEND=(--append); shift; fi
exec python3 "$R/hidden_locks.py" lock "${APPEND[@]}" "$@"
