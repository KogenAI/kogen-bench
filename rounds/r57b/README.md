# r57b


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — No dated registration is linked in the committed public record.
- DESIGN — The README says no testable question or complete comparison protocol is established.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **48.6%** (96 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: unverified; no dated registration is linked in the committed public record.


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 57b: shell-only vs default tools on Rails (Studio) (4 Oct ~11:45Z)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-port-erase-account, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast, syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists elx-port-erase-account, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast, syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: None. Listed task IDs with no matching tagged delivery: elx-port-erase-account, syn-14-bug-sla-business-hours. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: The public exports record 32 passes among 48 shell-only rows and 31 passes among 48 default-tools rows. The previously reported accuracy bound is not reproduced because its interval method and assumptions are not documented. No non-inferiority decision is made.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r57b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-ac-throttle-search | studio | default-tools | not re-derivable | 8 | 8 | 4 | 4 | 0 |
| rails-ac-throttle-search | studio | shell-only | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | default-tools | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | shell-only | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | default-tools | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | shell-only | not re-derivable | 8 | 8 | 7 | 1 | 0 |
| rails-as-variant-processed-once | studio | default-tools | not re-derivable | 8 | 8 | 4 | 4 | 0 |
| rails-as-variant-processed-once | studio | shell-only | not re-derivable | 8 | 8 | 3 | 5 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | default-tools | not re-derivable | 8 | 8 | 0 | 8 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | shell-only | not re-derivable | 8 | 8 | 0 | 8 | 0 |
| rails-hw-scoped-broadcast | studio | default-tools | not re-derivable | 8 | 8 | 7 | 1 | 0 |
| rails-hw-scoped-broadcast | studio | shell-only | not re-derivable | 8 | 8 | 6 | 2 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r57b`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r57b.jsonl](../../results/run-records/r57b.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 96 captured deliveries (63 pass, 33 fail, 0 ungraded/unknown in `results/run-records/r57b.jsonl`); official outcome export has 96 rows: 63 pass, 33 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this captured round separate from r57/r57c/r57d and from r57e. The historical pooled non-inferiority interval and cost-per-pass comparison are source-reported, not reproducible from public data.
