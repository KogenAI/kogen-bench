.PHONY: setup build check format

setup:
	./setup.sh

build:
	. ./toolchain-env.sh && zig build -Doptimize=ReleaseFast
	mkdir -p build/bin
	cp zig-out/bin/kogen build/bin/kogen

check:
	. ./toolchain-env.sh && zig fmt --check build.zig src/*.zig
	. ./toolchain-env.sh && zig test src/main.zig

format:
	. ./toolchain-env.sh && zig fmt build.zig src/*.zig
