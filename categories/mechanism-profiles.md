# Checkpoint cost and provider-retry frequency: two profiles of Kogen run logs

**Descriptive, model-free.** This page profiles two costs in Kogen run logs that were already recorded. Each question was registered with a build threshold before the logs were read. Neither threshold was reached, so neither change was built. It is not a benchmark round: it has no cells of its own, no grades and no comparison of two settings, so it sits with the [mechanism inventory](mechanism-inventory.md) rather than in the [round register](../rounds/README.md).

## Question and scope

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

Exception for the first profile: two tasks with large repositories sit far above the threshold. They are described below, and they are the one open follow-up.

## Data

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

## Evidence level

**Observation.** The profiles describe how often a cost or a failure occurred in logs that were already recorded. They support "this cost or failure was below the registered threshold in these runs". They do not measure what a changed setting would do, and they do not show that the thresholds are the right ones.

## Limits

- Checkpoint timing is inferred from gaps between events, not from timers inside the save. The estimate includes the checks on saved state, tree hashing, index handling and the protected-file check, so it overstates pure writing. The write-only figure rests on a benchmark on a different disk, not on the machines that ran the cells.
- Only the final checkpoint of each cell is kept, so checkpoint size over a session is not observed. Growth is shown through input tokens and turn index.
- One machine has heavy tails (90th-percentile gaps of 1 to 2 s, up to 10 s), probably from other jobs running at the same time. The population mixes machines under different load.
- The builds are skewed to the benchmark tasks run in these days. The two large-repository tasks exist on one machine only.
- Kogen was built from 60 different uncommitted source versions in the window. The save pattern was read from one source commit.
- Retry profile: shape cells have no run log, so their provider comes from the plan or the output message. 220 kept cells from older runs have no recorded plan and count as unknown. Retries inside Claude Code and inside OpenCode Go shaping are not visible. Anthropic HTTP 400 refusals without message text cannot be separated from exhausted credit.
- The outage window was taken from the operator's set-aside records; no kept cell ended inside it, so none was excluded.
- The run logs and the row-level outputs are not published here. The counts above are reported, not recomputable from this repository.

## What was measured, and what is not published

Measured: the share of build wall time between a turn's last tool call and the next model request (an upper bound for checkpoint cost); the number of cells that ended on a provider failure, by kind and route; and the number and duration of retries that recovered. Not measured: the time inside a checkpoint save, task success, cost in money, or any effect of changing the checkpoint frequency or the retry policy.

The run logs and the row-level outputs are not published, and the analysis scripts are not either, so the counts here are reported and cannot be recomputed from this repository. The cells ran on 60 different uncommitted builds of Kogen, so there is no single Kogen commit to cite; the save and retry code was read from commit `323a967c`. The task `pool-go` named above appears in [the session-cache round](../rounds/chatgpt-session-cache-1/README.md); the two large-repository Go tasks are not part of the published task set. The [mechanism inventory](mechanism-inventory.md) lists checkpoint frequency and the retry policy among 80 changeable parts of Kogen and its build loop.
