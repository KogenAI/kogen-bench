# e06 context

## Status

**PILOT**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the pilot result is established.
- **UNMATCHED_CONDITIONS:** Only one pilot cell is reported and no comparison arm was run.
- **RAW_EVIDENCE_MISSING:** The exact task ID and sanitized raw cell record are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H54, H55 (provisional mapping; see the hypothesis register).
Question: Does forced context compaction improve a Build relative to a matched uncompressed control?
Population: One pilot cell is reported; no adjacent comparison arm is reported.
Headline: No comparative efficacy claim.

## Reported observations

- The pilot is reported as 1/1 run with six effective compactions. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No adjacent comparison was run. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision is not recovered. |
| Model and effort | Model and effort are not recovered. |
| Task IDs | One pilot cell is reported; exact task ID is not recovered. |
| Command | Not recovered; no public launch command or cell ID is available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** A single unpaired pilot cannot estimate a compaction treatment effect.

**Smallest useful next test:** Run matched forced-compaction and control cells under a frozen threshold, with exact context and outcome receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
