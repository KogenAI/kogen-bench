# x review

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_MISMATCH, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_MISMATCH:** Review diagnostics and the separate repair screen have no combined planned or ITT denominator.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Task IDs: not recorded in the cited round source.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H67, H68 and H69, provisionally mapped to reviewer, executable-review and contract-audit questions.
Question: Can review methods identify supported defects without false accepts or false blocks, and do they help a repair session deliver a confirmed result?
Population: reported review-case diagnostics and a separate small semantic-repair screen; the combined planned and ITT denominators are not recovered.
Headline: These diagnostics do not establish a live review-policy benefit.

## Reported observations

- Checklist and risk-directed review are each reported with 0/14 false accepts, 0/10 false blocks and 14/14 supported-defect recall. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- In a separate repair workflow, 1/4 sessions reportedly emitted the required final result, with 0/8 fresh confirmation calls. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A distinct Sol-high semantic-repair summary reports 1/2 versus 0/2 failing a confirmation gate on complete delivery. Its arm mapping is unrecovered and it is not pooled with the diagnostic cases. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact revision was not recovered. |
| Model and effort | Exact model/effort by arm was not recovered. A separate semantic-repair summary identifies Sol high, without a recoverable cell mapping. |
| Task and case IDs | Exact task and diagnostic case IDs are not recovered. |
| Command | Not recovered; no public launch command or selected-cell manifest is available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

## Interpretation

**Limitation:** Review-case accuracy diagnostics, repair-session completion and a small semantic-repair comparison use different populations. None is a public exact-cell analysis.

**Smallest useful next test:** Freeze a blinded case set and matched live repair arms, record exact reviewer decisions and false-block controls, and require a fresh confirmation call before counting a delivered result.

