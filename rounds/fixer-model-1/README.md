# Fixer model: in one attempt per task, Sol medium kept the Sol high fixer's correctness at 70% of the input on the four tasks the baseline finished, and a Luna medium fixer was weaker; the run stopped at its input budget (19 of 24 attempts scored)

Exploratory screen in Kogen Lab, reported descriptively, **stopped at its predeclared input budget**: 24 attempts were planned (six tasks, four settings, one attempt each); 21 started; **19 were scored, 2 were interrupted by the budget stop and have no outcome, and 3 never started**. The run was not continued, so the sixth task, `env-ex`, has no usable comparison.

In Kogen's current version (commit b2c9876b), after verification the independent reviewer repairs concrete defects itself. Kogen Lab, set to that commit, does not have that step yet; this run used the closest mechanism Lab has, a separate fixer role that repairs in a fresh conversation (the setup of the [repair cost round](../repair-cost-1/README.md)). The question was how strong that repairing model has to be. A weak builder was used on purpose, GPT-6 Luna at low effort, because Kogen's default builder solves the easier tasks first time ([planner removal round](../planner-direct-1/README.md)); every setting had the same reviewer, GPT-6.1 Sol at high effort. The four settings differ only in the fixer: Sol at high, medium or low effort, or Luna at medium effort.

- On the four tasks where the baseline finished (`r70-4-go`, `r70-4-elixir`, `r70-6-elixir`, `r70-5-elixir`): the Sol high baseline was correct in 4 of 4, the Sol medium fixer in 4 of 4 with 70% of the baseline's input (1.96M against 2.79M) and a median of 2 repairs against 3, the Sol low fixer in 3 of 4 at 78% of the input, and the Luna medium fixer in 2 of 4 at 148% of the input.
- On the fifth task that all four settings started, `r70-1-go`, the baseline attempt was interrupted by the budget stop, so it has no outcome: the Sol low fixer was correct (5 repairs), and the Sol medium and Luna medium fixers ended at the six-repair stop.
- No attempt submitted code that failed the hidden tests. The five attempts that stopped at the repair cap or on a changed approved test file held code that passed every hidden test; the two interrupted attempts have no grade. "Correct" here counts attempts that ended with an approved submission.
- With one attempt per task and setting, these are candidates for the next screen, not results. The Luna medium fixer is the clearest difference: it ended with an approved submission in 2 of 5 scored attempts and used the most input.
- The review-limit counterfactuals were not graded for this run: the grading host's evaluation could not be trusted at publication time.

## Question and scope

With a weak builder and a high-effort reviewer, does a cheaper fixer keep the Sol high fixer's correctness at lower cost? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine; Lab's equivalence to Kogen was checked only against an earlier version of Kogen, and at b2c9876b it is not measured, so these results are Lab-only. The fixer role is Lab's stand-in for the reviewer-repairs step of Kogen b2c9876b; it does not measure it.

- Tasks: `r70-4-go`, `r70-4-elixir`, `r70-1-go`, `r70-6-elixir` and `r70-5-elixir` from this repository's [task catalogue](../../tasks/README.md), converted for Lab with the catalogue's public specification and hidden tests (18, 18, 24, 24 and 24 hidden tests), and `env-ex` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), where Luna-low builders failed in earlier rounds. They are development tasks, not held-out ones: the hidden suites are published here and have been used in earlier rounds.
- Shared configuration: GPT-6 Luna at low effort as builder, a direct build (no planner), supplied specifications (no shaper calls), GPT-6.1 Sol at high effort as reviewer after every passing verification, and every repair by the fixer in a fresh conversation, given the specification, the diff, the changed files, the check results and the review findings.
- Four settings, by fixer: GPT-6.1 Sol at high effort (the baseline), GPT-6.1 Sol at medium effort, GPT-6.1 Sol at low effort, and GPT-6 Luna at medium effort. The first three differ in effort only; the fourth changes the model.
- One attempt per task and setting, so 24 planned; each task's attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Budget: at most 16M input tokens, with a guard that interrupts the run when it is reached and stops dispatch.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens across all models. "Stopped" means the attempt ended at the six-repair stop without an approved submission.

| Task | Sol high fixer (baseline) | Sol medium fixer | Sol low fixer | Luna medium fixer |
| --- | --- | --- | --- | --- |
| `r70-1-go` | interrupted at the budget stop after 3 repairs, c c c, 0.88M (no outcome) | stopped (6), c c c c c c, 1.09M | correct (5), c c c c a, 0.94M | stopped (6), c c c c c c, 1.51M |
| `r70-4-go` | correct (4), c c c a, 0.61M | correct (5), c c c c a, 0.79M | correct (3), c c c a, 0.49M | ended by the fixer's change to approved test files (3), c c, 0.39M |
| `r70-4-elixir` | correct (6), c c c c c a, 1.14M | correct (2), c a, 0.32M | stopped (6), c c c c c c, 0.82M | stopped (6), c c c c c c, 1.34M |
| `r70-6-elixir` | correct (2), c a, 0.64M | correct (2), c a, 0.47M | correct (4), c c c a, 0.57M | correct (5), c c a, 1.55M |
| `r70-5-elixir` | correct (2), c c a, 0.39M | correct (2), c a, 0.37M | correct (1), a, 0.28M | correct (4), c c a, 0.85M |
| `env-ex` | not started | not started | approved at the third review, but interrupted before grading (3 repairs, c c a, 0.61M; no outcome) | not started |
| Scored total | 4 of 4; 2.79M input | 4 of 5; 3.05M input | 4 of 5; 3.11M input | 2 of 5; 5.63M input |

