# Durable change-request workflow

Implement an offline CLI for a team's change-request approvals. Build `./bin/app` with `make build`. Keep the workflow in process in the selected language. `make check` and `make test` must work offline. No services or network access are needed.

## CLI and validation

```
./bin/app COMMAND --state DIR [FLAGS]
create          --id ID --request TOKEN --actor NAME --title TEXT --required N
revise          --id ID --request TOKEN --actor NAME --title TEXT --revision N
submit          --id ID --request TOKEN --actor NAME
review          --id ID --request TOKEN --actor NAME
approve         --id ID --request TOKEN --actor NAME --revision N
request-changes --id ID --request TOKEN --actor NAME --reason TEXT
merge           --id ID --request TOKEN --actor NAME
close           --id ID --request TOKEN --actor NAME
reopen          --id ID --request TOKEN --actor NAME
show            --id ID
history         --id ID
audit           [--id ID]
verify
```

The command is first; flags follow in any order as separate flag/value pairs. Exactly the listed flags are accepted, plus `--state` on every command. Reject unknown commands, missing, repeated or extra flags, positional arguments, and missing values with USAGE before touching storage. A value may start with `--`; it is still a value. ID, TOKEN and NAME match `[A-Za-z0-9][A-Za-z0-9_-]{0,63}` and are case sensitive. DIR and TEXT are nonempty UTF-8 strings (TEXT may contain newlines). N is canonical decimal `[1-9][0-9]*`; required is 1..16, revision is 1..2147483647. Every argument, including the command, flag names, and DIR, must be valid UTF-8; any non-UTF-8 argument is USAGE before touching storage. Invalid values are USAGE. All numeric outputs are JSON integers. No timestamps.

Every success exits 0, emits exactly one compact, single-line LF-terminated JSON object on stdout and nothing on stderr. Every failure emits no stdout and exactly one compact, single-line LF-terminated JSON error object on stderr. JSON object key order and whitespace within that single line do not matter; keys, types and array order do. Never emit build/debug chatter from the app.

## Records and transitions

A change view has exactly these keys:
`{"id":"C","author":"alice","title":"Fix","required":2,"revision":1,"status":"draft","approvers":[]}`.
Approvers are distinct names sorted in ASCII byte order. Author and required never change.

Each successful mutation returns `{"seq":S,"change":VIEW}`. S starts at 1 and increases globally by 1 for every successful mutation, including approvals that do not change status. Failed commands consume neither sequence numbers nor request tokens.

| Command | Allowed source | Result and guards |
| --- | --- | --- |
| create | absent | draft, revision 1, empty approvers; actor becomes author |
| revise | draft, submitted, in_review, approved, changes_requested | draft; author only; supplied revision must equal current + 1; replace title and clear all approvals even if title is unchanged |
| submit | draft | submitted; author only |
| review | submitted | in_review; any actor |
| approve | in_review, approved | non-author only; supplied revision must equal current; actor must not already be an approver; add actor, status becomes approved when count >= required, otherwise in_review |
| request-changes | in_review, approved | changes_requested; non-author only; clear all approvals; reason is retained in the journal |
| merge | approved | merged; author only; count of current approvers must be >= required |
| close | draft, submitted, in_review, approved, changes_requested | closed; any actor; clear all approvals |
| reopen | closed | draft; author only; clear approvals, keep revision and title |

`merged` is terminal. `changes_requested` must be revised before resubmission. Review does not itself grant approval. New revision numbers must be consecutive, including after reopen. Additional distinct approvals are permitted after the threshold has been reached.

## Idempotency and error contract

`--request` is an operation token, globally scoped to this state directory, distinct from the change's `--id`. After CLI validation and journal validation, check the token BEFORE entity lookup or transition guards. The same token and same semantic command (flag order and DIR spelling excluded) returns the original success object, even after later operations or restart, without adding an event. A previously used token with any different command/argument gives REQUEST_CONFLICT. A failed attempt does not reserve the token, so it can be retried after its guard is satisfied. Read commands and verify have no side effects on logical state and are naturally repeatable.

Errors have exactly the keys shown below. All messages are fixed strings:

