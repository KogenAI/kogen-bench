# Change workflow (Gleam)

Run `make build`, then `./bin/app COMMAND --state DIR FLAGS`.
Run `make check` for formatting, compilation, and tests, or `make test` for unit tests.
The starter deliberately returns `NOT_IMPLEMENTED` (exit 70) for every command.
The four Hex dependencies are vendored under `vendor/`, so builds work offline.

Linux locking is supplied by `src/workflow_lock_nif.c` through the Erlang
module in `src/workflow_os.erl`. `lock_exclusive` opens the stable `.lock`
file path and blocks in `flock(fd, LOCK_EX)`, retrying `EINTR`. Keep the
returned lock resource alive during the protected operation and call
`release_lock` to close it. The resource destructor also closes the fd if the
BEAM process exits first.
