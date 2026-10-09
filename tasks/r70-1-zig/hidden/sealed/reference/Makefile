ZIG ?= zig
export PATH := /srv/bh/bench/toolchains/zig-0.17.0:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/zig-0.17.0
export LANG := C.UTF-8
export ZIG_GLOBAL_CACHE_DIR := $(CURDIR)/.zig-global-cache
export ZIG_LOCAL_CACHE_DIR := $(CURDIR)/.zig-local-cache

.PHONY: build check format setup
setup:
	./setup.sh
build:
	$(ZIG) build -Doptimize=ReleaseFast --prefix build
check:
	$(ZIG) fmt --check build.zig src
	$(ZIG) build test
format:
	$(ZIG) fmt build.zig src
