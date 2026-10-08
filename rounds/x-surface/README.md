# x surface

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **INCOMPLETE_EXECUTION:** Only 8 of 16 planned or reported cells were complete at the cited cutoff.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H31, H33, H110 (provisional mapping; see the hypothesis register).
Question: Do changes to the agent-facing feedback surface improve completion or reduce unnecessary interaction?
Population: 16 cohort cells were planned/reported; 8/16 completed at the cited cutoff.
Headline: No agent-output format claim.

## Reported observations

- The feedback-format cohort is reported as 8/16 completed. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- On the fixture repair subset, the compared models are reported tied at 2/2 versus 2/2. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The remaining repetition was unrun. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Models are reported as compared for a fixture repair; exact model/effort receipt is unavailable. |
| Task IDs | Fixture task IDs are not recovered. |
| Command | Not recovered; launch command and exact cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** This partial fixture cohort does not establish an output-format preference or a completion benefit.

**Smallest useful next test:** Complete the registered repetitions on the same tasks and compare parse success, diagnosis, repair and resource use.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-surface.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 55 rows (infra 1, pass 47, restore_failed 4, ungraded 3); overall pass rate is 100.0% (47/47) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 192 field mismatches across 8 cell IDs (`experiment` 24, `patch.archive_member.07b97f0f6de22d9d61754471d34e6feaa9b3ed9b554358d0fc757ab13cda4d9c` 1, `patch.archive_member.09e281f0372e51396634c5b2e0cfe691b80d05765415b114a2a1a8eaeea705df` 1, `patch.archive_member.0ecb6b7722cb2e6589cf198cd2f12700a272b9242ac2befae05d1d044bf25a91` 1, `patch.archive_member.0ef04a9f3ee5b1fe4f4ae71ada994276dd17c9ad347dd7d659a95469708ff4e0` 1, `patch.archive_member.1ffc94db54b99d556b3f5124d9b38e763a61094fc71d084281a43297168b739b` 1, `patch.archive_member.20396114a0a585e655836d3c38cdac94b654ac7e5c2496e141909ff8ec07497c` 1, `patch.archive_member.328e4a8d3ad300dee2fc60e656f12da0ef71acc542dd3d5cf41c1a500750e24d` 1, `patch.archive_member.3a8501e8913bbcd00a3f6b4865195dff03fb25f72296705fea667b710643fb0e` 1, `patch.archive_member.3b4fa76745d83c0127bfa99dba8b37cd101995bbff13fff76b06c836491822a6` 1, `patch.archive_member.4cb7f56124efa7b796455134143f3754258d4838854b28ebd2931a96dae3b5ab` 1, `patch.archive_member.764b160c18124007f9a0525643fb6f69f66bb46985e88dc452ac8871be8b5832` 1, `patch.archive_member.999d2352aa821062f7f6f749e85855dd90d36caeb61734f1b3b077016d21dc56` 1, `patch.archive_member.9fa8dc7685b84abeaddf991484607fc8ce70ae5aa7b9b9dbae54506301ce1f49` 1, `patch.archive_member.a92b2f007a50005460ae7006de2faf9c99b2ef1fd71b52f8c37ab9b036e7725c` 1, `patch.archive_member.aac1720ba895e44413b63c823779d47077e408f77e68dc76d023f4c7c49f073b` 1, `patch.archive_member.b5c27950eb19b60f39d84fadeca87e0ad43cfe5b728b245abf30f0e1b5b8990f` 1, `patch.archive_member.c233539a27fa2f78723ac1003270640f0b402e91c5e27bdb2e7185a788fd9d84` 1, `patch.archive_member.ce0c19a3f4c7ba9bda6fbccf306f311d83c39501510f22d6ba1e7e6bd6868c53` 1, `patch.archive_member.cfc9e8698aac76eaeb5544fbe8e58fe51cbbefdbc856a5308d2db07d0d2c5b80` 1, `patch.archive_member.d3b9f5aa6f5b5d057e9b2d58c813c48428bd4b19d3c3c440a867378a26779d06` 1, `patch.archive_member.e666a82c3af99d484476139697849321ad4ac5109ccd2619e667fb238359698c` 1, `patch.archive_member.f0be6ffe09fbb97fbaacd80c568f8de982f250b9150b75f6206fb2ff0c38e309` 1, `patch.archive_member.f16d08ceb0ce3df567c683766d393c7c94486d08212473f1586eb7e107174419` 1, `patch.archive_member.f35a924c04bc54902deb2f3fd720bb5e15d080f1defae41798bd901c17fee794` 1, `patch.attempt-1` 24, `usage.cached_input_tokens` 24, `usage.input_tokens` 24, `usage.output_tokens` 24, `usage.reasoning_tokens` 24, `wall_s` 24). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T140043.275428Z-46339-ba3c7aca"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.448744Z-1421-d3eb5575"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.453393Z-1422-885b532d"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.07b97f0f6de22d9d61754471d34e6feaa9b3ed9b554358d0fc757ab13cda4d9c`: kept `{"archive_member": null, "sha256": "07b97f0f6de22d9d61754471d34e6feaa9b3ed9b554358d0fc757ab13cda4d9c", "size_bytes": 4507}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.1ffc94db54b99d556b3f5124d9b38e763a61094fc71d084281a43297168b739b`: kept `{"archive_member": null, "sha256": "1ffc94db54b99d556b3f5124d9b38e763a61094fc71d084281a43297168b739b", "size_bytes": 4019}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.c233539a27fa2f78723ac1003270640f0b402e91c5e27bdb2e7185a788fd9d84`: kept `{"archive_member": null, "sha256": "c233539a27fa2f78723ac1003270640f0b402e91c5e27bdb2e7185a788fd9d84", "size_bytes": 4080}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "fa0b55c6642f96e1b9c42c45ced5bc0a4e336d4467363f3ee6fe5d5d341caf19", "size_bytes": 3901}`, recovered `{"sha256": "07b97f0f6de22d9d61754471d34e6feaa9b3ed9b554358d0fc757ab13cda4d9c", "size_bytes": 4507}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "fa0b55c6642f96e1b9c42c45ced5bc0a4e336d4467363f3ee6fe5d5d341caf19", "size_bytes": 3901}`, recovered `{"sha256": "1ffc94db54b99d556b3f5124d9b38e763a61094fc71d084281a43297168b739b", "size_bytes": 4019}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "fa0b55c6642f96e1b9c42c45ced5bc0a4e336d4467363f3ee6fe5d5d341caf19", "size_bytes": 3901}`, recovered `{"sha256": "c233539a27fa2f78723ac1003270640f0b402e91c5e27bdb2e7185a788fd9d84", "size_bytes": 4080}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `22016`, recovered `22528`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `22016`, recovered `28160`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `22016`, recovered `34816`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `10543`, recovered `12293`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `10543`, recovered `14652`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `10543`, recovered `21135`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `2172`, recovered `2733`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `2172`, recovered `3123`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `2172`, recovered `4985`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `786`, recovered `1072`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `786`, recovered `907`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `786`, recovered `979`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `84.223`, recovered `100.096`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `84.223`, recovered `129.472`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `84.223`, recovered `91.611`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T140043.275428Z-46339-ba3c7aca"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.448744Z-1421-d3eb5575"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.453393Z-1422-885b532d"`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.328e4a8d3ad300dee2fc60e656f12da0ef71acc542dd3d5cf41c1a500750e24d`: kept `{"archive_member": null, "sha256": "328e4a8d3ad300dee2fc60e656f12da0ef71acc542dd3d5cf41c1a500750e24d", "size_bytes": 3605}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.4cb7f56124efa7b796455134143f3754258d4838854b28ebd2931a96dae3b5ab`: kept `{"archive_member": null, "sha256": "4cb7f56124efa7b796455134143f3754258d4838854b28ebd2931a96dae3b5ab", "size_bytes": 3381}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.b5c27950eb19b60f39d84fadeca87e0ad43cfe5b728b245abf30f0e1b5b8990f`: kept `{"archive_member": null, "sha256": "b5c27950eb19b60f39d84fadeca87e0ad43cfe5b728b245abf30f0e1b5b8990f", "size_bytes": 3939}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "0c8f7237a607eeef85c1b5273f7ca5363d605203124899ac0222299133e8b389", "size_bytes": 3988}`, recovered `{"sha256": "328e4a8d3ad300dee2fc60e656f12da0ef71acc542dd3d5cf41c1a500750e24d", "size_bytes": 3605}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "0c8f7237a607eeef85c1b5273f7ca5363d605203124899ac0222299133e8b389", "size_bytes": 3988}`, recovered `{"sha256": "4cb7f56124efa7b796455134143f3754258d4838854b28ebd2931a96dae3b5ab", "size_bytes": 3381}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "0c8f7237a607eeef85c1b5273f7ca5363d605203124899ac0222299133e8b389", "size_bytes": 3988}`, recovered `{"sha256": "b5c27950eb19b60f39d84fadeca87e0ad43cfe5b728b245abf30f0e1b5b8990f", "size_bytes": 3939}`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `40960`, recovered `22016`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `40960`, recovered `25600`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `40960`, recovered `29184`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `15694`, recovered `11249`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `15694`, recovered `12592`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `15694`, recovered `22116`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `2441`, recovered `2475`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `2441`, recovered `2557`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `2441`, recovered `4602`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `888`, recovered `1098`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `888`, recovered `1146`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `888`, recovered `948`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `84.417`, recovered `112.168`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `84.417`, recovered `146.332`.
- `kh-gpt__gpt-6-luna__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `84.417`, recovered `82.693`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T140043.275428Z-46339-ba3c7aca"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.448744Z-1421-d3eb5575"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.453393Z-1422-885b532d"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.archive_member.0ef04a9f3ee5b1fe4f4ae71ada994276dd17c9ad347dd7d659a95469708ff4e0`: kept `{"archive_member": null, "sha256": "0ef04a9f3ee5b1fe4f4ae71ada994276dd17c9ad347dd7d659a95469708ff4e0", "size_bytes": 3459}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.archive_member.20396114a0a585e655836d3c38cdac94b654ac7e5c2496e141909ff8ec07497c`: kept `{"archive_member": null, "sha256": "20396114a0a585e655836d3c38cdac94b654ac7e5c2496e141909ff8ec07497c", "size_bytes": 3352}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.archive_member.cfc9e8698aac76eaeb5544fbe8e58fe51cbbefdbc856a5308d2db07d0d2c5b80`: kept `{"archive_member": null, "sha256": "cfc9e8698aac76eaeb5544fbe8e58fe51cbbefdbc856a5308d2db07d0d2c5b80", "size_bytes": 3406}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "fe2de83ab1657386fd2b12248cd6ecb1d45955b92df5690334aedb6e7a8dad90", "size_bytes": 4048}`, recovered `{"sha256": "0ef04a9f3ee5b1fe4f4ae71ada994276dd17c9ad347dd7d659a95469708ff4e0", "size_bytes": 3459}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "fe2de83ab1657386fd2b12248cd6ecb1d45955b92df5690334aedb6e7a8dad90", "size_bytes": 4048}`, recovered `{"sha256": "20396114a0a585e655836d3c38cdac94b654ac7e5c2496e141909ff8ec07497c", "size_bytes": 3352}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "fe2de83ab1657386fd2b12248cd6ecb1d45955b92df5690334aedb6e7a8dad90", "size_bytes": 4048}`, recovered `{"sha256": "cfc9e8698aac76eaeb5544fbe8e58fe51cbbefdbc856a5308d2db07d0d2c5b80", "size_bytes": 3406}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `33280`, recovered `17408`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `33280`, recovered `18432`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `33280`, recovered `8704`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.input_tokens`: kept `18909`, recovered `10776`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.input_tokens`: kept `18909`, recovered `12775`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.input_tokens`: kept `18909`, recovered `16689`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.output_tokens`: kept `1772`, recovered `1447`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.output_tokens`: kept `1772`, recovered `1640`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.output_tokens`: kept `1772`, recovered `2392`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `352`, recovered `185`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `352`, recovered `202`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `352`, recovered `251`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `wall_s`: kept `327.5`, recovered `380.332`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `wall_s`: kept `327.5`, recovered `435.684`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r1` field `wall_s`: kept `327.5`, recovered `59.352`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T140043.275428Z-46339-ba3c7aca"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.448744Z-1421-d3eb5575"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `experiment`: kept `"20260930T140043.279003Z-46340-1b530cdd"`, recovered `"20260930T142442.453393Z-1422-885b532d"`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.archive_member.0ecb6b7722cb2e6589cf198cd2f12700a272b9242ac2befae05d1d044bf25a91`: kept `{"archive_member": null, "sha256": "0ecb6b7722cb2e6589cf198cd2f12700a272b9242ac2befae05d1d044bf25a91", "size_bytes": 3406}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.archive_member.d3b9f5aa6f5b5d057e9b2d58c813c48428bd4b19d3c3c440a867378a26779d06`: kept `{"archive_member": null, "sha256": "d3b9f5aa6f5b5d057e9b2d58c813c48428bd4b19d3c3c440a867378a26779d06", "size_bytes": 3366}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.archive_member.f16d08ceb0ce3df567c683766d393c7c94486d08212473f1586eb7e107174419`: kept `{"archive_member": null, "sha256": "f16d08ceb0ce3df567c683766d393c7c94486d08212473f1586eb7e107174419", "size_bytes": 3550}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "7e1c5d0d26c1bcc0b726b4b826267ac4efc0656c0c6e01526d964ccf114b1c67", "size_bytes": 3297}`, recovered `{"sha256": "0ecb6b7722cb2e6589cf198cd2f12700a272b9242ac2befae05d1d044bf25a91", "size_bytes": 3406}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "7e1c5d0d26c1bcc0b726b4b826267ac4efc0656c0c6e01526d964ccf114b1c67", "size_bytes": 3297}`, recovered `{"sha256": "d3b9f5aa6f5b5d057e9b2d58c813c48428bd4b19d3c3c440a867378a26779d06", "size_bytes": 3366}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "7e1c5d0d26c1bcc0b726b4b826267ac4efc0656c0c6e01526d964ccf114b1c67", "size_bytes": 3297}`, recovered `{"sha256": "f16d08ceb0ce3df567c683766d393c7c94486d08212473f1586eb7e107174419", "size_bytes": 3550}`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `18944`, recovered `10240`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `18944`, recovered `13824`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `18944`, recovered `73216`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.input_tokens`: kept `17819`, recovered `10937`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.input_tokens`: kept `17819`, recovered `11426`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.input_tokens`: kept `17819`, recovered `24075`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.output_tokens`: kept `1552`, recovered `1422`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.output_tokens`: kept `1552`, recovered `1526`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.output_tokens`: kept `1552`, recovered `4520`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `263`, recovered `175`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `263`, recovered `186`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `263`, recovered `418`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `wall_s`: kept `61.013`, recovered `136.514`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `wall_s`: kept `61.013`, recovered `341.11`.
- `kh-gpt__gpt-6-luna__high__default__rt-02__r2` field `wall_s`: kept `61.013`, recovered `57.964`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.269244Z-46336-d496da77"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.270567Z-46338-4d93508c"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T142442.442815Z-1419-353e743c"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.09e281f0372e51396634c5b2e0cfe691b80d05765415b114a2a1a8eaeea705df`: kept `{"archive_member": null, "sha256": "09e281f0372e51396634c5b2e0cfe691b80d05765415b114a2a1a8eaeea705df", "size_bytes": 8276}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.3b4fa76745d83c0127bfa99dba8b37cd101995bbff13fff76b06c836491822a6`: kept `{"archive_member": null, "sha256": "3b4fa76745d83c0127bfa99dba8b37cd101995bbff13fff76b06c836491822a6", "size_bytes": 9115}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.f35a924c04bc54902deb2f3fd720bb5e15d080f1defae41798bd901c17fee794`: kept `{"archive_member": null, "sha256": "f35a924c04bc54902deb2f3fd720bb5e15d080f1defae41798bd901c17fee794", "size_bytes": 8985}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "62d1c55f1a646aacb20f92348664b317a778f2f2758c660887bed8783baf20d4", "size_bytes": 8016}`, recovered `{"sha256": "09e281f0372e51396634c5b2e0cfe691b80d05765415b114a2a1a8eaeea705df", "size_bytes": 8276}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "62d1c55f1a646aacb20f92348664b317a778f2f2758c660887bed8783baf20d4", "size_bytes": 8016}`, recovered `{"sha256": "3b4fa76745d83c0127bfa99dba8b37cd101995bbff13fff76b06c836491822a6", "size_bytes": 9115}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "62d1c55f1a646aacb20f92348664b317a778f2f2758c660887bed8783baf20d4", "size_bytes": 8016}`, recovered `{"sha256": "f35a924c04bc54902deb2f3fd720bb5e15d080f1defae41798bd901c17fee794", "size_bytes": 8985}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `61056`, recovered `26368`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `61056`, recovered `26496`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `61056`, recovered `60544`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `26903`, recovered `16750`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `26903`, recovered `17126`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `26903`, recovered `26709`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `5571`, recovered `3641`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `5571`, recovered `3927`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `5571`, recovered `4060`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `728`, recovered `1064`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `728`, recovered `720`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `728`, recovered `819`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `328.586`, recovered `225.509`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `328.586`, recovered `232.439`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `328.586`, recovered `254.165`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.269244Z-46336-d496da77"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.270567Z-46338-4d93508c"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T142442.442815Z-1419-353e743c"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.9fa8dc7685b84abeaddf991484607fc8ce70ae5aa7b9b9dbae54506301ce1f49`: kept `{"archive_member": null, "sha256": "9fa8dc7685b84abeaddf991484607fc8ce70ae5aa7b9b9dbae54506301ce1f49", "size_bytes": 8957}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.e666a82c3af99d484476139697849321ad4ac5109ccd2619e667fb238359698c`: kept `{"archive_member": null, "sha256": "e666a82c3af99d484476139697849321ad4ac5109ccd2619e667fb238359698c", "size_bytes": 9255}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.f0be6ffe09fbb97fbaacd80c568f8de982f250b9150b75f6206fb2ff0c38e309`: kept `{"archive_member": null, "sha256": "f0be6ffe09fbb97fbaacd80c568f8de982f250b9150b75f6206fb2ff0c38e309", "size_bytes": 9177}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "581c9a73e86109967cf567acecbaf73d4773807e40a185e1d4c745bfac323ab1", "size_bytes": 9177}`, recovered `{"sha256": "9fa8dc7685b84abeaddf991484607fc8ce70ae5aa7b9b9dbae54506301ce1f49", "size_bytes": 8957}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "581c9a73e86109967cf567acecbaf73d4773807e40a185e1d4c745bfac323ab1", "size_bytes": 9177}`, recovered `{"sha256": "e666a82c3af99d484476139697849321ad4ac5109ccd2619e667fb238359698c", "size_bytes": 9255}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "581c9a73e86109967cf567acecbaf73d4773807e40a185e1d4c745bfac323ab1", "size_bytes": 9177}`, recovered `{"sha256": "f0be6ffe09fbb97fbaacd80c568f8de982f250b9150b75f6206fb2ff0c38e309", "size_bytes": 9177}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `84480`, recovered `16896`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `84480`, recovered `18432`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `84480`, recovered `29184`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `22547`, recovered `14193`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `22547`, recovered `18912`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `22547`, recovered `26149`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `6925`, recovered `3594`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `6925`, recovered `3714`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `6925`, recovered `4167`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `977`, recovered `1339`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `977`, recovered `727`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `977`, recovered `768`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `407.731`, recovered `211.876`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `407.731`, recovered `220.532`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `407.731`, recovered `236.242`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.269244Z-46336-d496da77"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.270567Z-46338-4d93508c"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T142442.442815Z-1419-353e743c"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.archive_member.999d2352aa821062f7f6f749e85855dd90d36caeb61734f1b3b077016d21dc56`: kept `{"archive_member": null, "sha256": "999d2352aa821062f7f6f749e85855dd90d36caeb61734f1b3b077016d21dc56", "size_bytes": 5294}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.archive_member.a92b2f007a50005460ae7006de2faf9c99b2ef1fd71b52f8c37ab9b036e7725c`: kept `{"archive_member": null, "sha256": "a92b2f007a50005460ae7006de2faf9c99b2ef1fd71b52f8c37ab9b036e7725c", "size_bytes": 5536}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.archive_member.aac1720ba895e44413b63c823779d47077e408f77e68dc76d023f4c7c49f073b`: kept `{"archive_member": null, "sha256": "aac1720ba895e44413b63c823779d47077e408f77e68dc76d023f4c7c49f073b", "size_bytes": 6562}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "de117dd3450a6e6ec1678394c4495e300e88a436690f1b2ecfc731485ece92f9", "size_bytes": 5629}`, recovered `{"sha256": "999d2352aa821062f7f6f749e85855dd90d36caeb61734f1b3b077016d21dc56", "size_bytes": 5294}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "de117dd3450a6e6ec1678394c4495e300e88a436690f1b2ecfc731485ece92f9", "size_bytes": 5629}`, recovered `{"sha256": "a92b2f007a50005460ae7006de2faf9c99b2ef1fd71b52f8c37ab9b036e7725c", "size_bytes": 5536}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "de117dd3450a6e6ec1678394c4495e300e88a436690f1b2ecfc731485ece92f9", "size_bytes": 5629}`, recovered `{"sha256": "aac1720ba895e44413b63c823779d47077e408f77e68dc76d023f4c7c49f073b", "size_bytes": 6562}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `27648`, recovered `14208`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `27648`, recovered `29696`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `27648`, recovered `36352`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.input_tokens`: kept `21375`, recovered `19098`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.input_tokens`: kept `21375`, recovered `20821`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.input_tokens`: kept `21375`, recovered `7774`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.output_tokens`: kept `3322`, recovered `2058`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.output_tokens`: kept `3322`, recovered `2082`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.output_tokens`: kept `3322`, recovered `2177`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `338`, recovered `170`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `338`, recovered `43`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `338`, recovered `73`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `wall_s`: kept `214.729`, recovered `144.349`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `wall_s`: kept `214.729`, recovered `149.675`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `wall_s`: kept `214.729`, recovered `281.515`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.269244Z-46336-d496da77"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T140043.270567Z-46338-4d93508c"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `experiment`: kept `"20260930T142442.445867Z-1420-059c9961"`, recovered `"20260930T142442.442815Z-1419-353e743c"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.archive_member.3a8501e8913bbcd00a3f6b4865195dff03fb25f72296705fea667b710643fb0e`: kept `{"archive_member": null, "sha256": "3a8501e8913bbcd00a3f6b4865195dff03fb25f72296705fea667b710643fb0e", "size_bytes": 5926}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.archive_member.764b160c18124007f9a0525643fb6f69f66bb46985e88dc452ac8871be8b5832`: kept `{"archive_member": null, "sha256": "764b160c18124007f9a0525643fb6f69f66bb46985e88dc452ac8871be8b5832", "size_bytes": 6739}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.archive_member.ce0c19a3f4c7ba9bda6fbccf306f311d83c39501510f22d6ba1e7e6bd6868c53`: kept `{"archive_member": null, "sha256": "ce0c19a3f4c7ba9bda6fbccf306f311d83c39501510f22d6ba1e7e6bd6868c53", "size_bytes": 5295}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "c5e24c5b7eb6e770aa8cb63c362195c746f4c835c506ea6b0956a2eae94a3ddd", "size_bytes": 5917}`, recovered `{"sha256": "3a8501e8913bbcd00a3f6b4865195dff03fb25f72296705fea667b710643fb0e", "size_bytes": 5926}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "c5e24c5b7eb6e770aa8cb63c362195c746f4c835c506ea6b0956a2eae94a3ddd", "size_bytes": 5917}`, recovered `{"sha256": "764b160c18124007f9a0525643fb6f69f66bb46985e88dc452ac8871be8b5832", "size_bytes": 6739}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "c5e24c5b7eb6e770aa8cb63c362195c746f4c835c506ea6b0956a2eae94a3ddd", "size_bytes": 5917}`, recovered `{"sha256": "ce0c19a3f4c7ba9bda6fbccf306f311d83c39501510f22d6ba1e7e6bd6868c53", "size_bytes": 5295}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `93696`, recovered `24320`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `93696`, recovered `29440`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `93696`, recovered `32512`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.input_tokens`: kept `48192`, recovered `14209`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.input_tokens`: kept `48192`, recovered `17705`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.input_tokens`: kept `48192`, recovered `22197`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.output_tokens`: kept `4050`, recovered `2033`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.output_tokens`: kept `4050`, recovered `2123`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.output_tokens`: kept `4050`, recovered `2240`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `270`, recovered `49`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `270`, recovered `55`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `270`, recovered `81`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `wall_s`: kept `268.091`, recovered `147.526`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `wall_s`: kept `268.091`, recovered `154.166`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `wall_s`: kept `268.091`, recovered `165.768`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 55 missing published metadata). Missing counters remain unknown, not zero.
This round also has 55 raw-only or non-public rows; they are kept separate from the published-export denominator.
