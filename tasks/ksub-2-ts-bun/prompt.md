# Change approval ledger

Implement a persistent, offline approval desk shared by independent processes.
`make build` creates `./bin/app`; `make check` and `make test` pass. All runtime
logic stays in process in the requested language. No database, network or daemon.
Native OS facilities and subprocesses solely for locking/signaling are allowed;
Linux supplies `flock`. All runtime files and markers stay under `--root DIR`.

## CLI and JSON

```
./bin/app apply  --root DIR             # one command object on stdin
./bin/app card   --root DIR --key KEY
./bin/app status --root DIR [--key KEY]
./bin/app log    --root DIR [--after N]
```

The subcommand is first; flags are separate flag/value pairs in any order.
Reject missing, duplicate, unknown, inapplicable or equals-form flags and extra
positionals. DIR is nonempty. Validate syntax and stdin before touching DIR.
Create missing roots and parents. Paths have no hostile symlinks. Reads on an
empty root are valid. Read commands do not consume stdin.

Apply reads exactly one UTF-8 JSON object, with optional surrounding JSON
whitespace. Reject duplicate keys at every depth, unknown/missing keys,
NaN/Infinity, and wrong types. N is an integer 0..1000000000 written as an
unsigned JSON decimal token; bool, negative spellings (including -0), fractional
and exponent spellings are invalid. CLI N is `[0-9]+` in that range (leading
zeroes accepted). KEY matches `[a-z][a-z0-9_-]{0,31}`. ID and actor match
`[A-Za-z0-9_-]{1,48}`. Text tokens match `[A-Za-z0-9_./:-]{1,128}`.
HEX is even-length lowercase hex, up to 8192 characters. Required byte strings
are nonempty HEX. Source is null or HEX, including the empty string. SHA is
exactly 64 lowercase hex digits. No wall clock is sampled.

Success exits 0 with empty stderr and JSON object(s), each followed by exactly
one LF, on stdout. Only overview status has multiple rows. Error stdout is empty;
stderr is one LF-terminated object:
`{"error":{"code":"CODE","message":"nonempty human-readable text"}}`.
Message wording is free. Key order on output is free; key sets, types, array
order and null values are exact. Skeleton errors are NOT_IMPLEMENTED, exit 70.

| Code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | Syntax, JSON or value invalid |
| NOT_FOUND | 3 | Unknown or removed request |
| ID_REUSED | 4 | A committed command ID has different normalized command |
| FORBIDDEN | 5 | Role or identity may not perform this action |
| BAD_STATE | 6 | Lifecycle or queue guard fails |
| HASH_MISMATCH | 7 | Approval token does not match current content |
| FORCE_REQUIRED | 8 | Removing this state needs force |
| TIME_REVERSED | 9 | Fresh command at is below the committed clock |
| CORRUPT_LOG | 10 | Complete log record or record ordering is invalid |
| IO_ERROR | 11 | Storage access, locking, persistence or sync fails |

Error precedence: USAGE, storage/recovery, committed ID comparison/replay,
TIME_REVERSED, FORBIDDEN role, NOT_FOUND (except create), FORBIDDEN identity,
BAD_STATE, HASH_MISMATCH, FORCE_REQUIRED. A semantic failure commits nothing,
consumes no ID/sequence and advances no clock. Directories/lock files may exist.
Ordinary permission/access errors are tested; arbitrary disk faults are not.

## Commands, cards and approval

Every apply input has EXACTLY these keys:
`{"id":ID,"at":N,"actor":ID,"role":ROLE,"action":ACTION,"key":KEY_or_null,"data":OBJECT}`.
Roles are `planner`, `caller`, `controller`. Only start/stop have key:null.
Data key sets and allowed roles are:

| Action | Role | Data |
| --- | --- | --- |
| create | planner | `{request:HEX,plan:HEX,criteria:HEX,source:HEX_or_null}` |
| revise | planner | `{plan:HEX,criteria:HEX,source:HEX_or_null}` |
| approve | caller | `{token:PREFIX}`; PREFIX is 6..64 lowercase hex digits |
| remove | caller | `{force:BOOL}` |
| start, stop | controller | `{}` |
| begin | controller | `{diff:TOKEN,journal:TOKEN}` |
| progress | controller | `{kind:KIND,name:NAME}` |
| finish | controller | `{outcome:OUTCOME,reason:TOKEN_or_null,sha:SHA_or_null}` |

