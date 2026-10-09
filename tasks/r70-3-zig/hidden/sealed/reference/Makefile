ZIG ?= zig
ROOT := $(CURDIR)
export ZIG_GLOBAL_CACHE_DIR := $(ROOT)/.zig-global-cache
export ZIG_LOCAL_CACHE_DIR := $(ROOT)/.zig-local-cache
export LANG := C.UTF-8

.PHONY: build check setup format
setup:
	./setup.sh
build:
	$(ZIG) build --prefix build -Doptimize=ReleaseFast
check:
	$(ZIG) fmt --check build.zig src/*.zig
	$(ZIG) build test
format:
	$(ZIG) fmt build.zig src/*.zig
