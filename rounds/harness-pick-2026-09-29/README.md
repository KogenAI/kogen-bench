# September harness pick

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of OUTCOME_CROSSWALK_MISSING, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
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

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/harness-pick-2026-09-29.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 22 rows (fail 5, pass 17); overall pass rate is 77.3% (17/22) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 17 field mismatches across 2 cell IDs (`experiment` 2, `patch.archive_member.94b3fd2ac1dd555ddb9f03958da17149aec8a472bff78633e02e50ccc0564d27` 1, `patch.archive_member.be5e8e3909427d7c16ee6d89beb3d7d695c5eef196ddd33e4c60e6457b138161` 1, `patch.attempt-1` 2, `status` 2, `usage.cached_input_tokens` 2, `usage.input_tokens` 2, `usage.output_tokens` 2, `usage.reasoning_tokens` 1, `wall_s` 2). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `experiment`: kept `"hp-grok"`, recovered `"hp-rerun"`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `patch.archive_member.94b3fd2ac1dd555ddb9f03958da17149aec8a472bff78633e02e50ccc0564d27`: kept `{"archive_member": null, "sha256": "94b3fd2ac1dd555ddb9f03958da17149aec8a472bff78633e02e50ccc0564d27", "size_bytes": 31865}`, recovered `null`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `patch.attempt-1`: kept `{"sha256": "88bbf1796d85cb44853cb0fb894b1af3365448b6f76a1572eb2d3d8d4219c3c0", "size_bytes": 28008}`, recovered `{"sha256": "94b3fd2ac1dd555ddb9f03958da17149aec8a472bff78633e02e50ccc0564d27", "size_bytes": 31865}`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `status`: kept `"ok"`, recovered `"timeout"`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `usage.cached_input_tokens`: kept `5867520`, recovered `3841280`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `usage.input_tokens`: kept `214085`, recovered `206280`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `usage.output_tokens`: kept `110632`, recovered `110367`.
- `grok__grok-4.7__high__default__hp-syn-40__r1` field `wall_s`: kept `1655.55`, recovered `1801.972`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `experiment`: kept `"hp-grok"`, recovered `"hp-rerun"`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `patch.archive_member.be5e8e3909427d7c16ee6d89beb3d7d695c5eef196ddd33e4c60e6457b138161`: kept `{"archive_member": null, "sha256": "be5e8e3909427d7c16ee6d89beb3d7d695c5eef196ddd33e4c60e6457b138161", "size_bytes": 27672}`, recovered `null`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `patch.attempt-1`: kept `{"sha256": "e489e4637e7abf2fa8842bcc0ecb9d017287c0e96a28952ce1eede828b226c80", "size_bytes": 26353}`, recovered `{"sha256": "be5e8e3909427d7c16ee6d89beb3d7d695c5eef196ddd33e4c60e6457b138161", "size_bytes": 27672}`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `status`: kept `"ok"`, recovered `"error"`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `usage.cached_input_tokens`: kept `3853824`, recovered `3972096`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `usage.input_tokens`: kept `340676`, recovered `704945`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `usage.output_tokens`: kept `98236`, recovered `95384`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `usage.reasoning_tokens`: kept `79808`, recovered `76243`.
- `pi__xai-grok-4.7__high__default__hp-syn-40__r1` field `wall_s`: kept `1212.437`, recovered `1208.136`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 22 missing published metadata). Missing counters remain unknown, not zero.
This round also has 22 raw-only or non-public rows; they are kept separate from the published-export denominator.
