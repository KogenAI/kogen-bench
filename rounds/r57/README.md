# r57


## Status

**INVALID**

Why not VALID:
- NO_PREREG — No dated pre-registration is recorded in the round files.
- ARM_MAPPING — The control-default-tools pass count differs from official cells, and the label maps to multiple exported arms.
- EVIDENCE — The pooled r57–r57d cohort ledger and missing-cell identity are not linked.

## Required reproduction metadata

- Kogen commit: not applicable; the r57 exported records identify the Harness arm as not using Kogen.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **49.9%** (41 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).













Status reason: The control-default-tools pass count differs from official cells, and default-tools maps to multiple exported arms; the local table is removed. The pooled r57–r57d analysis remains unreproducible.





Pre-registered: no


Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Does shell-only reduce tokens without materially reducing accuracy?

Venue: r57 kogen-bench-us; r57b/r57d studio; r57c kogen-bench-eu.

Design: A pooled r57–r57d analysis was reported, but its cohort ledger and missing-cell identity are not linked; this page retains only the local r57 delivery record.

Decision rule: Lower shell median tokens in ≥80% strata; one-sided 95% accuracy lower bound ≥−10 pp.

Arms: default-tools and shell-only; Luna actual xhigh builder.

Planned tasks in the surviving round note: 

- [elx-05-cache-single-flight](../../tasks/elx-05-cache-single-flight/task.json)
- [elx-07-cli-stats](../../tasks/elx-07-cli-stats/task.json)
- [elx-12-retry-api-deprecation](../../tasks/elx-12-retry-api-deprecation/task.json)
- [rails-ac-throttle-search](../../tasks/rails-ac-throttle-search/task.json)
- [rails-aj-enqueue-after-commit](../../tasks/rails-aj-enqueue-after-commit/task.json)
- [rails-ar-bulk-access-grants](../../tasks/rails-ar-bulk-access-grants/task.json)
- [rails-as-variant-processed-once](../../tasks/rails-as-variant-processed-once/task.json)
- [rails-ft-mysql-fulltext-search-foundation](../../tasks/rails-ft-mysql-fulltext-search-foundation/task.json)
- [rails-hw-scoped-broadcast](../../tasks/rails-hw-scoped-broadcast/task.json)
- [syn-13-bug-empty-filter-crash](../../tasks/syn-13-bug-empty-filter-crash/task.json)
- [syn-14-bug-sla-business-hours](../../tasks/syn-14-bug-sla-business-hours/task.json)

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r57.jsonl](../../results/run-records/r57.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `elx-05-cache-single-flight`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `syn-13-bug-empty-filter-crash`, `syn-14-bug-sla-business-hours`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r57`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r57.jsonl](../../results/run-records/r57.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 41 captured deliveries (34 pass, 7 fail, 0 ungraded/unknown in `results/run-records/r57.jsonl`); official outcome export has 41 rows: 34 pass, 7 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** The [L0 pooled CSV](../l0-reconcile/data/r57-pooled-itt.csv) and `python3 reproduce/reconcile_l0.py` reproduce a separate recovered 311-row pooled population, with public outcome matches for those 311 rows. One planned Studio shell-only slot has no recovered cell ID or outcome, so the full planned denominator remains incomplete. This does not resolve the control-arm mapping conflict on this page: default-tools maps to multiple public exported arms, so this round's own arm-level comparison is not reconstructed. Do not pool this page with r57b/r57c/r57d or the separate r57e replacement.
