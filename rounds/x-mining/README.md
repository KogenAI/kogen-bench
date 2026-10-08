# x mining

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_MISMATCH:** The inventory, usage audit, and diagnostic panel are distinct populations.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H80, H84, H89 (provisional mapping; see the hypothesis register).
Question: Can observed development-run failures be classified into reusable failure modes, and does a diagnostic playbook change outcomes?
Population: The observation inventory and X09 panel are separate populations; neither supplies an ITT denominator for the other.
Headline: Inventory and diagnostic only.

## Reported observations

- The inventory reports 2,608 contestant observations: 2,152 PASS, 295 FAIL, 54 INFRA and 107 PENDING. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate usage audit reports missing usage on 124/2,649 observations; this denominator is not the 2,608 status inventory. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- X09 reports 14/14 completed, described as inconclusive. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Mixed versions; no single exact harness/Kogen SHA applies to the inventory. |
| Model and effort | Mixed model/harness versions; per-observation model and effort are not present in the public summary. |
| Task IDs | Task IDs for the inventory and X09 panel are not recovered. |
| Command | Not recovered; no mining or X09 launch command is published. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** Mixed versions, distinct denominators and the diagnostic selection prevent a general failure-rate or playbook-efficacy claim.

**Smallest useful next test:** Freeze the event schema and cohort, reconcile all attempts and missing usage, then validate a failure classifier prospectively against blinded outcomes.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
