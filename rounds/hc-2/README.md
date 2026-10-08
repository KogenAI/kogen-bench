# Studio hill climb iteration 2

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
- Raw records: safe per-cell records and joined official grades are in [data/mined/hc-2.jsonl.gz](../../data/mined/hc-2.jsonl.gz); per-arm outcomes, token totals, wall medians, and comparisons are in [recomputed.json](recomputed.json). Request logs and transcripts are not included.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H75 (difficulty ladder) and H136 (ladder diversity).

Date: 6 October 2026 (source-reported).

Question: Does ladder diversity or a shaping-free direct-shell floor improve success over the current Kogen ladder on the revised development panel?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes a ten-task v2 panel with two repetitions per arm and separate v1 guard cells. The guard observations are not part of the promotion comparison.

**Published source-reported headline, now checked against mined rows below:** 90/90 scored and guard cells were reported as officially graded. On v2, the mixed Luna/Sol ladder scored 16/20; ladder-diverse scored 13/20; the shaping-free direct-shell floor scored 13/20. Both challengers were discarded. Separate v1 guards were reported as 9/10, 10/10, and 7/10 respectively and were excluded from promotion. The mined store contains five additional smoke grades, listed separately below.

## Lifecycle counts

**Source-reported scored lifecycle:** Planned = 90 cells (60 v2 decision cells plus 30 v1 guards). Started = not recovered. Finished = not separately recorded. The mined store confirms 90 scored/guard grades and separates five smoke grades. ITT denominator and disposition partition = not recovered; keep guards out of promotion.

## Reproduction

- Exact Kogen commit: Kogen pin `c056dccb` resolves to [`c056dccb9ee7534490102c8ae316122983b6f17b`](https://github.com/KogenAI/kogen-ex/commit/c056dccb9ee7534490102c8ae316122983b6f17b).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Reported labels are mixed Luna/Sol ladder, ladder-diverse with a raw Sol-medium sibling, and a Luna-max raw development floor. Exact per-stage requested/effective models and effort receipts are unavailable.
- Task IDs: Ten-task v2 panel plus a separate v1 guard panel reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary names iteration-2 result and decision records. Safe per-cell manifests, official grades, usage/wall fields, and patch hashes are now in [data/mined/hc-2.jsonl.gz](../../data/mined/hc-2.jsonl.gz); complete request and all-attempt records are not included.
- Reproduction procedure: To reproduce the reported comparison, the mined records now support v2 and guard outcome counts separately under the original KEEP rule; full request/all-attempt history, complete environment receipts, and the launch command remain unavailable.

## Limits

The v2 panel is reused in iteration 3 and is not an independent replication. Guards are separated from promotion. These small, adaptive development comparisons do not establish benchmark qualification.

No measured superiority claim is made from this page. The source-reported run outcomes and counts are now checked against mined cell records below.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-2`; that export does not establish that no historical run occurred.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/hc-2.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 95 rows (fail 24, pass 71); overall pass rate is 74.7% (71/95) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 95 missing published metadata). Missing counters remain unknown, not zero.
This round also has 95 raw-only or non-public rows; they are kept separate from the published-export denominator.
Historical headline check: published 90 scored/guard cells, v2 counts 16/20, 13/20, 13/20, and guard counts 9/10, 10/10, 7/10; recomputed v2 (hc2-floor 13/20, hc2-ladder 16/20, hc2-ladder-diverse 13/20) and guards (hc2-floor 7/10, hc2-ladder 9/10, hc2-ladder-diverse 10/10). These counts match the published claims.
Separate cells excluded from that headline cohort:
- `codex__gpt-6-luna__max__default__elx-port-board-publish-unpublish-public-boundary__r1-hc2-port-codex-luna-max-hc2-port-studio-smoke`
- `codex__gpt-6-luna__max__default__elx-port-erase-account__r1-hc2-port-codex-luna-max-hc2-port-studio-smoke`
- `hc2-floor__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc2-floor-hc2-studio-smoke`
- `hc2-ladder-diverse__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc2-ladder-diverse-hc2-studio-smoke`
- `hc2-ladder__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc2-ladder-hc2-studio-smoke`
