# Model-free profiles of Kogen run logs

**Descriptive, model-free.** This page profiles Kogen run logs that were already recorded: checkpoint cost, provider-retry frequency, build round bounds, provider response durations, losses from cut tool results, roles that end without calling their submit tool, acceptance-named tests by builder model, and builder search tools. It also records one observation about reviewing from on-demand material. Where a question had a registered rule, the rule is stated with its result. For the first two profiles, each question was registered with a build threshold before the logs were read, and neither threshold was reached, so neither change was built. Every analysis is a replay of recorded logs: no model was run, no provider request was made and no setting was changed for any of them. The page is not a benchmark round: it has no cells of its own, no grades and no comparison of two settings, so it sits with the [mechanism inventory](mechanism-inventory.md) rather than in the [round register](../rounds/README.md).

The first two profiles come first and share a data description. Each later section carries its own data window, method and limits.

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
| [Provider response durations](#provider-response-durations) | A 10-minute budget goes forward if no productive response took longer than 10 minutes | Of 23,368 completed responses the longest took 274.8 s. The only attempts over 10 minutes were 3 stalls with no result. | No cells run; the rule's confirmation run has not been done. |
| [Tool-result cut losses](#tool-result-cut-losses) | 5% of cut results lose needed content | 17 of 606 cut results (2.8%) are confirmed losses, a lower bound: 575 cannot be tested. | No |
| [Roles that end without calling their submit tool](#roles-that-end-without-calling-their-submit-tool) | None (descriptive) | Shaper 38 of 970 sessions (3.9%), reviewer 3 of 1,200 (0.25%). | Not a round |
| [Acceptance-named tests by builder model](#acceptance-named-tests-by-builder-model) | None (observational) | Terra at high effort missed a named test in 4 of 8 development builds, Sonnet in 0 of 17. Model and loop are confounded. | Not a round |
| [Builder search tools](#builder-search-tools) | Pass and input rule, after a witness that the tools are used | In two exploratory cells the builder never called the offered list and search tools. | No. Closed before any comparison cell. |
| [Review material on demand](#review-material-on-demand-an-observation) | Registered; the comparison is still running | Observation only: clean controls 30 of 30 landed in both arms. | Running, no verdict |

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

## Evidence level

**Observation.** The profiles describe how often a cost, a failure or a behaviour occurred in logs that were already recorded. They support statements such as "this cost or failure was below the registered threshold in these runs" or "this role ended without a submission in this share of sessions". They do not measure what a changed setting would do, and they do not show that the thresholds are the right ones. Where a section reports a statistical test, it is on observational data from builds that were not randomised, and the section says so.

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

Later sections. Measured: the distribution of build requests per cell and the projected effect of a limit; response durations of provider attempts; the share of cut tool results whose omitted part was later read again; how often roles ended without a submission; and, in Kogen's own development builds, how often named tests were missing. Not measured: any effect of changing a bound, a budget, a cut size, a tool set or a review option on pass rate, cost or time, except the two exploratory witness cells and the on-demand clean controls described above, which are observations of single behaviours.

The run logs and the row-level outputs are not published, and the analysis scripts are not either, so the counts here, in every section, are reported and cannot be recomputed from this repository. The cells ran on 60 different uncommitted builds of Kogen, so there is no single Kogen commit to cite; the save and retry code was read from commit `323a967c`. The task `pool-go` named above appears in [the session-cache round](../rounds/chatgpt-session-cache-1/README.md); the two large-repository Go tasks are not part of the published task set. The [mechanism inventory](mechanism-inventory.md) lists the parts these profiles touch among 80 changeable parts of Kogen and its build loop.
