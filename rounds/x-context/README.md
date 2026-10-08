# x context

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Planned, started, finished, graded, and ITT counts are not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H51, H54, H55, H56, H57, H58 (provisional mapping; see the hypothesis register).
Question: Does the tested context-admission or preparation method improve task outcomes on this development cohort?
Population: Exact planned, started, finished, graded and ITT counts are not recovered.
Headline: No context efficacy claim.

## Reported observations

- The context comparison is described as inconclusive. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A scoped admission guard identified as B005 was listed as a transfer candidate; the public task and cell crosswalk is unavailable. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No numerical treatment effect is published in the current public record. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Per-cell model and effort values were not recovered. |
| Task IDs | Exact task IDs and selected cell IDs are not recovered. |
| Command | Not recovered; no public command or launch manifest is available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The available report does not establish that context preparation improves live task completion.

**Smallest useful next test:** Recover the arm manifest and task-level outcomes, then test the scoped guard prospectively against a matched no-context control.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-context.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 39 rows (infra 4, pass 28, restore_failed 6, ungraded 1); overall pass rate is 100.0% (28/28) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 82 field mismatches across 5 cell IDs (`experiment` 11, `patch.archive_member.05fd3db97bc8453cd492d83a5423ffcc69b656111e5a0a78dd7e8b2184b06ff4` 1, `patch.archive_member.13c21056151de416208029878e81c8070226e6e3d81527b9973362b74e3ac83d` 1, `patch.archive_member.337f61330b38f7f19537a14737da3ecd72c39803d7a156980124bce7fa954e28` 1, `patch.archive_member.352dd8ed9e80fef3b5d2cf243803f5e41ce61cc4863c85349ee29f95e0468f84` 1, `patch.archive_member.3bb4ddbdbd80be169b2f6ba46c94707f3e48f8712e7e1223bb85864aa4f2fcb3` 1, `patch.archive_member.49c8c8fd1faec8d9f743aafa16b10afe10379516fe0baa2ec343feb96639d759` 1, `patch.archive_member.5f8eeeb81dc58c2d58c46f6c3cbe109a794e72c3c5447d138cbc827ecd6da418` 1, `patch.archive_member.751d9060929cafa8355b734305f45b45a4d8415f3421dde1fb4c0bdcd0d9cdd1` 1, `patch.archive_member.894c90069859656f1015463891d4eb81ff236eeeab484bca70cfaf075ecc5e91` 1, `patch.archive_member.933fc3fd54bcac389191f732e5f2a914dbd055436596ef462da0ed910b19f22c` 1, `patch.attempt-1` 10, `status` 1, `usage.cached_input_tokens` 10, `usage.input_tokens` 10, `usage.output_tokens` 10, `usage.reasoning_tokens` 10, `wall_s` 10). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `experiment`: kept `"20260930T155903.019855Z-54488-7f0f53e8"`, recovered `"20260930T155903.014393Z-54486-e6d99a05"`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `patch.archive_member.894c90069859656f1015463891d4eb81ff236eeeab484bca70cfaf075ecc5e91`: kept `{"archive_member": null, "sha256": "894c90069859656f1015463891d4eb81ff236eeeab484bca70cfaf075ecc5e91", "size_bytes": 3471}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `patch.attempt-1`: kept `{"sha256": "1438fc877f29ddd76c7476acbf4e77e314a6bdb684b252c7d7f385c7326ebf89", "size_bytes": 4150}`, recovered `{"sha256": "894c90069859656f1015463891d4eb81ff236eeeab484bca70cfaf075ecc5e91", "size_bytes": 3471}`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `usage.cached_input_tokens`: kept `59392`, recovered `30720`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `usage.input_tokens`: kept `22559`, recovered `14284`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `usage.output_tokens`: kept `5085`, recovered `3450`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `usage.reasoning_tokens`: kept `2475`, recovered `1797`.
- `kh-gpt__gpt-6-luna__high__default__elx-06-command-runner__r1` field `wall_s`: kept `158.433`, recovered `100.971`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T135731.732431Z-43276-6d6760ae"`, recovered `"20260930T135731.732256Z-43274-e47d64c5"`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T135731.732431Z-43276-6d6760ae"`, recovered `"20260930T140756.683834Z-54548-62e4f9d8"`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T135731.732431Z-43276-6d6760ae"`, recovered `"20260930T140756.685561Z-54547-cd635d8e"`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.337f61330b38f7f19537a14737da3ecd72c39803d7a156980124bce7fa954e28`: kept `{"archive_member": null, "sha256": "337f61330b38f7f19537a14737da3ecd72c39803d7a156980124bce7fa954e28", "size_bytes": 3611}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.3bb4ddbdbd80be169b2f6ba46c94707f3e48f8712e7e1223bb85864aa4f2fcb3`: kept `{"archive_member": null, "sha256": "3bb4ddbdbd80be169b2f6ba46c94707f3e48f8712e7e1223bb85864aa4f2fcb3", "size_bytes": 3871}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.751d9060929cafa8355b734305f45b45a4d8415f3421dde1fb4c0bdcd0d9cdd1`: kept `{"archive_member": null, "sha256": "751d9060929cafa8355b734305f45b45a4d8415f3421dde1fb4c0bdcd0d9cdd1", "size_bytes": 4572}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "707e3f07c84d9fa90f433d0b0e4e54fdd1ed276afca554cc7f883512ebfd477c", "size_bytes": 4085}`, recovered `{"sha256": "337f61330b38f7f19537a14737da3ecd72c39803d7a156980124bce7fa954e28", "size_bytes": 3611}`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "707e3f07c84d9fa90f433d0b0e4e54fdd1ed276afca554cc7f883512ebfd477c", "size_bytes": 4085}`, recovered `{"sha256": "3bb4ddbdbd80be169b2f6ba46c94707f3e48f8712e7e1223bb85864aa4f2fcb3", "size_bytes": 3871}`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "707e3f07c84d9fa90f433d0b0e4e54fdd1ed276afca554cc7f883512ebfd477c", "size_bytes": 4085}`, recovered `{"sha256": "751d9060929cafa8355b734305f45b45a4d8415f3421dde1fb4c0bdcd0d9cdd1", "size_bytes": 4572}`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `192000`, recovered `151040`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `192000`, recovered `152576`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `192000`, recovered `208896`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `30316`, recovered `26061`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `30316`, recovered `28664`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `30316`, recovered `28787`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `2573`, recovered `2711`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `2573`, recovered `2728`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `2573`, recovered `2956`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `989`, recovered `1071`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `989`, recovered `887`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `989`, recovered `933`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `126.817`, recovered `104.478`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `126.817`, recovered `106.508`.
- `kh-gpt__gpt-6-luna__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `126.817`, recovered `114.785`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `experiment`: kept `"20260930T160740.898874Z-24583-c70ccec4"`, recovered `"20260930T155903.014308Z-54487-34e79cca"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `experiment`: kept `"20260930T160740.898874Z-24583-c70ccec4"`, recovered `"20260930T155903.014383Z-54485-13fcfa2e"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `experiment`: kept `"20260930T160740.898874Z-24583-c70ccec4"`, recovered `"20260930T160740.899159Z-24585-2e4b6ac6"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.archive_member.05fd3db97bc8453cd492d83a5423ffcc69b656111e5a0a78dd7e8b2184b06ff4`: kept `{"archive_member": null, "sha256": "05fd3db97bc8453cd492d83a5423ffcc69b656111e5a0a78dd7e8b2184b06ff4", "size_bytes": 8137}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.archive_member.13c21056151de416208029878e81c8070226e6e3d81527b9973362b74e3ac83d`: kept `{"archive_member": null, "sha256": "13c21056151de416208029878e81c8070226e6e3d81527b9973362b74e3ac83d", "size_bytes": 9048}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.archive_member.49c8c8fd1faec8d9f743aafa16b10afe10379516fe0baa2ec343feb96639d759`: kept `{"archive_member": null, "sha256": "49c8c8fd1faec8d9f743aafa16b10afe10379516fe0baa2ec343feb96639d759", "size_bytes": 9418}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.attempt-1`: kept `{"sha256": "0d4b984bd4b3e1d6f357153642c8a2a6ceb9f669131f2cf586f91b8eef29631c", "size_bytes": 7348}`, recovered `{"sha256": "05fd3db97bc8453cd492d83a5423ffcc69b656111e5a0a78dd7e8b2184b06ff4", "size_bytes": 8137}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.attempt-1`: kept `{"sha256": "0d4b984bd4b3e1d6f357153642c8a2a6ceb9f669131f2cf586f91b8eef29631c", "size_bytes": 7348}`, recovered `{"sha256": "13c21056151de416208029878e81c8070226e6e3d81527b9973362b74e3ac83d", "size_bytes": 9048}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `patch.attempt-1`: kept `{"sha256": "0d4b984bd4b3e1d6f357153642c8a2a6ceb9f669131f2cf586f91b8eef29631c", "size_bytes": 7348}`, recovered `{"sha256": "49c8c8fd1faec8d9f743aafa16b10afe10379516fe0baa2ec343feb96639d759", "size_bytes": 9418}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.cached_input_tokens`: kept `52352`, recovered `44416`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.cached_input_tokens`: kept `52352`, recovered `48128`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.cached_input_tokens`: kept `52352`, recovered `95616`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.input_tokens`: kept `21741`, recovered `21551`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.input_tokens`: kept `21741`, recovered `22674`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.input_tokens`: kept `21741`, recovered `25389`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.output_tokens`: kept `4146`, recovered `5101`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.output_tokens`: kept `4146`, recovered `5727`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.output_tokens`: kept `4146`, recovered `5892`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.reasoning_tokens`: kept `1184`, recovered `1976`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.reasoning_tokens`: kept `1184`, recovered `2109`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `usage.reasoning_tokens`: kept `1184`, recovered `2130`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `wall_s`: kept `252.584`, recovered `287.587`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `wall_s`: kept `252.584`, recovered `345.033`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-06-command-runner__r1` field `wall_s`: kept `252.584`, recovered `388.792`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `experiment`: kept `"20260930T161412.363030Z-21616-6cc0a4f2"`, recovered `"20260930T161412.367461Z-21617-9376eb29"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-05__r1` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T140756.686118Z-54549-d4c1c259"`, recovered `"20260930T135731.732256Z-43273-7ce0cba6"`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T140756.686118Z-54549-d4c1c259"`, recovered `"20260930T135731.732256Z-43275-660049ad"`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `experiment`: kept `"20260930T140756.686118Z-54549-d4c1c259"`, recovered `"20260930T140756.687050Z-54550-c21068bc"`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.352dd8ed9e80fef3b5d2cf243803f5e41ce61cc4863c85349ee29f95e0468f84`: kept `{"archive_member": null, "sha256": "352dd8ed9e80fef3b5d2cf243803f5e41ce61cc4863c85349ee29f95e0468f84", "size_bytes": 13886}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.5f8eeeb81dc58c2d58c46f6c3cbe109a794e72c3c5447d138cbc827ecd6da418`: kept `{"archive_member": null, "sha256": "5f8eeeb81dc58c2d58c46f6c3cbe109a794e72c3c5447d138cbc827ecd6da418", "size_bytes": 13550}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.archive_member.933fc3fd54bcac389191f732e5f2a914dbd055436596ef462da0ed910b19f22c`: kept `{"archive_member": null, "sha256": "933fc3fd54bcac389191f732e5f2a914dbd055436596ef462da0ed910b19f22c", "size_bytes": 12103}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "3f1765a9bc36009abf875b33f356681b2bf4a33702e4fb4ae51d53ad3d9e9bbb", "size_bytes": 13547}`, recovered `{"sha256": "352dd8ed9e80fef3b5d2cf243803f5e41ce61cc4863c85349ee29f95e0468f84", "size_bytes": 13886}`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "3f1765a9bc36009abf875b33f356681b2bf4a33702e4fb4ae51d53ad3d9e9bbb", "size_bytes": 13547}`, recovered `{"sha256": "5f8eeeb81dc58c2d58c46f6c3cbe109a794e72c3c5447d138cbc827ecd6da418", "size_bytes": 13550}`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `patch.attempt-1`: kept `{"sha256": "3f1765a9bc36009abf875b33f356681b2bf4a33702e4fb4ae51d53ad3d9e9bbb", "size_bytes": 13547}`, recovered `{"sha256": "933fc3fd54bcac389191f732e5f2a914dbd055436596ef462da0ed910b19f22c", "size_bytes": 12103}`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `322048`, recovered `256640`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `322048`, recovered `428416`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.cached_input_tokens`: kept `322048`, recovered `432896`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `52277`, recovered `32538`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `52277`, recovered `40619`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.input_tokens`: kept `52277`, recovered `84021`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `5099`, recovered `4586`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `5099`, recovered `5112`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.output_tokens`: kept `5099`, recovered `5217`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `523`, recovered `497`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `523`, recovered `502`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `usage.reasoning_tokens`: kept `523`, recovered `741`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `666.577`, recovered `307.274`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `666.577`, recovered `340.671`.
- `kh-gpt__gpt-6.1-sol__high__default__syn-13-bug-empty-filter-crash__r1` field `wall_s`: kept `666.577`, recovered `372.519`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 39 missing published metadata). Missing counters remain unknown, not zero.
This round also has 39 raw-only or non-public rows; they are kept separate from the published-export denominator.
