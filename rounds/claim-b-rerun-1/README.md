# Claim B worker rerun

## Status

**INVALID**

### Why not VALID
- **CONFOUNDED_ASSIGNMENT:** Host is assigned by repetition, confounding the reported comparison.
- **OUTCOME_CROSSWALK_MISSING:** No exact-ID grade crosswalk or complete raw grade bundle is present.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **CONFOUNDED**

Status reason: the research summary reports a host-by-repetition assignment, while the public snapshot contains no exact-ID grade crosswalk. The result remains a source-reported replication, not a verified comparison.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H21–H22**, custom-harness parity and end-to-end comparison. The reported rerun does not show a retry-policy benefit.

## Design and correction status

The research summary describes a worker rerun after the transport correction, with a setup amendment and a retry variant. It identifies host as repetition, which limits interpretation. The public capture contains no exact IDs for this rerun or its setup failures, so this page withholds the source-reported outcome totals and does not verify a retry-policy benefit.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is header-only: no delivery ID could be assigned to this named rerun. The public [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl) do not provide an exact-ID grade crosswalk for these reported outcomes.

## Reproduction record

- Harness and Kogen revision: full commit SHAs are not bound to the scored cells in the public record.
- Model and effort: no public exact-ID record binds the model and effort to this scored cohort.
- Task IDs: the exact scored task IDs are not enumerated in the cited public summary.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun or grade the historical cells.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl); no exact rerun IDs are present in the capture manifest.

## Interpretation

Keep this worker rerun separate from the transport-confounded Studio screen. The source-reported equal scores do not verify the retry fix, because the public grade rows and full cohort assignment are missing and host is confounded with repetition.
