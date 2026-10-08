# Studio hill climb iteration 3

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No dated pre-registration before the first result is established.
- **RAW_EVIDENCE_MISSING:** The round-specific request and grade bundle is absent.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H75 (difficulty ladder) and H136 (ladder variants).

Date: 6 October 2026 (source-reported).

Question: Do generated edge tests and their repair loop improve the current ladder on the revised development panel?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes a ten-task v2 panel with two repetitions per scored arm and a separate v1 guard panel.

**Source-reported, not reproducible from public data:** 60/60 scored and guard cells were reported as officially graded. The plain mixed Luna/Sol ladder scored 16/20; ladder plus generated edge tests scored 13/20 and was discarded. The separate v1 guards were reported as 7/10 for the ladder and 10/10 for edge. The edge arm generated 197 tests, kept 50, dropped 147, triggered four repairs, selected zero repaired candidates, and produced zero candidate rerankings. These diagnostics do not show that all probe designs fail.

## Lifecycle counts

**Source-reported, not reproducible from public data:** Planned = 60 cells (40 v2 decision cells plus 20 v1 guards). Started = not recovered. Finished = not separately recorded. Officially graded = 60 scored/guard cells. ITT denominator and disposition partition = not recovered; keep guards out of promotion.

## Reproduction

- Exact Kogen commit: Kogen scored revision [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Mixed Luna/Sol ladder; the edge arm adds a Sol edge writer and repair path. Exact per-stage requested and effective model/effort receipts are unavailable.
- Task IDs: Same ten-task v2 panel as iteration 2 plus separate v1 guards; `elx-12` is named in the source as the task where the edge arm lost both repetitions. The full task-ID list is not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary names iteration-3 result and decision records. The cell manifest, request records, and official grade rows have not been transferred into this repository.
- Reproduction procedure: To reproduce the reported result, recover the exact v2/guard manifests, retained edge-test configuration, all attempts and official grades, plus full harness/Kogen pins and launch command; then calculate v2 scores separately from guard and candidate-repair diagnostics. Those inputs are not in the public snapshot.

## Limits

The v2 panel is shared with iteration 2; the guards are not promotion cells. The source report identifies an added timeout stop class and slower wall distribution for the edge arm, but no public cell rows or timing ledger are available here. The result is an exploratory development diagnostic.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-3`; that export does not establish that no historical run occurred.
