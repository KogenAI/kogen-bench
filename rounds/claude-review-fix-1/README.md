# Review and fix, exploratory (two repetitions per task): with prose specifications the Sonnet reviewer fixed 2 of 4 wrong builds and the Haiku reviewer fixed none; run 1 was inconclusive

Exploratory screen in Kogen Lab, reported descriptively: two runs of the same question, each with two repetitions per task and two reviewer settings, 36 attempts in all, all scored. Every model that ran was one of Anthropic's: a deliberately weak builder (Haiku 5.5 at low effort) writes the code, then Kogen's review-and-fix reviewer reads it and edits it itself. The question is the one left open by the [review and fix round](../review-fix-1/README.md), where every builder that reached review had already solved the task: **when the builder's code is green on its own checks but wrong on the hidden tests, does the reviewer catch and fix it, and does the reviewer's strength matter?** The two reviewer settings are Sonnet 5.5 and Haiku 5.5, both at medium effort. In Kogen's review-and-fix flow, once the builder's checks are green a second model reviews the code and fixes any defects it finds by editing the files itself. If it changed anything, the checks run again. If it returns a "changes" verdict instead of approving, the attempt ends.

Lab runs the checks in the folder where the builder worked, not on a clean copy of the candidate (clean-candidate verification is not implemented), so these runs are labelled **approximate** against Kogen at commit b45ba32b.

- **Run 1, supplied Gherkin scenarios (16 attempts), is inconclusive for the rescue question.** All 16 attempts were correct, and the builder's code was already correct before review in all 16: the Sonnet reviewer approved 8 of 8 unchanged, and the Haiku reviewer approved 5 unchanged and edited 3, each already correct. No wrong code reached a reviewer, so there were 0 rescues and 0 misses.
- **Run 2, prose specifications with no scenarios (20 attempts), did produce wrong code at review.** 15 of 20 attempts were correct, 4 submitted wrong code and 1 was ended by a blocking review. Every attempt reached review, and in 6 of the 20 the code, graded on the hidden tests before the review, was already wrong.
- **The key table** classifies each reviewed attempt in run 2 from its last green code before the review. "Fixed" and "rescued" mean the same: the code was wrong before review and correct after the reviewer's edit. "Polish" means the reviewer edited code that was already correct.

| Reviewer | Attempts | Code graded wrong before review | **Rescued** (edited, then correct) | **Approved wrong code unchanged** | **Edited but still wrong** | Blocked (code before review not graded) | Polish (edited, already correct) | Approved correct code unchanged |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet reviewer | 10 | 4 | 2 | 2 | 0 | 0 | 0 | 6 |
| Haiku reviewer | 10 | 2 | 0 | 0 | 2 | 1 | 2 | 5 |

- **The Sonnet reviewer rescued 2 and missed 2.** Of the 4 attempts whose code was wrong before review, it edited 2 into correct code (both `r70-1-go`) and approved the other 2 unchanged (`r70-4-elixir-2` and `r70-6-elixir-2`, first repetition each), which then failed 1 hidden test each.
- **The Haiku reviewer rescued none.** It edited 2 wrong builds and both stayed wrong (one improved from 11 to 24 of 25 checks, the other stayed at 17 of 18), and in a third attempt it edited the code and then blocked it, so that attempt submitted nothing; that attempt's code before review was not graded. It approved no wrong code unchanged.
- Each attempt is its own builder run, so the two reviewers did not see the same code: Sonnet saw 4 wrong builds, Haiku 2 graded wrong and 1 blocked. Two repetitions per task make this a screen. The counts are small; they are candidates, not results.
- Usage at list price was about $0.70 for run 1 and about $0.83 for run 2 (sums of unrounded per-request estimates). A replication is planned.

## Question and scope

