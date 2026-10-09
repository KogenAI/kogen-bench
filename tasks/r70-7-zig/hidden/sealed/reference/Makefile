.PHONY: build check format setup

setup:
	./setup.sh

build:
	. ./toolchain-env.sh; zig build -Doptimize=ReleaseFast --prefix build

check:
	. ./toolchain-env.sh; zig fmt --check build.zig src/main.zig src/core.zig src/shared.zig
	. ./toolchain-env.sh; zig build test

format:
	. ./toolchain-env.sh; zig fmt build.zig src/main.zig src/core.zig src/shared.zig
