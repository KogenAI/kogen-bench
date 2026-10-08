#!/bin/sh
set -eu
: "${NIGHT_STAGE:?private grader stage is required}"
TASK_ID=r70-3-ts-bun
SEALED="$NIGHT_STAGE/synthetic/tasks/$TASK_ID/sealed"
test -s "$SEALED/test_hidden.py"
exec /srv/bh/bench/toolchains/python-3.14.7/bin/python3 "$SEALED/grade.py"
