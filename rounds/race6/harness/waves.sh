#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
exec "$R/race6-wave.sh" "$@"
