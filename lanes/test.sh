#!/bin/sh
# Run every lane test offline. Exits non-zero on any failure.
cd "$(dirname "$0")/.." || exit 1
if ! command -v python3 >/dev/null 2>&1 ||
  ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
  echo "lanes/test.sh: Python 3.11 or later not found; install it or put it on PATH" >&2
  exit 1
fi
go=
if [ -f lanes/grade/go.mod ]; then
  go=$(command -v go 2>/dev/null)
  if [ -z "$go" ] && command -v mise >/dev/null 2>&1; then
    go=$(mise which go 2>/dev/null)
    [ -f "$go" ] && [ -x "$go" ] || go=$(mise where go 2>/dev/null)/bin/go
  fi
  if [ ! -f "$go" ] || [ ! -x "$go" ]; then
    want=$(sed -n 's/^go[[:space:]][[:space:]]*//p' lanes/grade/go.mod | head -n 1)
    echo "lanes/test.sh: Go not found; install Go $want or put it on PATH" >&2
    exit 1
  fi
  PATH=$(dirname "$go"):$PATH
  export PATH
fi
status=0
python3 -m unittest discover -s lanes/tests -t lanes || status=1
if [ -n "$go" ]; then
  (cd lanes/grade && go test ./...) || status=1
fi
exit $status
