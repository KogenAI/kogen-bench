# x roles

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Cohort-specific planned, started, finished, and ITT denominators are incomplete.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H39, H43, H49 (provisional mapping; see the hypothesis register).
Question: Do different model assignments to worker and reviewer roles improve completion or review quality at an acceptable cost?
Population: Cohort-specific planned, started, finished and ITT denominators are not fully recovered.
Headline: Operational screens only; no role policy qualification.

## Reported observations

- A one-task worker pilot reports Sol high 2/2 and Luna max 2/2; the source estimates Luna at about 7× lower API-equivalent cost and 1.7× the wall time. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- An implementation screen reports Sol high 4/7 and Luna high 2/7, with one infrastructure result in each arm. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A reviewer-envelope screen reports Sol high 0/4 complete and Luna high 2/2 complete, with 23/24 judgments correct in the reported Luna cohort. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No worker or reviewer policy was selected. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision per role cohort was not recovered. |
| Model and effort | Reported worker arms use Sol high and Luna max; an implementation screen uses Luna high; reviewer comparisons include Sol high and Luna high. Exact effective-effort receipts are unavailable. |
| Task IDs | The worker pilot used one CSV task. The implementation cohort task IDs and reviewer fixture IDs are not recovered. |
| Command | Not recovered; no public launch command or exact cell IDs are available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The task and reviewer samples are small and not a common matched cohort. Cost is an API-equivalent estimate, not invoice spend.

**Smallest useful next test:** Predeclare matched role/task cells, reviewer ground truth, effective settings, cost definitions and completion criteria before a larger held-out comparison.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
