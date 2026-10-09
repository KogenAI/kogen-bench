#!/usr/bin/env bash
# Build a patch from a copy of the work tree without consulting its Git metadata.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")

if [[ ${1:-} == --inside ]]; then
  (( EUID != 0 )) || { echo 'patch extraction must not run as root' >&2; exit 2; }
  shift
  base=$1 bundle=$2 input=$3 scratch=$4
  export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_ATTR_NOSYSTEM=1
  unset GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
  while IFS= read -r name; do unset "$name"; done < <(compgen -e | sed -n '/^GIT_CONFIG_KEY_[0-9][0-9]*$/p; /^GIT_CONFIG_VALUE_[0-9][0-9]*$/p')
  python3 - "$input" "$scratch/tree" <<'PY'
import os, shutil, stat, sys
source, target = sys.argv[1:]
os.mkdir(target)
def copy_dir(src, dst):
    with os.scandir(src) as entries:
        for entry in entries:
            if entry.name == '.git':
                continue
            s, d = entry.path, os.path.join(dst, entry.name)
            try: mode = entry.stat(follow_symlinks=False).st_mode
            except FileNotFoundError: continue
            if stat.S_ISLNK(mode):
                os.symlink(os.readlink(s), d)
            elif stat.S_ISDIR(mode):
                os.mkdir(d, stat.S_IMODE(mode)); copy_dir(s, d)
            elif stat.S_ISREG(mode):
                shutil.copyfile(s, d, follow_symlinks=False)
                os.chmod(d, stat.S_IMODE(mode))
copy_dir(source, target)
PY
  tree=$scratch/tree
  git -c init.defaultBranch=patch-base init -q "$tree"
  git -C "$tree" config core.hooksPath /dev/null
  git -C "$tree" config core.fsmonitor false
  mkdir -p "$tree/.git/info"
  printf '* -filter -diff -merge\n' > "$tree/.git/info/attributes"
  git -C "$tree" fetch -q --no-tags "$bundle" "$base"
  git -C "$tree" update-ref refs/heads/patch-base FETCH_HEAD
  git -C "$tree" symbolic-ref HEAD refs/heads/patch-base
  git -C "$tree" read-tree "$base"
  git -C "$tree" add -A
  git -C "$tree" diff --binary --no-ext-diff --no-textconv "$base" --cached > "$scratch/out.diff"
  exit 0
fi

if (( $# != 4 )); then
  echo 'usage: lane-patch.sh BASE BASE_BUNDLE REPO RESULT' >&2; exit 2
fi
base=$1 bundle=$2 repo=$3 out=$4
[[ $base =~ ^[0-9a-f]{40}$ && -f $bundle ]] || { echo 'patch inputs unavailable' >&2; exit 2; }
if (( EUID == 0 )); then
  bench_uid=$(id -u bench); bench_gid=$(id -g bench)
  scratch=$(mktemp -d /tmp/lane-patch.XXXXXX)
  chown "$bench_uid:$bench_gid" "$scratch"
  chmod 0700 "$scratch"
  cleanup() { rm -rf -- "$scratch"; }
  trap cleanup EXIT
  timeout --signal=KILL 300 /usr/sbin/runuser -u bench -- \
    "$HERE/sandbox-profile.sh" patch "$repo" "$scratch" "$bundle" -- \
    /bin/bash /lane-patch.sh --inside "$base" /base.bundle /input /scratch
  /usr/bin/python3 - "$scratch/out.diff" "$out" <<'PY'
import os, secrets, stat, sys
source, destination = sys.argv[1:]
parent, name = os.path.split(os.path.abspath(destination))
if not name or name in ('.', '..'):
    raise SystemExit('invalid patch result path')
src = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
try:
    if not stat.S_ISREG(os.fstat(src).st_mode): raise SystemExit('patch output is not regular')
    dfd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    temp = f'.{name}.tmp.{os.getpid()}.{secrets.token_hex(8)}'
    try:
        dst = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=dfd)
        try:
            while True:
                block = os.read(src, 1024 * 1024)
                if not block: break
                view = memoryview(block)
                while view:
                    written = os.write(dst, view); view = view[written:]
            os.fsync(dst)
        finally: os.close(dst)
        os.replace(temp, name, src_dir_fd=dfd, dst_dir_fd=dfd)
    except BaseException:
        try: os.unlink(temp, dir_fd=dfd)
        except FileNotFoundError: pass
        raise
    finally: os.close(dfd)
finally: os.close(src)
PY
else
  # This branch is used on development hosts; production invokes the wrapper as root.
  scratch=$(mktemp -d)
  trap 'rm -rf -- "$scratch"' EXIT
  timeout --signal=KILL 300 "$HERE/sandbox-profile.sh" patch "$repo" "$scratch" "$bundle" -- \
    /bin/bash /lane-patch.sh --inside "$base" /base.bundle /input /scratch
  install -m 0644 "$scratch/out.diff" "$out"
fi