| Code | Exit | Object |
| --- | --- | --- |
| USAGE | 2 | `{"error":{"code":"USAGE","message":"invalid arguments"}}` |
| NOT_FOUND | 3 | `{"error":{"code":"NOT_FOUND","message":"change not found"}}` |
| ALREADY_EXISTS | 4 | `{"error":{"code":"ALREADY_EXISTS","message":"change already exists"}}` |
| REQUEST_CONFLICT | 4 | `{"error":{"code":"REQUEST_CONFLICT","message":"request token already used"}}` |
| INVALID_TRANSITION | 5 | `{"error":{"code":"INVALID_TRANSITION","message":"transition rejected","from":SOURCE,"to":TARGET,"reason":REASON}}` |
| CORRUPT_LOG | 6 | `{"error":{"code":"CORRUPT_LOG","message":"invalid journal"}}` |
| IO_ERROR | 7 | `{"error":{"code":"IO_ERROR","message":"storage failure"}}` |

SOURCE is the current status. TARGET is draft for revise/reopen, submitted for submit, in_review for review, approved for approve, changes_requested for request-changes, merged for merge, closed for close. Test guards in this order: allowed source (`STATE`), author-only (`AUTHOR_REQUIRED`) or non-author (`SELF_REVIEW`), revision (`REVISION_MISMATCH`), duplicate approver (`DUPLICATE_APPROVER`), merge threshold (`INSUFFICIENT_APPROVALS`). The first failed guard is REASON. For example approving one's own submitted change fails STATE, while approving one's own in_review change fails SELF_REVIEW even with a stale revision. Missing entity precedes guards; create on an existing ID is ALREADY_EXISTS. Every error leaves the journal byte-for-byte unchanged. A lock file or empty directory created to open storage is not logical state.

## Durable journal, audit and replay

All application-created filesystem entries must be below DIR. Create DIR when necessary. Use a stable `DIR/.lock` regular file with an exclusive Linux `flock(2)` lock (`LOCK_EX`; fcntl record locks are not interchangeable), acquired using blocking `flock(fd, LOCK_EX)` with EINTR retry and held across loading, validating, token checking, mutation, durable commit and response construction. Reads also take this lock. Process exit or SIGKILL must release it; never delete/replace `.lock`. Each base supplies a ready-to-use flock helper (documented in its README), including the standard `bun:ffi` binding to libc for TS/Bun; using it is optional. Parallel successes are linearizable and no events or approvals may be lost.

The sole authoritative state is `DIR/journal.jsonl`. Absence or an empty file means no events. Each event is one UTF-8 JSON object followed by LF, with exactly these keys:
`{"seq":S,"request":TOKEN,"command":COMMAND,"from":SOURCE_OR_NULL,"to":STATUS,"result":{"seq":S,"change":VIEW}}`.
COMMAND has exactly `op`, `id`, `actor`, plus `title` and integer `required` for create; `title` and integer `revision` for revise; integer `revision` for approve; string `reason` for request-changes. It excludes state and request. `from` is null only for create. The result is the response at that event, not the current view. Every mutation is an event, even a partial approval. The journal order is sequence order. No other authoritative state files; optional caches must not affect behavior.

Commit an entire new journal by writing a temporary file below DIR, flushing it to disk, atomically renaming it over journal.jsonl, then flushing DIR. A kill during commit may leave either the old or the new complete journal, never a partial event. Ignore leftover temporary files on startup. This small workload permits rewriting the whole journal. Do not attempt to salvage malformed journals.

Journal numeric values must use JSON integer syntax (no decimal point or exponent): `1.0` and `1e0` are CORRUPT_LOG even when mathematically integral; booleans are not integers.

Every command validates the whole journal before doing anything else with logical state: complete LF-terminated lines, JSON objects with the exact schema/types above, consecutive seq values, unique request tokens, valid commands/arguments, legal transitions, and exact from/to/result under replay. Empty lines, trailing partial bytes, or altered result data are CORRUPT_LOG. It must not repair or truncate the file on error.

`show` returns `{"change":VIEW}`. `history` requires an existing ID and returns `{"events":[EVENT,...]}` filtered to that ID in sequence order. `audit` returns the same shape for all events, or filters by optional ID (an unknown filter gives an empty array). `verify` rebuilds all changes and token responses by replaying the journal, returning `{"valid":true,"events":COUNT,"changes":[VIEW,...]}` with changes sorted by ID in ASCII order. It must work with only journal.jsonl present in a fresh directory; keep the journal unchanged. All readers see a consistent complete prefix under concurrency.

Scope: Linux validation environment, ordinary local filesystem, no malicious symlinks, no external journal writers during an invocation. Inputs and committed journal are at most 8 MiB. OS/storage failures map to IO_ERROR; no specific recovery is required for a failing fsync or full disk. No flags or commands beyond this contract are required.

Stack and checks: TypeScript/Bun. Build: `make build`; test: `make test`.
Checks: `make check` runs tsc --noEmit (strict), biome check, bun test.
