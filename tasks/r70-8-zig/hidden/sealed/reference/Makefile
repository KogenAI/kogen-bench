ZIG_BIN := $(shell if [ -x /srv/bh/bench/toolchains/zig-0.17.0/zig ]; then printf '%s' /srv/bh/bench/toolchains/zig-0.17.0/zig; else printf '%s/.local/share/mise/installs/zig/0.17.0/zig' '$(HOME)'; fi)
ZIG_ROOT := $(dir $(ZIG_BIN))
export PATH := $(ZIG_ROOT):/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := $(ZIG_ROOT)
export LANG := C.UTF-8
export ZIG_GLOBAL_CACHE_DIR := $(CURDIR)/.cache/zig-global
export ZIG_LOCAL_CACHE_DIR := $(CURDIR)/.cache/zig-local

.PHONY: build check format setup
setup:
	./setup.sh
build:
	$(ZIG_BIN) build -Doptimize=ReleaseFast --prefix build
check:
	$(ZIG_BIN) fmt --check build.zig src/main.zig
	$(ZIG_BIN) build -Doptimize=ReleaseFast --prefix build
	$(ZIG_BIN) test src/main.zig
format:
	$(ZIG_BIN) fmt build.zig src/main.zig
