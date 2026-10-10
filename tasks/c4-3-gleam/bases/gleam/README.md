# Process supervisor starter

Use Gleam 1.18.1 on Erlang/OTP 29. Run `make build`, then `./bin/app run --root DIR --spec spec.json`. The starter returns NOT_IMPLEMENTED (70).
`make check` formats/checks source, builds with warnings as errors and runs public tests; `make test` runs public tests. Every build/check/test target clears compiled artifacts and recompiles; vendored sources remain in `vendor/`.
Offline path dependencies: gleam_stdlib 1.0.5 and gleeunit 1.11.0 (Apache-2.0). OTP 29 provides its JSON module.
`src/linux.gleam`, `src/c4_os.erl` and `native/sys_nif.c` provide raw Linux/glibc primitives through a thin NIF: prctl, waitpid, posix_spawn, kill, process IDs, signal notification, pipe/read/write/close and realpath. They contain no process-tree discovery, supervisor events, timeout, grace or cleanup policy. The lifecycle must be implemented in Gleam.
The native bridge compiles with the installed C compiler and OTP headers offline; it is analogous to the raw libc bindings supplied to other stacks.
BEAM initially ignores SIGCHLD; the raw `watch_signal(17)` primitive makes native-spawned children waitable. `watch_signal(15)` supplies TERM notification.
