# Does a stable session id fix prompt caching on a ChatGPT subscription?

Kogen can run its models through a ChatGPT subscription. Each request carried a cache key in its body, but no session id in its headers, and the provider's prompt cache was mostly missed. This round tests a small fix: send the same id as `session_id` and `conversation_id` headers. It has three parts: a single-request probe, a 24-cell comparison of Kogen with and without the fix, and a descriptive look at how the plan's usage meter grew.

## Summary

| Part | What it is | Result | Evidence level |
| --- | --- | --- | --- |
| 1. Single-request probe | A synthetic 8-turn conversation sent in 9 request shapes, one run each (the header shape three times) | With a `session_id` header, 0.91 to 0.98 of the previous request's input came from the cache (median per run), in 6 of 6 runs on two models. Without it, 0.00 in 6 of 6. | Observation |
| 2. Kogen, with and without the header | 24 real builds: 6 tasks, 2 repetitions, 2 lanes | The cached share rose from 16% to 89% in build and from 6% to 84% in review. All 12 builds were correct in both lanes. List-price cost fell 67%. | Observation; the lab's pre-run rule was met |
| 3. Usage meter | Meter readings against the work done on one evening | The meter rose 16 points for $44.65 of list-price work. It kept rising for hours after the work stopped, so the measurement cannot say how the meter weights cached tokens. | Descriptive only |

## Evidence level

Part 2 had a decision rule written down before its first cell (see Part 2). The rule was met. This page still calls it an observation, for four reasons.

- The run's own plan file records only the rule kind "descriptive". The wording of the rule comes from the lab's notes, and this repository cannot check when they were written.
- The Standard capture is incomplete (declared in "What's missing and why"), and there are no official grades.
- It is one model, one route, one host and one day, with short and mid-length tasks.
- It measures cost at list price, not the plan's charge.

Part 1 is an observation by design: one run per shape. Nothing here is production qualification. Part 3 is descriptive only.

## The change

Kogen already sent a per-conversation cache id as `prompt_cache_key` in the request body. The change also sends that same id as two HTTP headers, `session_id` and `conversation_id`. It changes no body, history, instruction or tool. A switch (`KOGEN_CHATGPT_SESSION_HEADERS=off`) turns it off. The patch also updates Kogen's test that lists the exact request headers.

