# e09 locators and Tidewave

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**PILOT**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **INCOMPLETE_EXECUTION:** The Tidewave campaign stopped at 6 of 12 planned cells.
- **RAW_EVIDENCE_MISSING:** The public exact-ID capture remains absent; Studio rows are recovered below, but their mapping to the reported 6-of-12 campaign is unresolved.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H55, H60 (provisional mapping; see the hypothesis register).
Question: Do static/dynamic code locators or runtime inspection tools provide accurate, useful context for agent task completion?
Population: The locator case set is reported as 49 development oracle cases from a 70-case set. The Tidewave campaign planned 12 cells and stopped at 6.
Headline: No locator or Tidewave efficacy claim.

## Reported observations

- All 13 locator variants reportedly failed their per-case gate, set at 100% recall of affected tests and at least 75% precision; no locator model cells were dispatched. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate Tidewave screen reports zero unprompted calls and 17 calls when instructed. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- On the reported Phoenix subset, plain use scored 2/2 and Tidewave-instructed use 0/2; the campaign stopped after 6/12 cells. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The locator and runtime-tool studies are different protocols and should not be pooled. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | No locator Kogen harness run is reported. Exact revision for the runtime-tool cohort is not recovered. |
| Model and effort | The locator variants had no model dispatches. The runtime-tool summary reports Luna max; effective effort receipts are unavailable. |
| Task IDs | The oracle cohort spans seven stacks; exact case and runtime task IDs are not recovered. |
| Command | Not recovered; no public locator or Tidewave launch commands are available. |
| Raw records | The exact-ID query returned zero rows in the committed public exports. Filtered Studio rows are linked in the source recovery section below; see [reported-data.json](reported-data.json) for the public-export check. |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** Offline locator gate results and a small partial runtime-tool screen do not establish a live task-success benefit.

**Smallest useful next test:** Publish the per-case locator matrix, then run a preregistered matched Phoenix task comparison with identical prompts and complete cell receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/e09-tidewave.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 14 rows (fail 3, infra 7, interrupted 2, pass 2); overall pass rate is 40.0% (2/5) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 14 missing published metadata). Missing counters remain unknown, not zero.
This round also has 14 raw-only or non-public rows; they are kept separate from the published-export denominator.
