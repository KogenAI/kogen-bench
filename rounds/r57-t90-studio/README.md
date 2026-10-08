# R57 T90 Studio retry lane


## Status

**PILOT**

Why not VALID:
- NO_PREREG — A dated pre-registration is not established in the public record.
- SMOKE_ONLY — One setup smoke passed and the other was invalid; no catalogue cells were released.
- NO_OUTCOME — No scored efficacy comparison exists.

## Required reproduction metadata

- Kogen commit: [`8c705841d66023dcc7025dba9a24208afd794a02`](https://github.com/KogenAI/kogen-ex/commit/8c705841d66023dcc7025dba9a24208afd794a02), the T90 retry pin.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Task IDs (smoke receipts): `rails-ar-archive-book-access` and `rails-hw-scoped-broadcast`. The planned 17-task catalogue's complete ID list is not recorded.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H87 (round design/status), H88 (intention-to-treat handling), and H89 (reproduction receipts).

Date: 6 October 2026 (source-reported).

Question: Did the T90 retry pass both representative setup smokes and release the catalogue cohort?

Design: **Source-reported design/status, not reproducible from public data.** Retry lane with archive and scoped-broadcast smoke labels; the remaining catalogue was not released.

**Source-reported status, not reproducible from public data:** the archive smoke passed and the broadcast smoke was invalid. Zero of 34 catalogue cells were reported as released. No efficacy comparison is available.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned catalogue = 34 cells; released = 0. Two smoke outcomes are reported separately. Started, finished, and officially graded catalogue counts = not recovered. No scored ITT denominator is available.

## Reproduction

- Exact Kogen commit: Kogen pin `8c705841` resolves to [`8c705841d66023dcc7025dba9a24208afd794a02`](https://github.com/KogenAI/kogen-ex/commit/8c705841d66023dcc7025dba9a24208afd794a02). The separate harness source revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Kogen retry path; exact model, effort, and per-stage roles are unavailable.
- Task IDs: The smoke receipts name `rails-ar-archive-book-access` and `rails-hw-scoped-broadcast`; the complete 17-task catalogue ID list is not recorded.
- Exact command: The exact retry and smoke commands are not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived R57 T90 Studio lane packet `rounds/r57-t90-studio/`; the source reports do not identify a host-relative raw cell-record path. Smoke and release ledgers are not included in this repository.
- Reproduction procedure: To reproduce the status, recover the retry manifest, both smoke IDs and outcomes, full pins, model/effort receipts, exact task IDs, command, and official disposition for the planned catalogue. Those artifacts are absent from the public snapshot.

## Limits

One smoke pass does not validate the other smoke path. An invalid setup smoke and unreleased catalogue supply no scored comparison.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `r57-t90-studio`; that export does not establish that no historical run occurred.
