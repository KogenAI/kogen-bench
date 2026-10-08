# Claim B worker rerun

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of CONFOUNDED_ASSIGNMENT, OUTCOME_CROSSWALK_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

### Why not VALID
- **CONFOUNDED_ASSIGNMENT:** Host is assigned by repetition, confounding the reported comparison.
- **OUTCOME_CROSSWALK_MISSING:** No exact-ID grade crosswalk or complete raw grade bundle is present.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the public capture manifest is linked above; the scored source rows and a complete raw request/grade bundle are not present in this snapshot.


STATUS: **CONFOUNDED**

Status reason: the research summary reports a host-by-repetition assignment, while the public snapshot contains no exact-ID grade crosswalk. The result remains a source-reported replication, not a verified comparison.

See [missing evidence](MISSING.md) for release blockers.

Hypotheses covered: **H21–H22**, custom-harness parity and end-to-end comparison. The reported rerun does not show a retry-policy benefit.

## Design and correction status

The research summary describes a worker rerun after the transport correction, with a setup amendment and a retry variant. It identifies host as repetition, which limits interpretation. The public capture contains no exact IDs for this rerun or its setup failures, so this page withholds the source-reported outcome totals and does not verify a retry-policy benefit.

## Public capture

The [public capture manifest](public-capture-manifest.csv) is header-only: no delivery ID could be assigned to this named rerun. The public [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl) do not provide an exact-ID grade crosswalk for these reported outcomes.

## Reproduction record

- Harness and Kogen revision: full commit SHAs are not bound to the scored cells in the public record.
- Model and effort: no public exact-ID record binds the model and effort to this scored cohort.
- Task IDs: the exact scored task IDs are not enumerated in the cited public summary.
- Historical launch command: not recoverable from the public record.
- Rebuild the sanitized public ledgers with `python3 reproduce/build_records.py` and `python3 reproduce/export_results.py`. This does not rerun or grade the historical cells.
- Raw public records: [run-record index](../../results/run-records/index.json) and [cells.jsonl](../../results/cells.jsonl); no exact rerun IDs are present in the capture manifest.

## Interpretation

