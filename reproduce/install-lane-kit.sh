#!/usr/bin/env bash
# Atomically install this release's lane runtime while carrying the host task tree forward.
set -euo pipefail
umask 022

SOURCE_ROOT=$(dirname -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")")
ROOT=/srv/bh/bench
RELEASE_ID=''
while (( $# )); do
  case $1 in
    --root) (( $# >= 2 )) || { echo '--root requires a directory' >&2; exit 2; }; ROOT=$2; shift 2 ;;
    --release-id) (( $# >= 2 )) || { echo '--release-id requires a full revision' >&2; exit 2; }; RELEASE_ID=$2; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
[[ $RELEASE_ID =~ ^[0-9a-f]{40}$ ]] || { echo '--release-id must be a 40-character lowercase revision' >&2; exit 2; }
if [[ $ROOT == /srv/bh/bench && $EUID != 0 ]]; then
  echo 'install the production lane kit as root' >&2; exit 1
fi

KITS=$ROOT/kits
CURRENT=$KITS/current
[[ -d $KITS && ! -L $KITS && -L $CURRENT ]] || {
  echo 'expected an existing kits directory and current symlink' >&2; exit 1;
}
CURRENT_REAL=$(realpath -- "$CURRENT")
CURRENT_TASKS=$(realpath -- "$CURRENT_REAL/tasks")
[[ -d $CURRENT_TASKS ]] || {
  echo 'current kit must resolve to an existing tasks directory' >&2; exit 1;
}
RELEASE=$KITS/$RELEASE_ID
runtime_files=(
  reproduce/run-lane.sh reproduce/sandbox-profile.sh reproduce/lane-patch.sh
  reproduce/lane-plan.py reproduce/generate-host-plan.py reproduce/lane-receipt.py
  reproduce/lane-sample.py reproduce/lane-snapshot.py reproduce/lane-codex-info.py
  reproduce/lane_watchdog.py reproduce/candidate_revision.py reproduce/control-worker.py
  reproduce/audit_cell.py reproduce/egress-proxy.py reproduce/egress-bridge.py
  reproduce/doctor.sh reproduce/selftest-lane-hostile.sh reproduce/egress-selftest.sh
  reproduce/standard_record.py reproduce/check_standard_cell.py reproduce/cost_calc.py
  reproduce/price-table-v1.json reproduce/price-table-v1.sha256 reproduce/safe_rows.py
  reproduce/host-pins.lock reproduce/disk-floor.sh reproduce/run-controls.sh
  reproduce/validate_round.py reproduce/missing_reasons.py reproduce/run_records.py
  reproduce/partitioned_jsonl.py schema/run-record.schema.json results/missing-reasons.json
)

install_safe_rows_helper() {
  [[ $ROOT == /srv/bh/bench ]] || return 0
  local helper_dir=/root/Areas/Kogen/bench-manager/rz1-pack/rz1-export/levers/lib
  local helper=$helper_dir/safe_rows.py temporary
  mkdir -p -- "$helper_dir"
  if [[ -e $helper || -L $helper ]]; then
    [[ -f $helper && ! -L $helper ]] || {
      echo 'safe_rows helper destination must be a regular file' >&2; return 1;
    }
    if cmp -s "$SOURCE_ROOT/reproduce/safe_rows.py" "$helper"; then return 0; fi
  fi
  temporary=$(mktemp "$helper_dir/.safe-rows.XXXXXX")
  install -m 0644 -- "$SOURCE_ROOT/reproduce/safe_rows.py" "$temporary"
  mv -f -- "$temporary" "$helper"
}

switch_current() {
  python3 - "$KITS" "$CURRENT" "$RELEASE_ID" <<'PY'
import os,sys,uuid
kits,current,revision=sys.argv[1:]
if os.path.realpath(current)==os.path.realpath(os.path.join(kits,revision)):
    raise SystemExit(0)
next_link=os.path.join(kits,'.current-'+revision+'-'+uuid.uuid4().hex)
os.symlink(revision,next_link)
try:
    os.replace(next_link,current)
except BaseException:
    os.unlink(next_link)
    raise
PY
}

if [[ -e $RELEASE || -L $RELEASE ]]; then
  [[ -d $RELEASE && ! -L $RELEASE && -f $RELEASE/.complete ]] || {
    echo 'existing release is incomplete; refusing to overwrite it' >&2; exit 1;
  }
  [[ $(<"$RELEASE/.complete") == "$RELEASE_ID" ]] || {
    echo 'existing release identity does not match its directory' >&2; exit 1;
  }
  [[ -d $RELEASE/tasks ]] || { echo 'existing release task tree is unavailable' >&2; exit 1; }
  for relative in "${runtime_files[@]}"; do
    source=$SOURCE_ROOT/$relative
    destination=$RELEASE/$relative
    [[ -f $source && ! -L $source && -f $destination && ! -L $destination ]] &&
      cmp -s -- "$source" "$destination" || {
        echo "existing release differs from source: $relative" >&2; exit 1;
      }
  done
  install_safe_rows_helper
  switch_current
  printf 'Release %s already exists; current now points to the verified release.\n' "$RELEASE_ID"
  exit 0
fi

STAGE=$(mktemp -d "$KITS/.lane-kit-${RELEASE_ID}.XXXXXX")
cleanup() {
  if [[ -n ${STAGE:-} && -d $STAGE ]]; then rm -rf -- "$STAGE"; fi
}
trap cleanup EXIT
chmod 0755 "$STAGE"
mkdir -p "$STAGE/reproduce" "$STAGE/schema" "$STAGE/results" \
  "$STAGE/.git/refs/heads" "$STAGE/.git/refs/tags" "$STAGE/.git/objects/info" "$STAGE/.git/objects/pack"

# Reuse the host's task tree by reference. This keeps task assets on their
# existing paths and never opens hidden/grader or protected receipt files.
ln -s -- "$CURRENT_TASKS" "$STAGE/tasks"
for relative in "${runtime_files[@]}"; do
  source=$SOURCE_ROOT/$relative
  [[ -f $source && ! -L $source ]] || { echo "required lane file unavailable: $relative" >&2; exit 1; }
  mode=0644
  case $relative in
    *.sh) mode=0755 ;;
    reproduce/lane-patch.sh|reproduce/run-lane.sh|reproduce/disk-floor.sh|reproduce/run-controls.sh) mode=0755 ;;
  esac
  destination=$STAGE/$relative
  mkdir -p -- "$(dirname -- "$destination")"
  install -m "$mode" -- "$source" "$destination"
done

printf '%s\n' "$RELEASE_ID" > "$STAGE/.complete"
cat > "$STAGE/.git/config" <<'EOF'
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = false
EOF
printf 'ref: refs/heads/kit-release\n' > "$STAGE/.git/HEAD"
printf '%s\n' "$RELEASE_ID" > "$STAGE/.git/refs/heads/kit-release"
chmod 0755 "$STAGE/.git" "$STAGE/.git/refs" "$STAGE/.git/refs/heads"
python3 - "$STAGE" "$RELEASE" <<'PY'
import os,sys
os.rename(sys.argv[1],sys.argv[2])
PY
STAGE=''
install_safe_rows_helper
switch_current
printf 'Installed lane kit %s and preserved the existing task tree.\n' "$RELEASE_ID"