Progress KIND is `phase`, `step`, or `note`; NAME is empty or a text token.
OUTCOME is `blocked`, `failed`, `parked`, `interrupted`, or `landed`.
Landed requires reason:null and a SHA; other outcomes require a reason and
sha:null. No source bytes may be passed in argv.

Canonical JSON means recursively ASCII-sorted object keys, compact punctuation,
no whitespace, decimal integers, lowercase JSON literals, and ordinary JSON
strings. All strings in hash inputs contain only ASCII letters, digits and the
punctuation allowed above, so no escaping ambiguity arises. Hash UTF-8 canonical
JSON bytes, WITHOUT a trailing LF, with SHA-256; output lowercase hex.

Content is `{request:HEX,plan:HEX,criteria:HEX,source:HEX_or_null}`. Hash this
object to get content_id. Hash the complete CARD to get card_id. CARD has exactly:
`{key,status,version,planner,content,content_id,approval,last_run,runs,reason,landed_sha,updated}`.
All absent values are null. version is a per-key positive integer; runs starts 0.
approval is null or `{actor:ID,content_id:SHA}`. last_run is null or
`{id:ID,status:STRING,stage:TOKEN_or_null,started:N,finished:N_or_null,diff:TOKEN,journal:TOKEN}`.
Its ID is KEY followed by `-` and the decimal run counter. updated is the at of
this key's latest command. Every successful per-key command increments version,
even identical revise; global actions have no card. create starts version:1,
status:draft, planner:actor, approval/last_run/reason/landed_sha:null, runs:0.

create rejects an existing or previously removed key as BAD_STATE. The original
request and planner are immutable. revise is allowed in every state except
building or removed; it replaces plan/criteria/source, ALWAYS clears approval,
reason and landed_sha, and sets draft, retaining last_run and runs. Even an
identical revise clears approval. planner identity need not equal the creator.
The creator's identity cannot approve their own request, even with role:caller.
approve is allowed in draft, blocked, failed, parked, interrupted and landed.
The token must prefix current content_id. It sets queued, stores the approver,
and clears reason and landed_sha, retaining last_run/runs. It does not start work.
An already queued request cannot be approved again with a fresh ID.
remove rejects building; draft removes without force; all other states require
force:true. It sets removed, clears approval/reason/landed_sha, retains content
and last_run/runs. Removed keys remain permanent tombstones and are absent from
status and card; their remove command still returns its removed card.

## Serial work and exact status

Queue state starts `stopped`; start is allowed only from stopped and changes it
to running, even when empty. stop from stopped is BAD_STATE. stop from running
sets stopping if a request is building, otherwise stopped. stop from stopping
is BAD_STATE. A finish while stopping changes the queue to stopped; a finish
while running keeps it running. An empty running queue does not stop itself.

Queued requests are ordered by their MOST RECENT approve sequence, ascending.
begin requires running, no other building request, and key equal to queue head.
It sets building, increments runs, and replaces last_run with status:running,
stage:null, started:at, finished:null and the supplied paths. Approval remains.
progress requires building. phase/step with nonempty name replaces last_run.stage;
note and empty names do not change stage. It still increments version/updated.
finish requires building. It sets status to outcome and last_run.status to that
outcome, finished:at; stage/diff/journal remain in last_run. reason and landed_sha
come from data, and approval is cleared. All five terminal outcomes are permitted.
This desk records an external controller's outcome; it executes no build/check.

card returns `{card_id:SHA,card:CARD}` for a current nonremoved key.
status --key returns one row as below, with type:`detail`, for ANY nonremoved
key, including older landed keys. Overview begins with exactly
`{schema:1,type:"queue",state:STRING,queued:N,next:KEY_or_null,active:KEY_or_null,done:BOOL}`.
queued counts queued requests, next is their head; done is true exactly when
stopped AND no request is building. Then request rows in this category order:
building, queued, blocked, failed, parked, interrupted, draft, landed.
Queued rows use queue order. Other nonlanded categories use key ASCII order.
Include only the five most recently landed current requests, ordered by their
finish sequence descending. Reapproval/revision removes them from this category.

