#!/bin/bash
R=$(cd "$(dirname "$0")" && pwd)
exec "$R/score-wave.sh" "$@"
