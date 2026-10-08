## Context packet (provided)

### Relationship and flow

- The requested entry point is an executable named `kogen` with the form `kogen supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]`; it is an Elixir task built with `make build`, with `make check` running formatting, Credo, Dialyzer, and Mix tests. [prompt.md:L3-L7] [prompt.md:L26-L28]
- The public skeleton exposes `Kogen.Core.execute/1`, whose current body returns an empty string, and `Kogen.CLI.main/1`, which writes the result to `:stdio`; `Kogen.Error` carries a message and exit code, and the CLI rescue writes the message plus LF to stderr before halting. [skeleton/lib/core.ex:L1-L4] [skeleton/lib/kogen.ex:L1-L4] [skeleton/lib/kogen.ex:L38-L48]
- The command starts without a shell in a new process group, whose descendants inherit the group; the command’s stdout and stderr must be forwarded byte-for-byte to the supervisor’s corresponding streams. [prompt.md:L9-L9]
- The supervisor does not read stdin, and the command receives an empty `/dev/null` stream with immediate EOF; input written to the supervisor is ignored. [prompt.md:L11-L11]

### Invariants

- Each option must appear once, in the specified order before the literal `--`; each value must be ASCII decimal digits parsing to 1–60000, and at least one argument must follow `--`. [prompt.md:L16-L16]
- The parser consumes every argument through `--`, rejecting malformed or extra options before it; arguments after it are passed as the command and its arguments without interpretation. [prompt.md:L16-L16]
- Use a monotonic clock, starting the timeout immediately after process start; at the timeout boundary, the invocation times out if the group still has a live member. A process is live unless its Linux `/proc` state is `Z` or `X`, and group completion does not depend on the direct child remaining alive. [prompt.md:L20-L20]
- On ordinary completion, the direct child is reaped before status is printed, and its result is its normal exit code or 128 plus its signal number; the status line reports `reaped=1` when successfully waited. [prompt.md:L13-L13] [prompt.md:L20-L20]
- The exact status line goes to stderr after all command output is forwarded and is the final stderr bytes; fixed diagnostics and status lines end in one LF, and the supervisor writes no other bytes. [prompt.md:L22-L22]

### Edge cases

- Invalid, unknown, repeated, or missing options produce `error: invalid arguments\n` on stderr and return 2; signs and whitespace are disallowed in option values, while leading zeroes are not restricted. [prompt.md:L9-L9] [prompt.md:L16-L16]
- If a syntactically valid command cannot start as an executable, stderr gets exactly `error: cannot start command\n`, stdout stays empty, no status line is emitted, and the return code is 127. [prompt.md:L18-L18]
- On timeout, send SIGTERM to the group, wait the full grace interval, then send SIGKILL only if a live member remains; wait until none remain and reap the direct child before returning 124. Completed timeouts must report `reaped=1`. [prompt.md:L20-L22]
- The load requirement is 50 simultaneous invocations supervising sleeping command trees; after completion, no live member may remain in each recorded group, and peak RSS is measured. [prompt.md:L24-L24]

### Uncertainty

- The prompt defines liveness and timeout-boundary behavior but does not specify a polling cadence for detecting live group members. [prompt.md:L20-L20]