No review or veto policy is qualified by these records.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-review.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 34 rows (fail 5, infra 1, pass 26, ungraded 2); overall pass rate is 83.9% (26/31) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 59 field mismatches across 3 cell IDs (`experiment` 7, `manifest_grade.classification` 3, `manifest_grade.outcome` 3, `manifest_grade.pass_fail` 3, `patch.archive_member.331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e` 2, `patch.archive_member.455bc1c03446ae4049e56120782c39a73ced8f534ec320908c469526857d01ab` 1, `patch.archive_member.a09b1468da2c58cd39fa6829637eccee6b0775aa78e59f9bb25da14fd2c9667a` 1, `patch.archive_member.a9cff19b01cbc1753df0d670969c80dd11668dd8bbdbfb4015b8e15b0480f3d3` 1, `patch.archive_member.b45ab63561b0651c247760f44480c9c23d0f722a73b911b6dc3b7cf84ba1ed23` 1, `patch.attempt-1` 6, `status` 4, `usage.cached_input_tokens` 5, `usage.input_tokens` 5, `usage.output_tokens` 5, `usage.reasoning_tokens` 5, `wall_s` 7). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `experiment`: kept `"20260930T141318.681059Z-59360-2a589b44"`, recovered `"20260930T141319.767697Z-59379-42591075"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `manifest_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `manifest_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `manifest_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `patch.archive_member.b45ab63561b0651c247760f44480c9c23d0f722a73b911b6dc3b7cf84ba1ed23`: kept `{"archive_member": null, "sha256": "b45ab63561b0651c247760f44480c9c23d0f722a73b911b6dc3b7cf84ba1ed23", "size_bytes": 1561}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `patch.attempt-1`: kept `{"sha256": "3069a690b4119eb3a27bab64314e1d34b05e2ac090409e670778f2a62d3002da", "size_bytes": 1562}`, recovered `{"sha256": "b45ab63561b0651c247760f44480c9c23d0f722a73b911b6dc3b7cf84ba1ed23", "size_bytes": 1561}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `usage.cached_input_tokens`: kept `29056`, recovered `17920`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `usage.input_tokens`: kept `13252`, recovered `8359`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `usage.output_tokens`: kept `1612`, recovered `796`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `usage.reasoning_tokens`: kept `255`, recovered `32`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `wall_s`: kept `146.972`, recovered `108.043`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `experiment`: kept `"20260930T154059.220068Z-70254-82eceb5e"`, recovered `"20260930T135327.533026Z-39253-50d49bf6"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `experiment`: kept `"20260930T154059.220068Z-70254-82eceb5e"`, recovered `"20260930T135452.713896Z-40634-9ecb3ec5"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `experiment`: kept `"20260930T154059.220068Z-70254-82eceb5e"`, recovered `"20260930T135802.170732Z-44095-bedf47f3"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `manifest_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `manifest_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `manifest_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `patch.archive_member.331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e`: kept `{"archive_member": null, "sha256": "331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e", "size_bytes": 1965901}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `patch.archive_member.a09b1468da2c58cd39fa6829637eccee6b0775aa78e59f9bb25da14fd2c9667a`: kept `{"archive_member": null, "sha256": "a09b1468da2c58cd39fa6829637eccee6b0775aa78e59f9bb25da14fd2c9667a", "size_bytes": 778}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "da0198695f2a86075b1729334c7c4cb4d1022e10850041358506321d5084ab9b", "size_bytes": 1336}`, recovered `{"sha256": "331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e", "size_bytes": 1965901}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "da0198695f2a86075b1729334c7c4cb4d1022e10850041358506321d5084ab9b", "size_bytes": 1336}`, recovered `{"sha256": "a09b1468da2c58cd39fa6829637eccee6b0775aa78e59f9bb25da14fd2c9667a", "size_bytes": 778}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `status`: kept `"error"`, recovered `"infra_error"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `status`: kept `"error"`, recovered `"ok"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `39168`, recovered `12032`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `39168`, recovered `5120`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.input_tokens`: kept `28519`, recovered `11215`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.input_tokens`: kept `28519`, recovered `20945`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.output_tokens`: kept `578`, recovered `697`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.output_tokens`: kept `578`, recovered `815`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `150`, recovered `14`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `150`, recovered `204`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `wall_s`: kept `54.724`, recovered `0.502`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `wall_s`: kept `54.724`, recovered `60.475`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-06__r1` field `wall_s`: kept `54.724`, recovered `82.575`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `experiment`: kept `"20260930T135720.591758Z-43106-8678d225"`, recovered `"20260930T135356.067288Z-39681-f14898ca"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `experiment`: kept `"20260930T135720.591758Z-43106-8678d225"`, recovered `"20260930T135453.790803Z-40692-c80d65dd"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `experiment`: kept `"20260930T135720.591758Z-43106-8678d225"`, recovered `"20260930T135720.585973Z-43105-fdf99dbf"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `manifest_grade.classification`: kept `"fail"`, recovered `"pass"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `manifest_grade.outcome`: kept `"fail"`, recovered `"pass"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `manifest_grade.pass_fail`: kept `"fail"`, recovered `"pass"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.archive_member.331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e`: kept `{"archive_member": null, "sha256": "331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e", "size_bytes": 1965901}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.archive_member.455bc1c03446ae4049e56120782c39a73ced8f534ec320908c469526857d01ab`: kept `{"archive_member": null, "sha256": "455bc1c03446ae4049e56120782c39a73ced8f534ec320908c469526857d01ab", "size_bytes": 1968624}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.archive_member.a9cff19b01cbc1753df0d670969c80dd11668dd8bbdbfb4015b8e15b0480f3d3`: kept `{"archive_member": null, "sha256": "a9cff19b01cbc1753df0d670969c80dd11668dd8bbdbfb4015b8e15b0480f3d3", "size_bytes": 3255}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.attempt-1`: kept `{"sha256": "03d47f45936ea3e9c53a743db49bf93b5542101b53e84d996165b27befcd4d15", "size_bytes": 2865}`, recovered `{"sha256": "331cff0ab11894bd6f6338681dd624beba71bbc4829527e96f96c66260e6095e", "size_bytes": 1965901}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.attempt-1`: kept `{"sha256": "03d47f45936ea3e9c53a743db49bf93b5542101b53e84d996165b27befcd4d15", "size_bytes": 2865}`, recovered `{"sha256": "455bc1c03446ae4049e56120782c39a73ced8f534ec320908c469526857d01ab", "size_bytes": 1968624}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `patch.attempt-1`: kept `{"sha256": "03d47f45936ea3e9c53a743db49bf93b5542101b53e84d996165b27befcd4d15", "size_bytes": 2865}`, recovered `{"sha256": "a9cff19b01cbc1753df0d670969c80dd11668dd8bbdbfb4015b8e15b0480f3d3", "size_bytes": 3255}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `status`: kept `"ok"`, recovered `"error"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `status`: kept `"ok"`, recovered `"infra_error"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.cached_input_tokens`: kept `21376`, recovered `1536`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.cached_input_tokens`: kept `21376`, recovered `22016`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.input_tokens`: kept `15615`, recovered `18810`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.input_tokens`: kept `15615`, recovered `7193`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.output_tokens`: kept `1314`, recovered `166`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.output_tokens`: kept `1314`, recovered `1881`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.reasoning_tokens`: kept `47`, recovered `0`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `usage.reasoning_tokens`: kept `47`, recovered `279`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `wall_s`: kept `120.279`, recovered `0.502`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `wall_s`: kept `120.279`, recovered `133.068`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-08__r1` field `wall_s`: kept `120.279`, recovered `40.484`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 34 missing published metadata). Missing counters remain unknown, not zero.
This round also has 34 raw-only or non-public rows; they are kept separate from the published-export denominator.
