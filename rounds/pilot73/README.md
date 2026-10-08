# pilot73 — recovered shaper source round

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of NO_PUBLIC_CELLS, PRE_REGISTRATION_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.

## Status

STATUS: **DESCRIPTIVE**

### Why not VALID

- **NO_PUBLIC_CELLS:** None of the recovered source cell IDs occur in the public grade export.
- **DESCRIPTIVE:** The recovered source is an exploratory shaper pilot, separate from the registered r73 scored phase.
- **PRE_REGISTRATION_MISSING:** No pre-registration for this recovered source pilot is present in the public record.

## Required reproduction metadata

- Kogen commit: not recorded in the recovered source.
- Harness commit: not recorded as a Git commit in the recovered source.
- Model and effort: mined manifests report `gpt-6-luna`, `max`; this does not establish the registered r73 configuration.
- Task IDs: `elx-05-cache-single-flight`, `syn-13-bug-empty-filter-crash`, and `syn-14-bug-sla-business-hours` appear in the recovered cell records; mapping to the registered r73 plan is not established.
- Historical execution command: not recorded in the recovered source.
- Raw records: [mined public-safe cell records](../../data/mined/pilot73.jsonl.gz); source transcripts, rollouts, and request logs are excluded.

## Recovered source scope

The recovered probe store contains 25 raw rows across the `pilot-shaper-luna` and `pilot-shaper-sol` labels. These are observed source records, not a recovered intention-to-treat denominator or a public grade-export cohort. The descriptive source tag `pilot73` is registered separately here because it is not the registered r73 scored phase, whose page records an executed scored n of zero.

Published token metadata is absent for all 25 rows. Their manifest usage counters are retained as raw source observations and are not substitutes for a missing published token total.

| Lifecycle population | Count | Basis |
|---|---:|---|
| Planned | Unknown | No complete planned-cell list is recovered. |
| Started | Unknown | Starts are not separately recorded. |
| Finished | Unknown | Finished attempts are not separately recorded. |
| Graded count | 25 | Raw source records contain 25 grade entries; none appear in the public grade export. |
| ITT denominator | Unknown | No evidence-backed inclusion/exclusion partition is recovered. |

## Limits

This page makes no comparative efficacy claim and does not update any published r73 result. The observed source tag cannot establish that a planned r73 cell ran or that the recovered rows belong to the registered r73 scored phase.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/pilot73.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 25 rows (fail 1, pass 24); overall pass rate is 96.0% (24/25) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 25 missing published metadata). Missing counters remain unknown, not zero.
This round also has 25 raw-only or non-public rows; they are kept separate from the published-export denominator.
