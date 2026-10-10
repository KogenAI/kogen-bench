# Durable queue starter

Implement the supplied task contract in Gleam. The starter deliberately returns
`NOT_IMPLEMENTED` (exit 70) for every invocation.

Run `make build` offline, then `./bin/app stats --state ./state`. `make check`
runs the pinned formatter, warning-clean build, and public tests; `make test`
runs the public tests. The Erlang FFI is reserved for runtime and operating
system facilities. Queue behavior belongs in Gleam.
