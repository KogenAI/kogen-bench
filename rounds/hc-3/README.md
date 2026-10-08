# Studio hill climb iteration 3

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
- Raw records: safe per-cell records and joined official grades are in [data/mined/hc-3.jsonl.gz](../../data/mined/hc-3.jsonl.gz); per-arm outcomes, token totals, wall medians, and comparisons are in [recomputed.json](recomputed.json). Request logs and transcripts are not included.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H75 (difficulty ladder) and H136 (ladder variants).

Date: 6 October 2026 (source-reported).

Question: Do generated edge tests and their repair loop improve the current ladder on the revised development panel?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes a ten-task v2 panel with two repetitions per scored arm and a separate v1 guard panel.

**Published source-reported headline, now checked against mined rows below:** 60/60 scored and guard cells were reported as officially graded. The plain mixed Luna/Sol ladder scored 16/20; ladder plus generated edge tests scored 13/20 and was discarded. The separate v1 guards were reported as 7/10 for the ladder and 10/10 for edge. The mined store also contains four smoke grades and a separate ten-cell `allin-diverse-edge` arm; these cells are listed separately below. The edge arm generated 197 tests, kept 50, dropped 147, triggered four repairs, selected zero repaired candidates, and produced zero candidate rerankings. These diagnostics do not show that all probe designs fail.

## Lifecycle counts

**Source-reported scored lifecycle:** Planned = 60 cells (40 v2 decision cells plus 20 v1 guards). Started = not recovered. Finished = not separately recorded. The mined store confirms 60 scored/guard grades and separately identifies four smokes plus ten additional `allin-diverse-edge` grades. ITT denominator and disposition partition = not recovered; keep guards out of promotion.

## Reproduction

- Exact Kogen commit: Kogen scored revision [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Mixed Luna/Sol ladder; the edge arm adds a Sol edge writer and repair path. Exact per-stage requested and effective model/effort receipts are unavailable.
- Task IDs: Same ten-task v2 panel as iteration 2 plus separate v1 guards; `elx-12` is named in the source as the task where the edge arm lost both repetitions. The full task-ID list is not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary names iteration-3 result and decision records. Safe per-cell manifests, official grades, usage/wall fields, and patch hashes are now in [data/mined/hc-3.jsonl.gz](../../data/mined/hc-3.jsonl.gz); complete request and all-attempt records are not included.
- Reproduction procedure: To reproduce the reported result, the mined records now support the reported v2 and guard counts; a separate ten-cell arm is retained as additional evidence. Full request/all-attempt history, the retained edge-test configuration, and the launch command remain unavailable.

## Limits

The v2 panel is shared with iteration 2; the guards are not promotion cells. Mined rows now provide observed cell outcomes and wall values; the complete timing ledger and stop-cause receipts remain unavailable. The result is an exploratory development diagnostic.

No measured superiority claim is made from this page. The source-reported run outcomes and counts are now checked against mined cell records below.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-3`; that export does not establish that no historical run occurred.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/hc-3.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 74 rows (fail 18, pass 56); overall pass rate is 75.7% (56/74) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 74 missing published metadata). Missing counters remain unknown, not zero.
This round also has 74 raw-only or non-public rows; they are kept separate from the published-export denominator.
Historical headline check: published 60 scored/guard cells, v2 counts 16/20 and 13/20, and guard counts 7/10 and 10/10; recomputed v2 (hc3-ladder 16/20, hc3-ladder-edge 13/20) and guards (hc3-ladder 7/10, hc3-ladder-edge 10/10). These counts match the published claims.
Separate cells excluded from that headline cohort:
- `hc3-diverse-edge__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc3-diverse-edge-hc3-studio-smoke`
- `hc3-diverse__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc3-diverse-hc3-studio-smoke`
- `hc3-ladder-edge__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc3-ladder-edge-hc3-studio-smoke`
- `hc3-ladder__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-hc3-ladder-hc3-studio-smoke`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-07-cli-stats__r1-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-07-cli-stats__r2-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-12-retry-api-deprecation__r1-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-12-retry-api-deprecation__r2-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-port-board-publish-unpublish-public-boundary__r1-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-port-board-publish-unpublish-public-boundary__r2-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-port-erase-account__r1-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__elx-port-erase-account__r2-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__syn-31-inbound-email-webhook__r1-allin-diverse-edge-allin-studio`
- `hc3-diverse-edge__gpt-6-luna__max__default__syn-31-inbound-email-webhook__r2-allin-diverse-edge-allin-studio`