The patch is [session-id.diff](patches/session-id/session-id.diff), 60 lines added and 2 removed, sha256 `43c0f97759168066251c21cbbddc76b9262dc412b1f42811d74e4a16fd8bc2ee`, on Kogen [`687f1407`](https://github.com/KogenAI/kogen/commit/687f140700426b3b4ad3e3eae7f1d854762dad31). Of its files, `cli/provider/wire.go` holds the change, `wire_sid_test.go` tests it, `respond_test.go` is the updated header test, and the rest only add a log event when Kogen resets a long conversation. The comparison lane without the change ([baseline.diff](patches/baseline/baseline.diff)) carries the same logging hunks and nothing else, so both lanes log alike. The comments inside the patch use the lab's working names. The patch is published byte for byte because its hash is part of the run's plan.

## Part 1. Single-request probe (observation)

**Method.** A test file added to Kogen's provider code (Kogen `a0b5e842`) sends a synthetic conversation straight to the ChatGPT-subscription route (`api.openai.com/v1/responses`, the same sign-in token Kogen uses). The probe's source is not published in this round. The conversation has 8 turns. A fixed front of about 5,900 tokens (instructions and 6 tool definitions) comes first. Each turn adds about 500 tokens. Turns 3, 5 and 7 are tool-call turns, and the model's tool call and our answer are replayed with encrypted reasoning, as Kogen does. Every shape sends the same content with its own salt in the first message. Reasoning effort is low.

**Measure.** For each follow-up turn, the share of the previous request's input tokens that the response reports as cached. A turn is a full hit if the cached tokens are at least the previous input minus 1,024. Each run has 7 follow-up turns.

Model gpt-6.1-sol unless stated. "Median" is over the 7 follow-up turns of one run.

| Request shape | Run | Median share cached | Full hits of 7 |
| --- | --- | ---: | ---: |
| No key, no headers | first | 0.00 | 1 |
| Key only (how Kogen sent it) | first | 0.00 | 0 |
| Key only, reasoning items dropped from the replay | first | 0.00 | 0 |
| Key and `conversation_id` header only | second | 0.00 | 0 |
| Key and both headers | first | 0.97 | 6 |
| Key and both headers | second | 0.98 | 7 |
| Key and both headers, repeat with a new salt | second | 0.91 | 6 |
| Key and `session_id` header only | second | 0.98 | 6 |
| Both headers, no key | second | 0.98 | 7 |
| Stored responses with a previous response id | first | refused, HTTP 400 "Store must be set to false" | not run |
| Key and a cache-retention parameter | first | refused, HTTP 400 "Unsupported parameter: prompt_cache_retention" | not run |

| Control model (gpt-6-luna) | Run | Median share cached | Full hits of 7 |
| --- | --- | ---: | ---: |
| No key, no headers | first | 0.00 | 1 |
| Key only | first | 0.00 | 2 |
| Key and both headers | second | 0.98 | 7 |

**Reading.** With the `session_id` header, a growing conversation reused its own cache: 0.91 to 0.98 in 6 of 6 runs on two models. Without it the median was 0.00 in 6 of 6 runs, whatever the body held. The `conversation_id` header alone did nothing. Once `session_id` was present, the body key made no measurable difference. Dropping reasoning items did not help, and Kogen must not drop them. This is what the provider did in these runs. This page does not claim to know the provider's reason.

**Limits.** One synthetic conversation, short (8 turns, under 10,000 tokens), one host, one evening. One run per shape, except the key-and-both-headers shape (three runs on gpt-6.1-sol, one on gpt-6-luna). The shapes were chosen by the lab in two batches. The first batch's shapes were written down before its calls (calls at 16:38 to 16:41 UTC). For the second batch, the lab's notes give a freeze time of about 17:10 UTC, but the batch's output files were last written at 17:06 UTC, so its shapes cannot be shown to predate its calls. The probes cost $0.63 at list price. Per-request records are in [single-call-probe.jsonl](single-call-probe.jsonl); response ids and timings are left out.

## Part 2. Kogen with and without the header

Two lanes build the same six tasks from the same approved Intents, twice each (24 cells). A lane is a Kogen build plus an optional patch.

| Lane | Base Kogen | Patch | Models |
| --- | --- | --- | --- |
| baseline | [`687f1407`](https://github.com/KogenAI/kogen/commit/687f140700426b3b4ad3e3eae7f1d854762dad31) | [baseline.diff](patches/baseline/baseline.diff), logging only | gpt-6.1-sol, medium effort for build and high for review (read from the request log; Kogen's defaults) |
| session-id | the same commit | [session-id.diff](patches/session-id/session-id.diff), the change above | the same |

Build phase only: Kogen builds from a frozen, approved Gherkin Intent, then its own review stage runs. Hidden tests grade the final tree. Tasks: cron-go, inventory-go, ledger-go, pool-go, rate-go, vm-go. All cells ran on one Linux host, two cells at a time, with the baseline and session-id cells of a task interleaved. A one-cell dry run of the session-id lane passed first and is not counted. The ChatGPT cache status was "applied" on all 372 requests, so no request was refused or had its key stripped.

### Rule declared before the run

Taken from the lab's notes, which give the freeze time as about 17:10 UTC. The run's plan file was written at 17:08 and the first cell started at 17:13:

- The session id holds if its build and review cached shares each exceed the baseline's by more than 30 percentage points, with no loss of correctness on the hidden tests.
- Whole-pipeline uncached input, list-price cost and wall time are reported with paired differences. No savings claim goes beyond them.

Cached share is cached input tokens divided by all input tokens, summed over the requests of that stage.

### Results

| Measure | baseline | session-id |
| --- | ---: | ---: |
| Cells correct (all hidden tests passed) | 12 of 12 | 12 of 12 |
| Build cached share | 16.3% (115 requests) | 89.5% (113 requests) |
| Review cached share | 6.5% (70 requests) | 83.8% (74 requests) |
| Build follow-ups with the whole earlier input cached / partly / not at all | 7 / 16 / 80 | 97 / 2 / 2 |
| Review follow-ups, same split | 2 / 2 / 54 | 61 / 0 / 1 |
| Uncached input tokens per cell, mean | 271,715 | 44,763 |
| Cached input tokens, total | 417,792 | 3,394,944 |
| List-price cost, 12 cells | $7.66 | $2.52 |
| List-price cost per cell, mean | $0.64 | $0.21 |
| Requests per cell, mean | 15.4 | 15.6 |
| Wall time per cell, mean | 308 s | 307 s |

A follow-up is any request after the first of its conversation. "Whole earlier input cached" means cached tokens of at least the previous request's input minus 1,024. Each stage of a cell is one conversation, so each lane has 12 build and 12 review conversations, and their first requests are the only cold ones left in the session-id lane.

**Rule check.** Build cached share rose by 73.1 points and review by 77.3 points, both above 30. Correctness was 12 of 12 in each lane, a loss of 0 points. By the lab's rule the session id holds.

**Paired by task and repetition (12 pairs).** The session-id cost was lower in 12 of 12 pairs (two-sided sign test p = 0.0005). The median cost difference was -$0.41 per cell, the median uncached-input difference -206,543 tokens per cell, and the median wall-time difference -9 s. In total, uncached input fell 83.5% and list-price cost fell 67.0%, at the same number of requests and the same wall time.

| Task | Mean cost per cell, baseline | Mean cost per cell, session-id |
| --- | ---: | ---: |
| cron-go | $0.67 | $0.18 |
| inventory-go | $1.13 | $0.36 |
| ledger-go | $0.42 | $0.16 |
| pool-go | $1.00 | $0.31 |
| rate-go | $0.12 | $0.05 |
| vm-go | $0.50 | $0.20 |

**Limits.**

- One route, one model, one host, one day.
- Short and mid-length tasks, and no conversation was reset to a smaller window. Behaviour in long sessions is not measured.
- Cost is the harness's list-price estimate from token counts (`reproduce/cost_calc.py`), not the plan's charge.
- All cells passed in both lanes, so the round cannot show whether the change affects correctness on harder tasks. It shows no loss on these.
- Wall time is not a controlled measure. Cells ran two at a time and the provider's speed varies.
- Per-request token counts are in [request-usage.jsonl](request-usage.jsonl). The run logs they come from are not published.

## Part 3. Usage meter against work done (descriptive only)

This part measures. It does not test anything. It asks how the plan's weekly usage meter, which shows whole percentage points, grew as work was done on one login.

The ledger lists every ChatGPT-model cell that finished on the test host after the weekly reset at 15:46 UTC on 25 October, plus the two probe runs (80 items). Each item's spend is counted at the time it ended. The meter was read about every 10 minutes. The ledger and the meter readings are account activity, so they stay private, and the table below is all this round publishes of them. The cells in the ledger belong to other experiments as well as this round.

| Reading (UTC) | Meter | Items ended | Input tokens | of which cached | Output tokens | List price | Per meter point |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 Oct 17:51 | 6% | 43 | 13.1M | 2.3M | 0.6M | $28.01 | $4.67 |
| 25 Oct 18:21 | 8% | 61 | 18.7M | 5.0M | 0.9M | $36.99 | $4.62 |
| 25 Oct 19:22 | 9% | 76 | 25.7M | 10.4M | 1.2M | $43.01 | $4.78 |
| 25 Oct 19:52 | 10% | 79 | 27.8M | 12.3M | 1.2M | $44.16 | $4.42 |
| 25 Oct 20:53 | 13% | 80 | 30.1M | 14.5M | 1.2M | $44.65 | $3.43 |
| 25 Oct 22:54 | 15% | 80 | 30.1M | 14.5M | 1.2M | $44.65 | $2.98 |
| 26 Oct 03:57 | 16% | 80 | 30.1M | 14.5M | 1.2M | $44.65 | $2.79 |

What the data show:

- On the evening of 25 October, 80 items with $44.65 of list-price work (30.1M input tokens, 48% of them cached, and 1.2M output tokens) moved the meter from 0 to 16 points, which is $2.79 per point.
- Two early windows had a similar raw input but a very different cached share. From the reset to 17:51 the meter rose 6 points for $28.0 (17% of input cached). From 17:51 to 19:22 it rose 3 points for $15.0 (65% cached). Per point that is $4.7 and $5.0, so the meter tracked something close to list-price cost and not raw input tokens.
- That reading does not hold up. The last item ended at 19:55. After that nothing ran on the test host, yet the meter rose from 10 to 16 points by 03:57 the next morning. The meter may update late, or the same login may have been used elsewhere; this data cannot tell which. Either one distorts every per-window ratio above, including the $4.7 and $5.0.

So this part cannot say how the plan's meter weights cached tokens. It also does not support a claim that Part 2's 67% list-price saving would use a third of the weekly allowance. That would need a run that does nothing else on the login and reads the meter after it settles.

**Limits.** Whole-percent readings (up to half a point of rounding each). Spend is booked when a cell ends, but the meter moves during it. One login, one route, one evening. Cells that ran on other hosts or logins are not in the ledger.

## Tasks

Five of the six tasks (cron-go, inventory-go, ledger-go, pool-go, vm-go) are still in use by running experiments. For them, and for the task rate-go, this round publishes IDs and content hashes only (in [PLAN.json](PLAN.json)). No task text, Intent, hidden test, reference code or final code tree is published. The hidden-test names in the bundles are replaced by `test:` followed by the first 12 hex digits of the sha256 of the name, so a later publication of the tests can be matched to them. The five tasks will be published once the experiments using them finish. The sixth, rate-go, is not in use by a running experiment. Its materials are held back here because the export publishes a run's tasks together; a later commit can add them. No task from a real project is part of this round.

## Files

- [records.jsonl](records.jsonl): one Standard record per graded cell (24).
- [bundles/](bundles/chatgpt-session-cache-1/): the published attempt and evaluation of each cell.
- [PLAN.json](PLAN.json): hashes of tasks, hidden tests, Intents, patches, settings and the two Kogen builds, written for the run. The experiment and lane labels in it and in the cell paths are the plain names used on this page. They replace the lab's working labels; no hash input changed.
- [patches/](patches/): the two lane patches.
- [request-usage.jsonl](request-usage.jsonl), [single-call-probe.jsonl](single-call-probe.jsonl): the data of Parts 1 and 2.
- [analysis.py](analysis.py): `python3 -I analysis.py` recomputes every number of Parts 1 and 2 from those files. It checks the token sums in request-usage.jsonl against the records.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 24 |
| Started cells | 24 |
| Finished cells | 24 |
| Graded cells | 24 |
| ITT count | 24 |

## Metadata

Round date: 2026-10-25
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 280d45388bb2170b6d9efc4c39f36917b995050c
Model and effort: gpt-6.1-sol at Kogen's defaults (medium effort for build, high for review; the effort fields of the records are declared missing)
Task IDs: cron-go, ledger-go, vm-go, rate-go, pool-go, inventory-go
Command: lanes-run, lanes-grade and lanes-export on experiment `chatgpt-session-cache-1`.
Kogen commits: 687f140700426b3b4ad3e3eae7f1d854762dad31
Raw records: records.jsonl and the bundle in bundles/chatgpt-session-cache-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings. The task files are not published in this round (see Tasks above); the grades are therefore not recomputable from this repository, and the usage figures are not either, because the run logs are not published.

## What's missing and why
- `circumstances.cap_end` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.effective` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (24 missing): Kogen 687f1407 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): Kogen 687f1407 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (24 missing): Kogen 687f1407 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
