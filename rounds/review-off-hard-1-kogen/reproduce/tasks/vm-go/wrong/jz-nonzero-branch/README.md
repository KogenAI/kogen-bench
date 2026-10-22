# kogen CLI

A dependency-free Go module. `make build` creates `build/bin/kogen`, which `./run` executes with its arguments and streams. `make check` runs the stack checks: gofmt, `go vet ./...` and `go test ./...`. Builds and checks work offline.
