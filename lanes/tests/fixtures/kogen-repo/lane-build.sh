#!/bin/sh
# Trivial build for tests: lane-out is a script that prints the tree's VERSION.
# VERSION "hang" makes `lane-out version` start a background sleep (pid in $LANE_PID_FILE) and wait.
echo build >> "${LANE_BUILD_COUNT:-/dev/null}"
if [ "$(cat VERSION)" = hang ]; then
  printf '#!/bin/sh\nsleep 30 &\necho $! > "$LANE_PID_FILE"\nwait\n' > lane-out
else
  printf '#!/bin/sh\necho "kogen v%s (test)"\n' "$(cat VERSION)" > lane-out
fi
chmod +x lane-out
