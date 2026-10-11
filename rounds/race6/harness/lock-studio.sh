#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in
  --list) exec python3 "$R/hidden_locks.py" list ;;
  --test-dir) exec python3 "$R/hidden_locks.py" lock "$2" ;;
  '') python3 "$R/hidden_inventory.py" --output-dir "$R/out/host-inventory"
      python3 - "$R" <<'PYCODE'
import hashlib,sys
from pathlib import Path
r=Path(sys.argv[1])/'out/host-inventory';(r/'INVENTORY-SHA256').write_text(hashlib.sha256((r/'hidden-inventory.json').read_bytes()).hexdigest()+'\n')
PYCODE
      exec python3 "$R/hidden_locks.py" lock ;;
  *) exit 2 ;;
esac
