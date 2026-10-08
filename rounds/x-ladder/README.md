# x ladder

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Total planned cells across the ladder contracts are not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H39, H41, H42, H47, H49 (provisional mapping; see the hypothesis register).
Question: Do model escalation profiles improve success on the selected development tasks enough to justify their added time and cost?
Population: The model screen reports 8 tasks × 2 repetitions for selected arms; total planned cells across ladder contracts are not recovered.
Headline: Exploratory model and escalation observations only; no general routing claim.

## Reported observations

- On the reported eight-task/two-repetition comparison, Luna max and Sol 6.1 high each scored 15/16; Luna high scored 12/16. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate ladder matrix is reported as 117 attempts: 109 correct, 7 incorrect and 1 infrastructure result. All 7 incorrect outputs reportedly passed visible checks. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A time-first ladder and control are each reported at 6/6, with two rescues and about 141 additional seconds per attempt; a patient profile and control are each reported at 4/4. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A checkpoint-reproducibility screen reported 0/145 development runs with reproducible checkpoints. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness and Kogen revision were not recovered for this screen. |
| Model and effort | Reported profiles include Luna max, Sol 6.1 high and Luna high. Per-cell requested/effective effort records are unavailable. |
| Task IDs | An eight-task development panel is reported; exact task IDs are not recovered. |
| Command | Not recovered; the public snapshot has no launch manifest or selected cell IDs. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The development panel is small and selected. It does not establish a generally superior model route, and the visible-check result limits what the ladder matrix says about correctness.

**Smallest useful next test:** Freeze the model/effort map, task IDs, timeout, checkpoint rule and cost accounting; then evaluate matched profiles on held-out tasks.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-ladder.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 153 rows (fail 10, infra 2, pass 132, ungraded 9); overall pass rate is 93.0% (132/142) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 153 missing published metadata). Missing counters remain unknown, not zero.
This round also has 153 raw-only or non-public rows; they are kept separate from the published-export denominator.
