# x race

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **ARITHMETIC_UNRECOMPUTABLE:** The reported 48-cell pass total is not reproducible from retained records.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H30 (provisional mapping; see the hypothesis register).
Question: Do racing multiple workers improve selected task outcomes over simpler arms when a deterministic selector chooses a candidate?
Population: Six tasks × two repetitions × four arms = 48 reported cells.
Headline: No superiority or deployment claim; the pass total is source-reported and not reproducible.

## Reported observations

- The four-arm panel is reported as 48/48 graded passes, a ceiling result on this task set. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A selector false-acceptance check is reported as 0/24. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No two-agent policy was promoted. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Per-arm model and effort values were not recovered in the public snapshot. |
| Task IDs | Six tasks are reported; exact public task IDs are not recovered. |
| Command | Not recovered; public launch command and cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** A ceiling panel cannot estimate improvement in success rate, and the selector check does not qualify a live multi-agent route.

**Smallest useful next test:** Use tasks with measured headroom, compare solo and race under a frozen selection rule, and report wall time and token cost by task.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
