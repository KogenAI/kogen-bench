# Four-harness comparison

## Status

**DESCRIPTIVE**

### Why not VALID
- **OUTCOME_CROSSWALK_MISSING:** The reported score table has no exact-ID public grade crosswalk.
- **TASK_VALIDITY_UNRESOLVED:** Later review identified task-set defects without an affected-cell map.
- **RAW_EVIDENCE_MISSING:** A complete raw request and grade bundle is absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **INTERIM**

Status reason: the reported scored outcome table has no exact-ID public grade crosswalk. Later grader review also identified defects in the surrounding task set, but the public record does not establish which reported cells change.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H19–H22** and **H28**, covering same-model harness comparison, custom-kh parity and harness maintenance tradeoffs. The result is not a verified winner.

## Design and correction status

The research summary describes a scored comparison across four harnesses. Later grader review identified defects in the broader task set, but the public evidence does not map corrected grades to this comparison. The exact cell IDs and outcome rows are absent from the public capture, so this page withholds source-reported outcome totals and makes no comparative claim.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is header-only: no delivery ID could be assigned to this named comparison from the public captures. The public [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl) contain no exact-ID grade crosswalk for the reported 80-cell table.

## Reproduction record

- Harness and Kogen revision: full commit SHAs are not bound to the scored cells in the public record.
- Model and effort: no public exact-ID record binds the model and effort to the scored cohort.
- Task IDs: the exact scored task IDs are not enumerated in the cited public record.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun or grade the historical comparison.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl); no exact comparison IDs are listed in the capture manifest.

## Interpretation

Keep this result separate from the three-task harness pick, the Claim B screen and the hard1 calibration. Saturated tasks, the small discriminating subset, unresolved grader corrections and missing exact grades prevent a release claim of general harness superiority.
