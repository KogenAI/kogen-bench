# Durable change queue

Implement an offline CLI that schedules proposed Git changes, grants one worker a lease, checks its candidate, and publishes one commit using an atomic comparison against a branch's previous tip. Build `./bin/app` with `make build`. Implement application logic in the selected language; system Git and configured checks are the only external runtime programs allowed. `make check` and `make test` must work offline.

## Interface

```
./bin/app init    --root DIR --config PATH
./bin/app enqueue --root DIR --now N --id ID --base SHA --candidate SHA
./bin/app claim   --root DIR --now N --ttl N
./bin/app renew   --root DIR --now N --id ID --token TOKEN --ttl N
./bin/app land    --root DIR --now N --id ID --token TOKEN
./bin/app release --root DIR --now N --id ID
./bin/app status  --root DIR --now N
./bin/app events  --root DIR --now N --after N
```

The command is first; flags follow in any order. Reject unknown, repeated, missing or inappropriate flags, extra positional arguments and invalid flag values before accessing files. Each valued flag consumes the next argument. DIR is nonempty and already exists; PATH is a nonempty relative slash-separated path with no empty, `.` or `..` components, backslash or NUL. IDs match `[a-z][a-z0-9-]{0,31}`; tokens match `c[1-9][0-9]*`; SHAs are 40 lowercase hex digits. Integers are canonical decimal `0|[1-9][0-9]*`, at most 1000000000; ttl is 1..1000000 and now+ttl must be at most 1000000000. No stdin or network. Inputs are UTF-8. No malicious symlinks, hardware failure or corrupt app-owned state are tested.

All application reads and writes stay under DIR, apart from executing system Git and configured executables. DIR contains an existing SHA-1, non-bare repository at `repo/`. The configured target branch exists and is not checked out in the supplied checkout. Never modify that checkout's HEAD, index or working files. Isolated worktrees and durable metadata belong elsewhere under DIR. Git's own administrative writes inside repo are allowed. No file layout is imposed for application metadata. Do not alter the configuration input. Tests may change the target ref through Git while a command is running.

Each success exits 0, with empty stderr and exactly one compact LF-terminated JSON object on stdout: `{"result":VALUE,"events":[EVENT,...]}`. Each error emits empty stdout and one compact LF-terminated object on stderr: `{"error":{"code":CODE,"message":STRING}}`. Message is a nonempty human-readable string; its text is unspecified. Key order and interior whitespace do not matter; key sets, types and array order do. Integers use integer syntax. No other output; capture Git/check/hook output. A parked landing is a successful command with a parked result.

| Code | Exit | Meaning |
|---|---:|---|
| USAGE | 2 | Invalid command/flags or values |
| CONFIG | 2 | Invalid initialization configuration |
| NOT_INITIALIZED | 3 | Commands other than init before initialization |
| ALREADY_INITIALIZED | 3 | Repeated init |
| GIT | 3 | Invalid repository/object/ref or unexpected Git failure |
| IO | 3 | Other filesystem failure |
| CLOCK | 4 | now less than the last accepted now |
| EXISTS | 4 | ID already exists, including landed IDs |
| NOT_FOUND | 4 | ID does not exist |
| STATE | 4 | Operation not allowed for the item's state |
| LEASE | 4 | Wrong, superseded or expired token |

After CLI validation, check initialization, then CLOCK, then recover prepared publications and expire leases, then command-specific validity. Command-specific admission errors do not append events or change item state, except that recovery/expiry is committed before these errors. Operational GIT/IO errors after landing has begun retain all completed durable checkpoints (events, turns, prepared/landed records); they must never refund turns or erase publication custody. A rejected CLOCK does nothing. A command-specific error still accepts now. Init has no clock; initial accepted now is zero.

## Initialization and submitted changes

A missing or unreadable configuration file is IO. PATH contains exactly `{"branch":STRING,"check":[STRING,...],"timeout_ms":INTEGER}`. Reject invalid JSON, duplicate decoded keys at any depth, NaN/Infinity, extra/missing keys, wrong types, empty check, empty argv entries, or timeout_ms outside 1..10000 as CONFIG. branch matches `[a-z][a-z0-9-]{0,31}`. Integers must have integer syntax (no exponent or fractional syntax); booleans are not integers. Configure an immutable copy of these values. The first check entry is an absolute executable path or a name resolved through PATH; other entries are literal argv, never shell-interpreted. Executable availability is tested only when running land; resolve a PATH name using that invocation's environment. The supplied configuration path and executables can contain spaces. init validates repository and branch, creates durable empty state, and returns result `{"branch":BRANCH}` with events `[]`.

