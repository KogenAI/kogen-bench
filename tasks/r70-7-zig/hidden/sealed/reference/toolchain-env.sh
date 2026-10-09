#!/bin/sh
if [ -x /srv/bh/bench/toolchains/zig-0.17.0/zig ]; then
	PATH="/srv/bh/bench/toolchains/zig-0.17.0:$PATH"
elif [ -x "$HOME/.local/share/mise/installs/zig/0.17.0/zig" ]; then
	PATH="$HOME/.local/share/mise/installs/zig/0.17.0:$PATH"
fi
export PATH
export LANG=C.UTF-8
export ZIG_GLOBAL_CACHE_DIR="$(pwd)/.cache/zig-global"
export ZIG_LOCAL_CACHE_DIR="$(pwd)/.cache/zig-local"
