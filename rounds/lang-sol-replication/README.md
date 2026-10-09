# Sol-medium language replication

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of DECISION_RULE_UNDEFINED, CONDITIONS_MISMATCH. See the round evidence and limitations below.
Recomputation status: FULLY RECOMPUTABLE


## Required reproduction metadata

- Kogen commit: not applicable as a single round-level value; exact per-task SHAs are linked in the table below.
- Harness commit: not recorded as a separate Git commit in the cited rows. Harness and CLI: direct Codex; CLI version recorded on every scoped cell is codex-cli 0.160.0. No official harness version label is recorded.
- Model and effort: gpt-6.1-sol, MEDIUM.
- Task IDs: r70-1-rust, r70-1-go, r70-1-ts-bun; r70-2-rust, r70-2-go, r70-2-ts-bun; r70-4-rust-fe2, r70-4-go-fe2, r70-4-ts-bun-fe2; reused r70-5, r70-6, and r70-7 variants for Rust, Go, and TS-Bun.
- Historical execution command: not recorded in the cited design and official grade sources. The exact commands for reproducing this page are below.
- Raw records: raw run captures are not retained; data/cells.csv preserves the exact cell IDs, official grades, token counts, wall times, grade-window times, Kogen base SHAs, and CLI version used here. DESIGN.md is a sanitized design presentation with operator-reported original source SHA-256 provenance.

STATUS: **DESCRIPTIVE** — raw rates are reported; the combined registered decision is UNRESOLVED.

Pre-registered: operator-reported at 10:01:53Z before the first grade window; the public bundle does not independently establish that timing. The round was added to this repository after the first grade window.

Label: DESCRIPTIVE — raw captures not retained; results verified against official grades

Question: Is the Round 70 language result specific to Luna max?

n: 27 new cells; 31 reused Sol-medium cells on t5–t7; 58 exact cell IDs in the comparison. The frozen design says 36 existing cells; the exact latest official IDs for the three named stacks yield 31 reusable rows (Rust 11, Go 11, TS-Bun 9). Results use all 31, with no reruns.

| Population | N |
| --- | ---: |
| Planned new cells | 27 |
| Started new cells | 27 |
| Finished new cells | 27 |
| Officially graded new cells | 27 |
| ITT denominator for new cells | 27 |

Headline: New passes were Rust 8/9, Go 7/9, and TS-Bun 6/9. Combined raw passes were Rust 18/20, Go 18/20, and TS-Bun 15/18. A post-hoc equal-task mean is Rust 90.3%, Go 88.9%, and TS-Bun 83.3%; the registered combined branch has no formula or scale for its four-pass threshold. The new-cell threshold was not triggered; the combined decision is **UNRESOLVED**.

## Why not VALID

- The registered combined four-pass branch lacks a formula and scale, so the full decision cannot be executed. The equal-task rates are post-hoc sensitivity values, not a substitute rule.
- The available operator design bytes hash to `66f5d590…`, while the published source hash is `c9394487…`. The available design's filesystem time follows the first new official grade, and the public rule was committed later. This does not prove a post-hoc edit, but independent pre-registration timing is unproven.
- New Rust cells ran on EU, while Go and TS-Bun ran on US; stack and host cannot be separated in this comparison.
- The 31 reused cells come from a different date window with unequal replication, including one INVALID Rust cell retained as a non-pass. The reused and new cohorts cannot support a single matched language effect.
- No round `ENVIRONMENT.md` records start and end host conditions. New Standard rows omit effective model and effort, grader, host class, sandbox, and price; public reproducibility is incomplete.

Configuration: direct Codex, gpt-6.1-sol at MEDIUM, 3600-second cap, zero retries. New tasks were t1, t2, and t4-fe2 on fixed skeletons, crossed with Rust, Go, and TS-Bun at three reps each. Rep 1 was the rule-L smoke for each task-by-stack pair; reps 2–3 followed the host smoke gates. Reused t5–t7 cells were not rerun. New Rust cells ran on kogen-bench-eu; new Go and TS-Bun cells ran on kogen-bench-us. Wall times are comparable only within a host.

Release-gate evidence: all nine rep-1 cells received official grades through the sandbox before the bulk reps; both host smoke-gate receipts report passed=true. The TS-Bun t4-fe2 rep-1 cell scored 17/18 and remains a scored fail. The lane receipts say the pre-run gate accepted an emitter-gap exception and deferred full Standard-record validation until analysis; the referenced exception receipt is not in the public bundle. The exact design-freeze timing is operator-reported, not independently established.

Limit: small n, one model per arm, and a decision rule designed to detect only large reversals. The reused t5–t7 cohort has varying rep counts; the INVALID Rust t6 rep 3 row is retained as a non-pass in the denominator.

Sources: sanitized [DESIGN.md](DESIGN.md), preserving the operator-reported original source SHA-256 `c9394487c2a139ff57e98fe8c9d5c44d6f6b5e7b33d1a33abba87479fb575892`; [public smoke-gate receipt extracts](data/smoke-gates.json); the cited cohort, host-assignment, and grade-window ledgers; and the sanitized per-cell rows in data/cells.csv. The original source bytes and strict-exception receipt are not included.

