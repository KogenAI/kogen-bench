export ERL_FLAGS := +S 2:2
export PATH := /srv/bh/bench/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/gleam-1.18.1/bin:/opt/bench/mise/installs/erlang/29.0.3/bin
export LANG := C.UTF-8

.PHONY: setup build check format
setup:
	./setup.sh
build:
	gleam build
check:
	gleam format --check src test
	gleam check
	gleam test
format:
	gleam format src test
