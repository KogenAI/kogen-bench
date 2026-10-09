#!/bin/sh
if [ -x /srv/bh/bench/toolchains/zig-0.17.0/zig ]; then
    ZIG_BIN='/srv/bh/bench/toolchains/zig-0.17.0/zig'
else
    ZIG_BIN="${HOME}/.local/share/mise/installs/zig/0.17.0/zig"
fi
ZIG_ROOT=$(dirname -- "$ZIG_BIN")
export ZIG_BIN
export PATH="$ZIG_ROOT:/usr/bin:/bin:/usr/sbin:/sbin"
export BENCH_EXTRA_PATH="$ZIG_ROOT"
export LANG='C.UTF-8'
export ZIG_GLOBAL_CACHE_DIR="${PWD}/.cache/zig-global"
export ZIG_LOCAL_CACHE_DIR="${PWD}/.cache/zig-local"
