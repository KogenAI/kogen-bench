#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
exec python3 "$R/snapshot-scheduler.py" "$1"
