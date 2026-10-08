# Studio Kogen smoke lane

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_UNPROVEN:** No dated pre-registration before the first result is established.
- **RAW_EVIDENCE_MISSING:** A complete round-specific request and grade bundle is absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H65 (recovery and stage visibility), H87 (round design/status), and H89 (reproduction receipts).

Date: 5–6 October 2026 (source-reported).

Question: Did the initial and retry smoke checks admit the provided and shaped Intent Kogen paths for a larger run?

Design: **Source-reported design/status, not reproducible from public data.** Smoke/setup lane only; no bulk scored comparison was reported. The public summary does not recover the full arm manifest or per-attempt cell IDs.

**Source-reported status, not reproducible from public data:** four original/retry smoke attempts were reported. A provided-Intent retry passed; a shaped-Intent retry was invalid after provider overload. No bulk scored cells were reported. These setup checks are not efficacy evidence.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Original/retry smoke attempts = 4 reported; exact planned, started, finished, and officially graded smoke counts by identity are not recovered. Scored bulk cells = none reported. Scored ITT denominator = not applicable to a bulk comparison; no public cell-level partition exists.

## Reproduction

- Exact Kogen commit: No exact Kogen commit SHA or harness source SHA is reported for this lane.
- Exact Kogen harness commit: not recovered; the source pin statement above records this limitation.
- Model and effort: The lane used Kogen; exact model and requested/effective effort for each smoke are not recovered.
- Task IDs: Provided and shaped Intent labels are reported; exact task IDs are not recovered.
- Exact command: The exact smoke command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived round packet `rounds/studio-kogen/`; the source reports do not identify a host-relative raw cell-record path. Raw requests, smoke IDs, and grades are not included in this repository.
- Reproduction procedure: To reproduce the status, recover the original/retry smoke manifests, all attempts and official smoke grades, exact Kogen/harness pins, model/effort receipts, task IDs, and command. No such public record bundle is present.

## Limits

Smoke admission and one provider-overload invalid do not estimate Build success. No bulk cohort or official scored comparison is established.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `studio-kogen`; that export does not establish that no historical run occurred.
