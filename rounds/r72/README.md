# R72 same-model ladder comparison


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG_EVIDENCE — The README says registration is not established in the public record.
- INCOMPLETE_EXECUTION — The round stopped early and the complete planned/start/cancelled partition is absent.
- CROSSWALK — Recovered counts are not independently joined to the canonical official outcome export.

## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H113 (the R72 headline claim), H136 (ladder variants), and H138 (matched model/effort baselines).

Date: 5–6 October 2026 (source-reported).

Question: How did the stopped Kogen ladder compare descriptively with direct Codex at the same builder model on the dispatched cells?

Design: **Source-reported design/status, not reproducible from public data.** A planned same-model comparison was amended during execution and stopped early. The research summary describes an initial 456-cell specification. The surviving summary distinguishes P1, P2, and P3; the task-level manifest and complete planned/start/cancelled partition are not present in the public record.

The published L0 reconciliation CSVs and [`reproduce/reconcile_l0.py`](../../reproduce/reconcile_l0.py) reproduce the recovered P1 tallies: Kogen Luna ladder 64/84 versus direct Codex Luna max 60/84. They also reproduce partial P3: mixed Kogen ladder 12/13 versus direct Codex Sol high 10/11. These CSV rows do not match the canonical public official outcome export. P2 had no scored cells. The initial 456-cell plan and complete start/finish/ITT partition remain source-reported or unrecovered. R72 is descriptive only; do not infer superiority, pool it with R74, or treat the superseded Kogen revision as a current-version result. See [L0 reconciliation inputs and results](../l0-reconcile/README.md).

## Lifecycle counts

The published L0 CSV reproduces the recovered P1 and partial P3 counts above. Initial planned specifications = 456 (source-reported); exact started and finished totals are not reconciled. Recovered official-grade counts are P1 Kogen 84 and Codex 84; P3 Kogen 13 and Codex 11; P2 scored = 0. These historical rows are not independently joined to the canonical public outcome export. Exact overall ITT denominator and disposition partition remain unrecovered. Phase counts must remain separate.

## Reproduction

- Exact Kogen commit: Kogen pin `260a73bc` resolves to [`260a73bc06be16e563cb4e56a168ffd078cec677`](https://github.com/KogenAI/kogen-ex/commit/260a73bc06be16e563cb4e56a168ffd078cec677). The separate Codex CLI source or binary revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: P1 Kogen ladder roles are reported as Luna max with no observed fallback; direct comparator is Codex Luna max. P3 is a mixed Kogen ladder versus direct Codex Sol high. The P1 role/fallback detail is a source summary, not an independently joined request receipt.
- Task IDs: The published L0 CSVs identify exact task and cell IDs for the recovered P1 and partial P3 subsets; complete plan membership and P3 task coverage are not recovered.
- Exact command: The exact dispatch command and model request configuration are not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Worker result roots are identified in the source inventory on kogen-bench-us and kogen-bench-eu. Their folder paths, cell manifests, and joined official-grade rows are not included in this repository.
- Reproduce the available reconciliation: run `python3 reproduce/reconcile_l0.py` from the repository root. It reads the seven sanitized CSV inputs listed in [L0's reproduction notes](../l0-reconcile/README.md) and prints the recovered R72 tallies. This is an analysis replay of published reconciliation data, not a replay of the model executions or an independent join to the canonical official outcome export.
- Full execution replay: not available; the exact amended plan, complete attempts, model/fallback receipts, and launch command from both worker roots are absent.

## Limits

The comparison stopped early and used a superseded Kogen revision. The reported P1 advantage is descriptive and statistically unresolved in the source analysis; P3 has incomplete coverage. Initial design size, dispatched cells, and the final ITT partition must remain separate.

No measured superiority claim is made from this page. The recovered P1 and P3 counts are reproducible from the L0 CSVs but are not independently joined to the canonical public official outcome export; the original plan and complete lifecycle remain source-reported or unrecovered.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `r72`; that export does not establish that no historical run occurred.
