## Architecture

Implement supervision in `Kogen.Core`, with `Kogen.CLI` handling the command’s stderr diagnostics and final exit code. The core should return a structured result so output streams, status text, and exit status can be handled separately; the current string-only `execute/1` interface cannot express those outcomes.

## Key implementation decisions

- Parse the exact `supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]` form with a strict positional parser. Validate each numeric value as ASCII digits in range, and preserve every argument after `--` unchanged.
- Launch the executable directly, without a shell, in a new process group. Use `/dev/null` for child stdin and a launch mechanism that distinguishes failure to exec the requested command from a command that later exits with code 127.
- Forward stdout and stderr as byte streams with bounded buffering, and finish forwarding before writing the status line. Avoid retaining command output in memory.
- Base lifecycle decisions on monotonic time and process-group liveness from Linux `/proc`, treating `Z` and `X` states as not live. A direct child’s exit alone does not complete the group.
- On completion, reap the direct child and report its normal exit code or `128 + signal`. On timeout, signal the group with SIGTERM, allow the full grace interval, send SIGKILL only if live members remain, then wait for group completion and reap the child. Emit the required status line last on stderr; keep argument errors and command-start errors on their specified diagnostic paths.