# Incremental tree watcher

Implement an offline polling watcher in the requested language, in process.
`make build` creates `./bin/app`; `make check` and `make test` pass offline.
Use ordinary filesystem APIs, not inotify, external scanners, databases, or
network services. Subprocesses solely for locking/signaling are permitted;
Linux `flock` is available. Separate scanning, event reconciliation, and durable
state management into modules. Each `poll` performs one scan and exits; a caller
schedules polls. No resident daemon is required.

## CLI

```
./bin/app init   --root DIR --state DIR --debounce-ms D TIME
./bin/app poll   --root DIR --state DIR TIME
./bin/app events --state DIR [--after ID]
./bin/app ack    --state DIR --through ID
./bin/app status --state DIR
TIME = exactly one of --now-ms N or --clock-file REL
```

Command comes first. Flags are separate flag/value pairs in any order. Unknown,
repeated, missing-value, command-inapplicable flags, extra positionals, empty
paths and missing required flags are USAGE. There is no help flag. Numbers match
`[0-9]+`, accept leading zeroes, and are integers: N is 0..4000000000000,
D is 0..60000, ID is 0..4000000000000. Validate syntax before opening storage.
`--clock-file` is a relative slash-separated path beneath state, with no empty,
`.` or `..` component; it cannot start with `/`. Read it once after acquiring
serialization. Its exact bytes must be `[0-9]+` optionally followed by one LF,
with the same range as N; other contents are BAD_CLOCK. Missing/unreadable clock
is IO_ERROR. No real-time fallback. `events`, `ack`, `status` neither sample time
nor scan root.

Root must be an existing directory. State is created, including parents.
Canonicalize both paths; state may be inside root, in which case exclude that
entire subtree from every scan (including init). State must not equal root or be
an ancestor of root: ROOT_MISMATCH. Persist canonical root at init; subsequent
polls require exactly that canonical root. Aliased spellings of the same root
are accepted. State and root paths have no hostile symlink races. Only read
watched entries under root and the clock under state; all runtime writes,
locks, temporaries and hook markers are under state. Do not read symlink targets.

Success: exit 0, empty stderr, exactly ONE JSON object plus LF on stdout.
Member order is immaterial; arrays follow the ordering below. No extra members,
duplicate keys, NaN/Infinity or other output. Numeric fields are JSON integers;
boolean fields are JSON booleans. Errors: empty stdout, exactly one object plus
LF on stderr: `{"error":{"code":"CODE","message":"nonempty text"}}`.
Message wording is free. Codes and exits:

| Code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | Invalid CLI syntax/value |
| NOT_INITIALIZED | 3 | No committed watcher exists (except init) |
| ALREADY_INITIALIZED | 3 | init against an existing valid watcher |
| ROOT_MISMATCH | 4 | Invalid state/root containment or different bound root |
| BAD_CLOCK | 4 | Invalid fake-clock contents |
| TIME_REVERSED | 4 | N less than the last successful init/poll time |
| ACK_RANGE | 4 | through greater than the largest assigned batch ID |
| IO_ERROR | 5 | Filesystem, scan, lock or persistence failure |
| CORRUPT_STATE | 6 | Malformed/inconsistent committed storage |

After syntax: load/validate state, check initialization, root, clock, then time
or ack range, in that order where applicable. A missing root is IO_ERROR.
Errors must preserve logical state; creating state/lock directories is allowed.
A failed scan must not advance time, observed snapshot or debounce deadline.
The starting skeleton uses NOT_IMPLEMENTED/70; replace this behavior.

## Snapshots and net event reconciliation

Recursively enumerate regular files and symlinks; directories are traversed but
are not entries and produce no events. Include dotfiles. Symlinks, including
broken links and links to directories, are entries of kind `symlink` and are
never followed. Ignore other file kinds. Paths are relative to root, use `/`,
and retain exact UTF-8 (no Unicode normalization). Tested names/link text are
valid UTF-8 and may contain whitespace/newlines/non-ASCII. Tested roots contain
at most 1000 entries, depth at most 16, regular files at most 1 MiB each.

Each entry records `(kind, device, inode, hash)`. Identity is `(kind, device,
inode)` from lstat; preserve full integer precision internally. Hash is lowercase
64-hex SHA-256 of regular-file bytes or of UTF-8 symlink text returned by
readlink. mtime, ctime, mode and directory metadata are irrelevant. A snapshot
changes iff its path map or any recorded tuple changes. Hash bytes on each poll,
even if size and mtime are unchanged. The tree is stable during each scan;
changes between polls, including changes while the process is stopped, are
observed at the next poll. A transient never present at any scan is out of scope.

Reconcile two snapshots B (last sealed baseline) and O (latest observation) with
this EXACT algorithm; comparisons/sorting use unsigned UTF-8 byte order:

1. Match entries at the same path with the same identity. Emit `modify` iff their
   hashes differ, then remove these entries from both unmatched maps.
2. For every identity remaining in both maps, sort its old and new paths and zip
   the lists up to the shorter length. Emit one `rename` per pair and remove it.
   This handles hard links deterministically. A rename may also change content;
   do not emit a separate modify. Never guess a rename from hash equality alone.
