# x parallel

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **SMALL_SAMPLE:** The reported comparison is two tasks by two repetitions per arm.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H30 (provisional mapping; see the hypothesis register).
Question: Does planned parallel work improve completion enough to justify its additional requests, tokens and wall time?
Population: Two tasks × two repetitions for solo and planned-DAG arms are reported.
Headline: No throughput or general parallel-work claim.

## Reported observations

- Solo and planned-DAG arms are each reported at 4/4 passes. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The candidate parallel arm is reported at about 1.4× wall time and about 1.9× requests. A separate summary reports 1.84× input tokens and 2.50× output tokens; these measures are retained separately. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The summary recommends retaining solo for this two-task panel. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Per-cell model and effort values were not recovered. |
| Task IDs | Two tasks are reported; exact IDs are not recovered. |
| Command | Not recovered; public launch command and exact cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The panel is too small to establish general parallel-work effects; the reported resource increase did not accompany a pass-rate gain here.

**Smallest useful next test:** Test on tasks with demonstrated parallelizable work using a frozen DAG, matched solo controls, and public request/token/wall receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