Keep this worker rerun separate from the transport-confounded Studio screen. The source-reported equal scores do not verify the retry fix, because the public grade rows and full cohort assignment are missing and host is confounded with repetition.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/claim-b-rerun-1.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 57 rows (fail 18, pass 36, ungraded 3); overall pass rate is 66.7% (36/54) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 6/6 shared cell IDs match; 0/0 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 84 field mismatches across 6 cell IDs (`patch.attempt-1` 6, `round` 6, `usage.cached_input_tokens` 12, `usage.input_tokens` 12, `usage.output_tokens` 12, `usage.reasoning_tokens` 12, `versions.cli` 12, `wall_s` 12). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `patch.attempt-1`: kept `{"sha256": "7d00500f707d3cec10092d90a9fe9e805569a713037424fb54b28f0940fba613", "size_bytes": 7498}`, recovered `{"sha256": "e8e90936c9419eb2207fb3fb33d5c201dceb853d838ffec20811b0575514b373", "size_bytes": 7246}`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `round`: kept `"r60"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `392448`, recovered `470400`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `392448`, recovered `470400`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `46859`, recovered `37401`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `46859`, recovered `37401`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `5364`, recovered `5327`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `5364`, recovered `5327`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1143`, recovered `905`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1143`, recovered `905`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `wall_s`: kept `262.757`, recovered `318.951`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r1-Codex-Sol-high-r60-studio` field `wall_s`: kept `262.757`, recovered `318.951`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `patch.attempt-1`: kept `{"sha256": "4f53e69008ab19fa86921a7f34ec768770d4b56cf4a120a9a2252002e493ed87", "size_bytes": 5831}`, recovered `{"sha256": "abd864cc93dbe0cb523964d2353e46d231a0e6b8cd87736c8b7511971de71a57", "size_bytes": 6623}`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `round`: kept `"r60"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `487424`, recovered `714624`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `487424`, recovered `714624`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `35772`, recovered `70041`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `35772`, recovered `70041`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `7075`, recovered `6386`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `7075`, recovered `6386`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `2002`, recovered `1683`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `2002`, recovered `1683`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `wall_s`: kept `336.115`, recovered `426.686`.
- `codex__gpt-6.1-sol__high__default__rails-aj-enqueue-after-commit__r2-Codex-Sol-high-r60-studio` field `wall_s`: kept `336.115`, recovered `426.686`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `patch.attempt-1`: kept `{"sha256": "5d905eedddfa769a1f128bd11196e96cf47c9f6486a66bca3ee182ced4172f8e", "size_bytes": 6865}`, recovered `{"sha256": "a11da3fe98978525fb2cfe04de1cfddd7fdfa85ac4b794bb19daaf36b1446dd4", "size_bytes": 6784}`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `round`: kept `"r53"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.cached_input_tokens`: kept `246400`, recovered `237056`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.cached_input_tokens`: kept `246400`, recovered `237056`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.input_tokens`: kept `19464`, recovered `54393`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.input_tokens`: kept `19464`, recovered `54393`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.output_tokens`: kept `4577`, recovered `5390`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.output_tokens`: kept `4577`, recovered `5390`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.reasoning_tokens`: kept `1328`, recovered `1529`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `usage.reasoning_tokens`: kept `1328`, recovered `1529`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `wall_s`: kept `255.175`, recovered `314.738`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r1-Codex-Sol-high-r53-studio` field `wall_s`: kept `255.175`, recovered `314.738`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `patch.attempt-1`: kept `{"sha256": "238d188f0933b6ef69adc3b09b5b5a13d8b308f2c12eddba6ed3bce10b50ad84", "size_bytes": 7219}`, recovered `{"sha256": "8adaadcfd29048c3be8b5b9e6fd0a340c6cb8d1a13b2645d24160ddc96cfa3bd", "size_bytes": 6496}`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `round`: kept `"r53"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.cached_input_tokens`: kept `200192`, recovered `257664`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.cached_input_tokens`: kept `200192`, recovered `257664`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.input_tokens`: kept `25571`, recovered `43337`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.input_tokens`: kept `25571`, recovered `43337`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.output_tokens`: kept `4495`, recovered `4753`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.output_tokens`: kept `4495`, recovered `4753`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.reasoning_tokens`: kept `1568`, recovered `1573`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `usage.reasoning_tokens`: kept `1568`, recovered `1573`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `wall_s`: kept `196.494`, recovered `307.614`.
- `codex__gpt-6.1-sol__high__default__rails-ar-atomic-import__r2-Codex-Sol-high-r53-studio` field `wall_s`: kept `196.494`, recovered `307.614`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `patch.attempt-1`: kept `{"sha256": "4e1b442cc5e7e999e56a839224dd241535d90df37948ef8c752d8a4ab3d8a946", "size_bytes": 13717}`, recovered `{"sha256": "b6f2c19b505e1abb18d2bde7993e96089496cb2aef2d313552b3117b7e148a81", "size_bytes": 15919}`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `round`: kept `"r60"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `586752`, recovered `1438208`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `586752`, recovered `1438208`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `49014`, recovered `80937`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `49014`, recovered `80937`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `6402`, recovered `13020`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `6402`, recovered `13020`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1018`, recovered `4157`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1018`, recovered `4157`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `wall_s`: kept `325.932`, recovered `795.414`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r1-Codex-Sol-high-r60-studio` field `wall_s`: kept `325.932`, recovered `795.414`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `patch.attempt-1`: kept `{"sha256": "0bc487ebe0a29fb7d523f40766d71e67d833184f963476a838227ad4f9c28a7b", "size_bytes": 14040}`, recovered `{"sha256": "4dedec6faa665d9523a330f7f7d212d1cc307cb84ffbd9808a4c77d7f8d2b747", "size_bytes": 15061}`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `round`: kept `"r60"`, recovered `"claim-b-rerun-1"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `699264`, recovered `1122304`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.cached_input_tokens`: kept `699264`, recovered `1122304`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `47425`, recovered `74627`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.input_tokens`: kept `47425`, recovered `74627`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `6950`, recovered `9868`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.output_tokens`: kept `6950`, recovered `9868`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1098`, recovered `2057`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `usage.reasoning_tokens`: kept `1098`, recovered `2057`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `versions.cli`: kept `"codex-cli 0.160.0"`, recovered `"codex-cli 0.159.2"`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `wall_s`: kept `327.598`, recovered `595.768`.
- `codex__gpt-6.1-sol__high__default__rails-sec-audit-sweep__r2-Codex-Sol-high-r60-studio` field `wall_s`: kept `327.598`, recovered `595.768`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 6/6 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
This round also has 51 raw-only or non-public rows; they are kept separate from the published-export denominator.
