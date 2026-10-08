# September kh comparison

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of COHORT_MISMATCH, OUTCOME_GRADES_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
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

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/kh-compare-2026-09-29.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 49 rows (fail 8, pass 15, ungraded 10, unknown 16); overall pass rate is 65.2% (15/23) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 42 field mismatches across 5 cell IDs (`experiment` 5, `manifest_grade.classification` 2, `manifest_grade.outcome` 2, `manifest_grade.pass_fail` 2, `patch.archive_member.5bd14d66c12431526c066a24f3187055e533b09d119fcec7e926b49e939d14b3` 1, `patch.archive_member.724a974eefef749309343b3e791dbf2e659b30488ecf795c4af8a533c5b5c915` 1, `patch.archive_member.8e14825cb41374b1f0352f8311bba30fca78993a40512e957117db0895782418` 1, `patch.archive_member.c9ce4c96dc20cfda0af6bb34782c69e58d76b959f57a177e80748fde0c38ab46` 1, `patch.attempt-1` 4, `status` 2, `usage.cached_input_tokens` 4, `usage.input_tokens` 4, `usage.output_tokens` 4, `usage.reasoning_tokens` 4, `wall_s` 5). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `experiment`: kept `"kh-compare-2026-09-29/cl-khcc-lean"`, recovered `"kh-compare-2026-09-29/cl-khcc-all"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `manifest_grade.classification`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `manifest_grade.outcome`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `manifest_grade.pass_fail`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `patch.archive_member.724a974eefef749309343b3e791dbf2e659b30488ecf795c4af8a533c5b5c915`: kept `{"archive_member": null, "sha256": "724a974eefef749309343b3e791dbf2e659b30488ecf795c4af8a533c5b5c915", "size_bytes": 7068}`, recovered `null`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `patch.attempt-1`: kept `{"sha256": "45b08b26c4e24d21d72b7cf2cd8d3214ffc43d10148b2c0a83cd3d7ef17a4e60", "size_bytes": 4612}`, recovered `{"sha256": "724a974eefef749309343b3e791dbf2e659b30488ecf795c4af8a533c5b5c915", "size_bytes": 7068}`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `usage.cached_input_tokens`: kept `402302`, recovered `195121`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `usage.input_tokens`: kept `32`, recovered `18`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `usage.output_tokens`: kept `6628`, recovered `4863`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `usage.reasoning_tokens`: kept `1881`, recovered `978`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-13__r1` field `wall_s`: kept `275.808`, recovered `45.725`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `experiment`: kept `"kh-compare-2026-09-29/cl-khcc-lean"`, recovered `"kh-compare-2026-09-29/cl-khcc-all"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `manifest_grade.classification`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `manifest_grade.outcome`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `manifest_grade.pass_fail`: kept `"fail"`, recovered `"pass"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `patch.archive_member.c9ce4c96dc20cfda0af6bb34782c69e58d76b959f57a177e80748fde0c38ab46`: kept `{"archive_member": null, "sha256": "c9ce4c96dc20cfda0af6bb34782c69e58d76b959f57a177e80748fde0c38ab46", "size_bytes": 8631}`, recovered `null`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `patch.attempt-1`: kept `{"sha256": "e32135319614e737db5c931304483120a13f077f66815bacae2e7a1ebec1374a", "size_bytes": 8058}`, recovered `{"sha256": "c9ce4c96dc20cfda0af6bb34782c69e58d76b959f57a177e80748fde0c38ab46", "size_bytes": 8631}`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `usage.cached_input_tokens`: kept `377864`, recovered `262454`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `usage.input_tokens`: kept `28`, recovered `20`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `usage.output_tokens`: kept `8122`, recovered `7766`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `usage.reasoning_tokens`: kept `2580`, recovered `2471`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-23__r1` field `wall_s`: kept `278.225`, recovered `72.537`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-40__r1` field `experiment`: kept `"kh-compare-2026-09-29/cl-khcc-lean"`, recovered `"kh-compare-2026-09-29/cl-khcc-all"`.
- `kh-cc__claude-sonnet-5-5__high__default__hp-syn-40__r1` field `wall_s`: kept `0.204`, recovered `0.205`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `experiment`: kept `"kh-compare-2026-09-29/oc-kh-base"`, recovered `"kh-compare-2026-09-29/oc-kh-feat"`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `patch.archive_member.8e14825cb41374b1f0352f8311bba30fca78993a40512e957117db0895782418`: kept `{"archive_member": null, "sha256": "8e14825cb41374b1f0352f8311bba30fca78993a40512e957117db0895782418", "size_bytes": 4050}`, recovered `null`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `patch.attempt-1`: kept `{"sha256": "36ed8eb6717a3743d1d1e2147d03d719d9bc5177eebd967749c26e723dda3809", "size_bytes": 4419}`, recovered `{"sha256": "8e14825cb41374b1f0352f8311bba30fca78993a40512e957117db0895782418", "size_bytes": 4050}`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `usage.cached_input_tokens`: kept `1622528`, recovered `1589248`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `usage.input_tokens`: kept `66659`, recovered `93823`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `usage.output_tokens`: kept `26631`, recovered `28645`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `usage.reasoning_tokens`: kept `19171`, recovered `22465`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-13__r1` field `wall_s`: kept `504.385`, recovered `525.628`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `experiment`: kept `"kh-compare-2026-09-29/oc-kh-base"`, recovered `"kh-compare-2026-09-29/oc-kh-feat"`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `patch.archive_member.5bd14d66c12431526c066a24f3187055e533b09d119fcec7e926b49e939d14b3`: kept `{"archive_member": null, "sha256": "5bd14d66c12431526c066a24f3187055e533b09d119fcec7e926b49e939d14b3", "size_bytes": 6744}`, recovered `null`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `patch.attempt-1`: kept `{"sha256": "f5bc75c257cee73b6f88e234492b812224e3ad77dccf96fdd16778f95188d461", "size_bytes": 6977}`, recovered `{"sha256": "5bd14d66c12431526c066a24f3187055e533b09d119fcec7e926b49e939d14b3", "size_bytes": 6744}`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `status`: kept `"ok"`, recovered `"error"`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `status`: kept `"ok"`, recovered `"running"`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `usage.cached_input_tokens`: kept `5157376`, recovered `8019328`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `usage.input_tokens`: kept `184340`, recovered `124614`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `usage.output_tokens`: kept `81494`, recovered `70409`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `usage.reasoning_tokens`: kept `66920`, recovered `57179`.
- `kh__opencode-go-deepseek-v4-pro__max__default__hp-syn-23__r1` field `wall_s`: kept `1312.101`, recovered `634.844`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 49 missing published metadata). Missing counters remain unknown, not zero.
This round also has 49 raw-only or non-public rows; they are kept separate from the published-export denominator.
