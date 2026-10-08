# r48

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE; the available public record does not support upgrading that classification.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **NO_RESEARCH_QUESTION** — The README says no testable research question is recoverable from the committed public record.
- **EVIDENCE_GAPS** — MEASURED.md and MISSING.md document missing per-cell execution, environment, or timing evidence that prevents full reproduction and audit.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **44.7%** (66 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 48: contract-gated cascade.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r48.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-05-cache-single-flight | kogen-bench-us | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-us | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ac-throttle-search | studio | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | cascade-contract | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| rails-ar-archive-book-access | studio | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-as-variant-processed-once | studio | cascade-contract | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-ft-active-storage-tracking | studio | cascade-contract | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-activity-feed-api | studio | cascade-contract | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | cascade-contract | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-cancelled-account-cleanup | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-ft-entropy-sweep | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-ft-i18n-support | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | cascade-contract | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-notification-bundle-window-overlap | studio | cascade-contract | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-saas-billing | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-hw-scoped-broadcast | studio | cascade-contract | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| rails-sec-audit-sweep | studio | cascade-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| rails-sup-legacy-conversions | studio | cascade-contract | not re-derivable | 3 | 3 | 2 | 1 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | cascade-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r48.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 60 rows (fail 36, pass 24); overall pass rate is 40.0% (24/60) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 60/60 shared cell IDs match; 0/60 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 60/60 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
