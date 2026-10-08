# r70 compilation timing


## Status

**DESCRIPTIVE**

Why not VALID:
- NO_PREREG — The README explicitly says no pre-registration.
- DESCRIPTIVE_ONLY — The round measures compile timing and does not have a pre-registered inferential decision rule.
- EVIDENCE_SCOPE — Retained timing summaries support description but do not establish the full VALID criteria.
- relabelled 2026-10-08 after scrutiny

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs: not recorded in the cited round source.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **N/A** (0 deliveries; NO DELIVERED DATA). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no
Label: DESCRIPTIVE
Question: How long does each candidate language take to compile Kogen-like code?
n: 300 timing rows; n=5 per tool/task combination and timed phase.
Headline: The two timing windows each contain 150 rows and are marked valid in their raw summaries; the timing table is in [RESULTS.md](RESULTS.md).
Limit: One host, two timing windows, five repetitions per cell; descriptive timing only.
Headline-number note: Counts are not re-derived here; the raw timing ledgers and summaries are linked below.

Sources: [method](METHOD.md); [main raw timing ledger](raw/timings.jsonl); [main run summary](raw/worker-summary.json); [supplement timing ledger](raw/timings-supplement.jsonl); [supplement run summary](raw/supplement-summary.json).

## Public delivery and outcome reconciliation

No standard scored benchmark cells are attributed to this round. The timing study contains 300 rows; see the [main timing ledger](raw/timings.jsonl), [supplement timing ledger](raw/timings-supplement.jsonl), and [timing results](RESULTS.md) for its n and measurements.
