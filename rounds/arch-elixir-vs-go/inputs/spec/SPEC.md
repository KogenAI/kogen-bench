# kogen-mini external contract, version 1

This document and PROTOCOL.md specify the common ARCH build slice. DESIGN-ARCH.md is authoritative for experiment scope. Decisions here resolve its unspecified observable details. Implementations must expose the same contract regardless of language. The E arm uses an Elixir/OTP coordinator and worker core with a Go CLI; the G arm uses Go throughout. The maintenance priority extension is specified separately in MAINTENANCE.md and is not part of this base contract.

## 1. Environment and inputs

The target is macOS, with one coordinator, two separately launched worker OS processes (`w1`, `w2`), and a CLI executable named `kogen`. All communication uses localhost TCP. Git and `/bin/sh` are available. Paths in fixtures may contain spaces. Tests use temporary repositories and directories; they never use real repositories or network remotes.

A repository input is an absolute path to an existing **bare local Git repository**, with a symbolic HEAD naming an existing branch and at least one commit. Resolve symlinks to obtain its canonical path. That path is the repository identity and serialization key. Capture HEAD's branch name on the repository's first accepted submission and retain it for that data directory. The target branch must not change. Non-bare repositories, URLs, missing repositories, detached HEAD, and unborn branches are invalid inputs. Fixtures use SHA-1 Git object IDs; full IDs are 40 lowercase hexadecimal characters.

The exact job input fields are:

| Field | Decision |
| --- | --- |
| `id` | String matching `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`; unique within `--data`. |
| `repo` | Absolute repository path as described above; normalized to canonical path. |
| `base` | Full commit ID existing in that repository; must be an ancestor of the captured target branch head when first submitted. |
| `patch` | UTF-8 unified Git diff content, not a filename; nonempty, applicable using ordinary `git apply` semantics. A syntactically valid string is accepted even if applying it later fails. |
| `build_cmd` | Nonempty UTF-8 string, executed as `/bin/sh -c STRING` in the attempt's checkout. |
| `timeout_s` | Integer from 1 through 3600; a separate wall-clock budget for each invocation of `build_cmd`. |

All six fields are required; unknown job fields, nulls, wrong types, unsafe IDs, invalid repository/base, or out-of-range timeouts are `INVALID_JOB`. JSON integers are mathematically integral JSON numbers; booleans are not integers. Normalize only `repo`; do not trim or rewrite command, patch, or ID. Submitted JSON key order and whitespace are irrelevant. A repeated ID with identical normalized fields returns the original acceptance sequence and `duplicate:true`, regardless of current state. Reusing an ID with any different normalized field returns `ID_CONFLICT` and changes nothing. An accepted ID is never forgotten or reused.

## 2. Commands and exit codes

```
kogen coordinator --data DIR --port P
kogen worker --id ID --coordinator [IP omitted]:P --work DIR
kogen submit --coordinator [IP omitted]:P JOB.json
kogen status --coordinator [IP omitted]:P [--json]
kogen wait --coordinator [IP omitted]:P JOB_ID --timeout S
kogen cancel --coordinator [IP omitted]:P JOB_ID
kogen --help
```

Flags may occur before or after positional arguments. Each required flag must occur exactly once. There are no default addresses, data/work directories, timeout, or port. `P` is a decimal integer 1–65535; port zero is invalid. The listener binds IPv4 `[IP omitted]` only. Worker IDs obey the job ID syntax. `S` is a decimal integer 0–3600; zero performs one immediate terminal-state check. Unknown flags, duplicate flags, missing/excess positionals, unreadable/invalid job JSON, and invalid CLI values exit 2. `--help` alone, and a subcommand followed by `--help` alone, print usage and exit 0 without connecting. Usage wording is not asserted.

