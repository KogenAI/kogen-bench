# Studio hill climb iteration 4

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No dated pre-registration before the first result is established.
- **RAW_EVIDENCE_PARTIAL:** Mined per-cell grades, available usage and wall fields, and patch hashes now cover the observed source rows; request logs, full attempt history, and a complete planned/ITT identity set remain unavailable.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: safe per-cell records and joined official grades are in [data/mined/hc-4.jsonl.gz](../../data/mined/hc-4.jsonl.gz); per-arm outcomes, token totals, wall medians, and comparisons are in [recomputed.json](recomputed.json). Request logs and transcripts are not included.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H75 (difficulty ladder), H136 (ladder variants), and H138 (matched model/effort baselines).

Date: 6 October 2026 (source-reported).

Question: Can shaping and planning effort be varied independently to find a cheaper ladder configuration without losing success?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio status record. The source summary describes a proposed ladder with Sol high, medium, or xhigh shaping/planning coupled to a Luna-max builder, using v2 discriminators and guards. The summary notes later planner-overlay instrumentation, but no completed decision record.

**Source-reported lifecycle status:** a duplicate trim was reported to avoid 47 unstarted cells; 43 cells were described as expected to remain, including nine already-started diagnostics; six Studio cells were owner-stopped. Smokes and planner-overlay instrumentation occurred. The mined store now contains 26 official-grade rows, including smoke cells, but the full planned cohort and its closed scored denominator remain unresolved, so no efficacy result is reported.

## Lifecycle counts

**Source-reported lifecycle counts:** Planned = not recovered. Started = not recovered; the reported 43 expected retained cells included nine already-started diagnostics, but this is not a complete start count. Finished = not recovered. The mined source now has 26 official-grade rows (20 non-smoke rows and six smokes); their relation to the reported lifecycle buckets and ITT denominator remains unresolved. The separate status summary reports 47 unstarted cells avoided and six owner-stopped Studio cells.

## Reproduction

- Exact Kogen commit: Kogen pin `cde7a380` resolves to [`cde7a380455e9793cb1fc8315791bc9beffb863b`](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Proposed Sol high/medium/xhigh shaping and planning with Luna-max builder. Whether shaping and planning were separated in every executed request is not verified; effective per-cell models and effort are unavailable.
- Task IDs: v2 discriminator and guard sets reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is a status record and is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary identifies status, brief, smoke, and variant records, but no final iteration result. Safe per-cell manifests, official grades, usage/wall fields, and patch hashes are now in [data/mined/hc-4.jsonl.gz](../../data/mined/hc-4.jsonl.gz); complete request and all-attempt records are not included.
- Reproduction procedure: The mined records recover 26 official grades and preserve smoke IDs, but the final cell-selection manifest, full attempt history, planner-overlay receipt, and complete ITT cohort are still missing. Keep unstarted, started, smoke, stopped, and graded identities distinct.

## Limits

The 26 mined grade rows include six smokes and cannot be assigned to a closed scored denominator from the surviving lifecycle records. Per-arm observed outcomes are in recomputed.json; no winner or full-round efficacy claim follows.

No measured superiority claim is made from this page. The recovered outcomes remain descriptive because the planned and ITT cohort is unresolved.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-4`; that export does not establish that no historical run occurred.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/hc-4.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 26 rows (fail 12, pass 14); overall pass rate is 53.8% (14/26) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 26 missing published metadata). Missing counters remain unknown, not zero.
This round also has 26 raw-only or non-public rows; they are kept separate from the published-export denominator.
Evidence update: raw storage contains 26 officially graded rows, although this page previously said the count was not recovered. Their exact IDs are listed in `recomputed.json`; the closed scored denominator remains unresolved, so this does not establish an efficacy cohort.
