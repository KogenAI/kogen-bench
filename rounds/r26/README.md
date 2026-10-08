# r26

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

Data completeness: **44.1%** (55 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical screening capture; the validity status is shown above.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Router capture, initially queued on 2 October 2026; 55 deliveries were later captured. The retained planning stage is the stated confound.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r26.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-05-cache-single-flight | kogen-bench-us | r26-elx05:route | 3 | 3 | 3 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-us | r26-elx07:route | 3 | 3 | 3 | 0 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | r26-elx12:route | 3 | 3 | 2 | 1 | 0 |
| rails-ac-throttle-search | studio | route | 5 | 5 | 4 | 1 | 0 |
| rails-aj-enqueue-after-commit | studio | route | 5 | 4 | 4 | 0 | 0 |
| rails-ar-archive-book-access | studio | route | 5 | 3 | 3 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | route | 5 | 5 | 5 | 0 | 0 |
| rails-as-variant-processed-once | studio | route | 5 | 3 | 3 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | route | 5 | 5 | 5 | 0 | 0 |
| rails-sec-audit-sweep | studio | route | 5 | 4 | 4 | 0 | 0 |
| rails-sup-legacy-conversions | studio | route | 5 | 5 | 5 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | r26-syn13:route | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r26-syn14:route | 3 | 3 | 3 | 0 | 0 |
