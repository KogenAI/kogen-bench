# Studio hill climb iteration 1

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

Date: 5 October 2026 (source-reported).

Question: Does a Sol-shaped Kogen ladder improve the development panel over a shorter ladder with a Sol-medium builder?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio development diagnostic. The source summary describes two arms on a ten-task development set with two repetitions per arm. Exact task IDs and the full arm manifest are not in the public record.

**Source-reported, not reproducible from public data:** 40/40 cells were officially graded. The mixed Luna/Sol ladder with Sol-high shaping scored 19/20; the Sol-medium-builder challenger with Sol-high support scored 17/20 and was discarded under the reported KEEP rule. The control was already saturated on this development panel; these results do not qualify a benchmark advantage.

## Lifecycle counts

**Source-reported, not reproducible from public data:** Planned = 40 cells. Started = not recovered. Finished = not separately recorded. Officially graded = 40 cells. ITT denominator and disposition partition = not recovered; the reported graded denominator is not an ITT reconstruction.

## Reproduction

- Exact Kogen commit: Kogen pin `1d567772` resolves to [`1d567772446a66ea75fd04ae0e9c514b835f2d20`](https://github.com/KogenAI/kogen-ex/commit/1d567772446a66ea75fd04ae0e9c514b835f2d20).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Control: mixed Luna/Sol ladder with Sol-high shaping. Challenger: Sol-medium builder with Sol-high support. Exact per-stage requested and effective model/effort receipts are unavailable.
- Task IDs: Ten-task v1 development panel reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary also identifies an archived iteration-1 report. The cell manifest, request records, and official grade rows have not been transferred into this repository.
- Reproduction procedure: To reproduce the reported comparison, recover the exact manifest and all-attempt/official-grade rows from the Studio result family, add the full Kogen and harness pins and launch command, then recompute the two arms by task under the original KEEP rule. Those inputs are not in the public snapshot.

## Limits

Development-only, saturated panel; the contrast also changes builder configuration. No causal attribution to a single implementation change or broad ladder claim follows. The public export has no cell-level rows for this round ID.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-1`; that export does not establish that no historical run occurred.
