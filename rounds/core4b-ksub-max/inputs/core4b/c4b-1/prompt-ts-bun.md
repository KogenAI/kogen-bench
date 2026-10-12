# Resumable build queue

Implement a durable local build queue in the requested language. `make build`
produces `./bin/app`; builds and checks work offline. Queue logic, persistence,
and scheduling must be in process, in that language. No database or network.
Linux process APIs, libc FFI, and subprocesses used solely for locking, signaling,
or supervising an argv command are permitted. Do not delegate queue logic to
another language. The runtime supplies `flock`, `setsid`, `/bin/sh`, and `/proc`.

## Commands and framing

```
./bin/app init --root DIR
./bin/app enqueue --root DIR --manifest REL
./bin/app run --root DIR [--grace-ms N]
./bin/app status --root DIR
./bin/app events --root DIR
```

Command comes first; subsequent arguments are flag/value pairs in any order.
Unknown, repeated, inapplicable, missing or empty flags/values are USAGE. Root
may be absolute or relative. Manifest must obey the relative-path grammar below; an invalid CLI manifest
path is USAGE. It is resolved beneath root. There is
no help command. N matches `[0-9]+`, range 10..1000, default 100; leading zeroes
are accepted. Validate CLI before touching root. There are no timestamps.
Every output row is exactly one JSON object followed by LF. Object member order
is immaterial; include exactly the documented keys. Empty stderr on success.
No worker stdout/stderr may reach app stdout/stderr; discard it or store it
beneath root. Workers receive EOF on stdin.

Errors have empty stdout and exactly one LF-terminated stderr object:
`{"error":{"code":"CODE","message":"nonempty human-readable text"}}`.
Message wording is free. Codes/exits: USAGE/2, INVALID_MANIFEST/3, LOCK_BUSY/4,
NOT_INITIALIZED/5, DUPLICATE_JOB/6, IO_ERROR/7. The skeleton returns
NOT_IMPLEMENTED/70; replace it. A `run` that completes one or more failed or
conflicted jobs in THIS invocation exits 1 with its normal stdout and empty
stderr; otherwise exits 0. Old terminal jobs do not affect the exit code.
An operational IO error during run may follow already printed event rows.

Except `init`, root must already be initialized; otherwise NOT_INITIALIZED.
Init creates root and parents if needed. All commands use one exclusive,
nonblocking root lock held through their entire operation. A competing command
returns LOCK_BUSY promptly (within 1 second), including status/events. The lock
must release automatically after SIGKILL. Don't replace its inode. Syntactic
errors precede lock errors, which precede initialization/manifest errors.
Invalid enqueue and DUPLICATE_JOB must not change logical state or consume a
queue position. Manifests and runtime paths are non-hostile regular files and
directories except for the target symlink described below; input files may be
changed or removed externally. No storage corruption or hostile symlinks are
in scope. All app-owned files, logs, lock files and temporaries are under root.
Executing system programs and reading `/proc` is permitted.

## Initialization and manifest

Init prints `{"initialized":true}` on first initialization and
`{"initialized":false}` subsequently. It creates `inputs/` and an empty target
view at `target/`. Target is a symlink to an immutable directory beneath root;
readers access it with ordinary filesystem APIs. Preserve state on repeat init.
Users supply regular source files in root/inputs and a manifest beneath root.
Manifest is UTF-8 JSON, at most 1 MiB, with exactly this schema:

```
{"id":"job-a","inputs":["a.txt"],"steps":[
  {"id":"compile","deps":[],"argv":["/bin/sh","-c",
    "mkdir -p out; cat in/a.txt > out/a.bin"],
   "outputs":["a.bin"],"timeout_ms":1000}
]}
```

