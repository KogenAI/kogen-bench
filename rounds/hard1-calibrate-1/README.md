# Hard-task harness calibration

## Status

**INVALID**

### Why not VALID
- **OUTCOME_CLASSIFICATION_UNRESOLVED:** Later review found false blockers, but the affected-cell map is unavailable.
- **OUTCOME_CROSSWALK_MISSING:** Exact-ID scored rows and complete raw grades are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **CONFOUNDED**

Status reason: the source summary reports floor and ceiling tasks, and later grader review found false blockers in some Elixir floor tasks. The exact affected-cell map is unavailable.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H19–H22**, same-model harness comparison and custom-kh parity. This calibration does not establish a general harness winner.

## Design and correction status

The research summary describes a harness calibration on hard tasks. Some tasks were later identified as floor or ceiling cases, and a grader review found false blockers among Elixir floor tasks. The exact mapping from those corrections to this calibration is unresolved. The public capture has no exact calibration IDs or grades, so this page withholds the source-reported outcome totals and makes no comparative claim. Runner completion, if recovered, would not by itself establish task success.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is header-only: no delivery ID could be assigned to this named calibration from the public captures. The public [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl) do not provide an exact-ID grade crosswalk for the reported outcomes.

## Reproduction record

- Harness and Kogen revision: the public evidence does not provide exact per-arm harness or Kogen commit SHAs for this calibration.
- Model and effort: no public exact-ID record binds the model and effort to the scored cohort.
- Task IDs: the exact scored task IDs are not enumerated in the cited public summary.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun or grade the historical cells.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl); no exact calibration IDs are listed in the capture manifest.

## Interpretation

Runner completion must not be read as task success. The reported false-blocker corrections and floor/ceiling tasks make a general superiority claim unsupported; preserve the original and corrected grader states separately if exact cell receipts become available.
