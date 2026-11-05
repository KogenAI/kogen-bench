# Lab C1: the Linux acceptance-reaper helper leaves zombies while a check runs

Finding id: `lab-c1-linux-reaper-zombies-20261105`. Comparison: kogen-verification. Model-free: no model call, no seat tokens.
Verdict: **unresolved (interim, one host, one repetition)**. The mechanism reproduced exactly, and continuous reaping removed it in every run. But the registered rule needs 30 of 30 B runs on two hosts. Only lm ran, and only part of one repetition, because delivery Builds took the host. EU never became quiet.

## Question
Since kogen-verification [fb288e6](https://github.com/KogenAI/kogen-verification/commit/fb288e6ce4edbbcaf6426ca7f8e8d6de9cf76e47) (in Kogen releases 41d70052 and d98cfe01, which pins kogen-verification [3cb7305a](https://github.com/KogenAI/kogen-verification/tree/3cb7305a56907d7105cd20cf51de6767f488fbf6)), every Linux check runs as `exec <kogen> --kogen-verification-acceptance-reaper '<check>'`. The helper in `verify/sweep_linux.go` makes itself a child subreaper and waits only for its shell. It reaps adopted orphans only after the shell exits. Any grandchild whose parent dies while the check runs therefore stays a zombie, and `kill(pid, 0)` still succeeds on a zombie. A test that kills a process group and waits for its members to disappear hangs until go test's 10-minute timeout.

Does a helper that reaps continuously while the shell runs remove the hang and still leave no orphan?

## Arms
- **A**: the released helper: the d98cfe01 release `kogen` binary (go1.27.2, kogen-verification 3cb7305a), unchanged.
- **B**: kogen-verification 3cb7305a with one change in `runAcceptanceReaper`. Instead of `proc.Wait()` on the shell, the helper loops on a blocking `wait4(-1, &status, 0)`. It reaps every child as it exits (the shell or any adopted orphan) and returns when the reaped pid is the shell's, keeping the shell's own wait status. Exit 128+n for signal n, as today. `stopAdoptedChildren()` then runs after the shell exits, exactly as today. No process is signalled during the loop, so the pid-recycling argument of `stopAdoptedChildren` is unchanged. The helper binary is `harness/helperb/main.go` (a main package that only links `verify`), built inside a scratch clone of 3cb7305a with the change applied.
- **C**: no helper: `/bin/sh -c '<check>'`.

## Workload and metric
- **go-test check:** each repo's go-test check from `.kogen/project.yaml`, run literally. The trees are frozen: kogen-shaping [3696dba](https://github.com/KogenAI/kogen-shaping/tree/3696dba67f13c16aae5978c943d9a6ec844c5b63), kogen-verification main [6ffb2d1a](https://github.com/KogenAI/kogen-verification/tree/6ffb2d1a24a4dd07a6ad4e65a88269845fecffbd) and kogen-loop main [268327e7](https://github.com/KogenAI/kogen-loop/tree/268327e7f9503310dd9834f17f283effa17a2c09). Each run uses go1.27.2 with `GOTOOLCHAIN=local`, its own warm build cache, and `go clean -testcache` first. Each check runs in its own session as the `lanes` user.
- **sweep:** kogen-verification's 15 orphan-sweep tests (`-run 'Sweep|Orphan|Detached|Acceptance|Reap|ClimbLauncher' ./verify/`), run on the helper's own source. The run includes delivery experiment R-20261103-X-V1's `TestClimbLauncher`, which starts servers through python, node, perl, go and ruby launchers via `RunAcceptance` (environment cleared, new session, launcher exits). It is copied unchanged except for its survivor cleanup, which uses a checked process-group kill instead of `pkill`: `harness/xv1/zz_c1xv1_test.go.txt`.
- **fixture:** a check that starts four detached servers (node, perl, go, python; environment cleared, new session, descriptors closed, launcher exits) and then runs a kill-group zombie probe (`harness/fixture/`). The probe kills a group, then polls `kill(pid, 0)` on its orphaned member for up to 5 s.
- **Metric:** pass or fail (exit status and go test FAIL or timeout lines), wall seconds, and orphans. An orphan is a process that carries the run's environment marker, or a pid the fixture recorded, and is still present 1.5 s after the check returns.
- **Registered n:** 3 repos × 2 hosts × 5 repetitions × 3 arms = 90 go-test runs.
- **Registered success rule:** B passes 30 of 30 within 10% of C's duration and leaves 0 orphans, and A fails at least 80%.
- **Hosts:** lm (a 4-core Linux laptop) and kogen-bench-eu (EU). EU replaced eu2, which another Lab held for a timing endpoint.

## Results (lm, measured repetition 1; arms interleaved A, B, C)
| unit | arm | pass | wall s | orphans | notes |
|---|---|---|---|---|---|
| kogen-shaping go-test | A | 0/1 | 605.0 | 0 | `TestKillGroupOnExit` (a process of the killed group is reported alive after Run; exact line in `results/lm/measured/shaping-A-r1/output-excerpt.txt`); `panic: test timed out after 10m0s` in `TestWrongImplementationCaps/the_time_cap_ends_the_check_at_the_run_it_cuts_off` (9m55s), the same two signatures as the failed Builds |
| kogen-shaping go-test | B | 1/1 | 210.5 | 0 | |
| kogen-shaping go-test | C | 1/1 | 217.9 | 0 | |
| kogen-verification go-test | A | 1/1 | 60.6 | 0 | main has no kill-and-wait test that meets the zombie |
| kogen-verification go-test | B | 1/1 | 70.5 | 0 | |
| kogen-verification go-test | C | not run | | | delivery Builds started on lm |
| kogen-loop go-test | A, B, C | not run | | | delivery Builds started on lm |
| sweep (15 tests + X-V1) | A, B, C | 1/1 each (+1 dry each) | 11.5–11.6 | 0 | X-V1: python, node, perl and go servers swept in every arm; ruby not installed |
| fixture | A | 0/1 (+0/1 dry) | 5.2 | 0 | zombie probe failed 2 of 2: the killed member was still in state Z after 5 s; all 4 servers stopped |
| fixture | B | 1/1 (+1/1 dry) | 0.2 | 0 | zombie probe passed 2 of 2 (gone in ≤ 0.05 s); all 4 servers stopped |
| fixture | C | 1/1 (+1/1 dry) | 0.2 | 4 per run | zombie probe passed 2 of 2; all 4 detached servers survive without a helper |

- **go-test totals:** A 1 of 2 passed; B 2 of 2 passed, 0 orphans; C 1 of 1 passed.
- **B vs C duration:** kogen-shaping 210.5 s vs 217.9 s (−3.4%, n = 1).
- **Exit status:** passed through identically in A and B (4 for `exit 4`, 143 for SIGTERM; smoke run, not counted).
- **Data:** per-run data is in `results/lm/{dry,measured}/*/result.json` with `output-excerpt.txt`. `results/summary-lm.md` is the summary script's output.

## Reading
- **Mechanism (A):** reproduced exactly. The released helper turns a killed group member into a zombie that the check itself can still see. kogen-shaping 3696dba then fails at the 10-minute timeout, as the failed Linux Builds did.
- **Fix (B):** continuous reaping removes the zombie, so the probe sees the member gone at once. B ran as fast as no helper (−3.4%) and still stopped every detached server (0 orphans), which C does not do.
- **Not settled:**
  - B ran 2 of the registered 30 go-test runs.
  - kogen-loop was not reached.
  - EU did not run.
  - A failed 1 of 2 go-test runs, not at least 80%. kogen-verification main passes under A, so the hang depends on whether a repo has a test that kills a group and waits for it, not on the helper alone.
- **Next step:** a confirmation with the same harness on a host that delivery leaves alone for about 3 h (lm or EU). Under the rule, no Build request is filed from this interim result.

## Rerun
Run everything on a Linux host as an unprivileged user with go1.27.2, node, perl and python3. Use the release `kogen` binary of d98cfe01 (or any binary built from kogen-verification 3cb7305a that links `verify`) as A.
1. Clone [kogen-shaping](https://github.com/KogenAI/kogen-shaping) at 3696dba, [kogen-verification](https://github.com/KogenAI/kogen-verification) at 6ffb2d1a, and [kogen-loop](https://github.com/KogenAI/kogen-loop) at 268327e7 into `src/`. Clone kogen-verification twice more at 3cb7305a as `src/kv-a` and `src/kv-b`.
2. In `src/kv-b/verify/sweep_linux.go`, make the arm B change described above. Copy `harness/helperb/main.go` to `src/kv-b/c1cmd/kogenb/main.go` and run `go build -o kogen-b ./c1cmd/kogenb` in `src/kv-b`. Copy `harness/xv1/zz_c1xv1_test.go.txt` to `verify/zz_c1xv1_test.go` in both kv-a and kv-b.
3. Build `harness/fixture/golaunch` (output `golaunch`) and `harness/xv1/gol` (output `launch`).
4. Write a config JSON with `host`, `src`, `work`, `gobin`, `nodebin`, `gocache`, `tmp`, `helper_a` and `helper_b`, as read by `harness/run.py`.
5. Run `harness/launch.sh <work> <config> <runs dir>`. It runs setup and warm-compile, then the dry plan, then the measured plan. The plan files list `<arm> <unit> <rep> <tag>` per line, rotating the arm order ABC, BCA, CAB by repetition. `driver.sh` waits while a delivery Build runs on the host and skips units that already have a `result.json`.
6. Run `python3 harness/summarize.py <runs dir>` to print the table above from the `result.json` files.
