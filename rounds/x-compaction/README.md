# x compaction

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Planned-run totals are not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H54 (provisional mapping; see the hypothesis register).
Question: Did context compaction occur often enough in the traced hard-task runs to explain observed harness differences?
Population: The traced cohort is reported as 20 runs each for kh, Codex and Pi; planned-run totals are not recovered.
Headline: No causal compaction claim.

## Reported observations

- No compaction was recorded in 0/60 traced runs: 0/20 each for kh, Codex and Pi. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- Reported median peak input was 40.5k tokens for kh, 64.1k for Codex and 38.5k for Pi. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A kh elision review reports retaining 14/18 facts, marked preliminary. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate forced-compaction pilot in e06-context ran once and had no adjacent comparison. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact per-run revisions were not recovered. |
| Model and effort | Model names and efforts by harness are not fully recoverable from this public summary. |
| Task IDs | The summary covers 60 hard-task runs; task IDs are not recovered. |
| Command | Not recovered; this is a trace analysis, not a reproducible launch command. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** These runs did not exercise compaction. They cannot estimate the effect of compaction or attribute a measured harness gap to compaction.

**Smallest useful next test:** Use a predeclared context-pressure cohort that triggers compaction in each matched arm and records exact before/after context and task outcomes.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Studio source recovery

Studio retains source patches only; the staged source contains no per-cell model manifests or outcome rows. This source remains in [the source inventory](../../data/mined/STUDIO-SOURCES.json); the round’s published status and numbers are unchanged.
