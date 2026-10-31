# verification-reuse-replay

A replay of Kogen's recorded build logs, with no model call, to find out how much time its checks (the test, format, compile and acceptance commands run before and after the builder edits) could save if some of them were skipped or reused. Of the six mechanisms looked at, only one has real headroom: reusing a **passing** baseline check when a build restarts on the same starting tree. It could save up to 7,059 s, 30% of the 23,865 s spent on baseline checks in 44 delivery builds, but only if the reuse key includes the toolchain and environment, and the logs record neither. The other five (running checks concurrently, re-running only tests the repair touched, staged scope, fix cadence, and exact reuse inside one build) show no headroom or too little to pursue. Verdict: **unresolved** (descriptive; nothing was changed in Kogen and no change was tested). Finished 31 October 2026.

## What was measured

The input is the command log of 44 distinct Kogen delivery builds from 30 October (49 log files; five copied trees counted once), of which 16 reached at least one verification pass, plus 114 small benchmark cells from 22 to 24 October used only as a control. Every executed command was read from its start and end events: its name, whether it ran before any change (baseline), as setup, as a verification pass, or as a formatter fix, how long it took and whether it exited 0. 2,471 executions were read in total. Nothing was run again.

The row-level data in `data/` is these executions with every identifier replaced by a number: task names became `task-001` to `task-017`, run and starting-tree identifiers became counters (`r001`, `h001`), and the command text was replaced by a 10-character digest, so two runs of the same command still match. Seconds, exit status, check names and timestamps are unchanged.

## Where the time goes

| Kind of command | Executions | Seconds |
| --- | ---: | ---: |
| Baseline (before any change) | 224 | 23,865 |
| Verification | 161 | 15,124 (red passes 9,142; green passes 5,874) |
| Setup (repeated in every pass) | 243 | 1,176 |
| Formatter fix | 50 | 23 |

By check, verification time is: Go tests 6,687 s (15 executions), acceptance 5,669 s (44), cucumber 1,057 s, the other test command 1,321 s, spec 314 s. Baseline time is: test 11,476 s (38), Go tests 9,536 s (29), cucumber 2,232 s, spec 499 s. In the 114 small benchmark cells the whole verification cost is 2.4 ks, about 21 s per cell, so the question only matters for long delivery builds.

## Result per mechanism

Seconds are upper bounds. Several are only estimates because the logs do not record what would be needed to prove two runs equivalent (see the next section).

| Mechanism | What was counted | Upper bound on seconds saved | Risk | Decision |
| --- | --- | --- | --- | --- |
| **Reuse a passing baseline check after a restart** (same starting tree, same check, same task, an earlier run of it passed) | 82 baseline executions | **7,059 s**, 30% of baseline seconds, 47% of verification seconds. Mostly the test command (13 executions, 3,965 s), cucumber (4, 577 s) and Go tests (7, 2,297 s). A looser key (same starting tree and command text only, one count per execution) gives 78 executions and 3,118 s | Real: 3 of 133 groups with the same key have mixed outcomes (one task's test command passed 2 of 9 times at one starting tree and 1 of 5 times at another, from load, timeouts and environment; another task's Go test failed twice and then passed). Reusing a pass would hide an environment-caused failure the baseline exists to catch. Reusing a failure is never allowed | **Headroom is real but only with a full environment key. First candidate to prototype.** |
| **Exact reuse inside one build** (same tree, command and environment) | 0 observed: every build runs its baseline once; verification passes follow builder edits. The only repeats with no logged edit are 18 acceptance re-runs of 2 to 87 s (508 s) | at most 508 s, unproven | low if keyed properly | **No headroom inside one build.** |
| **Run independent checks at the same time** | 42 verification passes; the test and Go test commands already start together, while acceptance, format, compile, then no-home-paths, spec and cucumber run one after another | 1,821 s (12% of verification wall) if every check of every pass ran at once. 32 of 42 passes stop at the first failure, so most of it exists only in green passes | No change of verdict, but load: two database and install tests hit their 60 s limit at machine load 20 or more, so concurrency can create false failures. Whether checks are independent (shared build directories, the packaged binary) is not in the logs | Small and contention-prone. Second priority; needs a load control. |
| **Re-run only tests the repair touched** | 17 re-runs of a check that passed in the previous pass, in non-final or red passes | 703 s (4.6% of verification). The final green pass re-runs 1,492 s that must stay (the gates run on the final candidate) | A wrong selection misses a regression; no map from tests to files exists in the logs | **No headroom for the verifier.** The larger target is the builder's own tests inside a round (19.8 ks, 34% of build wall in an earlier profile), which this replay cannot attribute to trees. |
| **Change how often a full verification pass runs per repair** | Passes per build among the 16 with passes: one pass 5 builds, two 5, three 2, five 3, six 1. 22 passes repeat the previous failing set | The long repeated passes are 913, 618 and 625 s in one task (Go test, each after a builder round) and 2,954 s in another: about 2.2 ks for the first three, which the build notes attribute to the 600 s timeout of one Go package and not to the cadence (not re-derived here). Acceptance repeats take seconds | A faster cadence delays feedback or lets a builder submit unverified work | **No headroom independent of the Go-test timeout.** Close unless that timeout is fixed and Go-test failures remain. |
| **Narrower scope in early passes** | 32 of 42 passes already stop at the first failure and cheap checks run first | Passing checks run inside red passes: 23 executions, 165 s | A scope that skips the final full gates is outside Kogen's rules | **No headroom**; already staged. |

