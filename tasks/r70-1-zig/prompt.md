# Task 1 — durable serial job queue

Implement an executable named `kogen` with these commands:

```
kogen queue add --store PATH --id ID --argv JSON_ARRAY
kogen queue run --store PATH
kogen queue status --store PATH
```

Each command word is case-sensitive. `add` requires exactly one `--store`, `--id`, and `--argv` option; `run` and `status` require exactly one `--store`. Options may appear in any order after the command. Each option takes exactly one following argument. Unknown, repeated, missing, extra, or valueless options are invalid. `PATH` names a directory. IDs match `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`. `JSON_ARRAY` must be one valid JSON array containing at least one nonempty string. Its first string names an executable and later strings are passed as its arguments, without a shell. Strings containing NUL are invalid. No output is written for invalid arguments; stderr is exactly `error: invalid arguments\n` and the exit code is 2.

The directory is created, including parents, if it does not exist. Adding a job persists it before returning. A repeated ID prints exactly `error: duplicate job id\n` to stderr and exits 3. A successful add prints `queued ID\n` to stdout and exits 0. `run` and `status` print no success text to stderr. A store read, write, locking, or durability failure prints exactly `error: store failure\n` to stderr, writes no stdout, and exits 4.

The on-disk representation is implementation-defined. It must preserve job order, arguments, attempt counts, and completion results across process termination and machine restart. All three commands take an exclusive lock for the store for their full duration; calls to `add` and `status` wait while a `run` is in progress. Jobs run serially in insertion order. A `run` processes every job that is pending when it acquires the lock, continuing after failed jobs. Adding while a `run` is in progress waits and is not part of that run.

A job remains pending until its completion record is durably committed. Before each child start, durably increment and save its attempt count. If the queue process or child receives SIGKILL before the completion record is committed, the job remains pending and the next `run` starts it again; already completed jobs never run again. A crash after child exit but before commit is incomplete and is retried. Thus execution is at least once, while the store has exactly one completion record per ID. Exactly-once external side effects are not promised.

Capture child stdout and stderr separately. Decode each as UTF-8, replacing each invalid byte with U+FFFD. A normal child exit uses its exit status. A child terminated by signal N uses exit code 128+N. If the executable cannot be started, record exit code 127 and stderr text `exec failed\n`. For every completed job, print exactly one compact JSON object followed by LF, in insertion order. Its keys and order are `id` (string), `attempt` (positive integer counting starts, including starts before crashes), `exit_code` (integer), `stdout` (string), `stderr` (string), and `status` (`succeeded` exactly when exit_code is 0, otherwise `failed`). JSON strings use standard JSON escaping; do not add spaces outside strings. `run` exits 0 even when children fail. An empty queue prints nothing and exits 0.

`status` prints one line per job in insertion order: `ID pending\n`, `ID succeeded\n`, or `ID failed EXIT_CODE\n`, according to the durable record. An empty store prints nothing and exits 0. This task runs on Linux.

Stack: Zig 0.17.0.
Build: `make build`.
Checks: `make check` runs `zig fmt --check` and `zig build test`.
