# r56


## Status

**INVALID**

Why not VALID:
- NO_PREREG — The README says the adoption criterion was not predeclared in a verifiable registration.
- OUTCOME_MISMATCH — Official outcomes and captured run-record classifications differ.
- FILTER — The source valid-grade filter cannot be reconstructed from the round files.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **46.7%** (222 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Status reason: The official outcome states and the captured run-record classifications differ, and the source valid-grade filter cannot be reconstructed; no adoption test is assessed here.



Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Which individual stages and context options justify their cost?

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Design: Eight tuning tasks; corrected single-stage ablations and builder-context arms. The source note targeted 93 valid reps per arm, but the valid-grade filter cannot be reconstructed from the public record.

Decision rule: The source note proposed adoption only at a gain of at least 15 percentage points with one-sided p<0.05 and at least 93 valid reps in both arms. The public valid-grade filter is not reconstructable, so this criterion is not evaluated.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: 

- [elx-07-cli-stats](../../tasks/elx-07-cli-stats/task.json)
- [elx-12-retry-api-deprecation](../../tasks/elx-12-retry-api-deprecation/task.json)
- [rails-ac-throttle-search](../../tasks/rails-ac-throttle-search/task.json)
- [rails-aj-enqueue-after-commit](../../tasks/rails-aj-enqueue-after-commit/task.json)
- [rails-ar-bulk-access-grants](../../tasks/rails-ar-bulk-access-grants/task.json)
- [rails-as-variant-processed-once](../../tasks/rails-as-variant-processed-once/task.json)
- [rails-ft-mysql-fulltext-search-foundation](../../tasks/rails-ft-mysql-fulltext-search-foundation/task.json)
- [rails-hw-scoped-broadcast](../../tasks/rails-hw-scoped-broadcast/task.json)

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r56.jsonl](../../results/run-records/r56.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56.jsonl](../../results/run-records/r56.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 222 captured deliveries (156 pass, 44 fail, 22 ungraded/unknown in `results/run-records/r56.jsonl`); official outcome export has 200 rows: 156 pass, 44 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this original capture separate from r56b, r56c, r56d and r56p2. The public records do not reproduce the historical validity-filtered analysis or its arm-level adoption tests; retain INTERIM and do not reinstate the old comparison table.
