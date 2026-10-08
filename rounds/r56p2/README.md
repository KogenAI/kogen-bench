# r56p2

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of CROSSWALK, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No public predeclared decision rule was recovered.
- CROSSWALK — Official outcomes cannot be matched to the prior builder-context arm rows.
- DESIGN — The dedicated design section and exact arm specification are absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **46.9%** (336 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior builder-context arm rows; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r56p2.jsonl](../../results/run-records/r56p2.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56p2`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56p2.jsonl](../../results/run-records/r56p2.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 336 captured deliveries (167 pass, 154 fail, 15 ungraded/unknown in `results/run-records/r56p2.jsonl`); official outcome export has 321 rows: 167 pass, 154 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** This is a separate later capture. Keep it apart from the r56/r56b/r56c/r56d cohorts; the historical pooled decision table is not reproduced by this page.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r56p2.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 321 rows (fail 154, pass 167); overall pass rate is 52.0% (167/321) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 321/321 shared cell IDs match; 0/321 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 451 field mismatches across 24 cell IDs (`manifest_cell_id` 40, `patch.archive_member.049ccccecfe1aa6fdcd21c7936afcc10b0bdb62351f75506ccd224a6d633d6e6` 1, `patch.archive_member.25f2397085a40f776fa23984f268d8f6b82fc6cb8ca874faef14f9389ad560f2` 1, `patch.archive_member.3ac747d9ab24ce05b54a94cecefb1750fa83a24efb76f257ede7fd58e5e0e755` 1, `patch.archive_member.44ab81a1ac556be76b6861796649c6272adf41f0b960dfa741cf43119d88cacc` 1, `patch.archive_member.6d1ec7f34a00f03ed57360f45e03a8b8082888542c5234c3419c1dccc0b28dce` 1, `patch.archive_member.81b65cf1fbb41ebc41ef29e25afeb70157deda1d6736a151e1955d9112246230` 1, `patch.archive_member.98803e3e451c1e383899e7e9baa5ae1dd1bba2cfd928fe3d14962e4a0a5e5e3c` 1, `patch.archive_member.a07b097e2cdf9da7858ea66c0536bcfab09cd16f5b7284e3fecba29d4d454f00` 1, `patch.archive_member.ae256c054daf8f12aa24faa737bd3ae0c95bc352b6dfb7c1a6c531215f28199b` 1, `patch.archive_member.b0a64a8023e3601c2cac535123ff9ac9e04b66edd34a213edff4156f5cf61e10` 1, `patch.archive_member.be4b2bfd27d22b1086b0d47e0db6c1c7218a264f934da1c1fc282150b4fdb993` 1, `patch.archive_member.d7bd9fbcd0e8b9786542c2988477124b702f697b808d4aecf7f3ae6e38b86ae8` 1, `patch.archive_member.da9f664772712d6f13b0f26d3bc54dca7535e874f02c02e8e1c6878f739df194` 1, `patch.archive_member.e0f7e9824a34f853c9d649d1d43900115522a6babcd376ab338ed240316bbf2f` 1, `patch.archive_member.e3ad23dea9a9943670595a9b2a6c2e7c20035af030a6a715c21d415ddb273e08` 1, `patch.archive_member.f6589930be2c004b4d4d9a324a397d5db152fd8a02b14a21018b800fc94ed00d` 1, `patch.archive_member.fa6566a29d4dd33eeedcd5f975f0fa44af809294ab9965e13033fdc8a87e0f3d` 1, `patch.attempt-1` 64, `rep` 40, `usage.cached_input_tokens` 52, `usage.input_tokens` 56, `usage.output_tokens` 56, `usage.reasoning_tokens` 56, `wall_s` 70). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r10"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "43ed4d12de1c51f69574772f28372256bcdc50e811e09c837f3a35b6e6a0a803", "size_bytes": 496}`, recovered `{"sha256": "6030c194e85364f8b1bbe4f11001182ce3c665739c45f4cb3cc423d7d25c7e7b", "size_bytes": 460}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "43ed4d12de1c51f69574772f28372256bcdc50e811e09c837f3a35b6e6a0a803", "size_bytes": 496}`, recovered `{"sha256": "6030c194e85364f8b1bbe4f11001182ce3c665739c45f4cb3cc423d7d25c7e7b", "size_bytes": 460}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `171520`, recovered `108544`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `usage.input_tokens`: kept `34739`, recovered `23127`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `usage.output_tokens`: kept `4472`, recovered `2621`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `3474`, recovered `1804`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-det-r1` field `wall_s`: kept `206.096`, recovered `116.895`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "43ed4d12de1c51f69574772f28372256bcdc50e811e09c837f3a35b6e6a0a803", "size_bytes": 496}`, recovered `{"sha256": "8490ffe9228f31556878f7f64f2953457829a8eea22fad37a6453f6f427f0ec9", "size_bytes": 460}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "8490ffe9228f31556878f7f64f2953457829a8eea22fad37a6453f6f427f0ec9", "size_bytes": 460}`, recovered `{"sha256": "43ed4d12de1c51f69574772f28372256bcdc50e811e09c837f3a35b6e6a0a803", "size_bytes": 496}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `100352`, recovered `91648`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `91648`, recovered `100352`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `91648`, recovered `100352`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.input_tokens`: kept `20210`, recovered `26023`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.input_tokens`: kept `20210`, recovered `26023`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.input_tokens`: kept `26023`, recovered `20210`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.output_tokens`: kept `2465`, recovered `6429`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.output_tokens`: kept `2465`, recovered `6429`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.output_tokens`: kept `6429`, recovered `2465`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `1480`, recovered `5441`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `1480`, recovered `5441`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `5441`, recovered `1480`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `wall_s`: kept `179.973`, recovered `333.888`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `wall_s`: kept `179.973`, recovered `333.888`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-ls-r1` field `wall_s`: kept `333.888`, recovered `179.973`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "7f947660dc3a1481650f929a2e167ca7a6f926140744c34656326cb3013fe512", "size_bytes": 481}`, recovered `{"sha256": "90b03533e4154742850258df939925087f42acf8b26af26c1d6b68d2b2a6cc07", "size_bytes": 2772}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "90b03533e4154742850258df939925087f42acf8b26af26c1d6b68d2b2a6cc07", "size_bytes": 2772}`, recovered `{"sha256": "7f947660dc3a1481650f929a2e167ca7a6f926140744c34656326cb3013fe512", "size_bytes": 481}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `117248`, recovered `1180160`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `117248`, recovered `1180160`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `1180160`, recovered `117248`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.input_tokens`: kept `27284`, recovered `67082`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.input_tokens`: kept `27284`, recovered `67082`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.input_tokens`: kept `67082`, recovered `27284`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.output_tokens`: kept `11106`, recovered `2585`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.output_tokens`: kept `2585`, recovered `11106`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.output_tokens`: kept `2585`, recovered `11106`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `1644`, recovered `7966`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `1644`, recovered `7966`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `7966`, recovered `1644`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `wall_s`: kept `110.27`, recovered `520.358`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `wall_s`: kept `110.27`, recovered `520.358`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-none-r1` field `wall_s`: kept `520.358`, recovered `110.27`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-ac-throttle-search__r1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "8749f8dcdae67a52f0f6e0389450ebc114a3ff05c255fb4c8fc4268bf5917195", "size_bytes": 2937}`, recovered `{"sha256": "cebe7a1ad10481aafac7092eddcb8f4975884548f400076b0394c4c91f7c50a8", "size_bytes": 4237}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "cebe7a1ad10481aafac7092eddcb8f4975884548f400076b0394c4c91f7c50a8", "size_bytes": 4237}`, recovered `{"sha256": "8749f8dcdae67a52f0f6e0389450ebc114a3ff05c255fb4c8fc4268bf5917195", "size_bytes": 2937}`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `1086976`, recovered `1203712`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `1086976`, recovered `1203712`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `1203712`, recovered `1086976`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.input_tokens`: kept `68365`, recovered `69039`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.input_tokens`: kept `68365`, recovered `69039`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.input_tokens`: kept `69039`, recovered `68365`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.output_tokens`: kept `18245`, recovered `19582`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.output_tokens`: kept `19582`, recovered `18245`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.output_tokens`: kept `19582`, recovered `18245`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `14046`, recovered `14059`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `14059`, recovered `14046`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `14059`, recovered `14046`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `wall_s`: kept `2023.809`, recovered `901.003`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `wall_s`: kept `2023.809`, recovered `901.003`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1` field `wall_s`: kept `901.003`, recovered `2023.809`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-det-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-det-r1` field `wall_s`: kept `0.739`, recovered `1.09`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-det-r1` field `wall_s`: kept `1.09`, recovered `0.739`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-det-r1` field `wall_s`: kept `1.09`, recovered `0.739`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r10"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `patch.archive_member.e3ad23dea9a9943670595a9b2a6c2e7c20035af030a6a715c21d415ddb273e08`: kept `{"archive_member": null, "sha256": "e3ad23dea9a9943670595a9b2a6c2e7c20035af030a6a715c21d415ddb273e08", "size_bytes": 3191}`, recovered `null`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "8963ccaff862b9f59f97ea30ae20956783a8eadc7adc058a073eea80789e7f2f", "size_bytes": 3834}`, recovered `{"sha256": "e3ad23dea9a9943670595a9b2a6c2e7c20035af030a6a715c21d415ddb273e08", "size_bytes": 3191}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "8963ccaff862b9f59f97ea30ae20956783a8eadc7adc058a073eea80789e7f2f", "size_bytes": 3834}`, recovered `{"sha256": "e3ad23dea9a9943670595a9b2a6c2e7c20035af030a6a715c21d415ddb273e08", "size_bytes": 3191}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `462336`, recovered `745984`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `usage.input_tokens`: kept `49759`, recovered `74173`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `usage.output_tokens`: kept `10750`, recovered `13242`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `7642`, recovered `9603`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-ls-r1` field `wall_s`: kept `343.161`, recovered `401.832`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "01ace00033087ec2643b4bf2895f17078d7248c645f068568b51c7092ff22207", "size_bytes": 2728}`, recovered `{"sha256": "01b0a82072ce2394e2e646a061a0e3c060fcc572262ba838d2bf67bfa1aaf395", "size_bytes": 3173}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "01b0a82072ce2394e2e646a061a0e3c060fcc572262ba838d2bf67bfa1aaf395", "size_bytes": 3173}`, recovered `{"sha256": "01ace00033087ec2643b4bf2895f17078d7248c645f068568b51c7092ff22207", "size_bytes": 2728}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `416256`, recovered `958464`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `416256`, recovered `958464`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `958464`, recovered `416256`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.input_tokens`: kept `44290`, recovered `62033`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.input_tokens`: kept `44290`, recovered `62033`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.input_tokens`: kept `62033`, recovered `44290`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.output_tokens`: kept `10261`, recovered `9798`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.output_tokens`: kept `9798`, recovered `10261`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.output_tokens`: kept `9798`, recovered `10261`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `6813`, recovered `7231`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `7231`, recovered `6813`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `7231`, recovered `6813`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `wall_s`: kept `392.606`, recovered `420.242`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `wall_s`: kept `392.606`, recovered `420.242`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-none-r1` field `wall_s`: kept `420.242`, recovered `392.606`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "6ba75f15065fd7396952e8538157978a969719dbcfba1d114450015a4ecd0b0d", "size_bytes": 3838}`, recovered `{"sha256": "e656a8cf620ff535c940e25efd0221fa70bde74d9f96e72b74c637c7a6975581", "size_bytes": 4324}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "e656a8cf620ff535c940e25efd0221fa70bde74d9f96e72b74c637c7a6975581", "size_bytes": 4324}`, recovered `{"sha256": "6ba75f15065fd7396952e8538157978a969719dbcfba1d114450015a4ecd0b0d", "size_bytes": 3838}`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `1271808`, recovered `569344`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `569344`, recovered `1271808`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `569344`, recovered `1271808`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.input_tokens`: kept `58341`, recovered `86072`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.input_tokens`: kept `58341`, recovered `86072`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.input_tokens`: kept `86072`, recovered `58341`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.output_tokens`: kept `11770`, recovered `18669`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.output_tokens`: kept `11770`, recovered `18669`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.output_tokens`: kept `18669`, recovered `11770`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `13378`, recovered `8777`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `8777`, recovered `13378`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `8777`, recovered `13378`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `wall_s`: kept `609.638`, recovered `653.102`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `wall_s`: kept `653.102`, recovered `609.638`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1` field `wall_s`: kept `653.102`, recovered `609.638`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "35e65ae61b8bc0d5922e489bee028248f3f4a4eb21ce1812d50ba08b0baaaac8", "size_bytes": 1419}`, recovered `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "35e65ae61b8bc0d5922e489bee028248f3f4a4eb21ce1812d50ba08b0baaaac8", "size_bytes": 1419}`, recovered `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `242176`, recovered `150016`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `usage.input_tokens`: kept `45364`, recovered `38398`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `usage.output_tokens`: kept `5754`, recovered `2781`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `3722`, recovered `1559`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-det-r1` field `wall_s`: kept `212.991`, recovered `130.885`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "5374f276036b211121fd28d5e6358c8f6282d6a63682ffea8ac325c6c3362f82", "size_bytes": 831}`, recovered `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`, recovered `{"sha256": "5374f276036b211121fd28d5e6358c8f6282d6a63682ffea8ac325c6c3362f82", "size_bytes": 831}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `102912`, recovered `106496`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `106496`, recovered `102912`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `106496`, recovered `102912`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.input_tokens`: kept `20065`, recovered `32575`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.input_tokens`: kept `32575`, recovered `20065`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.input_tokens`: kept `32575`, recovered `20065`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.output_tokens`: kept `2180`, recovered `2584`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.output_tokens`: kept `2584`, recovered `2180`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.output_tokens`: kept `2584`, recovered `2180`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `1234`, recovered `1423`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `1423`, recovered `1234`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `1423`, recovered `1234`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `wall_s`: kept `118.833`, recovered `164.371`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `wall_s`: kept `164.371`, recovered `118.833`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-ls-r1` field `wall_s`: kept `164.371`, recovered `118.833`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`, recovered `{"sha256": "e7dd9747051b6be6fa5d1884d5906f19095a63e07acf818ff728a07fe4549dd5", "size_bytes": 1580}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "d0c4dcc13092bf852c3ff570600b0becce48f492ee3c551fc98bd9da2d99bd8a", "size_bytes": 1252}`, recovered `{"sha256": "e7dd9747051b6be6fa5d1884d5906f19095a63e07acf818ff728a07fe4549dd5", "size_bytes": 1580}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `usage.input_tokens`: kept `34867`, recovered `29609`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `usage.output_tokens`: kept `3920`, recovered `4106`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `2604`, recovered `2469`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-none-r1` field `wall_s`: kept `139.203`, recovered `183.891`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `patch.archive_member.be4b2bfd27d22b1086b0d47e0db6c1c7218a264f934da1c1fc282150b4fdb993`: kept `{"archive_member": null, "sha256": "be4b2bfd27d22b1086b0d47e0db6c1c7218a264f934da1c1fc282150b4fdb993", "size_bytes": 1338}`, recovered `null`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "90a7f4c627e4baf441d7de2cd5b08506beaf563b97a67795285500a489a0e03a", "size_bytes": 1328}`, recovered `{"sha256": "be4b2bfd27d22b1086b0d47e0db6c1c7218a264f934da1c1fc282150b4fdb993", "size_bytes": 1338}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "90a7f4c627e4baf441d7de2cd5b08506beaf563b97a67795285500a489a0e03a", "size_bytes": 1328}`, recovered `{"sha256": "be4b2bfd27d22b1086b0d47e0db6c1c7218a264f934da1c1fc282150b4fdb993", "size_bytes": 1338}`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `118272`, recovered `98816`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `usage.input_tokens`: kept `43695`, recovered `34020`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `usage.output_tokens`: kept `4040`, recovered `3677`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `2664`, recovered `2523`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1` field `wall_s`: kept `243.506`, recovered `251.922`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r1"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-det-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-det-r1` field `wall_s`: kept `0.747`, recovered `1.087`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-det-r1` field `wall_s`: kept `1.087`, recovered `0.747`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-det-r1` field `wall_s`: kept `1.087`, recovered `0.747`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r1"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "6a26933ed108e9c2dc66dd2c0ba2694327ab2790c6ff54c6ea119a04acf85534", "size_bytes": 2364}`, recovered `{"sha256": "7b448105461a7b7ba440ae81d1692a5a53ffc69f6edfb56d0ee7a41bd30a34e9", "size_bytes": 2355}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "7b448105461a7b7ba440ae81d1692a5a53ffc69f6edfb56d0ee7a41bd30a34e9", "size_bytes": 2355}`, recovered `{"sha256": "6a26933ed108e9c2dc66dd2c0ba2694327ab2790c6ff54c6ea119a04acf85534", "size_bytes": 2364}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `1199616`, recovered `1343488`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `1199616`, recovered `1343488`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `1343488`, recovered `1199616`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.input_tokens`: kept `71245`, recovered `78439`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.input_tokens`: kept `71245`, recovered `78439`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.input_tokens`: kept `78439`, recovered `71245`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.output_tokens`: kept `15173`, recovered `15590`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.output_tokens`: kept `15173`, recovered `15590`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.output_tokens`: kept `15590`, recovered `15173`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `11175`, recovered `11319`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `11175`, recovered `11319`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `11319`, recovered `11175`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `wall_s`: kept `484.249`, recovered `812.748`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `wall_s`: kept `812.748`, recovered `484.249`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-ls-r1` field `wall_s`: kept `812.748`, recovered `484.249`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r10"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `patch.archive_member.f6589930be2c004b4d4d9a324a397d5db152fd8a02b14a21018b800fc94ed00d`: kept `{"archive_member": null, "sha256": "f6589930be2c004b4d4d9a324a397d5db152fd8a02b14a21018b800fc94ed00d", "size_bytes": 3227}`, recovered `null`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "8e59de96cdb5c10ca34b7078f3176e59d1d10a5c5f8d62e2a52e025d51d1f0c6", "size_bytes": 2257}`, recovered `{"sha256": "f6589930be2c004b4d4d9a324a397d5db152fd8a02b14a21018b800fc94ed00d", "size_bytes": 3227}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "8e59de96cdb5c10ca34b7078f3176e59d1d10a5c5f8d62e2a52e025d51d1f0c6", "size_bytes": 2257}`, recovered `{"sha256": "f6589930be2c004b4d4d9a324a397d5db152fd8a02b14a21018b800fc94ed00d", "size_bytes": 3227}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `1420800`, recovered `1999360`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `usage.input_tokens`: kept `96407`, recovered `104046`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `usage.output_tokens`: kept `17237`, recovered `17840`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `11597`, recovered `13354`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-none-r1` field `wall_s`: kept `504.621`, recovered `569.009`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__rails-as-variant-processed-once__r10"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `patch.archive_member.81b65cf1fbb41ebc41ef29e25afeb70157deda1d6736a151e1955d9112246230`: kept `{"archive_member": null, "sha256": "81b65cf1fbb41ebc41ef29e25afeb70157deda1d6736a151e1955d9112246230", "size_bytes": 2239}`, recovered `null`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "a4a27d228a903f727359aefb7562c3e2df36e40331a23f2931a491b8befedb72", "size_bytes": 3035}`, recovered `{"sha256": "81b65cf1fbb41ebc41ef29e25afeb70157deda1d6736a151e1955d9112246230", "size_bytes": 2239}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "a4a27d228a903f727359aefb7562c3e2df36e40331a23f2931a491b8befedb72", "size_bytes": 3035}`, recovered `{"sha256": "81b65cf1fbb41ebc41ef29e25afeb70157deda1d6736a151e1955d9112246230", "size_bytes": 2239}`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `796672`, recovered `1229312`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `usage.input_tokens`: kept `64714`, recovered `80038`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `usage.output_tokens`: kept `18978`, recovered `16276`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `15291`, recovered `10743`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1` field `wall_s`: kept `755.777`, recovered `939.36`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `0.654`, recovered `0.816`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `0.654`, recovered `0.818`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `0.654`, recovered `1.246`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.archive_member.6d1ec7f34a00f03ed57360f45e03a8b8082888542c5234c3419c1dccc0b28dce`: kept `{"archive_member": null, "sha256": "6d1ec7f34a00f03ed57360f45e03a8b8082888542c5234c3419c1dccc0b28dce", "size_bytes": 8542}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.archive_member.da9f664772712d6f13b0f26d3bc54dca7535e874f02c02e8e1c6878f739df194`: kept `{"archive_member": null, "sha256": "da9f664772712d6f13b0f26d3bc54dca7535e874f02c02e8e1c6878f739df194", "size_bytes": 7305}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.archive_member.e0f7e9824a34f853c9d649d1d43900115522a6babcd376ab338ed240316bbf2f`: kept `{"archive_member": null, "sha256": "e0f7e9824a34f853c9d649d1d43900115522a6babcd376ab338ed240316bbf2f", "size_bytes": 7441}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "6d1ec7f34a00f03ed57360f45e03a8b8082888542c5234c3419c1dccc0b28dce", "size_bytes": 8542}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "6d1ec7f34a00f03ed57360f45e03a8b8082888542c5234c3419c1dccc0b28dce", "size_bytes": 8542}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "da9f664772712d6f13b0f26d3bc54dca7535e874f02c02e8e1c6878f739df194", "size_bytes": 7305}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "da9f664772712d6f13b0f26d3bc54dca7535e874f02c02e8e1c6878f739df194", "size_bytes": 7305}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "e0f7e9824a34f853c9d649d1d43900115522a6babcd376ab338ed240316bbf2f", "size_bytes": 7441}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "b35878ddfd472b31fdb60d90b9481baa42ba82370550ef8740bc4539dd974e77", "size_bytes": 8474}`, recovered `{"sha256": "e0f7e9824a34f853c9d649d1d43900115522a6babcd376ab338ed240316bbf2f", "size_bytes": 7441}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `279040`, recovered `104448`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `279040`, recovered `237568`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `279040`, recovered `256512`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.input_tokens`: kept `36083`, recovered `28970`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.input_tokens`: kept `36083`, recovered `34574`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.input_tokens`: kept `36083`, recovered `49040`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.output_tokens`: kept `14668`, recovered `10659`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.output_tokens`: kept `14668`, recovered `11711`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.output_tokens`: kept `14668`, recovered `14110`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `7071`, recovered `4052`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `7071`, recovered `4189`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `7071`, recovered `6946`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `wall_s`: kept `342.111`, recovered `230.941`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `wall_s`: kept `342.111`, recovered `285.007`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-ls-r1` field `wall_s`: kept `342.111`, recovered `310.041`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.archive_member.3ac747d9ab24ce05b54a94cecefb1750fa83a24efb76f257ede7fd58e5e0e755`: kept `{"archive_member": null, "sha256": "3ac747d9ab24ce05b54a94cecefb1750fa83a24efb76f257ede7fd58e5e0e755", "size_bytes": 8113}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.archive_member.b0a64a8023e3601c2cac535123ff9ac9e04b66edd34a213edff4156f5cf61e10`: kept `{"archive_member": null, "sha256": "b0a64a8023e3601c2cac535123ff9ac9e04b66edd34a213edff4156f5cf61e10", "size_bytes": 8694}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "ae7c797688c8b847f427c19184d442b850a03e7fccdca22757be0096dcddf9ce", "size_bytes": 10003}`, recovered `{"sha256": "3ac747d9ab24ce05b54a94cecefb1750fa83a24efb76f257ede7fd58e5e0e755", "size_bytes": 8113}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "ae7c797688c8b847f427c19184d442b850a03e7fccdca22757be0096dcddf9ce", "size_bytes": 10003}`, recovered `{"sha256": "b0a64a8023e3601c2cac535123ff9ac9e04b66edd34a213edff4156f5cf61e10", "size_bytes": 8694}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "ae7c797688c8b847f427c19184d442b850a03e7fccdca22757be0096dcddf9ce", "size_bytes": 10003}`, recovered `{"sha256": "cc4bcc3cc8444e3c31fe238dc0ca6ce373017ada1e01c2b754b9c46c4705453e", "size_bytes": 8281}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "cc4bcc3cc8444e3c31fe238dc0ca6ce373017ada1e01c2b754b9c46c4705453e", "size_bytes": 8281}`, recovered `{"sha256": "3ac747d9ab24ce05b54a94cecefb1750fa83a24efb76f257ede7fd58e5e0e755", "size_bytes": 8113}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "cc4bcc3cc8444e3c31fe238dc0ca6ce373017ada1e01c2b754b9c46c4705453e", "size_bytes": 8281}`, recovered `{"sha256": "ae7c797688c8b847f427c19184d442b850a03e7fccdca22757be0096dcddf9ce", "size_bytes": 10003}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "cc4bcc3cc8444e3c31fe238dc0ca6ce373017ada1e01c2b754b9c46c4705453e", "size_bytes": 8281}`, recovered `{"sha256": "b0a64a8023e3601c2cac535123ff9ac9e04b66edd34a213edff4156f5cf61e10", "size_bytes": 8694}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `276480`, recovered `212480`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `276480`, recovered `331776`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `276480`, recovered `413696`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `413696`, recovered `276480`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `413696`, recovered `276480`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.input_tokens`: kept `41348`, recovered `33013`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.input_tokens`: kept `41348`, recovered `42630`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.input_tokens`: kept `41348`, recovered `59845`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.input_tokens`: kept `59845`, recovered `41348`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.input_tokens`: kept `59845`, recovered `41348`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.output_tokens`: kept `17282`, recovered `11611`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.output_tokens`: kept `17282`, recovered `17453`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.output_tokens`: kept `17282`, recovered `28692`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.output_tokens`: kept `17453`, recovered `17282`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.output_tokens`: kept `17453`, recovered `17282`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `5468`, recovered `4190`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `5468`, recovered `5664`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `5468`, recovered `6227`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `6227`, recovered `5468`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `6227`, recovered `5468`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `wall_s`: kept `365.585`, recovered `1516.19`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `wall_s`: kept `365.585`, recovered `280.156`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `wall_s`: kept `365.585`, recovered `475.37`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `wall_s`: kept `475.37`, recovered `365.585`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-none-r1` field `wall_s`: kept `475.37`, recovered `365.585`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.archive_member.98803e3e451c1e383899e7e9baa5ae1dd1bba2cfd928fe3d14962e4a0a5e5e3c`: kept `{"archive_member": null, "sha256": "98803e3e451c1e383899e7e9baa5ae1dd1bba2cfd928fe3d14962e4a0a5e5e3c", "size_bytes": 7818}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.archive_member.a07b097e2cdf9da7858ea66c0536bcfab09cd16f5b7284e3fecba29d4d454f00`: kept `{"archive_member": null, "sha256": "a07b097e2cdf9da7858ea66c0536bcfab09cd16f5b7284e3fecba29d4d454f00", "size_bytes": 7264}`, recovered `null`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "03328602a78db17ea128acd2d725483f3465c136ba995d3c885df46173ce5064", "size_bytes": 8217}`, recovered `{"sha256": "98803e3e451c1e383899e7e9baa5ae1dd1bba2cfd928fe3d14962e4a0a5e5e3c", "size_bytes": 7818}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "03328602a78db17ea128acd2d725483f3465c136ba995d3c885df46173ce5064", "size_bytes": 8217}`, recovered `{"sha256": "a07b097e2cdf9da7858ea66c0536bcfab09cd16f5b7284e3fecba29d4d454f00", "size_bytes": 7264}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "03328602a78db17ea128acd2d725483f3465c136ba995d3c885df46173ce5064", "size_bytes": 8217}`, recovered `{"sha256": "b2e08d36f2a0d319451d2331545220514ef1500432acfa0c8a5196052eb36971", "size_bytes": 6850}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "b2e08d36f2a0d319451d2331545220514ef1500432acfa0c8a5196052eb36971", "size_bytes": 6850}`, recovered `{"sha256": "03328602a78db17ea128acd2d725483f3465c136ba995d3c885df46173ce5064", "size_bytes": 8217}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "b2e08d36f2a0d319451d2331545220514ef1500432acfa0c8a5196052eb36971", "size_bytes": 6850}`, recovered `{"sha256": "98803e3e451c1e383899e7e9baa5ae1dd1bba2cfd928fe3d14962e4a0a5e5e3c", "size_bytes": 7818}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "b2e08d36f2a0d319451d2331545220514ef1500432acfa0c8a5196052eb36971", "size_bytes": 6850}`, recovered `{"sha256": "a07b097e2cdf9da7858ea66c0536bcfab09cd16f5b7284e3fecba29d4d454f00", "size_bytes": 7264}`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `rep`: kept `"10"`, recovered `"11"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `rep`: kept `"10"`, recovered `"12"`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `169984`, recovered `210944`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `169984`, recovered `524800`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.input_tokens`: kept `30013`, recovered `30724`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.input_tokens`: kept `30013`, recovered `31170`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.input_tokens`: kept `30013`, recovered `46134`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.input_tokens`: kept `30724`, recovered `30013`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.input_tokens`: kept `30724`, recovered `30013`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.output_tokens`: kept `10531`, recovered `10396`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.output_tokens`: kept `10531`, recovered `12709`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.output_tokens`: kept `10531`, recovered `14769`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.output_tokens`: kept `12709`, recovered `10531`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.output_tokens`: kept `12709`, recovered `10531`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `4706`, recovered `3927`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `4706`, recovered `5665`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `4706`, recovered `6780`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `5665`, recovered `4706`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `5665`, recovered `4706`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `wall_s`: kept `364.507`, recovered `371.72`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `wall_s`: kept `364.507`, recovered `371.72`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `wall_s`: kept `371.72`, recovered `330.691`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `wall_s`: kept `371.72`, recovered `364.507`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1` field `wall_s`: kept `371.72`, recovered `492.595`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"10"`, recovered `"11"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"10"`, recovered `"12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `1.046`, recovered `1.252`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `1.046`, recovered `1.252`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `1.252`, recovered `1.046`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `1.252`, recovered `1.225`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `1.252`, recovered `1.238`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.archive_member.25f2397085a40f776fa23984f268d8f6b82fc6cb8ca874faef14f9389ad560f2`: kept `{"archive_member": null, "sha256": "25f2397085a40f776fa23984f268d8f6b82fc6cb8ca874faef14f9389ad560f2", "size_bytes": 6197}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.archive_member.ae256c054daf8f12aa24faa737bd3ae0c95bc352b6dfb7c1a6c531215f28199b`: kept `{"archive_member": null, "sha256": "ae256c054daf8f12aa24faa737bd3ae0c95bc352b6dfb7c1a6c531215f28199b", "size_bytes": 5682}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "873daa402cefadf60e9f3c265a47b4e8c8b830a9f11e2642ceaec450a5f65829", "size_bytes": 6296}`, recovered `{"sha256": "25f2397085a40f776fa23984f268d8f6b82fc6cb8ca874faef14f9389ad560f2", "size_bytes": 6197}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "873daa402cefadf60e9f3c265a47b4e8c8b830a9f11e2642ceaec450a5f65829", "size_bytes": 6296}`, recovered `{"sha256": "9c3d183a1b5c0e3eb064afdd9dcc37509b0f2f9fb6c888ae1f497a00304859db", "size_bytes": 6468}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "873daa402cefadf60e9f3c265a47b4e8c8b830a9f11e2642ceaec450a5f65829", "size_bytes": 6296}`, recovered `{"sha256": "ae256c054daf8f12aa24faa737bd3ae0c95bc352b6dfb7c1a6c531215f28199b", "size_bytes": 5682}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "9c3d183a1b5c0e3eb064afdd9dcc37509b0f2f9fb6c888ae1f497a00304859db", "size_bytes": 6468}`, recovered `{"sha256": "25f2397085a40f776fa23984f268d8f6b82fc6cb8ca874faef14f9389ad560f2", "size_bytes": 6197}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "9c3d183a1b5c0e3eb064afdd9dcc37509b0f2f9fb6c888ae1f497a00304859db", "size_bytes": 6468}`, recovered `{"sha256": "873daa402cefadf60e9f3c265a47b4e8c8b830a9f11e2642ceaec450a5f65829", "size_bytes": 6296}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `patch.attempt-1`: kept `{"sha256": "9c3d183a1b5c0e3eb064afdd9dcc37509b0f2f9fb6c888ae1f497a00304859db", "size_bytes": 6468}`, recovered `{"sha256": "ae256c054daf8f12aa24faa737bd3ae0c95bc352b6dfb7c1a6c531215f28199b", "size_bytes": 5682}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `188928`, recovered `90112`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `188928`, recovered `90112`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `90112`, recovered `126976`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `90112`, recovered `188928`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.cached_input_tokens`: kept `90112`, recovered `99328`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.input_tokens`: kept `31661`, recovered `24954`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.input_tokens`: kept `31661`, recovered `34148`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.input_tokens`: kept `31661`, recovered `35525`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.input_tokens`: kept `34148`, recovered `31661`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.input_tokens`: kept `34148`, recovered `31661`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.output_tokens`: kept `7664`, recovered `7639`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.output_tokens`: kept `7664`, recovered `8203`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.output_tokens`: kept `7664`, recovered `8416`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.output_tokens`: kept `8416`, recovered `7664`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.output_tokens`: kept `8416`, recovered `7664`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `4041`, recovered `4253`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `4041`, recovered `4762`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `4041`, recovered `4849`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `4762`, recovered `4041`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `usage.reasoning_tokens`: kept `4762`, recovered `4041`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `wall_s`: kept `176.895`, recovered `185.376`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `wall_s`: kept `176.895`, recovered `199.857`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `wall_s`: kept `176.895`, recovered `206.346`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `wall_s`: kept `206.346`, recovered `176.895`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-ls-r1` field `wall_s`: kept `206.346`, recovered `176.895`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.archive_member.d7bd9fbcd0e8b9786542c2988477124b702f697b808d4aecf7f3ae6e38b86ae8`: kept `{"archive_member": null, "sha256": "d7bd9fbcd0e8b9786542c2988477124b702f697b808d4aecf7f3ae6e38b86ae8", "size_bytes": 6883}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.archive_member.fa6566a29d4dd33eeedcd5f975f0fa44af809294ab9965e13033fdc8a87e0f3d`: kept `{"archive_member": null, "sha256": "fa6566a29d4dd33eeedcd5f975f0fa44af809294ab9965e13033fdc8a87e0f3d", "size_bytes": 5974}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "76963b929a843205cc6cc35a99be66bb5a9d344db181f979f9ad1d0cacfe88bc", "size_bytes": 6738}`, recovered `{"sha256": "d65a49a0b47b6906dce6b2714c8237396fb2aba14750a0596e4cc722add36543", "size_bytes": 7179}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "76963b929a843205cc6cc35a99be66bb5a9d344db181f979f9ad1d0cacfe88bc", "size_bytes": 6738}`, recovered `{"sha256": "d7bd9fbcd0e8b9786542c2988477124b702f697b808d4aecf7f3ae6e38b86ae8", "size_bytes": 6883}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "76963b929a843205cc6cc35a99be66bb5a9d344db181f979f9ad1d0cacfe88bc", "size_bytes": 6738}`, recovered `{"sha256": "fa6566a29d4dd33eeedcd5f975f0fa44af809294ab9965e13033fdc8a87e0f3d", "size_bytes": 5974}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "d65a49a0b47b6906dce6b2714c8237396fb2aba14750a0596e4cc722add36543", "size_bytes": 7179}`, recovered `{"sha256": "76963b929a843205cc6cc35a99be66bb5a9d344db181f979f9ad1d0cacfe88bc", "size_bytes": 6738}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "d65a49a0b47b6906dce6b2714c8237396fb2aba14750a0596e4cc722add36543", "size_bytes": 7179}`, recovered `{"sha256": "d7bd9fbcd0e8b9786542c2988477124b702f697b808d4aecf7f3ae6e38b86ae8", "size_bytes": 6883}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `patch.attempt-1`: kept `{"sha256": "d65a49a0b47b6906dce6b2714c8237396fb2aba14750a0596e4cc722add36543", "size_bytes": 7179}`, recovered `{"sha256": "fa6566a29d4dd33eeedcd5f975f0fa44af809294ab9965e13033fdc8a87e0f3d", "size_bytes": 5974}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `rep`: kept `"11"`, recovered `"1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `rep`: kept `"11"`, recovered `"10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `rep`: kept `"11"`, recovered `"12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `157696`, recovered `52224`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `157696`, recovered `52224`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `52224`, recovered `122880`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `52224`, recovered `157696`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.cached_input_tokens`: kept `52224`, recovered `223744`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.input_tokens`: kept `19733`, recovered `24806`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.input_tokens`: kept `19733`, recovered `29290`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.input_tokens`: kept `19733`, recovered `32472`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.input_tokens`: kept `29290`, recovered `19733`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.input_tokens`: kept `29290`, recovered `19733`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.output_tokens`: kept `6826`, recovered `10500`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.output_tokens`: kept `6826`, recovered `9162`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.output_tokens`: kept `6826`, recovered `9387`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.output_tokens`: kept `9387`, recovered `6826`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.output_tokens`: kept `9387`, recovered `6826`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `4253`, recovered `5919`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `4253`, recovered `5973`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `4253`, recovered `6094`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `5919`, recovered `4253`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `usage.reasoning_tokens`: kept `5919`, recovered `4253`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `wall_s`: kept `328.491`, recovered `215.978`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `wall_s`: kept `328.491`, recovered `258.339`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `wall_s`: kept `328.491`, recovered `335.383`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `wall_s`: kept `335.383`, recovered `328.491`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-none-r1` field `wall_s`: kept `335.383`, recovered `328.491`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.archive_member.049ccccecfe1aa6fdcd21c7936afcc10b0bdb62351f75506ccd224a6d633d6e6`: kept `{"archive_member": null, "sha256": "049ccccecfe1aa6fdcd21c7936afcc10b0bdb62351f75506ccd224a6d633d6e6", "size_bytes": 6989}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.archive_member.44ab81a1ac556be76b6861796649c6272adf41f0b960dfa741cf43119d88cacc`: kept `{"archive_member": null, "sha256": "44ab81a1ac556be76b6861796649c6272adf41f0b960dfa741cf43119d88cacc", "size_bytes": 6485}`, recovered `null`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "3d2d786cb9e15454daa89a33fa043a9435fbdcfd38e6e30f3e66d5914c064547", "size_bytes": 6667}`, recovered `{"sha256": "049ccccecfe1aa6fdcd21c7936afcc10b0bdb62351f75506ccd224a6d633d6e6", "size_bytes": 6989}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "3d2d786cb9e15454daa89a33fa043a9435fbdcfd38e6e30f3e66d5914c064547", "size_bytes": 6667}`, recovered `{"sha256": "44ab81a1ac556be76b6861796649c6272adf41f0b960dfa741cf43119d88cacc", "size_bytes": 6485}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "3d2d786cb9e15454daa89a33fa043a9435fbdcfd38e6e30f3e66d5914c064547", "size_bytes": 6667}`, recovered `{"sha256": "f94c402b6ef4c7ec73d33e21936d432c6cb67d6217a089d3ee65a8875b9b0ee0", "size_bytes": 5818}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "f94c402b6ef4c7ec73d33e21936d432c6cb67d6217a089d3ee65a8875b9b0ee0", "size_bytes": 5818}`, recovered `{"sha256": "049ccccecfe1aa6fdcd21c7936afcc10b0bdb62351f75506ccd224a6d633d6e6", "size_bytes": 6989}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "f94c402b6ef4c7ec73d33e21936d432c6cb67d6217a089d3ee65a8875b9b0ee0", "size_bytes": 5818}`, recovered `{"sha256": "3d2d786cb9e15454daa89a33fa043a9435fbdcfd38e6e30f3e66d5914c064547", "size_bytes": 6667}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `patch.attempt-1`: kept `{"sha256": "f94c402b6ef4c7ec73d33e21936d432c6cb67d6217a089d3ee65a8875b9b0ee0", "size_bytes": 5818}`, recovered `{"sha256": "44ab81a1ac556be76b6861796649c6272adf41f0b960dfa741cf43119d88cacc", "size_bytes": 6485}`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `rep`: kept `"11"`, recovered `"1"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `rep`: kept `"11"`, recovered `"10"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `rep`: kept `"11"`, recovered `"12"`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `125440`, recovered `74240`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `125440`, recovered `74240`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `74240`, recovered `103424`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `74240`, recovered `125440`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.cached_input_tokens`: kept `74240`, recovered `90112`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.input_tokens`: kept `25946`, recovered `30440`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.input_tokens`: kept `25946`, recovered `30440`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.input_tokens`: kept `30440`, recovered `21130`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.input_tokens`: kept `30440`, recovered `23809`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.input_tokens`: kept `30440`, recovered `25946`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.output_tokens`: kept `6604`, recovered `7897`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.output_tokens`: kept `6604`, recovered `8038`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.output_tokens`: kept `6604`, recovered `8772`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.output_tokens`: kept `8772`, recovered `6604`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.output_tokens`: kept `8772`, recovered `6604`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `3801`, recovered `4333`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `3801`, recovered `5014`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `3801`, recovered `5320`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `5320`, recovered `3801`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `usage.reasoning_tokens`: kept `5320`, recovered `3801`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `wall_s`: kept `217.883`, recovered `238.75`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `wall_s`: kept `217.883`, recovered `257.255`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `wall_s`: kept `217.883`, recovered `282.935`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `wall_s`: kept `282.935`, recovered `217.883`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1` field `wall_s`: kept `282.935`, recovered `217.883`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 206/289 published metadata totals equal the manifest `input + cached input + output` sum; 83 differ (multi request aggregation 83). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r10-B-ctx-pack-r56p2-studio`: published `747834`, manifest `684712`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r11-B-ctx-pack-r56p2-studio`: published `441519`, manifest `379770`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r12-B-ctx-pack-r56p2-studio`: published `519620`, manifest `477815`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-B-ctx-pack-r56p2-studio`: published `477186`, manifest `421213`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r4-B-ctx-pack-r56p2-studio`: published `511096`, manifest `449106`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r5-B-ctx-pack-r56p2-studio`: published `310658`, manifest `276682`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r6-B-ctx-pack-r56p2-studio`: published `320278`, manifest `284357`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r7-B-ctx-pack-r56p2-studio`: published `470118`, manifest `426883`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r8-B-ctx-pack-r56p2-studio`: published `335773`, manifest `278977`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r9-B-ctx-pack-r56p2-studio`: published `497129`, manifest `456580`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r10-B-ctx-pack-r56p2-studio`: published `1946737`, manifest `1856692`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r11-B-ctx-pack-r56p2-studio`: published `2290924`, manifest `2204591`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r12-B-ctx-pack-r56p2-studio`: published `2445397`, manifest `2335101`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-B-ctx-pack-r56p2-studio`: published `1068383`, manifest `936566`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r4-B-ctx-pack-r56p2-studio`: published `2405462`, manifest `2362271`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r5-B-ctx-pack-r56p2-studio`: published `2124613`, manifest `2051161`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r6-B-ctx-pack-r56p2-studio`: published `2220183`, manifest `2126251`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r7-B-ctx-pack-r56p2-studio`: published `1983839`, manifest `1875047`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r8-B-ctx-pack-r56p2-studio`: published `2329585`, manifest `2277294`, provider responses `36`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r1`: published `1232696`, manifest `1174923`, provider responses `42`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r10`: published `390833`, manifest `361714`, provider responses `19`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r2`: published `519425`, manifest `471177`, provider responses `21`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r3`: published `502926`, manifest `443058`, provider responses `23`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r4`: published `784241`, manifest `757920`, provider responses `32`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r5`: published `464572`, manifest `408350`, provider responses `20`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r6`: published `717938`, manifest `646924`, provider responses `25`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r7`: published `355052`, manifest `325476`, provider responses `20`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r8`: published `360991`, manifest `321783`, provider responses `20`; `multi_request_aggregation`.
- `r56p2-eu-acthrottle-eu-rails-ac-throttle-search-B-ctx-pack-r9`: published `454205`, manifest `398007`, provider responses `22`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r1`: published `677194`, manifest `639455`, provider responses `27`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r10`: published `937634`, manifest `866991`, provider responses `33`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r2`: published `426910`, manifest `378588`, provider responses `18`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r3`: published `667461`, manifest `633089`, provider responses `27`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r4`: published `1137666`, manifest `1096838`, provider responses `39`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r5`: published `640729`, manifest `600189`, provider responses `26`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r6`: published `623160`, manifest `579646`, provider responses `29`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r7`: published `657931`, manifest `619294`, provider responses `28`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r8`: published `986463`, manifest `949781`, provider responses `38`; `multi_request_aggregation`.
- `r56p2-eu-hwbroadcast-eu-rails-hw-scoped-broadcast-B-ctx-pack-r9`: published `1006809`, manifest `978433`, provider responses `38`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r1`: published `229647`, manifest `166007`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r10`: published `174308`, manifest `93830`, provider responses `12`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r2`: published `129616`, manifest `96204`, provider responses `11`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r3`: published `159771`, manifest `89716`, provider responses `10`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r4`: published `116593`, manifest `71479`, provider responses `9`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r5`: published `139851`, manifest `118559`, provider responses `12`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r6`: published `210387`, manifest `159980`, provider responses `13`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r7`: published `147981`, manifest `105426`, provider responses `10`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r8`: published `158801`, manifest `133032`, provider responses `12`; `multi_request_aggregation`.
- `r56p2-us-ajenqueue-us-rails-aj-enqueue-after-commit-B-ctx-pack-r9`: published `213308`, manifest `167112`, provider responses `13`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r1`: published `976518`, manifest `880364`, provider responses `29`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r10`: published `664429`, manifest `608224`, provider responses `23`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r2`: published `666275`, manifest `632324`, provider responses `24`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r3`: published `1864054`, manifest `1828351`, provider responses `43`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r4`: published `1382209`, manifest `1347820`, provider responses `47`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r5`: published `839854`, manifest `778084`, provider responses `24`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r6`: published `1112522`, manifest `1054548`, provider responses `36`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r7`: published `1018487`, manifest `984334`, provider responses `32`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r8`: published `519893`, manifest `465064`, provider responses `21`; `multi_request_aggregation`.
- `r56p2-us-asvariant-us-rails-as-variant-processed-once-B-ctx-pack-r9`: published `1308132`, manifest `1259445`, provider responses `40`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r1`: published `232624`, manifest `213417`, provider responses `13`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r10`: published `511965`, manifest `491811`, provider responses `23`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r11`: published `348551`, manifest `330347`, provider responses `15`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r12`: published `248601`, manifest `228011`, provider responses `13`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r2`: published `274611`, manifest `253702`, provider responses `15`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r3`: published `246794`, manifest `225085`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r4`: published `322360`, manifest `306597`, provider responses `19`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r5`: published `319202`, manifest `300673`, provider responses `16`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r6`: published `404215`, manifest `386818`, provider responses `21`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r7`: published `254449`, manifest `238681`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r8`: published `171503`, manifest `141581`, provider responses `11`; `multi_request_aggregation`.
- `r56p2-us-elx07-us-elx-07-cli-stats-B-ctx-pack-r9`: published `341627`, manifest `320379`, provider responses `18`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r1`: published `205093`, manifest `160158`, provider responses `12`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r10`: published `207942`, manifest `186030`, provider responses `15`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r11`: published `139086`, manifest `118464`, provider responses `12`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r12`: published `426635`, manifest `400433`, provider responses `25`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r2`: published `244567`, manifest `219226`, provider responses `16`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r3`: published `205596`, manifest `181551`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r4`: published `163350`, manifest `145921`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r5`: published `217144`, manifest `202442`, provider responses `15`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r6`: published `209879`, manifest `190309`, provider responses `14`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r7`: published `207048`, manifest `176172`, provider responses `13`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r8`: published `208780`, manifest `195042`, provider responses `18`; `multi_request_aggregation`.
- `r56p2-us-elx12-us-elx-12-retry-api-deprecation-B-ctx-pack-r9`: published `189871`, manifest `169627`, provider responses `14`; `multi_request_aggregation`.
