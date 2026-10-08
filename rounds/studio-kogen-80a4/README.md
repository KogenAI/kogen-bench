# Studio Kogen 80a4 smoke lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No dated pre-registration before the first result is established.
- **RAW_EVIDENCE_MISSING:** Raw requests, smoke IDs, and grades are absent.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H65 (recovery and stage visibility), H87 (round design/status), and H89 (reproduction receipts).

Date: 6 October 2026 (source-reported).

Question: Did the three Kogen arms pass smoke checks after correcting shared temporary-directory journal contamination?

Design: **Source-reported design/status, not reproducible from public data.** Smoke/setup lane only, with three arms and two attempts per arm reported. No bulk scored run was reported.

**Source-reported status, not reproducible from public data:** six smoke attempts were reported; the first attempts were reported as passing, and shared temporary-directory journal contamination was repaired. The summary does not provide the final outcome for every attempt. No efficacy claim is made.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Smoke attempts = 6 reported across three arms and two attempts per arm. Exact started, finished, and officially graded counts by identity are not recovered. Scored bulk cells = none reported. No scored ITT denominator is available.

## Reproduction

- Exact Kogen commit: The lane label `80a4` is not a verified full Kogen commit SHA. Exact Kogen and harness source SHAs are unavailable.
- Exact Kogen harness commit: not recovered; the source pin statement above records this limitation.
- Model and effort: Three Kogen arms are reported; exact arm recipes, models, and requested/effective efforts are not recovered.
- Task IDs: Exact smoke task IDs are not recovered.
- Exact command: The exact smoke command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived round packet `rounds/studio-kogen-80a4/`; the source reports do not identify a host-relative raw cell-record path. Raw requests, smoke IDs, and grades are not included in this repository.
- Reproduction procedure: To reproduce the status, recover the three-arm smoke manifest, all attempts and official grades, exact recipes, full pins, per-stage model/effort receipts, task IDs, and command. No public run-record bundle is present.

## Limits

Smoke attempts and a repaired journal issue do not establish scored Build success. The final per-attempt grades and bulk-run status are absent.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `studio-kogen-80a4`; that export does not establish that no historical run occurred.
