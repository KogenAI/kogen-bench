# September kh comparison

## Status

**INVALID**

### Why not VALID
- **COHORT_MISMATCH:** The public candidate deliveries do not reconcile to the reported three-task comparison.
- **OUTCOME_GRADES_MISSING:** The retained candidate records are ungraded and have no arm mapping.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **INTERIM**

Status reason: the public delivery capture has no official grades for candidate records, and its task/venue coverage does not reconcile to the small comparison described in the research summary.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H21** (custom kh parity), **H23** (Elixir kh versus Rust khr), and **H26–H28** (Claude harness and wrapper questions). None is resolved by this page.

## Design and correction status

The research summary describes exploratory harness and wrapper comparisons. A path-check defect led to a grading correction for the Sonnet comparison; the corrected grade rows are not in the public capture. Rust khr was not run. Because the public candidate records do not reconcile to the reported small Studio cohort, this page withholds the source-reported outcome totals and makes no comparative claim.

## Public capture

The [public capture manifest](public-capture-manifest.csv) contains 33 records with harness label kh-compare: 32 exact delivery IDs and one captured handle that is not a unique cell ID. The records span 16 task IDs and two public venues, unlike the source summary's three-task Studio screen; they are retained as candidate records and are not assigned to that reported cohort. Every row has an unmapped audit round and a missing arm label. All 33 have completed stop receipts, but all are ungraded and none joins to an official row in [cells.jsonl](../../results/cells.jsonl). The manifest and [run-record index](../../results/run-records/index.json) are the public evidence for those delivery counts.

## Reproduction record

- Harness and Kogen revision: a full commit SHA is not available. The public adapter fingerprint in the manifest is not a Git commit. The exact revision for the scored comparison is missing.
- Model and effort: the public candidate records retain per-delivery model and effort where captured. The exact model and effort assignment for the scored comparison is missing.
- Task IDs: the candidate delivery IDs and task IDs are listed in the manifest. The three scored task IDs from the source summary are not recoverable from the public record.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun the historical jobs or grading.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl).

## Interpretation

Keep the corrected Sonnet grading separate from the earlier artifact. The one-repetition exploratory comparisons and the unreconciled public capture cannot establish harness superiority. The unrun Rust implementation has no outcome.
