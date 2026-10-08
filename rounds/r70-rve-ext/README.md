# r70-RvE language extension


## Status

**VALID** — registered reps 31–32 only; rep 33 is post-hoc and reported separately

### Limits
- Restored to VALID 2026-10-08: the round executed its registered rule as registered and its numbers recompute; the points below are limits on public evidence, not contradictions in the round's own files.
- PARTIAL_PREREG — Only reps 31–32 are stated as pre-registered; rep 33 is explicitly post-hoc.
- NO_PREREG_EVIDENCE — The files do not establish that the limited registration predates the first result.
- SCOPE — The reported cohort mixes registered and post-hoc cells.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs: r70-2-elixir, r70-2-go, r70-2-rust, r70-2-ts-bun, r70-5-elixir, r70-5-go, r70-5-rust, r70-5-ts-bun, r70-7-elixir, r70-7-go, r70-7-rust, r70-7-ts-bun; the complete scored-cell mapping is not recorded where noted above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **VALID** — registered decision covers the 24 pre-registered rep 31–32 cells; the 5 post-hoc rep-33 cells are reported separately and are outside the registered rule.

Data completeness (standard run-record capture): **N/A** (0 deliveries; NO DELIVERED DATA). Supplemental evidence: 29 official grades; 60 control receipts. [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).




Pre-registered: yes for reps 31–32; design date 6 October 2026.
Label: DESCRIPTIVE
Question: What hidden-suite full-pass outcomes did Rust, Elixir, Go, and TypeScript/Bun record on tasks 2, 5, and 7, alongside the prior Round 70 language observations?
n: 24 pre-registered cells at reps 31–32; 5 post-hoc rep-33 cells; 29 official grades total.
Headline: Reps 31–32 per stack: Rust 5/6, Elixir 4/6, Go 4/6, and TypeScript/Bun 6/6.
Evidence note: The public test-count and controls ledgers identify the rep-31 smokes, admission controls, and contestant-path X-controls. All smokes met Rule L; admission controls and X-controls had their expected outcomes.
Configuration: direct Codex, gpt-6-luna at max; n=2 per task and stack for pre-registered reps 31–32, with selected post-hoc rep-33 additions. Rust and Elixir ran on kogen-bench-eu; Go and TypeScript/Bun ran on kogen-bench-us. Wall comparisons are within-host only. Per-cell token and wall medians are reported separately for pre-registered reps 31–32 and post-hoc rep 33 in the results; the cost/time ledger provides per-cell token and wall fields.
Original cohort context: [40-cell as-graded RvE comparison](../r70/README.md#original-40-cell-rve-language-comparison).
Limit: Descriptive, small per-task samples, one model, and author-selected task templates. The extension observations do not establish differences among stacks.

Sources: [decision rule](DECISION-RULE.md); [results](RESULTS.md); [test-count ledger](../../results/test-counts.jsonl); [cost/time ledger](../../results/cost-time.jsonl); [controls ledger](../../results/controls.jsonl); [sanitized official grade rows](../../reproduce/inputs/grades.final.jsonl); [public cell export](../../results/cells.jsonl).
