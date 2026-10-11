#!/bin/bash
# Race 4 uses the fixed 60-minute A/B schedule.
R=$(cd "$(dirname "$0")" && pwd)
exec "$R/waves.sh" "$@"
