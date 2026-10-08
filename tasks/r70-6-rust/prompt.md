# Task 6: JSONL job event log and reconciliation

Implement `eventlog`, which appends job lifecycle events to a JSON Lines file and reconciles that log into status counts. `make build` creates the executable used by `./run`; `./run` forwards arguments, stdin, stdout and stderr without building. `make check` runs the deterministic stack checks. All builds work offline.

## Event format

Each complete log line is one UTF-8 JSON object with exactly four keys: `id` (string), `type` (string), `job` (string), and `ts` (integer). Object-key order is arbitrary. Duplicate object keys are invalid. `id` matches `e-[a-z0-9]{1,16}` and is globally unique in the log. `job` matches `[a-z][a-z0-9-]{0,31}`. `ts` is an integer from 0 through 9223372036854775807. `type` is one of `created`, `started`, `completed`, `failed`. No extra keys or values of other JSON types are allowed. There is no whitespace restriction on JSON outside strings.

For each job, events describe the lifecycle `created` → `started` → exactly one of `completed` or `failed`. The events may appear in any line order. Reconcile orders events for each job by ascending `ts`; timestamps for the same job must be distinct. A missing/duplicate `created`, invalid lifecycle transition, or timestamp tie is an invalid event at the physical line containing the offending event. Jobs may be interleaved arbitrarily.

## Commands

```text
eventlog append --log PATH --event JSON
eventlog reconcile --log PATH
```

Options must appear in the shown order; extra, missing or repeated arguments are usage errors. Usage errors print exactly `eventlog: usage error\n` to stderr, no stdout, and exit 2. `append` validates the supplied event, rejects an event ID already present in any complete existing log line, then appends the compact JSON object plus LF. An empty or missing log is allowed. A nonempty existing log whose last byte is not LF is rejected as malformed, with the invalid-event error at its final physical line. On success it prints `appended ID\n` and exits 0. `reconcile` never modifies the log; a missing log is treated as empty. Any other log read or append write failure prints exactly `eventlog: cannot access log\n`, exits 1 and has empty stdout.

For both commands, invalid JSON, wrong/missing/extra/duplicate object keys, invalid field shapes or values print `eventlog:LINE: invalid event\n` and exit 1; `LINE` is the physical input line (for an append argument, line 1; for a log, its 1-based line). An unrecognized string `type` prints `eventlog:LINE: unknown event type 'VALUE'\n` and exits 1. A repeated event ID in a log prints `eventlog:LINE: duplicate event id 'ID'\n`. Lifecycle and timestamp errors print `eventlog:LINE: invalid transition for job 'JOB'\n`. These errors have empty stdout and exactly the stated stderr line. Stop at the first error in physical log order for parse/duplicate-ID validation; after all lines validate, report the first lifecycle error by ascending timestamp and then physical line.

During reconciliation, ignore a final nonempty fragment that does not end in LF, without parsing it. All earlier LF-terminated lines must be valid. An empty log therefore yields zero counts. Output is exactly five LF-terminated lines, with no stderr, and exit 0:

```text
total=N
queued=N
running=N
done=N
failed=N
```

`total` is the number of jobs with a valid `created` event. The other counts report each job's state after replay: `created` means `queued`, `started` means `running`, `completed` means `done`, and `failed` means `failed`. Counts sum to total. A log is limited to 10 MiB; behavior beyond that size is unspecified.

Stack: rust.
Build: `make build`.
Checks: `make check` runs cargo fmt --check, clippy -D warnings, cargo test.
