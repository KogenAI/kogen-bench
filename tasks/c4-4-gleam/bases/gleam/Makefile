GLEAM ?= gleam
ERL_ROOT := /opt/bench/mise/installs/erlang/29.0.3
ERL_BIN := $(ERL_ROOT)/bin
ERL_NIF_INCLUDE := $(ERL_ROOT)/lib/erlang/usr/include
APP_EBIN := build/dev/erlang/changeflow_gleam/ebin
APP_PRIV := build/dev/erlang/changeflow_gleam/priv

export PATH := $(dir $(GLEAM)):$(ERL_BIN):/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := $(dir $(GLEAM)):$(ERL_BIN)
export LANG := C.UTF-8
export ERL_FLAGS := +S 1:1 +SDcpu 1 +SDio 1 +A 1

.PHONY: build check test
build:
	rm -rf build
	rm -f bin/app
	$(GLEAM) build --target erlang --warnings-as-errors
	mkdir -p $(APP_EBIN) $(APP_PRIV) bin
	$(ERL_BIN)/erlc -o $(APP_EBIN) src/workflow_os.erl
	/usr/bin/cc -std=c11 -O2 -fPIC -shared -Wall -Wextra -Werror -I$(ERL_NIF_INCLUDE) src/workflow_lock_nif.c -o $(APP_PRIV)/workflow_os_nif.so
	cp launcher bin/app
	chmod +x bin/app

check:
	$(GLEAM) format --check src test
	$(MAKE) build
	$(GLEAM) test --target erlang

test:
	$(MAKE) build
	$(GLEAM) test --target erlang
