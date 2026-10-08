# r56c


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — No public predeclared decision rule was recovered.
- DESIGN — The dedicated design section and complete comparison protocol are absent.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **49.0%** (128 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r56c.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-07-cli-stats | kogen-bench-us | B-ctx-det | not re-derivable | 12 | 12 | 7 | 5 | 0 |
| elx-07-cli-stats | kogen-bench-us | P-noplan2 | not re-derivable | 12 | 12 | 8 | 4 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | P-noplan2 | not re-derivable | 12 | 12 | 6 | 6 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-us | B-ctx-det | not re-derivable | 12 | 12 | 2 | 10 | 0 |
| rails-ac-throttle-search | studio | P-noplan2 | not re-derivable | 12 | 12 | 11 | 1 | 0 |
| rails-aj-enqueue-after-commit | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |
| rails-as-variant-processed-once | kogen-bench-us | B-ctx-det | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-as-variant-processed-once | studio | P-noplan2 | not re-derivable | 12 | 12 | 9 | 3 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | P-noplan2 | not re-derivable | 12 | 11 | 10 | 1 | 0 |
| rails-hw-scoped-broadcast | kogen-bench-eu | B-ctx-det | not re-derivable | 6 | 6 | 6 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56c`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56c.jsonl](../../results/run-records/r56c.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 128 captured deliveries (95 pass, 32 fail, 1 ungraded/unknown in `results/run-records/r56c.jsonl`); official outcome export has 127 rows: 95 pass, 32 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** This is a separate corrective capture. It does not reconstruct the original validity-filtered analysis or authorize pooling with r56, r56b, r56d or r56p2.
