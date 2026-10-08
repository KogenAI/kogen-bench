# x models

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **COHORTS_NOT_POOLABLE:** The separate model screens must not be combined.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H39, H40, H41, H42, H43, H46 (provisional mapping; see the hypothesis register).
Question: Which model and effort setting is the most useful starting point for this development task panel?
Population: 204 attempts planned for the broader x-models collection; 155 completed graded attempts are reported and 49 planned attempts were cancelled.
Headline: No model or effort default follows from these exploratory screens.

## Reported observations

- The broader collection reports 155 completed graded attempts, 122 correct and 33 incorrect; 49 of 204 planned attempts were cancelled. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The primary eight-task screen reports Luna max 7/8 and adjacent Sol 6.1 high 6/8; the source labels it inconclusive. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate eight-task/two-repetition model panel reports Luna max 15/16, Sol 6.1 high 15/16, and Luna high 12/16. Do not combine the screens. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- Astra medium is reported at 16/16 in a separate small comparison with Sol high; exact task and cell alignment is unavailable. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness and Kogen revision were not recovered. |
| Model and effort | Reported arms include Luna max and Sol 6.1 high; a separate comparison includes Luna high and Astra medium. Exact per-cell effective-effort receipts are unavailable. |
| Task IDs | The primary model screen is reported over eight tasks; exact task IDs are not recovered. |
| Command | Not recovered; no public launch command or selected-cell manifest is available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The reported screens are small, adaptive and development-only. They do not establish a causal model ranking or an effort policy.

**Smallest useful next test:** Run a frozen, randomized, task-matched effort panel with explicit effective-effort receipts, full ITT and a held-out set.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