Job and step IDs match `[a-z][a-z0-9_-]{0,31}`. Inputs: 0..32 distinct relative
paths, each naming an existing regular file under root/inputs at enqueue.
Steps: 1..32 records, distinct IDs. Each has exactly id, deps, argv, outputs,
timeout_ms. Deps: distinct existing other step IDs forming a DAG. Argv: 1..32
nonempty strings without NUL, each at most 4096 UTF-8 bytes; first is an
absolute executable path (existence is checked when executed, not enqueue).
Timeout_ms is a JSON integer, never boolean or float, range 20..10000.
Outputs: 1..32 distinct relative paths. Across ALL steps output paths must be
unique and no output path may be an ancestor of another output path.
Relative paths are ASCII, length 1..128, consisting of slash-separated nonempty
components matching `[A-Za-z0-9_.-]+`; no component is `.` or `..`; no leading
or trailing slash. Input paths also cannot be ancestors of each other.
Unknown keys, wrong types, duplicate JSON object keys, nonfinite numbers,
cycles, invalid paths, missing source files, or duplicate IDs/deps/paths give
INVALID_MANIFEST. Malformed JSON does too. Non-readable manifest is IO_ERROR.
Validate the entire manifest and input files before checking DUPLICATE_JOB.
Job IDs are permanently unique, including terminal jobs.

Enqueue durably copies input BYTES and stores SHA-256 of each original file,
not mtime/size. Store an immutable copy of the manifest; editing the manifest
later has no effect. Each accepted job gets a consecutive integer position,
starting at 1, and status queued. Print `{"queued":"job-a","position":1}`.
Hash and snapshot correspond to the same bytes read at enqueue; external
changes during that read itself are outside scope. Crash hooks below make
lost enqueue responses unambiguous through status.

## Scheduling and step receipts

Run drains nonterminal jobs serially in increasing position. There is no
parallel step execution. A job becomes running once, then choose the
lexicographically smallest ready step ID, where every dependency is done.
Manifest array order is irrelevant. Workers run in a private, persistent
workspace beneath root. It contains `in/PATH` with the immutable input snapshot
and `out/PATH` containing all earlier completed outputs. It starts with an empty
out directory. Environment is inherited with `BUILD_JOB_ID` and `BUILD_STEP_ID`
set to current IDs. Cwd is that workspace. Relative files used by workers stay
there. Workers are trusted commands, not a security sandbox; tests use only
declared outputs plus disposable temporary files inside the workspace.

After worker exit 0, every output declared by that step must be a regular file.
A missing/nonregular output fails the job with reason missing_output. Execute
failure (including a nonexistent executable or signal termination) gives
worker_exit. No downstream step executes after failure. Timeout gives timeout.
A success receipt is durably committed BEFORE a step_done event is visible.
Once committed, the step and its output bytes never execute again on resume.
An interrupted step without a receipt may execute again; remove ALL its declared
output paths before rerunning it. Retain the same workspace and its other
temporary files on resume; workers may manage their own temporary files. Completed outputs stay unchanged by later
workers (trusted worker assumption). Failed/conflicted/landed jobs are terminal
and never rerun. Terminal failures preserve the entire previous target view.

Supervise the actual worker and EVERY descendant, including ones that change
session/process group. Enforce each timeout using monotonic elapsed time from
worker launch, with tolerance 500 ms. On timeout send TERM to all descendants,
wait grace-ms, then KILL survivors and reap. Even after worker success/failure,
clean up surviving descendants with the same bounded escalation before recording
the outcome. A surviving child does not itself turn an exit-0 worker into a
failure. No descendants or zombies remain after app exit. If the queue process
is SIGKILLed during a worker, a surviving guardian must terminate and reap the
worker tree within grace-ms + 1500 ms; a new run may return LOCK_BUSY during that
cleanup, but must be able to resume afterwards. Linux subreapers and/or scanning
/proc are suitable; process group killing alone is insufficient. External
SIGTERM/SIGINT of app are outside scope; power loss and kernel failure are outside
scope. SIGKILL may occur at arbitrary times. Persisted successful receipts and
published targets survive; transient unreceipted declared outputs are safely discarded.

## Input CAS and atomic landing

When a running job has all steps done, rehash EVERY declared file in root/inputs.
Different bytes, removal or replacement with a nonregular file conflicts the
job with reason inputs_changed; equal bytes with a new inode/mtime do not.
No refresh/rebuild on conflict. Snapshot bytes were used throughout execution.
Check even inputs not used by argv, and empty input lists always match.
Only changes completed before the CAS check are in scope; the pause hook below
occurs BEFORE that check. No external write races during the hash read or
between the check and symlink publication are in scope.

