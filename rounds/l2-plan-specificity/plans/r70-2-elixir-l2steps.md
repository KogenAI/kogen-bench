1. Replace the stub in `Kogen.Core.execute/1` with a parser for `supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]`. Require each option exactly once and in order; accept only ASCII decimal digits with values from 1 through 60000; require at least one command argument. Route every malformed or extra pre-`--` argument through the existing error path so it writes the required diagnostic and returns 2. Pass everything after `--` unchanged.

2. Add a process-launch and supervision layer that can execute the command directly, without a shell, in a new process group. Connect its stdin to `/dev/null`, and stream stdout and stderr byte-for-byte to their matching supervisor streams. Include a reliable launch-failure signal so an executable that cannot be started produces only the specified diagnostic and exit code 127.

3. Monitor the process group using a monotonic clock and Linux `/proc` state. Start the timeout immediately after launch, and count members in states other than `Z` or `X` as live. Continue monitoring the group even after the direct child exits.

4. On ordinary completion, wait for and reap the direct child. Derive its result from its normal exit code or `128 + signal number`. Ensure all command output has been forwarded before writing the required completion status line to stderr.

5. At the timeout boundary, check whether the group still has a live member. If so, mark the invocation timed out, send SIGTERM to the group, and wait the full grace interval. Send SIGKILL only if a live member remains then; afterward, wait for the group to have no live members and reap the direct child. Return 124 and report the signal flags and reaping result accurately.

6. Keep output handling streaming so the supervisor does not buffer whole command streams. Check that the design handles 50 simultaneous invocations of sleeping command trees without leaving live process-group members and meets the load’s peak RSS measurement.

7. Wire the implementation into the existing Elixir CLI and build flow so `make build` produces the executable `kogen`. Run `make build` and `make check` as listed in the prompt.

8. Verify prompt-derived cases: valid and invalid argument forms; direct command execution and launch failure; empty child stdin; byte-preserving stdout and stderr forwarding; normal exit and signal termination; a direct child that exits while a descendant remains; completion just before and at the timeout boundary; TERM handling with and without a remaining live member at the grace deadline; final status-line formatting and ordering; and the 50-invocation process-group and RSS check.