# HC01 small32

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of INCOMPLETE_EXECUTION, RAW_EVIDENCE_PARTIAL (owner stop at 25/32 graded; label DESCRIPTIVE). See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY

STATUS: **INCOMPLETE** (owner stopped at 25/32 graded). Label: **DESCRIPTIVE**. Ceiling: **NOT CONFIRMED**. See [OWNER-STOP.md](OWNER-STOP.md) for the recorded stop and limits.

This page registers the HC01 small32 source bundle. Supporting receipts, patches, captured grader artifacts, and verification metadata are retained in this directory. Grader outputs are opaque and are not reproduced here.

## Lifecycle counts

Planned: 32. Started: 26. Finished: 25. Graded: 25. ITT: unavailable; cell 26 was owner-stopped after starting, and cells 27–32 were never started.

## Reproduction

Kogen commit: unavailable. Harness commit: unavailable. Model and effort: recorded in the source receipts. Task IDs: recorded in the source bundle. Historical execution command: unavailable. Raw records: [mined HC01 records](../../data/mined/hc01-small32.jsonl.gz) and this directory.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/hc01-small32.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 32 rows (fail 11, no_patch 3, pass 11, ungraded 7); overall pass rate is 50.0% (11/22) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 32 missing published metadata). Missing counters remain unknown, not zero.
