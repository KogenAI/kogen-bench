# x continuation

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of NOT_EXECUTED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **NOT_EXECUTED:** No real model-backed attempt ran; only scripted-provider checks are reported.
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the result is established.
- **RAW_EVIDENCE_MISSING:** Exact-ID round records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **NOT-RUN**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H31, H65 (provisional mapping; see the hypothesis register).
Question: Can the headless continuation bridge resume a Build after a bounded handoff without losing task state?
Population: No real model attempt. A scripted-provider check is reported before and after a mechanical change.
Headline: NOT-RUN for model-backed efficacy; mechanical checks only.

## Reported observations

- The real-model continuation lane is reported at 0 attempts because of headless-bridge and keyless-Build blockers. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- Offline scripted-provider checks are reported to change from 3/6 to 6/6. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The offline checks are not model-backed Build outcomes. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | No live Kogen/harness revision is attributable to a scored model run. |
| Model and effort | No real model attempts were run. |
| Task IDs | No live task IDs are attributable; scripted test IDs are not in the public snapshot. |
| Command | The scripted-provider test command was not recovered. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** No live continuation or Build-success effect was measured.

**Smallest useful next test:** Repair launch prerequisites, freeze task state and handoff criteria, then run a live matched continuation test with full attempt receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Studio source recovery

Studio retains source patches only, and the source reports no real model attempts. No outcome row was imported. This source remains in [the source inventory](../../data/mined/STUDIO-SOURCES.json); the round’s published status and numbers are unchanged.
