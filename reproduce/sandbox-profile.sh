#!/usr/bin/env bash
# Whitelist mount profile. Agent mode has only its worktree and its own Codex home.
set -euo pipefail
mode=${1:-}; work=${2:-}; shift 2 || true
[[ -d $work ]] || { echo 'sandbox work directory missing' >&2; exit 2; }
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
work_bind=(--bind "$work" /work)
chdir=/work
case $mode in
  agent)
    socket_path=${1:-}; shift || true
    work_real=$(realpath -- "$work")
    repo_real=$(realpath -- "$work/repo" 2>/dev/null || true)
    [[ -d $work_real && ! -L $work && -d $repo_real && ! -L $work/repo && $repo_real == "$work_real/repo" ]] || {
      echo 'agent mode requires a real WORK directory with a real repo child' >&2; exit 2;
    }
    socket_real=$(realpath -- "$socket_path" 2>/dev/null || true)
    [[ -S $socket_path && $socket_real == "$work_real"/* ]] || {
      echo 'agent mode requires its per-cell egress socket inside WORK' >&2; exit 2;
    }
    socket_in_sandbox=/work/${socket_real#"$work_real"/}
    net=(--unshare-net)
    extra=(--dir /home --dir /home/bench --bind /home/bench/.codex /home/bench/.codex
           --ro-bind "$HERE/egress-bridge.py" /egress-bridge.py)
    # Keep the /work/repo mountpoint itself immutable. The agent may edit
    # contents, but cannot replace the root before post-run patch extraction.
    work_bind=(--ro-bind "$work_real" /work --bind "$repo_real" /work/repo)
    ;;
  grade) task=${1:-}; shift; [[ -d $task ]] || exit 2; net=(--unshare-net); extra=(--ro-bind "$task" /task) ;;
  patch)
    input=$work; scratch=${1:-}; bundle=${2:-}
    if [[ ! -d $input || -L $input ]]; then
      echo 'patch mode requires a real input and scratch directory plus a base bundle (input is not a real directory)' >&2; exit 2
    fi
    if [[ ! -d $scratch || -L $scratch ]]; then
      echo 'patch mode requires a real input and scratch directory plus a base bundle (scratch is not a real directory)' >&2; exit 2
    fi
    if [[ ! -f $bundle || -L $bundle ]]; then
      echo 'patch mode requires a real input and scratch directory plus a base bundle (bundle is not a regular file)' >&2; exit 2
    fi
    work_real=$(realpath -- "$input")
    scratch_real=$(realpath -- "$scratch")
    bundle_real=$(realpath -- "$bundle")
    net=(--unshare-net)
    extra=(--ro-bind "$HERE/lane-patch.sh" /lane-patch.sh
           --bind "$scratch_real" /scratch
           --ro-bind "$bundle_real" /base.bundle)
    work_bind=(--ro-bind "$work_real" /input)
    chdir=/scratch
    ;;
  *) echo 'usage: sandbox-profile.sh agent WORK -- COMMAND | grade WORK TASK -- COMMAND | patch WORK -- COMMAND' >&2; exit 2 ;;
esac
if [[ $mode == patch ]]; then shift 2; fi
[[ ${1:-} == -- ]] || exit 2
shift
if [[ $mode == agent ]]; then
  [[ $# -gt 0 ]] || { echo 'agent mode requires a command' >&2; exit 2; }
  set -- /usr/bin/python3 /egress-bridge.py --unix-socket "$socket_in_sandbox" --port 18765 -- "$@"
fi
exec /usr/bin/bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts \
  --die-with-parent --new-session "${net[@]}" \
  --proc /proc --dev /dev --tmpfs /tmp --dir /tmp/home --tmpfs /run --tmpfs /var --symlink ../tmp /var/tmp \
  --dir /srv --dir /srv/bh --dir /srv/bh/bench \
  --ro-bind /usr /usr --ro-bind /etc /etc --ro-bind /opt/bench /opt/bench \
  --ro-bind /srv/bh/bench/toolchains /srv/bh/bench/toolchains \
  --symlink usr/bin /bin --symlink usr/sbin /sbin \
  --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  "${extra[@]}" "${work_bind[@]}" --chdir "$chdir" "$@"
