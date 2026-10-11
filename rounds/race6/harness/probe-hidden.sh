#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$R/probe_hidden.py" "$@"