Request/detail rows have exactly
`{schema:1,type:STRING,key:KEY,status:STRING,queue_position:N_or_null,reason:TOKEN_or_null,run_id:ID_or_null,run_status:STRING_or_null,stage:TOKEN_or_null,elapsed:N_or_null,landed_sha:SHA_or_null,diff:TOKEN_or_null,journal:TOKEN_or_null,card_id:SHA}`.
Overview type is `request`; queue_position is 1-based only for queued.
run_id/run_status/diff/journal always retain last_run when present. stage is
last_run.stage ONLY while building, null in ALL other states (even queued after
reapproval). elapsed is null without last_run; while building it is updated minus
started, otherwise finished minus started. All values derive from records, not
filesystem path existence or clock sampling. No agent/watch command is required.

## Append-only log, replay and recovery

Use DIR/status.jsonl as the authoritative state. All reads and writes serialize
across processes; locks auto-release after SIGKILL and their inode is never
replaced. Supplemental files may be caches only: deleting every runtime file
except status.jsonl on a quiescent root must preserve all observations, receipts,
queue order, tombstones and clock. Do not create files outside DIR.

Each successful fresh apply appends EXACTLY one LF-terminated record with keys
`{schema:1,seq:N,id:ID,at:N,command:COMMAND,result:RESULT}`. Sequences start 1
and are contiguous across all keys and global actions. COMMAND has exactly
`{actor,role,action,key,data}` (input minus id/at). RESULT has exactly
`{seq:N,card_id:SHA_or_null,card:CARD_or_null,queue:STRING}`; seq agrees with the
record, queue is the queue state AFTER this action, and global actions use null
card/card_id. The append preserves every prior complete byte verbatim. Record
JSON need not be canonical, but its framing is exactly one object per LF line.
apply returns RESULT plus `replayed:false`. Committed ID lookup is global; an
identical normalized COMMAND returns its ORIGINAL RESULT plus replayed:true,
even after removal or with an older at. Object key order and JSON whitespace
are irrelevant to equality; at is excluded. Different COMMAND gives ID_REUSED.
Replays alter nothing and never reach hooks. Failed IDs are reusable.

log returns one object `{entries:[RECORD,...]}`, in ascending sequence order,
including exactly records with seq strictly greater than --after (default 0).

Persist and sync before stdout. A record becomes committed only with its LF.
A trailing non-LF suffix (even valid JSON) is uncommitted: every invocation must
truncate it and sync before replay/observation. A malformed COMPLETE line, blank
line, wrong shape/type/hash, noncontiguous seq, repeated id, reversed at, or
command/result inconsistent with these transition rules gives CORRUPT_LOG and
must not truncate or rewrite ANY bytes. Validate all complete records BEFORE
truncating an incomplete suffix. Empty files are valid. Thus even fabricated
well-hashed cards must be checked against command replay. Reads never append.

Two fault hooks are required on every fresh successful apply. `before_append`
is after validation but before changing log bytes. `after_append` is after the
complete record and its file (and directory if newly created) are durable, before
stdout. If APP_CRASH_AT equals the hook, kill yourself with real SIGKILL (9), no
JSON. If APP_PAUSE_AT equals the hook, write DIR/hook.ready with hook name plus
LF, then wait indefinitely holding serialization. External tests send SIGKILL.
Crash precedes pause at the same hook. Unrecognized/unset variables have no
effect. Failures and replays never trigger hooks. A pre-append kill leaves the
old state; a post-append kill leaves the committed operation, replayable by ID.

Ordinary invocations and hook markers complete within 8 seconds (including
lock waiting in tests). Intentional pause is exempt. Every test is bounded at
60 seconds; the suite is bounded at 300 seconds. At most 500 committed commands
and 100 keys are tested. A global lock and full log replay are sufficient.
No child process may survive completion except during intentional pause.

Stack and checks: TypeScript/Bun; build with `make build`.
`make check` runs tsc --noEmit (strict), biome check ., bun test; `make test` runs public tests.
