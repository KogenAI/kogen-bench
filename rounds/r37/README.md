# r37

## Status

**INVALID**

Why not VALID:
- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **OUTCOME_CROSSWALK** — The README marks this round INVALID and its README does not establish a complete, preregistered comparison protocol.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **40.7%** (84 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: On elx-07-cli-stats, the r37 contract-review arm recorded 0/5 passes; see the [public delivery and outcome table](#public-delivery-and-outcome-reconciliation). This is an observed outcome only. The stated contract-validation defect behind INVALID is source-reported and not independently verified: no public validation receipt or reproducible diagnostic identifies it. [r37c](../r37c/README.md) is a separate follow-up with 4/5 passes; no public validation receipt links those results to a correction.



Pre-registered: no


Status: invalid, for a source-reported contract-validation defect that is not independently verified. [r37c](../r37c/README.md) is a separate follow-up attempt; it remains INTERIM because no public validation receipt is linked.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 37: contract tests + plan debate.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-07-cli-stats, rails-ac-throttle-search, rails-as-variant-processed-once, rails-ft-cancelled-account-cleanup, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast, syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists elx-07-cli-stats, rails-ac-throttle-search, rails-as-variant-processed-once, rails-ft-cancelled-account-cleanup, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast, syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-sup-legacy-conversions. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r37.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-07-cli-stats | kogen-bench-us | r37-elx07:contract-review-sol | 5 | 5 | 0 | 5 | 0 |
| elx-07-cli-stats | kogen-bench-us | r37-elx07:debate-packplan-review | 5 | 5 | 2 | 3 | 0 |
| rails-ac-throttle-search | studio | contract-review-sol | 5 | 1 | 1 | 0 | 0 |
| rails-ac-throttle-search | studio | debate-packplan-review | 5 | 5 | 2 | 2 | 1 |
| rails-aj-enqueue-after-commit | kogen-bench-us | r37reg-aj:contract-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-aj-enqueue-after-commit | kogen-bench-us | r37reg-aj:debate-packplan-review | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | r37reg-arch:contract-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | r37reg-arch:debate-packplan-review | 3 | 3 | 3 | 0 | 0 |
| rails-as-variant-processed-once | studio | contract-review-sol | 5 | 1 | 1 | 0 | 0 |
| rails-as-variant-processed-once | studio | debate-packplan-review | 5 | 5 | 0 | 5 | 0 |
| rails-ft-cancelled-account-cleanup | studio | contract-review-sol | 5 | 1 | 0 | 1 | 0 |
| rails-ft-cancelled-account-cleanup | studio | debate-packplan-review | 5 | 5 | 0 | 5 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | contract-review-sol | 5 | 1 | 1 | 0 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | debate-packplan-review | 5 | 5 | 5 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | contract-review-sol | 5 | 1 | 1 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | debate-packplan-review | 5 | 3 | 3 | 0 | 0 |
| rails-sup-legacy-conversions | kogen-bench-eu | r37reg-sup:contract-review-sol | 3 | 3 | 0 | 3 | 0 |
| rails-sup-legacy-conversions | kogen-bench-eu | r37reg-sup:debate-packplan-review | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r37reg-syn14:contract-review-sol | 3 | 3 | 0 | 3 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r37reg-syn14:debate-packplan-review | 3 | 3 | 3 | 0 | 0 |
