export PATH := /srv/bh/bench/toolchains/zig-0.17.0:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/zig-0.17.0
export LANG := C.UTF-8
export ZIG_GLOBAL_CACHE_DIR := $(CURDIR)/.cache/zig-global
export ZIG_LOCAL_CACHE_DIR := $(CURDIR)/.cache/zig-local

.PHONY: build check format setup
setup:
	./setup.sh
build:
	zig build -Doptimize=ReleaseFast
	mkdir -p build/bin
	cp zig-out/bin/kogen build/bin/kogen
check:
	zig fmt --check src build.zig
	zig test src/main.zig -lc
format:
	zig fmt src build.zig
