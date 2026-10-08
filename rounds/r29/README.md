# r29

## Status

**DESCRIPTIVE**

Why not VALID:
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

Data completeness: **45.4%** (75 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 29: router fix-route bug and A/B

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: None. Listed task IDs with no matching tagged delivery: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-ar-archive-book-access, rails-as-variant-processed-once, rails-sec-audit-sweep, rails-sup-legacy-conversions. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r29.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| rails-aj-enqueue-after-commit | studio | review-only | 5 | 5 | 3 | 2 | 0 |
| rails-aj-enqueue-after-commit | studio | route-asrun | 5 | 4 | 4 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | route-fixnoplan | 5 | 4 | 4 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | review-only | 5 | 5 | 0 | 5 | 0 |
| rails-ar-bulk-access-grants | studio | route-asrun | 5 | 5 | 5 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | route-fixnoplan | 5 | 5 | 0 | 5 | 0 |
| rails-hw-scoped-broadcast | studio | review-only | 5 | 5 | 0 | 5 | 0 |
| rails-hw-scoped-broadcast | studio | route-asrun | 5 | 5 | 5 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | route-fixnoplan | 5 | 5 | 0 | 5 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r29-syn13:review-only | 5 | 5 | 5 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r29-syn13:route-asrun | 5 | 5 | 5 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r29-syn13:route-fixnoplan | 5 | 5 | 5 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r29-syn14:review-only | 5 | 5 | 5 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r29-syn14:route-asrun | 5 | 5 | 5 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r29-syn14:route-fixnoplan | 5 | 5 | 5 | 0 | 0 |