| Exit | Decision |
| --- | --- |
| 0 | Accepted/idempotent submit; successful status/cancel; wait observes `landed`; successful daemon startup followed by graceful shutdown; help. |
| 1 | Wait observes any other terminal job state. |
| 2 | CLI usage/input error or server `INVALID_JOB`, `INVALID_REQUEST`, `ID_CONFLICT`, `NOT_FOUND`, or `WORKER_CONFLICT`. |
| 3 | Connection/protocol failure, server `INTERNAL`, `DATA_CORRUPT`, `REPO_CHANGED`, session/lease errors, data/work lock failure, or daemon startup error. |
| 4 | Wait expires with a nonterminal job. This does not cancel it. |

Client commands print exactly one compact JSON object and newline to stdout on success, and no progress logs there. Submit prints `{"id":ID,"seq":N,"duplicate":BOOL}`. `status --json` prints `{"version":1,"jobs":[JOB_RECORD,...]}` in increasing acceptance sequence. Plain `status` prints `id\tstate\tattempt\trepo\n`, followed by one tab-separated row per job in sequence order, with canonical repo paths. Wait prints a JOB_RECORD on exit 0, 1, or 4. Cancel prints `{"job":JOB_RECORD,"cancel_requested":BOOL}`; it exits 0 even when the job already terminated. Errors other than wait expiry print one JSON object `{"error":{"code":CODE,"message":TEXT}}` to stderr and nothing to stdout. Error message wording and daemon stderr logs are not asserted.

Coordinator startup creates/recovers the data directory, acquires its exclusive lock, and listens before printing one stdout line `{"type":"coordinator_ready","version":1,"address":"[IP omitted]:P","data":CANONICAL_DIR,"pid":PID}`. A client must be usable when this line appears. Recovery may leave previously leased jobs awaiting expiry; it must finish prepared Git transactions before readiness. Worker startup creates/locks its work directory, registers, and prints `{"type":"worker_ready","version":1,"id":ID,"work":CANONICAL_DIR,"pid":PID}` only after successful registration. Daemons print no further stdout lines. A second coordinator sharing a data directory fails with exit 3 without modifying it. A second worker sharing a work directory also fails with exit 3. Locks are released on process death; stale lock files alone cannot prevent restart.

For a valid invocation when the required local resources are available, each daemon must either print its ready line or exit with startup error within 10 seconds. The coordinator's 10-second startup budget includes recovery and reconciliation of prepared Git intents; it must not advertise readiness first. The worker's budget includes registration. This is a maximum, not a required delay.

SIGTERM/SIGINT initiate graceful daemon shutdown and exit 0 after cleanup. The coordinator stops accepting requests and renewing leases, resolves any prepared Git intent, and exits within 2 seconds; independent worker containment continues enforcing existing lease deadlines. The worker stops starting commands, kills and reaps its whole current descendant tree within 2 seconds, then surrenders any unprepared lease and exits. If a protected landing intent exists, it is reconciled before exit. SIGKILL is deliberately unhandled; its conventional signal exit status is not an application exit-code assertion.

## 3. Observable job record and lifecycle

Every JOB_RECORD has **all** these fields, including null values:

| Field | Type and meaning |
| --- | --- |
| `id` | Input ID. |
| `repo` | Canonical bare repository path. |
| `seq` | Durable acceptance integer, starting at 1; increases by one for each new accepted ID globally. |
| `state` | `queued`, `running`, `ready`, `landing`, `cancelling`, `landed`, `failed`, `rejected`, `timed_out`, or `cancelled`. |
| `attempt` | Integer, initially 0; increases by one on every build lease grant, including retries. |
| `worker_id` | Assigned worker ID or null when no lease is held. |
| `lease_expires_at_ms` | UTC Unix millisecond integer or null when no lease is held. Diagnostic deadline, not a client scheduling instruction. |
| `accepted_at_ms` | UTC Unix milliseconds at durable acceptance; never changes. |
| `updated_at_ms` | UTC Unix milliseconds at last durable record transition, nondecreasing for this job. Heartbeat renewal is a transition. |
| `landed_commit` | Full commit ID iff `state` is `landed`; otherwise null. |
| `reason` | Null for nonterminal states and `landed`; otherwise one of the reasons below. |

