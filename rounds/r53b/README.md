# r53b


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — No dated registration or predeclared decision rule is recorded.
- CROSSWALK — Official outcomes cannot be matched to the captured arm rows.
- DESIGN — The testable question and exact arm recipes are not recoverable.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **32.6%** (108 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior captured arm table; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 53b: held-out replication (reps 4–6)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable. The previous label table is removed because no cell-level crosswalk is published; restoration requires a public mapping of captured deliveries to official cell IDs and outcomes.

Planned tasks in the surviving round note: elx-02-ingest-supervision, elx-04-queue-backpressure, rails-aj-resumable-cleanup, rails-ar-atomic-import, rails-ar-erase-account, rails-ar-tenant-isolation, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r53b.jsonl](../../results/run-records/r53b.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded in the public snapshot; per-cell `tools.harness` values are in the raw records.
- Models and effort (requested → effective): `codex: model requested/effective gpt-6-luna → gpt-6-luna; effort requested/effective max → max`; `codex: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective max → not recorded (Not recorded in available public metadata)`; `codex: model requested/effective gpt-6.1-sol → gpt-6.1-sol; effort requested/effective high → high`; `codex: model requested/effective gpt-6.1-sol → not recorded (Not recorded in available public metadata); effort requested/effective high → not recorded (Not recorded in available public metadata)`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `not recorded (Harness not retained): model requested/effective not recorded (Not recorded in available public metadata) → not recorded (Not recorded in available public metadata); effort requested/effective not recorded (Not recorded in available public metadata) → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `rails-aj-resumable-cleanup`, `rails-ar-atomic-import`, `rails-ar-erase-account`, `rails-ar-tenant-isolation`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`. Some delivery rows do not retain a task ID; see the declared gaps in [MISSING.md](MISSING.md).
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r53b`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r53b.jsonl](../../results/run-records/r53b.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 108 captured deliveries (44 pass, 3 fail, 61 ungraded/unknown in `results/run-records/r53b.jsonl`); official outcome export has 47 rows: 44 pass, 3 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this replication separate from r53. The public delivery export contains substantial ungraded and incompletely labelled rows; the overload correction does not provide a public exact delivery-to-official-cell crosswalk. Do not pool a replication headline.
