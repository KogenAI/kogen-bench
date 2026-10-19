# Claude roles: a Sonnet reviewer approved wrong code twice; Haiku and all-Sonnet settings were correct on all seven tasks (one attempt each)

Exploratory screen in Kogen Lab, reported descriptively: one attempt per task, seven tasks, five settings. Earlier Lab rounds used OpenAI models in every role. This run put Anthropic's Claude models into single roles and into every role, against the OpenAI settings on the same tasks.

- Baseline: GPT-6 Luna at low effort as planner and builder, GPT-6.1 Sol at low effort as reviewer. Correct in 6 of 7; one attempt ended at the six-repair stop.
- Claude Sonnet 5.5 at medium effort as reviewer, the rest as the baseline: correct in 5 of 7 and **wrong in 2 of 7**. It approved two submissions that each fail one hidden test. No other setting in this run, and no OpenAI reviewer in this or the [repair cost round](../repair-cost-1/README.md), approved wrong code.
- Claude Haiku 5.5 at medium effort as builder, the rest as the baseline: correct in 7 of 7, four of them with no repair; about $0.15 of Anthropic usage at list price for all seven attempts (all prompts were under the 100K-token price threshold).
- GPT-6 Luna at medium effort as builder, the rest as the baseline: correct in 6 of 7; one attempt ended at the six-repair stop.
- Claude Sonnet 5.5 at medium effort as planner, builder and reviewer: correct in 7 of 7, four of them with no repair; about $1.81 of Anthropic usage at list price.

With one attempt per task, none of this is a result. The two settings that solved every task are candidates for a confirmation run on harder tasks. The reviewer that approved wrong code is a risk to check before a Claude reviewer is used anywhere: a reviewer that lets wrong code through is the failure that matters most in this loop.

## Question and scope

Three questions were fixed before the run. (a) Does Claude Sonnet 5.5 as reviewer match the OpenAI reviewer at low effort (here) and at high effort (the baseline setting of the [repair cost round](../repair-cost-1/README.md), which used the same builder, tasks and caps)? (b) Does Claude Haiku 5.5 as builder match GPT-6 Luna at low and at medium effort? (c) How does an all-Claude setting compare with the OpenAI settings on correctness, tokens and cost? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine; its equivalence to Kogen is not measured.

- Tasks: `env-go`, `env-ex` and `sched-go` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), whose public parts are in that round's [`tasks/`](../confirm-builder-effort-1/tasks/). Also `r70-5-go`, `r70-7-go`, `r70-5-elixir` and `r70-7-elixir`, as in [the second mechanism screen](../screen-kogen-2/README.md).
- Shared configuration: review after every passing verification; supplied specifications, so no shaper calls. Claude roles ran at medium effort throughout. The five settings differ only in the roles listed above.
- One attempt per task and setting; each task's five attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, so the review-limit counterfactuals of the [review round limit rounds](../review-bound-2/README.md) were also computed for this run, without model calls.
- A Claude setting "matches" its OpenAI comparison, by the reading fixed before the run, when it is correct within one attempt and has no more wrong submissions; tokens and dollars are then compared.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's prompt tokens across all models (for Claude, cached prompt tokens included). "Stopped" means the attempt ended at the six-repair stop without an approved submission; "wrong" means the review approved code that then failed a hidden test.

| Task | Baseline | Sonnet reviewer | Haiku builder | Luna medium builder | All Sonnet |
| --- | --- | --- | --- | --- | --- |
| `env-go` | correct (2), c c a, 0.38M | correct (2), c c a, 0.26M | correct (2), c c a, 0.83M | correct (2), c c a, 0.35M | correct (1), c a, 0.13M |
| `env-ex` | stopped (6), c, 1.73M | **wrong** (4), c c c a, 25 of 26, 0.92M | correct (2), c c a, 0.79M | correct (2), c c a, 0.45M | correct (1), c a, 0.18M |
| `sched-go` | correct (5), c c c a, 0.56M | correct (4), c c c a, 0.38M | correct (0), a, 0.23M | correct (1), c a, 0.22M | correct (0), a, 0.10M |
| `r70-5-go` | correct (3), c c c a, 0.41M | correct (2), c c a, 0.24M | correct (0), a, 0.22M | correct (2), c c a, 0.45M | correct (0), a, 0.07M |
| `r70-7-go` | correct (3), c c c a, 0.45M | correct (2), c c a, 0.18M | correct (0), a, 0.44M | correct (1), c a, 0.21M | correct (1), c a, 0.15M |
| `r70-5-elixir` | correct (5), c c a, 0.99M | **wrong** (1), c a, 23 of 24, 0.20M | correct (1), c a, 0.64M | stopped (6), c c c c, 0.90M | correct (0), a, 0.13M |
| `r70-7-elixir` | correct (2), c a, 0.37M | correct (1), c a, 0.19M | correct (0), a, 0.22M | correct (4), c c c a, 0.46M | correct (0), a, 0.07M |
| Total | 6 of 7 | 5 of 7, 2 wrong | 7 of 7 | 6 of 7 | 7 of 7 |

