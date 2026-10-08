# Round 70 original RvE cohort

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of EVIDENCE, NO_PREREG_EVIDENCE, UNMATCHED_CONDITIONS. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



## Status

**INVALID**

- UNMATCHED_CONDITIONS — The README labels the study confounded.
- NO_PREREG_EVIDENCE — The round files do not establish a timestamped pre-registration predating the first result.
- EVIDENCE — The round is not documented as executed under one matched registered protocol.

STATUS: **INVALID**
Analysis: **DESCRIPTIVE**; this cohort does not establish a general language ranking.

This page records only the original 40-cell Rust, Elixir, Go, and TypeScript/Bun cohort on tasks 1, 3, 4, and 6. The fixed-front-end rerun, the later task 2/5/7 extension, task 8, and compile measurements are separate cohorts and are not pooled here. See [R70](../r70/README.md), the [fixed-skeleton rerun](../r70-rve-rerun/README.md), the [extension](../r70-rve-ext/README.md), [task 8](../r70-task8/README.md), and [compile measurements](../r70-compile/README.md).

## Question and observed outcomes

The measured outcome was the official hidden-suite full-pass result for a direct Codex build on each implementation stack. Own checks are a separate secondary endpoint. The exact 40 graded cell IDs and test counts are in the [test-count ledger](../../results/test-counts.jsonl), under cohort `r70-original-rve`.

| Task ID | Exact arm | Official full passes | Graded cells |
|---|---|---:|---:|
| r70-1-elixir | elixir | 0 | 3 |
| r70-1-go | go | 2 | 3 |
| r70-1-rust | rust | 3 | 3 |
| r70-1-ts-bun | ts-bun | 3 | 3 |
| r70-3-elixir | elixir | 1 | 2 |
| r70-3-go | go | 2 | 2 |
| r70-3-rust | rust | 2 | 2 |
| r70-3-ts-bun | ts-bun | 2 | 2 |
| r70-4-elixir | elixir | 0 | 3 |
| r70-4-go | go | 1 | 3 |
| r70-4-rust | rust | 1 | 3 |
| r70-4-ts-bun | ts-bun | 0 | 3 |
| r70-6-elixir | elixir | 1 | 2 |
| r70-6-go | go | 2 | 2 |
| r70-6-rust | rust | 2 | 2 |
| r70-6-ts-bun | ts-bun | 2 | 2 |

The outcomes remain descriptive. Tasks 1 and 4 have documented front-end or skeleton confounds; task 4 admission controls failed for three stacks in the separate rerun. The original as-graded outcomes are retained, and the rerun does not replace them. The task-6 output-order question is also unresolved. These limits prevent this cohort from supporting a causal stack ranking.

## Cohort accounting

| Count | n | Basis |
|---|---:|---|
| Planned scored cells | 40 | The selected cohort is 4 tasks × 4 stacks, with the planned repetitions represented in the export. |
| Identified scored starts | 40 | Forty unique scored cell IDs appear in the outcome ledger. |
| Officially graded | 40 | Forty latest official rows appear in the outcome ledger. |
| ITT denominator | Unresolved | Five additional ungraded deliveries are source-reported without joinable cell IDs; their disposition cannot be reconciled to the public cell identity ledger. |

The 40-row scored cohort is reproducible from the public export. The additional five deliveries and their exclusion from scored summaries are **source-reported, not reproducible from public data**. They do not receive invented outcomes or cell IDs. The [cost/time ledger](../../results/cost-time.jsonl) contains 20 original resource records for Rust and Elixir; it does not contain matching resource rows for Go or TypeScript/Bun. Cost estimates are not invoice totals.

## Reproduction record

- **Kogen commit:** not applicable; the tested implementation was built directly with Codex from task scaffolds, not with Kogen.
- **Harness commit:** no Codex harness Git commit is preserved in the public record. The 20 Rust/Elixir resource rows record Codex CLI `0.160.0` and harness fingerprint `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`; that fingerprint is not a Git commit and is not a per-cell receipt for the 20 Go/TypeScript/Bun rows.
- **Model and effort:** direct Codex, `gpt-6-luna`, `max`.
- **Task IDs:** `r70-1-{rust,elixir,go,ts-bun}`, `r70-3-{rust,elixir,go,ts-bun}`, `r70-4-{rust,elixir,go,ts-bun}`, and `r70-6-{rust,elixir,go,ts-bun}`. The concrete task IDs are listed in the table above.
- **Historical execution command:** not retained in the public record, so the model runs cannot be replayed exactly from this snapshot.
- **Reproduce the published outcome summary:** run `python3 rounds/r70-rve/reproduce.py` from the repository root. The script reads the public test-count and cost/time ledgers; it does not launch cells.
- **Raw records:** [test-count ledger](../../results/test-counts.jsonl), filtered by `cohort == "r70-original-rve"`; [cost/time ledger](../../results/cost-time.jsonl), filtered by the same cohort; own-check diagnostics are in [`r70-original-own-checks.jsonl`](../../reproduce/inputs/r70-original-own-checks.jsonl).

## Smallest useful follow-up

Run a separately registered parity-controlled cohort with identical task behavior at each stack boundary, exact per-cell harness pins, and joinable planned/start/grade IDs. Preserve the original and rerun cohorts as separate records.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r70-rve.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 51 rows (fail 18, pass 28, ungraded 5); overall pass rate is 60.9% (28/46) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 51 missing published metadata). Missing counters remain unknown, not zero.
This round also has 51 raw-only or non-public rows; they are kept separate from the published-export denominator.
