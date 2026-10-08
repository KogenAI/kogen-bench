# Studio hill climb iteration 2

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

Related hypotheses: H75 (difficulty ladder) and H136 (ladder diversity).

Date: 6 October 2026 (source-reported).

Question: Does ladder diversity or a shaping-free direct-shell floor improve success over the current Kogen ladder on the revised development panel?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes a ten-task v2 panel with two repetitions per arm and separate v1 guard cells. The guard observations are not part of the promotion comparison.

**Source-reported, not reproducible from public data:** 90/90 scored and guard cells were reported as officially graded. On v2, the mixed Luna/Sol ladder scored 16/20; ladder-diverse scored 13/20; the shaping-free direct-shell floor scored 13/20. Both challengers were discarded. Separate v1 guards were reported as 9/10, 10/10, and 7/10 respectively and were excluded from promotion.

## Lifecycle counts

**Source-reported, not reproducible from public data:** Planned = 90 cells (60 v2 decision cells plus 30 v1 guards). Started = not recovered. Finished = not separately recorded. Officially graded = 90 scored/guard cells. ITT denominator and disposition partition = not recovered; keep guards out of promotion.

## Reproduction

- Exact Kogen commit: Kogen pin `c056dccb` resolves to [`c056dccb9ee7534490102c8ae316122983b6f17b`](https://github.com/KogenAI/kogen-ex/commit/c056dccb9ee7534490102c8ae316122983b6f17b).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Reported labels are mixed Luna/Sol ladder, ladder-diverse with a raw Sol-medium sibling, and a Luna-max raw development floor. Exact per-stage requested/effective models and effort receipts are unavailable.
- Task IDs: Ten-task v2 panel plus a separate v1 guard panel reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary names iteration-2 result and decision records. The cell manifest, request records, and official grade rows have not been transferred into this repository.
- Reproduction procedure: To reproduce the reported comparison, recover the exact v2 and guard manifests plus attempt and official-grade ledgers, attach full harness/Kogen pins and the launch command, and recompute v2 outcomes separately from guards under the original KEEP rule. Those inputs are not in the public snapshot.

## Limits

The v2 panel is reused in iteration 3 and is not an independent replication. Guards are separated from promotion. These small, adaptive development comparisons do not establish benchmark qualification.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-2`; that export does not establish that no historical run occurred.
