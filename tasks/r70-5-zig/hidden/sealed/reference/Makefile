ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: build check format setup

setup:
	"$(ROOT)/setup.sh"

build:
	cd "$(ROOT)" && . ./toolchain-env.sh && zig build -Doptimize=ReleaseFast && mkdir -p build/bin && cp zig-out/bin/kogen build/bin/kogen

check:
	cd "$(ROOT)" && . ./toolchain-env.sh && zig fmt --check build.zig src && zig build test -Doptimize=Debug

format:
	cd "$(ROOT)" && . ./toolchain-env.sh && zig fmt build.zig src
