# r53


## Status

**INVALID**

Why not VALID:
- NO_PREREG — The README says no standalone success threshold was predeclared.
- OUTCOME_MISMATCH — Official cells and captured run records differ on one outcome.
- UNMATCHED_EFFORT — Kogen requested max ran at xhigh while direct Codex ran at true max.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **50.8%** (110 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Status reason: Official cells and captured run records differ on one outcome, so the former summary is removed. The known effort confound remains: Kogen requested max ran xhigh while direct Codex ran true max.



Pre-registered: no


Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Pipeline versus direct agents on 12 frozen held-out tasks.

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Design: 12 tasks × 3 arms × 3 reps = 108.

Decision rule: Frozen task set and arms; no standalone success threshold predeclared in headline source.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
- [rails-aj-resumable-cleanup](../../tasks/rails-aj-resumable-cleanup/task.json)
- [rails-ar-atomic-import](../../tasks/rails-ar-atomic-import/task.json)
- [rails-ar-erase-account](../../tasks/rails-ar-erase-account/task.json)
- [rails-ar-tenant-isolation](../../tasks/rails-ar-tenant-isolation/task.json)
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r53.jsonl](../../results/run-records/r53.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Reproduction record and source reconciliation

This section records the limits of exact replay and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` (per-cell `setup.kogen_sha`).
- Harness source commit: not recorded. The per-cell `tools.harness` SHA-256 fingerprint(s) are `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`, `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`, `b615447ac30a139410874241579db9c0e0d937340ec2d5d8350aca6643e1cfcf`; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `codex: model requested/effective gpt-6-luna → gpt-6-luna; effort requested/effective low → low`; `codex: model requested/effective gpt-6-luna → gpt-6-luna; effort requested/effective max → max`; `codex: model requested/effective gpt-6.1-sol → gpt-6.1-sol; effort requested/effective high → high`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs in captured records: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `rails-aj-resumable-cleanup`, `rails-ar-atomic-import`, `rails-ar-erase-account`, `rails-ar-tenant-isolation`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r53`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r53.jsonl](../../results/run-records/r53.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: captured deliveries 110 (97 pass, 9 fail, 4 ungraded/unknown in `results/run-records/r53.jsonl`); official outcome export 106 rows: 97 pass, 9 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** A one-cell classification conflict is recorded in the current status, but its exact cell is not established by the public aggregate rows. That conflict is source-reported, not reproducible from public data. Preserve INTERIM and do not restore the historical comparison or its p-value.
