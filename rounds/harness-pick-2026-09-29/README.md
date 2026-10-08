# September harness pick

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered decision rule predating the first result is documented.
- **OUTCOME_CROSSWALK_MISSING:** Surviving delivery records are ungraded and do not identify an official outcome cohort.
- **RAW_EVIDENCE_MISSING:** The scored source rows and complete raw bundle are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **INTERIM**

Status reason: the surviving public delivery records are ungraded and do not resolve to an official outcome cohort. The historical comparison below is exploratory and does not support a harness winner.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H19** (Pi versus Codex on matched models) and **H20** (cross-harness comparison). These questions remain open.

## Design and correction status

The research summary describes an early multi-harness screen on development tasks. A faulty grader check was later excluded, and the early harness selection was treated as low-confidence and superseded. The exact scored-cell IDs and corrected grade rows are not present in the public capture, so this page withholds the source-reported outcome totals and makes no comparative claim.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is an extraction from [run-record index](../../results/run-records/index.json). It contains 32 records tagged with the hp-syn task IDs: 25 exact delivery IDs and 7 captured handles that are not unique cell IDs. Of these records, 25 have a completed stop receipt, 2 have a timeout receipt, and 5 lack a normalized stop receipt. Every row has an unmapped audit round and a missing arm label. All are ungraded in the public capture, and none joins to an official row in [cells.jsonl](../../results/cells.jsonl). These captured rows do not reconstruct the reported scored outcomes.

The public task identifiers in that manifest are hp-syn-13, hp-syn-23 and hp-syn-40. Their relationship to the source-reported scored cells is not established.

## Reproduction record

- Harness and Kogen revision: no full commit SHA is bound to the scored cells in the public record. Any adapter fingerprint in the manifest is a fingerprint, not a Git commit.
- Model and effort: the manifest retains values for candidate public deliveries; the scored-cell assignment is unavailable.
- Task IDs: the public capture IDs are listed above; the source-reported scored task-to-arm mapping is missing.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This rebuilds the captured records; it does not rerun the models or grading.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl). The manifest links each retained delivery by its public cell ID.

## Interpretation

The check correction must remain separate from the original grades. The small screen, mixed model assignments, missing exact commit pins and absent official grade join prevent a comparative efficacy or speed claim.
