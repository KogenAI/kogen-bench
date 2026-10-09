ZIG ?= zig
ZIG_TOOLCHAIN_BIN ?= /srv/bh/bench/toolchains/zig-0.17.0
ROOT := $(CURDIR)
export ZIG_GLOBAL_CACHE_DIR := $(ROOT)/.cache/zig-global
export ZIG_LOCAL_CACHE_DIR := $(ROOT)/.cache/zig-local
export PATH := $(ZIG_TOOLCHAIN_BIN):/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := $(ZIG_TOOLCHAIN_BIN)
export LANG := C.UTF-8

.PHONY: build check format setup
setup:
	./setup.sh
build:
	$(ZIG) build -Doptimize=ReleaseFast
	mkdir -p build/bin
	cp zig-out/bin/eventlog build/bin/eventlog
	chmod u+x build/bin/eventlog
check:
	$(ZIG) fmt --check build.zig src/main.zig src/core.zig
	$(ZIG) build test
format:
	$(ZIG) fmt build.zig src/main.zig src/core.zig