Terminal states are `landed`, `failed`, `rejected`, `timed_out`, `cancelled`; they are immutable and have null worker/deadline. Failure reasons are `clone_failed`, `patch_failed`, `build_failed` (`failed`); `rebase_failed`, `landing_build_failed`, `landing_timeout`, `target_changed` (`rejected`); `build_timeout` (`timed_out`); and `user_cancelled` (`cancelled`). Worker loss, coordinator loss, and graceful worker shutdown cause retry, not terminal failure. No logs, PIDs, lease tokens, input patch, or commands appear in JOB_RECORD.

The ordinary path is `queued -> running -> ready -> landing -> landed`. `running` is committed before a build assignment is delivered. `ready` means the initial build passed and its private commit/workspace is available. `landing` is committed before a landing assignment is delivered and covers rebase, rerun, and a possible prepared Git transaction. A ready or landing job still occupies its worker's single slot. A failed initial build terminates as `failed`; a failed landing rebase or rerun terminates as `rejected`. An initial command timeout terminates as `timed_out`; a landing rerun timeout terminates as `rejected` with `landing_timeout`, following the design's rule that unsuccessful reruns reject. Cancellation may pass through `cancelling` while cleanup is pending. An expired lease without an irrevocable landing intent returns its job to `queued`, preserving ID, sequence, inputs, and attempt count.

Workers have one leased job at a time. Initial build assignment chooses the lowest acceptance sequence among queued jobs; concurrent workers may build different jobs from the same repository. A lower sequence that is already running does not block initial assignment of a later one.

## 4. Build and landing decisions

For each attempt, clone into a new private checkout, check out exactly `base`, apply `patch`, and create exactly one job commit containing the patch's changes. The commit author and committer are `kogen-mini <kogen-mini@localhost>`; subject is `kogen-mini: JOB_ID`. Timestamps, commit IDs before landing, and local branch names are implementation choices. Patch deletions, additions, executable bits, and nested filenames must work. Do not include files created or changed solely by the build command in the job commit. Run the initial build with the patched source visible. After that command's entire tree exits, restore tracked content to the private patch commit and remove untracked build artifacts before rebase; fixture control files and output live outside the checkout. The landing candidate likewise contains only committed patch changes, regardless of rerun artifacts. Build output goes to attempt files described below; it must not corrupt CLI/protocol stdout. Run both build invocations with the same inherited worker environment, except ordinary Git and process-control variables needed for isolation; no shell expansion of `repo`, ID, or patch is allowed.

The landing order for each canonical repository is **strict increasing acceptance sequence**, including when later initial builds finish first. A ready job can enter landing only when every earlier accepted job for that repo is terminal. A failed, rejected, timed-out, or cancelled predecessor releases the lane. No cross-repo ordering or global landing lock is required. A single repo has at most one active landing transaction, including recovery.

On lane grant capture the target branch's current commit as `expected_head`. Rebase the job's single patch commit onto that head, using the same final source effect as applying/replaying that commit. A conflict rejects the job with `rebase_failed` and leaves the target untouched. Rerun `build_cmd` in the rebased checkout with a fresh `timeout_s` budget. A nonzero exit rejects with `landing_build_failed`; timeout rejects with `landing_timeout`. Even if `base` already equals `expected_head`, the second invocation is mandatory. The candidate commit is a direct child of `expected_head`, retaining the job subject and patch effect. Empty patches or a patch whose entire effect is already present reject with `rebase_failed`; no empty landing commit is created. Extra build-output changes are never landed.

After the rerun passes, the coordinator obtains the candidate Git object from the private workspace without changing the target branch. It durably records an intent `(job ID, attempt, lease token, target ref, expected_head, candidate)` **before** any target-ref update. Only the coordinator mutates the target ref. It performs a compare-and-swap fast-forward from `expected_head` to `candidate`, then durably records `landed` and `landed_commit` before replying. A target ref changed by an external writer before intent preparation rejects with `target_changed`; external writers during an already prepared transaction are outside the fixture scope. Implementations must never reset the target backward.

