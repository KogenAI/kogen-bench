#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CANDIDATE=$PWD
if [ $# -gt 0 ]; then CANDIDATE=$1; fi
export PYTHONPATH=/srv/bh/bench/toolchains/python-3.14.7/lib/python3.14/site-packages
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
exec /srv/bh/bench/toolchains/python-3.14.7/bin/python3 "$ROOT/sealed/grade.py" "$CANDIDATE"
