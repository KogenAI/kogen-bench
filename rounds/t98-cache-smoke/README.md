# T98 prompt-cache smoke

## Status

**PILOT**

### Why not VALID
- **PILOT_N1:** One-cell telemetry smoke only.
- **PRE_REGISTRATION_UNPROVEN:** No pre-registered rule predating the smoke result is established.
- **RAW_EVIDENCE_MISSING:** Raw per-request usage records are absent.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — One-cell cache telemetry smoke; source-reported request metrics are not fully reproducible from public records. All request counts and cache rates below are source-reported, not reproducible from public data.

## Scope and reported result

The source describes one EU smoke on an R74-style ladder cell using Kogen commit [`3644d35d7b83f171cf4461f931885daccad1014a`](https://github.com/KogenAI/kogen-ex/commit/3644d35d7b83f171cf4461f931885daccad1014a). It reports 20 develop requests, 18 with usage records, a weighted cache-hit rate of 67.0%, and a 0% minimum from turn 3 onward. The required gate was at least 95%; this smoke did not pass it. It does not show whether the code change improves Build success, cost or time.

## Cell accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 |

The smoke is cache telemetry, not a scored Build cell. Its request and usage counts are separate from these cell counts.

## Reproduction record

| Field | Record |
|---|---|
| Harness commit | Exact harness commit is not supplied in the public input. |
| Kogen commit | `3644d35d7b83f171cf4461f931885daccad1014a` (source-reported short SHA resolved to the public commit linked above). |
| Model and effort | Sol medium is reported for the T98 diagnostic lane; request-level model/effort rows are not supplied. |
| Task IDs | One R74-style ladder cell is described; its exact task and cell IDs are not supplied. |
| Command | The exact smoke command is not recovered from the supplied public input. |
| Raw records | The source inventory names `RESULT.md` and `PLAN.json`. Raw per-request usage records are not included in this public data tree. |

Until the request records, cell ID and exact command are published, all figures remain source-reported, not reproducible from public data. The cache gate remains unverified after this smoke.
