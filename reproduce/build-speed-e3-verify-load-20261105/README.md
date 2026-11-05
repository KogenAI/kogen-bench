# Verify timeouts and land-red under load: no re-run possible, log evidence only

Lab lever `build-speed-e3-verify-load-20261105` (Studio, product kogen, revision 2 before any run) asked whether the 10 `host_or_base_failure` Builds and a sample of the 28 land-red retries from 3 to 5 Nov are load-induced (pass solo, fail loaded), flaky (mixed within an arm) or real (fail solo). Arm A re-runs the failing check solo on a quiet host, arm B under the E2 replayed 4-Build load, 3 reps each. The fix is chosen by the dominant class: a scheduling or timeout fix if load-induced, one rerun before requeue if flaky, nothing if real.

**No tree was re-run, so none of the 20 items is classified and no fix is chosen. The verdict is unresolved.** Both arms need a quiet host, and EU never met the registered guard (see the E2 pack `build-speed-e2-go-lock-20261105`: 2.8% of monitored samples passed, longest stretch 20 s). The original candidate and land trees are also gone on every host (the `src` directories were deleted), so the re-run would have used proxy trees: the repository at the commit current when the Build started (or, for land-red, kogen-build main at the landing time). A pass on a proxy tree would have meant "not reproduced", not "load-induced".

## What the retained evidence says

The 20 items and the exact check each would have run are in `data/e3-items.json`; `python3 -I report.py` prints the numbers below.

**host_or_base (10 Builds).** Every one spent 1,227 to 1,668 s in its final verify phase, which fits two passes that each ended at go test's default 10-minute timeout. The Build logs that remain name the cause for four of them:

- Three kogen-verification Builds: `panic: test timed out after 10m0s` with `TestProbeCustodyAndResults (10m0s)` running, in `contract` or `verify`, in passes 1 and 2 alike. The test arms a 200 ms probe deadline and expects the process group to be gone; the goroutine dump shows it waiting in `kogen-loop/sys.(*Session).awaitTimeout`. A hang that repeats identically in two passes looks deterministic for that tree, but it passed on the later main in uncontrolled EU runs of the whole suite (rc 0, 41 to 77 s, load1 1.5 to 4.4), so it is not a plain failure at today's head.
- One kogen-loop Build: `panic: test timed out after 10m0s` after the shell lifecycle tests in `sys` failed at 5 to 18 s each (deadline and group-kill tests, which are time-sensitive).
- Six kogen-shaping Builds, all on eu2: the retained extracts record `go-test failed` in passes 1 and 2 and a final verify of 1,232 to 1,645 s; the log text itself was not read because eu2 was held by another Lab. They are unexplained here.

**land-red (28 retries; sample of 10).** The recorded failure text of all 28 rows (`data/landred-28.json`):

| Recorded signature | Rows (28) | In the sample of 10 |
|---|---|---|
| Assertion or golden mismatch in a named test (log line differs at byte N, no scripted executor round left, identity not current, missing file) | 14 | 8 |
| Compile or API drift against a moved dependency | 3 | 0 |
| Only "FAIL" or no cause line | 9 | 2 |
| Model usage limit or push failure (not a test) | 2 | 0 |
| Mentions a timeout or deadline | 0 | 0 |

The sample is the first ten chronological rows that name a kogen-build test (`TestBuildRequestBudgetOff` three times, the external-review pair, the context-external pair, `TestNativeConformance`, `TestCommitLandsTheReviewedTree`, a legacy-review test). Nothing in the 28 looks like a load symptom; the signatures point to deterministic or environment-dependent failures of a candidate merged onto a moved main. That is a reading of log text, not a Lab classification, and it cannot separate "real" from "flaky" without re-runs.

## Verdict and decision

Unresolved. By the registered rule no bucket can name a fix: a timeout or scheduling fix needs the load-induced result for the host_or_base bucket, and a one-rerun-before-requeue rule needs flaky results for land-red, which the signatures do not suggest. No delivery request is filed. The strongest lead is the 10-minute hang of `TestProbeCustodyAndResults`; the cheap next test is that one test, `go test -count=1 -run TestProbeCustodyAndResults ./verify ./contract` on the kogen-verification commit that was main when each of the three Builds started, solo and then beside four parallel suites, on a quiet host with at least 4 cores.

## Rerun

Needs the apparatus from the E2 pack (`scripts/` there: `heavy-lab.sh`, `e2.py`, `sched.json`) plus `scripts/e3.py` here, a Linux host with Go 1.27 and Node 24, network for module fetch, and a quiet machine.

1. Prepare trees as in the E2 pack at `$W/trees/<repo>` (full clones of the public repos, for example [kogen-verification](https://github.com/KogenAI/kogen-verification) and [kogen-build](https://github.com/KogenAI/kogen-build)); `e3.py` adds a detached worktree per item at the commit current at the item's `at` time and copies the cucumber `node_modules`.
2. Put `data/e3-items.json` and the E2 `sched.json` in `$W/bin`, set `W`, and run `python3 e3.py $W/bin/e3-items.json $W/bin/sched.json <outdir> 3 1` (3 reps, 1 for the shaping full suite). It calls `gate.sh quiet` before every phase, runs arm A, then arm B with the E2 arm-B load looped in the background, and writes `runs.jsonl`.
3. `python3 -I scripts/analyze_e3.py <outdir>` prints the class per item (real, flaky, load-induced, not-reproduced) and the counts per bucket.
