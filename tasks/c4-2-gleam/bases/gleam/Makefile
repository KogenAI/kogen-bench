GLEAM_ROOT ?= $(shell dirname $$(command -v gleam))
GLEAM := $(GLEAM_ROOT)/bin/gleam
ERLANG_ROOT := /opt/bench/mise/installs/erlang/29.0.3
export PATH := $(GLEAM_ROOT)/bin:$(ERLANG_ROOT)/bin:/usr/bin:/bin:/usr/sbin:/sbin
export ERL_ROOT := $(ERLANG_ROOT)
export ERL_FLAGS := +S 1:1 +SDcpu 1 +SDio 1 +A 1 +sbwt none +sbwtdcpu none +sbwtdio none

.PHONY: build check test clean launcher

build: clean
	$(GLEAM) build --warnings-as-errors
	$(MAKE) launcher

launcher:
	mkdir -p bin
	cp launcher.sh bin/app
	chmod +x bin/app

check: clean
	$(GLEAM) format --check src test
	$(GLEAM) build --warnings-as-errors
	$(GLEAM) test

test: clean
	$(GLEAM) test

clean:
	rm -rf build/dev build/prod build/lsp
	if [ -L priv ]; then rm priv; fi
