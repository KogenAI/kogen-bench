# Configuration migrator starter — Gleam

Gleam 1.18.1 with Erlang/OTP 29. Run `make build` offline to create `./bin/app`; `make check` runs source formatting, a build with warnings as errors, and public unit tests. `make test` runs the public unit tests. The placeholder emits NOT_IMPLEMENTED and exits 70. Implement the task in process in Gleam; Erlang FFI is permitted.

All dependencies are included as path dependencies: gleam_stdlib 1.0.5 and gleeunit 1.11.0. They came from the pinned public toolchain package cache; upstream licences and source are retained in vendor/. No Hex registry or network access is needed. Erlang/OTP 29 includes its standard JSON module and ordinary file/Unicode facilities. The launcher runs the compiled BEAM modules with two schedulers and one async thread; it does not build on invocation.
