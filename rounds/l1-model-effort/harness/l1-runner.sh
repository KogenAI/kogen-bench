#!/bin/bash
set -euo pipefail
cd /root/l1
exec /usr/bin/python3 -u /root/l1/l1_runner.py "$@"
