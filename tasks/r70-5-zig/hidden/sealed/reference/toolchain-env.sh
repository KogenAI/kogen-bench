#!/bin/sh
set -eu

if [ -x /srv/bh/bench/toolchains/zig-0.17.0/zig ]; then
    ZIG_BIN_DIR=/srv/bh/bench/toolchains/zig-0.17.0
elif [ -n "${HOME:-}" ] && [ -x "$HOME/.local/share/mise/installs/zig/0.17.0/zig" ]; then
    ZIG_BIN_DIR="$HOME/.local/share/mise/installs/zig/0.17.0"
else
    echo "zig 0.17.0 is not installed at the pinned toolchain path" >&2
    exit 1
fi

export PATH="$ZIG_BIN_DIR:/usr/bin:/bin:/usr/sbin:/sbin"
export BENCH_EXTRA_PATH="$ZIG_BIN_DIR"
export LANG=C.UTF-8
export ZIG_GLOBAL_CACHE_DIR="$(pwd)/.zig-global-cache"
export ZIG_LOCAL_CACHE_DIR="$(pwd)/.zig-cache"
