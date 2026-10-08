# Offline contract audit

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_ANALYSIS:** This is an offline blinded replay without a repair or Build rerun.
- **RAW_EVIDENCE_MISSING:** The contract-level raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline blinded replay; no repair or Build rerun. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The contract-level audit records are not included in this public page.

## Scope and reported result

The audit compared Sol medium and Luna max on five known R48 false accepts plus passing-contract controls. The source report records 40 audits over 20 recoverable contracts. Sol medium identified the exact defect in 1 of 5 cases; Luna max identified 0 of 5. On passing contracts, the audit flagged 10 of 10 for Sol medium and 6 of 10 for Luna max. The report gives approximate per-audit costs of $0.049–$0.050 for Sol medium and $0.0042–$0.0044 for Luna max.

The controls measure a flagging/noise proxy. Because no repair or Build rerun was performed, the result does not show that contract review prevents false acceptance or improves live completion.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers an offline audit of saved contracts, not a live Build cohort. Audit calls and contract cases are separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No live harness or Kogen execution is described. Revisions for the historical R48 contracts are not listed in the supplied public input. |
| Model and effort | Sol medium and Luna max are source-reported; exact model builds are not supplied. |
| Task IDs | Exact R48 false-accept and control IDs are not supplied in a public crosswalk. |
| Command | The exact audit command is not recovered from the supplied public input. |
| Raw records | The source inventory names `OFFLINE-CONTRACT-AUDIT.md` and an `offline-contract-audit` record set; the contract-level raw records are not included in the public data tree. |

Until the contract IDs and audit records are published, all figures remain source-reported, not reproducible from public data.
