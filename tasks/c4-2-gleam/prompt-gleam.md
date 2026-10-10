# Durable leased job queue

Implement a small persistent job queue for independent worker processes. Build
offline with `make build`, producing `./bin/app`; `make check` and `make test`
must succeed. Keep the queue logic in the requested language, in process.
No database, daemon, network, or subprocess-based queue implementation.
The runtime provides the `flock` utility on PATH. Subprocesses used only for
locking or signaling are permitted; queue logic must remain in process.

## CLI and JSON

```
./bin/app COMMAND --state DIR [--now-ms N] FLAGS
enqueue   --key TEXT --payload TEXT [--priority P] [--max-attempts M]
claim     --worker TEXT --lease-ms L
heartbeat --id ID --worker TEXT --token TEXT --lease-ms L
ack       --id ID --worker TEXT --token TEXT
nack      --id ID --worker TEXT --token TEXT
list      [--status all|ready|leased|acked|dead]
stats
recover
```

COMMAND must be first. There are no positional arguments after it. Flags may
appear in any order after COMMAND, each as a separate flag/value pair; repeated,
unknown, missing-value and command-inapplicable flags are usage errors. There is
no help flag. `--state` is required and nonempty. `--now-ms` is optional: absent,
sample Unix epoch milliseconds once, after acquiring the state lock; present,
use N exactly. There is no persisted clock high-water mark: time may move backward.
All times, IDs and counts in JSON are integers, never strings.

N matches `[0-9]+` and is in 0..4000000000000. L and ID match `[0-9]+`, L is
1..86400000 and ID is 1..4000000000000. M is 1..16, default 3. P matches
`-?[0-9]+`, is -1000..1000, default 0. Leading zeroes are accepted. Numeric
arguments with plus signs, spaces, fractions or exponents are invalid.
Key and worker are nonempty UTF-8 strings of at most 256 bytes. Token is any
nonempty UTF-8 string of at most 256 bytes (a well-formed but wrong token is a
lease error). Payload is a UTF-8 string of at most 65536 bytes, including empty
strings, newlines and JSON-looking text. It is not parsed as JSON. Valid input
arguments contain no NUL. Validate the entire CLI before opening state.

Success: exit 0, empty stderr, exactly one JSON object followed by LF on stdout.
No other output. Object member order is immaterial; arrays have the order specified
below. Include exactly the documented members. String escaping follows JSON.

Errors: empty stdout, exactly one LF-terminated JSON object on stderr:
`{"error":{"code":"CODE","message":"nonempty human-readable text"}}`.
Message wording is not prescribed. Error codes and exits:

| Code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | Any invalid command, flag, value or missing required flag |
| NOT_FOUND | 3 | Syntactically valid ID does not exist |
| LEASE_MISMATCH | 4 | Job is not leased, worker/token differ, or lease has expired |
| IO_ERROR | 5 | Cannot read, create, lock, persist or sync state |
| CORRUPT_STATE | 6 | Committed storage is malformed or internally inconsistent |

Syntax validation precedes all state errors; storage errors precede job lookup;
NOT_FOUND precedes lease checks. USAGE, NOT_FOUND, LEASE_MISMATCH and
CORRUPT_STATE must not change logical queue state, including expiration recovery.
IO_ERROR must leave recoverable storage representing the entire old or new
transaction; callers may retry an enqueue by key when the commit is uncertain.
Creating storage/lock directories during a failed command is permitted. The
initial skeleton uses NOT_IMPLEMENTED, exit 70; replace it for the implementation.

## Job records and responses

A job has exactly these fields (nulls must be explicit):

```
{"id":1,"key":"task-a","payload":"hello","priority":0,
 "max_attempts":3,"attempts":0,"status":"ready","available_at":1000,
 "worker":null,"lease_until":null,"token":null}
```

IDs are assigned as consecutive positive integers in committed enqueue order,
starting at 1. Jobs are retained forever, including acked and dead jobs. Key
uniqueness is permanent and byte-exact, with no Unicode normalization. Enqueue
of an existing key returns its current record and `created:false`, ignoring the
new payload, priority and max-attempts (but still validating these arguments).
It never allocates an ID or revives a terminal job. A new job has attempts 0,
status ready, available_at equal to now, and all lease fields null.

| Command | Response |
| --- | --- |
| enqueue | `{"created":true_or_false,"job":JOB}` |
| claim | `{"job":JOB_or_null}` |
| heartbeat, ack, nack | `{"job":JOB}` |
| list | `{"jobs":[JOB,...]}` sorted by increasing numeric ID; default status all |
| stats | `{"total":N,"ready":N,"delayed":N,"leased":N,"acked":N,"dead":N,"attempts":N}` |
| recover | `{"requeued":N,"dead_lettered":N}` counting expired leases handled by this invocation |

For stats, ready counts ready-state jobs with available_at <= now, delayed
counts ready-state jobs with available_at > now. Thus total equals ready +
delayed + leased + acked + dead. Attempts is the sum across ALL retained jobs.
No timestamp fields other than available_at and lease_until are emitted.

Committed records must satisfy the input ranges and string limits above, unique
keys and consecutive IDs, and these invariants: attempts is in 0..max_attempts;
ready has attempts < max_attempts; leased and acked have attempts >= 1; dead has
attempts == max_attempts. Leased records have a nonempty valid worker, an integer
lease_until, and the canonical ID:ATTEMPTS token; all other statuses have null
lease fields. Timestamps are nonnegative integers (derived deadlines may exceed
the --now-ms input bound). Any violation is CORRUPT_STATE before recovery.

