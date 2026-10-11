#!/bin/bash
# Local race 4 scoring driver; score-wave runs both phases with SCORE_CONCURRENCY default 3.
R=$(cd "$(dirname "$0")" && pwd)
exec "$R/score-wave.sh" "$@"
