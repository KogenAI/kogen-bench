# Frozen offline reviewer comparison

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of INCOMPLETE_EXECUTION, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **INCOMPLETE_EXECUTION:** The offline comparison stopped at its budget limit.
- **RAW_EVIDENCE_MISSING:** Patch-level outputs and the cost ledger are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Partial offline comparison stopped at its budget limit; no live Build efficacy claim. Study counts, rates, times and costs in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The patch-level review ledger is not included in this public page.

## Scope and reported result

The comparison applied tool-less and executable final-patch review to a frozen set of 80 patches. The source report says the study stopped with 63 of 80 paired first-run patches complete: 31 hidden-pass and 32 hidden-fail patches. It identifies Sol high as the reviewer model/effort for both variants.

For tool-less review, the reported precision was 19/23 (82.6%), recall 19/32 (59.4%), and false vetoes 4/31 (12.9%); mean cost was $0.0288 and mean time was 31.1 seconds. For executable review, the reported precision was 21/29 (72.4%), recall 21/32 (65.6%), and false vetoes 8/31 (25.8%); mean cost was $0.0776 and mean time was 104.7 seconds. The source describes a $10 budget limit and a final ledger of $9.5511. The executable variant had higher reported recall and twice as many false vetoes. The partial sample and overlapping uncertainty do not establish a net causal review benefit.

An earlier interim comparison is superseded by this budget-stop report. This offline review did not test a prospective repair loop.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers offline review calls on saved patches, not a live Build cohort. The planned patch set and completed paired reviews are separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No live Kogen execution is described. Source revisions for the frozen patches are not supplied in the public input. |
| Model and effort | Sol high is source-reported for both review variants; exact model build/version is not supplied. |
| Task IDs | The planned patch set and completed patch IDs are not supplied in a sanitized public crosswalk. |
| Command | The exact review command is not recovered from the supplied public input. |
| Raw records | The source inventory names `OFFLINE-REVIEW3.md` and an `offline-review3` record set. The patch-level outputs and cost ledger are not included in the public data tree. |

Until the patch IDs and review records are published, all figures remain source-reported, not reproducible from public data.
