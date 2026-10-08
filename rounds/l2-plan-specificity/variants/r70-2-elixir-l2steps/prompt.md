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

Stack: Elixir.
Build: `make build`.
Checks: `make check` runs mix format --check-formatted, credo --strict, dialyzer, mix test.

## Plan (provided)

1. Replace the stub in `Kogen.Core.execute/1` with a parser for `supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]`. Require each option exactly once and in order; accept only ASCII decimal digits with values from 1 through 60000; require at least one command argument. Route every malformed or extra pre-`--` argument through the existing error path so it writes the required diagnostic and returns 2. Pass everything after `--` unchanged.

2. Add a process-launch and supervision layer that can execute the command directly, without a shell, in a new process group. Connect its stdin to `/dev/null`, and stream stdout and stderr byte-for-byte to their matching supervisor streams. Include a reliable launch-failure signal so an executable that cannot be started produces only the specified diagnostic and exit code 127.

3. Monitor the process group using a monotonic clock and Linux `/proc` state. Start the timeout immediately after launch, and count members in states other than `Z` or `X` as live. Continue monitoring the group even after the direct child exits.

4. On ordinary completion, wait for and reap the direct child. Derive its result from its normal exit code or `128 + signal number`. Ensure all command output has been forwarded before writing the required completion status line to stderr.

5. At the timeout boundary, check whether the group still has a live member. If so, mark the invocation timed out, send SIGTERM to the group, and wait the full grace interval. Send SIGKILL only if a live member remains then; afterward, wait for the group to have no live members and reap the direct child. Return 124 and report the signal flags and reaping result accurately.

6. Keep output handling streaming so the supervisor does not buffer whole command streams. Check that the design handles 50 simultaneous invocations of sleeping command trees without leaving live process-group members and meets the load’s peak RSS measurement.

7. Wire the implementation into the existing Elixir CLI and build flow so `make build` produces the executable `kogen`. Run `make build` and `make check` as listed in the prompt.

8. Verify prompt-derived cases: valid and invalid argument forms; direct command execution and launch failure; empty child stdin; byte-preserving stdout and stderr forwarding; normal exit and signal termination; a direct child that exits while a descendant remains; completion just before and at the timeout boundary; TERM handling with and without a remaining live member at the grace deadline; final status-line formatting and ordering; and the 50-invocation process-group and RSS check.