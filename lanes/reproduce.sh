#!/bin/sh
# Reproduce a published lane round: lanes/reproduce.sh <kogen-bench>/rounds/<id> [--rerun N] [--hosts FILE]
here=$(cd "$(dirname "$0")" && pwd) || exit 1
PYTHONPATH="$here${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m lanes.reproduce "$@"
