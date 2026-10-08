# R57 Rails Studio smoke lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of NO_OUTCOME, NO_PREREG, SMOKE_ONLY. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**PILOT**

- NO_PREREG — A dated pre-registration is not established in the public record.
- SMOKE_ONLY — The files report two setup-invalid smoke attempts and zero released catalogue cells.
- NO_OUTCOME — No scored efficacy cohort was run.

## Required reproduction metadata

- Kogen commit: [`6747368333e55a694338d32312eb1f49ec2b4813`](https://github.com/KogenAI/kogen-ex/commit/6747368333e55a694338d32312eb1f49ec2b4813), the pin recorded for the Studio smoke attempts.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Task IDs (smoke receipts): `rails-ar-archive-book-access` and `rails-hw-scoped-broadcast`. The planned 17-task catalogue's complete ID list is not recorded.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H87 (round design/status), H88 (intention-to-treat handling), and H89 (reproduction receipts).

Date: 6 October 2026 (source-reported).

Question: Did the R57 Kogen Rails profile pass its Studio setup smokes and release the catalogue comparison?

Design: **Source-reported design/status, not reproducible from public data.** Kogen Rails profile with setup smoke checks; a 17-task catalogue was a potential follow-up, not a completed scored cohort.

**Source-reported status, not reproducible from public data:** two smoke attempts were reported invalid at setup. Zero of 34 catalogue cells were reported as released. This is a blocked setup record, not an efficacy result.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned catalogue = 34 cells; released = 0. Two setup smoke attempts were reported invalid. Started, finished, and officially graded catalogue counts = not recovered. No scored ITT denominator is available.

## Reproduction

- Exact Kogen commit: Kogen pin `67473683` resolves to [`6747368333e55a694338d32312eb1f49ec2b4813`](https://github.com/KogenAI/kogen-ex/commit/6747368333e55a694338d32312eb1f49ec2b4813). The separate harness source revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Kogen profile; exact smoke model and effort receipts are unavailable.
- Task IDs: The smoke receipts name `rails-ar-archive-book-access` and `rails-hw-scoped-broadcast`; the complete 17-task catalogue ID list is not recorded.
- Exact command: The exact setup/smoke and release commands are not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived R57 Studio lane packet `rounds/r57-studio/`; the source reports do not identify a host-relative raw cell-record path. Smoke and release ledgers are not included in this repository.
- Reproduction procedure: To reproduce the status, recover the smoke and 34-slot catalogue manifests, setup logs classified without private diagnostics, full pins, model/effort receipts, task IDs, command, and official disposition records. Those artifacts are absent from the public snapshot.

## Limits

Setup-invalid smokes do not count as model success or failure. The catalogue was not released; no comparison is available.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `r57-studio`; that export does not establish that no historical run occurred.
