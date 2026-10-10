# Worktree landing queue

Implement a local CLI for isolated changes to a Git repository. Use the system
`git` executable through subprocesses. Implement the controller in the selected
language; do not delegate it to an interpreter or another language. The Linux
runtime supplies Git, `/bin/sh`, and `flock`. Everything must build and run offline.
`make build` produces `./bin/app`; `make check` runs the supplied stack checks.

## Invocation and output

```
./bin/app init   --root DIR --source REPO --target refs/heads/BRANCH
./bin/app create --root DIR --name NAME --base REF
./bin/app record --root DIR --name NAME
./bin/app land   --root DIR --name NAME --check COMMAND [--attempts N]
./bin/app abort  --root DIR --name NAME
./bin/app list   --root DIR
```

Flags may appear in any order after the subcommand. Every flag has exactly one
value. Unknown, repeated, missing, or inapplicable flags and positional arguments
are `USAGE`. `N` is decimal digits with value 1..10 (default 3). NAME matches
`[a-z][a-z0-9_-]{0,39}`. A target must be a valid full `refs/heads/` ref, excluding
`refs/heads/changes` and all refs under `refs/heads/changes/` (reserved for
working branches). Do not treat data arguments as shell
syntax or Git options. The check string alone is intentionally shell syntax.

Success exits 0, with empty stderr and exactly one LF-terminated JSON object on
stdout. Errors have empty stdout and exactly one LF-terminated JSON object on
stderr: `{"error":{"code":"CODE","message":"nonempty diagnostic"}}`.
Messages are not otherwise prescribed. Object key order is immaterial; object
fields below are exact. Arrays have the specified order. No progress output,
timestamps, or subprocess output may leak into these streams.

All created files, Git objects, refs, metadata, locks and worktrees must be under
DIR. The source is read-only and may be outside DIR; no source refs, configuration,
worktree registrations or files may be changed. DIR is not inside the source.
Canonicalize DIR for reported paths. Names are not reusable, including after abort
or land. The caller owns DIR and does not replace its contents with symlinks or
edit controller metadata. Git repos use SHA-1. Repositories have an initial commit,
local identity configuration, no hooks/submodules, and no signing requirement.

## Initialization and changes

`init` creates a private bare repository at `DIR/repo.git`, copying the source's
objects and branch refs without relying on source object storage. It also copies
`user.name` and `user.email` if configured in the source. Source may be bare or
non-bare. Resolve the target to a commit and retain its full ref as the configured
target. Missing/noncommit target or base is `BAD_REF`. An already initialized root
is `EXISTS`. Other commands on an uninitialized root are `NOT_INITIALIZED`.
Output: `{"repo":"<absolute DIR/repo.git>","target":"<full ref>","head":"<oid>"}`.

`create` resolves REF to a commit in the private repository and creates the
linked worktree `DIR/worktrees/NAME` on branch `changes/NAME` at that commit. Its
state starts open with base=head=that OID and commits=[]. Output is the change
object defined below. Existing names produce `EXISTS`.

Users edit and commit with ordinary Git in the worktree. `record` snapshots its
current HEAD. The worktree must be clean, including no untracked files (`DIRTY`).
HEAD must descend from the stored base by a linear sequence with no merge commits
(`BAD_HISTORY`). Save HEAD and all commits in `base..HEAD`, oldest first. Repeated
record is allowed, including an empty sequence. Pin recorded heads with persistent
Git refs before operations that might replace or remove them. Output is the change
object. Record on a terminal change is `STATE_ERROR`.

Every change object has exactly these fields:

```
{"name":"NAME","status":"open|landed|aborted","base":"<oid>",
 "head":"<oid>","commits":["<oldest oid>","<next oid>"],
 "path":"<absolute DIR/worktrees/NAME>"}
```

`list` outputs `{"target":"<full ref>","head":"<current target oid>",
"changes":[<change objects>]}`; sort changes by ASCII name. Listing reports
recorded state, not unrecorded worktree commits. Unknown names are `NOT_FOUND`.
All state survives a new process. Atomic state publication and process-safe locks
are required; separate names must be able to execute checks concurrently.

## Landing

`land` acts on the recorded sequence, without squashing or manufacturing a landing
commit. For an open change, reject a dirty worktree (`DIRTY`), an actual HEAD that
differs from recorded HEAD (`UNRECORDED`), or an empty sequence (`EMPTY_CHANGE`),
in that order. A landed change is idempotent: return its saved change object and
attempts=0, without running the check. An aborted change is `STATE_ERROR`.

Each attempt (1..N) works as follows:

1. Read the target. If it differs from the stored base, rebase exactly the change's
   `base..head` sequence onto the observed target in its worktree. On conflict,
   abort the rebase, restore the pre-attempt HEAD and clean worktree, report
   `CONFLICT`, and stop. Do not update the target. On successful rebase, pin both
   old and new heads and atomically save the new base, head and commit sequence.
   Empty commits/patches must be preserved, even if the target already has their
   tree changes; do not silently drop commits during rebase.
2. Run `/bin/sh -c COMMAND` in that worktree and wait. Capture and discard both
   streams. Set `LAND_ROOT` (absolute DIR), `LAND_TARGET` (full ref), `LAND_HEAD`
   (candidate OID), `LAND_EXPECTED` (attempt base OID), and `LAND_ATTEMPT` (decimal
   attempt index). A nonzero check exits `CHECK_FAILED`; the rebased recorded state
   remains available for another invocation. Check failure precedes the next step.
3. Verify HEAD and worktree still exactly match the checked candidate. A changed
   HEAD, tracked file, index or untracked file is `CANDIDATE_CHANGED`. Preserve any
   new HEAD, but do not silently record it or land it.
4. Compare-and-swap the target from that exact base to that exact candidate OID,
   e.g. `git update-ref TARGET HEAD BASE`. Only success marks the change landed.
   On a lost comparison, start the next attempt, rebase onto the newly observed
   target, and run the check again. After N unsuccessful comparisons, report
   `RETRY_EXHAUSTED`. N bounds CAS opportunities, not just rebase operations.

Successful output is `{"change":<saved change object>,"attempts":<integer>}`.
A successful land retains its worktree. Abort on a landed change is disallowed;
no cleanup of landed worktrees is required. In all failure cases, the controller must never overwrite another
writer's target. An externally moved target stays at its externally written value.
Use the Git CAS primitive; a read followed by an unconditional write is incorrect.

## Abort, preservation, and interruption

`abort` on an open change first preserves its current committed HEAD, including
commits made since the last record. Remove the linked worktree (dirty files may be
discarded), remove its working branch, and mark it aborted. Its reported base,
head and commits remain the last recorded values. Output is the change object.
A repeated abort returns the same object. Abort on landed state is `STATE_ERROR`.
No recorded or rebased-away committed head, or committed HEAD present at abort,
may become unreachable after reflog expiration and immediate Git garbage
collection. Keep permanent refs inside the private repository, even after abort.
Uncommitted dirty file preservation is not required.

Two land processes for different names may race; both must eventually land their
commits when checks pass and the attempt budget suffices. Two processes for the
same name must serialize and return one applied result plus an idempotent result.
Process locks must be released by the OS if a process is killed. Tests may kill
a controller while its check is waiting, before CAS; this must leave the target
unchanged and allow a later land/abort to proceed. A running check must continue after the controller alone is killed with SIGKILL;
the controller must not arrange parent-death termination of its check. The test
releases and waits for that check before invoking another command. Checks in interruption tests
never alter Git state and are released before the next command. Full recovery
from power loss, arbitrary disk corruption or a crash inside Git rebase is out of
scope. Git failures unrelated to ref comparisons produce `GIT_ERROR`.

## Errors

| Code | Exit | Meaning |
| --- | --- | --- |
| USAGE | 2 | Invalid command, flags, name, target syntax or attempt count |
| NOT_INITIALIZED | 3 | Root has no initialized controller state |
| EXISTS | 4 | Root already initialized or change name already used |
| NOT_FOUND | 5 | Change name unknown |
| BAD_REF | 6 | Ref does not resolve to a commit |
| STATE_ERROR | 7 | Operation disallowed in terminal state |
| DIRTY | 8 | Worktree/index/untracked files are not clean |
| UNRECORDED | 9 | HEAD differs from the recorded candidate |
| EMPTY_CHANGE | 10 | No recorded commits to land |
| BAD_HISTORY | 11 | Candidate is not a linear descendant of its base |
| CONFLICT | 12 | Rebase conflict; rebase has been aborted |
| CHECK_FAILED | 13 | Configured check returned nonzero |
| RETRY_EXHAUSTED | 14 | All allowed CAS attempts lost |
| CANDIDATE_CHANGED | 15 | Check changed the candidate |
| GIT_ERROR | 16 | Other Git subprocess failure |
| IO_ERROR | 17 | Other filesystem/process failure |
| NOT_IMPLEMENTED | 70 | Starter placeholder only |

Validate invocation before reading or creating state. After that, check root
initialization before looking up a name. Multiple simultaneous unrelated errors
are not tested except where a precedence is explicitly stated above.

Stack and checks: Gleam 1.18.1 on Erlang/OTP 29; build with `make build`.
Checks: `make check` runs gleam format --check src test, gleam build --warnings-as-errors, gleam test; dependencies are vendored offline; `make test` runs public tests.