Prepare a fresh immutable target directory containing the previous target's
regular files merged with this job's declared outputs (outputs overwrite matching
paths; preserve unrelated files). If a prior file/directory blocks an output
path, replace the blocking subtree to install that output; if an output replaces
a directory, discard that subtree. Publish by ONE atomic symlink rename at
target. A reader holding a resolved old directory may keep reading it. A reader
that resolves target once sees the complete old or complete new directory, never
a partial generation. Never alter a published directory. Fsync files AND parent
directories for durable transitions, including the target switch. Recovery must
recognize a published generation belonging to this job, finalize its landed
status/event, and never rebuild or republish it. The switch is irreversible:
input changes after publication do not invalidate it. Crash before publication
keeps the previous target; crash after publication keeps the complete new one.

## Status and event journal

Status prints one object `{"jobs":[JOB,...]}` sorted by position. Each JOB has
exactly `id`, `position`, `status`, `reason`, `done`. Status is queued, running,
landed, failed, or conflict. Reason is null except for failed/conflict as above.
Done is the array of successful step IDs sorted lexicographically. Status and
events are read-only and MUST NOT perform crash reconciliation. Run reconciles.
An empty queue is `{"jobs":[]}`.

All transitions atomically commit a durable event with the state they describe.
Events are objects with exactly `seq`, `event`, `job`, `step`, `reason`.
Seq is consecutive positive integer starting at 1, globally, never reused.
Events: queued, started, step_done, landed, failed, conflict. Job is its ID;
step is nonnull only for step_done; reason is nonnull only for failed/conflict.
A job has exactly one queued, at most one started, one step_done per completed
step, and at most one terminal event. Event order follows scheduling above.
Enqueue prints only its response, not the event. Events command prints ALL
journal events, one per line, in seq order; empty journal gives empty stdout.
Run prints only the events committed by this invocation (including recovered
landing), as they commit, then one final row `{"event":"drained","remaining":0}`.
No queued rows are printed by run. Resume never prints old journal rows again.
A crash can lose a stdout event but must never lose/duplicate its journal entry.
If a committed receipt is ahead of its journal due to implementation-internal
recovery, reconcile them as one logical transaction before any subsequent
step or terminal event; documented hooks always expose consistent state.

## Crash and pause hooks

At each boundary, if APP_CRASH_AT equals its name, terminate the queue process
by real SIGKILL immediately. If APP_PAUSE_AT equals it, atomically write
root/hook.ready containing the name + LF, then wait indefinitely holding the
lock. The tester removes old markers. Crash takes precedence. Unknown/unset
values have no effect. Hooks are per invocation and fire only when that
invocation reaches the corresponding transition; no replay for old transitions.

* after_enqueue: full enqueue state/event/snapshot durable, before response.
* after_start: started state/event durable, before the first uncompleted step.
* after_launch:STEP: worker actually launched, before awaiting its exit.
* after_step:STEP: receipt, output bytes and step_done event durable, before stdout.
* before_land: all receipts durable; before the final input CAS check.
* after_publish: target switch durable, BEFORE landed state/event is committed.
* after_land: landed state/event durable, before stdout.

Run must reconcile a publication BEFORE considering any remaining hook/CAS.
For after_launch, publish readiness only after the actual argv process exists;
an executable launch failure does not reach this hook. `init`, status, events
have no hooks. Ordinary commands with <=32 steps finish within 2 seconds plus
sum of worker timeouts and cleanup grace periods. Individual worker fixtures
are small and <=64 KiB per file. Each complete test has a 90-second limit;
the complete black-box suite has a 900-second limit, including hanging
implementations. Remaining tests fail when that suite deadline is reached. Behavior above these
bounds is unspecified. Implement public unit tests as useful; no network needed.

Stack and checks: TypeScript/Bun; build with `make build`.
`make check` runs strict tsc --noEmit, biome check, bun test; `make test` runs public tests.
