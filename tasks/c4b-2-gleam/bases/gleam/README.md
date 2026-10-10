# Atomic reference store

Build offline with `make build`; run `./bin/app COMMAND --root DIR FLAGS`.
`make check` runs formatting, a warnings-as-errors build, and public tests;
`make test` runs public tests. The CLI skeleton returns NOT_IMPLEMENTED/70.
See the task statement for the contract.

Gleam 1.18.1 targets Erlang/OTP 29. Source dependencies are vendored locally:
gleam_stdlib 1.0.5, gleam_json 3.1.0 and gleeunit 1.11.0. Their dependency
paths point within vendor/, so no Hex download or toolchain cache is required.
Erlang FFI may be used for native OS facilities.

The launcher uses file-only hostname lookup and retires/reaps the unused ERTS
subprocess broker before main. This native startup code handles process signals
only; the application uses in-process facilities and does not spawn executables.
