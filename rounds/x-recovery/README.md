# x recovery

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Planned, started, finished, graded, and ITT counts are not recoverable.
- **RAW_EVIDENCE_MISSING:** The public exact-ID capture remains absent; the Studio rows below do not establish the full published cohort.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H65 (provisional mapping; see the hypothesis register).
Question: Do the tested failure and checkpoint mechanisms recover a task after interruption without corrupting or losing progress?
Population: Planned, started, finished, graded and ITT counts are not recoverable from the public summary.
Headline: No recovery efficacy claim.

## Reported observations

- A separate fault/checkpoint ledger is reported to exist, but no per-arm extraction or cell-to-outcome crosswalk is available here. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No quantitative recovery result is published on this page. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Model and effort applicability is not recovered. |
| Task IDs | Exact task and fault-injection IDs are not recovered. |
| Command | Not recovered; no public fault-injection command or cell IDs are available. |
| Raw records | The exact-ID query returned zero rows in the committed public exports. Filtered Studio rows are linked in the source recovery section below; see [reported-data.json](reported-data.json) for the public-export check. |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The current record does not support a recovery-effect claim.

**Smallest useful next test:** Publish a sanitized fault matrix with exact attempt IDs, initial checkpoint state, injected fault, recovery outcome and task correctness.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-recovery.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 32 rows (fail 1, pass 31); overall pass rate is 96.9% (31/32) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 32 missing published metadata). Missing counters remain unknown, not zero.
This round also has 32 raw-only or non-public rows; they are kept separate from the published-export denominator.
