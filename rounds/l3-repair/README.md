# L3 actionable self-verification repair

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of REGISTERED_THRESHOLD_NOT_MET. See the round evidence and limitations below.
Recomputation status: FULLY RECOMPUTABLE


## Required reproduction metadata

- Kogen commit: not applicable; the scored arm is direct Codex. The public task bases are Kogen-ex commits listed below.
- Harness commit: no harness Git commit is recorded. The runner tree fingerprint on both workers is `7e7a8d406e99436bce20de4f1f1347e9dfa91e73b9b89759e8887cd073faf6d4`; contestant wrapper SHA-256 is `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`.
- Model and effort: direct Codex `gpt-6-luna` at `max`; Codex CLI `0.160.0`.
- Runner: Python `3.14.7`; 3,600-second cap; zero retries.
- Task IDs: `r70-2-elixir-l3r31`, `r70-2-elixir-l3r33`, `r70-2-go-l3r32`, `r70-5-go-l3r1`, `r70-5-go-l3r32`, and `r70-7-rust-l3r31`.
- Host assignment: EU for Elixir and Rust; US for Go.
- Variant base provenance: the operator created and signed each variant commit from its registered public base plus the delivered failed patch. Exact parent and variant base SHAs are linked below.

STATUS: **DESCRIPTIVE** — six graded repairs; the registered decision is not fully supported.

Pre-registered: **operator-reported** before the first scored cell; the public bundle does not independently establish the exact commitment time.
Label: DESCRIPTIVE — raw captures not retained; results verified against official grades
Question: When direct Codex `gpt-6-luna` at max resumes a prior failed implementation with a fixed self-verification instruction, how often does it repair an official hidden-suite failure without losing checks passed by the prior implementation?
n: **6 matched failures**.
Headline: **2/6 repairs rescued; the ≥3/6 threshold was not met, so repair-with-verification remains budget-limited.**
Configuration: same direct Codex harness, runner, and sandbox; official grade route `r70-macbook-window-v1` (the MacBook-driven grade window that drains the host and runs the pinned grade worker). The fixed instruction asks Codex to check every prompt requirement against the code, write and run its own tests for each, and fix any gap. No hidden-test names or grader output were given to the model.
Limit: six selected failures across tasks 2, 5, and 7; one model; descriptive rescue rule. The comparator is the official pass rate among each original cell's other reps. Aggregate test counts do not establish per-test pass-set preservation; that registered condition is unverifiable from the public data.

## Why not VALID

- The registered decision required at least three rescues; only 2/6 occurred ([decision rule](DECISION-RULE.md#decision), [results](RESULTS.md#decision)).
- The registered per-test preservation condition is unmeasured: aggregate counts cannot show whether every previously passing test still passed.
- No round `ENVIRONMENT.md` records start and end host conditions. The six Standard records omit effective model and effort, grader, host class, sandbox, price, and cost fields; public reproducibility is incomplete.
- The rule first appears in public Git after the run. The operator-reported design time is a filesystem time, not immutable evidence that the rule preceded the first result.
Raw records: raw run captures are not retained. The public bundle includes [aggregate official-grade rows](data/cells.csv) and the [sanitized lane release-state summary](data/lane-release-state.json); the per-cell official grade receipt index and per-test result file are also absent, so do not infer either from aggregate counts.
Sources: [decision rule](DECISION-RULE.md); [results](RESULTS.md); [pre-registration inputs](INPUTS.json); [lane release state](data/lane-release-state.json); [aggregate cell data](data/cells.csv); [reproducer](reproduce/l3_repair.py); [H12 / F01 evidence summary](../../hypotheses/f01-shape-intent-plan.md); [status-only claim](../../results/claim-ledger.jsonl).

Evidence links: [H12 — checks, review, and actionable retries](../../hypotheses/f01-shape-intent-plan.md); [F01 findings summary](../../FINDINGS.md#f01-shape-intent-and-plan); claim `CL-L3-REPAIR-RESCUE-RATE` (**STATUS_ONLY**).

## Reproduce

### Public task base commits

- Task 2 Elixir: [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975)
- Task 2 Go: [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82)
- Task 5 Go: [e0b4a2478a17a924fcecb965b2941ca3396f49d6](https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6)
- Task 7 Rust: [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838)

### Operator-created variant base commits

- `r70-2-elixir-l3r31`: [5c5727999486d1c783a704121a182165422d443e](https://github.com/KogenAI/kogen-ex/commit/5c5727999486d1c783a704121a182165422d443e)
- `r70-2-elixir-l3r33`: [bcf8ab895355cfe822b08d187373dbc6faccb36c](https://github.com/KogenAI/kogen-ex/commit/bcf8ab895355cfe822b08d187373dbc6faccb36c)
- `r70-2-go-l3r32`: [a25ca44fcd42ac0f98b47de2361517171775480a](https://github.com/KogenAI/kogen-ex/commit/a25ca44fcd42ac0f98b47de2361517171775480a)
- `r70-5-go-l3r1`: [aade0efcbc2a6c592bf0c22ea84f82405c369d5b](https://github.com/KogenAI/kogen-ex/commit/aade0efcbc2a6c592bf0c22ea84f82405c369d5b)
- `r70-5-go-l3r32`: [54091c79f09540e6d773be15dcc54df6232a48d8](https://github.com/KogenAI/kogen-ex/commit/54091c79f09540e6d773be15dcc54df6232a48d8)
- `r70-7-rust-l3r31`: [ec773802393fe9d7cd19e493a5e749809470cb03](https://github.com/KogenAI/kogen-ex/commit/ec773802393fe9d7cd19e493a5e749809470cb03)

### Commands and data files

The worker dispatcher sequence was `python3 dispatch.py repair --batch first`, then `python3 dispatch.py repair --batch next-two`, then `python3 dispatch.py repair --batch final-three`, with the preregistered release gates between batches. Variant admission controls used the documented commands:

```sh
python3 grade_window_l3.py kogen-bench-eu --admission-controls --controls-only --fixed-variants r70-2-elixir-l3r31,r70-2-elixir-l3r33,r70-7-rust-l3r31
python3 grade_window_l3.py kogen-bench-us --admission-controls --controls-only --fixed-variants r70-2-go-l3r32,r70-5-go-l3r1,r70-5-go-l3r32
```

From the repository root, reproduce the public results and validate the page with:

```sh
python3 rounds/l3-repair/reproduce/l3_repair.py
python3 reproduce/validate_repo.py
```

The reproducer uses only the standard library and reads [rounds/l3-repair/data/cells.csv](data/cells.csv). The CSV records cell IDs, aggregate test counts, wall seconds, uncached/cached/output token counts, independent base pass rates, and operator variant SHAs. No hidden-test names or reference content are included. The frozen [pre-registration bundle](INPUTS.json) preserves the design-time inputs; the final grades and deployment SHAs are recorded in this page and the CSV.
