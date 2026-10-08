# Studio hill climb iteration 4

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

Related hypotheses: H75 (difficulty ladder), H136 (ladder variants), and H138 (matched model/effort baselines).

Date: 6 October 2026 (source-reported).

Question: Can shaping and planning effort be varied independently to find a cheaper ladder configuration without losing success?

Design: **Source-reported design/status, not reproducible from public data.** Exploratory Studio status record. The source summary describes a proposed ladder with Sol high, medium, or xhigh shaping/planning coupled to a Luna-max builder, using v2 discriminators and guards. The summary notes later planner-overlay instrumentation, but no completed decision record.

**Source-reported status, not reproducible from public data:** a duplicate trim was reported to avoid 47 unstarted cells; 43 cells were described as expected to remain, including nine already-started diagnostics; six Studio cells were owner-stopped. Smokes and planner-overlay instrumentation occurred. No closed scored denominator or outcome was recovered, so no efficacy result is reported.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned = not recovered. Started = not recovered; the reported 43 expected retained cells included nine already-started diagnostics, but this is not a complete start count. Finished = not recovered. Officially graded = not recovered. ITT denominator = not recovered. The separate status summary reports 47 unstarted cells avoided and six owner-stopped Studio cells.

## Reproduction

- Exact Kogen commit: Kogen pin `cde7a380` resolves to [`cde7a380455e9793cb1fc8315791bc9beffb863b`](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b).
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Proposed Sol high/medium/xhigh shaping and planning with Luna-max builder. Whether shaping and planning were separated in every executed request is not verified; effective per-cell models and effort are unavailable.
- Task IDs: v2 discriminator and guard sets reported; exact task IDs are not recovered.
- Exact command: The exact launch command is not recovered. This page is a status record and is not independently rerunnable from the public snapshot.
- Raw record location: Studio result family identified in the source summary; its host filesystem path is not published; the source summary identifies status, brief, smoke, and variant records, but no final iteration result. The cell manifest and official grade rows are not in this repository.
- Reproduction procedure: A result cannot be reproduced until the final cell-selection manifest, per-cell attempts and grades, planner-overlay receipt, full pins, and launch command are recovered. Keep unstarted, started, smoke, stopped, and graded identities distinct.

## Limits

The expected retained count, started diagnostics, and owner-stopped cells are different lifecycle categories and are not a final scored n. No pass/fail rate or winner can be inferred.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `hc-4`; that export does not establish that no historical run occurred.
