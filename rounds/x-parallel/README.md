# x parallel

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING, SMALL_SAMPLE. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **SMALL_SAMPLE:** The reported comparison is two tasks by two repetitions per arm.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H30 (provisional mapping; see the hypothesis register).
Question: Does planned parallel work improve completion enough to justify its additional requests, tokens and wall time?
Population: Two tasks × two repetitions for solo and planned-DAG arms are reported.
Headline: No throughput or general parallel-work claim.

## Reported observations

- Solo and planned-DAG arms are each reported at 4/4 passes. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The candidate parallel arm is reported at about 1.4× wall time and about 1.9× requests. A separate summary reports 1.84× input tokens and 2.50× output tokens; these measures are retained separately. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The summary recommends retaining solo for this two-task panel. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Per-cell model and effort values were not recovered. |
| Task IDs | Two tasks are reported; exact IDs are not recovered. |
| Command | Not recovered; public launch command and exact cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The panel is too small to establish general parallel-work effects; the reported resource increase did not accompany a pass-rate gain here.

**Smallest useful next test:** Test on tasks with demonstrated parallelizable work using a frozen DAG, matched solo controls, and public request/token/wall receipts.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-parallel.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 19 rows (fail 1, pass 17, ungraded 1); overall pass rate is 94.4% (17/18) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 19 field mismatches across 2 cell IDs (`experiment` 2, `manifest_grade.classification` 1, `manifest_grade.outcome` 1, `manifest_grade.pass_fail` 1, `patch.archive_member.cde19e2724d42f21f0b85e94b22ca9eaa5b72b630cdcad33f6511642f3d1d062` 1, `patch.archive_member.d8fb640e01c861b236812c46cc53831eb9542fa2961a9bd182ad183cab63b8a1` 1, `patch.attempt-1` 2, `usage.cached_input_tokens` 2, `usage.input_tokens` 2, `usage.output_tokens` 2, `usage.reasoning_tokens` 2, `wall_s` 2). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `experiment`: kept `"20260930T134928.088568Z-34880-64b375af"`, recovered `"20260930T132706.880923Z-22635-699173f7"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `manifest_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `manifest_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `manifest_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `patch.archive_member.cde19e2724d42f21f0b85e94b22ca9eaa5b72b630cdcad33f6511642f3d1d062`: kept `{"archive_member": null, "sha256": "cde19e2724d42f21f0b85e94b22ca9eaa5b72b630cdcad33f6511642f3d1d062", "size_bytes": 10863}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `patch.attempt-1`: kept `{"sha256": "6f6930517e97e8f5a175407813e29e27269ec8e28cd7d8779c6fb4fc97b5ddd6", "size_bytes": 11380}`, recovered `{"sha256": "cde19e2724d42f21f0b85e94b22ca9eaa5b72b630cdcad33f6511642f3d1d062", "size_bytes": 10863}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `usage.cached_input_tokens`: kept `118272`, recovered `73984`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `usage.input_tokens`: kept `29606`, recovered `14784`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `usage.output_tokens`: kept `5444`, recovered `5054`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `usage.reasoning_tokens`: kept `647`, recovered `327`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-07-cli-stats__r1` field `wall_s`: kept `363.572`, recovered `305.157`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T134928.088568Z-34880-64b375af"`, recovered `"20260930T132706.880923Z-22635-699173f7"`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.d8fb640e01c861b236812c46cc53831eb9542fa2961a9bd182ad183cab63b8a1`: kept `{"archive_member": null, "sha256": "d8fb640e01c861b236812c46cc53831eb9542fa2961a9bd182ad183cab63b8a1", "size_bytes": 13954}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "65c12c71602af667fb85a41f19ec2ecb9f19544deadd38f078778a96a330e55d", "size_bytes": 13098}`, recovered `{"sha256": "d8fb640e01c861b236812c46cc53831eb9542fa2961a9bd182ad183cab63b8a1", "size_bytes": 13954}`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `516352`, recovered `356608`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `47200`, recovered `60589`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `5140`, recovered `5055`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `408`, recovered `559`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `372.45`, recovered `331.307`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 19 missing published metadata). Missing counters remain unknown, not zero.
This round also has 19 raw-only or non-public rows; they are kept separate from the published-export denominator.
