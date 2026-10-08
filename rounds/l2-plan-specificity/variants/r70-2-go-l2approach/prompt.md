# Task 2 — process-tree supervision

Implement an executable named `kogen` with this command line:

```
kogen supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]
```

Both values are base-10 integers from 1 through 60000. `COMMAND` is required. Invalid, unknown, repeated or missing options print `error: invalid arguments\n` to stderr and return 2. Start the command without a shell in a new process group; descendants inherit that group. Forward the command tree's stdout and stderr byte-for-byte to the supervisor's corresponding streams.

The supervisor does not read stdin. The launched command receives an empty stream from `/dev/null` and immediate EOF; bytes written to the supervisor's stdin are ignored.

If the whole group completes before N milliseconds, reap the direct child and return its normal exit status (0–255) or 128+signal. Print exactly `status=exited exit_code=E term_sent=false kill_sent=false reaped=R\n` on stderr after forwarding child stderr. R is 1 when the direct child was reaped and 0 otherwise. A normal successful invocation reports 1.


The options must occur once each, in the order shown, before the literal `--`; at least one argument must follow `--`. Each option value must contain only ASCII decimal digits (no sign or whitespace), parse to 1..60000, and have no leading restriction. The option parser consumes every argument through `--`; malformed or extra options before it are invalid. Everything after `--` is passed as the command and its arguments without interpretation.

If the syntactically valid `COMMAND` cannot be started as an executable, write exactly `error: cannot start command\n` to stderr, write nothing to stdout, emit no status line, and return 127.

Use a monotonic clock. The timeout begins immediately after the command process is started. At the timeout boundary, if the process group still has a live member, the invocation is a timeout. A process is live unless its Linux `/proc` state is `Z` or `X`; zombies do not keep the group alive. “Whole group completes” means no live member remains, even if the direct child has already exited. On ordinary completion, wait for and reap the direct child before printing status. Its exit code is its normal code, or 128 plus the signal number if it died from a signal. For timeout, send SIGTERM to the process group, wait the full grace interval, and send SIGKILL only if a live member remains at the end of that interval. After SIGKILL, wait until the group has no live members and reap the direct child before returning. The timeout result is always 124. `reaped` is `1` if the direct child was waited successfully and `0` otherwise; successful runs and completed timeouts must report `1`.

For process-group signaling, signal number 15 is SIGTERM and 9 is SIGKILL. The status line is written by the supervisor to stderr only after all command output has been forwarded. It is the final bytes written to stderr. Status lines and all fixed diagnostics are UTF-8/ASCII with one final LF. No other bytes are written by the supervisor. A command's own bytes are unchanged.

The implementation must correctly handle 50 simultaneous invocations, each supervising a sleeping command tree. After all 50 complete, the test checks each recorded process group and requires that no live member remains. Tests also measure peak RSS during this load.

Stack: Go.
Build: `make build`.
Checks: `make check` runs gofmt, go vet, golangci-lint, go test.

## Plan (provided)

# Plan

Use the existing Go entry point in `main.go` and replace the placeholder in `core.go` with a supervisor. Change the current buffered `execute` result so command output can be forwarded as it arrives, while the entry point handles the final exit code and fixed diagnostics.

Parse only the required `supervise` syntax: accept the two decimal options once, in order, before `--`, validate their ranges, and pass all remaining arguments unchanged. Start the executable directly with `os/exec`, place it in a new process group, and give it `/dev/null` as stdin.

Forward stdout and stderr concurrently without buffering whole streams. Track group liveness independently of the direct child by inspecting Linux `/proc` entries for the process group and treating `Z` and `X` states as dead. Use Go’s monotonic timer for the timeout and grace interval. On timeout, signal the group with SIGTERM, then SIGKILL only if a live member remains after the full grace period; wait for the group to finish and reap the direct child before reporting.

Keep spawn errors separate from status reporting. For completed runs, derive the child’s normal exit code or signal-based status, then write the required final status line to stderr only after forwarded output is complete. Streaming output keeps per-invocation memory use low during concurrent supervision.