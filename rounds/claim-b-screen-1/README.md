# Claim B transport screen

## Status

**INVALID**

### Why not VALID
- **OUTCOME_CLASSIFICATION_INVALID:** Transport interruptions were classified as model failures.
- **OUTCOME_CROSSWALK_MISSING:** Exact affected cell IDs and corrected grades are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **CONFOUNDED**

Status reason: the research summary attributes several kh failures to a transport interruption that the runner classified as a model failure. This screen cannot support an efficacy comparison.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H21–H22**, asking whether a custom kh harness can match another harness and whether an end-to-end route changes that comparison. This screen did not establish either proposition.

## Design and correction status

The research summary records a harness comparison that was confounded by a transport interruption. The runner classified some transport failures as model failures. The exact cell IDs and corrected grades are not in the public capture, so this page withholds the source-reported outcome totals and does not establish Claim B.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is header-only: no delivery ID could be assigned to this named screen from the public captures. The public [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl) therefore contain no exact-ID grade crosswalk for the reported outcomes.

## Reproduction record

- Harness and Kogen revision: a full commit SHA is not bound to the scored cells in the public record. The captured source metadata does not establish the historical harness revision.
- Model and effort: no public exact-ID record binds the model and effort to the scored cells.
- Task IDs: the exact scored task IDs are not enumerated in the cited public record.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun or grade the historical cells.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl); no exact screen IDs are present in the capture manifest.

## Interpretation

The transport correction changes the meaning of the initial failure tally. Preserve the patch and autonomous columns separately, and do not treat the reported 2/6 versus 5/6 patch result as model evidence.
