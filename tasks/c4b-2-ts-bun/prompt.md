# Atomic reference store

Implement an offline, persistent content-addressed store shared by independent
processes. `make build` produces `./bin/app`; `make check` and `make test` pass.
Keep store logic in process in the requested language. No database, daemon,
network, or implementation in another language. Native OS calls and subprocesses
used solely for locking/signaling are permitted. Linux provides `flock`.

## CLI and framing

```
./bin/app COMMAND --root DIR FLAGS
put      --now N --data HEX [--parent OID ...]
object   --oid OID
get      --name NAME
list
transact --now N --id ID --edit NAME:EXPECTED:VERSION:NEW [--edit ...]
log      [--after N]
gc       --now N --grace N
stats
recover
```

COMMAND is first. Remaining arguments are separate flag/value pairs in any order;
no positionals, equals-form flags, or help flag. `--root` is required and nonempty.
Only `--parent` and `--edit` may repeat. Reject unknown, duplicate, missing-value,
and command-inapplicable flags. Validate the entire invocation before creating
or opening DIR. All runtime files, locks, temporary files and hook markers must
be beneath DIR; create missing directories and parents. Paths are ordinary local
Linux directories with no hostile symlinks. The storage layout is your choice.

N and VERSION match `[0-9]+`, range 0..1000000000; leading zeroes are accepted.
All numeric JSON fields are integers. NAME has 1..4 slash-separated segments,
each matching `[a-z][a-z0-9_-]{0,31}`. Names are flat keys: `a` and `a/b` may
coexist. ID matches `[A-Za-z0-9_-]{1,64}`. OID is exactly 64 lowercase hex digits.
HEX is an even number of lowercase hex digits, 0..8192 characters; empty is valid.
EXPECTED and NEW are OID or `-`, which means null. An edit has exactly four
colon-separated components; version is the expected ref version. There are
1..32 edits, with distinct names. There are 0..32 parents, with distinct OIDs.
Sort edits by NAME and parents by OID before further processing. ASCII ordering
is used throughout. No implicit wall-clock sampling occurs.

Success: exit 0, empty stderr, exactly one JSON object plus one LF on stdout.
Errors: empty stdout, exactly one JSON object plus one LF on stderr:
`{"error":{"code":"CODE","message":"nonempty human-readable text"}}`.
Object key order is immaterial; exact key sets, types, nulls and array ordering
are prescribed. There must be no extra output. Message wording is free.

| Code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | Invalid CLI syntax or value |
| NOT_FOUND | 3 | Object or parent or transaction NEW OID does not exist |
| CONFLICT | 4 | At least one expected (OID, version) pair differs |
| ID_REUSED | 5 | Transaction ID exists with different normalized edits |
| TIME_REVERSED | 6 | Fresh mutator has --now smaller than persisted clock |
| IO_ERROR | 7 | Cannot create, read, lock, persist or sync storage |

The initial skeleton uses NOT_IMPLEMENTED, exit 70; replace it.
Precedence: USAGE, storage access/recovery, existing transaction ID handling,
TIME_REVERSED, NOT_FOUND, CONFLICT. Check all NEW OIDs before any expectations.
EXPECTED OIDs need not exist. Semantic errors do not change logical state or
clock. Creating directories/lock files on errors is allowed. IO_ERROR may leave
an entire old or new operation, recoverable on retry. Disk corruption and disk
fault injection are outside the test domain; ordinary access failures are not.

## Objects and graph

Object identity is SHA-256 of these ASCII bytes, including every LF:
`refstore-v1\n` followed by each sorted parent OID plus `\n`, followed by
`\n` then the lowercase HEX string then `\n`. Hash HEX as text, not decoded bytes.
Objects are immutable. Parent objects must exist when put executes under the
store lock. This creates a DAG; sharing and arbitrarily deep chains are allowed.
Put returns `{"oid":OID,"created":BOOL}`. A duplicate returns created:false,
keeps its original unreachable-since time, and still advances the clock to N.
If a collected object is put again, it is new, created:true; parents must again
exist. `object` returns `{"oid":OID,"data":HEX,"parents":[OID,...],"unreachable_since":N_or_null}`;
a missing object is NOT_FOUND.

A live ref (non-null OID) reaches its object and every transitive parent. Neither
reflog entries nor replay receipts are roots. A new unreferenced object has
unreachable_since equal to put's N. On each committed transaction, compute the
new reachable set: reachable objects have unreachable_since:null; a previously
reachable object becoming unreachable gets N; an already unreachable object's
time is unchanged. Reachability through another ref or shared ancestor prevents
that transition. Reattaching and later detaching starts a new grace interval.

## Refs, transactions, replay and reflog

