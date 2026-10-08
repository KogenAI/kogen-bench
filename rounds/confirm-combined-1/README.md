# Combined kh confirmation

## Status

**INCOMPLETE**

### Why not VALID
- **PARTIAL_CAPTURE:** The retained delivery capture is partial and has no arm identities or official grades.
- **DENOMINATOR_UNVERIFIED:** The reported cohort denominator cannot be matched to retained records.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **INTERIM**

Status reason: the source summary reports a registered internal comparison, but the public capture contains only a partial ungraded delivery set with no arm identity or official grades.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H21–H22**, custom-harness and end-to-end comparison. The tested variants are internal kh changes, not a Kogen-versus-Codex comparison.

## Design and correction status

The research summary describes an internal comparison of combined and individual kh changes. It records that the registered promotion decision did not select the combined variant. The public capture is partial and lacks arm identity and grades, so this page withholds the source-reported outcome and timing totals. It does not establish a general advantage or disadvantage for combining the changes.

## Public capture

The [public capture manifest](public-capture-manifest.csv) contains 16 exact delivery IDs across eight task IDs and two public venues. Every row has an unmapped audit round and a missing arm label. All 16 records have completed stop receipts, but all are ungraded and none joins to an official row in [cells.jsonl](../../results/cells.jsonl). This partial capture cannot reproduce the reported four-arm, 64-cell outcome table. The count is traceable to the manifest and [run-record index](../../results/run-records/index.json).

## Reproduction record

- Harness and Kogen revision: full commit SHAs and the arm-to-revision mapping are missing. Public adapter fingerprints in the manifest are not Git commits.
- Model and effort: captured candidate deliveries record model and effort where present; their relationship to the scored cohort is not verified.
- Task IDs: candidate delivery task IDs are listed in the manifest. The scored task-to-arm assignment is not verified.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not repeat the historical jobs or grading.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl).

## Interpretation

Retain the registered decision as a source-reported disposition, not as a public outcome. Do not pool this internal kh-variant comparison with harness-compare-1 or another round.
