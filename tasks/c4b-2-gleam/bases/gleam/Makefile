# The benchmark runner supplies Gleam on PATH.
export ERL_FLAGS := +S 1:1 +SDcpu 1 +SDio 1 +A 1
export LANG := C.UTF-8

.PHONY: build check test format native clean-build
build: clean-build
	rm -f bin/app
	gleam build --warnings-as-errors
	$(MAKE) native
	mkdir -p bin
	cp scripts/app.sh bin/app
	chmod +x bin/app
check: clean-build
	gleam format --check src test
	gleam build --warnings-as-errors
	$(MAKE) native
	gleam test
test: clean-build
	gleam build --warnings-as-errors
	$(MAKE) native
	gleam test
format:
	gleam format src test

clean-build:
	rm -rf build

native:
	mkdir -p build/dev/erlang/refstore/priv
	cc -std=c11 -Wall -Wextra -Werror -O2 -fPIC -shared -I/opt/bench/mise/installs/erlang/29.0.3/lib/erlang/usr/include -o build/dev/erlang/refstore/priv/runtime_cleanup.so src/runtime_cleanup.c
