# r30

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

Data completeness: **45.5%** (110 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 30: uniform harness, no router: Luna context pack + one-turn plan + scoped review, on every task. Two model arms: Sol high (`packplan-review-sol`) and Luna max (`packplan-review-lmax`). Studio: 8 Rails tasks × 5 reps; workers: 5 Elixir/syn tasks × 3 reps.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r30.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-05-cache-single-flight | kogen-bench-us | r30-elx05:packplan-review-lmax | 3 | 3 | 3 | 0 | 0 |
| elx-05-cache-single-flight | kogen-bench-us | r30-elx05:packplan-review-sol | 3 | 3 | 3 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-us | r30-elx07:packplan-review-lmax | 3 | 3 | 0 | 3 | 0 |
| elx-07-cli-stats | kogen-bench-us | r30-elx07:packplan-review-sol | 3 | 3 | 2 | 1 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | r30-elx12:packplan-review-lmax | 3 | 3 | 1 | 2 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | r30-elx12:packplan-review-sol | 3 | 3 | 3 | 0 | 0 |
| rails-ac-throttle-search | studio | packplan-review-lmax | 5 | 5 | 5 | 0 | 0 |
| rails-ac-throttle-search | studio | packplan-review-sol | 5 | 5 | 3 | 1 | 1 |
| rails-aj-enqueue-after-commit | studio | packplan-review-lmax | 5 | 5 | 5 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | packplan-review-sol | 5 | 5 | 5 | 0 | 0 |
| rails-ar-archive-book-access | studio | packplan-review-lmax | 5 | 4 | 4 | 0 | 0 |
| rails-ar-archive-book-access | studio | packplan-review-sol | 5 | 5 | 5 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | packplan-review-lmax | 5 | 5 | 4 | 1 | 0 |
| rails-ar-bulk-access-grants | studio | packplan-review-sol | 5 | 5 | 5 | 0 | 0 |
| rails-as-variant-processed-once | studio | packplan-review-lmax | 5 | 5 | 0 | 5 | 0 |
| rails-as-variant-processed-once | studio | packplan-review-sol | 5 | 5 | 1 | 4 | 0 |
| rails-hw-scoped-broadcast | studio | packplan-review-lmax | 5 | 5 | 4 | 1 | 0 |
| rails-hw-scoped-broadcast | studio | packplan-review-sol | 5 | 5 | 4 | 1 | 0 |
| rails-sec-audit-sweep | studio | packplan-review-lmax | 5 | 5 | 5 | 0 | 0 |
| rails-sec-audit-sweep | studio | packplan-review-sol | 5 | 5 | 5 | 0 | 0 |
| rails-sup-legacy-conversions | studio | packplan-review-lmax | 5 | 5 | 4 | 1 | 0 |
| rails-sup-legacy-conversions | studio | packplan-review-sol | 5 | 5 | 5 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r30-syn13:packplan-review-lmax | 3 | 3 | 3 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r30-syn13:packplan-review-sol | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r30-syn14:packplan-review-lmax | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r30-syn14:packplan-review-sol | 3 | 3 | 3 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r30.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 109 rows (fail 20, grader_error 1, pass 88); overall pass rate is 81.5% (88/108) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 109/109 shared cell IDs match; 0/109 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 108/108 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
