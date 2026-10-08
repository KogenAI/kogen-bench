# x minikogen

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Exact allocation by mechanism is not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H31, H32 (provisional mapping; see the hypothesis register).
Question: Can selected Kogen loop mechanisms be removed or simplified without reducing task outcomes or coverage?
Population: Five mechanism pairs are reported at n=4 per arm; exact allocation by mechanism is not recovered.
Headline: No net simplification claim.

## Reported observations

- Test-first removal is reported at 4/4 versus 4/4; reported wall changed from 2,658 to 1,586 seconds, while coverage equivalence was not measured. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A frozen-decision answer mechanism is reported to change strict acceptance from 2/4 to 4/4 at higher cost. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No net simplification was established. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Model and effort per mechanism pair were not recovered. |
| Task IDs | Exact task IDs are not recovered. |
| Command | Not recovered; no public launch command or cell IDs are available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The mechanism pairs do not isolate an overall simplification benefit, and the reported coverage measure is incomplete.

**Smallest useful next test:** Freeze one mechanism at a time, preserve equivalent checks and coverage, and publish paired task-level cost and outcome records.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
