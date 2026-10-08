# r68b


## Status

**DESCRIPTIVE**

Why not VALID:
- NO_PREREG — The README records no pre-registration or decision rule.
- UNMATCHED_EFFORT — Requested max was clamped to xhigh, while historical controls used different effort settings.
- COMPARATOR — Controls are historical rather than contemporaneous matched conditions.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **46.6%** (24 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: How did the Kogen plan-shell arm perform on the held-out Elixir/Phoenix task panel?

Venue: Fixed eight-task HELDOUT kogen-bench-us/kogen-bench-eu placement.

Design: 8 tasks × 3 reps, historical same-task direct comparisons.

Decision rule: none predeclared located in supplied sources.

Arms: Current Kogen plan-shell. Historical direct controls are public [r53](../r53/README.md) cells filtered to `round=r53` and `arm=r53:lmax` (Luna max) or `arm=r53:sol-high` (Sol high); see the [cells export](../../results/cells.jsonl).

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Recomputed 6 October 2026 from the public cell export: current r68b Kogen plan-shell passed 21/24. The r53 direct Luna-max arm (`arm=r53:lmax`) passed 21/24 and ran at `gpt-6-luna / max`; the r53 direct Sol-high arm (`arm=r53:sol-high`) passed 22/24 and ran at `gpt-6.1-sol / high`. Kogen requested max was clamped to xhigh; these small, effort-confounded cohorts do not establish superiority.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r68b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-02-ingest-supervision | kogen-bench-us | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| elx-04-queue-backpressure | kogen-bench-eu | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-01-live-ticket-filters | kogen-bench-us | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-06-migration-ticket-numbers | kogen-bench-eu | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-15-validation-ticket-form | kogen-bench-eu | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-20-email-invite-flow | kogen-bench-us | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-24-csv-import | kogen-bench-eu | plan-shell | 3 | 3 | 3 | 3 | 0 | 0 |
| syn-31-inbound-email-webhook | kogen-bench-us | plan-shell | 3 | 3 | 3 | 0 | 3 | 0 |
