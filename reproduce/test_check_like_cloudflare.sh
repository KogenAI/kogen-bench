#!/bin/sh
set -eu

repo=$(git rev-parse --show-toplevel)
script=${CHECK_SCRIPT:-$repo/reproduce/check-like-cloudflare.sh}
old_commit=${1:-55cb369}
new_commit=${2:-HEAD}

expect() {
    label=$1
    expected=$2
    shift 2
    if "$@"; then
        actual=0
    else
        actual=$?
    fi
    if [ "$expected" = fail ] && [ "$actual" -ne 0 ]; then
        printf '%s: expected failure (exit %s)\n' "$label" "$actual"
    elif [ "$expected" = pass ] && [ "$actual" -eq 0 ]; then
        printf '%s: expected success\n' "$label"
    else
        printf '%s: unexpected result (exit %s)\n' "$label" "$actual" >&2
        exit 1
    fi
}

# Regression: inside a hook from a worktree git exports an absolute GIT_DIR; the
# scratch checkout must still hold the committed files. A stub mise stands in
# for the build and records what the scratch clone contained.
tmp=$(mktemp -d "${TMPDIR:-/tmp}/test-check-like-cloudflare.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
main=$tmp/main
git init --quiet "$main"
git -C "$main" config core.hooksPath /dev/null
mkdir -p "$main/site"
echo 22.1.0 > "$main/site/.node-version"
git -C "$main" add site
git -C "$main" -c user.name=t -c "user.email=test$(printf '\100')example.invalid" commit --quiet -m init
git -C "$main" worktree add --quiet --detach "$tmp/wt"
mkdir "$tmp/bin"
cat > "$tmp/bin/mise" <<STUB
#!/bin/sh
# The build runs under env -i, so the probe path is written in here.
[ -f site/.node-version ] && echo present > "$tmp/probe"
exit 1
STUB
chmod +x "$tmp/bin/mise"
wt_git_dir=$(git -C "$tmp/wt" rev-parse --path-format=absolute --git-dir)
out=$tmp/out
(cd "$tmp/wt" && GIT_DIR=$wt_git_dir PATH="$tmp/bin:$PATH" TMPDIR=$tmp \
    "$script" HEAD >"$out" 2>&1) || true
if [ -f "$tmp/probe" ]; then
    echo "hook GIT_DIR: scratch checkout has the committed files"
else
    echo "hook GIT_DIR: scratch checkout is empty" >&2
    cat "$out" >&2
    exit 1
fi
rm -rf "$tmp"
trap - EXIT HUP INT TERM

expect "55cb369" fail "$script" "$old_commit"
expect "new commit" pass "$script" "$new_commit"
