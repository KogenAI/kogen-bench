# r36

## Status

**INVALID**

Why not VALID:
- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **OUTCOME_CROSSWALK** — The README says official cells outcomes do not match a prior captured pass count.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-hw-scoped-broadcast, rails-sup-legacy-conversions, syn-14-bug-sla-business-hours.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **44.7%** (33 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).













Status reason: Official cells outcomes do not match one prior captured pass count; the table and result summary are removed.





Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: Can a lower-cost ensemble reach the observed pass rates of the Sol-helped pipeline on the selected tasks?
Design: The historical recipe describes a Luna high pack plan, five Luna low builds, Luna high selection and scoped review. The selected-build criterion is not re-derivable from the public record. Studio worker tasks: rails-aj-enqueue-after-commit, rails-sup-legacy-conversions, rails-hw-scoped-broadcast, rails-ar-bulk-access-grants and rails-ac-throttle-search, three reps each; worker tasks: elx-07-cli-stats, elx-12-retry-api-deprecation and syn-14-bug-sla-business-hours, three reps each. The Sol-assisted reproduction-and-review comparison used the same worker tasks.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-hw-scoped-broadcast, rails-sup-legacy-conversions, syn-14-bug-sla-business-hours

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r36.jsonl](../../results/run-records/r36.jsonl); no combined result is reported here.
