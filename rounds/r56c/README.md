# r56c

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DESIGN, ENVIRONMENT, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No public predeclared decision rule was recovered.
- DESIGN — The dedicated design section and complete comparison protocol are absent.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **49.0%** (128 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r56c.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-07-cli-stats | kogen-bench-us | B-ctx-det | not re-derivable | 12 | 12 | 7 | 5 | 0 |
| elx-07-cli-stats | kogen-bench-us | P-noplan2 | not re-derivable | 12 | 12 | 8 | 4 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | P-noplan2 | not re-derivable | 12 | 12 | 6 | 6 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-us | B-ctx-det | not re-derivable | 12 | 12 | 2 | 10 | 0 |
| rails-ac-throttle-search | studio | P-noplan2 | not re-derivable | 12 | 12 | 11 | 1 | 0 |
| rails-aj-enqueue-after-commit | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |
| rails-as-variant-processed-once | kogen-bench-us | B-ctx-det | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-as-variant-processed-once | studio | P-noplan2 | not re-derivable | 12 | 12 | 9 | 3 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | P-noplan2 | not re-derivable | 12 | 11 | 10 | 1 | 0 |
| rails-hw-scoped-broadcast | kogen-bench-eu | B-ctx-det | not re-derivable | 6 | 6 | 6 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | P-noplan2 | not re-derivable | 12 | 12 | 12 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56c`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56c.jsonl](../../results/run-records/r56c.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 128 captured deliveries (95 pass, 32 fail, 1 ungraded/unknown in `results/run-records/r56c.jsonl`); official outcome export has 127 rows: 95 pass, 32 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** This is a separate corrective capture. It does not reconstruct the original validity-filtered analysis or authorize pooling with r56, r56b, r56d or r56p2.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r56c.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 127 rows (fail 32, pass 95); overall pass rate is 74.8% (95/127) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 127/127 shared cell IDs match; 0/127 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 138 field mismatches across 4 cell IDs (`manifest_cell_id` 12, `patch.archive_member.2013f0a835799a889d873c2d1d2db223c21b74f51f9f43556ac6a2bb976bc6db` 1, `patch.archive_member.2dd8300b9c520c3bcecbec1d20a3a78bd42c5af027ec746cbd6caa0f846e96c5` 1, `patch.archive_member.58692bac412bcdcaa7e1415cfe0ab26fd5ae503c086eccc3c4c1e6ea7f37bca7` 1, `patch.archive_member.69362a9c4cdd261fe8cc7a89f63181e00e2ee444ece6b015fed79313ea0d21d4` 1, `patch.archive_member.741590ec38a40e3d33e8eb6fead09a3397331a87f866419d3ac0b9aa078bec92` 1, `patch.archive_member.7f276fcf45fd1a7d7832c9a5734f287aea751590e7256fb113e6950cc0d39f6d` 1, `patch.archive_member.ab8a03cf948ce3d238d660236cb3016e85be72257e700a75224aef385af46ff6` 1, `patch.archive_member.b555719de19056d5531ceb79272910afbde1044ce3c6121dc79035cf10f1940a` 1, `patch.archive_member.baf4006fc2ecfe7ca7299f2ac889945a9bfb42be3934a3097c6e3c2b77347605` 1, `patch.archive_member.db0889f851a69aad7e8483e69982f94ee87fef6fb5480be1390d224fc55c6dd0` 1, `patch.attempt-1` 24, `rep` 12, `usage.cached_input_tokens` 16, `usage.input_tokens` 16, `usage.output_tokens` 16, `usage.reasoning_tokens` 16, `wall_s` 16). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.archive_member.b555719de19056d5531ceb79272910afbde1044ce3c6121dc79035cf10f1940a`: kept `{"archive_member": null, "sha256": "b555719de19056d5531ceb79272910afbde1044ce3c6121dc79035cf10f1940a", "size_bytes": 25850}`, recovered `null`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.archive_member.db0889f851a69aad7e8483e69982f94ee87fef6fb5480be1390d224fc55c6dd0`: kept `{"archive_member": null, "sha256": "db0889f851a69aad7e8483e69982f94ee87fef6fb5480be1390d224fc55c6dd0", "size_bytes": 22983}`, recovered `null`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "15ebc967cb02bf756a240d8f09e19dd694bd3d68135014c36df2e73538712b66", "size_bytes": 5911}`, recovered `{"sha256": "b555719de19056d5531ceb79272910afbde1044ce3c6121dc79035cf10f1940a", "size_bytes": 25850}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "15ebc967cb02bf756a240d8f09e19dd694bd3d68135014c36df2e73538712b66", "size_bytes": 5911}`, recovered `{"sha256": "c58add9bb07741eb3e8aa06e01efe7d7b1bebecede6bb49eae0f4ca1508178d6", "size_bytes": 5505}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "15ebc967cb02bf756a240d8f09e19dd694bd3d68135014c36df2e73538712b66", "size_bytes": 5911}`, recovered `{"sha256": "db0889f851a69aad7e8483e69982f94ee87fef6fb5480be1390d224fc55c6dd0", "size_bytes": 22983}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c58add9bb07741eb3e8aa06e01efe7d7b1bebecede6bb49eae0f4ca1508178d6", "size_bytes": 5505}`, recovered `{"sha256": "15ebc967cb02bf756a240d8f09e19dd694bd3d68135014c36df2e73538712b66", "size_bytes": 5911}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c58add9bb07741eb3e8aa06e01efe7d7b1bebecede6bb49eae0f4ca1508178d6", "size_bytes": 5505}`, recovered `{"sha256": "b555719de19056d5531ceb79272910afbde1044ce3c6121dc79035cf10f1940a", "size_bytes": 25850}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c58add9bb07741eb3e8aa06e01efe7d7b1bebecede6bb49eae0f4ca1508178d6", "size_bytes": 5505}`, recovered `{"sha256": "db0889f851a69aad7e8483e69982f94ee87fef6fb5480be1390d224fc55c6dd0", "size_bytes": 22983}`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `rep`: kept `"11"`, recovered `"1"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `rep`: kept `"11"`, recovered `"10"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `rep`: kept `"11"`, recovered `"12"`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.cached_input_tokens`: kept `109056`, recovered `247296`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.cached_input_tokens`: kept `109056`, recovered `247296`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.cached_input_tokens`: kept `247296`, recovered `109056`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.cached_input_tokens`: kept `247296`, recovered `231936`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.cached_input_tokens`: kept `247296`, recovered `262144`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.input_tokens`: kept `25007`, recovered `50950`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.input_tokens`: kept `25007`, recovered `50950`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.input_tokens`: kept `50950`, recovered `25007`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.input_tokens`: kept `50950`, recovered `63925`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.input_tokens`: kept `50950`, recovered `82484`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.output_tokens`: kept `12779`, recovered `11688`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.output_tokens`: kept `12779`, recovered `16128`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.output_tokens`: kept `12779`, recovered `8730`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.output_tokens`: kept `8730`, recovered `12779`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.output_tokens`: kept `8730`, recovered `12779`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.reasoning_tokens`: kept `5507`, recovered `7862`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.reasoning_tokens`: kept `5507`, recovered `7862`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.reasoning_tokens`: kept `7862`, recovered `11213`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.reasoning_tokens`: kept `7862`, recovered `5507`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `usage.reasoning_tokens`: kept `7862`, recovered `7806`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `wall_s`: kept `1012.629`, recovered `1002.25`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `wall_s`: kept `1012.629`, recovered `1212.819`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `wall_s`: kept `1012.629`, recovered `946.879`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `wall_s`: kept `946.879`, recovered `1012.629`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1` field `wall_s`: kept `946.879`, recovered `1012.629`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.archive_member.69362a9c4cdd261fe8cc7a89f63181e00e2ee444ece6b015fed79313ea0d21d4`: kept `{"archive_member": null, "sha256": "69362a9c4cdd261fe8cc7a89f63181e00e2ee444ece6b015fed79313ea0d21d4", "size_bytes": 23338}`, recovered `null`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.archive_member.7f276fcf45fd1a7d7832c9a5734f287aea751590e7256fb113e6950cc0d39f6d`: kept `{"archive_member": null, "sha256": "7f276fcf45fd1a7d7832c9a5734f287aea751590e7256fb113e6950cc0d39f6d", "size_bytes": 25271}`, recovered `null`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "467bea543bc9e84e38cf72852d326d6ccb63c6f8f2b54fb6707ad45813a80115", "size_bytes": 26956}`, recovered `{"sha256": "69362a9c4cdd261fe8cc7a89f63181e00e2ee444ece6b015fed79313ea0d21d4", "size_bytes": 23338}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "467bea543bc9e84e38cf72852d326d6ccb63c6f8f2b54fb6707ad45813a80115", "size_bytes": 26956}`, recovered `{"sha256": "7f276fcf45fd1a7d7832c9a5734f287aea751590e7256fb113e6950cc0d39f6d", "size_bytes": 25271}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "467bea543bc9e84e38cf72852d326d6ccb63c6f8f2b54fb6707ad45813a80115", "size_bytes": 26956}`, recovered `{"sha256": "c7e31fd413a05e1033538b9f50e4b72db57e5e2f00778edb85b27b1bad737b54", "size_bytes": 25572}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c7e31fd413a05e1033538b9f50e4b72db57e5e2f00778edb85b27b1bad737b54", "size_bytes": 25572}`, recovered `{"sha256": "467bea543bc9e84e38cf72852d326d6ccb63c6f8f2b54fb6707ad45813a80115", "size_bytes": 26956}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c7e31fd413a05e1033538b9f50e4b72db57e5e2f00778edb85b27b1bad737b54", "size_bytes": 25572}`, recovered `{"sha256": "69362a9c4cdd261fe8cc7a89f63181e00e2ee444ece6b015fed79313ea0d21d4", "size_bytes": 23338}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `patch.attempt-1`: kept `{"sha256": "c7e31fd413a05e1033538b9f50e4b72db57e5e2f00778edb85b27b1bad737b54", "size_bytes": 25572}`, recovered `{"sha256": "7f276fcf45fd1a7d7832c9a5734f287aea751590e7256fb113e6950cc0d39f6d", "size_bytes": 25271}`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `rep`: kept `"10"`, recovered `"1"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `rep`: kept `"10"`, recovered `"11"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `rep`: kept `"10"`, recovered `"12"`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.cached_input_tokens`: kept `386048`, recovered `709120`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.cached_input_tokens`: kept `386048`, recovered `709120`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.cached_input_tokens`: kept `709120`, recovered `160256`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.cached_input_tokens`: kept `709120`, recovered `335872`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.cached_input_tokens`: kept `709120`, recovered `386048`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.input_tokens`: kept `65680`, recovered `72016`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.input_tokens`: kept `65680`, recovered `72016`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.input_tokens`: kept `72016`, recovered `30498`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.input_tokens`: kept `72016`, recovered `65680`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.input_tokens`: kept `72016`, recovered `92200`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.output_tokens`: kept `11140`, recovered `10849`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.output_tokens`: kept `11140`, recovered `11324`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.output_tokens`: kept `11140`, recovered `13763`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.output_tokens`: kept `13763`, recovered `11140`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.output_tokens`: kept `13763`, recovered `11140`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.reasoning_tokens`: kept `3428`, recovered `4816`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.reasoning_tokens`: kept `3428`, recovered `5492`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.reasoning_tokens`: kept `3428`, recovered `6352`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.reasoning_tokens`: kept `6352`, recovered `3428`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `usage.reasoning_tokens`: kept `6352`, recovered `3428`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `wall_s`: kept `1344.956`, recovered `869.366`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `wall_s`: kept `1344.956`, recovered `869.366`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `wall_s`: kept `869.366`, recovered `1266.654`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `wall_s`: kept `869.366`, recovered `1344.956`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1` field `wall_s`: kept `869.366`, recovered `823.471`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r10"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r11"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-07-cli-stats__r12"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.archive_member.2dd8300b9c520c3bcecbec1d20a3a78bd42c5af027ec746cbd6caa0f846e96c5`: kept `{"archive_member": null, "sha256": "2dd8300b9c520c3bcecbec1d20a3a78bd42c5af027ec746cbd6caa0f846e96c5", "size_bytes": 8885}`, recovered `null`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.archive_member.741590ec38a40e3d33e8eb6fead09a3397331a87f866419d3ac0b9aa078bec92`: kept `{"archive_member": null, "sha256": "741590ec38a40e3d33e8eb6fead09a3397331a87f866419d3ac0b9aa078bec92", "size_bytes": 8500}`, recovered `null`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.archive_member.ab8a03cf948ce3d238d660236cb3016e85be72257e700a75224aef385af46ff6`: kept `{"archive_member": null, "sha256": "ab8a03cf948ce3d238d660236cb3016e85be72257e700a75224aef385af46ff6", "size_bytes": 8928}`, recovered `null`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "2dd8300b9c520c3bcecbec1d20a3a78bd42c5af027ec746cbd6caa0f846e96c5", "size_bytes": 8885}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "2dd8300b9c520c3bcecbec1d20a3a78bd42c5af027ec746cbd6caa0f846e96c5", "size_bytes": 8885}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "741590ec38a40e3d33e8eb6fead09a3397331a87f866419d3ac0b9aa078bec92", "size_bytes": 8500}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "741590ec38a40e3d33e8eb6fead09a3397331a87f866419d3ac0b9aa078bec92", "size_bytes": 8500}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "ab8a03cf948ce3d238d660236cb3016e85be72257e700a75224aef385af46ff6", "size_bytes": 8928}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "1f8ccd6023c122d865330bcaf2d31ee2b7ab8ba5a5a7502994650bb504836a85", "size_bytes": 7482}`, recovered `{"sha256": "ab8a03cf948ce3d238d660236cb3016e85be72257e700a75224aef385af46ff6", "size_bytes": 8928}`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `159232`, recovered `120320`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `159232`, recovered `251392`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `159232`, recovered `310784`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.input_tokens`: kept `37641`, recovered `37917`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.input_tokens`: kept `37641`, recovered `57682`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.input_tokens`: kept `37641`, recovered `65630`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.output_tokens`: kept `10360`, recovered `14415`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.output_tokens`: kept `10360`, recovered `15195`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.output_tokens`: kept `10360`, recovered `7939`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4384`, recovered `4268`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4384`, recovered `6283`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4384`, recovered `6757`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `268.142`, recovered `189.7`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `268.142`, recovered `316.549`.
- `r56c-us-elx07det-us-elx-07-cli-stats-B-ctx-det-r1` field `wall_s`: kept `268.142`, recovered `324.046`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r10"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r11"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `manifest_cell_id`: kept `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r1"`, recovered `"kh-plan__gpt-6-luna__low__default__elx-12-retry-api-deprecation__r12"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.archive_member.2013f0a835799a889d873c2d1d2db223c21b74f51f9f43556ac6a2bb976bc6db`: kept `{"archive_member": null, "sha256": "2013f0a835799a889d873c2d1d2db223c21b74f51f9f43556ac6a2bb976bc6db", "size_bytes": 7028}`, recovered `null`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.archive_member.58692bac412bcdcaa7e1415cfe0ab26fd5ae503c086eccc3c4c1e6ea7f37bca7`: kept `{"archive_member": null, "sha256": "58692bac412bcdcaa7e1415cfe0ab26fd5ae503c086eccc3c4c1e6ea7f37bca7", "size_bytes": 6852}`, recovered `null`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.archive_member.baf4006fc2ecfe7ca7299f2ac889945a9bfb42be3934a3097c6e3c2b77347605`: kept `{"archive_member": null, "sha256": "baf4006fc2ecfe7ca7299f2ac889945a9bfb42be3934a3097c6e3c2b77347605", "size_bytes": 6405}`, recovered `null`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "2013f0a835799a889d873c2d1d2db223c21b74f51f9f43556ac6a2bb976bc6db", "size_bytes": 7028}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "2013f0a835799a889d873c2d1d2db223c21b74f51f9f43556ac6a2bb976bc6db", "size_bytes": 7028}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "58692bac412bcdcaa7e1415cfe0ab26fd5ae503c086eccc3c4c1e6ea7f37bca7", "size_bytes": 6852}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "58692bac412bcdcaa7e1415cfe0ab26fd5ae503c086eccc3c4c1e6ea7f37bca7", "size_bytes": 6852}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "baf4006fc2ecfe7ca7299f2ac889945a9bfb42be3934a3097c6e3c2b77347605", "size_bytes": 6405}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `patch.attempt-1`: kept `{"sha256": "cc4213f9a7c3a44633a290750cd3a00f04288c23d92080af9f795b7433526a33", "size_bytes": 6748}`, recovered `{"sha256": "baf4006fc2ecfe7ca7299f2ac889945a9bfb42be3934a3097c6e3c2b77347605", "size_bytes": 6405}`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"10"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"11"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `rep`: kept `"1"`, recovered `"12"`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `116736`, recovered `166400`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `116736`, recovered `180224`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.cached_input_tokens`: kept `116736`, recovered `228352`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.input_tokens`: kept `35480`, recovered `27183`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.input_tokens`: kept `35480`, recovered `28910`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.input_tokens`: kept `35480`, recovered `38987`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.output_tokens`: kept `7027`, recovered `10200`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.output_tokens`: kept `7027`, recovered `8111`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.output_tokens`: kept `7027`, recovered `8575`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4003`, recovered `5245`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4003`, recovered `5359`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `usage.reasoning_tokens`: kept `4003`, recovered `6094`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `162.441`, recovered `193.612`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `162.441`, recovered `201.442`.
- `r56c-us-elx12det-us-elx-12-retry-api-deprecation-B-ctx-det-r1` field `wall_s`: kept `162.441`, recovered `371.129`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 32/127 published metadata totals equal the manifest `input + cached input + output` sum; 95 differ (multi request aggregation 95). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noplan2-r56c-studio`: published `1446274`, manifest `992181`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r10-P-noplan2-r56c-studio`: published `1121287`, manifest `771988`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r11-P-noplan2-r56c-studio`: published `1282573`, manifest `728099`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r12-P-noplan2-r56c-studio`: published `1231094`, manifest `631612`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-noplan2-r56c-studio`: published `1075861`, manifest `441575`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-P-noplan2-r56c-studio`: published `1302216`, manifest `665817`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r4-P-noplan2-r56c-studio`: published `1673137`, manifest `985214`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r5-P-noplan2-r56c-studio`: published `1488531`, manifest `888585`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r6-P-noplan2-r56c-studio`: published `1251125`, manifest `833301`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r7-P-noplan2-r56c-studio`: published `1932249`, manifest `1222491`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r8-P-noplan2-r56c-studio`: published `879829`, manifest `524002`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r9-P-noplan2-r56c-studio`: published `1343258`, manifest `871521`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noplan2-r56c-studio`: published `1302821`, manifest `680931`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r10-P-noplan2-r56c-studio`: published `1561366`, manifest `1031051`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r11-P-noplan2-r56c-studio`: published `612024`, manifest `152578`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r12-P-noplan2-r56c-studio`: published `1169023`, manifest `341819`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-noplan2-r56c-studio`: published `655652`, manifest `186595`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-P-noplan2-r56c-studio`: published `578635`, manifest `361231`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r4-P-noplan2-r56c-studio`: published `950839`, manifest `411747`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r5-P-noplan2-r56c-studio`: published `768223`, manifest `479968`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r6-P-noplan2-r56c-studio`: published `1090478`, manifest `732584`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r7-P-noplan2-r56c-studio`: published `528594`, manifest `167831`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r8-P-noplan2-r56c-studio`: published `1013004`, manifest `757089`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r9-P-noplan2-r56c-studio`: published `1103787`, manifest `748521`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noplan2-r56c-studio`: published `547789`, manifest `166175`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r10-P-noplan2-r56c-studio`: published `909793`, manifest `513855`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r11-P-noplan2-r56c-studio`: published `1111862`, manifest `472127`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r12-P-noplan2-r56c-studio`: published `946283`, manifest `331331`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-noplan2-r56c-studio`: published `795859`, manifest `364608`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-P-noplan2-r56c-studio`: published `1308487`, manifest `810555`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r4-P-noplan2-r56c-studio`: published `1049559`, manifest `585812`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r5-P-noplan2-r56c-studio`: published `992590`, manifest `267764`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r6-P-noplan2-r56c-studio`: published `1712885`, manifest `991730`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r7-P-noplan2-r56c-studio`: published `1024658`, manifest `526618`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r8-P-noplan2-r56c-studio`: published `962392`, manifest `440868`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r9-P-noplan2-r56c-studio`: published `713748`, manifest `316395`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noplan2-r56c-studio`: published `1130485`, manifest `600493`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r10-P-noplan2-r56c-studio`: published `1613318`, manifest `993631`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r11-P-noplan2-r56c-studio`: published `3102360`, manifest `2223357`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r12-P-noplan2-r56c-studio`: published `1103075`, manifest `622749`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-noplan2-r56c-studio`: published `833025`, manifest `608812`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-P-noplan2-r56c-studio`: published `2151180`, manifest `1569039`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r4-P-noplan2-r56c-studio`: published `2432570`, manifest `2002270`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r5-P-noplan2-r56c-studio`: published `1181033`, manifest `575393`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r6-P-noplan2-r56c-studio`: published `814766`, manifest `416731`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r7-P-noplan2-r56c-studio`: published `1384948`, manifest `1127260`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r8-P-noplan2-r56c-studio`: published `1244209`, manifest `566343`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r9-P-noplan2-r56c-studio`: published `769043`, manifest `488838`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noplan2-r56c-studio`: published `2871385`, manifest `2137344`, provider responses `66`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r11-P-noplan2-r56c-studio`: published `2169569`, manifest `1634828`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r12-P-noplan2-r56c-studio`: published `5163071`, manifest `4580115`, provider responses `116`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-noplan2-r56c-studio`: published `2267167`, manifest `1814427`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-P-noplan2-r56c-studio`: published `2792900`, manifest `2061270`, provider responses `70`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r4-P-noplan2-r56c-studio`: published `4599651`, manifest `4037764`, provider responses `86`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r5-P-noplan2-r56c-studio`: published `3235311`, manifest `2572360`, provider responses `74`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r6-P-noplan2-r56c-studio`: published `2915815`, manifest `2331690`, provider responses `71`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r7-P-noplan2-r56c-studio`: published `3729168`, manifest `2937729`, provider responses `80`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r8-P-noplan2-r56c-studio`: published `3308102`, manifest `2689076`, provider responses `83`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r9-P-noplan2-r56c-studio`: published `3809745`, manifest `3165389`, provider responses `82`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noplan2-r56c-studio`: published `2070113`, manifest `1438193`, provider responses `59`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r10-P-noplan2-r56c-studio`: published `1493772`, manifest `778846`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r11-P-noplan2-r56c-studio`: published `1186692`, manifest `563219`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r12-P-noplan2-r56c-studio`: published `927047`, manifest `611574`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-noplan2-r56c-studio`: published `1071246`, manifest `557619`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-P-noplan2-r56c-studio`: published `1144762`, manifest `670150`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r4-P-noplan2-r56c-studio`: published `1038846`, manifest `523368`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r5-P-noplan2-r56c-studio`: published `758941`, manifest `396763`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r6-P-noplan2-r56c-studio`: published `1047855`, manifest `450241`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r7-P-noplan2-r56c-studio`: published `893768`, manifest `448002`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r8-P-noplan2-r56c-studio`: published `1014316`, manifest `536771`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r9-P-noplan2-r56c-studio`: published `753795`, manifest `378276`, provider responses `32`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r1`: published `429263`, manifest `142793`, provider responses `15`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r10`: published `532975`, manifest `201040`, provider responses `23`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r11`: published `755260`, manifest `405620`, provider responses `34`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r12`: published `509895`, manifest `201664`, provider responses `21`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r2`: published `1248965`, manifest `888399`, provider responses `49`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r3`: published `1025325`, manifest `473754`, provider responses `34`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r4`: published `1075612`, manifest `666964`, provider responses `40`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r5`: published `916090`, manifest `474912`, provider responses `33`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r6`: published `558694`, manifest `198279`, provider responses `19`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r7`: published `611889`, manifest `294652`, provider responses `23`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r8`: published `792523`, manifest `426029`, provider responses `33`; `multi_request_aggregation`.
- `r56c-eu-elx12-eu-elx-12-retry-api-deprecation-P-noplan2-r9`: published `930796`, manifest `501877`, provider responses `34`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r1`: published `971714`, manifest `465491`, provider responses `23`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r10`: published `723250`, manifest `256408`, provider responses `23`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r11`: published `351509`, manifest `153978`, provider responses `11`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r12`: published `491106`, manifest `208425`, provider responses `15`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r2`: published `761036`, manifest `361189`, provider responses `25`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r3`: published `1032485`, manifest `723402`, provider responses `23`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r4`: published `565358`, manifest `313864`, provider responses `26`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r5`: published `605446`, manifest `170959`, provider responses `15`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r6`: published `643594`, manifest `357662`, provider responses `19`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r7`: published `679808`, manifest `272345`, provider responses `24`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r8`: published `535838`, manifest `269445`, provider responses `17`; `multi_request_aggregation`.
- `r56c-us-elx07-us-elx-07-cli-stats-P-noplan2-r9`: published `502427`, manifest `219372`, provider responses `18`; `multi_request_aggregation`.
