# Context packet (provided)

**Command and argument flow**

- The deliverable is a Go executable named `kogen`, invoked as `kogen supervise --timeout-ms N --grace-ms N -- COMMAND [ARG ...]`. Both values must be base-10 integers from 1 through 60000, and a command is required. [prompt.md:L3-L9] [prompt.md:L26-L27]
- Each option must appear once, in the specified order before `--`; values allow ASCII digits only, with leading zeroes allowed. Missing, repeated, unknown, malformed, or extra pre-`--` options are invalid; at least one argument must follow `--`. Arguments after `--` pass through without interpretation. [prompt.md:L9] [prompt.md:L16]
- Invalid arguments produce `error: invalid arguments\n` on stderr and return 2. If a syntactically valid command cannot be started as an executable, the supervisor writes `error: cannot start command\n` to stderr, writes nothing to stdout, emits no status line, and returns 127. [prompt.md:L9] [prompt.md:L18]
- Start the command without a shell in a new process group; descendants inherit that group. The command receives `/dev/null` as stdin and immediate EOF, while input written to the supervisor is ignored. [prompt.md:L9-L11]
- **Public interface:** `main` passes command-line arguments to `execute`, writes its returned error to stderr or output to stdout, then exits with its returned code; the visible `execute` signature is `func execute([]string) (string, int, error)`. [skeleton/main.go:L32-L39] [skeleton/core.go:L1-L3]

**Lifecycle and output**

- Use a monotonic clock; the timeout starts immediately after command start. At the timeout boundary, a live group member makes the run a timeout. A process counts as live unless its Linux `/proc` state is `Z` or `X`; zombies do not keep the group alive. Whole-group completion means no live members remain, even if the direct child has exited. [prompt.md:L20]
- On ordinary completion, wait for and reap the direct child before status output. Return its normal exit code or 128 plus its signal number. [prompt.md:L13] [prompt.md:L20]
- On timeout, send SIGTERM to the group, wait the full grace interval, and send SIGKILL only if a live member remains at its end. After SIGKILL, wait for the group to have no live members and reap the direct child. A timeout returns 124. [prompt.md:L20-L22]
- A normal successful invocation reports `reaped=1`; completed timeouts must also report `reaped=1`. The prompt gives the exact ordinary-completion status format and defines `reaped` as 1 when the direct child was successfully waited, otherwise 0. [prompt.md:L13] [prompt.md:L20]
- Forward command stdout and stderr byte-for-byte to the corresponding supervisor streams. The status line goes to stderr after all command output has been forwarded and is the final stderr bytes; fixed diagnostics and status lines end in one LF. [prompt.md:L9] [prompt.md:L22]

**Edge cases and uncertainty**

- The prompt names signal numbers 15 for SIGTERM and 9 for SIGKILL, and requires handling 50 simultaneous invocations supervising sleeping command trees; afterward, each recorded group must have no live member. [prompt.md:L22-L24]
- The prompt defines the timeout boundary and live-member criterion, but does not prescribe a polling cadence or `/proc` scanning strategy. [prompt.md:L20]