# r64d


## Status

**DESCRIPTIVE**

Why not VALID:
- NO_PREREG — The README explicitly says no preregistration evidence is identified.
- DESIGN — The round note is source-reported and does not establish the complete comparison protocol.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **44.8%** (20 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 64d: Kogen plan-shell on held-out Rails tasks in Studio; described in a surviving note dated approximately 00:45Z on 5 October. No preregistration evidence is identified.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-aj-resumable-cleanup, rails-ar-atomic-import, rails-ar-erase-account, rails-ar-tenant-isolation

Verdict: This capture is descriptive; its public page does not support a comparison with the historical direct reference cohorts.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r64d.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). No planned n is reported here; captured repetitions are delivered-row counts and are not used to infer a plan.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-aj-resumable-cleanup | studio | kh-plan-shell | not reported | 5 | 5 | 4 | 1 | 0 |
| rails-ar-atomic-import | studio | kh-plan-shell | not reported | 5 | 5 | 5 | 0 | 0 |
| rails-ar-erase-account | studio | kh-plan-shell | not reported | 5 | 4 | 0 | 4 | 0 |
| rails-ar-tenant-isolation | studio | kh-plan-shell | not reported | 5 | 5 | 5 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-aj-resumable-cleanup`, `rails-ar-atomic-import`, `rails-ar-erase-account`, `rails-ar-tenant-isolation`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r64d`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r64d.jsonl](../../results/run-records/r64d.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 20 captured deliveries (14 pass, 5 fail, 1 ungraded/unknown in `results/run-records/r64d.jsonl`); official outcome export has 19 rows: 14 pass, 5 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** This held-out capture remains distinct from r64/r64b/r64c/r64e and historical direct anchors. Do not treat its public delivery table as a cross-round comparison.
