# r56

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of FILTER, NO_PREREG, OUTCOME_MISMATCH. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README says the adoption criterion was not predeclared in a verifiable registration.
- OUTCOME_MISMATCH — Official outcomes and captured run-record classifications differ.
- FILTER — The source valid-grade filter cannot be reconstructed from the round files.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **46.7%** (222 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Status reason: The official outcome states and the captured run-record classifications differ, and the source valid-grade filter cannot be reconstructed; no adoption test is assessed here.



Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Which individual stages and context options justify their cost?

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Design: Eight tuning tasks; corrected single-stage ablations and builder-context arms. The source note targeted 93 valid reps per arm, but the valid-grade filter cannot be reconstructed from the public record.

Decision rule: The source note proposed adoption only at a gain of at least 15 percentage points with one-sided p<0.05 and at least 93 valid reps in both arms. The public valid-grade filter is not reconstructable, so this criterion is not evaluated.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: 

- [elx-07-cli-stats](../../tasks/elx-07-cli-stats/task.json)
- [elx-12-retry-api-deprecation](../../tasks/elx-12-retry-api-deprecation/task.json)
- [rails-ac-throttle-search](../../tasks/rails-ac-throttle-search/task.json)
- [rails-aj-enqueue-after-commit](../../tasks/rails-aj-enqueue-after-commit/task.json)
- [rails-ar-bulk-access-grants](../../tasks/rails-ar-bulk-access-grants/task.json)
- [rails-as-variant-processed-once](../../tasks/rails-as-variant-processed-once/task.json)
- [rails-ft-mysql-fulltext-search-foundation](../../tasks/rails-ft-mysql-fulltext-search-foundation/task.json)
- [rails-hw-scoped-broadcast](../../tasks/rails-hw-scoped-broadcast/task.json)

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r56.jsonl](../../results/run-records/r56.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56.jsonl](../../results/run-records/r56.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 222 captured deliveries (156 pass, 44 fail, 22 ungraded/unknown in `results/run-records/r56.jsonl`); official outcome export has 200 rows: 156 pass, 44 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this original capture separate from r56b, r56c, r56d and r56p2. The public records do not reproduce the historical validity-filtered analysis or its arm-level adoption tests; retain INTERIM and do not reinstate the old comparison table.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r56.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 200 rows (fail 44, pass 156); overall pass rate is 78.0% (156/200) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 200/200 shared cell IDs match; 0/170 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 313 field mismatches across 10 cell IDs (`manifest_cell_id` 30, `patch.archive_member.0ead9a098cfc36cd92a53d659ed838c79a0f8228e20f5eb591c370d6ade01143` 1, `patch.archive_member.501b9565000642b33d9f41cf62641b3cbb255efb161cc622e34cf9310c58c380` 1, `patch.archive_member.51d18d360fd1b71404507d030b36b587862ac8527330e8945b44df1a811c2c52` 1, `patch.archive_member.5208bb7cf84f349e1ecd20da90c726372e8e2527650568d178afc6b48f43fe83` 1, `patch.archive_member.56187a59917f0a208513d1d0d42b7fca72421e97ad836bbb9ef1259d3b7dd909` 1, `patch.archive_member.5b36fd5d319b8338f1f721d663685fe03e0667c2a59231a1157c3d58aa005583` 1, `patch.archive_member.61dad7c1d4c44c380d2828aca886a3eaf1ec1d34a4ceba120421063b6da6959b` 1, `patch.archive_member.642288a731640177c5d3f9017adb8a194a2aa0a7167bd77796b2fa223f00ca26` 1, `patch.archive_member.6faeddcf56f0715079789d100990a7ad2633d8fd3ee57c342d532d486e75ba14` 1, `patch.archive_member.743663f5952051e997be8e2e4b91f250a02d0cef45c583a2628ecaac8944bca9` 1, `patch.archive_member.768423914ad3c8ea403cd32b739b4869c9ac25560556cb15c92198b03f2ee61a` 1, `patch.archive_member.81916ee15fe365d9747287cddd365be53842f816d93ae81ebb556c44c0d5a0e1` 1, `patch.archive_member.89fd1b5fed743b4c5b54f7be9d8cf64d486923d66c902e7462ddae41c9d9e257` 1, `patch.archive_member.97cabf71249d443746e3c71e193fdb292634f9a3035d6a6be6d1736c8bc758b4` 1, `patch.archive_member.a5fb846b3b6b93617f1435781e35f4476be400df68a5b0938001fc39b323735a` 1, `patch.archive_member.b9f2a25fee17e85c4836b2137ffeb54300ce2cb1f34ab2eb36fb26e764cfc852` 1, `patch.archive_member.c0076a7375bbfe13915b6fdba18325d7f846d9384187ad2f94d8b11a319bc7bf` 1, `patch.archive_member.dacb0dcbbfa7f2aafd64c201a96e659e7287f12f60fa8e49abf93e5586c2c610` 1, `patch.attempt-1` 48, `rep` 30, `status` 1, `usage.cached_input_tokens` 33, `usage.input_tokens` 36, `usage.output_tokens` 36, `usage.reasoning_tokens` 36, `wall_s` 45). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.archive_member.0ead9a098cfc36cd92a53d659ed838c79a0f8228e20f5eb591c370d6ade01143`: kept `{"archive_member": null, "sha256": "0ead9a098cfc36cd92a53d659ed838c79a0f8228e20f5eb591c370d6ade01143", "size_bytes": 29925}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.archive_member.6faeddcf56f0715079789d100990a7ad2633d8fd3ee57c342d532d486e75ba14`: kept `{"archive_member": null, "sha256": "6faeddcf56f0715079789d100990a7ad2633d8fd3ee57c342d532d486e75ba14", "size_bytes": 30099}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "2482dfbf076e2bbc836b8fa89a8c27a3daf0f895e137fb11f7d328ec7d0520c1", "size_bytes": 25891}`, recovered `{"sha256": "0ead9a098cfc36cd92a53d659ed838c79a0f8228e20f5eb591c370d6ade01143", "size_bytes": 29925}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "2482dfbf076e2bbc836b8fa89a8c27a3daf0f895e137fb11f7d328ec7d0520c1", "size_bytes": 25891}`, recovered `{"sha256": "6faeddcf56f0715079789d100990a7ad2633d8fd3ee57c342d532d486e75ba14", "size_bytes": 30099}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "2482dfbf076e2bbc836b8fa89a8c27a3daf0f895e137fb11f7d328ec7d0520c1", "size_bytes": 25891}`, recovered `{"sha256": "cd6e2c73fb6937bb5ea5482fc75ffd4a4d850f8a2f93270926a6750b512454ec", "size_bytes": 11610}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "cd6e2c73fb6937bb5ea5482fc75ffd4a4d850f8a2f93270926a6750b512454ec", "size_bytes": 11610}`, recovered `{"sha256": "0ead9a098cfc36cd92a53d659ed838c79a0f8228e20f5eb591c370d6ade01143", "size_bytes": 29925}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "cd6e2c73fb6937bb5ea5482fc75ffd4a4d850f8a2f93270926a6750b512454ec", "size_bytes": 11610}`, recovered `{"sha256": "2482dfbf076e2bbc836b8fa89a8c27a3daf0f895e137fb11f7d328ec7d0520c1", "size_bytes": 25891}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "cd6e2c73fb6937bb5ea5482fc75ffd4a4d850f8a2f93270926a6750b512454ec", "size_bytes": 11610}`, recovered `{"sha256": "6faeddcf56f0715079789d100990a7ad2633d8fd3ee57c342d532d486e75ba14", "size_bytes": 30099}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `rep`: kept `"11"`, recovered `"1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `rep`: kept `"11"`, recovered `"10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `rep`: kept `"11"`, recovered `"12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.cached_input_tokens`: kept `771584`, recovered `834560`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.cached_input_tokens`: kept `771584`, recovered `834560`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.cached_input_tokens`: kept `834560`, recovered `1006592`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.cached_input_tokens`: kept `834560`, recovered `1220608`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.cached_input_tokens`: kept `834560`, recovered `771584`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.input_tokens`: kept `114134`, recovered `136872`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.input_tokens`: kept `114134`, recovered `139331`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.input_tokens`: kept `114134`, recovered `92008`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.input_tokens`: kept `92008`, recovered `114134`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.input_tokens`: kept `92008`, recovered `114134`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.output_tokens`: kept `24656`, recovered `32995`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.output_tokens`: kept `24656`, recovered `32995`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.output_tokens`: kept `32995`, recovered `24656`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.output_tokens`: kept `32995`, recovered `29384`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.output_tokens`: kept `32995`, recovered `39540`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.reasoning_tokens`: kept `14048`, recovered `21270`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.reasoning_tokens`: kept `14048`, recovered `21270`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.reasoning_tokens`: kept `21270`, recovered `14048`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.reasoning_tokens`: kept `21270`, recovered `18065`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `usage.reasoning_tokens`: kept `21270`, recovered `22438`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `wall_s`: kept `1857.404`, recovered `1882.689`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `wall_s`: kept `1857.404`, recovered `1927.613`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `wall_s`: kept `1857.404`, recovered `2222.696`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `wall_s`: kept `1927.613`, recovered `1857.404`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1` field `wall_s`: kept `1927.613`, recovered `1857.404`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.archive_member.51d18d360fd1b71404507d030b36b587862ac8527330e8945b44df1a811c2c52`: kept `{"archive_member": null, "sha256": "51d18d360fd1b71404507d030b36b587862ac8527330e8945b44df1a811c2c52", "size_bytes": 10421}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.archive_member.89fd1b5fed743b4c5b54f7be9d8cf64d486923d66c902e7462ddae41c9d9e257`: kept `{"archive_member": null, "sha256": "89fd1b5fed743b4c5b54f7be9d8cf64d486923d66c902e7462ddae41c9d9e257", "size_bytes": 12583}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "17b96f0448bd32550f5ff3dd2438578bc6d31b8a57f9dcce3062626c47ec9034", "size_bytes": 12355}`, recovered `{"sha256": "51d18d360fd1b71404507d030b36b587862ac8527330e8945b44df1a811c2c52", "size_bytes": 10421}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "17b96f0448bd32550f5ff3dd2438578bc6d31b8a57f9dcce3062626c47ec9034", "size_bytes": 12355}`, recovered `{"sha256": "5b6b3ef967baf920d5c602c858de647d163e815125576846fc35c3fecbe20213", "size_bytes": 11029}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "17b96f0448bd32550f5ff3dd2438578bc6d31b8a57f9dcce3062626c47ec9034", "size_bytes": 12355}`, recovered `{"sha256": "89fd1b5fed743b4c5b54f7be9d8cf64d486923d66c902e7462ddae41c9d9e257", "size_bytes": 12583}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "5b6b3ef967baf920d5c602c858de647d163e815125576846fc35c3fecbe20213", "size_bytes": 11029}`, recovered `{"sha256": "17b96f0448bd32550f5ff3dd2438578bc6d31b8a57f9dcce3062626c47ec9034", "size_bytes": 12355}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "5b6b3ef967baf920d5c602c858de647d163e815125576846fc35c3fecbe20213", "size_bytes": 11029}`, recovered `{"sha256": "51d18d360fd1b71404507d030b36b587862ac8527330e8945b44df1a811c2c52", "size_bytes": 10421}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "5b6b3ef967baf920d5c602c858de647d163e815125576846fc35c3fecbe20213", "size_bytes": 11029}`, recovered `{"sha256": "89fd1b5fed743b4c5b54f7be9d8cf64d486923d66c902e7462ddae41c9d9e257", "size_bytes": 12583}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.cached_input_tokens`: kept `435200`, recovered `595456`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.cached_input_tokens`: kept `435200`, recovered `595456`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.cached_input_tokens`: kept `595456`, recovered `1153024`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.cached_input_tokens`: kept `595456`, recovered `397824`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.cached_input_tokens`: kept `595456`, recovered `435200`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.input_tokens`: kept `69830`, recovered `75191`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.input_tokens`: kept `69830`, recovered `75191`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.input_tokens`: kept `75191`, recovered `126489`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.input_tokens`: kept `75191`, recovered `69830`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.input_tokens`: kept `75191`, recovered `91664`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.output_tokens`: kept `20679`, recovered `24653`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.output_tokens`: kept `20679`, recovered `24653`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.output_tokens`: kept `24653`, recovered `20275`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.output_tokens`: kept `24653`, recovered `20679`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.output_tokens`: kept `24653`, recovered `39741`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.reasoning_tokens`: kept `11446`, recovered `13417`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.reasoning_tokens`: kept `11446`, recovered `13417`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.reasoning_tokens`: kept `13417`, recovered `10813`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.reasoning_tokens`: kept `13417`, recovered `11446`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `usage.reasoning_tokens`: kept `13417`, recovered `21123`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `wall_s`: kept `1054.255`, recovered `1067.416`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `wall_s`: kept `1054.255`, recovered `1176.833`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `wall_s`: kept `1054.255`, recovered `1667.881`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `wall_s`: kept `1176.833`, recovered `1054.255`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1` field `wall_s`: kept `1176.833`, recovered `1054.255`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.archive_member.5208bb7cf84f349e1ecd20da90c726372e8e2527650568d178afc6b48f43fe83`: kept `{"archive_member": null, "sha256": "5208bb7cf84f349e1ecd20da90c726372e8e2527650568d178afc6b48f43fe83", "size_bytes": 30832}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.archive_member.81916ee15fe365d9747287cddd365be53842f816d93ae81ebb556c44c0d5a0e1`: kept `{"archive_member": null, "sha256": "81916ee15fe365d9747287cddd365be53842f816d93ae81ebb556c44c0d5a0e1", "size_bytes": 29354}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.archive_member.a5fb846b3b6b93617f1435781e35f4476be400df68a5b0938001fc39b323735a`: kept `{"archive_member": null, "sha256": "a5fb846b3b6b93617f1435781e35f4476be400df68a5b0938001fc39b323735a", "size_bytes": 28607}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "5208bb7cf84f349e1ecd20da90c726372e8e2527650568d178afc6b48f43fe83", "size_bytes": 30832}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "5208bb7cf84f349e1ecd20da90c726372e8e2527650568d178afc6b48f43fe83", "size_bytes": 30832}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "81916ee15fe365d9747287cddd365be53842f816d93ae81ebb556c44c0d5a0e1", "size_bytes": 29354}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "81916ee15fe365d9747287cddd365be53842f816d93ae81ebb556c44c0d5a0e1", "size_bytes": 29354}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "a5fb846b3b6b93617f1435781e35f4476be400df68a5b0938001fc39b323735a", "size_bytes": 28607}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "1f159ccc06f7ccd03d6b6eec569524836b15e036c7d24c134c181afef8af169e", "size_bytes": 27472}`, recovered `{"sha256": "a5fb846b3b6b93617f1435781e35f4476be400df68a5b0938001fc39b323735a", "size_bytes": 28607}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.cached_input_tokens`: kept `1335296`, recovered `1117184`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.cached_input_tokens`: kept `1335296`, recovered `1586688`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.cached_input_tokens`: kept `1335296`, recovered `1945088`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.input_tokens`: kept `141766`, recovered `127482`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.input_tokens`: kept `141766`, recovered `150042`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.input_tokens`: kept `141766`, recovered `160220`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.output_tokens`: kept `43898`, recovered `37147`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.output_tokens`: kept `43898`, recovered `40080`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.output_tokens`: kept `43898`, recovered `42977`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.reasoning_tokens`: kept `29430`, recovered `25582`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.reasoning_tokens`: kept `29430`, recovered `25607`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `usage.reasoning_tokens`: kept `29430`, recovered `27850`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `wall_s`: kept `1909.464`, recovered `1864.259`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `wall_s`: kept `1909.464`, recovered `1934.93`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1` field `wall_s`: kept `1909.464`, recovered `1998.074`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `rep`: kept `"11"`, recovered `"1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `rep`: kept `"11"`, recovered `"10"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `rep`: kept `"11"`, recovered `"12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `wall_s`: kept `0.657`, recovered `0.815`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `wall_s`: kept `0.657`, recovered `0.815`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `wall_s`: kept `0.815`, recovered `0.657`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan-r1` field `wall_s`: kept `0.815`, recovered `0.688`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.archive_member.c0076a7375bbfe13915b6fdba18325d7f846d9384187ad2f94d8b11a319bc7bf`: kept `{"archive_member": null, "sha256": "c0076a7375bbfe13915b6fdba18325d7f846d9384187ad2f94d8b11a319bc7bf", "size_bytes": 29510}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.archive_member.dacb0dcbbfa7f2aafd64c201a96e659e7287f12f60fa8e49abf93e5586c2c610`: kept `{"archive_member": null, "sha256": "dacb0dcbbfa7f2aafd64c201a96e659e7287f12f60fa8e49abf93e5586c2c610", "size_bytes": 25746}`, recovered `null`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "dc68913a108ea8f58baf8d01acb0e2c9ae18da65fe470994156f529138057584", "size_bytes": 13233}`, recovered `{"sha256": "c0076a7375bbfe13915b6fdba18325d7f846d9384187ad2f94d8b11a319bc7bf", "size_bytes": 29510}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "dc68913a108ea8f58baf8d01acb0e2c9ae18da65fe470994156f529138057584", "size_bytes": 13233}`, recovered `{"sha256": "dacb0dcbbfa7f2aafd64c201a96e659e7287f12f60fa8e49abf93e5586c2c610", "size_bytes": 25746}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "dc68913a108ea8f58baf8d01acb0e2c9ae18da65fe470994156f529138057584", "size_bytes": 13233}`, recovered `{"sha256": "fa1013dfd0fe7ebe683c50e734e7f4ac9860415380adcb1aaa75f9186262eb37", "size_bytes": 26259}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "fa1013dfd0fe7ebe683c50e734e7f4ac9860415380adcb1aaa75f9186262eb37", "size_bytes": 26259}`, recovered `{"sha256": "c0076a7375bbfe13915b6fdba18325d7f846d9384187ad2f94d8b11a319bc7bf", "size_bytes": 29510}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "fa1013dfd0fe7ebe683c50e734e7f4ac9860415380adcb1aaa75f9186262eb37", "size_bytes": 26259}`, recovered `{"sha256": "dacb0dcbbfa7f2aafd64c201a96e659e7287f12f60fa8e49abf93e5586c2c610", "size_bytes": 25746}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "fa1013dfd0fe7ebe683c50e734e7f4ac9860415380adcb1aaa75f9186262eb37", "size_bytes": 26259}`, recovered `{"sha256": "dc68913a108ea8f58baf8d01acb0e2c9ae18da65fe470994156f529138057584", "size_bytes": 13233}`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `rep`: kept `"10"`, recovered `"11"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `rep`: kept `"10"`, recovered `"12"`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.cached_input_tokens`: kept `288256`, recovered `243712`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.cached_input_tokens`: kept `288256`, recovered `355328`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.input_tokens`: kept `39671`, recovered `48532`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.input_tokens`: kept `39671`, recovered `48532`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.input_tokens`: kept `48532`, recovered `33268`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.input_tokens`: kept `48532`, recovered `38879`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.input_tokens`: kept `48532`, recovered `39671`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.output_tokens`: kept `12340`, recovered `14585`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.output_tokens`: kept `12340`, recovered `14585`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.output_tokens`: kept `14585`, recovered `10509`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.output_tokens`: kept `14585`, recovered `12340`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.output_tokens`: kept `14585`, recovered `9637`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.reasoning_tokens`: kept `5380`, recovered `7770`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.reasoning_tokens`: kept `5380`, recovered `7770`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.reasoning_tokens`: kept `7770`, recovered `3944`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.reasoning_tokens`: kept `7770`, recovered `4751`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `usage.reasoning_tokens`: kept `7770`, recovered `5380`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `wall_s`: kept `1000.614`, recovered `1006.618`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `wall_s`: kept `1000.614`, recovered `1112.87`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `wall_s`: kept `1000.614`, recovered `939.519`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `wall_s`: kept `939.519`, recovered `1000.614`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1` field `wall_s`: kept `939.519`, recovered `1000.614`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.archive_member.642288a731640177c5d3f9017adb8a194a2aa0a7167bd77796b2fa223f00ca26`: kept `{"archive_member": null, "sha256": "642288a731640177c5d3f9017adb8a194a2aa0a7167bd77796b2fa223f00ca26", "size_bytes": 27752}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.archive_member.b9f2a25fee17e85c4836b2137ffeb54300ce2cb1f34ab2eb36fb26e764cfc852`: kept `{"archive_member": null, "sha256": "b9f2a25fee17e85c4836b2137ffeb54300ce2cb1f34ab2eb36fb26e764cfc852", "size_bytes": 13069}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "516f5ab77cf546362697a39c86c5458b54e21bce1241d907ee1dbc63a903f4ae", "size_bytes": 28015}`, recovered `{"sha256": "642288a731640177c5d3f9017adb8a194a2aa0a7167bd77796b2fa223f00ca26", "size_bytes": 27752}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "516f5ab77cf546362697a39c86c5458b54e21bce1241d907ee1dbc63a903f4ae", "size_bytes": 28015}`, recovered `{"sha256": "b9f2a25fee17e85c4836b2137ffeb54300ce2cb1f34ab2eb36fb26e764cfc852", "size_bytes": 13069}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "516f5ab77cf546362697a39c86c5458b54e21bce1241d907ee1dbc63a903f4ae", "size_bytes": 28015}`, recovered `{"sha256": "bff16023286612ca42003ab1c04dfdc700af517fb136a3c1cd9a7caff6e023e8", "size_bytes": 27171}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "bff16023286612ca42003ab1c04dfdc700af517fb136a3c1cd9a7caff6e023e8", "size_bytes": 27171}`, recovered `{"sha256": "516f5ab77cf546362697a39c86c5458b54e21bce1241d907ee1dbc63a903f4ae", "size_bytes": 28015}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "bff16023286612ca42003ab1c04dfdc700af517fb136a3c1cd9a7caff6e023e8", "size_bytes": 27171}`, recovered `{"sha256": "642288a731640177c5d3f9017adb8a194a2aa0a7167bd77796b2fa223f00ca26", "size_bytes": 27752}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `patch.attempt-1`: kept `{"sha256": "bff16023286612ca42003ab1c04dfdc700af517fb136a3c1cd9a7caff6e023e8", "size_bytes": 27171}`, recovered `{"sha256": "b9f2a25fee17e85c4836b2137ffeb54300ce2cb1f34ab2eb36fb26e764cfc852", "size_bytes": 13069}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.cached_input_tokens`: kept `388608`, recovered `482304`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.cached_input_tokens`: kept `388608`, recovered `482304`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.cached_input_tokens`: kept `482304`, recovered `388608`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.cached_input_tokens`: kept `482304`, recovered `391168`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.cached_input_tokens`: kept `482304`, recovered `496128`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.input_tokens`: kept `47314`, recovered `49458`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.input_tokens`: kept `47314`, recovered `49458`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.input_tokens`: kept `49458`, recovered `43372`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.input_tokens`: kept `49458`, recovered `47314`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.input_tokens`: kept `49458`, recovered `52193`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.output_tokens`: kept `13341`, recovered `14015`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.output_tokens`: kept `13341`, recovered `14623`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.output_tokens`: kept `13341`, recovered `15181`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.output_tokens`: kept `14015`, recovered `13341`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.output_tokens`: kept `14015`, recovered `13341`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.reasoning_tokens`: kept `6393`, recovered `6496`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.reasoning_tokens`: kept `6393`, recovered `6496`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.reasoning_tokens`: kept `6496`, recovered `5952`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.reasoning_tokens`: kept `6496`, recovered `6393`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `usage.reasoning_tokens`: kept `6496`, recovered `7945`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `wall_s`: kept `1319.625`, recovered `1479.798`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `wall_s`: kept `1319.625`, recovered `1547.629`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `wall_s`: kept `1319.625`, recovered `1577.285`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `wall_s`: kept `1577.285`, recovered `1319.625`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1` field `wall_s`: kept `1577.285`, recovered `1319.625`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.archive_member.743663f5952051e997be8e2e4b91f250a02d0cef45c583a2628ecaac8944bca9`: kept `{"archive_member": null, "sha256": "743663f5952051e997be8e2e4b91f250a02d0cef45c583a2628ecaac8944bca9", "size_bytes": 12806}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.archive_member.97cabf71249d443746e3c71e193fdb292634f9a3035d6a6be6d1736c8bc758b4`: kept `{"archive_member": null, "sha256": "97cabf71249d443746e3c71e193fdb292634f9a3035d6a6be6d1736c8bc758b4", "size_bytes": 12779}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "d03731d5fb32b62124ebf87d1770ae3afa707669b67d958a81c5da5990108b28", "size_bytes": 12317}`, recovered `{"sha256": "743663f5952051e997be8e2e4b91f250a02d0cef45c583a2628ecaac8944bca9", "size_bytes": 12806}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "d03731d5fb32b62124ebf87d1770ae3afa707669b67d958a81c5da5990108b28", "size_bytes": 12317}`, recovered `{"sha256": "97cabf71249d443746e3c71e193fdb292634f9a3035d6a6be6d1736c8bc758b4", "size_bytes": 12779}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "d03731d5fb32b62124ebf87d1770ae3afa707669b67d958a81c5da5990108b28", "size_bytes": 12317}`, recovered `{"sha256": "fd4756856b3f9cd258a9b59b21242b46c0fe95a57900533349675d562b872625", "size_bytes": 13034}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "fd4756856b3f9cd258a9b59b21242b46c0fe95a57900533349675d562b872625", "size_bytes": 13034}`, recovered `{"sha256": "743663f5952051e997be8e2e4b91f250a02d0cef45c583a2628ecaac8944bca9", "size_bytes": 12806}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "fd4756856b3f9cd258a9b59b21242b46c0fe95a57900533349675d562b872625", "size_bytes": 13034}`, recovered `{"sha256": "97cabf71249d443746e3c71e193fdb292634f9a3035d6a6be6d1736c8bc758b4", "size_bytes": 12779}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `patch.attempt-1`: kept `{"sha256": "fd4756856b3f9cd258a9b59b21242b46c0fe95a57900533349675d562b872625", "size_bytes": 13034}`, recovered `{"sha256": "d03731d5fb32b62124ebf87d1770ae3afa707669b67d958a81c5da5990108b28", "size_bytes": 12317}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.cached_input_tokens`: kept `375296`, recovered `823808`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.cached_input_tokens`: kept `375296`, recovered `823808`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.cached_input_tokens`: kept `823808`, recovered `375296`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.cached_input_tokens`: kept `823808`, recovered `647168`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.cached_input_tokens`: kept `823808`, recovered `712704`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.input_tokens`: kept `72340`, recovered `53922`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.input_tokens`: kept `72340`, recovered `56757`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.input_tokens`: kept `72340`, recovered `88763`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.input_tokens`: kept `88763`, recovered `72340`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.input_tokens`: kept `88763`, recovered `72340`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.output_tokens`: kept `17129`, recovered `18836`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.output_tokens`: kept `17129`, recovered `18836`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.output_tokens`: kept `18836`, recovered `17129`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.output_tokens`: kept `18836`, recovered `19836`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.output_tokens`: kept `18836`, recovered `21469`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.reasoning_tokens`: kept `7757`, recovered `7989`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.reasoning_tokens`: kept `7757`, recovered `8263`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.reasoning_tokens`: kept `7757`, recovered `9016`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.reasoning_tokens`: kept `7989`, recovered `7757`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `usage.reasoning_tokens`: kept `7989`, recovered `7757`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `wall_s`: kept `893.944`, recovered `949.237`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `wall_s`: kept `893.944`, recovered `949.237`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `wall_s`: kept `949.237`, recovered `1140.445`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `wall_s`: kept `949.237`, recovered `1191.152`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1` field `wall_s`: kept `949.237`, recovered `893.944`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.archive_member.5b36fd5d319b8338f1f721d663685fe03e0667c2a59231a1157c3d58aa005583`: kept `{"archive_member": null, "sha256": "5b36fd5d319b8338f1f721d663685fe03e0667c2a59231a1157c3d58aa005583", "size_bytes": 29187}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.archive_member.61dad7c1d4c44c380d2828aca886a3eaf1ec1d34a4ceba120421063b6da6959b`: kept `{"archive_member": null, "sha256": "61dad7c1d4c44c380d2828aca886a3eaf1ec1d34a4ceba120421063b6da6959b", "size_bytes": 15407}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "755f943c6497bd68cb05f930e2f921e0e8a686bd6f031f8393b6b83981049844", "size_bytes": 29029}`, recovered `{"sha256": "5b36fd5d319b8338f1f721d663685fe03e0667c2a59231a1157c3d58aa005583", "size_bytes": 29187}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "755f943c6497bd68cb05f930e2f921e0e8a686bd6f031f8393b6b83981049844", "size_bytes": 29029}`, recovered `{"sha256": "61dad7c1d4c44c380d2828aca886a3eaf1ec1d34a4ceba120421063b6da6959b", "size_bytes": 15407}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "755f943c6497bd68cb05f930e2f921e0e8a686bd6f031f8393b6b83981049844", "size_bytes": 29029}`, recovered `{"sha256": "c8a0a5a69e98f0397b0e641ff052adcb152d4013f57f5c4fc08d230ee5998570", "size_bytes": 28017}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "c8a0a5a69e98f0397b0e641ff052adcb152d4013f57f5c4fc08d230ee5998570", "size_bytes": 28017}`, recovered `{"sha256": "5b36fd5d319b8338f1f721d663685fe03e0667c2a59231a1157c3d58aa005583", "size_bytes": 29187}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "c8a0a5a69e98f0397b0e641ff052adcb152d4013f57f5c4fc08d230ee5998570", "size_bytes": 28017}`, recovered `{"sha256": "61dad7c1d4c44c380d2828aca886a3eaf1ec1d34a4ceba120421063b6da6959b", "size_bytes": 15407}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `patch.attempt-1`: kept `{"sha256": "c8a0a5a69e98f0397b0e641ff052adcb152d4013f57f5c4fc08d230ee5998570", "size_bytes": 28017}`, recovered `{"sha256": "755f943c6497bd68cb05f930e2f921e0e8a686bd6f031f8393b6b83981049844", "size_bytes": 29029}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `rep`: kept `"10"`, recovered `"11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `rep`: kept `"10"`, recovered `"12"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `status`: kept `"ok"`, recovered `"timeout"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.cached_input_tokens`: kept `681984`, recovered `2812928`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.cached_input_tokens`: kept `681984`, recovered `595456`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.cached_input_tokens`: kept `681984`, recovered `764928`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.cached_input_tokens`: kept `764928`, recovered `681984`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.cached_input_tokens`: kept `764928`, recovered `681984`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.input_tokens`: kept `60664`, recovered `63447`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.input_tokens`: kept `60664`, recovered `63447`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.input_tokens`: kept `63447`, recovered `320683`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.input_tokens`: kept `63447`, recovered `60664`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.input_tokens`: kept `63447`, recovered `70930`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.output_tokens`: kept `14025`, recovered `14650`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.output_tokens`: kept `14025`, recovered `22014`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.output_tokens`: kept `14025`, recovered `60539`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.output_tokens`: kept `14650`, recovered `14025`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.output_tokens`: kept `14650`, recovered `14025`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.reasoning_tokens`: kept `6578`, recovered `10554`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.reasoning_tokens`: kept `6578`, recovered `40772`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.reasoning_tokens`: kept `6578`, recovered `7727`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.reasoning_tokens`: kept `7727`, recovered `6578`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `usage.reasoning_tokens`: kept `7727`, recovered `6578`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `wall_s`: kept `1185.553`, recovered `1240.734`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `wall_s`: kept `1185.553`, recovered `1240.734`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `wall_s`: kept `1240.734`, recovered `1185.553`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `wall_s`: kept `1240.734`, recovered `1396.768`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1` field `wall_s`: kept `1240.734`, recovered `2555.849`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `rep`: kept `"12"`, recovered `"1"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `rep`: kept `"12"`, recovered `"10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `rep`: kept `"12"`, recovered `"11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `wall_s`: kept `0.81`, recovered `0.809`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `wall_s`: kept `0.81`, recovered `0.815`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `wall_s`: kept `0.81`, recovered `1.018`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `wall_s`: kept `1.018`, recovered `0.81`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noplan-r1` field `wall_s`: kept `1.018`, recovered `0.81`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.archive_member.501b9565000642b33d9f41cf62641b3cbb255efb161cc622e34cf9310c58c380`: kept `{"archive_member": null, "sha256": "501b9565000642b33d9f41cf62641b3cbb255efb161cc622e34cf9310c58c380", "size_bytes": 13628}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.archive_member.56187a59917f0a208513d1d0d42b7fca72421e97ad836bbb9ef1259d3b7dd909`: kept `{"archive_member": null, "sha256": "56187a59917f0a208513d1d0d42b7fca72421e97ad836bbb9ef1259d3b7dd909", "size_bytes": 23012}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.archive_member.768423914ad3c8ea403cd32b739b4869c9ac25560556cb15c92198b03f2ee61a`: kept `{"archive_member": null, "sha256": "768423914ad3c8ea403cd32b739b4869c9ac25560556cb15c92198b03f2ee61a", "size_bytes": 27791}`, recovered `null`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "501b9565000642b33d9f41cf62641b3cbb255efb161cc622e34cf9310c58c380", "size_bytes": 13628}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "501b9565000642b33d9f41cf62641b3cbb255efb161cc622e34cf9310c58c380", "size_bytes": 13628}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "56187a59917f0a208513d1d0d42b7fca72421e97ad836bbb9ef1259d3b7dd909", "size_bytes": 23012}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "56187a59917f0a208513d1d0d42b7fca72421e97ad836bbb9ef1259d3b7dd909", "size_bytes": 23012}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "768423914ad3c8ea403cd32b739b4869c9ac25560556cb15c92198b03f2ee61a", "size_bytes": 27791}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `patch.attempt-1`: kept `{"sha256": "74703734a6facfcc0cccaf95eb2ba92885d42c94eb2f4df185af50ebe5d03955", "size_bytes": 23797}`, recovered `{"sha256": "768423914ad3c8ea403cd32b739b4869c9ac25560556cb15c92198b03f2ee61a", "size_bytes": 27791}`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.cached_input_tokens`: kept `467456`, recovered `465920`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.cached_input_tokens`: kept `467456`, recovered `573952`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.cached_input_tokens`: kept `467456`, recovered `761344`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.input_tokens`: kept `49028`, recovered `50246`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.input_tokens`: kept `49028`, recovered `59622`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.input_tokens`: kept `49028`, recovered `59856`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.output_tokens`: kept `15463`, recovered `15596`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.output_tokens`: kept `15463`, recovered `17567`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.output_tokens`: kept `15463`, recovered `18505`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.reasoning_tokens`: kept `5674`, recovered `5670`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.reasoning_tokens`: kept `5674`, recovered `5749`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `usage.reasoning_tokens`: kept `5674`, recovered `5858`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `wall_s`: kept `1117.692`, recovered `1193.62`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `wall_s`: kept `1117.692`, recovered `1265.196`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1` field `wall_s`: kept `1117.692`, recovered `1343.421`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 35/176 published metadata totals equal the manifest `input + cached input + output` sum; 141 differ (multi request aggregation 141). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-B-ctx-pack-r56-studio`: published `335188`, manifest `293110`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56-studio`: published `1698826`, manifest `760470`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56-studio`: published `3067572`, manifest `2290782`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56-studio`: published `1042549`, manifest `404711`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-B-ctx-pack-r56-studio`: published `232586`, manifest `208561`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-full-r56-studio`: published `2104548`, manifest `1055915`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-nocontract-r56-studio`: published `2972811`, manifest `1878994`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-noreview-r56-studio`: published `1264903`, manifest `374956`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-B-ctx-pack-r56-studio`: published `271774`, manifest `217190`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56-studio`: published `1411420`, manifest `582150`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56-studio`: published `1220995`, manifest `595794`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56-studio`: published `2607601`, manifest `1651666`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-B-ctx-pack-r56-studio`: published `157516`, manifest `119716`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-full-r56-studio`: published `2020220`, manifest `1218599`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-nocontract-r56-studio`: published `1280491`, manifest `783473`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-noreview-r56-studio`: published `971075`, manifest `272830`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-B-ctx-pack-r56-studio`: published `547701`, manifest `488565`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56-studio`: published `1789043`, manifest `618590`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56-studio`: published `2477298`, manifest `1654192`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56-studio`: published `3205588`, manifest `2250385`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-B-ctx-pack-r56-studio`: published `235557`, manifest `186468`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-full-r56-studio`: published `2125831`, manifest `1308422`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-nocontract-r56-studio`: published `1212270`, manifest `759905`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-noreview-r56-studio`: published `2108618`, manifest `1531087`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-B-ctx-pack-r56-studio`: published `926792`, manifest `840276`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56-studio`: published `3025377`, manifest `1552378`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56-studio`: published `1287468`, manifest `505121`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56-studio`: published `1307860`, manifest `497616`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-B-ctx-pack-r56-studio`: published `1388521`, manifest `1279912`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-full-r56-studio`: published `2040450`, manifest `555852`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-nocontract-r56-studio`: published `1674959`, manifest `791284`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-noreview-r56-studio`: published `1749697`, manifest `561352`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-B-ctx-pack-r56-studio`: published `1680942`, manifest `1608218`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-full-r56-studio`: published `4364869`, manifest `3078724`, provider responses `54`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56-studio`: published `3275284`, manifest `2414131`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-B-ctx-pack-r56-studio`: published `2230660`, manifest `2126208`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-full-r56-studio`: published `4023127`, manifest `2785844`, provider responses `60`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-B-ctx-pack-r56-studio`: published `728309`, manifest `646873`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56-studio`: published `1197760`, manifest `311976`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56-studio`: published `1773750`, manifest `1034494`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56-studio-fix`: published `2265843`, manifest `1592199`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-B-ctx-pack-r56-studio`: published `1465489`, manifest `1416782`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-full-r56-studio`: published `1634386`, manifest `797436`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-nocontract-r56-studio`: published `2058601`, manifest `1003039`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-noreview-r56-studio`: published `1965629`, manifest `1176305`, provider responses `37`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r1`: published `1305308`, manifest `888248`, provider responses `45`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r10`: published `2306156`, manifest `1861647`, provider responses `69`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r11`: published `1587283`, manifest `1119306`, provider responses `50`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r12`: published `1767648`, manifest `1359692`, provider responses `68`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r2`: published `1454202`, manifest `988506`, provider responses `55`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r3`: published `1568556`, manifest `968602`, provider responses `40`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r4`: published `1443439`, manifest `887902`, provider responses `44`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r5`: published `1596566`, manifest `1074147`, provider responses `55`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r6`: published `1004975`, manifest `648535`, provider responses `40`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r7`: published `2576726`, manifest `2019116`, provider responses `72`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r8`: published `1382810`, manifest `993645`, provider responses `53`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-full-r9`: published `1352599`, manifest `822099`, provider responses `40`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r1`: published `786591`, manifest `525709`, provider responses `32`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r10`: published `1245587`, manifest `781824`, provider responses `42`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r11`: published `926870`, manifest `679468`, provider responses `37`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r12`: published `1441020`, manifest `1128348`, provider responses `62`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r2`: published `870391`, manifest `598384`, provider responses `38`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r3`: published `868484`, manifest `621297`, provider responses `35`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r4`: published `935842`, manifest `730950`, provider responses `37`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r5`: published `2213422`, manifest `1891837`, provider responses `75`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r6`: published `968457`, manifest `729920`, provider responses `35`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r7`: published `1206454`, manifest `949821`, provider responses `48`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r8`: published `1065463`, manifest `787259`, provider responses `45`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-nocontract-r9`: published `1375318`, manifest `1150965`, provider responses `54`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r1`: published `2241024`, manifest `1520960`, provider responses `61`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r10`: published `3008667`, manifest `2537477`, provider responses `82`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r11`: published `1928632`, manifest `1507912`, provider responses `64`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r12`: published `3557613`, manifest `3074443`, provider responses `94`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r2`: published `2363894`, manifest `1864989`, provider responses `74`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r3`: published `2576298`, manifest `1962423`, provider responses `68`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r4`: published `2195639`, manifest `1767671`, provider responses `57`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r5`: published `5014976`, manifest `4658047`, provider responses `105`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r6`: published `1963269`, manifest `1521483`, provider responses `58`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r7`: published `2404790`, manifest `1840100`, provider responses `69`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r8`: published `1959123`, manifest `1606136`, provider responses `77`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noctx2-r9`: published `2749380`, manifest `2262670`, provider responses `72`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r1`: published `527025`, manifest `340267`, provider responses `20`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r10`: published `797563`, manifest `444724`, provider responses `27`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r11`: published `1050388`, manifest `734926`, provider responses `33`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r12`: published `1083945`, manifest `725456`, provider responses `30`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r2`: published `1059241`, manifest `731395`, provider responses `32`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r3`: published `692595`, manifest `420880`, provider responses `26`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r4`: published `952472`, manifest `695357`, provider responses `31`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r5`: published `538541`, manifest `173759`, provider responses `14`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r6`: published `781778`, manifest `362743`, provider responses `20`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r7`: published `1058548`, manifest `562515`, provider responses `25`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r8`: published `832504`, manifest `563139`, provider responses `30`; `multi_request_aggregation`.
- `r56-eu-elx12-eu-elx-12-retry-api-deprecation-P-noreview-r9`: published `954714`, manifest `630572`, provider responses `24`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r1`: published `1076306`, manifest `449937`, provider responses `22`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r10`: published `1379880`, manifest `885410`, provider responses `34`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r11`: published `1039382`, manifest `580190`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r12`: published `1124948`, manifest `573072`, provider responses `29`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r2`: published `848280`, manifest `533365`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r3`: published `1955707`, manifest `1201717`, provider responses `56`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r4`: published `1442656`, manifest `1074655`, provider responses `39`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r5`: published `832809`, manifest `371790`, provider responses `20`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r6`: published `1133528`, manifest `745667`, provider responses `30`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r7`: published `1372662`, manifest `689506`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r8`: published `1235220`, manifest `743550`, provider responses `29`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-full-r9`: published `1226081`, manifest `827101`, provider responses `31`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r1`: published `708545`, manifest `481188`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r10`: published `1275301`, manifest `851945`, provider responses `36`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r11`: published `797318`, manifest `615912`, provider responses `32`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r12`: published `928535`, manifest `663992`, provider responses `33`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r2`: published `606548`, manifest `412230`, provider responses `23`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r3`: published `764595`, manifest `599457`, provider responses `30`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r4`: published `929292`, manifest `529989`, provider responses `28`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r5`: published `896701`, manifest `585320`, provider responses `32`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r6`: published `931786`, manifest `772068`, provider responses `35`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r7`: published `643030`, manifest `452130`, provider responses `25`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r8`: published `884121`, manifest `661302`, provider responses `28`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-nocontract-r9`: published `623609`, manifest `463454`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r1`: published `1151764`, manifest `840242`, provider responses `33`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r10`: published `1090368`, manifest `773783`, provider responses `30`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r11`: published `1900153`, manifest `1458888`, provider responses `37`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r12`: published `1053384`, manifest `690586`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r2`: published `1157562`, manifest `877887`, provider responses `34`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r3`: published `1065397`, manifest `829522`, provider responses `33`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r4`: published `2177300`, manifest `1720348`, provider responses `66`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r5`: published `1452964`, manifest `1124916`, provider responses `47`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r6`: published `1996645`, manifest `1577581`, provider responses `53`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r7`: published `784662`, manifest `549558`, provider responses `25`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r8`: published `1160404`, manifest `790672`, provider responses `30`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noctx2-r9`: published `1017153`, manifest `722630`, provider responses `30`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r1`: published `884623`, manifest `531947`, provider responses `24`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r10`: published `953278`, manifest `574655`, provider responses `31`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r11`: published `1556020`, manifest `1080110`, provider responses `39`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r12`: published `1286529`, manifest `947035`, provider responses `38`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r2`: published `2183601`, manifest `1574092`, provider responses `49`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r3`: published `1076539`, manifest `787135`, provider responses `33`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r4`: published `701860`, manifest `360174`, provider responses `23`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r5`: published `1703293`, manifest `1409079`, provider responses `46`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r6`: published `1173764`, manifest `677361`, provider responses `29`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r7`: published `1641793`, manifest `1210834`, provider responses `42`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r8`: published `1026814`, manifest `580387`, provider responses `26`; `multi_request_aggregation`.
- `r56-us-elx07-us-elx-07-cli-stats-P-noreview-r9`: published `1006739`, manifest `611874`, provider responses `29`; `multi_request_aggregation`.