| Setting | Correct | Wrong | Stopped | Repairs, median | Reviews, median | GPT-6 Luna prompt | GPT-6.1 Sol prompt | Claude prompt (cached) | Output, all models | Anthropic usage at list price | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 6 of 7 | 0 | 1 | 3 | 3 | 4.05M | 0.83M | none | 86k | none | 2.38h |
| Sonnet reviewer | 5 of 7 | 2 | 0 | 2 | 3 | 1.80M | none | 0.56M (0.05M) | 65k | $1.51 | 1.24h |
| Haiku builder | 7 of 7 | 0 | 0 | 0 | 1 | 0.03M | 0.68M | 2.65M (2.39M) | 189k | $0.15 | 0.65h |
| Luna medium builder | 6 of 7 | 0 | 1 | 2 | 3 | 2.24M | 0.79M | none | 56k | none | 2.00h |
| All Sonnet | 7 of 7 | 0 | 0 | 0 | 1 | none | none | 0.82M (0.37M) | 64k | $1.81 | 0.38h |

- Against the high-effort OpenAI reviewer of the repair cost round (same builder, tasks and caps: 5 of 7 correct, 0 wrong, 2 stopped, median 3 repairs), the Sonnet reviewer was correct as often but approved wrong code twice, so it does not match either OpenAI reviewer by the reading fixed before the run. In both wrong attempts the code had passed the attempt's own checks and the supplied acceptance scenarios before the review approved it; the hidden tests then found one failure in each.
- The Haiku builder matches both Luna builders on correctness and wrong submissions; its prompt tokens are mostly cache reads (2.39M of 2.65M), which Anthropic prices far below fresh input, and its output (184,000 tokens) is the largest of any setting. The all-Sonnet setting matches every OpenAI setting on correctness, with the fewest requests (49).
- Both stopped attempts left code that fails some hidden tests (20 of 26 on `env-ex` for the baseline; 10 of 24 on `r70-5-elixir` for the Luna medium builder).
- OpenAI usage ran through a subscription and has no dollar figure here; Anthropic usage ran through the API and is priced at the list prices current at the time (Sonnet 5.5: $2 per million input tokens, $10 output, $0.20 cache read; Haiku 5.5: $0.10, $0.50, $0.01; cache writes at 1.25 times input). These are estimates from the recorded usage, not invoices; all Haiku prompts were under the 100K-token price threshold, so the lower Haiku prices apply throughout.
- The run recorded 35 attempts, all with Lab outcomes, and used about 10.42M OpenAI input tokens (budget 20M) and $3.47 of Anthropic usage at list price (budget $120), with no billing, credit, usage-limit or invalid-request responses. Totals are summed from unrounded values. Wall time is the sum of the attempts' durations.

### Review limits, graded afterwards

Kogen has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As in the [review round limit rounds](../review-bound-2/README.md), Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. "Same" means the limit does not change the outcome; test counts are hidden tests passed, and prompt tokens are counted up to the submission. When a repair changed nothing and the same code was reviewed twice, the two reviews count once here. The 18 attempts not listed are unchanged by every limit; among them are all seven all-Sonnet attempts, none of which needed more than two reviews.

| Task, setting | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `env-ex`, Haiku builder | c c a | correct, 26 of 26; 0.79M | correct, 26 of 26; 0.57M | same | same |
| `env-ex`, Luna medium builder | c c a | correct, 26 of 26; 0.45M | **wrong**, 24 of 26; 0.22M | same | same |
| `env-ex`, Sonnet reviewer | c c c a | wrong, 25 of 26; 0.92M | **wrong**, 22 of 26; 0.65M | **wrong**, 23 of 26; 0.75M | same |
| `env-go`, Haiku builder | c c a | correct, 26 of 26; 0.83M | correct, 26 of 26; 0.61M | same | same |
| `env-go`, Luna medium builder | c c a | correct, 26 of 26; 0.35M | correct, 26 of 26; 0.24M | same | same |
| `env-go`, baseline | c c a | correct, 26 of 26; 0.37M | **wrong**, 25 of 26; 0.16M | same | same |
| `env-go`, Sonnet reviewer | c c a | correct, 26 of 26; 0.26M | correct, 26 of 26; 0.13M | same | same |
| `r70-5-elixir`, Luna medium builder | c c c | stopped, 10 of 24; 0.90M | **wrong**, 23 of 24; 0.21M | correct, 24 of 24; 0.39M | correct, 24 of 24; 0.48M |
| `r70-5-elixir`, baseline | c c a | correct, 24 of 24; 0.99M | **wrong**, 23 of 24; 0.76M | same | same |
| `r70-5-go`, Luna medium builder | c c a | correct, 24 of 24; 0.45M | **wrong**, 23 of 24; 0.25M | same | same |
| `r70-5-go`, baseline | c c c a | correct, 24 of 24; 0.41M | **wrong**, 23 of 24; 0.16M | correct, 24 of 24; 0.25M | same |
| `r70-5-go`, Sonnet reviewer | c c a | correct, 24 of 24; 0.24M | correct, 24 of 24; 0.15M | same | same |
| `r70-7-elixir`, Luna medium builder | c c c a | correct, 24 of 24; 0.45M | correct, 24 of 24; 0.19M | correct, 24 of 24; 0.30M | same |
| `r70-7-go`, baseline | c c c a | correct, 24 of 24; 0.45M | correct, 24 of 24; 0.16M | correct, 24 of 24; 0.31M | same |
| `r70-7-go`, Sonnet reviewer | c c a | correct, 24 of 24; 0.17M | correct, 24 of 24; 0.10M | same | same |
| `sched-go`, baseline | c c c a | correct, 24 of 24; 0.55M | correct, 24 of 24; 0.32M | correct, 24 of 24; 0.41M | same |
| `sched-go`, Sonnet reviewer | c c c a | correct, 24 of 24; 0.38M | correct, 24 of 24; 0.22M | correct, 24 of 24; 0.28M | same |
| Changed by the limit | | | 17, of which 7 wrong | 7, of which 1 wrong | 1, correct |

