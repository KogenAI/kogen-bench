# Round 70 fixed-skeleton rerun

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of SENSITIVITY_ONLY, SEPARATE_COHORTS, UNMATCHED_CONDITIONS. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- SENSITIVITY_ONLY — The README describes this as a sensitivity check, not a standalone preregistered comparison.
- UNMATCHED_CONDITIONS — The rerun changes stdout encoding and front-end handling relative to the original cohort.
- SEPARATE_COHORTS — Original and rerun cells are explicitly separate cohorts.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs: r70-1-elixir-fe2, r70-4-elixir-fe2, r70-4-go-fe2, r70-4-rust-fe2, r70-4-ts-bun-fe2; the complete scored-cell mapping is not recorded where noted above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness (standard run-record capture): **N/A** (0 deliveries; NO DELIVERED DATA). Supplemental evidence: 15 official grades; 36 control receipts. [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).




Pre-registered: yes; descriptive sensitivity check.
Label: DESCRIPTIVE
Question: Are the task-1 Elixir results sensitive to fixed stdout encoding and task-4 results sensitive to fixed front-end handling?
n: 15 official rerun grades: three for task-1 Elixir and three for each task-4 stack.
Headline: The FE2 rerun recorded 11/15 full passes across the planned cells.
Evidence note: The public test-count and control ledgers identify the scored cells, admission controls, and X-controls. Task-4 fixed-front-end controls did not pass for Rust, Elixir, and TypeScript/Bun; the reported counts are descriptive.

Design: 40 original RvE cells and 15 pre-registered FE2 rerun cells (task 1 Elixir; task 4 all four stacks); the outcomes are reported as separate cohorts.

Configuration: direct Codex, gpt-6-luna at max; n=3 for each rerun variant. Task-1 Elixir and task-4 Rust/Elixir ran on kogen-bench-eu; task-4 Go/TypeScript-Bun ran on kogen-bench-us. Wall comparisons are within-host only. The supplemental rows do not include a verified per-cell harness version.
Original cohort context: [40-cell as-graded RvE comparison](../r70/README.md#original-40-cell-rve-language-comparison).

Limit: Task-4 admission controls failed for Rust, Elixir, and TypeScript/Bun, preventing causal front-end or stack conclusions.

Sources: [decision rule](DECISION-RULE.md); [rerun outcomes](RESULTS.md); [test-count ledger](../../results/test-counts.jsonl); [cost/time ledger](../../results/cost-time.jsonl); [controls ledger](../../results/controls.jsonl); [frozen plan](PLAN.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r70-rve-rerun.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 30 rows (fail 8, invalid 6, pass 16); overall pass rate is 66.7% (16/24) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 20 field mismatches across 5 cell IDs (`official_grade.classification` 5, `official_grade.outcome` 5, `official_grade.pass_fail` 5, `official_grade.test_counts.tests_passed` 5). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `codex__gpt-6-luna__max__default__r70-1-elixir-fe2__r6` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-1-elixir-fe2__r6` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-1-elixir-fe2__r6` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-1-elixir-fe2__r6` field `official_grade.test_counts.tests_passed`: kept `25`, recovered `1`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r10` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r10` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r10` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r10` field `official_grade.test_counts.tests_passed`: kept `18`, recovered `0`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r13` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r13` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r13` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r13` field `official_grade.test_counts.tests_passed`: kept `18`, recovered `0`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r9` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r9` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r9` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r9` field `official_grade.test_counts.tests_passed`: kept `18`, recovered `0`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r919` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r919` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r919` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-4-go-fe2__r919` field `official_grade.test_counts.tests_passed`: kept `18`, recovered `0`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 30 missing published metadata). Missing counters remain unknown, not zero.
This round also has 30 raw-only or non-public rows; they are kept separate from the published-export denominator.
