#!/usr/bin/env bash
# Whitelist mount profile. Agent mode has only its worktree and its own Codex home.
set -euo pipefail
mode=${1:-}; work=${2:-}; shift 2 || true
[[ -d $work ]] || { echo 'sandbox work directory missing' >&2; exit 2; }
case $mode in
  agent) task=; net=(); extra=(--dir /home --dir /home/bench --bind /home/bench/.codex /home/bench/.codex) ;;
  grade) task=${1:-}; shift; [[ -d $task ]] || exit 2; net=(--unshare-net); extra=(--ro-bind "$task" /task) ;;
  *) echo 'usage: sandbox-profile.sh agent WORK -- COMMAND | grade WORK TASK -- COMMAND' >&2; exit 2 ;;
esac
[[ ${1:-} == -- ]] || exit 2
shift
exec /usr/bin/bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts \
  --die-with-parent --new-session "${net[@]}" \
  --proc /proc --dev /dev --tmpfs /tmp --dir /tmp/home --tmpfs /run --tmpfs /var --symlink ../tmp /var/tmp \
  --dir /srv --dir /srv/bh --dir /srv/bh/bench \
  --ro-bind /usr /usr --ro-bind /etc /etc --ro-bind /opt/bench /opt/bench \
  --ro-bind /srv/bh/bench/toolchains /srv/bh/bench/toolchains \
  --symlink usr/bin /bin --symlink usr/sbin /sbin \
  --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  "${extra[@]}" --bind "$work" /work --chdir /work "$@"