- A one-round limit would have let wrong code through in 7 of the 17 attempts it changes, in line with the earlier rounds (8 of 15 changed attempts, with the low-effort OpenAI reviewer). The only two-round failure is the Sonnet reviewer's `env-ex` attempt, whose code was wrong at every review and when approved.
- In the Luna medium builder's stopped `r70-5-elixir` attempt, the code at the third review passed every hidden test; the review asked for further changes, the repair changed nothing, and the next repairs broke the code until the repair limit. A limit of two or three rounds would have submitted the correct code.
- The Haiku builder's two changed attempts would have been correct under a one-round limit. Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

## Limits

- Seven tasks, one attempt each per setting: a screen. Matches are candidates for confirmation, not results; the two wrong approvals are two attempts, and a confirmation run would be needed to estimate how often a Sonnet reviewer approves wrong code.
- Claude roles ran at medium effort only; other efforts, and Sonnet as builder with an OpenAI reviewer, were not tested.
- Tokens are not summed across models and prices differ by provider and model, so no single cost figure is given; the Anthropic dollars are list-price estimates.
- The high-effort OpenAI reviewer comparison reuses another round's attempts rather than paired attempts in this run.
- While this run was live, grading for another round with a different Lab version was attempted on the same hosts. Lab refused because the hosts were busy, but it installs its helper program on a host before that check, so this run's helper program may have been replaced mid-run. The records were checked afterwards: no evaluation shows every test failing (the sign of a broken helper), no attempt contains the errors a replacement would cause, and the wrong and stopped attempts fail between 1 and 14 of 24 to 26 hidden tests, which are ordinary failures. A disclosure, not an invalidation.
- Wall times are not comparable across settings: from about 13:30 UTC until the run ended at 14:02 UTC, unrelated test runs put extra processor and disk load on two of the three hosts. They used a separate work folder, so outcomes are unaffected, but the wall-time column describes this run only and supports no timing claim.
- The caps are experimental and not part of Kogen.
- Results describe Kogen Lab's reproduction of Kogen's loop; equivalence with Kogen itself is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: fd0cdcfb422f6edef5ec69146cdecdb3e3c1317a, as reproduced by Kogen Lab.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet. The attempts ran on Lab build `0c1adf01`, whose fingerprint is in the bundle's `frozen/manifest.json`; the report and this export were produced by build `312b574b`, the same build with a fix to the report's reading of Anthropic usage records, which is the version named in the records.
- Model and effort: planner and builder `gpt-6-luna` at `low` or `medium`, or `claude-sonnet-5-5` and `claude-haiku-5-5` at `medium`; reviewer `gpt-6.1-sol` at `low` or `claude-sonnet-5-5` at `medium`, as stated per setting.
- Task IDs: `env-go`, `env-ex`, `sched-go`, `r70-5-go`, `r70-7-go`, `r70-5-elixir`, `r70-7-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab export in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on seven tasks, one attempt per setting, with one comparison reused from another round; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build. The plan named six host slots; by an amendment written just after the start, which changed capacity only, the run used three (two work folders on one Ubuntu 24.04 server, one Ubuntu 24.04 laptop), so that the workstation's slots stayed free for other work. The kept code was graded on the hosts that ran each attempt.
- The run's spending guard did not write its closing line when the run ended normally (its check mistook an unrelated waiting process for the run), so that line was added by hand afterwards. The attempt records are untouched.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (35). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (35 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (35 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (35 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (35 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (35 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (35 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (35 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (35 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (35 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (35 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (35 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (35 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (35 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (35 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (35 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (21 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (35 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (35 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (35 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (35 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (35 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (35 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (35 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (35 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (35 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (28 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (35 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (35 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (35 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (35 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (35 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (35 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (35 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (35 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (35 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (35 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (35 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (35 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (35 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (35 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (35 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (35 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (35 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (35 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (35 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (35 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (35 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tokens.phases.develop.cached_input` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.cached_input` (7 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.input` (7 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.output` (7 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.reasoning` (7 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (14 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (21 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (21 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (21 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (21 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (35 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (35 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (35 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (35 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
