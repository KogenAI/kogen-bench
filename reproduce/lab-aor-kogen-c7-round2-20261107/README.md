# Lab: Kogen with the shaping fix against Claude Code alone on five Rails tasks (round 2, smoke)

**Finding.** In round 1 of this comparison, Claude Code alone (Sonnet 5.5, high effort) finished all 15 cells on five request-only Rails tasks. It reached a mean of 0.83 of the hidden checks it could gain over the start tree, with 1 hidden all-pass. Kogen driving the same Claude Code was refused at shaping on all five tasks and scored the start tree. Round 2 ran Kogen v0.1.0-dev.40efd025 with the shaping changes that got those Rails shapes through in the shaping climb (stages 3 and 4: C6 and C7). The arm now gets past shaping on two of four tasks. Both of those cells built, passed review and landed. On **mysql-fulltext-search-foundation** Kogen passed **16 of 16** hidden checks (gain 1.00; alone 0.85, 1 all-pass in 3). On **webhook-delivery-trust-and-restart** it passed 11 of 12, failing the same single check every alone run fails (gain 0.88 = alone). On **data-export-and-import** and **notification-bundle-window-overlap** Kogen was still refused at shaping and scored the start tree (gain 0 against the alone arm's 0.85 and 0.86). Only 4 of the 10 planned Kogen cells ran, because the subscription seat's 5-hour window ran out of headroom (other jobs share it), and **saas-billing** got no Kogen cell. Over the four tasks with a cell, Kogen's mean gain is **0.47** and the alone arm's is **0.86**, with 1 all-pass each. That is too few cells for the registered 12-pair rule. **Verdict: unresolved** (descriptive). Where Kogen gets past shaping it is as good as or better than Claude Code alone; where it does not, it loses the whole task. One of the two remaining refusals comes from an environment mismatch between the shaper's own session and Kogen's readiness probes.

## Question

With the shaping fix, does Kogen driving Claude Code beat Claude Code alone at the same model and effort on the five Rails tasks of round 1?

## Arms

- **Kogen (round 2, run here):** Kogen release v0.1.0-dev.40efd025 ([`40efd025`](https://github.com/KogenAI/kogen/commit/40efd02571567cba8a069288f8557ef07645146b)), with kogen-shaping replaced by its pin [`0484edf`](https://github.com/KogenAI/kogen-shaping/tree/0484edf817f6dc74f691f44d5234cf7f6ae0435e) plus the shaping climb's changes C6 and C7. These are described in the published findings `lab-shaping-small-requests-20261107` (C6) and `lab-shaping-aor-diagnosis-20261107` (C7). Every other module is the release's. A plain rebuild of the release reproduces the released binary byte for byte, and the candidate's module list differs from it only in the kogen-shaping line. Claude Code 2.1.312 as Kogen manages it, claude-sonnet-5-5 at high effort for shape, build and review. Request only, no answers, full pipeline (shape, approve, build, independent review), 3600 s deadline per cell.
- **Claude Code alone (round 1, stored, not rerun):** one Claude Code 2.1.312 session per cell, claude-sonnet-5-5 at high effort, the same request text plus the task's check command, 3 repetitions per task.
- **Context only:** the Kogen release of round 1 (v0.1.0-dev.36075527), refused at shaping on all five tasks.

Both rounds ran on the same Mac, with the same task kits, the same protected final-tree hidden grader and the same start-tree floors. Round 2 used a newer version of the research harness, because Kogen releases from 47236bbb on read the model lineup from `.kogen/models.yaml`. Its grading code is unchanged.

## Method

Per cell, gain = (checks passed - start-tree floor) / (checks expected - start-tree floor) on the protected final tree (floors: billing 4/11, export 3/16, webhook 4/12, mysql 3/16, notification 3/10). A cell refused before building keeps the start tree and scores 0. The first Kogen cell was a dry run, watched until shaping was running with model output and no setup refusal. It was registered in advance to count if valid, and it did. Cells were admitted one at a time against the seat's 5-hour pace line, with at most 2 live; tasks were ordered so that a time stop still leaves one repetition per task. Cost is Claude Code's own list-equivalent figure.

## Result

| task | Kogen cells | Kogen gain | Kogen all-pass | alone cells | alone mean gain | alone all-pass | Kogen - alone |
|---|---|---|---|---|---|---|---|
| data-export-and-import | 1 | 0.00 | 0 of 1 | 3 | 0.85 | 0 of 3 | -0.85 |
| mysql-fulltext-search-foundation | 1 | 1.00 | 1 of 1 | 3 | 0.85 | 1 of 3 | +0.15 |
| notification-bundle-window-overlap | 1 | 0.00 | 0 of 1 | 3 | 0.86 | 0 of 3 | -0.86 |
| saas-billing | 0 | n/a | n/a | 3 | 0.71 | 0 of 3 | n/a |
| webhook-delivery-trust-and-restart | 1 | 0.88 | 0 of 1 | 3 | 0.88 | 0 of 3 | +0.00 |

- **Kogen cells:** 2 landed (shape ready at the first submission, the wrong-implementation check ran all 8 of its runs, build green at the second verification pass, review approved with 0 blocking findings), 2 refused at shaping after 3 submissions. The round-1 Kogen release: 0 of 5 got past shaping.
- **Requested hidden checks** (climb metric, `metrics.json`): Kogen 21 of 42 (mean fraction 0.47), Claude Code alone 126 of 150 (0.84), round-1 Kogen 3 of 50 (0.07).
- **Time and cost:** Kogen median wall 1435 s per cell, 13.98 USD for 4 cells. Alone median wall 260 s, 24.62 USD for 15 cells. Kogen times include the refused cells (1170 s and 1577 s).

**Why the two refused cells were refused (by component):**
- *data-export-and-import:* attempt 1, the decision check (2 lines: a Decisions line the request does not support). Attempts 2 and 3, readiness (1 line each): a support probe's recorded output did not match Kogen's run of the same command. The task's test reporter prints "N runs" or "N tests" depending on an environment variable. The shaper's own session inherits the variable from the environment Kogen was started in, while Kogen's readiness probes run with an allowlisted environment that drops it ([`verify/probe.go`](https://github.com/KogenAI/kogen-verification/blob/e1ff81b79447b6c7d43526db332d528a3820b93b/verify/probe.go), `probeEnv`). **Component: verification** (probe environment), with shaping not told about the difference. The variable was set by the research harness, but any variable in a user's shell does the same.
- *notification-bundle-window-overlap:* attempt 1, the contract review (4 lines). Each fresh-copy run of the app's test command failed while loading gems: an environment preload of the research harness activated a newer version of a native-extension gem than the task's lockfile pins. **Component: setup** (the benchmark environment, not Kogen). Attempt 2, the decision check (4 lines). Attempt 3, the contract review (3 lines): wrong implementations in the shaper's `controls.json` also broke scenarios of other properties. **Component: shaping** (the shaper's controls not isolated).
- The same preload made Kogen's static test check report a pre-existing failure in every cell, and one Kogen build added a workaround for it that the reviewer flagged as outside the Intent. Round 1's alone arm ran under the same environment, and the grader is unaffected.

## Limits

Only 4 of 10 planned Kogen cells ran, one per task on four tasks, and none on saas-billing. A single cell per task cannot separate Kogen's rate from the 18-27% chance that a rerun flips a result, so the per-task differences are observations, not estimates. The alone arm is round 1's stored cells, run one day earlier on the older harness version, with the same grader and environment. The Kogen arm is a research build (release plus shaping changes), not a shipped release. The refused export cell depends partly on a harness environment variable, and the notification cell's first refusal on a harness environment defect. Both are reported as they happened, not voided, because the cells ran to completion under the same environment the baseline had.

## Rerun

```sh
cd reproduce/lab-aor-kogen-c7-round2-20261107 && python3 report.py | diff - expected-output.txt
```

`report.py` uses only the standard library and rebuilds every number above from `data/cells.tsv` (one row per cell: arm, round, task, repetition, outcome, checks passed and expected, floor, gain, all-pass, requested checks, wall, cost, stages, times; no hidden test names). `metrics.json` holds the climb metric per arm. To run cells again you need Kogen 40efd025 rebuilt with kogen-shaping 0484edf plus the C6 and C7 changes (as published with the shaping climb findings), Claude Code 2.1.312, the five Agents-on-Rails task kits and their hidden graders (private), and a Claude subscription seat.