## Decision and results

- [Decision rule](DECISION-RULE.md)
- [Cell-level results and summaries](RESULTS.md)
- [Frozen design copy](DESIGN.md)
- [Public cell data](data/cells.csv)

## Reproduction

Run from the kogen-bench-sot repository root:

    python3 rounds/lang-sol-replication/reproduce/lang_sol_replication.py
    python3 reproduce/validate_repo.py

The round reproducer uses only Python's standard library. It validates the frozen design hash and exact cell set, recomputes every cell total, per-stack pass count, median, and verdict from data/cells.csv, and fails if RESULTS.md or the data-derived README claims differ.

Evidence links: [H91 — matched language comparison](../../hypotheses/f08-language-spec.md); [H114 — R70 language choice](../../hypotheses/f11-claim-reconciliation.md); [F08 findings summary](../../FINDINGS.md#f08-language-and-executable-spec); claim `CL-SOL-LANG-REPLICATION-POSTHOC-EQUAL-TASK` (**STATUS_ONLY**). The equal-task formula is a post-hoc sensitivity analysis because the original formula was not recorded.

## Kogen task commits

| Task ID | Kogen commit |
| --- | --- |
| r70-1-rust | [76b4f1fdc3bfb10f6a145de9c912fb0056239c16](https://github.com/KogenAI/kogen-ex/commit/76b4f1fdc3bfb10f6a145de9c912fb0056239c16) |
| r70-1-go | [ff3bbaed352843fbe44666650a30f49bbe64e0d5](https://github.com/KogenAI/kogen-ex/commit/ff3bbaed352843fbe44666650a30f49bbe64e0d5) |
| r70-1-ts-bun | [ceba0e8e071c6ae64b9d679d6196661e5454b968](https://github.com/KogenAI/kogen-ex/commit/ceba0e8e071c6ae64b9d679d6196661e5454b968) |
| r70-2-rust | [3bc3eac673cc5f4e81d1dd6b359998464eb9050d](https://github.com/KogenAI/kogen-ex/commit/3bc3eac673cc5f4e81d1dd6b359998464eb9050d) |
| r70-2-go | [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) |
| r70-2-ts-bun | [d834cb057114495d15905ae524c9157bc8f305d1](https://github.com/KogenAI/kogen-ex/commit/d834cb057114495d15905ae524c9157bc8f305d1) |
| r70-4-rust-fe2 | [7ec844419f66eb7508ee5da89ed2e6aca5768985](https://github.com/KogenAI/kogen-ex/commit/7ec844419f66eb7508ee5da89ed2e6aca5768985) |
| r70-4-go-fe2 | [21d21a2f420a387c921f998e5b4d16efc8f80904](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) |
| r70-4-ts-bun-fe2 | [cc3a831a167020538c4ca2ad90185606a2e4ad6a](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) |
| r70-5-rust | [8981c5fcfeecbd5851e01cca3531a8d96afa9376](https://github.com/KogenAI/kogen-ex/commit/8981c5fcfeecbd5851e01cca3531a8d96afa9376) |
| r70-5-go | [e0b4a2478a17a924fcecb965b2941ca3396f49d6](https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6) |
| r70-5-ts-bun | [c58bd4dd91b099cb8ce01f8adf1e4089efd00448](https://github.com/KogenAI/kogen-ex/commit/c58bd4dd91b099cb8ce01f8adf1e4089efd00448) |
| r70-6-rust | [2e15e5332f42c34957417a8ca69d747fb01bf488](https://github.com/KogenAI/kogen-ex/commit/2e15e5332f42c34957417a8ca69d747fb01bf488) |
| r70-6-go | [1eeb5b1b77c97102131fd97ec3f8ff85844b2534](https://github.com/KogenAI/kogen-ex/commit/1eeb5b1b77c97102131fd97ec3f8ff85844b2534) |
| r70-6-ts-bun | [41192b331e0bc75a19a4abc2f8213bb4571acc04](https://github.com/KogenAI/kogen-ex/commit/41192b331e0bc75a19a4abc2f8213bb4571acc04) |
| r70-7-rust | [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) |
| r70-7-go | [dfbf7e2eed40f53f0f694994f08ad50b48ee7de3](https://github.com/KogenAI/kogen-ex/commit/dfbf7e2eed40f53f0f694994f08ad50b48ee7de3) |
| r70-7-ts-bun | [01c5f1f43377834b800315964c5476aff341b26e](https://github.com/KogenAI/kogen-ex/commit/01c5f1f43377834b800315964c5476aff341b26e) |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/lang-sol-replication.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 18 rows (fail 5, pass 13); overall pass rate is 72.2% (13/18) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 18 missing published metadata). Missing counters remain unknown, not zero.
This round also has 18 raw-only or non-public rows; they are kept separate from the published-export denominator.