A ref record is `{"name":NAME,"oid":OID_or_null,"version":N}`. An untouched name
reads as oid:null, version:0. Keep tombstones forever. `get` returns the ref
record itself; `list` returns `{"refs":[RECORD,...]}` sorted by name, containing
all touched names, including tombstones, excluding untouched names.

A fresh transaction checks every expected pair against the SAME snapshot. On
any mismatch, apply none of the edits, append no log, consume neither sequence
nor ID, and do not advance time. Otherwise apply all edits atomically. Each
edited ref increments its own version by one, even if NEW equals its old OID,
or both are null. Unedited ref versions do not change. Versions fence ABA,
including create/delete/recreate. Committed transactions receive consecutive
positive sequence numbers starting at 1. Only transactions allocate sequences.

Each change is `{"name":NAME,"old":{"oid":OID_or_null,"version":N},"new":{"oid":OID_or_null,"version":N}}`.
Transact returns `{"seq":N,"changes":[CHANGE,...],"replayed":false}` with changes
sorted by name. Persist the ID, normalized edits, original response, and log
entry atomically with ref changes. Normalization includes parsed numeric version
and sorted edits, and excludes --now. Retrying an ID with equal normalized edits
returns the original seq/changes with replayed:true, even if refs moved, objects
were collected, or the supplied --now is smaller. It changes NOTHING, including
the clock, versions and log. Different edits with that ID give ID_REUSED.

`log` returns `{"entries":[{"seq":N,"id":ID,"now":N,"changes":[CHANGE,...]},...]}`,
ascending seq, containing only entries with seq strictly greater than --after
(default 0). Keep the entire log and replay receipts forever. A successful
fresh put/transact/gc sets the persisted clock to N (initially 0); equal N is
allowed. Reads, recover and transaction replay never advance it.

## GC and recovery

GC is atomic with all other commands. Compute roots consisting of all live ref
OIDs AND all unreachable objects whose `N - unreachable_since < grace`. Protect
these roots and all their transitive ancestors. Delete every unprotected object;
return `{"deleted":[OID,...]}` sorted by OID. Thus the grace boundary is inclusive
for deletion, grace 0 permits immediate collection, and young orphan descendants
protect older parents. The retained graph must remain closed. GC does not change
refs, versions, log, receipts or the unreachable times of retained objects.

`stats` returns exactly `{"clock":N,"seq":N,"objects":N,"reachable":N,"unreachable":N,"live_refs":N,"tombstones":N,"transactions":N}`.
Reachable/unreachable count object nodes (no double-counting shared ancestors),
objects is their sum; transactions equals the number of receipts/log entries.
`recover` returns exactly `{"recovered":true}`. Every command, including reads,
automatically recovers interrupted work before observing state; recover is also
safe and idempotent on an empty or clean root.

All commands must be linearizable across processes, including reads and GC.
Locks must be released automatically after SIGKILL; do not lock an inode later
replaced. Persist success before emitting stdout. Use file and directory fsync
with atomic replacement, or an equivalent durable protocol. An interrupted
operation is entirely old or new, with objects, versions, reachability, receipts
and reflog consistent. No partial transaction or partial logical GC is observable.
A lost response after commit does not undo a committed operation. A snapshot
containing objects is acceptable; physical layout is not prescribed.

## Fault hooks and bounds

Implement these hooks on every successful fresh transact and gc (not replay):

* `txn_prepared` / `gc_prepared`: complete tentative operation prepared, BEFORE
  durable commit. SIGKILL here must recover exactly the old logical state.
* `txn_committed` / `gc_committed`: full operation durably committed, BEFORE
  any stdout. SIGKILL here must recover exactly the new logical state.
* `gc_swept`: after reclamation of deleted object storage, before stdout.
  SIGKILL here must recover the committed new state. Snapshot implementations
  may perform reclamation at commit and reach both committed/swept afterward.

If APP_CRASH_AT equals a reached hook, immediately kill yourself with real
SIGKILL (9), emitting no JSON. If APP_PAUSE_AT equals it, write DIR/hook.ready
containing the hook name plus LF, then wait indefinitely holding serialization;
the tester removes old markers and sends external SIGKILL. Crash takes precedence
at the same hook. Unset/unrecognized values have no effect. Failed operations
and replay must not reach these hooks. All files remain beneath DIR.

An ordinary invocation must complete within 8 seconds, including tested lock
waiting. A hook must publish its marker within 8 seconds; intentional pause is
exempt. Each complete test has a 60-second bound; the complete suite has a
300-second bound. Workloads use at most 1000 objects, 200 refs and 500 transactions.
A global lock and full snapshot are sufficient within these limits. No process
may be left running after an invocation finishes except during intentional pause.

Stack and checks: TypeScript/Bun; build with `make build`.
`make check` runs tsc --noEmit (strict), biome check ., bun test; `make test` runs public tests.
