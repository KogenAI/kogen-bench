#!/bin/sh
# Run every lane test offline. Exits non-zero on any failure.
cd "$(dirname "$0")/.." || exit 1
status=0
python3 -m unittest discover -s lanes/tests -t lanes || status=1
if [ -f lanes/grade/go.mod ]; then
  (cd lanes/grade && go test ./...) || status=1
fi
exit $status