Does the reviewer in Kogen's current review-and-fix flow catch and fix code that is green on the builder's checks but wrong on the hidden tests, and does a stronger reviewer catch more? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b45ba32b is not measured, so any result is Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (the same tasks with one added `.gitignore` entry; see the [builder helpers round](../builder-subagents-1/README.md)), in both runs. They are development tasks with 18, 24 (plus one regression check), 18 and 24 hidden tests; the hidden suites of these four tasks are published here and have been used in earlier rounds. Run 2 added `artifact-go`, a word-frequency command-line tool written for this question; its public parts (request, task settings, starting project and prose specification) are in [`tasks/artifact-go/`](tasks/artifact-go/), and its 29 hidden tests, reference solution and wrong variants stay private (only the four earlier tasks' hidden suites are published). Its starting Makefile does not create the `build/app` program that the launcher runs, so a candidate has to change the Makefile. A candidate that only builds the program by hand leaves it in an ignored folder: it works in the builder's own folder but fails the hidden tests, which run the declared build step on the candidate's files first. The task qualified on all four work folders (qualification records are not published): the starting code fails every requested test, the reference solution is correct, each wrong variant fails at least one test, and repeated runs give identical results.
- Shared configuration: Kogen b45ba32b's review-and-fix flow as read by Lab, with no planner, a supplied specification (no shaper calls), the builder's verification stopping at the first failing check, and a reviewer that can edit files. The builder was Haiku 5.5 at low effort, an Anthropic model, in every attempt.
- Run 1 supplied the specification with Gherkin scenarios, which Lab executes as part of the builder's checks (acceptance, build, tests, format, and vet for Go). Run 2 supplied the same request as prose only, with no scenarios, so the builder's own checks were the build, the tests, the format check, and vet for Go.
- Two settings in each run: the Sonnet reviewer (Sonnet 5.5 at medium effort, the baseline) and the Haiku reviewer (Haiku 5.5 at medium effort); `rev-sonnet` and `rev-haiku` in the records.
- Two repetitions per task and setting, one attempt each: run 1 has 4 tasks, 16 attempts; run 2 has 5 tasks, 20 attempts. Each attempt has its own builder run. Attempts were spread over four work folders: one on a macOS workstation, two on one Linux server and one on a Linux laptop.
- Every attempt carried experimental stops that are not part of Kogen: at most six builder repairs, 900 seconds per command and 3,600 seconds of wall time. No attempt ended at one of them.
- The hidden tests grade each attempt independently of the workflow's own checks and review. "Checks" below means the hidden tests plus, for `r70-1-go`, one regression check that the starting code already satisfies.
- The code before review is the last green verification before the reviewer's first edit. Where the reviewer edited the code, Lab's snapshot grading ran the hidden tests on that earlier code afterwards, without model calls (see below). Where the reviewer approved unchanged, the code before review is the submitted code and its final evaluation is its grade.

## Results

Each cell gives the outcome with the hidden checks correct, how the review ended, and the attempt's input tokens across both roles, cached input included. "Rescued" means the code before review was graded wrong and the submitted code was correct; "wrong" means the submitted code failed hidden checks. "r0" is the first repetition and "r1" the second.

### Run 1: supplied scenarios

| Task | Repetition | Sonnet reviewer | Haiku reviewer |
| --- | --- | --- | --- |
| `r70-4-go` | r0 | correct (18 of 18), approved unchanged, 0.14M | correct (18 of 18), approved unchanged, 0.10M |
| `r70-4-go` | r1 | correct (18 of 18), approved unchanged, 0.10M | correct (18 of 18), edited; already correct before review, 0.44M |
| `r70-1-go` | r0 | correct (25 of 25), approved unchanged, 0.07M | correct (25 of 25), approved unchanged, 0.09M |
| `r70-1-go` | r1 | correct (25 of 25), approved unchanged, 0.16M | correct (25 of 25), approved unchanged, 0.14M |
| `r70-4-elixir-2` | r0 | correct (18 of 18), approved unchanged, 0.14M | correct (18 of 18), approved unchanged, 0.12M |
| `r70-4-elixir-2` | r1 | correct (18 of 18), approved unchanged, 0.12M | correct (18 of 18), edited; already correct before review, 0.29M |
| `r70-6-elixir-2` | r0 | correct (24 of 24), approved unchanged, 0.24M | correct (24 of 24), approved unchanged, 0.39M |
| `r70-6-elixir-2` | r1 | correct (24 of 24), approved unchanged, 0.18M | correct (24 of 24), edited; already correct before review, 0.27M |

| Setting | Correct | Wrong submissions | Ended by a blocking review | Reviewer edited the code | Builder input | Reviewer input | Output | Anthropic usage at list price | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet reviewer | 8 of 8 | 0 | 0 | 0 of 8 | 0.87M | 0.27M | 105k | $0.57 | 35.2 min |
| Haiku reviewer | 8 of 8 | 0 | 0 | 3 of 8 | 0.86M | 0.98M | 136k | $0.13 | 44.3 min |

- All 16 attempts were correct and needed no builder repair: the builder's first verification was green in every one, and each reviewer approved at its first review.
- The Sonnet reviewer edited the code in 0 of 8 attempts and the Haiku reviewer in 3 of 8. Those 3 trees were graded before review and were already correct (18 of 18, 18 of 18 and 24 of 24), so the edits were not needed (edited, already correct). No wrong code reached review in these 16 attempts, so run 1 cannot test the rescue question.
- With the scenarios, these four tasks were too well specified for the weak builder to reach review with wrong code. Run 2 removed them.

### Run 2: prose specifications, no scenarios

| Task | Repetition | Sonnet reviewer | Haiku reviewer |
| --- | --- | --- | --- |
| `r70-4-go` | r0 | correct (18 of 18), approved unchanged, 0.18M | **wrong** (17 of 18) after the edit, 17 of 18 before, 0.15M |
| `r70-4-go` | r1 | correct (18 of 18), approved unchanged, 0.09M | correct (18 of 18), approved unchanged, 0.19M |
| `r70-1-go` | r0 | **rescued**: correct (25 of 25) after the edit, 11 of 25 before, 0.15M | **wrong** (24 of 25) after the edit, 11 of 25 before, 0.22M |
| `r70-1-go` | r1 | **rescued**: correct (25 of 25) after the edit, 11 of 25 before, 0.13M | **blocked** after an edit; its last code, evaluated anyway, had 24 of 25; code before review not graded, 0.15M |
| `r70-4-elixir-2` | r0 | **wrong** (17 of 18), approved unchanged, 0.10M | correct (18 of 18), approved unchanged, 0.28M |
| `r70-4-elixir-2` | r1 | correct (18 of 18), approved unchanged, 0.21M | correct (18 of 18), edited; already correct before review, 0.38M |
| `r70-6-elixir-2` | r0 | **wrong** (23 of 24), approved unchanged, 0.20M | correct (24 of 24), approved unchanged, 0.13M |
| `r70-6-elixir-2` | r1 | correct (24 of 24), approved unchanged, 0.18M | correct (24 of 24), approved unchanged, 0.24M |
| `artifact-go` | r0 | correct (29 of 29), approved unchanged, 0.07M | correct (29 of 29), approved unchanged, 0.07M |
| `artifact-go` | r1 | correct (29 of 29), approved unchanged, 0.08M | correct (29 of 29), edited; already correct before review, 0.11M |

| Setting | Correct | Wrong submissions | Ended by a blocking review | Reviewer edited the code | Builder input | Reviewer input | Output | Anthropic usage at list price | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet reviewer | 8 of 10 | 2 | 0 | 2 of 10 | 0.98M | 0.41M | 131k | $0.67 | 48.1 min |
| Haiku reviewer | 7 of 10 | 2 | 1 | 5 of 10 | 1.09M | 0.83M | 201k | $0.17 | 58.5 min |

- Every attempt reached review at its first verification, with no builder repair. Wrong code reached the review in 6 of 20 attempts (4 with the Sonnet reviewer, 2 with the Haiku reviewer). One more attempt (the Haiku reviewer's second `r70-1-go`) was blocked; it has no submission and its pre-review code was not graded.
- **Rescues:** the Sonnet reviewer rescued both of its `r70-1-go` builds. Each had 11 of 25 checks correct before review and 25 of 25 after the reviewer's edit. The same 14 checks failed before review in both and in the Haiku reviewer's first `r70-1-go` build, the three `r70-1-go` builds graded before review.
- **Misses:** the Sonnet reviewer approved two wrong builds unchanged (17 of 18 and 23 of 24 checks). The Haiku reviewer approved no wrong build unchanged, but edited two without fixing them: its first `r70-1-go` build went from 11 to 24 of 25 checks and still failed one, the same check that its second `r70-1-go` attempt's final code failed; its first `r70-4-go` build was 17 of 18 before and after the edit, failing the same check.
- **Blocked:** in the Haiku reviewer's second `r70-1-go` attempt, the reviewer edited the code and returned a blocking finding, which said that every real invocation in the form the specification names was rejected; the attempt ended with no submission. Its final code, evaluated anyway, had 24 of 25 checks. The code before review was not graded, so whether it was wrong before the edit is the reviewer's judgement, not a measurement.
- `artifact-go`, the task built so that checks in the builder's folder can be green while a clean checkout fails, was correct in all four attempts (29 of 29 checks): the builders changed the declared build step to create the program, so the trap did not catch any of them.
- The Haiku reviewer edited the code in 5 of 10 attempts and the Sonnet reviewer in 2 of 10; the Sonnet reviewer edited only the two wrong `r70-1-go` builds that it rescued.
- Reviewer input was 0.41M for the Sonnet reviewer and 0.83M for the Haiku reviewer in this run. Input is summed from unrounded values across roles; wall time is the sum of the attempts' durations, and the four hosts differ in speed.
- Anthropic usage is priced at the list prices current at the time (Sonnet 5.5: $2 per million input tokens, $10 output, $0.20 cache read; Haiku 5.5: $0.10, $0.50, $0.01; cache writes at 1.25 times input). These are estimates from the recorded usage, not invoices. No Haiku request had a prompt of 100,000 tokens or more, so the lower Haiku prices apply throughout.
- The two runs recorded 36 attempts, all with Lab outcomes: run 1 used about 2.98M input and 241,000 output tokens, run 2 about 3.31M input and 332,000 output tokens, with no billing, credit, usage-limit or invalid-request responses. The declared budget was $40 per run.

### Were the reviewer's edits needed?

Each attempt in which the reviewer edited the code and approved it was graded on the hidden tests at the builder's last green code before the review: 3 attempts in run 1 and 6 in run 2, 9 in all. This used Lab's snapshot grading and made no model calls; the rows are in [`PRE-REVIEW-GRADES.json`](PRE-REVIEW-GRADES.json). In run 1, 3 of 3 were already correct. In run 2, 2 were already correct (edited, already correct), 2 were rescued and 2 stayed wrong after the edit. The one attempt in which the reviewer edited and then blocked is not in the file; it has no submission to compare with.

### Review limits

Not computed. In every attempt except the blocked one the reviewer approved at its first review, so a review limit would give the same outcome, and the blocked attempt ended at that review. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- Two repetitions per task and setting: a screen. The counts are small. The counts behind the key table are 4 wrong builds seen by the Sonnet reviewer and 2 graded wrong (plus 1 blocked, not graded) seen by the Haiku reviewer; the difference between reviewers rests on a few attempts.
- Each attempt is its own builder run, so the two reviewers were not compared on the same code: each saw only what its own builder runs produced, and a difference in rescues could come from the code as well as from the reviewer.
- The same 14 checks failed before review in all three graded `r70-1-go` builds, so the two rescues are on one task and are probably not independent; the other cases are one attempt each.
- One reviewer attempt, a block, has no grade for the code before review.
- Run 1 and run 2 differ in the specification (scenarios against prose) and in one task (`artifact-go` only in run 2), so they are not a controlled comparison of the two.
- One builder (Haiku 5.5 at low effort) and Kogen's own instruction text were used; other builders and efforts were not tested.
- The settings are approximate: Lab verifies in the builder's folder rather than on a clean copy of the candidate, and the stops are experimental. The frozen settings files also list two roles that were never used (shaper and planner) at Lab's defaults; no request by either is recorded.
- Lab's equivalence to Kogen at commit b45ba32b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b, as reproduced by Kogen Lab set to that commit (approximate: clean-candidate verification is not implemented).
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundles' `manifest.json`.
- Model and effort: builder `claude-haiku-5-5` at `low`; reviewer `claude-sonnet-5-5` at `medium` (setting `rev-sonnet`) or `claude-haiku-5-5` at `medium` (setting `rev-haiku`). Provider: Anthropic.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2` in both runs, and `artifact-go` in run 2.
- Command: `kogen-lab freeze`, then `kogen-lab run` on each frozen experiment, then `kogen-lab grade-snapshot` on the code before review of each attempt in which the reviewer edited the code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`PRE-REVIEW-GRADES.json`](PRE-REVIEW-GRADES.json) and the Lab exports in [`bundles/`](bundles/): `bundles/crf1` is run 1 and `bundles/crf2` is run 2. The kept code is not exported; its pre-review grades are in `PRE-REVIEW-GRADES.json`.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen with two repetitions per task, on an approximate build, using one builder and two reviewers; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- Two experiments, each frozen before its first attempt and run from the same frozen Lab development build over four work folders: one on a macOS workstation, two on one Linux server and one on a Linux laptop. Run 1 ran from about 05:42 to 06:05 UTC and run 2 from about 06:13 to 06:41 UTC on 20 October 2026.
- The first freeze of run 2 was refused before any model call, because Lab required scenarios while the specification was prose only; the scenario setting was turned off and the experiment was frozen again.
- The bundles were exported with a later Lab build (3bf295ef) than the one that ran the experiments (e1e0dc34); the later export leaves out the hosts' boundary evidence.
- No attempt was interrupted, repeated or excluded.
- The code before review of each attempt in which the reviewer edited the code was graded after the runs, with Lab's snapshot grading and without model calls.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (36). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public exports; each `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry; codes such as m08 name the reason (see [`MISSING-DECLARED.json`](MISSING-DECLARED.json)).

## What's missing and why

- `circumstances.cap_end` (36 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (36 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (36 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (36 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (36 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (36 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (36 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (36 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (36 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (36 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (36 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (36 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (36 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (36 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (36 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (36 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (36 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (36 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (36 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (36 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (36 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (36 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (36 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (36 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (18 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (36 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (36 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (36 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (36 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (36 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (36 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (1 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (36 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (36 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (36 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tokens.phases.develop.cached_input` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (36 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (36 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (36 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (36 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (36 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (36 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (36 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (36 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
