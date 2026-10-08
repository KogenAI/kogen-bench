# r67b


## Status

**INVALID**

Why not VALID:
- NO_PREREG — No public predeclared decision rule was recovered.
- CROSSWALK — Official outcomes cannot be matched to the prior Kogen arm rows.
- INCOMPLETE_CAPTURE — The refreshed public record includes ungraded or unknown deliveries and does not restore the planned arm comparison.

## Required reproduction metadata

- Kogen commit: [`6e826320bb4874a994d2a799b3d737f9b5400851`](https://github.com/KogenAI/kogen-ex/commit/6e826320bb4874a994d2a799b3d737f9b5400851), the round source's pinned build.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (cited Round 67b launch receipt): `elx-07-cli-stats`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, `elx-12-retry-api-deprecation`, and `elx-04-queue-backpressure`. The public delivery task mapping remains unresolved.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **51.9%** (55 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior Kogen arm rows; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 67b: T54/T60 Kogen rerun

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: elx-07-cli-stats

Task reconciliation: The surviving plan lists elx-07-cli-stats. Task IDs in the public run-record export but not in that list: elx-02-ingest-supervision, elx-04-queue-backpressure, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account. Listed task IDs with no matching tagged delivery: None. One captured delivery has no task ID in the public record. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Outcome interpretation remains **INTERIM** because task and arm assignments are not fully reconciled, and no public predeclared decision rule was recovered. Exact official grade verification resolves the export gap but does not supply an analysis rule or an unambiguous intended assignment. No benchmark comparison is reported.

## Refreshed official grades

The 2026-10-07 refresh adds 42 r67b official-grade rows recorded after the original public snapshot cut (`2026-10-05T11:08:31Z`). Before refresh, the public export had one row, an invalid `control_apply` control. The additions contain 25 model rows (17 PASS, 8 FAIL) and 17 invalid controls. The refreshed export has 43 exact-joined official rows: 25 model rows (17 PASS, 8 FAIL) and 18 invalid `control_apply` rows, including the pre-existing control. The controls have `result=invalid` and source `outcome=fail`; they are controls, not model failures. The refreshed [cells export](../../results/cells.jsonl) represents them as invalid.

The previous `cells.*` export displayed the pre-existing control as `outcome=fail`; the refreshed export uses its official `result=invalid` classification. The before/after table separates controls from model outcomes by source `kind` and `result`.

| Count | Before refresh | Added | Refreshed export |
|---|---:|---:|---:|
| Official rows | 1 | 42 | 43 |
| Model PASS | 0 | 17 | 17 |
| Model FAIL | 0 | 8 | 8 |
| Invalid `control_apply` rows | 1 | 17 | 18 |

The refresh changes the public row count and verifies the official results. It does not change the verdict: the public record still lacks a predeclared decision rule and fully reconciled task/arm assignments.

## Public outcome reconciliation status
The prior outcome table remains removed because the task and arm assignments are not fully reconciled to the surviving round record. The refresh exact-joins all 43 captured grade-flag rows, but official outcomes do not establish intended reassignment or provide a recovered decision rule. No combined result is reported.


Refreshed export for this tag: 55 captured deliveries; 43 exact-joined official rows (25 model rows: 17 PASS, 8 FAIL; 18 invalid controls); 12 ungraded/unknown capture rows. Control rows are not model failures.
