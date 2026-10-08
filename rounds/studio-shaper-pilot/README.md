# Studio shaper pilot

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of NO_SCORED_CELLS, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**PILOT**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No dated pre-registration before the first result is established.
- **RAW_EVIDENCE_MISSING:** Smoke receipts and official grade rows are absent.
- **NO_SCORED_CELLS:** The pilot did not release scored cells.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H65 (recovery and stage visibility), H87 (round design/status), and H88 (intention-to-treat handling).

Date: 5–6 October 2026 (source-reported).

Question: Did the Sol and Luna shaper smoke paths pass setup and release the planned scored comparison?

Design: **Source-reported design/status, not reproducible from public data.** Smoke/setup pilot with Sol and Luna shaper paths. The public summary does not recover exact task IDs, full command, or the complete planned manifest.

**Source-reported status, not reproducible from public data:** the Sol smoke passed; the Luna smoke was invalid with `control_apply` after a Kogen repair cap. Zero of 24 planned scored cells were reported as released. These smoke outcomes do not estimate comparative efficacy.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned scored cells = 24; released = 0. Started, finished, and officially graded scored counts are not independently reconciled. Smoke outcome labels are reported separately; no scored ITT denominator is available.

## Reproduction

- Exact Kogen commit: No exact Kogen commit SHA or harness source SHA is reported for this pilot.
- Exact Kogen harness commit: not recovered; the source pin statement above records this limitation.
- Model and effort: Sol and Luna are the reported smoke model labels; exact model IDs, requested/effective effort, and per-stage roles are unavailable.
- Task IDs: Exact task IDs are not recovered.
- Exact command: The exact smoke or dispatch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived round packet `rounds/studio-shaper-pilot/`; the source reports do not identify a host-relative raw cell-record path. Smoke receipts and official grade rows are not included in this repository.
- Reproduction procedure: To reproduce the status, recover the smoke and planned-cell manifests, all attempts, official grades and ITT decisions, exact pins, model/effort receipts, task IDs, and dispatch command. Those artifacts are absent from the public snapshot.

## Limits

The pilot did not release scored cells. The reported invalid is a setup/control state and must not be counted as a task failure or success without the official cell-level ITT record.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `studio-shaper-pilot`; that export does not establish that no historical run occurred.
