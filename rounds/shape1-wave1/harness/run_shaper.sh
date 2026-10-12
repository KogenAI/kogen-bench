#!/bin/bash
# Linux benchmark-lane adapter; without --launch this only prints a command.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 run_shaper.py "$@"
