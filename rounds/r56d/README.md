# r56d

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of CROSSWALK, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No public predeclared decision rule was recovered.
- CROSSWALK — Official outcomes cannot be matched to the prior builder-context and P-noctx2 rows.
- DESIGN — The dedicated design section and exact arm specification are absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **38.9%** (37 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior builder-context and P-noctx2 arm rows; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r56d.jsonl](../../results/run-records/r56d.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56d`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56d.jsonl](../../results/run-records/r56d.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 37 captured deliveries (12 pass, 2 fail, 23 ungraded/unknown in `results/run-records/r56d.jsonl`); official outcome export has 14 rows: 12 pass, 2 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** This validity/correction capture remains separate from r56, r56b, r56c and r56p2. The public ledger does not establish a complete original arm comparison.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r56d.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 14 rows (fail 2, pass 12); overall pass rate is 85.7% (12/14) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 14/14 shared cell IDs match; 0/14 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 3/14 published metadata totals equal the manifest `input + cached input + output` sum; 11 differ (multi request aggregation 11). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56d-studio`: published `2812589`, manifest `2013886`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56d-studio`: published `3217337`, manifest `2590734`, provider responses `59`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56d-studio`: published `3441900`, manifest `3062213`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-noctx2-r56d-studio`: published `3964455`, manifest `3542441`, provider responses `59`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-P-noctx2-r56d-studio`: published `3591397`, manifest `2992726`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-full-r56d-studio`: published `3226472`, manifest `2258224`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-noreview-r56d-studio`: published `3350450`, manifest `2221925`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-P-nocontract-r56d-studio`: published `2702389`, manifest `1820995`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-P-noreview-r56d-studio`: published `2906991`, manifest `2015616`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r4-P-nocontract-r56d-studio`: published `4729823`, manifest `3648841`, provider responses `60`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r4-P-noreview-r56d-studio`: published `4977917`, manifest `3927002`, provider responses `61`; `multi_request_aggregation`.
