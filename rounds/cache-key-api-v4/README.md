# H-API: STATUS VALID; primary finding NOT SUPPORTED

Round date: HISTORICAL (before 2026-10-09)
Publication badge: VALID; KEPT FOR AUDIT
Recomputation status: FULLY RECOMPUTABLE


STATUS: **VALID** — protocol completed as registered; primary finding NOT SUPPORTED.

This preregistered official Responses API route via subscription SIWC round reached its 11 transport-complete pairs in one execution. The frozen distinct-key ≥80% condition held in 1 of 11 complete pairs. K=1/11; exact one-sided p=0.9995117188; 99% Clopper–Pearson CI=[0.000456, 0.508565]. **VALID** describes protocol completion and counter integrity; it does not mean the directional hypothesis was supported.

The earlier cache-key-sharing (not in this repository) and cache-replay-v3 (not in this repository) are separate prior attempts. Their observations were not pooled into this round. See [DESIGN.md](DESIGN.md), [DECISION-RULE.md](DECISION-RULE.md), [RESULTS.md](RESULTS.md), [MEASURED.md](MEASURED.md), [ENVIRONMENT.md](ENVIRONMENT.md), and [sanitized.csv](sanitized.csv).

## What it shows

On this account, model, route, and date, provider-reported cache reuse varied across newly seeded pairs. The frozen hypothesis did not reproduce at its 10-of-11 threshold. The run sent 44 requests, spent 503,588 charged or reserved tokens, and replaced 0 transport-incomplete pairs.

## What it does not show

It does not locate physical cache entries, isolate `prompt_cache_key` from the linked session metadata, establish a future hit guarantee, measure billing savings or task quality, or explain the change from the prior attempts. The two endpoints use different OAuth grants and routing contexts.

## Lifecycle counts

Units are request pairs (one shared-key and one distinct-key probe arm per pair), not benchmark task cells.

| Lifecycle field | n | Basis |
|---|---:|---|
| Planned | 11 | Frozen target of transport-complete pairs. |
| Started | 11 | Attempted pairs (no transport-incomplete pair was replaced). |
| Finished | 11 | Transport-complete pairs. |
| Officially graded | 11 | Pairs evaluated by the frozen counter rule. |
| ITT denominator | 11 | All complete pairs enter the registered rule. |

## Required reproduction metadata

- Kogen commit: not applicable; this round sends direct provider requests and does not run Kogen.
- Harness commit: not recorded in the round files; the probe script is not bundled in this repository.
- Model and effort: gpt-6-luna as reported by every response; request settings are frozen in [DESIGN.md](DESIGN.md).
- Task IDs: not applicable; the fixed primer/probe fixture is identified by its manifest hash in [DESIGN.md](DESIGN.md).
- Historical execution command: not recorded in the round files.
- Raw records: raw plans, receipts and credentials are not retained in this repository; per-pair counters are in [sanitized.csv](sanitized.csv).
