# Lab C1 confirmation: continuous reaping in the Linux check helper

Finding id: `lab-c1-reaper-confirm-20261105`. Comparison: kogen-verification. Model-free: no model call, no seat tokens.
Verdict: **yes**, under a recorded reading of the registered rule (see Verdict). One Linux host, 10 repetitions, 150 measured runs. Follows the interim finding [lab-c1-linux-reaper-zombies-20261105](../lab-c1-linux-reaper-zombies-20261105/README.md).

## Question
The Linux acceptance-reaper helper of kogen-verification only waits for its shell, and reaps what it adopted afterwards. While a check runs, a process it adopted and that exits stays a zombie, so a test that kills a process group and waits for it to be gone hangs until the 10-minute test timeout. Does a helper that reaps every exited child while the shell runs remove the hang and still leave no orphan?

## Arms
- **A**: the released helper (the d98cfe01 release `kogen` binary, kogen-verification [3cb7305a](https://github.com/KogenAI/kogen-verification/tree/3cb7305a56907d7105cd20cf51de6767f488fbf6)), unchanged.
- **B**: the same tree with one change in `runAcceptanceReaper`: a blocking `wait4(-1)` loop replaces the wait on the shell, so every exited child is reaped at once and the shell's status is returned unchanged (`harness/helperb/main.go` is the launcher that calls it).
- **C**: no helper, `/bin/sh -c '<check>'`.

## Workload and metric
- **go-test:** each repo's own go-test check, run literally, on frozen trees: kogen-shaping [3696dba](https://github.com/KogenAI/kogen-shaping/tree/3696dba67f13c16aae5978c943d9a6ec844c5b63), kogen-verification main [6ffb2d1a](https://github.com/KogenAI/kogen-verification/tree/6ffb2d1a24a4dd07a6ad4e65a88269845fecffbd), kogen-loop main [268327e7](https://github.com/KogenAI/kogen-loop/tree/268327e7f9503310dd9834f17f283effa17a2c09).
- **sweep:** kogen-verification's orphan-sweep tests plus the climb-launcher test that starts detached servers in python, node, perl and go.
- **fixture:** four detached servers, then a kill-group zombie probe that kills a group and polls its orphaned member for up to 5 s.
- **Metric:** pass or fail (exit status, go test FAIL or timeout), wall seconds, and orphans (a process still present 1.5 s after the check returned that carries the run's marker or a recorded pid).
- **n:** 3 repos x 10 repetitions x 3 arms = 90 go-test runs on lm, plus 30 sweep and 30 fixture runs. Arm order rotated by repetition. The registered plan was 2 hosts x 5 repetitions; the host split was changed to one host (see Verdict).
- **Registered rule:** B passes 30 of 30 within 10 percent of C's duration and leaves 0 orphans, and A fails at least 80 percent.

## Results (lm, 10 repetitions)
| unit | arm | pass | median s (min-max) | orphans alive | 10 min timeouts |
|---|---|---|---|---|---|
| kogen-shaping go-test | A | 0/10 | 641.0 (605.1-641.4) | 0 | 10 |
| kogen-shaping go-test | B | 10/10 | 238.4 (204.5-250.7) | 0 | 0 |
| kogen-shaping go-test | C | 10/10 | 240.4 (219.2-261.5) | 0 | 0 |
| kogen-verification go-test | A | 10/10 | 69.1 (68.7-69.5) | 0 | 0 |
| kogen-verification go-test | B | 10/10 | 68.9 (68.8-69.6) | 0 | 0 |
| kogen-verification go-test | C | 10/10 | 68.9 (68.5-69.1) | 0 | 0 |
| kogen-loop go-test | A | 0/10 | 649.7 (602.1-652.2) | 0 | 10 |
| kogen-loop go-test | B | 10/10 | 84.8 (32.8-87.7) | 0 | 0 |
| kogen-loop go-test | C | 10/10 | 86.1 (65.5-87.8) | 0 | 0 |
| sweep (orphan-sweep tests + detached-server launcher) | A, B, C | 10/10 each | 11.6 | 0 | 0 |
| fixture zombie probe | A | 0/10 | 5.2 | 0 | 0 |
| fixture zombie probe | B | 10/10 | 0.2 | 0 | 0 |
| fixture zombie probe | C | 10/10 | 0.2 | 40 (4 per run) | 0 |

- **B:** 30 of 30 go-test runs passed, 0 orphans in any unit. B against C median: kogen-shaping -0.8 percent, kogen-verification +0.0 percent, kogen-loop -1.5 percent; pooled go-test wall time -2.2 percent. B still stopped all four detached servers in every fixture run; C leaves them (40 alive over 10 runs).
- **A:** failed the go-test check of kogen-shaping and kogen-loop in all 20 runs, every one at the 10 minute timeout (shaping: `TestKillGroupOnExit`; loop: `TestCallerShellBoundCustody`, `TestDeadlineTerminatesARunningShellGroup` and related kill-group tests). kogen-verification main has no test that kills a group and waits for it, so A passes there 10 of 10. The zombie probe failed 10 of 10 under A.
- **kogen-loop is not changed:** its tests that failed under A passed under B with kogen-loop 268327e7 unchanged, so on these runs the helper change alone was enough; no loop-side liveness change was needed.
- **Set aside:** one run (kogen-loop, A, repetition 3) overlapped a short-lived process of the host's maintenance and was repeated; no run was kept despite an overlap.
- **Data:** `results/lm/{dry,measured}/*/result.json` with `output-excerpt.txt` where kept; `results/summary-lm.md` and `results/lm/summary.json` are the summary script's output.

## Verdict
**Yes.** B meets its half of the rule: 30 of 30, within 10 percent of C on every repository, 0 orphans. The registered A clause "fails at least 80 percent of the 30 go-test runs" cannot be reached on this tree set: kogen-verification main has no kill-and-wait test, so A fails at most 20 of 30 (67 percent), and it did fail 20 of 20. Read over the 20 runs of the two repositories that have such a test, A failed 100 percent. The deviation is recorded here: (1) the A clause is read over those 20 runs, with the 10 kogen-verification A runs reported separately; (2) one host (lm) with 10 repetitions replaced two hosts with 5, because the second host was not available. The mechanism and the fix agree with the interim run.

## Rerun
Run everything on a Linux host as an unprivileged user with go1.27.2, node, perl and python3. Use the d98cfe01 release `kogen` binary (or one built from kogen-verification 3cb7305a that links `verify`) as A.
1. Clone kogen-shaping at 3696dba, kogen-verification at 6ffb2d1a and kogen-loop at 268327e7 into `src/`, and kogen-verification twice more at 3cb7305a as `src/kv-a` and `src/kv-b`.
2. In `src/kv-b/verify/sweep_linux.go`, make the arm B change described above; copy `harness/helperb/main.go` to `src/kv-b/c1cmd/kogenb/main.go` and build it as `kogen-b`. Copy `harness/xv1/zz_c1xv1_test.go.txt` to `verify/zz_c1xv1_test.go` in both kv-a and kv-b.
3. Build `harness/fixture/golaunch` (output `golaunch`) and `harness/xv1/gol` (output `launch`).
4. Write a config JSON with `host`, `src`, `work`, `gobin`, `nodebin`, `gocache`, `tmp`, `helper_a` and `helper_b`, as read by `harness/run.py`.
5. Run `harness/setup-dry.sh`, then `harness/launch-measured.sh`; `harness/driver-confirm.sh` waits while another build runs on the host and sets a run aside as intruded if one appears during it.
6. `python3 harness/summarize.py <runs dir>` (see the interim finding) prints the table above from the `result.json` files.