3. For unmatched old/new entries at the same path, emit `modify` (replacement,
   even with equal hashes or different kinds), and remove both.
4. Emit `delete` for remaining old entries and `create` for remaining new entries.

Every event has exactly these fields:
`{"type":"rename","path":"to","from":"from","kind":"file",`
`"old_hash":"...","hash":"...","modified":false}`.
Kind is `file` or `symlink`: use new kind, except delete uses old kind. `from` is
an old path ONLY for rename, otherwise null. `old_hash` is null ONLY for create;
`hash` is null ONLY for delete. `modified` is true for every modify, true for a
rename iff old/new hashes differ, false for create/delete. Sort the final event
array by `(path, type, from-or-empty-string)` in UTF-8 byte order. This is net
reconciliation: a->b->c within a window becomes a->c; create then delete cancels;
modify then restore cancels if the identity is unchanged. Path swaps remain
renames. Directory moves become file/symlink renames for all descendants.

## Global trailing debounce

Init scans root, sets B=O to that snapshot, sets last_poll=N, pending_since=null,
next batch ID=1, acknowledged=0, and an empty outbox. Existing files do not emit
creates. Response: `{"initialized":true,"entries":COUNT}`.

A successful poll first scans S. If S differs from stored O, set O=S and
pending_since=N. If O equals B, clear pending_since. Otherwise keep it (including
when S did not change). One global window applies to the ENTIRE tree: an unrelated
change postpones all pending events. If pending_since is non-null and
`N >= pending_since + D`, reconcile B->O, append ONE nonempty batch to the outbox,
advance B=O, clear pending_since, and increment next ID. Debounce 0 seals in the
same poll that observes a change. Always persist O, pending_since, last_poll=N,
B, and outbox atomically. Poll response is exactly:
`{"now_ms":N,"pending":BOOL,"emitted":BATCH_or_null}`.
Batch is `{"id":ID,"at_ms":N,"events":[EVENT,...]}`. Its time is the sealing poll's
time, never the first change or scheduled deadline. Equal poll times are allowed;
backward time fails without mutation. A poll arriving after a long gap scans
FIRST: if it sees a further change, the deadline resets before any sealing.

Example D=50: observe a change at 10, another at 40, unchanged polls at 89 and 90;
only the poll at 90 seals, with at_ms=90. A restart at 89 retains pending work.

## Durable outbox and restart semantics

`events` returns `{"batches":[BATCH,...]}` in increasing ID order containing only
unacknowledged IDs strictly greater than after (default 0). It never mutates the
outbox; repeat reads deliberately replay the same batch with the same ID/time.
`ack` cumulatively discards batches with ID <= through and advances acknowledged
to max(old,through). through=0 and stale acknowledgments succeed as no-ops;
through may not exceed next ID-1. Response: `{"acknowledged":ID}`.
Acknowledgment does not reset B/O/debounce, so a second window may progress while
older batches await ack. No gaps or ID reuse, even after all batches are acked.
`status` returns exactly `{"last_poll_ms":N,"pending_since_ms":N_or_null,`
`"next_batch_id":ID,"acknowledged":ID,"queued_batches":COUNT,"entries":COUNT}`;
entries counts O. Reads remain available even if root no longer exists.

Persist both observed and baseline snapshots, pending time, IDs, and outbox.
Commit durable state before printing. Use atomic replacement with file AND
parent-directory fsync, or equivalent durable primitives. Serialize the complete
read/scan/commit across concurrent invocations. Locking must recover automatically
on SIGKILL; never lock an inode later replaced. An interrupted transaction is
entirely old or entirely new. A lost poll response is recovered via events, with
no second assigned batch; an acknowledged batch never reappears. This is exactly
once batch assignment plus explicit replay/ack, not an impossible atomic stdout
and disk promise. Ignore/discard incomplete temporary files. Detect malformed or
inconsistent committed storage rather than silently reinitializing. Committed watcher data must use one or more regular files beneath
`state/storage/`; put only committed data there. Locks, hook markers and uncommitted temporary files must
remain elsewhere beneath state. The committed file names and format within
storage are your choice. Tests may replace regular-file contents beneath
`state/storage/` with garbage, `{}`, `null`, or truncated bytes while no
invocation runs; they never corrupt locks or uncommitted temporary files.

## Deterministic crash and pause hooks

Implement on EVERY successful invocation, including reads/no-ops:
`after_lock` (exclusive serialization acquired, before load), `before_commit`
(tentative result ready, before commit), `after_commit` (durable, before stdout).
If `APP_CRASH_AT` equals the hook, self-terminate with real SIGKILL, no JSON.
If `APP_PAUSE_AT` equals it, write `state/hook.ready` with hook name plus LF and
wait indefinitely retaining the lock. Crash takes precedence. Other/unset values
have no effect. Tester removes old markers. On reads, commit hooks bracket a
logical no-op. Before-commit kill preserves old state; after-commit kill preserves
new state. Hook waits are exempt from ordinary deadlines. Trees remain stable
while a paused scan/transaction runs.

Ordinary invocations, including tested contention, must complete in 6 seconds;
a pause marker must appear in 6 seconds. Each complete test is limited to 45
seconds and the entire suite to 240 seconds, including hanging implementations.
