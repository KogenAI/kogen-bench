export ERL_FLAGS := +S 2:2 +SDcpu 1 +SDio 1
# The benchmark runner supplies Gleam on PATH.
export LANG := C.UTF-8
ERLANG_ROOT := /opt/bench/mise/installs/erlang/29.0.3

.PHONY: clean native build check test format
clean:
	rm -rf build/dev build/prod build/lsp build/erlang-shipment
	rm -f priv/sys_nif.so
native: clean
	mkdir -p priv
	cc -std=c11 -O2 -fPIC -shared -Wall -Wextra -Werror -I$(ERLANG_ROOT)/lib/erlang/usr/include native/sys_nif.c -o priv/sys_nif.so
build: native
	gleam build --warnings-as-errors
	mkdir -p bin
	cp launcher.sh bin/app
	chmod +x bin/app
check: native
	gleam format --check src test
	gleam build --warnings-as-errors
	gleam test
test: native
	gleam build --warnings-as-errors
	gleam test
format:
	gleam format src test
