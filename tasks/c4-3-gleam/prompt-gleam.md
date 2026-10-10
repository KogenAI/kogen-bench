# Process supervisor

Implement a Linux process supervisor. Build offline with `make build`, producing `./bin/app`. `make check` and `make test` must work. Implement the lifecycle in the requested language; Linux syscall/FFI bindings and private helper processes implemented in that language are allowed. Do not delegate supervision to an external program or interpreter.

## Invocation and files

`./bin/app run --root DIR --spec RELATIVE_FILE`

The two flags may appear in either order, exactly once. No other public commands, flags or positional arguments are accepted. Private helper entry points are permitted. DIR must already be a directory; resolve it to its physical absolute path. The spec must resolve to a regular file inside that root, including after resolving symlinks. RELATIVE_FILE cannot be empty, absolute, contain a `..` component or NUL. Executable commands are absolute paths and are exempt from root containment. Application file reads/writes other than executables, system process metadata and `/dev/null` must stay under root. Child programs are trusted with respect to file access. Do not create supervisor state files.

Errors have empty stdout and exactly one LF-terminated JSON object on stderr:
`{"error":{"code":"CODE","message":"nonempty explanation"}}`.
Use UTF-8 and LF framing, with no raw CR. Message wording and JSON key order are free. Codes and exit status:

| Code | Status | Condition |
| --- | --- | --- |
| USAGE | 2 | invalid CLI |
| ROOT_ERROR | 3 | missing, inaccessible or non-directory root |
| PATH_ERROR | 3 | invalid/escaping spec path |
| IO_ERROR | 3 | spec absent, not regular or unreadable |
| INVALID_SPEC | 4 | invalid JSON or schema |
| INTERNAL_ERROR | 70 | unrecoverable supervision infrastructure failure |

Validate CLI, then root, then spec path, then read spec, then its entire schema. No child may start on any validation error. Duplicate input JSON keys, inaccessible executables and unrecoverable OS resource exhaustion are outside the tested domain. The initial skeleton returns NOT_IMPLEMENTED/status 70.

## JSON spec

The top-level object has exactly one key, `children`, an array of 0..32 objects. Each child has exactly these five required keys:

```json
{"id":"worker","command":"/bin/sleep","args":["60"],"timeout_ms":600,"grace_ms":300}
```

* `id`: unique ASCII string matching `[A-Za-z][A-Za-z0-9_-]{0,31}`.
* `command`: nonempty absolute executable path, with no NUL. Execute it directly, with `args` as individual arguments; no shell interpolation.
* `args`: array of strings, no NUL; empty strings and Unicode are valid.
* `timeout_ms`: integer 0..60000. Zero disables the timeout. Each child's deadline starts at successful process creation and uses a monotonic clock.
* `grace_ms`: integer 0..5000.

For valid numeric fields, inputs use plain nonnegative decimal JSON integer tokens. Reject booleans, nulls, strings, negative values, out-of-range values and ordinary fractional values such as 1.25. Integral decimal/exponent spellings such as 1.0 or 1e2, and fractions that round to integers in binary floating point, are outside the tested domain. Unknown keys are invalid. Each child runs exactly once, with cwd set to the physical root and the inherited supervisor environment.

## Processes and cleanup

Run the children concurrently, each as leader of a fresh process group. Redirect child stdin, stdout and stderr to `/dev/null`. The tracked process is the executable itself, not a shell or monitor. Preserve its exact wait status: an exit value 0..255 differs from a terminating signal (positive Linux signal number).

On a child's deadline, emit `timed_out` once and send SIGTERM to its whole group and descendants. On SIGTERM to the supervisor, stop starting children and perform the same cleanup for every live child, without `timed_out`. Cleanup also runs when the tracked process exits normally or crashes: terminate and reap any descendants it left behind. Do not wait for its original timeout to clean up leftovers.

Scan descendants before sending the initial cleanup signals. Send SIGTERM to the original group and individually to descendants in other groups, including ones that called setsid/setpgid. After grace_ms from those initial SIGTERM sends, send SIGKILL to remaining group members and descendants. **Zero grace still sends all initial SIGTERMs before any SIGKILL**; it does not guarantee time for handlers to run. A cooperative handler may exit during grace with any code: report that code, not an invented signal or timeout code.

Use orphan adoption (e.g. Linux PR_SET_CHILD_SUBREAPER) and reap every descendant before finishing the child. This includes double-forked orphans and descendants that escape their original group. No live processes or zombies from a child may remain when its terminal event is emitted or the supervisor exits. Descendant wait statuses do not produce public events. Child programs finish creating descendants before cleanup begins; spawning new descendants after the first cleanup SIGTERM is outside the contract.

On normal completion, including nonzero child exits and crashes, exit 0. Empty children also completes with exit 0 and no output. On SIGTERM, wait for all cleanup/reaping and exit **143**, with empty stderr. Only one shutdown SIGTERM is in the tested domain, delivered after at least one `started` event. SIGKILL to the supervisor and broken output pipes are outside the contract.

## Events

stdout contains exactly one LF-terminated JSON object per line, flushed promptly, and no other output. Use UTF-8, with no CR framing, blank lines or multiline JSON. Every event has exactly `id`, `seq`, `event` plus the additional fields below. `id` is the input child ID; `seq` is a per-child contiguous integer counter beginning at 1. There are no timestamps.

| event | Additional fields |
| --- | --- |
| started | `pid`: positive integer, the tracked executable PID |
| exited | `code`: exact integer exit value 0..255 |
| signaled | `signal`: exact positive terminating signal |
| timed_out | none |

Each child has `started`, optionally `timed_out`, then exactly one `exited` or `signaled`. Publish the terminal event only after that child's descendants have been cleaned up and reaped. Reap an already-waitable tracked process before deciding to expire its deadline, so an already-observed exit wins over the timer. Cross-child interleaving is unconstrained; order and sequence numbers within each child are deterministic. Do not emit events for helper processes or individual descendants.

Example (PID illustrative):

```json
{"id":"worker","seq":1,"event":"started","pid":301}
{"id":"worker","seq":2,"event":"exited","code":7}
```

## Timing bounds used for verification

All intervals use monotonic clocks. Timeout and grace must not occur early. Verification uses 600 ms timeouts and grace values of 0, 80, 300, 600, 1000, and 1200 ms. Cooperative shutdown may take 400 ms inside a 1200 ms grace. Timeout uses `/bin/sleep`, requiring no fixture initialization. Signal-handler and process-tree scenarios wait for readiness markers before sending shutdown. Concurrent-start verification uses a release-file barrier, with no cross-child event order requirement.

The harness allows 15 s for readiness, event receipt, each supervisor completion, error response, and reader joining, with a 60 s per-test runaway guard. It imposes no tighter completion or cross-child latency bounds. Failure cleanup has a 5 s kill/reap window, including escaped groups and adopted children. Event flushing is assessed within the 15 s event guard.

For TS/Bun, the starter supplies `src/sys.ts`: raw libc prctl, waitpid/WNOHANG, kill, getpgid, setpgid, and posix_spawn bindings, with no supervision logic. Rust has predeclared libc; Go has syscall. All three can use `/proc` ancestry and a private subreaper helper per child to isolate ownership. Everything works offline without installing packages.

Stack: Gleam 1.18.1 on Erlang/OTP 29. Build offline with `make build`.
Checks: `make check` runs gleam format --check src test, gleam build --warnings-as-errors, gleam test; `make test` runs public tests.
