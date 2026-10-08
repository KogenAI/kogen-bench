export PATH := /srv/bh/bench/toolchains/bun-1.4.2/bin:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/bun-1.4.2/bin
export LANG := C.UTF-8

.PHONY: build check format setup
setup:
	./setup.sh
build:
	mkdir -p build/bin
	bun build --compile --outfile build/bin/loop src/main.ts
check:
	bun ./node_modules/typescript/bin/tsc --strict --noEmit
	bun ./node_modules/@biomejs/biome/bin/biome check .
	bun test
format:
	bun ./node_modules/@biomejs/biome/bin/biome check --write .
