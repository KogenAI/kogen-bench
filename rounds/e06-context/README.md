# e06 context

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING, UNMATCHED_CONDITIONS. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**PILOT**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the pilot result is established.
- **UNMATCHED_CONDITIONS:** Only one pilot cell is reported and no comparison arm was run.
- **RAW_EVIDENCE_MISSING:** The B028 packet verifies one pass cell; the public exact-ID capture remains absent and the separate r1 ledger row has no manifest.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H54, H55 (provisional mapping; see the hypothesis register).
Question: Does forced context compaction improve a Build relative to a matched uncompressed control?
Population: One pilot cell is reported; no adjacent comparison arm is reported.
Headline: No comparative efficacy claim.

## Reported observations

- The pilot is reported as 1/1 run with six effective compactions. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No adjacent comparison was run. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision is not recovered. |
| Model and effort | Model and effort are not recovered. |
| Task IDs | One pilot cell is reported; exact task ID is not recovered. |
| Command | Not recovered; no public launch command or cell ID is available. |
| Raw records | The exact-ID query returned zero rows in the committed public exports. Filtered Studio rows are linked in the source recovery section below; see [reported-data.json](reported-data.json) for the public-export check. |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** A single unpaired pilot cannot estimate a compaction treatment effect.

**Smallest useful next test:** Run matched forced-compaction and control cells under a frozen threshold, with exact context and outcome receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/e06-context.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 2 rows (infra 1, pass 1); overall pass rate is 100.0% (1/1) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 2 missing published metadata). Missing counters remain unknown, not zero.
This round also has 2 raw-only or non-public rows; they are kept separate from the published-export denominator.
