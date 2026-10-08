# x surface

## Status

**INCOMPLETE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **INCOMPLETE_EXECUTION:** Only 8 of 16 planned or reported cells were complete at the cited cutoff.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H31, H33, H110 (provisional mapping; see the hypothesis register).
Question: Do changes to the agent-facing feedback surface improve completion or reduce unnecessary interaction?
Population: 16 cohort cells were planned/reported; 8/16 completed at the cited cutoff.
Headline: No agent-output format claim.

## Reported observations

- The feedback-format cohort is reported as 8/16 completed. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- On the fixture repair subset, the compared models are reported tied at 2/2 versus 2/2. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The remaining repetition was unrun. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Models are reported as compared for a fixture repair; exact model/effort receipt is unavailable. |
| Task IDs | Fixture task IDs are not recovered. |
| Command | Not recovered; launch command and exact cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** This partial fixture cohort does not establish an output-format preference or a completion benefit.

**Smallest useful next test:** Complete the registered repetitions on the same tasks and compare parse success, diagnosis, repair and resource use.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
