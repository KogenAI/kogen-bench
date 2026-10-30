#!/bin/bash
# Queue entry: pins new units to one harness release; atomically renamed into place, so running units keep theirs.
# Set LANES_RELEASE to the release's lanes/ dir (this repo's lanes/ for preflight5-20261030).
export LANES_NPMFIX_HARNESS=${LANES_RELEASE:?set LANES_RELEASE to the release lanes/ dir}
export LANES_NPM_CACHE=${LANES_NPM_CACHE:-$HOME/lanes-work/node-cache}
export LANES_APPROVAL_CACHE=${LANES_APPROVAL_CACHE:-$HOME/lanes-work/approval-cache}   # reuse identical ok approvals
exec /bin/bash "$LANES_RELEASE/ops/run-queued.sh" "$@"
