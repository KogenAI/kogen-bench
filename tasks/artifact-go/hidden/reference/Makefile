export GOFLAGS := -mod=mod
export GOPROXY := off
export GOTOOLCHAIN := local
export LANG := C.UTF-8
export GOCACHE := $(CURDIR)/.cache/go

.PHONY: build check format setup
setup:
	./setup.sh
build:
	mkdir -p build
	go build -trimpath -o build/app ./cmd/app
check:
	test -z "$$(gofmt -l .)"
	go vet ./...
	go test ./...
format:
	gofmt -w .
