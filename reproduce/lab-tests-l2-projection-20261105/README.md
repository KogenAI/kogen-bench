# A behaviour projection leaves every recorded false red of the budget-off test outside it: 10 of 10 recorded differing keys are timing, load or probe values

Finding `lab-tests-l2-projection-20261105`. A model-free Lab (no model call, no seat, 5 Nov 2026), step 0 of Lab L2 of the K-TESTS-ACCEPTANCE-FIRST request. The Studio record `lab-tests-l2-projection-20261105` was registered before the measurement and holds the fixed rule.

## Question

Kogen-build's `TestBuildRequestBudgetOff` runs two Builds and deep-compares their whole `log.jsonl` after masking a deny-list of volatile keys. It went red in 14 delivery land windows over 9 producer changes, and the list grew after each break. The request proposes to compare a behaviour projection instead: exit code, stop code and outcome, git commit facts, the number of builder and review requests, the `build.qnt` phase and reason trace, and the absence of any `budget` key in events, checkpoint and result. Step 0 asks, with no run: in the recorded red windows, is every key that differed outside that projection?

## Method

- Windows: every recorded land log that names the test or its source file, plus every row of the classified land-red table whose failing test names it. 13 of the 14 reported windows could be identified.
- The differing key comes from the `omitted:`/`zero:` diff lines where a log keeps them (3 windows), otherwise from the cause recorded in the classified table (7 windows). A window whose log keeps only `log line N differs at byte B` and no cause (3 windows) has no recorded key and is not counted.
- Rule fixed before measuring: a key is inside the projection only if it is exit/outcome/stop-code/reason/phase, a git commit fact, a count of request events, or contains `budget`. Pass (`yes`): at least 8 of the 14 windows have a recorded key, every recorded key is outside the projection, and the planted mutation key `build_request_budget` is inside it. `no`: any recorded key inside. `unresolved`: fewer than 8 recorded.

## Result

| Quantity | Value |
|---|---|
| Windows reported / identified | 14 / 13 |
| Windows with a recorded differing key | 10 |
| Recorded keys inside the projection | 0 |
| `request_offset_ms` (loop request timing) | 2 windows |
| `load_average` (host load in a log line) | 3 windows |
| step-sweep `ms` (duration) | 1 window |
| toolchain-probe `status` (`timed_out` vs `ok` under load) | 4 windows |
| Windows with no recorded key | 3 |
| Control keys `build_request_budget`, `outcome`, `commits` | inside the projection |

`data/l2.tsv` has one row per window: producer, producer main, key, where the key was read from, the two values where the log shows them, and the projection decision.

The Quint part of the projection could not have gone red for these either: `build.qnt` has no variable for toolchain probes, sweeps, timing or host load (its only `budget` text is the stop reason `context_budget_exceeded`). The deny-list of kogen-build 956b151 already masks `ms`, `_ms` and `load_average`; only the probe `status` is still unmasked today, which is the 4 of 10 that would still be red.

## Verdict

**Yes, for step 0.** Every recorded differing key falls outside the projection, so the projection would not have gone red for any of those windows, and the planted budget key is inside it. A parser pattern for the cause text "mix-probe flake" was added after the first run (9 recorded keys, same verdict); the rule was not changed.

## Limits

- 7 of the 10 keys come from a reader's classification of the log, not from the diff lines. 3 windows have no recorded key.
- This does not show that the projection still catches real defects: that needs the mutation arm of step 1. It also does not show that the projection's request counts and phase trace are stable under load.
- The Quint trace of the projection was not run here (see the L5 finding for the replay's own measurement).

## Step 1

Lab C6's design (34 trees, 2 arms, 2 load levels, 3 repetitions, one planted mutation, 396 probes) is the step 1. It was built and not yet measured because no quiet Linux host was free in its window. It needs 2 to 3 hours on one quiet 4-core Linux host.

## Rerun

Offline, from the published data, with no model call and no checkout:

```
python3 -I report.py data
```

It recounts the table from `data/l2.json`, prints the verdict and checks every count against `replay.json`. `extract/l2_project.py <land log dir> <classified table> <out dir>` is the extraction that produced `data/` from the delivery land logs and the classified land-red table; those two inputs hold internal run names, so the pack ships their extract in `data/` instead. Sources are public: https://github.com/KogenAI/kogen-build/blob/956b151/build/build_request_budget_test.go and https://github.com/KogenAI/kogen/blob/24136fc/spec/quint/build.qnt.
