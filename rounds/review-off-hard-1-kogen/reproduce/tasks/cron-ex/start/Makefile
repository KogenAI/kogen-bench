export LANG := C.UTF-8
export MIX_ENV := test

.PHONY: setup build check format
setup:
	./setup.sh
build:
	mix compile --warnings-as-errors
	mkdir -p build/bin
	mix escript.build
check:
	mix format --check-formatted
	mix test
format:
	mix format
