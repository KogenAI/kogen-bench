#!/usr/bin/env bash
# Host-side, model-free check of patch extraction and candidate grading wrappers.
set -euo pipefail
HERE=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
KIT=$(dirname -- "$HERE")
(( EUID == 0 )) || { echo 'run hostile lane self-test as root on the host' >&2; exit 2; }
[[ -x /usr/bin/bwrap && -x $HERE/lane-patch.sh ]] || {
  echo 'host patch sandbox prerequisites unavailable' >&2; exit 2;
}
TMP=$(mktemp -d "${TMPDIR:-/tmp}/lane-hostile.XXXXXX")
chmod 0755 "$TMP"
cleanup() { rm -rf -- "$TMP"; }
trap cleanup EXIT
repo=$TMP/base
candidate=$TMP/candidate
bundle=$TMP/base.bundle
result=$TMP/result
task=$TMP/kit/tasks/hostile-lane
mkdir -p "$repo" "$result" "$task/hidden"
mkdir "$TMP/work"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
git -C "$repo" init -q
git -C "$repo" config user.name 'Hostile Lane Selftest'
git -C "$repo" config user.email 'hostile-lane-selftest'
printf 'before\n' > "$repo/tracked.txt"
printf 'ignored-large/\n' > "$repo/.gitignore"
git -C "$repo" add -A
git -C "$repo" commit -qm base
base=$(git -C "$repo" rev-parse HEAD)
git -C "$repo" bundle create "$bundle" --all
git clone -q "$bundle" "$candidate"
git -C "$candidate" checkout -q "$base"
printf 'after\n' > "$candidate/tracked.txt"
ln -s /dev/zero "$candidate/dev-zero"
mkfifo "$candidate/agent.pipe"
mkdir "$candidate/ignored-large"
dd if=/dev/zero of="$candidate/ignored-large/payload.bin" bs=1048576 count=64 status=none
sentinel=$TMP/sentinel
printf 'sentinel intact\n' > "$sentinel"
mkdir "$TMP/external-info"
ln -s "$sentinel" "$TMP/external-info/attributes"
mv "$candidate/.git/info" "$TMP/original-info"
ln -s "$TMP/external-info" "$candidate/.git/info"

timeout --signal=KILL 150 "$HERE/lane-patch.sh" "$base" "$bundle" \
  "$candidate" "$result/patch.diff"
grep -q 'tracked.txt' "$result/patch.diff"
grep -q '+after' "$result/patch.diff"
grep -q 'dev-zero' "$result/patch.diff"
! grep -q 'ignored-large' "$result/patch.diff"
! grep -q 'agent.pipe' "$result/patch.diff"
[[ $(cat "$sentinel") == 'sentinel intact' ]]

cat > "$task/hidden/grade.sh" <<'GRADE'
#!/usr/bin/env bash
set -euo pipefail
[[ $(cat /work/tracked.txt) == after ]]
[[ -L /work/dev-zero ]]
[[ ! -e /work/agent.pipe ]]
[[ -s /work/ignored-large/payload.bin ]]
printf '{"pass":true,"tests":1}\n'
GRADE
chmod 0644 "$task/hidden/grade.sh"
mkdir -p "$TMP/kit"
timeout --signal=KILL 150 /usr/bin/python3 "$HERE/control-worker.py" \
  "$TMP/kit" grade-candidate hostile-lane "$candidate" "$result" "$TMP/work"
[[ $(cat "$sentinel") == 'sentinel intact' ]]
printf 'Hostile lane self-test: PASS (patch extraction and grading completed)\n'
