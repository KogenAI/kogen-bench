# x race

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of ARITHMETIC_UNRECOMPUTABLE, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **ARITHMETIC_UNRECOMPUTABLE:** The reported 48-cell pass total is not reproducible from retained records.
- **RAW_EVIDENCE_MISSING:** Exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H29, H30 (provisional mapping; see the hypothesis register).
Question: Do racing multiple workers improve selected task outcomes over simpler arms when a deterministic selector chooses a candidate?
Population: Six tasks × two repetitions × four arms = 48 reported cells.
Headline: No superiority or deployment claim; the pass total is source-reported and not reproducible.

## Reported observations

- The four-arm panel is reported as 48/48 graded passes, a ceiling result on this task set. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A selector false-acceptance check is reported as 0/24. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- No two-agent policy was promoted. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Exact harness/Kogen revision was not recovered. |
| Model and effort | Per-arm model and effort values were not recovered in the public snapshot. |
| Task IDs | Six tasks are reported; exact public task IDs are not recovered. |
| Command | Not recovered; public launch command and cell IDs are unavailable. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** A ceiling panel cannot estimate improvement in success rate, and the selector check does not qualify a live multi-agent route.

**Smallest useful next test:** Use tasks with measured headroom, compare solo and race under a frozen selection rule, and report wall time and token cost by task.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/x-race.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 53 rows (pass 50, restore_failed 2, ungraded 1); overall pass rate is 100.0% (50/50) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 24 field mismatches across 1 cell IDs (`experiment` 3, `patch.archive_member.5d61af3600d5819e6afd65f6c8cad5822cdea2b1b86fddbef3b85a71f6abe5ba` 1, `patch.archive_member.ce248f8131723e78bfca8d78f032869d5706e93bb474aa0aa3239e4df52d3059` 1, `patch.archive_member.f2aa98beee3bceb8e81c28be19b824754fa7ddf26b28d55d076739206937dd32` 1, `patch.attempt-1` 3, `usage.cached_input_tokens` 3, `usage.input_tokens` 3, `usage.output_tokens` 3, `usage.reasoning_tokens` 3, `wall_s` 3). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `experiment`: kept `"20260930T141459.099867Z-61322-f9e406cf"`, recovered `"20260930T141459.206999Z-61332-a1b32472"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `experiment`: kept `"20260930T141459.099867Z-61322-f9e406cf"`, recovered `"20260930T160600.797428Z-8421-27c94025"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `experiment`: kept `"20260930T141459.099867Z-61322-f9e406cf"`, recovered `"20260930T160600.906404Z-8424-4b907a91"`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.archive_member.5d61af3600d5819e6afd65f6c8cad5822cdea2b1b86fddbef3b85a71f6abe5ba`: kept `{"archive_member": null, "sha256": "5d61af3600d5819e6afd65f6c8cad5822cdea2b1b86fddbef3b85a71f6abe5ba", "size_bytes": 3303}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.archive_member.ce248f8131723e78bfca8d78f032869d5706e93bb474aa0aa3239e4df52d3059`: kept `{"archive_member": null, "sha256": "ce248f8131723e78bfca8d78f032869d5706e93bb474aa0aa3239e4df52d3059", "size_bytes": 4714}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.archive_member.f2aa98beee3bceb8e81c28be19b824754fa7ddf26b28d55d076739206937dd32`: kept `{"archive_member": null, "sha256": "f2aa98beee3bceb8e81c28be19b824754fa7ddf26b28d55d076739206937dd32", "size_bytes": 4813}`, recovered `null`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.attempt-1`: kept `{"sha256": "af7fbae8d5d97d47794f98fcca0706450b10614ac0fb407e5b15fd2684d9d4fc", "size_bytes": 5506}`, recovered `{"sha256": "5d61af3600d5819e6afd65f6c8cad5822cdea2b1b86fddbef3b85a71f6abe5ba", "size_bytes": 3303}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.attempt-1`: kept `{"sha256": "af7fbae8d5d97d47794f98fcca0706450b10614ac0fb407e5b15fd2684d9d4fc", "size_bytes": 5506}`, recovered `{"sha256": "ce248f8131723e78bfca8d78f032869d5706e93bb474aa0aa3239e4df52d3059", "size_bytes": 4714}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `patch.attempt-1`: kept `{"sha256": "af7fbae8d5d97d47794f98fcca0706450b10614ac0fb407e5b15fd2684d9d4fc", "size_bytes": 5506}`, recovered `{"sha256": "f2aa98beee3bceb8e81c28be19b824754fa7ddf26b28d55d076739206937dd32", "size_bytes": 4813}`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.cached_input_tokens`: kept `5120`, recovered `24576`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.cached_input_tokens`: kept `5120`, recovered `61312`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.cached_input_tokens`: kept `5120`, recovered `89088`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.input_tokens`: kept `22131`, recovered `18483`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.input_tokens`: kept `22131`, recovered `34962`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.input_tokens`: kept `22131`, recovered `35200`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.output_tokens`: kept `1849`, recovered `1568`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.output_tokens`: kept `1849`, recovered `3261`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.output_tokens`: kept `1849`, recovered `3702`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.reasoning_tokens`: kept `178`, recovered `337`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.reasoning_tokens`: kept `178`, recovered `586`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `usage.reasoning_tokens`: kept `178`, recovered `75`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `wall_s`: kept `124.299`, recovered `107.748`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `wall_s`: kept `124.299`, recovered `125.358`.
- `kh-gpt__gpt-6.1-sol__high__default__elx-02-ingest-supervision__r1` field `wall_s`: kept `124.299`, recovered `131.456`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 53 missing published metadata). Missing counters remain unknown, not zero.
This round also has 53 raw-only or non-public rows; they are kept separate from the published-export denominator.
