#!/bin/bash
# test-gates.sh DRY_CELL_ROOT|OUT — read-only source, all work on copies here.
R=$(cd "$(dirname "$0")" && pwd)
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 "$R/gate-runner.py" "$@"
