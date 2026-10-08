export PATH := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/bin:/opt/bench/mise/installs/erlang/29.0.3/bin
export LANG := C.UTF-8
export MIX_HOME := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/mix-home
export HEX_HOME := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/hex-home
export HEX_OFFLINE := 1
export MIX_ENV := test
export ERL_FLAGS := +S 2:2
export MIX_HOME := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/mix-home
export HEX_HOME := /srv/bh/bench/toolchains/elixir-1.20.2-otp29/hex-home
export HEX_OFFLINE := 1
export MIX_ENV := test
export ERL_FLAGS := +S 2:2

.PHONY: build check format setup
setup:
	./setup.sh
build:
	mix compile --warnings-as-errors
	mkdir -p build/bin
	mix escript.build
check:
	mix format --check-formatted
	mix credo --strict
	mix dialyzer
	mix test
format:
	mix format
