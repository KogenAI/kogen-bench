#!/bin/sh
# run-with-exit.sh <log> <command...>   (Lab C9 fix (b)): runs the command with its output appended to <log> and ALWAYS
# writes the "EXIT=<n>" line itself. If the wrapper is terminated (TERM/HUP/INT) the child is stopped and EXIT=143 is
# written from the trap, so a signalled wrapper never leaves a log without an EXIT line. SIGKILL cannot be trapped; reader
# fix (b) covers that case ("landed <slug> <sha>" counts as success without an EXIT line).
LOG=$1; shift
"$@" >> "$LOG" 2>&1 &
child=$!
trap 'kill -TERM "$child" 2>/dev/null; wait "$child" 2>/dev/null; echo "EXIT=143" >> "$LOG"; exit 143' TERM HUP INT
wait "$child"; rc=$?
echo "EXIT=$rc" >> "$LOG"; exit $rc
