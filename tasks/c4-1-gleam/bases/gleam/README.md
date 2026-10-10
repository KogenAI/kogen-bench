# Worktree landing queue (Gleam)

Implement the contract in the supplied prompt. The starter reports
`NOT_IMPLEMENTED` (exit 70) for every invocation.

Gleam 1.18.1 on Erlang/OTP 29 builds offline from the dependency sources in
`vendor/`: gleam_stdlib 1.0.5, gleam_json 3.1.0, gleam_erlang 1.3.0 and
gleeunit 1.11.0. Erlang FFI is available for OS facilities.

Run `make build` to produce `bin/app`, `make test` for public unit tests,
and `make check` for formatting, a build with warnings as errors and unit tests.
Each target clears compiled artifacts and rebuilds from source, preserving
vendored dependency sources. The generated launcher locates its compiled modules
relative to the repository, so a copied worktree rebuilds and runs correctly.

Invoke `./bin/app list --root /tmp/queue` after implementing initialization.
