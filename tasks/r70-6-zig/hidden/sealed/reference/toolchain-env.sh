#!/bin/sh
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ZIG_TOOLCHAIN_BIN=${ZIG_TOOLCHAIN_BIN:-/srv/bh/bench/toolchains/zig-0.17.0}
export ZIG_TOOLCHAIN_BIN
export PATH="$ZIG_TOOLCHAIN_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
export BENCH_EXTRA_PATH="$ZIG_TOOLCHAIN_BIN"
export LANG='C.UTF-8'
export ZIG_GLOBAL_CACHE_DIR="$ROOT/.cache/zig-global"
export ZIG_LOCAL_CACHE_DIR="$ROOT/.cache/zig-local"
