# Round 70 task 8 v2 smoke lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of NO_OUTCOME, NO_SCORED_RESULTS, SMOKE_GATE. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



## Status

**INCOMPLETE**

- NO_SCORED_RESULTS — The README says scored cells were not run.
- SMOKE_GATE — The v2 smoke did not pass its required admission gate.
- NO_OUTCOME — No scored task-8 comparison exists.

STATUS: **INCOMPLETE** for scored cells.
Analysis: **DESCRIPTIVE**; the two smoke results are not a language comparison.

This is the v2 prompt cohort for Rust and Go only. The separately recorded v1 smoke cohort remains in [task 8](../r70-task8/README.md). No scored v2 cells were released. The two v2 smoke cells both returned 1/25 and failed the predeclared release gate. This is an observed smoke outcome, not a scored task-8 result.

## Cohort accounting

| Lifecycle field | n | Basis |
|---|---:|---|
| Maximum planned v2 executions | 4 | One smoke per stack and at most one follow-up per stack if its smoke passed. |
| Started | 2 | Rust and Go v2 smoke IDs only. |
| Finished smoke executions | 2 | Both returned an official smoke grade. |
| Officially graded smoke cells | 2 | Both are marked not scored in the test-count ledger. |
| Scored cells | 0 | The release gate failed for both stacks; no bulk cells followed. |
| Scored ITT denominator | 0 | No scored cells were released. Smoke outcomes remain outside that denominator. |

| Task ID | Exact arm | Cell ID | Smoke result | Test fraction | Scored |
|---|---|---|---|---:|---|
| r70-8-rust-v2 | rust | `codex__gpt-6-luna__max__default__r70-8-rust-v2__r1` | fail | 1/25 | no |
| r70-8-go-v2 | go | `codex__gpt-6-luna__max__default__r70-8-go-v2__r1` | fail | 1/25 | no |

The v2 admission controls are separate from scored outcomes: one reference passed and one no-op failed for each stack. Exact rows are in the [controls ledger](../../results/controls.jsonl) under cohort `r70-task8-v2`. The public receipts do not include the versioned task-8 prompt or grader version/hash, so the prompt-based diagnosis is not independently checked here.

## Reproduction record

- **Kogen commit:** not applicable; these are direct Codex task builds, not Kogen runs.
- **Harness commit / CLI version:** no exact per-cell harness Git commit or Codex CLI release is recorded for this v2 smoke cohort. The design says the runner and sandbox follow R70; that does not establish an exact per-cell revision.
- **Model and effort:** direct Codex, `gpt-6-luna`, `max`.
- **Task IDs:** `r70-8-rust-v2` and `r70-8-go-v2`.
- **Historical execution command:** not retained in the public record.
- **Reproduce the published outcomes and control counts:** run `python3 rounds/r70-rve-task8v2/reproduce.py` from the repository root. This reads ledger rows and does not launch cells.
- **Raw records:** [test-count ledger](../../results/test-counts.jsonl), cohort `r70-task8-v2-smoke`; [controls ledger](../../results/controls.jsonl), cohort `r70-task8-v2`.

The prompt wording was changed from v1 for the retry-body/cache-key rule. Because v2 never passed the smoke gate, this lane establishes no language or prompt-effect result.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r70-rve-task8v2.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 2 rows (fail 2); overall pass rate is 0.0% (0/2) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 2 missing published metadata). Missing counters remain unknown, not zero.
This round also has 2 raw-only or non-public rows; they are kept separate from the published-export denominator.