Recovery of a prepared intent is deterministic: if the target is `expected_head`, apply the recorded fast-forward once; if the target equals `candidate` or is a descendant of it, record the original candidate as landed without adding another commit. Any unrelated target is `REPO_CHANGED`: fail startup/readiness without rewriting Git or dropping the intent. An intent remains protected from expiry/requeue and cancellation until reconciled. Thus a crash after ref update but before durable terminal state cannot duplicate landing. There is no guarantee that an unacknowledged new submission was accepted; resubmitting identical input resolves the ambiguity. An acknowledged submission must remain queryable forever.

## 5. Leases, containment, cancellation, and timing

Lease duration is **8 seconds** from the coordinator's last successful grant/renewal. Workers poll and heartbeat at least once per second, including during commands and while ready/landing. Each heartbeat is durably recorded before acknowledgement and returns a fresh expiry for the same token. Tokens fence assignments; every worker session and every attempt has a distinct unguessable token. Late results, heartbeats, or assignments cannot mutate a reassigned job. Duplicate result retransmissions are idempotent as specified in PROTOCOL.md.

Use monotonic elapsed time for live deadlines, translating to Unix milliseconds for reporting. Durable restart deadlines are absolute: restart never grants another eight seconds merely because a process restarted. Tests do not change the system clock. After coordinator restart, sessions are invalid; workers clean up old attempts before re-registering. Unprepared old leases are not renewed, and their jobs are requeued at their original expiration. Startup may reap them early but cannot reassign until their old descendants are dead.

A lease includes a **hard descendant-cleanup deadline at expiration**. A worker's independently surviving containment mechanism must know the last acknowledged deadline, track descendants explicitly across fork, double-fork, and setsid, and begin termination early enough that no attempt descendant remains alive at expiration. Process groups alone do not satisfy this requirement. No assignment may start any job descendants before that mechanism is installed. Killing the worker or losing both worker and coordinator cannot disable cleanup. No restart is required to make orphan cleanup happen. A worker losing coordinator connectivity stops using the lease at its hard deadline and removes the full tree. A successful renewal may extend containment only after the coordinator acknowledgement, never on a locally attempted heartbeat.

No live command/checkout writer from an expired attempt may overlap execution of a replacement attempt. Within **one second after expiration**, the coordinator (if running and reachable) must expose `queued` or a higher-attempt assignment. Therefore a worker SIGKILL is followed by whole-tree death within at most eight seconds of its last renewal and observable retry within nine seconds of that renewal. Timing checks allow 250 ms for external polling/scheduler observation; that allowance does not extend the contractual lease. Coordinator downtime does not count toward availability/requeue bounds, but independent containment deadlines still hold.

Cancel is linearized as a durable cancellation decision. A queued job becomes `cancelled` immediately. Running/ready/unprepared landing becomes `cancelling`; no new commands or intent may start, and the coordinator tells the worker to terminate its whole tree at its next poll/heartbeat. A connected worker completes cleanup and acknowledgement within two seconds of cancellation; if it is unavailable the hard lease deadline provides the bound. The job becomes `cancelled` only after cleanup is confirmed or the hard deadline has elapsed. A worker result crossing a cancellation cannot restore success. Repeated cancellation returns `cancel_requested:true` while cancelling/cancelled. On an already terminal non-cancelled job it returns `false` and leaves it unchanged. A prepared intent is irrevocable: complete/recover it first, then return its terminal record with `false`; cancellation never claims to undo a land.

Each build timeout is measured from starting its shell. Its entire descendant tree must be dead within one second after the budget expires; only then publish its terminal result. A normally exited shell also requires cleanup: terminate any remaining attempt descendants within one second of shell exit before publishing success/failure or starting another phase. Initial build and landing rerun have independent budgets; cloning, patching, and waiting for the lane do not consume these budgets. Timeout is independent of renewable leases. Graceful worker shutdown confirms tree death before surrendering its unprepared lease; the coordinator exposes retry within one second of acknowledgement. If a landing intent is prepared, shutdown must reconcile that intent rather than retry its ref update as a new job.