enqueue validates that base and candidate identify commits, and that candidate has exactly one parent, equal to base. The candidate's tree must differ from base's tree. The target need not currently equal base; base need not be an ancestor of the current target. Store the proposed commit and its original base without changing refs. IDs never become reusable. Return `{"id":ID,"state":"queued"}`; append `queued` with data `{"base":SHA,"candidate":SHA}`. Invalid objects or shape are GIT. Candidate commit message and identity are inputs, not the published message or identity.

## Durable scheduling and leases

Maintain queued, claimed, parked and landed states. At most one item may be claimed across the whole root. Queue order is insertion order; an expired claim retains its original place. A released parked item goes to the tail. Calls across processes must be serialized for metadata and scheduling; concurrent claims must never grant two live leases. Do not use an unrecoverable PID file as a lock.

claim first performs recovery/expiry. If any item remains claimed, return `{"id":null,"token":null,"expires":null,"reason":"busy"}`. If none is queued, use reason `"empty"`. Otherwise claim the first queued item and return `{"id":ID,"token":TOKEN,"expires":now+ttl,"reason":null}`. Tokens are `c1`, `c2`, ... from a root-wide persistent counter, incremented only when granting a new lease. Append `claimed`, data `{"token":TOKEN,"expires":INTEGER}`. ttl is logical time, not wall time.

A lease expires when now >= expires. Before the requested operation, process expired claims in insertion order: set queued, clear token/expires, and append `expired`, data `{"token":OLDTOKEN}`. A new claim always requires a new token. Old tokens can never authorize another claim. renew requires the item to be claimed and the exact live token, replaces expiry with now+ttl (it can shorten), returns `{"id":ID,"expires":INTEGER}`, and appends `renewed`, data `{"token":TOKEN,"expires":INTEGER}`. For renew/land: unknown ID is NOT_FOUND; any known item with a nonmatching token or not claimed is LEASE.

release requires parked (otherwise STATE), returns `{"id":ID,"state":"queued"}`, clears the reason and prior publication SHA, resets integration turns to zero, retains original candidate/base, moves it to the queue tail, and appends `released`, data `{}`. It does not claim or check the item.

## Landing algorithm

land is synchronous. Its logical now is fixed during the invocation; checks taking wall time do not expire a valid lease mid-command. Metadata commands for the same root may wait for it. Other programs can still update Git refs.

Begin every land invocation from the original candidate and original base, with the item's durable integration-turn count. Create an isolated clean detached worktree at the candidate. Run the configured check there with inherited environment plus `QUEUE_ROOT=DIR` (absolute), `QUEUE_ID=ID`, `QUEUE_TURN` (canonical decimal turn count), and `QUEUE_BASE` (the candidate's current base). Capture/discard both output streams. A nonzero exit parks with `check_failed` on the original candidate, or `recheck_failed` after integration. Failure to start or exceeding timeout_ms parks with `check_unavailable`. Checks wait for any short subprocesses they use and leave no descendants running at exit; tested timeout cases use a single check process with no descendants. Completion requires the check process to exit and captured output readers to finish. One timeout covers this operation. On timeout terminate and reap the check process within a further bounded two seconds; never wait indefinitely for pipe EOF. After a land command returns, none of its processes may remain alive or unreaped. The CLI is evaluated on Linux.

Record tree identity immediately before the check. Tree identity means the index tree with the tracked working files matching that index. After exit 0, both must still match the snapshot recorded before the check; untracked files are ignored. Staged changes produced by transplantation are part of the snapshot, not a check mutation. Otherwise park with `candidate_changed`. Append `checked` only after a passing, unchanged check: data `{"base":SHA,"tree":TREESHA,"turn":INTEGER}`. No check receipt is supplied by callers or reused after a crash.

