export ERL_FLAGS := +S 2:2
# The benchmark runner supplies Gleam on PATH.
export LANG := C.UTF-8
export ERL_INETRC := $(CURDIR)/inetrc

ERL_ROOT := /opt/bench/mise/installs/erlang/29.0.3/lib/erlang
NIF := build/dev/erlang/approval_desk/ebin/approval_nif.so

.PHONY: build check test format compile-nif

build:
	rm -rf build
	rm -f bin/app
	gleam build --warnings-as-errors
	$(MAKE) compile-nif
	mkdir -p bin
	cp run bin/app
	chmod +x bin/app

check:
	rm -rf build
	gleam format --check src test
	gleam build --warnings-as-errors
	$(MAKE) compile-nif
	gleam test

test:
	rm -rf build
	gleam build --warnings-as-errors
	$(MAKE) compile-nif
	gleam test

compile-nif:
	mkdir -p $(dir $(NIF))
	cc -std=c11 -O2 -fPIC -shared -Wall -Wextra -Werror -I$(ERL_ROOT)/usr/include src/approval_nif.c -o $(NIF)

format:
	gleam format src test
