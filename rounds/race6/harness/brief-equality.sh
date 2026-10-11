#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
python3 - "$R" <<'PY'
import sys
sys.path.insert(0,sys.argv[1])
from briefs import check
check(sys.argv[1])
PY
