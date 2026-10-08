# r55

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DESIGN, ENVIRONMENT, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No public predeclared decision rule was recovered.
- DESIGN — The round files do not establish a testable question or complete comparison protocol.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **52.0%** (30 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 55: Elixir ports of Luna-max-failed Rails tasks

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-port-active-storage-tracking, elx-port-board-publish-unpublish-public-boundary, elx-port-cancelled-account-cleanup, elx-port-erase-account, elx-port-variant-processed-once

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r55.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-port-active-storage-tracking | kogen-bench-eu | lmax | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-port-active-storage-tracking | kogen-bench-eu | sol-high | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| elx-port-board-publish-unpublish-public-boundary | kogen-bench-us | lmax | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| elx-port-board-publish-unpublish-public-boundary | kogen-bench-us | sol-high | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-port-cancelled-account-cleanup | kogen-bench-us | lmax | not re-derivable | 3 | 3 | 2 | 1 | 0 |
| elx-port-cancelled-account-cleanup | kogen-bench-us | sol-high | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-port-erase-account | kogen-bench-us | lmax | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| elx-port-erase-account | kogen-bench-us | sol-high | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-port-variant-processed-once | kogen-bench-eu | lmax | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-port-variant-processed-once | kogen-bench-eu | sol-high | not re-derivable | 3 | 3 | 3 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r55.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 30 rows (fail 8, pass 22); overall pass rate is 73.3% (22/30) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 30/30 shared cell IDs match; 0/30 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 30/30 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
