# r62b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of COMPARATOR, NO_PREREG, UNMATCHED_CONDITIONS. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- UNMATCHED_CONDITIONS — Baseline formatting checks failed for two tasks, so the comparison conditions did not match.
- COMPARATOR — The direct controls come from earlier rounds rather than a contemporaneous matched cohort.

## Required reproduction metadata

- Kogen commit: [`945548ba49b95079e3d17bba29d5d391dfd3d3af`](https://github.com/KogenAI/kogen-ex/commit/945548ba49b95079e3d17bba29d5d391dfd3d3af), the round source's pinned build.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **55.7%** (72 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Can Kogen 945548ba match direct agents on held-out Elixir/Phoenix?

Venue: Fixed HELDOUT workers: US elx-02/syn-01/syn-20/syn-31; EU elx-04/syn-06/syn-15/syn-24.

Design: 8 tasks × 3 arms × 3 reps = 72; historical r53/r53b direct controls.

Decision rule: none predeclared beyond Round 58 ITT and fixed design.

Arms: kogen-direct-escalate, kogen-direct-shell, kogen-staged.

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Recomputed 6 October 2026 from the public cell export: kogen-direct-escalate 19/24, kogen-direct-shell 16/24 and kogen-staged 17/24 passes; the measurement record reports 72/72 officially graded. The earlier 62/72 snapshot is stale. Base-wide formatting on elx-02/elx-04 confounds Kogen comparisons; no inferential result is reported.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r62b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-02-ingest-supervision | kogen-bench-us | kogen-direct-escalate | 3 | 3 | 3 | 2 | 1 | 0 |
| elx-02-ingest-supervision | kogen-bench-us | kogen-direct-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| elx-02-ingest-supervision | kogen-bench-us | kogen-staged | 3 | 3 | 3 | 3 | 0 | 0 |
| elx-04-queue-backpressure | kogen-bench-eu | kogen-direct-escalate | 3 | 3 | 3 | 3 | 0 | 0 |
| elx-04-queue-backpressure | kogen-bench-eu | kogen-direct-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| elx-04-queue-backpressure | kogen-bench-eu | kogen-staged | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-01-live-ticket-filters | kogen-bench-us | kogen-direct-escalate | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-01-live-ticket-filters | kogen-bench-us | kogen-direct-shell | 3 | 3 | 3 | 2 | 1 | 0 |
| syn-01-live-ticket-filters | kogen-bench-us | kogen-staged | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-06-migration-ticket-numbers | kogen-bench-eu | kogen-direct-escalate | 3 | 3 | 3 | 2 | 1 | 0 |
| syn-06-migration-ticket-numbers | kogen-bench-eu | kogen-direct-shell | 3 | 3 | 3 | 1 | 2 | 0 |
| syn-06-migration-ticket-numbers | kogen-bench-eu | kogen-staged | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-15-validation-ticket-form | kogen-bench-eu | kogen-direct-escalate | 3 | 3 | 3 | 2 | 1 | 0 |
| syn-15-validation-ticket-form | kogen-bench-eu | kogen-direct-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-15-validation-ticket-form | kogen-bench-eu | kogen-staged | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-20-email-invite-flow | kogen-bench-us | kogen-direct-escalate | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-20-email-invite-flow | kogen-bench-us | kogen-direct-shell | 3 | 3 | 3 | 1 | 2 | 0 |
| syn-20-email-invite-flow | kogen-bench-us | kogen-staged | 3 | 3 | 3 | 0 | 3 | 0 |
| syn-24-csv-import | kogen-bench-eu | kogen-direct-escalate | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-24-csv-import | kogen-bench-eu | kogen-direct-shell | 3 | 3 | 3 | 2 | 1 | 0 |
| syn-24-csv-import | kogen-bench-eu | kogen-staged | 3 | 3 | 3 | 1 | 2 | 0 |
| syn-31-inbound-email-webhook | kogen-bench-us | kogen-direct-escalate | 3 | 3 | 3 | 1 | 2 | 0 |
| syn-31-inbound-email-webhook | kogen-bench-us | kogen-direct-shell | 3 | 3 | 3 | 1 | 2 | 0 |
| syn-31-inbound-email-webhook | kogen-bench-us | kogen-staged | 3 | 3 | 3 | 1 | 2 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r62b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 72 rows (fail 20, pass 52); overall pass rate is 72.2% (52/72) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 72/72 shared cell IDs match; 0/72 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 72/72 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
