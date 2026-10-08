export PATH := /srv/bh/bench/toolchains/go-1.27.1/bin:/usr/bin:/bin:/usr/sbin:/sbin
export BENCH_EXTRA_PATH := /srv/bh/bench/toolchains/go-1.27.1/bin
export LANG := C.UTF-8
export GOROOT := /srv/bh/bench/toolchains/go-1.27.1/go
export GOMODCACHE := /srv/bh/bench/toolchains/go-1.27.1/cache/gomodcache
export GOPROXY := off
export GOFLAGS := -mod=mod
export GOCACHE := $(CURDIR)/.cache/go
export GOLANGCI_LINT_CACHE := $(CURDIR)/.cache/golangci
export GOTOOLCHAIN := local

.PHONY: build check format setup
setup:
	./setup.sh
build:
	mkdir -p build/bin
	go build -buildvcs=false -trimpath -o build/bin/loop .
check:
	test -z "$$(gofmt -l .)"
	go vet ./...
	golangci-lint run
	go test ./...
format:
	gofmt -w .
