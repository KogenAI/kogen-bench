# Model-free profiles of Kogen run logs

**Descriptive, model-free.** This page profiles Kogen run logs that were already recorded: checkpoint cost, provider-retry frequency, build round bounds, provider response durations, losses from cut tool results, roles that end without calling their submit tool, acceptance-named tests by builder model, and builder search tools. It also records one observation about reviewing from on-demand material, and a last section, [Climb results, 29 October](#climb-results-29-october), that reports eight further items. Where a question had a registered rule, the rule is stated with its result. For the first two profiles, each question was registered with a build threshold before the logs were read, and neither threshold was reached, so neither change was built. Every analysis before the last section is a replay of recorded logs: no model was run, no provider request was made and no setting was changed for any of them. The last section is the exception: it reports comparisons of two settings in which models ran, and replays of recorded logs. The page is not a benchmark round: it has no cell records of its own, so it sits with the [mechanism inventory](mechanism-inventory.md) rather than in the [round register](../rounds/README.md).

The first two profiles come first and share a data description. Each later section carries its own data window, method and limits. The summary table below covers the profiles before the last section; the last section has its own summary.

## Question and scope of the checkpoint and retry profiles

Kogen saves a **checkpoint** (a file holding the whole state of a build, so that an interrupted build can resume) several times around every model request and tool call. It also retries a failed model request a few times before it gives up. Two changes were considered:

1. **Checkpoint less often**, for example every few calls or at the end of a round, instead of around every call.
2. **Change the retry policy** for model requests that fail.

Each change is only worth building if the cost it targets is large. Before any model was run on either change, the thresholds were written down:

| Profile | Registered rule | Build it if |
| --- | --- | --- |
| Checkpoint cost | Measure the share of build wall time spent on checkpoint saves | the saves cost at least 5% of build wall time in a relevant group of builds |
| Retry frequency | Measure how many cells end because of a provider failure | provider failures end at least 2% of cells outside an outage |

This page reports both profiles. It uses only logs that were already recorded. It runs no model, makes no provider request and changes no setting. It is observation, not a comparison of two settings.

## Results at a glance

| Profile | Registered threshold | Result | Change built? |
| --- | --- | --- | --- |
| Checkpoint cost | 5% of build wall time | Upper bound for all checkpoint saves plus the checks around them: 2.2% of build wall time overall, 1.9% on short builds, 2.8% on long builds. Pure file-write cost estimated at 0.1% to 0.4%. | No |
| Retry frequency | 2% of cells | 1.03% of retained cells ended on a provider failure (33 of 3,193). 0.69% (22 cells) were of a kind a retry could change. | No |
| [Build round bounds](#build-round-bounds) | At least 20% saving on failing cells with at most 1% false stops | Round limit: met on paper (a global limit of 32 saves 37.8% of input and 41.8% of wall time as an upper bound, with 0.98% false stops) but all the saving is on four long tasks that never passed; on tasks that passed at least once it is about 5%. Repeated-call stop: never fires (0 of 960 cells). | No. The limit Kogen shipped counts requests per verification pass, not per build, so a per-round cap of 32 almost never binds. Comparison cells were cancelled before any ran. |
| [Provider response durations](#provider-response-durations) | A 10-minute budget goes forward if no productive response took longer than 10 minutes | Of 23,368 completed responses the longest took 274.8 s. The only attempts over 10 minutes were 3 stalls with no result. Correction: that replay read build and review only. Shape responses reach 834.8 s (see [the correction](#provider-response-budget-correction-and-stream-timeouts)). | No cells run for the replay itself. Kogen's main branch applies the ten-minute total to every role, including shape, where it would cut productive responses. A fix that restores the previous 30 minutes for shape, refine and init is being built and has not landed. |
| [Tool-result cut losses](#tool-result-cut-losses) | 5% of cut results lose needed content | 17 of 606 cut results (2.8%) are confirmed losses, a lower bound: 575 cannot be tested. | No |
| [Roles that end without calling their submit tool](#roles-that-end-without-calling-their-submit-tool) | None (descriptive) | Shaper 38 of 970 sessions (3.9%), reviewer 3 of 1,200 (0.25%). | Not a round |
| [Acceptance-named tests by builder model](#acceptance-named-tests-by-builder-model) | None (observational) | Terra at high effort missed a named test in 4 of 8 development builds, Sonnet in 0 of 17. Model and loop are confounded. | Not a round |
| [Builder search tools](#builder-search-tools) | Pass and input rule, after a witness that the tools are used | In two exploratory cells the builder never called the offered list and search tools. | No. Closed before any comparison cell. |
| [Review material on demand](#review-material-on-demand-an-observation) | Registered; the comparison is still running | Observation only: clean controls 30 of 30 landed in both arms. | Running, no verdict |
| [Climb results, 29 October](#climb-results-29-october) | Registered per item | Eight items, each with its own result and limits; see the table at the start of that section. | See that section |
| [Check reuse and the delivery time budget](#check-reuse-and-the-delivery-time-budget-descriptive) | None (descriptive) | Reusing a passing baseline check across restarts could save up to 30% of baseline check seconds in 44 delivery builds, but only with an environment key the logs do not hold. Check commands are 36% of build wall time in benchmark cells and 72% in 15 delivery builds. | Not built; candidate ranking only |
| [Loop stream and shell faults](#loop-stream-and-shell-faults-descriptive) | None (descriptive) | Against a fake model server, Loop never stopped a productive stream or a 700 s silent shell. Response headers do not count as a first byte (90 s wasted per stalled attempt), idle stop is 180 s and ignores comment pings and unfinished events, a 429 `Retry-After` is ignored (fixed 2 s), and a hung shell runs until the task deadline. | Not changed; candidate ranking only |
Exception for the checkpoint profile: two tasks with large repositories sit far above the threshold. They are described below, and they are the one open follow-up.

## Data for the checkpoint and retry profiles

Cells that ended between 24 October 00:09 and 28 October 16:06 (UTC) were read: 3,275 executed cells in 187 runs, of which 3,193 were kept and 82 had been set aside by the operator (61 for exhausted provider credit, 21 for a network outage). The cells ran on three machines. Kogen was built from 60 different source versions during the window, none of them exactly the commit `e2e8196e18facc62b258b29adb6e16ab149f0cbb` that the [mechanism inventory](mechanism-inventory.md) pins. The checkpoint pattern was read from the Kogen source at commit `323a967c`, which is close to but not identical with that commit.

- **Checkpoint population:** 1,048 builds run by Kogen's own build loop that made at least one tool call (11,346 model turns, 12,282 tool calls; 977 landed). Builds handed to an external coding tool are left out, because Kogen does not save a checkpoint around their individual calls. 9,933 turns have a clean measurable gap.
- **Retry population:** every cell with a recorded result: 2,011 build, 1,090 shape and 92 end-to-end cells kept, plus the 82 set-aside cells. By model route, among kept cells: ChatGPT subscription 1,719, Anthropic API 993, Claude Code 347, OpenCode Go 12, unknown 220 (old runs without a recorded plan, mostly shape). The attempt-level data cover 23,550 logical requests and 23,596 attempts.

## Checkpoint cost

**What Kogen does.** For each model turn Kogen walks the working tree, reads the git index, encodes the whole state as JSON (the conversation, the working context and the git index), writes a temporary file, forces it to disk and renames it into place. Around a turn with k tool calls it does this 4 + 2k times: before the request, before the request is sent, after the request is marked in flight, after the response, and before and after each tool call. That is about 6.2 saves per turn here, more than the two or three that were assumed when the change was first proposed.

**How the cost was estimated.** The logs have no timer around a save. The estimate uses the gap between the last tool call of a turn and the start of the next model request. By the order of the hooks, that gap holds 4 of the turn's saves, the checks on the saved state, the preparation of the next request's context and, after a shell call, a check that protected files are unchanged. Only gaps with no other event inside them were used. Each turn's total checkpoint time was then estimated as the gap divided by 4, times (4 + 2k). This is deliberately generous: it counts the checks and the tree hashing as checkpoint time, so it is an **upper bound**.

**A separate estimate of the pure write.** Kogen's save pattern (encode, write a temporary file, force it to disk, rename) was timed on a personal computer's disk for state sizes of 0.1 to 2 MB: 1 to 3 ms to encode and 0.5 to 7 ms to write. Taking 3, 10 and 50 ms per save over the 69,948 saves in the population gives 0.10%, 0.32% and 1.62% of build wall time. That disk is not the disk of the machines that ran the cells, so treat this as an order of magnitude only.

**Share of build wall time (upper bound, all saves plus the checks around them):**

| Group | Builds | Turns | Share of build wall time | Share of whole-cell wall time |
| --- | ---: | ---: | ---: | ---: |
| All | 1,047 | 11,345 | 2.16% | 1.08% |
| 5 turns or fewer | 460 | 1,688 | 1.52% | 0.53% |
| 6 to 20 turns | 458 | 4,387 | 1.86% | 0.87% |
| 21 to 60 turns | 113 | 4,047 | 2.80% | 1.48% |
| More than 60 turns | 16 | 1,223 | 1.39% | 0.91% |
| Build phase under 60 s | 425 | 1,624 | 1.91% | 0.58% |
| Build phase over 1,200 s | 40 | 2,253 | 1.17% | 0.79% |
| Machine A, B, C | 427, 202, 418 | | 1.32%, 1.62%, 3.07% | |
| Machine C, more than 20 turns | 55 | 2,199 | 3.71% | 2.04% |
| All except the two large-repository tasks | 1,024 | 10,805 | 1.39% | 0.70% |

The registered groups are the short and the long builds. Under the registered split (20 turns or fewer, and more than 20) they sit at 1.9% and 2.8%, below the 5% threshold. The threshold is not reached in any group in the table.

**Per-save cost.** The median cost of a save, including the checks around it, is about 20 to 50 ms on two of the machines and 25 ms early in a session on the third. Directly measured pairs of consecutive reads (two saves plus the checks) took 44 ms and 114 ms at the median on the two machines where they could be measured.

**Does it grow over a session?** Yes, by a factor of about 2.5, and then it levels off. The median gap for four saves grew from about 94 ms (turns 1 to 5) to 258 ms (turns 21 to 40) on one machine, and from 163 ms to about 200 ms on another. The levelling follows Kogen's input ceiling of 512 KB, after which the working context is reset and the checkpoint stops growing. The final checkpoint is 132 KB at the median for builds of 5 turns or fewer, 251 KB for 6 to 20 turns, 567 KB for 21 to 60 turns and 461 KB beyond 60. Model time per turn grows too, so the share stays between 1% and 3%.

**The exception: two large-repository tasks.** On two Go tasks with large repositories (23 cells, 3.6% of build wall time, all on one machine), the gap for four saves has a median of 1.3 to 2 s and reaches 10 s. That is 20% to 30% of build wall time as an upper bound, and all 23 cells are above 5%. Their checkpoints are 1.2 to 1.9 MB, about half of which is the encoded git index, because the repository is large. The same checkpoint size on other tasks costs about 200 ms. So the cost on these two tasks follows the size of the repository (reading and encoding the index, hashing the tree, checking protected files), not the length of the conversation, and the logs cannot say how much of it is the file write. Outside these two tasks, 31 more cells exceed 5% individually (3% of cells), mostly runs on a loaded machine; no group does.

**Reading of the result.** The registered groups sit at 1.5% to 2.8% as an upper bound that includes work other than writing, and the write itself is probably 0.1% to 0.4%. Saving less often would not remove the cost that exists on the large-repository tasks. No change to checkpoint frequency was built.

**One cheap follow-up that is not a lever.** Add a timer for each part of a save (tree hashing, index read, encoding, write and flush, checks) and run each of the two large-repository tasks once. That would show whether the index and tree cost matter for large repositories.

## Retry frequency

**What Kogen already does** (in its model-request code, source at `323a967c`): up to 3 transport attempts per request with waits of 2 s and then 8 s; one retry of an unreadable answer for providers that do not use an API key; one token refresh and retry after an authentication failure (never for key-based providers); a 30-minute budget per request. Rate limits, server errors, network errors and cut streams count as temporary. A definite refusal, such as an HTTP 400, is never retried. For key-based providers (Anthropic API, OpenCode Go) an unreadable answer is also never retried and ends the cell at once as an invalid response.

**How cells were classified.** The outcome comes from each cell's result file plus the last line in its output that names a provider failure, anchored to the start of a line so that task text quoting provider messages does not count. The provider comes from the failed attempt, the message text or the configured models. Attempt data come from the recorded provider attempts, grouped by request.

**Cells that ended on a provider failure (33 of 3,193 kept cells):**

| Kind of ending | Cells | Route | Notes |
| --- | ---: | --- | --- |
| Unreadable answer, one attempt, never retried | 17 | Anthropic API | 9 of the 17 are on one task (`pool-go`; 5 of its 6 repetitions in one 4-minute window). 15 in build, 2 in review. |
| Temporary failure that outlasted 3 attempts (10 s of waiting) | 5 | ChatGPT subscription 4, OpenCode Go 1 | The four ChatGPT cells are one name-lookup failure on one machine over 7 minutes on 26 October. The OpenCode Go cell is an HTTP 429 (rate limit) after 3 attempts in shape. |
| HTTP 400 refusal, reason text not kept | 7 | Anthropic API | Mostly next to the period of exhausted credit, so they cannot be told apart from it. |
| HTTP 400 with "credit balance too low" | 3 | Anthropic API | Account funds. |
| Output-length refusal on a stream | 1 | ChatGPT subscription | A request limit, not a temporary failure. |

**Cells set aside by the operator (not in the rates below).** 61 cells ended with an Anthropic HTTP 400 for exhausted credit (26, 24 and 11 on the three machines). 21 cells ended during a network outage on 28 October (19 shape or end-to-end cells that failed after 3 attempts with a network error, 1 Anthropic network failure and 1 more ChatGPT end-to-end cell). No kept cell ended inside the outage window. Of 347 cells run through Claude Code, none ended on a provider signal; retries inside Claude Code are not visible in these logs. No cell ended on a rate-limit or usage-limit message except the one OpenCode Go case, and ChatGPT server overload appeared only as retries that recovered.

**Rates.**

| Measure | Cells | Rate |
| --- | ---: | ---: |
| Provider-ended, kept cells | 33 of 3,193 | 1.03% |
| Of a kind a retry could change (temporary failures plus unreadable answers) | 22 of 3,193 | 0.69% |
| Temporary failures only | 5 of 3,193 | 0.16% (one name-lookup episode is 4 of the 5) |
| Kept cells plus the credit-exhaustion cells | 94 of 3,254 | 2.89% |
| Outage cells | 21 of 3,275 | 0.64% of executed cells |

The 2.89% figure is the only one above the 2% threshold, and it exists only if cells that ended for exhausted credit are counted. No retry can fix an empty account.

**By route (kept cells that used it).** Anthropic API 27 of 993 (2.72%: 17 unreadable answers and 10 HTTP 400), ChatGPT subscription 5 of 1,719 (0.29%), OpenCode Go 1 of 12, Claude Code 0 of 347.

**Attempt level.** Of 23,550 requests, 34 needed a retry and recovered. All 34 were on the ChatGPT route (19 network errors or cut streams, 14 server-overload answers, 1 HTTP 504), and all recovered on the second attempt. The recovered retries cost 2,202 s in total (median 4.5 s, 90th percentile 28 s; one took 903 s because the failed attempt itself ran about 15 minutes). That is 0.15% of the 403 hours of stage time in the cells. Of 38 temporary episodes (34 recovered, 4 that ended a cell), the existing policy recovered 34 (89%). The remaining failures were correlated name-lookup trouble and the outage, both infrastructure problems that outlast any waiting time that would be reasonable. The 7 cancelled attempts were cell deadlines, not provider failures.

**Reading of the result.** Temporary failures end 0.16% of cells, far below the 2% threshold, and the existing policy recovers most of them. No retry or waiting variant was built. Two observations are recorded for the owner and are not levers from this data: the 17 unreadable Anthropic answers cluster on one task, which looks task-specific rather than random, so a single retry may not help (retrying once on such cells is a cheap thing to try on that task); and credit exhaustion cost 61 cells, so stopping new launches when the account balance is low would have saved more than any retry change.

## Build round bounds

**Question.** A native Kogen build can run many model requests. Two bounds were proposed: stop a build after a fixed number of build rounds (a round here is one model request plus the tool calls it asked for), and stop it when the builder repeats the same tool call three times in a row. Would either one save work on builds that never pass without stopping builds that would have passed?

**Registered rule.** Written down before the logs were read. Candidate limit N, per task class, is the smallest round count that covers at least 99% of passing cells. Cells with a real limit would be run only if the replay projected a saving of at least 20% of wall time or of input tokens on failing cells, with at most 1% projected false stops (passing cells that the bound would have ended).

**Method.** 960 native build cells were read from 2,142 retained run logs of 24 to 28 October: 819 passed all hidden tests and 141 did not. Left out: 901 logs with no build request (877 review-only seeded cells, 24 empty), 181 Claude Code cells, 68 cells outside the build phase and 32 cells that ended on a provider or infrastructure failure. The logs carry no round number, so a round is counted as one build-role request. Task classes: short (13 small tasks), lc (8 long-session tasks), long (5 long tasks) and other (everything else). A limit is projected by dropping every request after the N-th on failing cells. Saved wall time is given as a range: an upper bound (cell end minus the end of request N, which includes review and finishing) and a model-only floor (the summed time of the skipped requests). The repeated-call check compares the tool name and a hash of the arguments of each build tool call, in order. This is a replay of recorded logs; it runs no model.

**Rounds to green.**

| Class | Passing cells | Failing cells | Rounds, passing cells (median, 99th percentile) | Rounds, failing cells (median) | Candidate N | False stops | Failing cells above N |
| --- | ---: | ---: | --- | ---: | ---: | --- | ---: |
| short | 220 | 18 | 5, 19 | 4.5 | 19 | 1 (0.45%) | 0 |
| lc | 144 | 10 | 4, 33 | 18 | 33 | 1 (0.69%) | 0 |
| long | 9 | 105 | 6, 11 | 37 | 11 | 0 of 9 | 82 |
| other | 446 | 8 | 6, 34 | 8.5 | 34 | 3 (0.67%) | 0 |
| All | 819 | 141 | 5, 32 (maximum 40) | 24 (90th percentile 61, maximum 132) | | 5 (0.61%) | 82 |

Passing cells need few rounds. Failing cells in the short, lc and other classes stop by themselves after a median of 4 to 18 rounds. The long class has 105 failing cells and only 9 passing ones, all on one task (`documentation-lookup-evidence`, 9 of its 33 cells). The other four long tasks never passed in these logs.

**Projected saving on failing cells.**

| Bound | False stops | Input tokens saved | Wall time saved (upper bound, model-only floor) |
| --- | --- | ---: | --- |
| Round limit, per-class N | 5 of 819 (0.61%) | 80.2% | 75.1%, 17.3% |
| Round limit, one global N of 32 | 8 of 819 (0.98%) | 37.8% | 41.8%, 7.1% |
| Round limit, per-class N, only tasks that have at least one passing cell | 1 hit in 60 failing cells | 5.2% | 4.8%, 1.0% |
| Stop on three identical tool calls in a row | 0 | 0% | 0% |

A grid of global limits shows the trade directly:

| Global N | False stops (of 819) | Failing cells that exceed N (of 141) | Input tokens saved | Wall time saved (upper bound, model-only floor) |
| ---: | ---: | ---: | ---: | --- |
| 20 | 33 (4.03%) | 83 | 63.4% | 63.9%, 12.7% |
| 25 | 18 (2.20%) | 70 | 52.4% | 53.6%, 10.1% |
| 30 | 10 (1.22%) | 61 | 41.8% | 44.8%, 7.8% |
| 32 | 8 (0.98%) | 58 | 37.8% | 41.8%, 7.1% |
| 40 | 0 | 47 | 22.8% | 31.6%, 4.3% |
| 50 | 0 | 30 | 11.6% | 16.6%, 2.6% |

**The repeated-call stop never fires.** No cell has two identical tool calls in a row, among 11,006 build tool calls in 960 cells. Nine cells repeat a call somewhere, one of them three times, never one right after the other. The same holds for three identical calls inside one model turn and for three identical whole turns in a row. So the stop would have saved nothing and stopped nothing, and it fails the 20% bar.

**Work after the last progress.** Counting from the last verification pass that changed which checks and acceptance scenarios passed, failing cells spent 16% of their wall time (34,485 s of 217,546 s) and 14% of their build input (44.5 M of 317.3 M tokens) afterwards. This sits in 29 of the 141 failing cells, 24 of them in the long class. With a stricter definition (the last pass that added a newly passing item) the wall-time share is 39% and the input share is still 14%.

**What the round limit does in Kogen.** The limit Kogen shipped counts model requests inside one loop round, which is one verification pass, not requests in a whole build. One witness cell was run on a long task (`opencode-go-subscription`) with the limit set to 32, as a check that the limit acts. It ended on Kogen's existing stop for identical red passes after 16 build requests over 4 verification passes, about 4 requests per pass, and the limit never fired. At that rate a per-round cap of 32 almost never binds. The planned comparison, already narrowed before any cell to a global limit of 32 on the lc and long tasks with the repeated-call arm dropped, was cancelled before any cell ran. The bound that the replay supports is a limit on total build requests, about 32 per build; a request budget of that kind was proposed to Kogen as an option that is off by default. No cell has run with it.

**Reading of the result.** The registered gate is met on paper for the round limit and not met for the repeated-call stop, but the round-limit result is not decisive: all of the saving comes from four long tasks that never passed, where a wrong stop cannot be seen. Restricted to tasks that have passed at least once, the saving is about 5%, below the 20% bar. The repeated-call stop does nothing on this evidence. No bound was switched on in any comparison.

**Limits.**
- The long-class limit rests on 9 passing cells of one task. Zero false stops in 9 is compatible with a true false-stop rate of up to about 28% (95% bound).
- Wall saving is a range of 17% to 75% because the logs do not say how much of the time after request N is review and finishing that a stopped cell would still run.
- The short, lc and other classes have few failing cells (18, 10 and 8), none of them long. "Saves 0" there means there is no evidence for a limit, not proof that no limit helps.
- The cells are the benchmark mix of five days, built from many Kogen source versions and run with many configurations and models. Repetitions of one configuration count as separate cells. No split by version was made.
- A "round" is counted as one request. If Kogen counts rounds differently, for example only requests with tool calls, N shifts by a small constant.
- The repeated-call definition is tool names plus argument hashes. A stop with a different window, or one that also counted turns with no tool call, could behave differently. No retained log contains an event of either new bound, because both are newer than the logs.
- Checks that stop at the first failure leave later checks "not run", so a pass that fails earlier can show a smaller passing set without a real regression. This affects only the progress point, not N or the repeated-call result.

## Provider response durations

**Question.** Kogen gives each model request a budget of 30 minutes, shared by retries and waits. Would a shorter budget of 10 minutes cut any response that eventually produces a result?

**Registered rule.** Decided without running cells. If no request that eventually produced a result took longer than 10 minutes, the 10-minute budget is a pure stall guard and goes forward as a default change, still to be confirmed in a run. If any productive request took longer than 10 minutes, no change.

**Method.** The recorded provider attempts in 2,202 retained run logs of 24 to 28 October: 23,431 attempts (23,368 completed, 56 failed, 7 cancelled). Duration is the recorded wall time of the attempt, in the build and review roles. Percentiles use the nearest rank. A second view counts one operation per request, which spans a failed attempt and its retry. The logs hold ChatGPT and Anthropic API cells on Kogen's own loop only; Claude Code cells have no provider attempt records. This is a replay; it runs no model.

**Completed responses (seconds).**

| Role | Completed | Median | 90th percentile | 99th percentile | 99.9th percentile | Longest | Over 5 min | Over 10 min |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Build | 11,113 | 6.7 | 30.3 | 69.6 | 127.3 | 194.5 | 0 | 0 |
| Review | 12,255 | 10.5 | 48.6 | 128.2 | 187.4 | 274.8 | 0 | 0 |
| All | 23,368 | 8.5 | 39.4 | 110.7 | 174.7 | 274.8 | 0 | 0 |

By route: Anthropic API 7,274 responses (median 4.0 s, 99th percentile 52.6 s, longest 160.7 s), ChatGPT subscription 16,094 (median 10.7 s, 99th percentile 122.2 s, longest 274.8 s). The longest completed responses came from Sol at high effort (99th percentile 146 s, longest 275 s); no model went above 275 s.

**Attempts that produced no result.** Of 63 failed or cancelled attempts that ended in the build and review roles (44 and 19), 33 ended in under 10 s, 27 took 10 to 60 s and 3 took more than 10 minutes. The three long ones lasted 847 s, 901 s and 901 s. All three were Terra requests on the ChatGPT route and all three ended in a provider failure with no result. Two were retried at once and the retry answered in 4.0 s and 8.7 s; the third ended a build cell as refused.

Counted per operation, 2 of 23,368 requests (both reviews, 906 s and 911 s) took more than 10 minutes and still ended in a result, but only through the retry after a stall of about 900 s. No productive provider response took more than 275 s.

**Reading of the result.** By the registered rule, a 10-minute budget would not have cut any response that produced a result in these logs, so it is a stall guard. Those two operations would have finished about 5 minutes sooner. This is a replay: no cell ran with a shorter budget, and the confirmation run the rule asks for has not been done.

**Correction, 29 October.** This replay read the build and review roles only. Calls made while shaping are logged in a different file that it did not read, and they run longer: 12 completed responses took more than 600 s, so a 10-minute total would have cut productive shape responses. The "stall guard" reading holds for build and review, not for shape. See [Provider response budget correction and stream timeouts](#provider-response-budget-correction-and-stream-timeouts).

**Limits.**
- The sample of stalls is three attempts, all from one model on one route. It shows no stall that a shorter budget would have turned into a loss, and it cannot show how a shorter budget behaves on a real stall.
- The longest completed response is 275 s. A slower model or a larger request could exceed 10 minutes legitimately; this replay says nothing beyond the models and requests in the window.
- Claude Code cells, and any provider other than the two named, are not in the data.
- The logs span many Kogen source versions on three machines.

## Tool-result cut losses

**Question.** Kogen bounds every tool result to 16,384 bytes, keeping the first 4,096 bytes and the end around an omission marker. How often does the omitted middle of a cut result hold something the builder later needed?

**Registered rule.** Cells comparing cut settings would be run only if at least 5% of cut results lost needed content. The comparison would be the current cut against the one alternative the replay points to (a larger head share at 16,384 bytes, or 32,768 bytes with an 8,192-byte head), on 13 short and 8 lc tasks, with hidden-test pass first and build input tokens second.

**Method.** In 2,202 retained run logs, a cut result is one whose delivered size is 16,370 to 16,384 bytes. There were 606: 404 among 11,105 build results and 202 among 21,685 review results. The logs record only the tool name, the size and a hash of the arguments and of the result, with no paths, commands or result text. So only one case can be tested: a build `read_file` of a large file. For each of the 54 such cuts, Kogen's own numbering and cut were applied to every large file of the task's start tree and the hash of the delivered text was compared; 31 matched a file. A cut counts as a loss (a confirmed hit) when a later `read_file` of the same file in the same cell overlaps the omitted lines. A symbol that was needed but never re-read cannot be seen, because arguments are hashes. For each hit the cut of the same read was recomputed under other settings, assuming the model would still ask for the same lines. This is a replay; it runs no model.

**Cut results and what could be tested.**

| Class | Build results | Build cuts | Build `read_file` cuts matched to a file | Confirmed hits | Hits among all build cuts |
| --- | ---: | ---: | ---: | ---: | ---: |
| short | 1,618 | 12 | 0 | 0 | 0.0% |
| lc | 1,271 | 42 | 14 | 1 | 2.4% |
| long | 4,367 | 270 | 17 | 16 | 5.9% |
| other | 3,849 | 80 | 0 | 0 | 0.0% |
| All | 11,105 | 404 | 31 | 17 | 4.2% |

Review results are cut less often (202 of 21,685, 0.9%, against 404 of 11,105, 3.6% for build). None of the 202 review cuts could be tested: 127 are reads of review material that is not retained, and 75 are shell or search output. Among build cuts, 350 are shell or search output and 23 are `read_file` cuts that did not match a file, for 575 of 606 cuts that cannot be tested. Among the 31 build cuts that could be tested, 17 (55%) lost needed content, 16 of 17 in the long class and 1 of 14 in the lc class. Short and lc tasks together show 1 hit in 54 build cuts.

**Confirmed losses.** 17 of 606 cut results (2.8%), or 4.2% of the 404 build cuts, below the 5% bar. The long class alone reaches 16 of 270 (5.9%) as a lower bound, but the registered comparison would run on short and lc tasks, which cut little.

**Other cut settings, replayed on the 17 hits** (the needed lines are the lines of the later reads of the same file):

| Cap and head (bytes) | Hits with no needed line omitted | Needed lines still omitted (of 4,923) |
| --- | ---: | ---: |
| 16,384 and 4,096 (current) | 0 of 17 | 4,796 (97%) |
| 16,384 and 8,192 | 0 of 17 | 3,654 (74%) |
| 16,384 and 12,288 | 8 of 17 | 2,665 (54%) |
| 32,768 and 4,096 | 13 of 17 | 641 (13%) |
| 32,768 and 8,192 | 13 of 17 | 884 (18%) |
| 32,768 and 16,384 | 9 of 17 | 1,181 (24%) |
| 8,192 and 4,096 | 0 of 17 | 4,810 (98%) |
| 8,192 and 2,048 | 0 of 17 | 4,923 (100%) |

**Reading of the result.** The registered threshold was not met, so no cells were run. This is not a "no": 575 of 606 cut results cannot be tested from these logs, so the true share can lie anywhere above 2.8%. If the long class were read as satisfying the gate, the replay points to a larger cap (32,768 bytes) over a larger head at the current cap. That reading has not been tested. The replay does not price the extra input: a larger cap doubles the worst-case size of a result carried in every later request. A re-run needs logs that record the bytes before and after the cut and the read range; none of the retained logs do. Newer loop code adds settings for the cut size and head share with the defaults unchanged; they are not part of the commit the [mechanism inventory](mechanism-inventory.md) pins.

**Limits.**
- Only a lower bound, and only for large-file reads, where re-reads are expected. Shell output (build output, searches, test logs) accounts for 350 of the 606 cuts (58%) in the build role alone, and the cost of omitting its middle is unknown.
- The 17 hits are 17 cells but only 8 distinct reads in 5 files of 23 to 47 KB, re-read across repetitions and runs of three long tasks and one lc task. The alternative settings are read from five files.
- Reads of an omitted part through the shell (`sed -n`, `cat`) are invisible, so "no overlapping re-read" does not prove no loss. Files the builder edited before the cut read do not match and count as unmatched.
- Cells are not independent: repetitions of one task and many runs count as separate cells.

## Roles that end without calling their submit tool

**Question.** How often does a Kogen role end without calling the tool that submits its result, which roles, which models, and does input size explain it? No threshold was registered: this is a descriptive replay.

**Method.** Events since 26 October 19:00 UTC, read on 28 October: benchmark cells and Kogen's own development builds. Signatures from the Go source, checked in the logs. For the shaper, the message "the shaper ended without calling submit" under an invalid-output ending after 3 attempts; the loop sends one text reminder per turn without a tool call and fails on the third invalid turn. For the reviewer, a verdict recorded as invalid with the outcome `review_invalid`, with the message "the review ended without calling submit_review" or a refusal for unread pinned source parts. For the builder, a round whose last tool call is not `finish` (a soft signal: a prose answer ends the round and verification runs anyway). Role, model, effort and size come from the request events; size is the input tokens of a session's final request. This is a replay; it runs no model.

**Rates by role.**

| Role | Sessions | Ended without submit | Rate |
| --- | ---: | ---: | ---: |
| Shaper | 970 | 38 | 3.9% |
| Reviewer | 1,200 | 3 | 0.25% |
| Builder round (soft, no `finish`) | 936 | 281 | 30.0% |

The shaper count is of 1,088 sessions: 970 reached an end (817 submitted files, 98 submitted questions, 38 ended without submit, 17 gave invalid submissions after 3 refusals); 55 provider errors, 3 still running and 60 refused for other reasons are left out. 402 of the 1,088 ran as Claude Code sessions (0 failures, size unknown). The reviewer count is of 1,211 sessions: 1,193 approved, 4 asked for changes, 3 were invalid, 11 were unfinished and left out. The request audit and the decision check (57 provider calls) show no case.

**Shaper: model and task, not size.**

| Model and effort | Sessions | Ended without submit | Rate |
| --- | ---: | ---: | ---: |
| Terra medium | 151 | 22 | 14.6% |
| Terra high | 69 | 8 | 11.6% |
| Terra low | 6 | 0 | 0% |
| Sol low | 202 | 8 | 4.0% |
| Sol medium | 47 | 0 | 0% |
| Sol high | 28 | 0 | 0% |
| Sonnet (medium and high) | 353 | 0 | 0% |
| Opus medium | 74 | 0 | 0% |
| Two other models (high) | 10 | 0 | 0% |

By family: Terra 30 of 226 (13.3%), Sol 8 of 277 (2.9%), Claude models 0 of 427, other and unlabelled 0 of 40. All 38 failures had a final request under 45,000 tokens, and no session whose final request was over 50,000 tokens failed (0 of 110). The median final input is 29,800 tokens for failures and 29,400 for successes. Effort alone does not explain it (Terra low 0 of 6, Sol medium 0 of 47). On three tasks the same request failed for Terra and not for Sol: 8 of 8, 10 of 16 and 6 of 8 sessions against 0 of 8, 0 of 19 and 1 of 8. A task that fails once for Terra tends to fail on every repetition. 35 of the 37 benchmark failures had made no submission at all; the other 2 had two refused submissions first. Failing sessions end with three consecutive short turns (41 to 206 output tokens, median 81, against a median of 355 for the last call of a successful session), and two text reminders did not change that.

**Reviewer: rare, and tied to the pinned-source gate.** All 3 failures are among the 36 reviews that carry pinned source parts (the reviewer must read every part before approving). The 1,164 reviews without the gate had 0 failures at any input size up to 250,000 tokens.

| Pinned source parts | Size | Reviews | Failed |
| --- | --- | ---: | ---: |
| 232 | 1.39 MB | 2 (Terra medium) | 2 |
| 100 to 143 | 0.6 to 0.86 MB | 9 (all Opus) | 0 |
| 67 to 97 | 0.4 to 0.58 MB | 25 | 1 (Sonnet, 73 parts, approved twice without reading 23 parts) |

By model: Opus medium 0 of 445, Sonnet medium 1 of 71, Sol high 0 of 285, Terra low 0 of 98, Terra high 0 of 20, Terra medium 2 of 273. Of the 36 gated reviews, 31 were Opus and all passed, so model and size are confounded.

In both 232-part reviews the first request was already about 490 KB of the 524,288-byte request ceiling, with only 26 and 38 of the 232 parts already included, so the reviewer had room for one to three reads. Each ended after a rejected verdict and a short prose turn, and both builds ended with `review_invalid` and the edits left in place. The code shows why the first prose turn is fatal: a rejection for unread parts already counts as the one allowed invalid submission, so the reminder that would follow is never sent.

One more large review was seen after these data were pulled, so it is not in the counts: 181 parts (1.08 MB) at Terra medium, with no rejection. It ran a window-reset loop: requests near 520 KB, each reset followed by re-adding pinned parts back to about 490 KB, then an ending with no tool call.

**Builder: not a failure.** 281 of 936 rounds answered in prose instead of calling `finish`, almost all in Terra repair rounds. From the second round on, Terra ended in prose in 99 of 130 rounds at high effort (76%), 77 of 78 at medium and 40 of 41 at low; in the first round, 12.9% at high effort. Claude builders did so in 5%. The 50,000 to 150,000 token bucket (64.7% of rounds without `finish`) is confounded with repair rounds.

**By input size (final request).**

| Input tokens | Shaper sessions, failed | Reviewer sessions, failed | Builder rounds, without `finish` |
| --- | --- | --- | --- |
| Under 50k | 527, 38 (7.2%) | 971, 0 | 556, 46 (8.3%) |
| 50k to 150k | 101, 0 | 191, 2 | 363, 235 (64.7%) |
| 150k to 300k | 9, 0 | 30, 1 | 17, 0 |
| Over 300k | 0 | 0 | 0 |
| Size not known (Claude Code) | 377, 0 | 8, 0 | not counted |

**Reading of the result.** The shaper pattern belongs to the GPT family and mostly to Terra, varies with the request, and is not explained by size; the loop shape is sound for Claude models and for Sol at medium and high effort (0 failures in more than 560 sessions). The reviewer pattern is rare and appears only in gated reviews whose pinned source nearly fills the request ceiling. Two options these data point to, neither tested: force a tool call at the interface on the turn after an answer with no tool call, and keep separate counters for refused submissions and answers with no tool call. They are observations from logs, not settings that were compared.

**Limits.**
- Shaper model and task are confounded in the benchmark data. The Sol rows on the same three tasks keep that comparison fair, but only for those tasks.
- Kogen's own development builds contribute 93 shape sessions (1 failure), 61 reviews (2 failures) and 103 build rounds. The reviewer size reading rests on 2 such reviews plus the gated passes.
- The assistant text is kept only for the two 232-part reviews. For the shaper, "prose" is inferred from zero tool calls and short output.
- Sessions that recovered (an answer with no tool call, then a valid submission after the reminder) are not logged, so the true rate of such turns is higher than the failure rate here. The failure rate is what ends a role.
- The window is about two days, and the builds ran on many Kogen source versions. Two further sources of runs are not in the data: one retired and one with no runs in the window.

## Acceptance-named tests by builder model

**Question.** When a build's acceptance criteria name Go tests, does the builder sometimes fail to create tests with exactly those names, and does that differ between Terra at high effort and Sonnet at medium effort? No threshold was registered.

**What the data are.** The comparison uses Kogen's own development builds (107 run logs of real Kogen work), not benchmark cells. It is observational: tasks differ between builders, the builds are not independent, and the model and the loop are confounded (Terra runs only in Kogen's own loop, and every Sonnet build whose steps enforce the named tests ran through Claude Code). The Terra high side is 8 builds of 7 distinct Intents, and the 4 builds with a miss come from 3 of them, one of which was built twice. The benchmark cannot test this question, as shown below.

**Method.** A missing named test shows in the acceptance run as a step failing with "required test must run exactly once" (0 found instead of 1), or "Required test did not execute and pass" with "no tests to run". A build counts as having a miss when at least one such scenario fails at any verification pass. Only builds whose step files actually enforce that a named test ran can show a miss; builds with lenient step files cannot, so a zero there is uninformative. Builder model and effort come from the request and executor events. Builds with at least one named test and at least one observed acceptance pass are counted. This is a replay; it runs no model.

**Result.**

| Builder | Builds | Missing at some pass | Missing at the first pass | Missing at the end | Ended by the stop on identical red passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Terra high, native loop | 8 | 4 (50%) | 4 | 2 (25%) | 2 |
| Sonnet medium, native loop | 9 | 0 | 0 | 0 | 0 |
| Sonnet medium, Claude Code | 8 | 0 | 0 | 0 | 0 |

Terra high against both Sonnet groups together: 4 of 8 against 0 of 17 (Fisher exact, two-sided, p = 0.0055). For builds naming 5 or more tests: Terra 4 of 6, Sonnet 0 of 8 (p = 0.015). In the strict subset, where the step file enforces that the named test ran exactly once, the only builds where a miss can show: Terra 4 of 6, Sonnet 0 of 4 (all four through Claude Code, none native), p = 0.076. This last comparison is the fair one, and it is weak. These p-values are unadjusted and the builds are not independent: the 4 Terra builds with a miss come from 3 Intents, and 13 of the 17 Sonnet builds have lenient step files.

In one case the acceptance named 7 tests. The builder wrote a new test file with 2 tests under other names and none of the 7. All 7 scenarios failed on every verification pass (6 passes in one build, 4 in the repeat), the builder answered the feedback without a tool call, and both builds stopped on the stop for identical red passes. The failure text printed only the scenario title and "0 !== 1", not the test names; the names are in the Intent. In another Intent the failure message did contain the name of the missing test, and Terra converged after four identical red passes, going green on pass 6. Terra also recovered in a second Intent after one pass. A Sonnet build of the same Intent as the 7-test case was still starting when the logs were copied, so it is pending and not a result.

**The benchmark has no such tasks.** No benchmark cell for Terra high (0 of 204) or Sonnet (0 of about 800) has acceptance that names tests; 2 cells for Sol at medium effort do. The benchmark grades with hidden tests that the Intent does not name, so missing-named-test rates there are 0 for every builder by construction, and a paired comparison over tasks has 0 informative tasks. For orientation only, paired landing over the 25 tasks that both builders ran (Terra high native against Sonnet medium, infrastructure endings left out): Terra better on 2, Sonnet better on 4, 19 ties; one-sided sign test p = 0.34 for Sonnet better and 0.89 for Terra better.

**A related stall.** A builder that answers red feedback in prose with no tool call, with the same acceptance staying red, is Terra-specific and also appears in the benchmark: three or more identical red passes in 7 of 204 Terra high cells (3.4%), 3 of 39 at medium and 2 of 8 at low, against 0 of 610 Sonnet native cells, 1 of 187 Sonnet Claude Code cells and 0 of 686 Sol medium cells. These benchmark stalls are on long tasks and are missing behaviour, not missing test names. On `opencode-go-subscription`, Sonnet landed 12 of 13 cells, Sol 15 of 15, Terra high 2 of 4, Terra medium 0 of 3 and Terra low 0 of 2.

**Reading of the result.** The pattern is supported only as a Terra-high pattern in Kogen's own builds. It is confounded with loop and step strictness, it is not shown to be general across builders, and the benchmark cannot test it. It is a stall risk, not a certainty: Terra recovered in 2 of its 4 builds with a miss. One cheap change this data suggests, not tested: name the missing test in the failure message. With the name in the message Terra converged; without it Terra stalled twice. Testing it needs a re-run of the 7-test Intent with Terra high plus the named feedback, and with Sonnet in the native loop as the control.

**Follow-up, 29 October: still open.** Two later Terra high development builds missed named items. In one, the failure message did name the 4 missing tests, and the build still stopped after 2 identical red passes; this points more toward the model than toward the wording of the feedback. In the other, the acceptance named a file the build had to produce; the builder made no edits, the file was missing at all 4 verification passes, and the build stopped. A small benchmark comparison then ran one task whose acceptance names tests. Terra high created every named test in 2 of 2 builds, and Sonnet did the same in 2 of 2 builds in the native loop and 2 of 2 through Claude Code. The comparison was set up to need at least 4 Terra builds before reading a result, so with 2 it decides nothing; it is to be re-run on more tasks. These are single builds, described as observed.

**Limits.**
- Observational, with 3 Intents behind the 4 Terra high builds that show a miss and a handful of builds per row of the table.
- Model and loop are confounded. The missing comparison is Sonnet in the native loop on an Intent whose steps enforce named tests.
- Lenient step files cannot show a miss, so the strict subset (0 of 4 for Sonnet) is the honest Sonnet number.
- No paired builds of the same Intent by both builders are usable yet.
- The run logs are not published, so none of this can be recomputed from this repository.

## Builder search tools

**Question.** Kogen's native builder has a shell, `read_file`, `write_file`, `view_image` and the terminal tools, but no `list_files` or `search_text` (the reviewer and the shaper have them). Would giving the builder dedicated list and search tools, instead of shell-only exploration, change cost or pass rate?

**Registered rule.** A research patch (not in Kogen) adds the two tools to the builder. The comparison would run on 13 short and 8 lc tasks with Terra high build and Terra medium review. Better: no task's hidden-test pass rate worse by more than 0.15, and build input tokens or build wall time lower by a median of 10% or more (p of 0.10 or less). Worse: a pass-rate drop of more than 0.15 at the set level, or p of 0.10 or less against. Before any comparison cell, a witness cell had to show the builder actually calling the new tools; if it never did, the climb would close as "offered but unused".

**Method and result.** Two exploratory witness cells with the patch applied.

| Cell | Result | Builder tool calls |
| --- | --- | --- |
| A small Go task | landed in 87 s | `read_file` 4, `shell` 3, `finish` |
| A large-repository Go task | landed | `read_file` 18, `shell` 17, `write_file` 2 |

In neither cell did the builder call `list_files` or `search_text`; it explored with the shell. The comparison cells were cancelled before any ran. No change to the builder tool set was made.

**Reading of the result.** The builder did not use the tools it was offered in these two cells. This is an observation of tool use, not a comparison: no pass rate, input or time was compared, and it does not say what a prompt that tells the builder to use the tools would do.

**Limits.** Two cells, one run each. A builder that is told to prefer the tools, or a different model, might use them.

## Review material on demand: an observation

**Question.** Kogen pushes the candidate source to the reviewer in hash-bound parts of about 6 KB. An option sends a manifest instead (per file the diff size, hunk line ranges and hashes) and lets the reviewer fetch what it needs by path and line range. Does this lower review input without hurting what the review catches?

**Registered rule (the comparison is still running).** Two arms on the same Kogen version: the default parts, and on-demand. Terra medium reviews. Primary, on the 5 long tasks with 2 repetitions per arm, paired by task and repetition: review input tokens per review, a median of 15% or more lower (p of 0.10 or less). Must hold: seeded defects escaping the review not worse by more than 1 in 52, false blocks on 15 clean controls not worse by more than 1 in 30, and no drop in landed long-task cells. Secondary: review wall time, requests and resets, the share of material bytes fetched, and blockers that assert no product defect.

**What has been observed so far. There is no verdict.** The comparison has not finished; the long-task and seeded-defect cells are still running.

- The clean controls are complete: 30 of 30 cells landed in each arm, and no review in either arm blocked without naming a defect.
- Outside the benchmark, whose tasks carry no pinned source, one Kogen development build ran a review in on-demand mode over 181 pinned parts. The reviewer read 2 parts and then blocked with the message that inspection of the complete pinned source was not completed, asserting no product defect. The pinned-source rule still requires every part to be read in on-demand mode, which conflicts with the on-demand option. The comparison does not decide this.
- In default mode, a large review ended in a window-reset loop (see the section on roles that end without calling their submit tool).

**Limits.** An observation, not a result. The clean controls say only that the on-demand option did not block clean cells in these 30 cells. The gated-review case is one build, with a task type the benchmark does not contain.

## Climb results, 29 October

**Correction, 29 October 2026.** Recalculation keeps each task and repetition, leaves evaluator infrastructure failures ungraded, and preserves missing usage. Review times below now measure elapsed review phases, including tool work. Excluding an evaluator infrastructure failure raises the perfect-picker gain to 0.25; the decision to leave that change out is unchanged. Some historical replay totals and blind grades could not be independently verified against a fixed set of source records and should not be cited as verified measurements.

**What this section is.** Unlike the sections above, this one reports comparisons in which models ran. They are "climbs": a part of Kogen was changed on its own, usually through a temporary research patch that is not in Kogen, and the changed setting was compared with the shipped one on the same tasks. The first items below come from the night of 28 to 29 October. All cells ran on Kogen commit [`e2e8196e18facc62b258b29adb6e16ab149f0cbb`](https://github.com/KogenAI/kogen/commit/e2e8196e18facc62b258b29adb6e16ab149f0cbb), the commit the [mechanism inventory](mechanism-inventory.md) pins, on the ChatGPT route, with one change per comparison. The last three items check recorded logs. Only the run-log field re-check ran cells, two small ones.

**How decisions were made.** Each comparison had a rule written before its cells ran. The inference unit is the task: a sign test over per-task means, with at most three looks (after 2, 4 and 6 repetitions) and a one-sided p of 0.02 or less to stop at a look. The effect bars are stated with each item. A result described here as "decided" means it was decided under such a rule written before the cells. It is not decision-grade in the strict statistical sense: the tasks are research-made, there are a few repetitions per task, the models are single named models, and some blocks were stopped early. Where a result is labelled interim or unresolved, no rule has decided it.

**Records.** No cell records are added to this repository with this section. The counts below are reported, and the cell records are not in this repository yet, so none of the numbers can be recomputed from here (the same holds for the interim comparison of review material on demand above).

| Item | Registered rule decided it? | Result | Change to Kogen |
| --- | --- | --- | --- |
| [Default reviewer](#default-reviewer) | Yes, for reviews that fit the window | Terra medium 0 of 52 seeded faults committed and 0 of 30 clean controls blocked, the same as Sol high, with a median review time five to six times shorter. | A change of the shipped default to Terra medium was passed on to be built, behind a confirmation run. Held for reviews larger than the context window until a follow-up reports. |
| [Default builder](#default-builder) | Yes | Terra high used 32% less build input on short tasks with equal pass, but passed 2 of 6 against Sol medium's 5 of 6 on one large-repository Go task. | No change. Sol medium stays the default. |
| [Default shaper effort, first look](#default-shaper-effort-first-look) | No, interim | Sol low shaped in 65% less wall time with the same catches on 5 of 6 tasks and fewer on one. | None yet. The next look is running. |
| [Compact verify-failure summary](#compact-verify-failure-summary) | Yes, no change | Short tasks: build input +0.1%, pass 1.00 against 1.00. Long-session tasks: build input -11.9% at p = 0.23, wall time +8.3%. | None. |
| [Sharing the build's cache key with review](#sharing-the-builds-cache-key-with-review) | Yes, no effect shown | Review uncached input -1.4% against a bar of -20%. | None. |
| [Run-log field re-check](#run-log-field-re-check) | Pass criteria written before the cells | Every field the two cells exercised was present. | None. |
| [Stall-stop threshold and step self-check](#native-stall-stop-threshold-and-shape-step-self-check) | Yes, model-free | No alternative stall threshold reaches the bar. The self-check fired in 24.9% of cells. Its measured time is at least 0.55% of shape time; full timing is missing. | None. An unused step definition was ruled to become a warning. |
| [Response budget correction and stream timeouts](#provider-response-budget-correction-and-stream-timeouts) | Correction of an earlier replay, plus a proposal | Shape responses run longer than build and review ones: 12 completed over 600 s. | None yet. The ten-minute total is safe for build and review only. A fix restoring 30 minutes for shape, refine and init has not landed, and an idle-stream timeout is proposed, not built. |

### Default reviewer

**Question.** A user who does not edit the configuration reviews with Sol at high effort (the shipped default). The review lineup chosen from earlier rounds uses Terra at medium effort. The earlier measurements of that choice ([reviewer-models-seeded-1](../rounds/reviewer-models-seeded-1/README.md), [reviewer-models-clean-1](../rounds/reviewer-models-clean-1/README.md) and [terra-reviewer-seeded-clean-1](../rounds/terra-reviewer-seeded-clean-1/README.md)) predate large changes to the review code. Does the result still hold on current code?

**Registered rule.** Terra medium keeps its candidate status if seeded-fault escapes are no worse than Sol high's (by the Wilson interval rule registered earlier for Terra) and false blocks on clean controls are within 1. A pass sends the maintainers a change of the shipped review default.

**Method.** Build at Sol medium on both arms, then review by Sol high or by Terra medium. Seeded set: 26 cases with a planted fault, 2 repetitions per case and arm. An escape is a committed tree that fails the hidden tests. Clean set: 15 controls without a fault, 2 repetitions per control and arm. A false block is a review that blocks a clean control.

| Set | Measure | Sol high | Terra medium |
| --- | --- | ---: | ---: |
| Seeded, 52 cells per arm | Escapes | 0 | 0 |
| Seeded | Median review wall time | 164 s | 28 s |
| Clean, 30 cells per arm | False blocks | 0 | 0 |
| Clean | Median review wall time | 131 s | 28 s |

Terra medium had one cell with a failing hidden test among the seeded cells. That review blocked, so it is a catch: nothing was committed.

**Reading of the result.** The registered rule passes: no escapes in either arm, no false blocks in either arm, and Terra medium reviews five to six times faster by median time. This agrees with the earlier round on current review code. It was decided under a rule written before the cells, and it is still observation-level evidence: 52 seeded and 30 clean cells per arm, one build model, research-made seeded faults, and no escape on either side, so the data cannot separate two reviewers that both catch every planted fault. A change of the shipped default was passed on to be built, and the registered gate is a confirmation run on the installed version, which is not reported here.

**Reviews larger than the window.** This comparison covers reviews whose material fits the working window. A separate class is large reviews. In one earlier development review, with Terra medium over 133 pinned parts (797 KB), the window reset from 657 KB to 298 KB, 157 KB had to be loaded again, and the review ended without a valid verdict even when the verdict tool was forced. A follow-up was registered before any cell: Sol high against Terra medium as reviewer, Terra high building, on 4 long tasks whose review material (0.47 to 0.61 MB) overflows into parts and resets, 2 repetitions per arm, 16 cells. The primary measure is reviews that end without a verdict, together with landed and hidden-test pass. Terra medium may be the default for large reviews only if its count of reviews without a verdict is not above Sol high's by more than 1 of 8 and its landed count is not lower by more than 1. Otherwise the default change is scoped, and large reviews keep Sol high until the review fixes land. **This was the plan at the first look. The completed follow-up is reported under [Review on a cheaper model for large reviews](#review-on-a-cheaper-model-for-large-reviews-yes).**

**Limits.** Neither arm had an escape or a false block, so the safety result rests on the upper bounds of 0 of 52 and 0 of 30, not on a measured difference. The seeded faults and tasks are research-made. The confirmation run and the large-review follow-up are not reported.

### Default builder

**Question.** The shipped builder is Sol at medium effort, while the chosen lineup builds with Terra at high effort. Would Terra high be a better default?

**Registered rule.** The registered builder rule: no task's hidden-test pass rate worse by more than 0.15, and build input tokens or build wall time lower by a median of 10% or more at a one-sided p of 0.02 or less. Both arms were reviewed by Terra medium. Tasks: 13 short tasks and 7 long-session tasks (an eighth was dropped before any cell because it fails its own start check in 17 of 21 recorded cells), 2 repetitions per arm. The task is the unit.

**Short tasks (13 tasks, all graded).**

| Measure | Result, Terra high against Sol medium |
| --- | --- |
| Hidden-test pass | 1.00 against 1.00 |
| Build input tokens, median per task | -32.4% (13 of 13 tasks lower, p below 0.001) |
| Whole-cell wall time | -40.2% (13 of 13 tasks lower) |

**Long-session tasks (7 tasks, graded).** Hidden-test pass was 1.00 for Sol medium and 0.86 for Terra high: one task failed in both Terra repetitions, and one of those was a review that blocked. Terra high's median build input was 6.4% lower (p = 0.50) and wall time 22.8% lower (p = 0.23). No threshold was reached. Combined over the 20 tasks, the efficiency rule holds on the short tasks and fails the "no task worse" condition on that one task: a large-repository Go task whose acceptance scenarios name items, where Terra high passed 0 of 2 against 2 of 2 for Sol medium.

**Replication, with its rule completed before any replication result.** If Terra passed 3 or more of 4 repetitions on that task, the drop counts as noise and the default changes. At 2 of 4, there is no change until more evidence arrives and the task class is logged as a Terra weakness. At 1 of 4 or fewer, no change, or a change with that class routed to another builder. The replication ran 4 repetitions on both arms on the same Kogen commit: Terra high passed 2 of 4 (one review blocked, one failed 2 hidden tests) and Sol medium 3 of 4 (one failed 2 hidden tests). Over all 6 repetitions, Terra high passed 2 of 6 and Sol medium 5 of 6.

**Decision.** No change: Sol medium stays the shipped build default. The class (large-repository Go whose acceptance names items) is logged as a Terra weakness. This agrees in direction with the observation about [acceptance-named tests by builder model](#acceptance-named-tests-by-builder-model) above. A build lineup scoped by task size (Terra high for small builds, Sol medium otherwise) was considered and is parked, not tested: the short-task result favours Terra, and the one large-repository task favours Sol.

**Reading of the result.** Decided under a rule written before the cells. The result is two facts on different tasks: a large input and time saving with equal pass on short tasks, and a pass difference on one large task over 6 repetitions per arm. The second is one task, not a class of tasks, and Sol medium also failed one repetition there.

**Limits.** 13 and 7 tasks with 2 repetitions per task and arm, one model pair and the ChatGPT route. The replication is one task with 4 repetitions per arm. The long-session block has 7 tasks, so a single task decides its "no task worse" condition.

### Default shaper effort, first look

**Question.** The shipped shaper is Sol at high effort. Would Sol at low effort write Intents that catch as many flaws in a request, in less time and at lower cost? Earlier evidence, in [shaper-models-1](../rounds/shaper-models-1/README.md): Sol low gave a good Intent in 13 of 32 cells against 6 of 32 at high effort, at about a third of the cost. Shape has changed since, so the comparison was repeated on the current shaper.

**Registered rule.** Better: more flaws caught under the frozen bar of the flawed-requests work, or equal catches with shape wall time or cost lower by a median of 20% or more (p of 0.10 or less) and no rise in new flaw hits. Worse: fewer catches, or new flaw hits up. Flaws are scored blind.

**First look (interim).** Six of the 8 planned requests are paired so far: 24 cells (2 repetitions per arm), graded blind. The other 2 requests produced no results in their first attempt and are being run again.

| Measure | Result, Sol low against Sol high |
| --- | --- |
| Flaws caught | Equal on 5 of 6 requests, worse on one (0 of 2 against 2 of 2). Mean change -0.167, one-sided p for worse = 0.50. |
| New flaw hits per cell | Unchanged |
| Shape wall time, median | -65% (p = 0.016) |
| Shape cost | -57% (p = 0.11) |
| Refused submissions | Sol low 0, Sol high 1 |

**Reading of the result.** Unresolved, so a second look runs. The time saving is below the 0.02 bar for a look, but the efficiency rule needs equal catches, and the catches are not significantly different yet numerically lower on one request. Nothing was decided and nothing was changed.

**Limits.** Interim: 6 of 8 requests, 2 repetitions each. Catch counts per request are 0 to 2, so the catch comparison cannot separate small differences. The rubric is research-made.

### Compact verify-failure summary

**Question.** After a failing verification pass, Kogen gives the builder a bounded excerpt of the failure output. A research patch (not in Kogen) gives it a compact summary instead: the failing test names plus the first assertion lines, capped. Earlier Kogen Lab evidence ([screen-kogen-2](../rounds/screen-kogen-2/README.md)) suggested that summaries halve input. Does the patch save input on current Kogen?

**Registered rule.** Better: no task worse on hidden-test pass, and build input tokens lower by a median of 10% or more (p of 0.02 or less at a look). Worse: a pass drop of more than 0.15, or p of 0.10 or less against.

**Result on the short tasks.** 13 short tasks, 2 repetitions per arm, Terra high building and Terra medium reviewing, 52 cells, all landed.

| Measure | Result, patch against shipped |
| --- | --- |
| Build input tokens, median per task | +0.1% (6 tasks lower, 7 higher, p for lower = 0.71) |
| Whole-cell wall time | -2.7% (p = 0.50) |
| Hidden-test pass, after grading | 1.00 against 1.00 |

**Result on the long-session tasks.** The second block ran the same comparison on the long-session tasks: 7 tasks, but only 27 of the 32 planned cells, because the run could not be resumed on another machine and the missing 5 cells were not repaired. The block was graded afterwards.

| Measure | Result, patch against shipped |
| --- | --- |
| Hidden-test pass | 0.79 without the patch, 0.86 with it (no task worse) |
| Build input tokens, median per task | -11.9% (5 of 7 tasks lower, p = 0.23) |
| Whole-cell wall time | +8.3% |

The pass figures of the short-task block need one correction. The first reading of this block ran before grading had finished, and cells without an evaluation counted as failures. After grading, pass is 1.00 in both arms. The same grading check for the next item is reported there.

**Reading of the result.** On short tasks the bar of -10% was not reached and the median change is zero. Short tasks rarely reach a failing verification pass, and that is the only place the summary acts, so the patch had almost nothing to act on: no saving and no harm. On long-session tasks the size of the change (-11.9%) clears the -10% bar, but p = 0.23 is far from the 0.02 the rule asks for, wall time went up, and pass was not lower on any task. The climb was closed as no change, because it is not being extended (the rule allows up to three looks, and none further was run). The bar written before the cells was not met, so the rule closes it as no change. That is a not-shown result, not evidence that the summary has no effect on repair-heavy tasks, where it could still help. It would be reopened only if repair-heavy tasks became a focus.

**Limits.** The long-session block has 27 of 32 cells and 7 tasks. Comparisons use the same 13 matched task-and-repetition pairs in both arms; the pass figures (0.79 and 0.86) are means of task pass rates. One control attempt has no matching patch attempt and is excluded from comparisons. The short-task builds seldom fail verification, so the lever was barely exercised there. Neither block was extended.

### Sharing the build's cache key with review

**Question.** A review starts without cached input: its first request is cold (a median of about 22,000 uncached tokens). A research patch (not in Kogen) gives review a cache routing key that continues the build's key. Does review then use less uncached input?

**Registered rule.** Better: review uncached input lower by a median of 20% or more (p of 0.10 or less before the later amendment, 0.02 per look after it), with no change in review verdicts on a seeded subset. The prediction written with the patch was that the shared key would route requests but, because build and review prompts differ, review would stay mostly cold.

**Result on the short tasks.** 13 short tasks, 2 repetitions per arm, Terra high building and Terra medium reviewing, 52 cells.

| Measure | Result, patch against shipped |
| --- | --- |
| Review uncached input, median per task | -1.4% (8 tasks lower, 5 higher, p for lower = 0.29) |
| Review verdicts | 26 of 26 approved without the patch, 25 of 26 with it |
| Hidden-test pass, after grading | 1.00 without the patch, 0.96 with it (one task dropped one cell) |

**Reading of the result.** No saving: the change is far from the bar of -20%. As predicted, build and review prompts share no cached prefix, so the shared key cannot make review warm. The one different verdict and the one lost hidden-test cell are single cells, not a pattern. Decided under a rule written before the cells: no change. The row of the inventory for the cache identity scope is now measured, with this result.

**Limits.** Short tasks only, one block, one model pair. The block was not extended. A different design that makes the review prompt share a prefix with the build prompt is not tested.

### Run-log field re-check

**Question.** Kogen commit e2e8196 added fields to the run log. Are they present in a real run? This is a check of the records, not of a changeable part of Kogen, so it has no row in the inventory.

**Registered check.** Written before any cell. Two small cells (two small Go tasks, Terra building with the native loop). Pass: request events carry the round and the request size in bytes, read tool calls carry the source kind and a content hash, any cut result carries the bytes before the cut and the bytes delivered, and any window reset carries its three size fields (input before and after, and the items carried over).

**Result.** A pass for every field these cells exercised. Present: round and request bytes on request events, source kind and content hash on read calls (build and review). Not exercised by these two cells: the cut fields (no result was cut), the cache write count (the ChatGPT route has none, and an empty value is allowed) and the window reset sizes. The reset size fields were seen in a separate dry cell with a lowered window budget, which logged input before (264,161 tokens) and after (107,042) a window reset. Still open: checking the cut fields once enough cut results have accumulated.

**Limits.** Two cells. A pass for the exercised fields says nothing about the fields that were not exercised.

### Native stall-stop threshold and shape step self-check

Two parts that had never been measured were replayed on recorded logs before any model was run. The stall rule was read at Kogen commit `16102c9`, and the replays used logs recorded up to 29 October.

**Native stall-stop threshold.** Kogen's native build stops when a build round made no tool call and its verification pass is identical to the previous red pass (same failing items, same candidate). The question was whether a different threshold would save work on builds that never pass without stopping builds that would have passed. Registered rule: a variant goes to a model comparison only if it saves at least 15% of wall time on failing cells with at most 1% false stops, where a false stop is a passing cell the rule would have ended. Corpus: 997 native build cells, 845 of which passed all hidden tests and 152 of which did not.

| Variant | Failing cells stopped | Wall saved on failing cells (upper bound) | False stops in 845 passing cells |
| --- | ---: | ---: | ---: |
| Stop at the first round without a tool call | 10 | 5.1% | 0 |
| Today's rule | 10 | 4.7% | 0 |
| One more identical pass | 8 | 4.5% | 0 |
| Two identical red passes, tool use ignored | 18 | 8.2% | 2 (0.24%) |
| Three | 15 | 6.6% | 1 |
| Four | 14 | 6.1% | 1 |
| Five | 11 | 5.6% | 0 |
| Six | 10 | 5.1% | 0 |

**Reading.** No variant reaches 15%. The model-only floor of the saving is 0.6% for today's rule and 1.1% at best. All the saving sits in 10 cells on two long tasks, and on failing cells of tasks that passed at least once, today's rule saves nothing. Today's rule has no false stop and is already in Kogen, so the threshold stays. The tool-blind variants carry the only false stops, which shows why the rule requires the absence of a tool call. Limits: "same candidate" is inferred from zero tool calls and no review activity between two passes, not read from a hash. Only 2 cells in the logs ended on this stop in a live run, so the other 8 are replays. The evidence is thin for any threshold.

**Shape step self-check.** Before a shaper submission is accepted, Kogen loads the candidate's step files itself and returns load, ambiguity and wrapper problems as feedback. The question was whether it does enough work to keep. The logs hold 1,498 shape cells, of which 205 ran a version with the check (the rest ran older versions).

- It ran 490 times and returned problems 55 times (11.2%), in 51 of the 205 cells (24.9%). One event can carry several problems: undefined step 38, unused definition 11 (in each of the 11 nothing else was wrong), load error 3, observer mismatch 2, ambiguous step 1, exit-code wrapper 1.
- After a failing check, the shaper's next check in the same cell was clean 37 times and showed a different problem 4 times. The same problem never came back unchanged. In 14 cells a failing check was the last submission and the cell ended refused.
- The 435 measurable clean checks averaged 0.54 s. Their known time is 0.55% of shape wall time. The other 55 checks could not be timed, so the full cost is missing. The readiness gate that follows costs a mean 23.8 s, 10.8% of shape time. Readiness refused 6 times in these cells, all for undefined steps that the check had passed (6 of 435 clean runs, 1.4%), so the check is mostly an earlier and cheaper catch.

**Reading.** The check fires in a quarter of cells, the shaper acts on it every time, and its cost is small, so an off-arm would test a part that does real work for a measured lower bound of about 0.55% of shape wall time, with the full cost missing. It was kept and no comparison was run. One ruling came out of the replay: an unused step definition, which was a refusal reason, becomes a warning, since 11 of the 55 problem events were that alone. That is a change to a rule, not a measured effect, and its effect on refusals is not measured.

**Limits.** The log has no submission text, so "changed in response" rests on the item sets of the next check. 15 runs and 8 tasks, mostly short and long-session tasks. The shaping lanes mix Sol low, Terra medium and Claude Code Sonnet shapers, so the 24.9% is a blend: it is about three times higher on the Sol low lanes.

### Provider response budget correction and stream timeouts

**Correction.** The earlier section on [provider response durations](#provider-response-durations) read the build and review roles only. It concluded that a 10-minute total budget is a pure stall guard. Shape calls are logged in a different file that replay did not read. Read together, the logs hold 34,800 provider attempts in 3,973 cells (25,629 in build and review, 9,171 in shape), of which 34,697 completed. For shape, 9,132 responses completed, with a 99th percentile of 410 s and a longest of 834.8 s. 12 completed after more than 600 s (11 by Sol high and 1 by an OpenCode Go model). Each of them streamed 16,782 to 27,882 output tokens at 33 to 36 tokens per second: long generations, not stalls. A 10-minute total would have cut every one. So the 10-minute result is true for build and review and false for shape. As of 29 October Kogen's main branch applies the ten-minute total to every role, so it applies to shape calls too. A fix that restores the previous 30-minute budget for shape, refine and init is being built and has not landed. The confirmation run for the shorter budget covers build tasks only, not shape.

**Completed response durations (seconds), by model, effort and role.**

| Model | Effort | Role | Responses | Median | 99th percentile | Longest |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Haiku 5.5 | medium | review | 478 | 4.1 | 41.8 | 57.4 |
| Opus 5.5 | medium | review | 1,390 | 8.0 | 59.9 | 84.4 |
| Opus 5.5 | medium | shape | 245 | 16.0 | 236.8 | 298.9 |
| Sonnet 5.5 | low | review | 179 | 2.4 | 11.9 | 14.7 |
| Sonnet 5.5 | medium | build | 4,679 | 3.3 | 54.3 | 160.7 |
| Sonnet 5.5 | medium | review | 611 | 3.7 | 29.8 | 61.0 |
| Sonnet 5.5 | medium | shape | 185 | 8.7 | 192.1 | 228.0 |
| Sol | high | review | 8,170 | 16.5 | 144.9 | 274.8 |
| Sol | high | shape | 2,519 | 23.1 | 565.6 | 825.0 |
| Sol | low | shape | 2,648 | 7.8 | 172.8 | 415.5 |
| Sol | medium | build | 4,093 | 10.9 | 84.6 | 194.5 |
| Sol | medium | shape | 1,045 | 11.7 | 280.2 | 519.7 |
| Terra | high | build | 2,049 | 5.4 | 48.7 | 114.8 |
| Terra | high | review | 120 | 4.9 | 15.0 | 16.2 |
| Terra | high | shape | 577 | 5.1 | 57.1 | 69.6 |
| Terra | low | build | 110 | 4.5 | 35.7 | 36.2 |
| Terra | low | review | 581 | 4.1 | 12.5 | 14.6 |
| Terra | low | shape | 57 | 5.4 | 54.3 | 54.3 |
| Terra | max | build | 168 | 10.9 | 81.1 | 113.4 |
| Terra | medium | build | 494 | 4.9 | 29.6 | 39.9 |
| Terra | medium | review | 2,443 | 4.5 | 23.2 | 44.5 |
| Terra | medium | shape | 1,373 | 5.4 | 59.4 | 126.3 |
| OpenCode Go model, first | high | shape | 167 | 4.8 | 237.9 | 834.8 |
| OpenCode Go model, second | high | shape | 316 | 8.0 | 241.1 | 410.6 |

By role: build 11,593 responses (median 6.5 s, 99th percentile 68.3 s, longest 194.5 s), review 13,972 (9.6, 125.0, 274.8) and shape 9,132 (9.0, 410.3, 834.8). No single total budget fits every model: the longest legitimate response is 16 s for Terra high review and 825 s for Sol high shape.

**Stalls.** Of 103 failed or cancelled attempts (7,617 s of wall, against 704,488 s of completed wall), 6 lasted 300 s or more and hold 4,367 s. Four were Terra build or review attempts of 757 to 901 s that ended with no result. Two of the four were retried at once and the retry answered in 4.0 s and 8.7 s. The other two ended their cell as refused. The other two long attempts were Sol high shape calls (570 s cancelled, 391 s ended by a server-overload error). The roughly 900 s endings fit an older 15-minute budget, not today's default. Replaying total budgets on the same data:

| Total budget | Completed responses cut (of 34,697) | Failed attempts over it | Their wall above the budget |
| ---: | ---: | ---: | ---: |
| 60 s | 2,268 | 22 | 5,278 s |
| 120 s | 746 | 15 | 4,158 s |
| 300 s | 183 | 6 | 2,567 s |
| 600 s | 12 | 4 | 1,005 s |

Every budget below 835 s cuts productive shape responses, and the only budget that cuts none (about 1,000 s) saves almost nothing.

**What the logs do not hold.** The run logs have a field for the time to the first content, and it is empty on all 34,800 records, because Kogen writes a constant empty value. Nothing records the time to the response headers, the time to the first byte, the timing of chunks, the bytes streamed or the longest silent gap inside a stream. So the time to first byte and the gaps between bytes cannot be measured from the retained logs. The only evidence about silence is an upper bound from completed responses with at most 100 visible output tokens: the longest silent period before content is 47.9 s for Sol high review, 11.4 s for the Anthropic models and 14.5 s for the OpenCode Go models. It is a proxy, not a measurement.

**Proposal: an idle-stream timeout (not built, no cell run).** Abort an attempt, to be retried by the existing 3-attempt loop, when no bytes arrive for N seconds after the first byte, or when no first byte arrives within F seconds of the request. The total budget stays as a safety ceiling above the largest legitimate generation. The argument is that the long legitimate generations are streams that deliver bytes every few hundred milliseconds, so an idle timeout does not touch them, while a total budget cuts them. The stalls were silent attempts that ran to the ceiling. Provisional values, to be replaced by measured gaps (twice the longest silent period, with a floor):

| Provider | First byte, F | Idle after first byte, N |
| --- | ---: | ---: |
| ChatGPT route | 90 s | 120 s |
| Anthropic API | 45 s | 60 s |
| OpenCode Go | 45 s | 60 s |

On this corpus, such values would have ended the four Terra stalls and the two Sol high shape stalls at 120 s, saving about 3,450 s of the 4,367 s, while cutting no completed response by gap. The second half of that cannot be checked until gaps are logged. The registered rule states that an idle abort that cuts any completed response is a guard failure that returns the setting for review, and that no timeout may be set or changed without per-model, per-effort and per-role percentiles. The plan has three steps: record the timing fields for a day (observation only, at least 5,000 attempts), replay the idle timeout on that data, and run a small live comparison on the cells where stalls occurred, after a fault-injection test with a server that stops sending mid-stream. Risks: a ChatGPT stream at high effort might stay silent during hidden reasoning for longer than the proxy shows; keep-alive events are documented for Anthropic and were not checked for ChatGPT; and one call path reads a whole body at once and has no idle signal.

**Limits.** Duration only: all N and F values are provisional. Stalls are rare (6 of 34,800 attempts reached 300 s) and mostly Terra, so the stall sample is small. The corpus holds ChatGPT, Anthropic API and OpenCode Go calls on the native loop and shaping, and Claude Code cells have no provider attempt records. Cells are not independent: repetitions and many runs of the same tasks.

## Further results of 29 October

Each item below records the decision at its stated look. A "no" means the change stays out of Kogen. Collection status is established from saved cells and evaluations; absence of a matching process does not establish completion.

### Prompt cache across effort and model changes

- **Anthropic:** a cached prefix survives a change of reasoning effort. It does not survive a change of thinking mode or model.
- **OpenAI:** the first request at a new reasoning effort or a new model read 0 cached tokens; the next read about 99%. Going back to an earlier setting hit that setting's cache entry again. A cache key made no difference.
- **Consequence:** on OpenAI, switching effort or model in the middle of a conversation costs one cold prefix per switch.

### Static repository map in the first request: no

A 2,000-token map of the repository covered 57% of the files the change touched on large tasks; the bar was 70%. It added about 17% to the task-input bytes; this is not the size of the full model request. The bar was 5%.

### Request-matched file retrieval: no

The best keyword-ranked map covered 54–57% of changed files at 2,000 tokens. It reached the 70% bar on 5 of 13 large tasks; the bar was 9. It did no better than a plain keyword search of the repository.

### Best of N with Kogen's own pick: no

A replay of two builds with a pick among those that landed projects a pass gain of 0.10 at 1.72 times the cost per pass. A perfect picker projects a gain of 0.25 after an evaluator infrastructure failure is left ungraded. The cost multiplier assumes both builds consume the same expected resources as a single build; it is a projection, not a measured bill.

### Routing tasks to models by predicted difficulty: no

- **Feature routers:** no router built on task features beat a fixed model lineup.
- **The ideal router:** its savings came only from sending tasks to a cheaper lineup.
- **An external difficulty score:** it tracked pass (correlation −0.50 to −0.64), but no better than the length of the task description (−0.62). A router built on it lost 1.2 to 1.6 task-cells of pass against the best fixed lineup.

### The shaper's conversation continuing into the build: no

At hand-off, the shaper's context was a median of 56,000 tokens. The builder's whole first request was 11,000 tokens. Carrying the context forward would cost 47% of build cost against the 18.5% it replaces. Even with every uncached builder token removed for free, the net change would be −9.4%, short of the 10% bar.

### Reasoning off for builder sub-steps: no

Reasoning tokens are 10–11% of builder output and 2.6–4.2% of build cost. Turning reasoning off could save 2–4% at most; the bar was 20%.

### Authority boundary in the build loop: no

Over 7 tasks:
- uncached review input rose 10.2%;
- cost per cell rose 10.0%;
- cached share fell 0.15 points;
- sign test p = 0.50.

The behaviour stays off.

### Review on a cheaper model for large reviews: yes

On 4 large tasks, reviewing with gpt-6.1-terra at medium effort instead of gpt-6.1-sol at high effort:
- landed 5 of 8 attempts in both arms;
- gave no verdict in neither arm;
- build input +0.8% (p = 0.69);
- wall time −20% (p = 0.06).

Three attempts in each setup stopped during building before review began. Neither setup passed the hidden tests in this block. The result supports the registered landing and verdict guard on this workload; it does not demonstrate equal review quality. Together with the earlier result on smaller reviews, Terra at medium effort holds as reviewer up to the review sizes tested here. The largest reviews remain under test: in one later build with about 200 evidence parts, two Terra-medium reviews ended without a verdict. A follow-up with 30 fresh reviews of that build is [reported below](#reviewing-a-202-part-build-descriptive).

### Ten-minute build and review response budget: confirmed

Over 13 tasks in both arms, every attempt landed and passed. There were no provider, unavailable or budget errors. Shaping keeps the longer 30-minute budget.

### Review resuming the build conversation: no

When Kogen drives Claude Code, having the review continue the builder's session instead of starting a fresh one raised cost per pass by 84%. Wall time was unchanged (p = 0.71), so review keeps a fresh session.

### First-byte timeout on the model stream: open

A batch with timeouts of 90, 30 and 20 seconds saw no stalled requests, so the setting never acted. The earlier stalls (11 of 153 recorded request attempts in one batch, all before response headers) clustered in time. The question stays open until a batch catches a stall window.

## Open results of 29 October

None of the items below is decided. Each is reported as observed, with its numbers, and stays open.

### Check and review changes when Kogen drives Claude Code

**Summary.** Three changes shortened Kogen's per-task wall time by a median of 9% to 14% per task, with cost per pass up 1.7% to 3.1%, but each passed one fewer run than the unchanged Kogen in the same batch (24 of 26 against 25 of 26). Because that pass difference is a single run on one task, it neither confirms nor rules out a pass loss, and all three stay open until a second look. Two further changes showed no clear effect.

The changes were: running the project's checks in parallel; verifying only the parts the change affects; running the independent review only when the change looks risky; deferring the baseline checks; and reusing the baseline check results.

#### Kogen driving Claude Code, claude-sonnet-5-5 at medium effort, 13 tasks, two runs per task

| Change | Median per-task wall change | Tasks faster / slower | One-sided p | Cost per pass change | Passed: change / unchanged Kogen |
|---|---:|---:|---:|---:|---|
| Parallel checks | −13.7% | 10 / 3 | 0.013 | +3.1% | 24/26 / 25/26 |
| Verify only affected parts | −9.1% | 10 / 3 | 0.016 | +2.5% | 24/26 / 25/26 |
| Review only when risky | −11.6% | 11 / 2 | 0.002 | +1.7% | 24/26 / 25/26 |
| Deferred baseline checks | +0.6% | 6 / 7 | 0.32 | −0.5% | 24/26 / 24/26 |
| Reuse of baseline check results | −5.5% | 7 / 6 | 0.21 | −1.2% | 25/26 / 25/26 |

Each change was compared with unchanged Kogen in the same batch. The first batch held deferred baseline checks (and the review-resume change reported above); the second held the other four. The unit is the task: each task's wall time is the mean of its two runs, and p is an exact one-sided Wilcoxon signed-rank test for a shorter wall. The rule written before the runs asked for p of 0.02 or less, no pass loss and a cost rise of at most 5%. Cost is the Claude Code client's own list-price estimate per passing run, not a bill. The p-values are not adjusted across the five changes.

### Landed builds that fail the hidden tests

**Summary.** Of 723 benchmark builds with unchanged Kogen settings that Kogen landed (its checks and review accepted them), 114 (15.8%) then failed the hidden tests. In 65 of the 114 (57%), the failing requirement was not in the Intent the builder received (Kogen's written statement of what the change must do); in 34 (30%) the Intent stated it but no acceptance scenario tested it; in 15 (13%) it was a convention the Intent only implied, such as what a command's help text lists. In none of the 114 did an acceptance scenario specify the failing behaviour exactly and still let the build through. The reviewer approved all 114 at the first attempt and raised no finding at all in 77 (68%).

**What the data are.** A replay of recorded runs: no model was run. The failures were grouped by the hidden test that failed and read against the Intent and acceptance scenarios each build received. The Go and Python failures were replayed against the saved final code; for the Elixir tasks the call rests on the Intent text and an earlier audit of the tasks. Most of the 65 unstated cases come from task versions that were corrected on 27 October, so on the current task versions the pool is about 52 of 723 builds (7.2%).

**Concentration.** Failures sit on a few behaviours, not spread at random: on each small Go or Python task that sometimes passes, nearly every failing build fails the same one or two behaviours. Three tasks never passed in these builds and account for 59 of the 114.

**What the reviewer did.** In the 3 builds where a review discussed the failing behaviour, it judged that behaviour correct, against the hidden test. Reviewers reason from the Intent, so a requirement missing from the Intent is not visible to them.

**Rates by builder (descriptive).** All builds: Sonnet medium through Claude Code 13 of 177 (7.3%), Sonnet medium in the native loop 22 of 154 (14.3%), Terra high 17 of 186 (9.1%), Terra medium 9 of 51 (17.6%), Sol medium 48 of 147 (32.7%). The reviewer differs with the builder, builds of the same task are not independent, and the task mix differs by builder, so these rates do not compare models.

**What would be tested next.** A candidate change is a list made during shaping (the step that writes the Intent) that maps every explicit requirement in the request to an acceptance scenario, with the reviewer checking each entry by running it. Estimated from the classes above, not measured, it could reach the 34 stated cases and remove about 20 to 27 of the 114. Implied conventions would need a separate check against how neighbouring features behave. Neither change has been run.

### Reviewing a 202-part build: descriptive

**Summary.** One large Kogen build, whose review material comes in 202 parts (about 1.2 MB), was reviewed 30 times from scratch, 10 times by each of three reviewers. gpt-6.1-terra at medium effort gave no verdict in any of its 10 reviews. gpt-6.1-sol at high effort and claude-opus-5-5 at high effort gave a verdict in all 10. Whether any verdict was correct was not judged.

| Reviewer, model and effort | Route | Verdicts | Verdicts given | Median wall | Parts read |
|---|---|---:|---|---:|---:|
| gpt-6.1-terra, medium | Kogen's own loop, ChatGPT sign-in | 0/10 | none | 27.9 s | 44 to 81 of 202 |
| gpt-6.1-sol, high | Kogen's own loop, ChatGPT sign-in | 10/10 | 8 approve, 2 request changes | 214.3 s | 202 of 202 |
| claude-opus-5-5, high | Claude Code, its own sign-in | 10/10 | 10 approve | 38.5 s | 202 of 202 |

Every Terra review ended the same way: the reviewer kept answering without using a tool to read the next parts, and the review stopped when Kogen's allowance of reminders ran out, after 44 to 81 parts. Total input over the 10 reviews was about 5.6 million tokens for Terra, 11.7 million for Sol and 36.6 million for Opus, mostly cached in Opus's case. Claude Code received the whole build as one prompt and read it with its own tools, while Kogen's own loop delivered the parts one by one, so the route differs between the reviewers as well as the model; the three rows are not a like-for-like comparison of models. Subscription charges for these reviews are not known. One build, ten repetitions each: this shows how repeatable each reviewer's outcome was on this input, not how often its verdicts are right.

### Jev for task size and difficulty: blocked

Jev is a hosted service that needs an API key, and none was available, so the comparison of task size and difficulty with Jev did not run.

## Check reuse and the delivery time budget: descriptive

Two replays of recorded logs, with no model call and no change to Kogen. Both are unresolved by design: they rank where time goes and which candidate changes have headroom.

### Which check reuse has headroom: only baseline reuse across restarts

[`reproduce/verification-reuse-replay/`](../reproduce/verification-reuse-replay/README.md) replays 2,471 recorded command executions from 44 delivery builds (30 October). Baseline checks (before any change) cost 23,865 s and verification passes 15,124 s. Reusing a **passing** baseline check when a build restarts on the same starting tree could save up to 7,059 s (30% of baseline seconds), but the logs record no toolchain, lockfile or environment, and 3 of 133 same-key groups had mixed outcomes, so reuse is safe only with a full environment key. Running checks at the same time (up to 1,821 s, with false failures at high machine load), re-running only the tests a repair touched (703 s), staged scope (165 s), a different pass cadence (tied to one Go package timeout) and reuse inside one build (no repeat without an edit observed) show no headroom or too little. The next step, a keyed baseline cache, was proposed and not built.

### Where build and shaping time goes

[`reproduce/delivery-path-timing/`](../reproduce/delivery-path-timing/README.md) decomposes the time of 4,389 Kogen cells (22 to 31 October) and 15 real delivery builds. Check commands (startup baseline plus verification) take 36% of build wall time in the benchmark cells and 72% in the delivery builds; the slowest shaping requests (180 s or longer) hold 39% of shaping request time. Review repair (3.3% of wall), builder prompt growth (1.4k tokens per round, 92% to 97% cached from round 2), a failing baseline at start (4 of 1,470 builds) and slow build or review requests (28 of about 28,000) show little headroom. The tables rerun from the published, anonymised rows.

**Limits.** Replay estimates are upper bounds, not measurements of a change. The delivery sample is small (44 builds for the reuse replay, 15 for delivery timing), covers a few days and many Kogen builds, and the logs record neither the Kogen build behind each delivery run nor machine load.

## Loop stream and shell faults: descriptive

[`reproduce/loop-stream-shell-fault-fixtures/`](../reproduce/loop-stream-shell-fault-fixtures/README.md) drives Kogen Loop (Kogen `3e759e88`, vendored Loop pin `89467b8b`) against a fake model server that injects stream and shell faults. It makes no model call and changes nothing, so it is unresolved by design: it decides which candidate changes to screen.

Productive runs were never stopped by mistake: a 60 s wait for the first byte, a 120 s gap, 20 events spread over 200 s and a shell that was silent for 700 s all finished. The waste that exists is bounded by fixed limits. Response headers do not count as a first byte, so a stalled attempt costs 90 s before the retry (280 s if all three attempts stall). The idle stop is 180 s; `: ping` comment lines and the bytes of an unfinished event are not progress. A 429 `Retry-After` is ignored (fixed 2 s then 8 s waits). An unreadable event gets one immediate retry. Loop's shell has no time limit and no silence detection, so a hung command runs until the task deadline; Kogen's 60 s dead-command stop for check commands fires at about 62 s, and the removed 10-minute silent-shell stop behaves as described. Only the Responses wire was driven, each fixture once; the pack lists three issue drafts.

## Evidence level

**Observation.** Except for the climb results, the profiles describe how often a cost, a failure or a behaviour occurred in logs that were already recorded. They support statements such as "this cost or failure was below the registered threshold in these runs" or "this role ended without a submission in this share of sessions". They do not measure what a changed setting would do, and they do not show that the thresholds are the right ones. The climb results are different in kind: they compare a changed setting with the shipped one in cells that ran models. They are observation-level too. Where a rule written before the cells decided an item, the result is called decided under that rule, and it is still not decision-grade in the strict statistical sense: research-made tasks, a few repetitions per task, single named models, and some blocks stopped early. Where a section reports a statistical test, it is on observational data from builds that were not randomised, and the section says so.

## Limits of the checkpoint and retry profiles

- Checkpoint timing is inferred from gaps between events, not from timers inside the save. The estimate includes the checks on saved state, tree hashing, index handling and the protected-file check, so it overstates pure writing. The write-only figure rests on a benchmark on a different disk, not on the machines that ran the cells.
- Only the final checkpoint of each cell is kept, so checkpoint size over a session is not observed. Growth is shown through input tokens and turn index.
- One machine has heavy tails (90th-percentile gaps of 1 to 2 s, up to 10 s), probably from other jobs running at the same time. The population mixes machines under different load.
- The builds are skewed to the benchmark tasks run in these days. The two large-repository tasks exist on one machine only.
- Kogen was built from 60 different uncommitted source versions in the window. The save pattern was read from one source commit.
- Retry profile: shape cells have no run log, so their provider comes from the plan or the output message. 220 kept cells from older runs have no recorded plan and count as unknown. Retries inside Claude Code and inside OpenCode Go shaping are not visible. Anthropic HTTP 400 refusals without message text cannot be separated from exhausted credit.
- The outage window was taken from the operator's set-aside records; no kept cell ended inside it, so none was excluded.
- The run logs and the row-level outputs are not published here. The counts above are reported, not recomputable from this repository.

## What was measured, and what is not published

Checkpoint and retry profiles. Measured: the share of build wall time between a turn's last tool call and the next model request (an upper bound for checkpoint cost); the number of cells that ended on a provider failure, by kind and route; and the number and duration of retries that recovered. Not measured: the time inside a checkpoint save, task success, cost in money, or any effect of changing the checkpoint frequency or the retry policy.

Later sections before the climb results. Measured: the distribution of build requests per cell and the projected effect of a limit; response durations of provider attempts; the share of cut tool results whose omitted part was later read again; how often roles ended without a submission; and, in Kogen's own development builds, how often named tests were missing. Not measured: any effect of changing a bound, a budget, a cut size, a tool set or a review option on pass rate, cost or time, except the two exploratory witness cells and the on-demand clean controls described above, which are observations of single behaviours.

Climb results. Measured: for each compared setting, hidden-test pass per task, build or review input tokens, wall time and review verdicts, in paired cells on one Kogen commit; for the replays, how often a stop or a check acted in recorded logs; and for the response budget, completed and failed attempt durations by model. Not measured: any effect on cost in money, any comparison on tasks or models other than the ones named, the time to first byte and gaps between bytes of a provider stream (not logged), and the confirmation runs of the changed defaults.

The run logs and the row-level outputs are not published, and the analysis scripts are not either, so the counts here, in every section, are reported and cannot be recomputed from this repository. The cell records of the climb results are not in this repository yet. The cells of the sections before the climb results ran on 60 different uncommitted builds of Kogen, so there is no single Kogen commit to cite for them; the save and retry code was read from commit `323a967c`. The climb results ran on Kogen commit `e2e8196e18facc62b258b29adb6e16ab149f0cbb`. The task `pool-go` named above appears in [the session-cache round](../rounds/chatgpt-session-cache-1/README.md); the two large-repository Go tasks are not part of the published task set. The [mechanism inventory](mechanism-inventory.md) lists the parts these profiles touch among 80 changeable parts of Kogen and its build loop.

## Baseline check reuse: a safe prototype with small headroom

[`reproduce/baseline-check-reuse-prototype/`](../reproduce/baseline-check-reuse-prototype/README.md) tests skipping a baseline check on a build restart when the identical check already passed on the same tree, command, toolchain, lockfiles and environment. The prototype (off by default; a failure poisons its key) passed all 15 negative controls and the positive control, and did not hide an environment-caused failure. Replayed over 44 delivery builds with a weaker key it would fire on 33.9% of baseline checks and skip up to 3,094 s, 27.0% of the seconds of restarted builds, but only 4 reuses reach 300 s (mean 41 s), and the logs lack the environment identity, so real savings are lower. Verdict: **unresolved**. Next: a heavy-checks-only variant, or defer.

## Shaping patch screen: the second-host half was an invalid instrument

[`reproduce/shape-screen-terra-b/`](../reproduce/shape-screen-terra-b/README.md) screened three shaping patches against the unpatched shaper (gpt-6.1-terra, medium effort, 13 request-only tasks, 2 repetitions, 4 arms, 104 shapes). Only the 40 shapes of the Linux half are a valid measurement: Intents accepted 9 of 10 (unpatched), 10 of 10, 10 of 10 and 9 of 10, coverage of the requirement lists on accepted Intents .284, .285, .263 and .267, with per-task paired changes in the pack. The other 64 shapes ran on builds that lacked a file written by the installer, so every one failed to start; they are not evidence about the shaper or the patches. A clean rerun of the unpatched shaper against one patch accepted 25 of 26 shapes in both arms ([`reproduce/shape-screen-s5/`](../reproduce/shape-screen-s5/README.md)). Verdict: **unresolved**; no patch raised coverage on five tasks.

