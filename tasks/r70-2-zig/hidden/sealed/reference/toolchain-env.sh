#!/bin/sh
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PATH='/srv/bh/bench/toolchains/zig-0.17.0:/usr/bin:/bin:/usr/sbin:/sbin'
export BENCH_EXTRA_PATH='/srv/bh/bench/toolchains/zig-0.17.0'
export LANG='C.UTF-8'
export ZIG_GLOBAL_CACHE_DIR="$ROOT/.cache/zig-global"
export ZIG_LOCAL_CACHE_DIR="$ROOT/.cache/zig-local"
