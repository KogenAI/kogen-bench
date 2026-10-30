# npm-preflight-cache

A methods change to the run harness, not a model result. Two changes, deployed on both Mac runners on 30 October 2026:

1. **Stage locked npm dependencies once** (`patches/npm-stage-once.diff`). A task's `npm ci --ignore-scripts --no-audit --no-fund` setup step used to run again inside Kogen's 120-second approval deadline for every preflight and every run. A stalled install then used up the deadline and refused the whole unit. The harness now installs once per lockfile into an external cache (keyed on the lockfile and package inputs, the command, npm and node versions, OS and architecture), and each preflight/run restores a private copy. A missing cache or changed inputs fail closed; npm is never called inside the deadline. Task kits, task inputs and plan hashes are untouched.
2. **Defer timed-out approvals instead of failing the unit** (`patches/defer-approval-timeouts.diff`, applied on top of the first). A deadline that Kogen actually hit defers the whole task (all lanes and repetitions) behind the ordinary runs, retries it once through the normal host gate with the same 120-second deadline, and otherwise leaves its cells in the plan as an infrastructure gap (dispatch exit 5, incomplete report) and writes a request that the next unit drains. A real refusal is still fatal. Kogen, its approval and snapshot behaviour, and all deadlines are unchanged.

What the change does **not** fix: a slow snapshot step. With a stalled `git add -A -- .` the patched harness still refuses at the deadline (126.756 s); the harness only defers and retries it. See [`reproduce/kogen-approve-deadline-load/`](../kogen-approve-deadline-load/) for the goose-labels-go measurements.

## Tools

No model is called. Real, pinned Kogen builds do the approvals (one pinned artifact per lane, hashes recorded before and after); the run executor in the deferral proof is the model-free `lanes/tests/fixtures/fake-lanes`. Task kits: `task-tags-go`, `bytefmt-go`, `goose-labels-go` (see [tasks.txt](tasks.txt); directories under `tasks/`). Host: two Macs (aliases mac-a and mac-b), Python 3.11+ and the npm and node versions recorded in each cache manifest.

## What is shipped

- `patches/npm-stage-once.diff`, `patches/defer-approval-timeouts.diff`: the `lanes/` changes (new `lanes/lanes/node_modules.py`, `lanes/bin/lanes-stage`, `lanes/lanes/approval.py`, `lanes/lanes/carry.py`, `lanes/bin/lanes-carry`, edits to `cell.py`, `preflight.py`, `dispatch.py`, `report.py`, and the new tests). Both apply in order to the `lanes/` tree of this repository (checked with `git apply`). The host operations scripts that route new launches to the release (`run-queued`, `cc-prep`, `cg-prep`, the two day runners) are host-specific and are not published; the pack describes only their effect.
- `faulttests/`: the four fault-test drivers as run (provenance copies with the paths turned into environment variables; they need the pinned Kogen artifacts and the private task kits and run directories, so they are not runnable standalone): `npm-stall-preflight.py` (npm stalls for 600 s, old and new harness), `git-add-stall-preflight.py` (only `git add -A -- .` stalls), `approval-deferral-fault.py` (setup stalls 125 s for one lane) and `completed-resume.py` (a completed task is not re-approved).
- `runs.csv`: one row per approval check: change, host alias, harness (patched or unpatched), fault, task, lane, stage, outcome, passed (= approved), seconds, deadline, npm calls observed, timed out. `tests.csv`: one row per test run. No logs, paths or hostnames.
- `analyze.py`, `expected-output.txt`.

## Rerun

Apply the patches and run the lane test suite offline (no model call):

```sh
git apply reproduce/npm-preflight-cache/patches/npm-stage-once.diff && git apply reproduce/npm-preflight-cache/patches/defer-approval-timeouts.diff && lanes/test.sh
```

The fault tests need a lanes run directory with a pinned Kogen artifact for the task. With `FAULT_ROOT`, `LANES_PRIVATE`, `NPM_STAGE_CACHE` and `OLD_LANES_RELEASE` set (see the drivers' headers), the npm stall test is

```sh
python3 reproduce/npm-preflight-cache/faulttests/npm-stall-preflight.py old && python3 reproduce/npm-preflight-cache/faulttests/npm-stall-preflight.py new
```

(`old` must refuse at the deadline with npm calls recorded; `new` must approve with zero npm calls), and the deferral test is `python3 reproduce/npm-preflight-cache/faulttests/approval-deferral-fault.py`, which asserts its own expectations and prints `FAULT PROOF PASSED`. Run these as the unprivileged benchmark user; use the default timeouts; each takes a few minutes. The unit tests in the original runs passed on both hosts (66 and 95 tests); they were **not** rerun against this repository's `lanes/` tree for this pack, only the patch application was checked.

## Reproduce the numbers

```sh
python3 -I reproduce/npm-preflight-cache/analyze.py | diff - reproduce/npm-preflight-cache/expected-output.txt
```

Verified 30 October 2026: this reproduces every published time, count and test total exactly.

## Expected results

Preflight with npm stalled for 600 s (deadline 120 s):

| Harness | Host | Task | Seconds | npm calls | Result |
|---|---|---|---:|---:|---|
| patched | mac-a | task-tags-go | 54.485 | 0 | approved |
| patched | mac-a | bytefmt-go | 14.609 | 0 | approved |
| patched | mac-b | task-tags-go | 36.191 | 0 | approved |
| patched | mac-b | bytefmt-go | 5.886 | 0 | approved |
| unpatched | mac-a | task-tags-go | 192.361 | 1 | refused at setup-1 (npm ci) |
| unpatched | mac-a | bytefmt-go | 120.431 | 2 | refused at setup-1 (npm ci) |

Total seconds include workspace preparation and cleanup; the approval deadline is still 120 s. Normal cached goose-labels-go preflight: 23.659 s, approved, 0 npm calls. Stalled `git add -A -- .`: refused after 126.756 s, `approve refused (timed out): no output`. The literal historical `status 143` text was not reproduced, because process-group cancellation suppressed it in that run.

Deferral proof (setup stalled 125 s for `task-tags-go`, lane a0, real Kogen approvals, model-free executor): bytefmt-go approved at 8.665 s and 7.775 s; task-tags-go a0 timed out at 132.848 s while its other lane was approved (53.135 s) so the whole task was deferred; after the two ordinary cells ran, a0 timed out again (128.133 s); on a later invocation both lanes approved (44.420 s, 50.770 s) and all four planned cells started with none re-run. First dispatch exit 5, later exit 0, 2 deadline failures, 0 provider calls, total 483.566 s. The published table lists 8 of the 10 approval rows; the other two are bytefmt-go re-checks at the start of the later invocation (4.829 s, 5.034 s; the final source skips approvals for completed tasks, proved separately by `completed-resume.py`: zero new approvals, zero new cells).

Tests: 66 passed on each host (87.923 s and 71.476 s) for the first change, 95 for the second (46.761 s; 41.751 s with one skip because `go` was not on the SSH `PATH`, passing at 0.525 s in the runner environment). Dependency parity: staged `node_modules` equal to a fresh install for task-tags-go, bytefmt-go and goose-labels-go on both hosts (2,510 entries each; file list, SHA-256, modes and symlink targets; lockfile hashes matched).

## Cost

No model calls, no API or subscription spend. The proofs used one machine for a few minutes each.

## Limits

Two hosts, two real task kits plus goose-labels-go, one fault at a time. The fault tests show the approval deadline is no longer consumed by npm and that a timed-out approval no longer loses a task; they do not show that approvals can never time out, and they do not locate the cause of the original goose-labels-go timeout.