## 6. Durable and workspace file layout

Only the data directory plus the local Git target is authoritative for accepted/landing state. Workers' work directories are disposable after cleanup. On a fresh coordinator startup create:

```
DIR/
  lock                 # exclusive OS lock; file may survive process death
  state.json           # authoritative durable UTF-8 JSON snapshot
  internal/            # optional implementation-private recovery/temp files
```

`state.json` is one complete JSON object: `{"version":1,"next_seq":N,"jobs":[ENTRY,...],"repos":[REPO_ENTRY,...]}`. `next_seq` is the next unused acceptance integer (initially 1). Jobs are ordered by `seq`. ENTRY has `input` (normalized six-field input), `record` (JOB_RECORD), and `internal` (object with implementation-private receipt/artifact/lease data). REPO_ENTRY has `repo` (canonical path), `ref` (captured `refs/heads/...`), and `intent` (null or `{"id":ID,"attempt":N,"lease_token":TOKEN,"expected_head":OID,"candidate":OID}`). Repos are sorted lexicographically by canonical path. All keys listed here are required; additional keys are permitted only inside `internal`. A syntactically invalid, missing-after-prior-initialization, unsupported-version, or inconsistent snapshot fails with `DATA_CORRUPT`; never silently initialize over corrupt state. A previously empty directory, or a directory containing only an unlocked `lock`, is fresh.

Publish snapshots by replacing the complete file atomically, with file and directory durability before acknowledgements or irreversible Git changes. Readers opening the final path see a complete old or new snapshot, never partial JSON. An implementation may use files beneath `internal/` for journaling but must make `state.json` authoritative at every acknowledged mutation. State holds enough information to recover prepared intents and receipts. No deletion/compaction of accepted jobs is part of this version. Tests may assert layout, readability, version, records, and intent fields, but cannot assert private encoding or temp filenames. They read a fresh snapshot per observation, not multiple files as a fictitious transaction.

Each worker has:

```
WORK/
  lock
  jobs/ID/attempt-N/
    checkout/           # private Git checkout, never the bare target
    build.stdout
    build.stderr
    landing.stdout
    landing.stderr
  internal/             # optional containment/session metadata
```

Create the attempt directory when granting the attempt, before starting its command. A phase's output files exist before its command starts, hold that phase's raw output, and are closed by completion/cleanup. Landing files need not exist if landing never starts. Keep attempt output through worker exit and subsequent attempts for inspection; disk-pressure cleanup is out of scope. A checkout may be recreated after stale attempt cleanup, but an attempt number is never reused. Tests assert known build output content rather than clone progress or Git diagnostic wording. Clone/Git process descendants are contained too.

## 7. Observable guarantees and test boundary

An acknowledged accepted job is present after coordinator SIGKILL/restart. Its sequence, identity, input, and acceptance time are unchanged; only documented state/attempt changes occur. A landed ID contributes exactly one commit to its repository branch across arbitrary restarts and identical resubmission. Per-repo landed commit subjects follow increasing acceptance sequence after skipping non-landed terminal jobs. Every landed commit passed both builds, and every failed/rejected/cancelled/timed-out job leaves the target unchanged by that job. A prepared successful intent may complete during recovery after its worker died; that is completion, not a duplicate attempt.

Status is a linearizable snapshot, wait observes the same records and never mutates jobs, and a terminal record never changes. No jobs disappearing during recovery, double landing, stale-worker acceptance, overlapping landing for one repo, or live descendants after cleanup deadlines are allowed. Liveness assumes a reachable running coordinator, an available worker, finite Git operations, and commands completing or timing out. A prior unfinished job can deliberately hold a repository's FIFO landing lane.

All behavioural and fault observations use the CLI, this TCP protocol, the specified file layout, local Git refs/history, and local OS process liveness. No tests depend on a particular language, supervisor architecture, private data keys, exact log wording, commit timestamps, or scheduling order across repositories. `features/` and STEPS.md make the B/F decisions concrete; `quint/` abstracts these safety decisions, without claiming to model OS containment or storage syscalls.
