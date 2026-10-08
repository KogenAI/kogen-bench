# benchmark night 2026-10-01

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** The reported approximate inventory is not a recovered planned or ITT denominator.
- **RAW_EVIDENCE_MISSING:** The public exact-ID capture remains absent; the Studio extraction has 84 cell rows, with 75 ungraded.


## Required reproduction metadata

- Kogen commit: not recorded as a resolvable commit in the cited round source; the source carries the unresolved identifier `52c43a05`.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H19, H21, H29, H31, H80, H81, H82, H84, H85, H86, H87, H88, H89, H90 (provisional mapping; see the hypothesis register).
Question: Across the exploratory P1–P5 lanes, did the tested Kogen configurations improve valid task completion or parallel efficiency over the comparison arms?
Population: About 265 cells are reported across the night; this is an approximate inventory, not a recovered planned or ITT denominator.
Headline: Exploratory night; no validated improvement.

## Reported observations

- About 265 cells across four hosts are reported. Thirty grades over seven tasks were invalid because a Trackline start overlay was missing; 20 invalid grades are attributed to syn-33. These are not model losses. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- P2 env-v2 valid-only summary: Kogen L1 34/47 and Codex 35/48. A broader admitted panel is described as 52 tasks; P1 env-v1 results are not reconstructed here. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- P3a relay and L1 are reported at 5/5 and 3/5; P3c relay and L1 at 4/5 and 5/5. These lanes remain separate. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- P5 selected-failure subset: relay 2/9 and L1 0/9; the report separately says seven Rails tasks all failed. Exact task mapping is unavailable. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A parallel-read-tools screen is reported tied at 5/5, with about 20–30% fewer requests; lane identity and raw request counts are not recovered. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- Pi 1.0.0 was installed for mining and was not run as a benchmark arm. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The documentary verdict is no validated improvement. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | A variant revision prefix 52c43a05 is reported. Full Kogen/harness SHA and mapping to each lane are not recovered. |
| Model and effort | Luna max is reported for the P2 Kogen L1 comparison. Exact model and effective effort by P1–P5 arm are not fully recovered. |
| Task IDs | A 52-task public development panel is reported for P2; exact per-lane task IDs are not recovered. syn-33 is identified among invalid grades. |
| Command | Not recovered; public launch commands and exact selected cell IDs are unavailable. |
| Raw records | The exact-ID query returned zero rows in the committed public exports. Filtered Studio rows are linked in the source recovery section below; see [reported-data.json](reported-data.json) for the public-export check. |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** Invalid grades, environment changes, small selected subsets and missing arm-to-cell mapping prevent a validated improvement claim. Do not pool P1 with P2 or P3a with P3c.

**Smallest useful next test:** Recover sanitized exact cell/arm IDs and invalid-grade partitions, pin one Kogen revision and environment epoch, then rerun the matched comparison with a preregistered ITT rule.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/night-2026-10-01.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 84 rows (fail 6, pass 3, ungraded 75); overall pass rate is 33.3% (3/9) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 84 missing published metadata). Missing counters remain unknown, not zero.
This round also has 84 raw-only or non-public rows; they are kept separate from the published-export denominator.
