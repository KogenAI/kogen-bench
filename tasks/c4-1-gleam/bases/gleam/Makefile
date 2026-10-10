# The benchmark runner supplies Gleam on PATH.
export ERL_FLAGS := +S 1:1 +A 1 +SDcpu 1 +SDio 1
export LANG := C.UTF-8

.PHONY: build check test format
.NOTPARALLEL:

build:
	./scripts/clear-compiled.sh
	gleam build --warnings-as-errors
	gleam export erlang-shipment
	./scripts/write-launcher.sh

check:
	./scripts/clear-compiled.sh
	gleam format --check src test
	gleam build --warnings-as-errors
	gleam test
	gleam export erlang-shipment
	./scripts/write-launcher.sh

test:
	./scripts/clear-compiled.sh
	gleam build --warnings-as-errors
	gleam test
	gleam export erlang-shipment
	./scripts/write-launcher.sh

format:
	gleam format src test
