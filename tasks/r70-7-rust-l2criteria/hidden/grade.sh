#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONPATH=/srv/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages
exec /srv/bh/bench/toolchains/python-3.14.7/bin/python3 "$ROOT/sealed/grade.py" "${1:-$PWD}"
