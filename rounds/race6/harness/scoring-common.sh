#!/bin/bash
# Shared host slot pool and configurable worker limit for official race 4 scoring.
SCORE_CONCURRENCY=${SCORE_CONCURRENCY:-3}
case "$SCORE_CONCURRENCY" in 1|2|3) ;; *) echo 'SCORE_CONCURRENCY must be 1, 2 or 3' >&2; exit 2;; esac
SCORE_POOL_DIR=${SCORE_POOL_DIR:-${RACE6_KIT_DIR:-$(dirname "$R")/race6-kit}/score-pool}
export SCORE_CONCURRENCY SCORE_POOL_DIR SCORE_JOBS=2
SCORE_SLOT=''
score_pool_acquire() {
  mkdir -p "$SCORE_POOL_DIR"
  while :; do
    for ((slot=1; slot<=SCORE_CONCURRENCY; slot++)); do
      if mkdir "$SCORE_POOL_DIR/slot-$slot" 2>/dev/null; then
        SCORE_SLOT=$SCORE_POOL_DIR/slot-$slot
        return 0
      fi
    done
    sleep 0.1
  done
}
score_pool_release() {
  [ -z "$SCORE_SLOT" ] || rmdir "$SCORE_SLOT"
}
