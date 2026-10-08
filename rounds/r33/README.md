# r33

## Status

**DESCRIPTIVE**

Why not VALID:
- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **NO_RESEARCH_QUESTION** — The README says no testable research question is recoverable from the committed public record.
- **EVIDENCE_GAPS** — MEASURED.md and MISSING.md document missing per-cell execution, environment, or timing evidence that prevents full reproduction and audit.
- **VENUE_CONFOUND** — The README states that arms ran on different venues, confounding arm and venue.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **47.5%** (81 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Arms ran on different venues, so arm and venue are confounded. The surviving public record also does not establish a testable research question or complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: The historical comparison was superseded by held-out comparisons; full closure is not independently verified from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 33: hard-list headline (launched 2026-10-02 18:38Z)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r33.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| rails-ft-active-storage-tracking | kogen-bench-us | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-active-storage-tracking | kogen-bench-us | r33sol:bare | 3 | 3 | 1 | 2 | 0 |
| rails-ft-active-storage-tracking | studio | packplan-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-ft-activity-feed-api | kogen-bench-us | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-activity-feed-api | kogen-bench-us | r33sol:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-activity-feed-api | studio | packplan-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | kogen-bench-us | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | kogen-bench-us | r33sol:bare | 3 | 3 | 2 | 1 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | packplan-review-sol | 3 | 2 | 0 | 2 | 0 |
| rails-ft-cancelled-account-cleanup | kogen-bench-us | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-cancelled-account-cleanup | kogen-bench-us | r33sol:bare | 3 | 3 | 3 | 0 | 0 |
| rails-ft-cancelled-account-cleanup | studio | packplan-review-sol | 3 | 2 | 0 | 2 | 0 |
| rails-ft-entropy-sweep | kogen-bench-us | r33lmax:bare | 3 | 3 | 2 | 1 | 0 |
| rails-ft-entropy-sweep | kogen-bench-us | r33sol:bare | 3 | 3 | 3 | 0 | 0 |
| rails-ft-entropy-sweep | studio | packplan-review-sol | 3 | 1 | 0 | 1 | 0 |
| rails-ft-i18n-support | kogen-bench-eu | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-i18n-support | kogen-bench-eu | r33sol:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-i18n-support | studio | packplan-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-ft-mysql-fulltext-search-foundation | kogen-bench-eu | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-mysql-fulltext-search-foundation | kogen-bench-eu | r33sol:bare | 3 | 3 | 3 | 0 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | packplan-review-sol | 3 | 2 | 2 | 0 | 0 |
| rails-ft-notification-bundle-window-overlap | kogen-bench-eu | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-notification-bundle-window-overlap | kogen-bench-eu | r33sol:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-notification-bundle-window-overlap | studio | packplan-review-sol | 3 | 2 | 0 | 2 | 0 |
| rails-ft-saas-billing | kogen-bench-eu | r33lmax:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-saas-billing | kogen-bench-eu | r33sol:bare | 3 | 3 | 0 | 3 | 0 |
| rails-ft-saas-billing | studio | packplan-review-sol | 3 | 3 | 0 | 3 | 0 |
