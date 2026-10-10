# Gleam base

This project uses Gleam 1.18.1 on Erlang/OTP 29. Build it with `make build`;
the command creates `./bin/app`. `make check` checks formatting, builds with
warnings as errors, and runs the public tests. `make test` runs those tests.

The exact Gleam 1.0.5 standard library, Gleam JSON 3.1.0, and Gleeunit 1.11.0
sources are included in `vendor/` and referenced as local path dependencies.
Builds do not need Hex or network access. The launcher starts the BEAM with
`+S 2:2` to keep startup resource use bounded. The native helper builds against the installed Erlang/OTP 29 headers.
It only removes the BEAM-owned `erl_child_setup` helper before process exit so
the launcher leaves no child behind. The helper is identified by its process
name and parent PID, signaled through a pidfd where supported, and reaped by
the BEAM runtime. `inetrc` selects local file lookup so Erlang does not start a
network resolver helper.

The base application is intentionally a placeholder. It writes a fixed
`NOT_IMPLEMENTED` JSON error to stderr and exits with status 70.
