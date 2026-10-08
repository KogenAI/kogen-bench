# Studio hill climb iteration 1

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
- Raw records: safe per-cell records and joined official grades are in [data/mined/hc-1.jsonl.gz](../../data/mined/hc-1.jsonl.gz); per-arm outcomes, token totals, wall medians, and comparisons are in [recomputed.json](recomputed.json). Request logs and transcripts are not included.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H75 (difficulty ladder) and H136 (ladder variants).

Date: 5 October 2026 (source-reported).

Question: Does a Sol-shaped Kogen ladder improve the development panel over a shorter ladder with a Sol-medium builder?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes two arms on a ten-task development set with two repetitions per arm. Exact task IDs and the full arm manifest are not in the public record.

**Published source-reported headline, now checked against mined rows below:** 40/40 scored cells were officially graded. The mixed Luna/Sol ladder with Sol-high shaping scored 19/20; the Sol-medium-builder challenger with Sol-high support scored 17/20 and was discarded under the reported KEEP rule. The mined store contains four additional smoke grades, listed separately below. The control was already saturated on this development panel; these results do not qualify a benchmark advantage.

## Lifecycle counts

**Source-reported scored lifecycle:** Planned = 40 scored cells. Started = not recovered. Finished = not separately recorded. Officially graded = 40 scored cells; the mined store separately contains four smoke grades. ITT denominator and disposition partition = not recovered; the reported scored denominator is not an ITT reconstruction.

## Reproduction

- Exact Kogen commit: Kogen pin `1d567772` resolves to [`1d567772446a66ea75fd04ae0e9c514b835f2d20`](https://github.com/KogenAI/kogen-ex/commit/1d567772446a66ea75fd04ae0e9c514b835f2d20).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Control: mixed Luna/Sol ladder with Sol-high shaping. Challenger: Sol-medium builder with Sol-high support. Exact per-stage requested and effective model/effort receipts are unavailable.
- Task IDs: Ten-task v1 development panel reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary also identifies an archived iteration-1 report. Safe per-cell manifests, official grades, usage/wall fields, and patch hashes are now in [data/mined/hc-1.jsonl.gz](../../data/mined/hc-1.jsonl.gz); complete request and all-attempt records are not included.
- Reproduction procedure: To reproduce the reported comparison, the mined records now support the reported 40-cell scored cohort and per-arm results under the original KEEP rule; the full Kogen/harness pins, request history, and launch command remain unavailable.

## Limits

Development-only, saturated panel; the contrast also changes builder configuration. No causal attribution to a single implementation change or broad ladder claim follows. The public export has no cell-level rows for this round ID.

No measured superiority claim is made from this page. The source-reported run outcomes and counts are now checked against mined cell records below.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-1`; that export does not establish that no historical run occurred.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/hc-1.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 44 rows (fail 4, pass 40); overall pass rate is 90.9% (40/44) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 44 missing published metadata). Missing counters remain unknown, not zero.
This round also has 44 raw-only or non-public rows; they are kept separate from the published-export denominator.
Historical headline check: published 40/40 scored cells and arm counts 19/20 and 17/20; recomputed 40 cells (hc-ladder-solshape 19/20, hc-ladderso-solshape 17/20). These counts match the published claims.
Separate cells excluded from that headline cohort:
- `hc-direct__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc-direct-hc1-studio-smoke`
- `hc-ladder-solshape-rawfb__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc-ladder-solshape-rawfb-hc1-studio-smoke`
- `hc-ladder-solshape__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc-ladder-solshape-hc1-studio-smoke`
- `hc-ladderso-solshape__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc-ladderso-solshape-hc1-studio-smoke`
