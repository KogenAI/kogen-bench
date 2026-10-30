# kogen-approve-deadline-load

Why did the `goose-labels-go` approval fail with "approve refused (timed out): controller/internal_error: git add -A -- . failed (status 143)"? The measurements say the `git add` step is not slow (0.26–0.39 s for 2,373 files). The 120-second approval deadline is shared by task setup, the build/check step and the candidate snapshot, and the cold setup/check work is CPU-heavy (a cold `go build` costs 42 CPU-seconds, a warm one 0.66 s). On a host with under 10% idle CPU that work could use the deadline up, and the error names whichever step is running when it expires, which here was `git add`. This explanation is unconfirmed; see Limits. The product decision (how Kogen should budget the deadline) was sent to delivery (the Kogen product side); this pack covers the measurements only. 30 October 2026.

## What was measured

Single measurements on a copy of the task's start tree, on one Mac runner with 44–74% idle CPU (the original refusal on 29 October happened with under 10% idle CPU). No model was called.

- Tree: 2,374 files, 73 MB; `vendor/` holds 2,117 files (71.7 MB of vendored Go dependencies). After `npm ci`, `node_modules` holds 2,227 files (27.5 MB); it is gitignored, so 0 of its files are staged.
- `git add -A -- .` into a fresh `GIT_INDEX_FILE`: 0.39 s without `node_modules`, 0.26 s with it; 2,373 files staged, no build output staged.
- `go build ./...` with `GOFLAGS=-mod=vendor GOPROXY=off`: cold `GOCACHE` 9.66 s wall and 42.1 s user CPU; warm 0.66 s.
- `npm ci` from a warm npm cache: 0.46 s. (Before 30 October the harness ran an uncached install inside the deadline; it now stages it once per lockfile, see [`reproduce/npm-preflight-cache/`](../npm-preflight-cache/).)
- Cross-checks from the harness change: a normal cached preflight of the same task passes in 23.659 s; with `git add -A -- .` made to stall, the patched harness refuses after 126.756 s (`approve refused (timed out): no output`). So a slow snapshot step is exposed to the same deadline; it is just not slow in normal conditions.

## Tools

No model. `git`, `go` (the version in the task's `go.mod`), Python 3 and npm. Task: `goose-labels-go` ([tasks.txt](tasks.txt), a directory under `tasks/`). Kogen is the pinned build used by the original preflight; the harness is the `lanes/` release before and after [`npm-preflight-cache`](../npm-preflight-cache/).

## Rerun

On a copy of the task's start tree (never the original), as the unprivileged benchmark user, one heavy job at a time, default timeouts:

```sh
reproduce/kogen-approve-deadline-load/profile.sh "$COPY_OF_TASK_START_TREE" profile.csv
```

`profile.sh` prints one CSV row per step (wall seconds, CPU seconds, file counts) in the same steps as `runs.csv`. It was written for this pack from the measurement note, because the original ad-hoc commands were not kept, and it was run only on a small synthetic Go and npm tree (not the real task tree, which is not published) to check that every step executes and prints a row. It has not been run on the original task, so treat its output as a re-measurement, not a replay. Expect different seconds on a different host; the shape (git add well under a second, cold build tens of CPU-seconds, warm build under a second) is what to compare. To rerun the end-to-end preflight, see the fault tests in [`reproduce/npm-preflight-cache/faulttests/`](../npm-preflight-cache/faulttests/).

## Reproduce the numbers

```sh
python3 -I reproduce/kogen-approve-deadline-load/analyze.py | diff - reproduce/kogen-approve-deadline-load/expected-output.txt
```

This reads [runs.csv](runs.csv) (the published measurements, one row each) and prints them with the ratios used in the text (git add is 0.33% of the deadline at most; cold/warm build wall 14.6×). Verified 30 October 2026: it reproduces every measured number in the note exactly. The note's numbers are the only source; the ratios are derived by `analyze.py`.

## Cost

No model or API spend; a few CPU-minutes on one runner.

## Limits

One measurement per step, no repetitions, one host, and the host's CPU load during the profile (44–74% idle) was lighter than during the original refusal (under 10% idle). The explanation (deadline used up by cold setup/check work, `git add` simply the running step) is an inference from these timings and from the error naming the running step; the original refusal's elapsed time and CPU contention were not recorded, so the load effect itself was not measured. The harness work separately showed that a stalled `git add` alone also refuses at the deadline. Kogen itself (approval, snapshot, deadline) was not changed.