Inspect the target's current tip after each successful check and immediately before commit. If it differs from the candidate's current base, integration is needed. If four turns are already consumed, park with `retry_limit` without another rebase or check. Otherwise durably increment turns, transplant the original candidate's one-commit change from its original base onto the new tip using Git's ordinary three-way cherry-pick semantics (equivalent to `git cherry-pick --no-commit CANDIDATE` in a clean worktree at the new tip). Preserve all changes in the new base. A conflict or empty transplant parks with `rebase_conflict`. Append `rebased` only on success, data `{"base":NEWTIP,"tree":TREESHA,"turn":INTEGER}`; then run the check on that exact result and repeat. Four turns are allowed across all movements, including races at publication; a green fourth turn may publish. The fifth movement parks. A failed recheck parks immediately; there is no automatic code repair.

When the base is current and the check is valid, publish exactly one new commit whose single parent is that base, whose tree is the checked tree, and whose complete message is `Apply ID\n` (Git's normal final newline). Use ordinary `git commit`, the supplied repository's identity and trusted configuration, and its hooks (including core.hooksPath). Do not bypass hooks or signing. A failed commit parks with `hook_failed`. If hooks succeed but the resulting message or parent is not exactly the required message/single base parent, also park with `hook_failed`; tree mismatch takes precedence and uses `candidate_changed`. Recompare the resulting commit tree and tracked working/index tree to the checked tree after hooks; a mismatch parks with `candidate_changed` and leaves target unchanged. A hook may move the target. Update `refs/heads/BRANCH` with Git compare-and-swap against the expected base. A lost comparison requires a new integration/check cycle on the newest target, consuming the same four-turn counter; never publish the stale commit. Unreachable stale commits may remain as Git objects.

On success set landed, clear lease/reason, retain publication SHA, return `{"id":ID,"state":"landed","reason":null,"sha":SHA}` and append `landed`, data `{"sha":SHA,"base":SHA,"tree":TREESHA,"turn":INTEGER}`. Parking clears the lease and publication SHA, retains turns, returns `{"id":ID,"state":"parked","reason":REASON,"sha":null}` and appends `parked`, data `{"reason":REASON,"turn":INTEGER}`. Never update target for any parked outcome. Normal completion removes invocation-owned worktrees and their registrations; preexisting files remain intact.

## Events, status and crash recovery

Every event is exactly `{"seq":INTEGER,"type":STRING,"id":ID,"data":OBJECT}`. Sequence starts at 1, increases by one globally, never resets and has no gaps or duplicates. events in an ordinary response are just those appended during that invocation, in sequence order, including recovery/expiry. events command returns all retained events with seq > after as result `{"events":[EVENT,...]}`; after may exceed the current sequence. Its outer events contains only events newly appended by recovery/expiry. No timestamps.

status result is exactly `{"branch":BRANCH,"tip":SHA,"next_token":INTEGER,"items":[ROW,...]}`. Items appear in original enqueue order, even after release. ROW is exactly `{"id":ID,"state":STATE,"position":INTEGER_OR_NULL,"token":STRING_OR_NULL,"expires":INTEGER_OR_NULL,"turns":INTEGER,"reason":STRING_OR_NULL,"sha":STRING_OR_NULL}`. Positions are 1-based among queued items in their current scheduling order; every nonqueued position is null. token/expires occur only for claimed; reason only for parked; sha only for landed. next_token is the integer that the next grant will use, initially 1.

Support `QUEUE_CRASH` with values `after_claim`, `after_prepare`, `after_publish`, and `before_park`. At the named point, kill the CLI itself with SIGKILL, not an error JSON or normal exit. Other values have no effect. after_claim acts after a durable new claimed event/state and before output. after_prepare acts after creating/hook-validating the commit and durably storing its ID, expected base, checked tree and turn, before target CAS. after_publish acts after successful target CAS but before durable landed state/event. before_park acts immediately before committing a parked transition. A hook is activated only when the named step is actually reached; no output precedes these kills.

On the next valid command, reconcile every prepared publication before lease expiry. If its exact commit is the target tip or an ancestor of the target tip, mark landed and append the ordinary landed event exactly once, even if its lease is now expired. Otherwise discard the prepared publication, keep the prior claimed item/turn count, append no recovery event, and expire normally if due. Never auto-publish a prepared commit. Uncommitted work and prior check results are discarded; a subsequent land must run the check again. A kill before parking leaves the lease and previously committed events/turns intact. On recovery remove worktrees left by the killed invocation. Repeated status/events must not duplicate transitions. Named crashes model abrupt process death with a working filesystem; durability across machine power loss is not required.