Ranking: baseline reuse across restarts (up to 7.1 ks of about 40 ks of command seconds in these 44 builds, 100 to 1,000 s per eligible restart); then concurrency (up to 1.8 ks, contention risk); everything else shows no headroom for a verifier change.

## What the logs do not record

Exact reuse needs a key of tree, command and environment. The logs hold:

| Field | Status |
| --- | --- |
| Command, check name, kind, start and end time, exit status | Recorded for all 2,471 executions |
| Starting commit of the task repository | Recorded for every build. It identifies the baseline tree only if the working tree was clean, which is **unknown** |
| Tree of each verification pass | Recorded for 9 of 42 delivery passes (on the review event); **unknown** for 33 |
| Temporary verification directory | Present on every verification command (221 directories). **None is used in more than one pass.** Whether its name is derived from the tree was not checked |
| Toolchain versions, dependency lockfile digests, environment, cache state | **Not recorded for any execution** |
| Edits between two passes | Per build only. Builder rounds between passes are logged for the 16 builds that used an external coding tool; the other 28 builds used Kogen's own builder, whose rounds are not logged, so "no builder between passes" is unknown there, not zero |

So the baseline-reuse number is a bound computed on starting commit, command and task only, with the environment unknown.

## Reproduce the numbers

```sh
python3 -I reproduce/verification-reuse-replay/analyze_executions.py reproduce/verification-reuse-replay/data > /tmp/out.txt
echo "=== runs ===" >> /tmp/out.txt
python3 -I reproduce/verification-reuse-replay/analyze_runs.py reproduce/verification-reuse-replay/data >> /tmp/out.txt
diff /tmp/out.txt reproduce/verification-reuse-replay/expected-output.txt
```

Both scripts use only the Python standard library and print every count above (`M2` is baseline reuse, `M4` re-runs of checks that already passed, `M5` repeated failing sets, `M6` passing checks inside red passes). `analyze_executions.py` prints the benchmark-cell control and the verification-directory check; `analyze_runs.py` prints the rest. The two baseline-reuse counts (78 and 82) differ only because the first keys on command text and starting commit, the second on check name, starting commit and task.

## Rerun

The counts rerun from the data files in this directory with the two commands above. The extraction step that produced `data/` reads Kogen's own run logs, which hold task text, commit identifiers and command output and are kept out of this repository; the data files hold only the extracted numbers.

## Limits

- Only 30 October delivery builds. 16 builds with verification passes is a small sample, and one task (129 executions) dominates a large share of the repeats.
- The Kogen build and its vendored loop version behind each run are **not recorded** in the logs, only the task repository's commit. The runs were not tied to one Kogen build.
- These are replay estimates from recorded logs, not a measurement of any change. No prototype of baseline reuse was built or run.
- Long benchmark cells with 3 to 9 minute test commands were not in the copied logs and are not replayed. The landing step, shaping time, queue waits and per-test times are not in this replay.

## Proposed next step (not run)

A verifier-side cache for baseline checks, keyed on the exact starting tree after a clean-status check, command text, toolchain versions, lockfile digests, relevant environment and machine class, with any missing field counted as a miss. It would be judged on at least 20% of restarted-build baseline seconds saved and at least 300 s per hit, with no reused failure, no hit on a changed command, lockfile, toolchain, tree or machine class, and equal verdicts on a 20% audit sample.
