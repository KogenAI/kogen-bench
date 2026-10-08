#!/usr/bin/env bash
# Model-free reference/no-op admission controls for explicit task IDs.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
if (( $# == 0 )); then echo 'usage: run-controls.sh TASK_ID [TASK_ID ...]' >&2; exit 2; fi
for task in "$@"; do
  [[ $task =~ ^[a-zA-Z0-9][a-zA-Z0-9-]*$ ]] || { echo "Invalid task ID: $task" >&2; exit 2; }
done
[[ $EUID == 0 ]] || { echo 'Run controls with sudo; graders require root-owned sealed kits' >&2; exit 1; }
KIT=/srv/bh/bench/kits/current
[[ -f $KIT/.complete ]] || { echo 'Host kits are absent; run setup-host.sh' >&2; exit 1; }
/usr/local/bin/bench-disk-floor /srv/bh/bench
if systemctl list-units --type=service --state=running --no-legend 'bench-*.service' | grep -q .; then
  echo 'A benchmark service is already running' >&2; exit 1
fi
exec /opt/bench/mise/installs/python/3.14.7/bin/python3 "$HERE/control-worker.py" "$KIT" "$@"
