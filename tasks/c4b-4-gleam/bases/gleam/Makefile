# The benchmark runner supplies Gleam on PATH.
export ERL_FLAGS := +S 2:2 +A 1
export LANG := C.UTF-8
.PHONY: build check test
build:
	rm -rf build
	rm -f bin/app
	gleam build --warnings-as-errors
	mkdir -p bin
	cp launcher.sh bin/app
	chmod +x bin/app
check:
	rm -rf build
	gleam format --check src test
	gleam build --warnings-as-errors
	gleam test
test:
	rm -rf build
	gleam test
