# x minikogen

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** Exact allocation by mechanism is not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H31, H32 (provisional mapping; see the hypothesis register).
Question: Can selected Kogen loop mechanisms be removed or simplified without reducing task outcomes or coverage?
Population: Five mechanism pairs are reported at n=4 per arm; exact allocation by mechanism is not recovered.
Headline: No net simplification claim.

## Reported observations

- Test-first removal is reported at 4/4 versus 4/4; reported wall changed from 2,658 to 1,586 seconds, while coverage equivalence was not measured. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A frozen-decision answer mechanism is reported to change strict acceptance from 2/4 to 4/4 at higher cost. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No net simplification was established. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Model and effort per mechanism pair were not recovered. |
| Task IDs | Exact task IDs are not recovered. |
| Command | Not recovered; no public launch command or cell IDs are available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** The mechanism pairs do not isolate an overall simplification benefit, and the reported coverage measure is incomplete.

**Smallest useful next test:** Freeze one mechanism at a time, preserve equivalent checks and coverage, and publish paired task-level cost and outcome records.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-minikogen.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 71 rows (fail 2, infra 8, pass 50, restore_failed 8, ungraded 3); overall pass rate is 96.2% (50/52) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 66 field mismatches across 4 cell IDs (`experiment` 8, `patch.archive_member.45ddb2bec508950c03f334ee6e84923baab6ee912beda8e36115ec1e3b32fe9b` 1, `patch.archive_member.484c3aab3d9fbd90fac5ac93445af9e195a62e3ec73badd8926c14d4366b114e` 1, `patch.archive_member.5d41d0f3fa19f66dd614ba2506e6d06851b919420c91db95630c97d61ffa90a3` 1, `patch.archive_member.7a0da55fa33ea386b996c8964326a7c82e448840194293a694f9cc79df7a40cd` 1, `patch.archive_member.7fcc0c03c550ab07f660a80ca0744e27017234425a3c67f388691288f650fb97` 1, `patch.archive_member.95134704909e1f59ddd949393d920cecd3b47edd30d502d7223d1d914004712d` 1, `patch.archive_member.c0a53d19c13cb8a415b3169dcd110f358edd483e3e0757cc197d9d1ea3a1e93d` 1, `patch.archive_member.e10b628a20a3fc9d7b9bc072a8c8d87d02566900a39c2beb96bb9f150a4880fd` 1, `patch.attempt-1` 8, `status` 2, `usage.cached_input_tokens` 8, `usage.input_tokens` 8, `usage.output_tokens` 8, `usage.reasoning_tokens` 8, `wall_s` 8). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T141438.578575Z-60458-cb649c58"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T150615.536466Z-96859-f2dde97d"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.7a0da55fa33ea386b996c8964326a7c82e448840194293a694f9cc79df7a40cd`: kept `{"archive_member": null, "sha256": "7a0da55fa33ea386b996c8964326a7c82e448840194293a694f9cc79df7a40cd", "size_bytes": 11727}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.archive_member.95134704909e1f59ddd949393d920cecd3b47edd30d502d7223d1d914004712d`: kept `{"archive_member": null, "sha256": "95134704909e1f59ddd949393d920cecd3b47edd30d502d7223d1d914004712d", "size_bytes": 8938}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "566af9f355815521e2cfdf4a73d2245aa4191303e72f8a3c0839ba4d999e6b73", "size_bytes": 8997}`, recovered `{"sha256": "7a0da55fa33ea386b996c8964326a7c82e448840194293a694f9cc79df7a40cd", "size_bytes": 11727}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `patch.attempt-1`: kept `{"sha256": "566af9f355815521e2cfdf4a73d2245aa4191303e72f8a3c0839ba4d999e6b73", "size_bytes": 8997}`, recovered `{"sha256": "95134704909e1f59ddd949393d920cecd3b47edd30d502d7223d1d914004712d", "size_bytes": 8938}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `16640`, recovered `155008`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.cached_input_tokens`: kept `16640`, recovered `48896`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `19818`, recovered `28614`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.input_tokens`: kept `19818`, recovered `79572`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `3693`, recovered `3977`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.output_tokens`: kept `3693`, recovered `7547`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `801`, recovered `1780`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `usage.reasoning_tokens`: kept `801`, recovered `732`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `230.325`, recovered `231.984`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r1` field `wall_s`: kept `230.325`, recovered `514.678`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T141438.578575Z-60458-cb649c58"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T150615.536466Z-96859-f2dde97d"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.45ddb2bec508950c03f334ee6e84923baab6ee912beda8e36115ec1e3b32fe9b`: kept `{"archive_member": null, "sha256": "45ddb2bec508950c03f334ee6e84923baab6ee912beda8e36115ec1e3b32fe9b", "size_bytes": 11100}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.archive_member.484c3aab3d9fbd90fac5ac93445af9e195a62e3ec73badd8926c14d4366b114e`: kept `{"archive_member": null, "sha256": "484c3aab3d9fbd90fac5ac93445af9e195a62e3ec73badd8926c14d4366b114e", "size_bytes": 9480}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "0081e6b609adb6cc4005454321a90672db1d165a1ca90de9b860bd424830e38b", "size_bytes": 8220}`, recovered `{"sha256": "45ddb2bec508950c03f334ee6e84923baab6ee912beda8e36115ec1e3b32fe9b", "size_bytes": 11100}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `patch.attempt-1`: kept `{"sha256": "0081e6b609adb6cc4005454321a90672db1d165a1ca90de9b860bd424830e38b", "size_bytes": 8220}`, recovered `{"sha256": "484c3aab3d9fbd90fac5ac93445af9e195a62e3ec73badd8926c14d4366b114e", "size_bytes": 9480}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `21888`, recovered `169728`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.cached_input_tokens`: kept `21888`, recovered `17664`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `19341`, recovered `18297`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.input_tokens`: kept `19341`, recovered `74222`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `3524`, recovered `3604`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.output_tokens`: kept `3524`, recovered `7656`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `670`, recovered `2118`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `usage.reasoning_tokens`: kept `670`, recovered `770`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `215.84`, recovered `211.828`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-05-cache-single-flight__r2` field `wall_s`: kept `215.84`, recovered `507.156`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T141438.578575Z-60458-cb649c58"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T150615.536466Z-96859-f2dde97d"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.archive_member.c0a53d19c13cb8a415b3169dcd110f358edd483e3e0757cc197d9d1ea3a1e93d`: kept `{"archive_member": null, "sha256": "c0a53d19c13cb8a415b3169dcd110f358edd483e3e0757cc197d9d1ea3a1e93d", "size_bytes": 7689}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.archive_member.e10b628a20a3fc9d7b9bc072a8c8d87d02566900a39c2beb96bb9f150a4880fd`: kept `{"archive_member": null, "sha256": "e10b628a20a3fc9d7b9bc072a8c8d87d02566900a39c2beb96bb9f150a4880fd", "size_bytes": 5070}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "091d70453548c7b16a79de25616938660b45a2dc9f1d647124f281fdd2e7878e", "size_bytes": 6263}`, recovered `{"sha256": "c0a53d19c13cb8a415b3169dcd110f358edd483e3e0757cc197d9d1ea3a1e93d", "size_bytes": 7689}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `patch.attempt-1`: kept `{"sha256": "091d70453548c7b16a79de25616938660b45a2dc9f1d647124f281fdd2e7878e", "size_bytes": 6263}`, recovered `{"sha256": "e10b628a20a3fc9d7b9bc072a8c8d87d02566900a39c2beb96bb9f150a4880fd", "size_bytes": 5070}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `status`: kept `"ok"`, recovered `"error"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `83200`, recovered `173568`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.cached_input_tokens`: kept `83200`, recovered `34304`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.input_tokens`: kept `32308`, recovered `16485`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.input_tokens`: kept `32308`, recovered `57791`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.output_tokens`: kept `2213`, recovered `2010`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.output_tokens`: kept `2213`, recovered `4504`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `117`, recovered `304`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `usage.reasoning_tokens`: kept `117`, recovered `67`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `wall_s`: kept `163.775`, recovered `140.931`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r1` field `wall_s`: kept `163.775`, recovered `333.419`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T141438.578575Z-60458-cb649c58"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `experiment`: kept `"20260930T133214.245115Z-24935-e6b6b08c"`, recovered `"20260930T150615.536466Z-96859-f2dde97d"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.archive_member.5d41d0f3fa19f66dd614ba2506e6d06851b919420c91db95630c97d61ffa90a3`: kept `{"archive_member": null, "sha256": "5d41d0f3fa19f66dd614ba2506e6d06851b919420c91db95630c97d61ffa90a3", "size_bytes": 5287}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.archive_member.7fcc0c03c550ab07f660a80ca0744e27017234425a3c67f388691288f650fb97`: kept `{"archive_member": null, "sha256": "7fcc0c03c550ab07f660a80ca0744e27017234425a3c67f388691288f650fb97", "size_bytes": 7098}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "2a6e88a1bc1962f44c6dec0fafe10c9462fe49be869877c051f9f4781ae169ce", "size_bytes": 5469}`, recovered `{"sha256": "5d41d0f3fa19f66dd614ba2506e6d06851b919420c91db95630c97d61ffa90a3", "size_bytes": 5287}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `patch.attempt-1`: kept `{"sha256": "2a6e88a1bc1962f44c6dec0fafe10c9462fe49be869877c051f9f4781ae169ce", "size_bytes": 5469}`, recovered `{"sha256": "7fcc0c03c550ab07f660a80ca0744e27017234425a3c67f388691288f650fb97", "size_bytes": 7098}`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `status`: kept `"ok"`, recovered `"error"`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `30208`, recovered `157824`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.cached_input_tokens`: kept `30208`, recovered `22912`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.input_tokens`: kept `17418`, recovered `17783`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.input_tokens`: kept `17418`, recovered `52947`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.output_tokens`: kept `2081`, recovered `1983`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.output_tokens`: kept `2081`, recovered `4278`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `73`, recovered `241`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `usage.reasoning_tokens`: kept `73`, recovered `46`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `wall_s`: kept `156.611`, recovered `145.69`.
- `kh-gpt__gpt-6.1-sol__high__default__rt-02__r2` field `wall_s`: kept `156.611`, recovered `301.689`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 71 missing published metadata). Missing counters remain unknown, not zero.
This round also has 71 raw-only or non-public rows; they are kept separate from the published-export denominator.