The first table lists every started attempt. The comparison below uses the four tasks where the baseline finished, so that every setting is compared with an outcome.

| Fixer | Correct | Stopped at the six-repair cap | Ended otherwise | Repairs, median | Reviews, median | Input | Input against baseline | Builder (Luna) input | Fixer input | Reviewer (Sol) input | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sol high fixer (baseline) | 4 of 4 | 0 | 0 | 3 | 3.5 | 2.79M | 100% | 0.17M | 1.61M | 1.00M | 0.76h |
| Sol medium fixer | 4 of 4 | 0 | 0 | 2 | 2 | 1.96M | 70% | 0.19M | 1.13M | 0.63M | 0.50h |
| Sol low fixer | 3 of 4 | 1 | 0 | 3.5 | 4 | 2.16M | 78% | 0.23M | 1.07M | 0.87M | 0.62h |
| Luna medium fixer | 2 of 4 | 1 | 1 | 4.5 | 3 | 4.13M | 148% | 0.21M | 3.05M | 0.87M | 0.85h |

- Stopped attempts: `r70-1-go` (Sol medium, Luna medium), `r70-4-elixir` (Sol low, Luna medium) at the cap, and `r70-4-go` (Luna medium) when its fixer changed the approved test files and Lab ended the attempt. All five held code that passed every hidden test; the two interrupted attempts have no grade.
- `r70-1-go` is not in the second table because the baseline attempt was interrupted after 3 repairs and 3 reviews that all asked for changes (0.88M of input). On that task the Sol low fixer was correct with 5 repairs (0.94M), the Sol medium fixer stopped at the cap (1.09M) and the Luna medium fixer stopped at the cap (1.51M).
- `env-ex`: only the Sol low attempt started, and it was approved at the third review but interrupted before grading, after 3 repairs (0.61M); the other three settings never started it.
- Input including the two interrupted attempts, per setting on all started cells: Sol high 3.67M, Sol medium 3.05M, Sol low 3.72M, Luna medium 5.63M.
- The Luna medium fixer's own input was 3.05M against 1.61M for the baseline's fixer on the same four tasks; the builder's and reviewer's input differ much less between settings.
- Input is summed from unrounded values across the builder, fixer and reviewer. Wall time is the sum of the attempts' durations.
- The run recorded 21 attempts, 19 with outcomes and 2 interrupted, and used about 16.07M input and 350,000 output tokens in all, against its 16M input budget: the guard's last reading, 16.04M, triggered the stop, and the recorded usage totals slightly more. No billing, credit, usage-limit or invalid-request responses were recorded.

### Review limits

Not graded: the grading host's evaluation could not be trusted at publication time. The [review round limit rounds](../review-bound-2/README.md) graded afterwards what a limit on review rounds would have submitted; that needs hidden-test grading on the local hosts, which was withdrawn for this run. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- Stopped at the budget: 5 of the 24 planned attempts have no outcome (2 interrupted, 3 never started), including the baseline's attempt on `r70-1-go` and the whole `env-ex` comparison. The comparison rests on four tasks where every setting has an outcome and on one more task without a baseline.
- One attempt per task and setting: a screen. A difference of one attempt (Sol medium 4 of 4 against Sol low 3 of 4) can be chance; the repair counts of single attempts vary from 1 to 6.
- The settings differ in effort (Sol high, medium, low) and, for the last one, in model, so the Luna medium result does not separate the effect of the model from that of the effort.
- The builder is weak on purpose and is not Kogen's default. Lab set to this commit repairs through a fixer role rather than by the reviewer, as Kogen b2c9876b does; whether these fixers behave the same when they are also the reviewer is not measured.
- All stopped attempts held passing code; "correct" counts approved submissions, so a setting whose reviewer loop does not end looks worse than the code it produces.
- The local sandbox settings were changed on 19 October, during a later round.
- The caps are experimental and not part of Kogen.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6-luna` at `low`; reviewer `gpt-6.1-sol` at `high`; fixer `gpt-6.1-sol` at `high`, `medium` or `low`, or `gpt-6-luna` at `medium`, as stated per setting.
- Task IDs: `r70-4-go`, `r70-4-elixir`, `r70-1-go`, `r70-6-elixir`, `r70-5-elixir`, `env-ex`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen stopped at its input budget with 19 of 24 attempts scored, one attempt per setting; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over three work folders on one macOS workstation, from about 14:55 to 16:36 UTC on 19 October 2026.
- The run was stopped by its budget guard at 16:36 UTC, which interrupted the attempts then running (SIGINT): the two interrupted attempts are in the records as incomplete, with no outcome. Three planned attempts never started. The run was not continued.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per started attempt (21). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (21 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (21 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (21 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (21 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (21 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (21 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (21 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (21 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (21 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (21 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (21 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (21 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (21 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (21 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (21 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (21 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (21 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (21 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (21 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (21 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (21 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (21 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (21 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (21 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (21 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (21 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (21 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (21 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (21 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (21 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (21 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (3 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (21 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (21 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (21 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (21 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (21 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (21 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
