#!/bin/sh
set -eu

repo=$(git rev-parse --show-toplevel)
script=$repo/reproduce/check-like-cloudflare.sh
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

expect "55cb369" fail "$script" "$old_commit"
expect "new commit" pass "$script" "$new_commit"