## Transitions, leases and retry policy

Every successful command, including list/stats/duplicate enqueue, first recovers
ALL leases with lease_until <= now, atomically with its own operation. Recovery
on NOT_FOUND or LEASE_MISMATCH is rolled back. A lease is valid strictly before its deadline.

Claim chooses a ready-state job with available_at <= now, ordered by descending
priority, then ascending ID; it skips delayed jobs regardless of priority. If
none is eligible, return job:null. Otherwise increment attempts by 1, set status
leased, worker to the supplied worker, lease_until to now + L, and token to
`ID:ATTEMPTS` in canonical decimal, e.g. `1:2`. Claim retains available_at.
Attempts increment ONLY on a committed claim, never on nack, expiry or heartbeat.
Tokens fence stale workers even if the same worker ID is reused.

Heartbeat/ack/nack require the ID to exist and have a live lease whose worker AND
token exactly match. Heartbeat sets lease_until to max(old deadline, now + L),
retaining the other fields. Ack sets status acked. Nack fails the current attempt:
if attempts >= max_attempts set status dead; otherwise set status ready and
available_at to now + retry_delay(attempts). Ack/dead transitions retain
available_at. Whenever leaving leased, clear worker, lease_until and token to null.

`retry_delay(a) = min(100 * 2^(a-1), 10000)` milliseconds for a >= 1.
Expiry applies the same attempt limit as nack, but a retry is scheduled at the
OLD lease deadline + retry_delay(attempts), not at the later recovery time.
Expired jobs can therefore be immediately claimable on a sufficiently late
restart. Recovery processes each expired lease once; repeated recover calls do
not add retries or drift available_at. A final attempt may still be acked while
its lease is live. Terminal jobs are never claimable.

## Durability and process coordination

All runtime state files, locks, temporary files and hook markers must be beneath
DIR. Create a missing DIR and needed parents. Storage layout and format are your
choice. After a successful command and with no invocation running, tests may
corrupt state files under DIR by replacing regular-file contents with arbitrary
bytes, including garbage, `{}`, `null`, or JSON describing impossible records.
Tests may replace all regular files without assuming any particular filename or
requiring JSON storage. Treat malformed or internally inconsistent committed
data as CORRUPT_STATE, not an empty queue; missing required committed metadata is
also corruption. Temporary/uncommitted data left by a
kill must be ignored or discarded safely. Inputs stay within 1000 jobs; no
performance target beyond bounded completion is imposed. State paths are ordinary
local Linux filesystem directories, without hostile symlink manipulation.

Multiple invocations against the same DIR must serialize the complete read,
recovery, mutation and commit transaction. The serialization mechanism must be
released automatically on SIGKILL or otherwise safely recover without manual
cleanup. Concurrent duplicate enqueues create exactly one job; concurrent claims
never lease one attempt twice. Do not lock an inode that you later replace.

Each ordinary invocation must finish within 6 seconds, including lock waiting
in tested concurrent workloads. Pause hooks must publish hook.ready within
6 seconds; their intentional wait is exempt from the invocation limit. Each
complete test has a 45-second limit. Tests use --now-ms for temporal assertions
and do not assume that the wall clock is monotonic. The whole black-box suite
has a 240-second deadline, including tests of a hanging implementation; any
remaining tests fail when that deadline is reached.

Use a write-ahead log or atomic replacement with file AND directory fsync (or
equivalent durable primitives). Flush durable state before printing success.
Once an enqueue success has been emitted it must survive any later process kill;
once an ack success has been emitted the job can never be delivered again. An
interrupted transaction must be entirely old or entirely new, with IDs, unique
keys, attempts, leases and stats consistent. Committed operations whose response
was lost remain committed. Retrying enqueue by key handles this ambiguity.

Implement these test hooks for EVERY successful invocation, including reads and
no-ops. They describe logical transaction boundaries independent of storage:

* `after_lock`: exclusive serialization acquired, before reading/recovering state.
* `before_commit`: full tentative transaction prepared, before the durable commit
  point. Restart must observe exactly the old logical state.
* `after_commit`: transaction fully durable, before any stdout. Restart must
  observe exactly the new logical state.

If `APP_CRASH_AT` equals the step, immediately terminate via real SIGKILL (signal
9), with no success or error JSON. Other values have no effect. If `APP_PAUSE_AT`
equals the step, write `DIR/hook.ready` containing that step plus LF, then wait
indefinitely while retaining serialization so a test can send external SIGKILL.
The tester removes any old marker before starting. Crash takes precedence over
pause at the same step. Ignore these variables when unset. A crash before the
commit point may leave physical temporary files; it must not consume IDs or
alter queue records. A crash after commit must not require the lost response to
make the change visible. Recovery itself obeys the same durability and hooks.

An example retry sequence: enqueue at 1000, claim with L=50 at 1000 (attempt 1),
recover at 1050 schedules available_at=1150, claim at 1149 returns null, claim at
1150 produces attempt 2 and token `1:2`. Ack at its exact lease deadline fails.

Stack and checks: Gleam 1.18.1 on Erlang/OTP 29; build with `make build`.
`make check` runs gleam format --check src test, gleam build --warnings-as-errors, gleam test; `make test` runs public tests.
