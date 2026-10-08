# x mining

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_MISMATCH, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_MISMATCH:** The inventory, usage audit, and diagnostic panel are distinct populations.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H80, H84, H89 (provisional mapping; see the hypothesis register).
Question: Can observed development-run failures be classified into reusable failure modes, and does a diagnostic playbook change outcomes?
Population: The observation inventory and X09 panel are separate populations; neither supplies an ITT denominator for the other.
Headline: Inventory and diagnostic only.

## Reported observations

- The inventory reports 2,608 contestant observations: 2,152 PASS, 295 FAIL, 54 INFRA and 107 PENDING. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate usage audit reports missing usage on 124/2,649 observations; this denominator is not the 2,608 status inventory. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- X09 reports 14/14 completed, described as inconclusive. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Mixed versions; no single exact harness/Kogen SHA applies to the inventory. |
| Model and effort | Mixed model/harness versions; per-observation model and effort are not present in the public summary. |
| Task IDs | Task IDs for the inventory and X09 panel are not recovered. |
| Command | Not recovered; no mining or X09 launch command is published. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** Mixed versions, distinct denominators and the diagnostic selection prevent a general failure-rate or playbook-efficacy claim.

**Smallest useful next test:** Freeze the event schema and cohort, reconcile all attempts and missing usage, then validate a failure classifier prospectively against blinded outcomes.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-mining.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 49 rows (fail 3, pass 46); overall pass rate is 93.9% (46/49) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 88 field mismatches across 3 cell IDs (`experiment` 11, `manifest_grade.classification` 1, `manifest_grade.outcome` 1, `manifest_grade.pass_fail` 1, `patch.archive_member.104f4780a6b3d94753664450adbe420b153f76ba8c157c53c0862f300c2cc9c7` 1, `patch.archive_member.43a33c89a961a7750c66409c33fda4605dcc4d26ecd424285125ff890de3bdd3` 1, `patch.archive_member.5b6e2f6709a7ad212eddf931ef463db146ae5959f39bf726ac31a1b2508273c4` 1, `patch.archive_member.6706bbedad1375e4f787fc048c9e3f339349ee0f6e3cac301aefc5d3d4b10885` 1, `patch.archive_member.684891b2fbc870537cf33e5729a1ff16556c3cf84bd01e43d57419b4c9103415` 1, `patch.archive_member.8243909697b293052e7c43de577946e44d38afc08d01072fe0f6bf46d7cbaf44` 1, `patch.archive_member.9e23d6a3268fb5bdb7583d795e50729782d5a585fa87a4e5ef87a3a48c1387a8` 1, `patch.archive_member.a9a88b209a4d54f0ccd55abaaf948ae2d1a7b39034d1e66e470ed2dbce509aa9` 1, `patch.archive_member.ad0ba5529a977687958ba00346765f1d10cff816b1637fb9b7466a46b9053be2` 1, `patch.attempt-1` 10, `usage.cached_input_tokens` 11, `usage.input_tokens` 11, `usage.output_tokens` 11, `usage.reasoning_tokens` 11, `wall_s` 11). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `experiment`: kept `"20260930T141520.976613Z-62893-7e27b289"`, recovered `"20260930T140204.331928Z-47797-cd88c72e"`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `experiment`: kept `"20260930T141520.976613Z-62893-7e27b289"`, recovered `"20260930T140204.331928Z-47798-8595f9d5"`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `experiment`: kept `"20260930T141520.976613Z-62893-7e27b289"`, recovered `"20260930T141520.976619Z-62892-49c08869"`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.archive_member.104f4780a6b3d94753664450adbe420b153f76ba8c157c53c0862f300c2cc9c7`: kept `{"archive_member": null, "sha256": "104f4780a6b3d94753664450adbe420b153f76ba8c157c53c0862f300c2cc9c7", "size_bytes": 6998}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.archive_member.684891b2fbc870537cf33e5729a1ff16556c3cf84bd01e43d57419b4c9103415`: kept `{"archive_member": null, "sha256": "684891b2fbc870537cf33e5729a1ff16556c3cf84bd01e43d57419b4c9103415", "size_bytes": 6739}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.archive_member.a9a88b209a4d54f0ccd55abaaf948ae2d1a7b39034d1e66e470ed2dbce509aa9`: kept `{"archive_member": null, "sha256": "a9a88b209a4d54f0ccd55abaaf948ae2d1a7b39034d1e66e470ed2dbce509aa9", "size_bytes": 8979}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.attempt-1`: kept `{"sha256": "20e4b34797c0a0b9d4378aa90afa8cb11d1a80183573a960b2ec0a399dceca9a", "size_bytes": 6301}`, recovered `{"sha256": "104f4780a6b3d94753664450adbe420b153f76ba8c157c53c0862f300c2cc9c7", "size_bytes": 6998}`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.attempt-1`: kept `{"sha256": "20e4b34797c0a0b9d4378aa90afa8cb11d1a80183573a960b2ec0a399dceca9a", "size_bytes": 6301}`, recovered `{"sha256": "684891b2fbc870537cf33e5729a1ff16556c3cf84bd01e43d57419b4c9103415", "size_bytes": 6739}`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `patch.attempt-1`: kept `{"sha256": "20e4b34797c0a0b9d4378aa90afa8cb11d1a80183573a960b2ec0a399dceca9a", "size_bytes": 6301}`, recovered `{"sha256": "a9a88b209a4d54f0ccd55abaaf948ae2d1a7b39034d1e66e470ed2dbce509aa9", "size_bytes": 8979}`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.cached_input_tokens`: kept `45568`, recovered `125440`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.cached_input_tokens`: kept `45568`, recovered `36864`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.cached_input_tokens`: kept `45568`, recovered `39424`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.input_tokens`: kept `14456`, recovered `24635`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.input_tokens`: kept `14456`, recovered `25241`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.input_tokens`: kept `14456`, recovered `25877`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.output_tokens`: kept `4408`, recovered `4715`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.output_tokens`: kept `4408`, recovered `4726`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.output_tokens`: kept `4408`, recovered `5748`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.reasoning_tokens`: kept `1311`, recovered `1056`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.reasoning_tokens`: kept `1311`, recovered `1440`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `usage.reasoning_tokens`: kept `1311`, recovered `1480`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `wall_s`: kept `152.821`, recovered `128.749`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `wall_s`: kept `152.821`, recovered `140.187`.
- `kh-gpt__gpt-6-luna__high__default__elx-04-queue-backpressure__r1` field `wall_s`: kept `152.821`, recovered `156.526`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `experiment`: kept `"20260930T161522.590747Z-32743-2e4f74fc"`, recovered `"20260930T141757.533755Z-77474-7ebc351b"`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `experiment`: kept `"20260930T161522.590747Z-32743-2e4f74fc"`, recovered `"20260930T141811.633758Z-78865-e58f643f"`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `experiment`: kept `"20260930T161522.590747Z-32743-2e4f74fc"`, recovered `"20260930T141933.854496Z-84362-3902f78a"`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `experiment`: kept `"20260930T161522.590747Z-32743-2e4f74fc"`, recovered `"20260930T142338.846283Z-99224-3bad3754"`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `experiment`: kept `"20260930T161522.590747Z-32743-2e4f74fc"`, recovered `"20260930T161745.495683Z-38847-82ae103c"`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.archive_member.43a33c89a961a7750c66409c33fda4605dcc4d26ecd424285125ff890de3bdd3`: kept `{"archive_member": null, "sha256": "43a33c89a961a7750c66409c33fda4605dcc4d26ecd424285125ff890de3bdd3", "size_bytes": 1997}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.archive_member.5b6e2f6709a7ad212eddf931ef463db146ae5959f39bf726ac31a1b2508273c4`: kept `{"archive_member": null, "sha256": "5b6e2f6709a7ad212eddf931ef463db146ae5959f39bf726ac31a1b2508273c4", "size_bytes": 1756}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.archive_member.6706bbedad1375e4f787fc048c9e3f339349ee0f6e3cac301aefc5d3d4b10885`: kept `{"archive_member": null, "sha256": "6706bbedad1375e4f787fc048c9e3f339349ee0f6e3cac301aefc5d3d4b10885", "size_bytes": 1977}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "e38078c14c3024cfcabc71f39955aa1c72cf0bf20f2cdb5790154a8fa3025dbc", "size_bytes": 522}`, recovered `{"sha256": "43a33c89a961a7750c66409c33fda4605dcc4d26ecd424285125ff890de3bdd3", "size_bytes": 1997}`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "e38078c14c3024cfcabc71f39955aa1c72cf0bf20f2cdb5790154a8fa3025dbc", "size_bytes": 522}`, recovered `{"sha256": "4dcfd2b86a60f733b1d705431856d0c1321656c0fd8ff49a4b9b54b45efa4af5", "size_bytes": 522}`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "e38078c14c3024cfcabc71f39955aa1c72cf0bf20f2cdb5790154a8fa3025dbc", "size_bytes": 522}`, recovered `{"sha256": "5b6e2f6709a7ad212eddf931ef463db146ae5959f39bf726ac31a1b2508273c4", "size_bytes": 1756}`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `patch.attempt-1`: kept `{"sha256": "e38078c14c3024cfcabc71f39955aa1c72cf0bf20f2cdb5790154a8fa3025dbc", "size_bytes": 522}`, recovered `{"sha256": "6706bbedad1375e4f787fc048c9e3f339349ee0f6e3cac301aefc5d3d4b10885", "size_bytes": 1977}`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `7168`, recovered `16384`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `7168`, recovered `28160`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `7168`, recovered `32768`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `7168`, recovered `37376`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.cached_input_tokens`: kept `7168`, recovered `8704`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.input_tokens`: kept `10831`, recovered `13139`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.input_tokens`: kept `10831`, recovered `14515`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.input_tokens`: kept `10831`, recovered `14893`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.input_tokens`: kept `10831`, recovered `14927`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.input_tokens`: kept `10831`, recovered `20298`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.output_tokens`: kept `630`, recovered `1628`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.output_tokens`: kept `630`, recovered `1694`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.output_tokens`: kept `630`, recovered `1707`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.output_tokens`: kept `630`, recovered `572`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.output_tokens`: kept `630`, recovered `719`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `130`, recovered `103`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `130`, recovered `160`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `130`, recovered `456`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `130`, recovered `486`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `usage.reasoning_tokens`: kept `130`, recovered `564`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `wall_s`: kept `55.312`, recovered `108.084`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `wall_s`: kept `55.312`, recovered `324.155`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `wall_s`: kept `55.312`, recovered `55.644`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `wall_s`: kept `55.312`, recovered `92.271`.
- `kh-gpt__gpt-6-luna__high__default__rt-06__r1` field `wall_s`: kept `55.312`, recovered `93.039`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `experiment`: kept `"20260930T155257.354081Z-9725-d911d7dc"`, recovered `"20260930T142032.073203Z-88707-70eac546"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `experiment`: kept `"20260930T155257.354081Z-9725-d911d7dc"`, recovered `"20260930T155215.164114Z-1210-8aa626f0"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `experiment`: kept `"20260930T155257.354081Z-9725-d911d7dc"`, recovered `"20260930T160231.380623Z-81576-d880607e"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `manifest_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `manifest_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `manifest_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.archive_member.8243909697b293052e7c43de577946e44d38afc08d01072fe0f6bf46d7cbaf44`: kept `{"archive_member": null, "sha256": "8243909697b293052e7c43de577946e44d38afc08d01072fe0f6bf46d7cbaf44", "size_bytes": 5807}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.archive_member.9e23d6a3268fb5bdb7583d795e50729782d5a585fa87a4e5ef87a3a48c1387a8`: kept `{"archive_member": null, "sha256": "9e23d6a3268fb5bdb7583d795e50729782d5a585fa87a4e5ef87a3a48c1387a8", "size_bytes": 5027}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.archive_member.ad0ba5529a977687958ba00346765f1d10cff816b1637fb9b7466a46b9053be2`: kept `{"archive_member": null, "sha256": "ad0ba5529a977687958ba00346765f1d10cff816b1637fb9b7466a46b9053be2", "size_bytes": 5512}`, recovered `null`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.attempt-1`: kept `{"sha256": "b74d8e4089d10254d88c753d56968320585d8160af9074524d72bea2760a6804", "size_bytes": 8192}`, recovered `{"sha256": "8243909697b293052e7c43de577946e44d38afc08d01072fe0f6bf46d7cbaf44", "size_bytes": 5807}`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.attempt-1`: kept `{"sha256": "b74d8e4089d10254d88c753d56968320585d8160af9074524d72bea2760a6804", "size_bytes": 8192}`, recovered `{"sha256": "9e23d6a3268fb5bdb7583d795e50729782d5a585fa87a4e5ef87a3a48c1387a8", "size_bytes": 5027}`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `patch.attempt-1`: kept `{"sha256": "b74d8e4089d10254d88c753d56968320585d8160af9074524d72bea2760a6804", "size_bytes": 8192}`, recovered `{"sha256": "ad0ba5529a977687958ba00346765f1d10cff816b1637fb9b7466a46b9053be2", "size_bytes": 5512}`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.cached_input_tokens`: kept `278528`, recovered `192512`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.cached_input_tokens`: kept `278528`, recovered `204800`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.cached_input_tokens`: kept `278528`, recovered `301056`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.input_tokens`: kept `50073`, recovered `26508`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.input_tokens`: kept `50073`, recovered `35374`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.input_tokens`: kept `50073`, recovered `36371`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.output_tokens`: kept `4757`, recovered `3158`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.output_tokens`: kept `4757`, recovered `3226`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.output_tokens`: kept `4757`, recovered `3380`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.reasoning_tokens`: kept `1121`, recovered `1105`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.reasoning_tokens`: kept `1121`, recovered `1111`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `usage.reasoning_tokens`: kept `1121`, recovered `967`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `wall_s`: kept `172.65`, recovered `127.86`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `wall_s`: kept `172.65`, recovered `135.96`.
- `kh-gpt__gpt-6-luna__high__default__syn-33-stale-event-ordering__r1` field `wall_s`: kept `172.65`, recovered `137.668`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 49 missing published metadata). Missing counters remain unknown, not zero.
This round also has 49 raw-only or non-public rows; they are kept separate from the published-export denominator.
