#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
    echo "usage: $0 <commit-ish>" >&2
    exit 2
fi

repo=$(git rev-parse --show-toplevel) || {
    echo "check-like-cloudflare: run inside a Git repository" >&2
    exit 2
}
commit=$(git -C "$repo" rev-parse --verify --end-of-options "$1^{commit}") || {
    echo "check-like-cloudflare: commit does not resolve" >&2
    exit 2
}
caller_home=${HOME:-}
mise_bin=$(command -v mise 2>/dev/null || true)
if [ -z "$mise_bin" ] && [ -n "$caller_home" ] && [ -x "$caller_home/.local/bin/mise" ]; then
    mise_bin=$caller_home/.local/bin/mise
fi
if [ -z "$mise_bin" ] || [ ! -x "$mise_bin" ]; then
    echo "check-like-cloudflare: mise is required (install it or add it to PATH)" >&2
    exit 127
fi
if [ -z "$caller_home" ]; then
    echo "check-like-cloudflare: caller HOME is required to locate mise caches" >&2
    exit 2
fi

scratch=$(mktemp -d "${TMPDIR:-/tmp}/check-like-cloudflare.XXXXXX") || exit 1
restricted_parent=
cleanup() {
    if [ -n "$restricted_parent" ] && [ -d "$restricted_parent" ]; then
        chmod 700 "$restricted_parent" 2>/dev/null || true
    fi
    chmod -R u+rwX "$scratch" 2>/dev/null || true
    rm -rf "$scratch"
}
trap cleanup EXIT HUP INT TERM

git_dir=$(git -C "$repo" rev-parse --path-format=absolute --git-common-dir)
source_repo=$scratch/source
if ! git clone --quiet --no-local --no-checkout "$git_dir" "$source_repo"; then
    echo "check-like-cloudflare: could not make a fresh repository clone" >&2
    exit 1
fi
if ! git -C "$source_repo" checkout --quiet --detach "$commit"; then
    echo "check-like-cloudflare: could not check out $commit" >&2
    exit 1
fi
clone=$source_repo

node_version=$(tr -d '\r\n' < "$clone/site/.node-version")
if [ -f "$clone/site/.python-version" ]; then
    python_version=$(tr -d '\r\n' < "$clone/site/.python-version")
else
    # Historical commits without a pin use the current Pages v3 default.
    python_version=3.13.3
fi
case "$node_version" in *[!0-9.]*|'') echo "check-like-cloudflare: invalid site/.node-version" >&2; exit 1 ;; esac
case "$python_version" in *[!0-9.]*|'') echo "check-like-cloudflare: invalid site/.python-version" >&2; exit 1 ;; esac

mise_data_dir=${MISE_DATA_DIR:-$caller_home/.local/share/mise}
check_npm_cache=${CHECK_NPM_CACHE:-}
minimal_path=/usr/bin:/bin:/usr/sbin:/sbin
run_build() {
    label=$1
    build_home=$2
    build_cache=$3
    log=$scratch/$label.log
    printf 'Cloudflare build (%s HOME): ' "$label"
    if (cd "$clone" && env -i \
        HOME="$build_home" \
        PATH="$minimal_path" \
        TMPDIR="$scratch" \
        MISE_DATA_DIR="$mise_data_dir" \
        MISE_STATE_DIR="$scratch/mise-state" \
        CHECK_NPM_CACHE="$check_npm_cache" \
        npm_config_cache="$build_cache" \
        "$mise_bin" exec "node@$node_version" "python@$python_version" -- \
        sh -c 'cd site && if [ -n "$CHECK_NPM_CACHE" ]; then npm ci --offline --cache "$CHECK_NPM_CACHE"; else npm ci; fi || exit 41; npm run release || exit 42') >"$log" 2>&1; then
        echo PASS
    else
        status=$?
        case "$status" in
            41)
                echo 'FAIL (npm ci)'
                tail -n 12 "$log" >&2
                ;;
            *)
                if grep -Fq 'scripts/check.py' "$log"; then
                    echo 'FAIL (site final checks)'
                elif grep -Fq 'scripts/finalize.py' "$log"; then
                    echo 'FAIL (site finalization)'
                elif grep -Fq 'astro build' "$log"; then
                    echo 'FAIL (Astro build)'
                elif grep -Fq 'npm run build' "$log"; then
                    echo 'FAIL (site preparation)'
                else
                    echo 'FAIL (release validation)'
                fi
                tail -n 12 "$log" >&2
                ;;
        esac
        return 1
    fi
}

empty_home=$scratch/home-empty
npm_cache=${check_npm_cache:-$scratch/npm-cache}
mkdir -p "$npm_cache"
mkdir -m 700 "$empty_home"
empty_status=0
run_build empty "$empty_home" "$npm_cache" || empty_status=1

restricted_parent=$scratch/restricted-parent
mkdir -m 700 "$restricted_parent"
restricted_home=$restricted_parent/home
mkdir -m 700 "$restricted_home"
chmod 000 "$restricted_parent"
restricted_status=0
run_build restricted "$restricted_home" "$npm_cache" || restricted_status=1
[ "$empty_status" -eq 0 ] && [ "$restricted_status" -eq 0 ]
