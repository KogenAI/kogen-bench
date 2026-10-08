# r61

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of CROSSWALK, NO_PREREG, OUTCOME_CLASSIFICATION. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- OUTCOME_CLASSIFICATION — Official cells and captured run records disagree on graded, unresolved, and smoke classifications.
- CROSSWALK — A matching cell-level reconciliation is not retained.

## Required reproduction metadata

- Kogen commit: [`945548ba49b95079e3d17bba29d5d391dfd3d3af`](https://github.com/KogenAI/kogen-ex/commit/945548ba49b95079e3d17bba29d5d391dfd3d3af), the round source's pinned build.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **52.5%** (34 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The official cells export and captured run-record export disagree on graded, unresolved, and smoke classifications; the former aggregate and table are withheld.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 61 pre-fill: Codex baselines

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r61.jsonl](../../results/run-records/r61.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r61.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 34 rows (fail 18, pass 16); overall pass rate is 47.1% (16/34) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 34/34 shared cell IDs match; 0/20 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 34/34 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
