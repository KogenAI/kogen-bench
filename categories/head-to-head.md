# Head-to-head: agent harnesses on short Go tasks (30 October 2026)

Status: DESCRIPTIVE. These are baselines for a hill-climb, not a pre-registered test.

**Correction, 29 October 2026.** An attempt without an evaluation was counted as a failed test, and missing usage was included as zero in some per-pass figures. The table now separates ungraded attempts and withholds totals when usage is missing. Comparisons retain every task and repetition. Passing tests describes the final code, separately from whether the agent completed cleanly.

**Configuration note, 29 October 2026.** In the earlier rounds under Scoreboards 1 and 2, kogen-loop ran with a one-line system instruction set by the test harness instead of its own built-in default instruction, while Codex CLI, Claude Code, Pi and OpenCode each ran with their own built-in instructions. The evening rounds below run kogen-loop with its shipped default instructions, the same way the other harnesses run.

This study compares coding-agent harnesses that get the same task and the same model. It has two scoreboards:

1. **Harness against harness.** The kogen-loop harness, run bare, against Codex CLI and Claude Code. Each harness receives the same single prompt.
2. **Kogen's pipeline against a bare agent.** Kogen adds an Intent, its own checks and an independent review. Each pipeline arm is compared with a bare agent on the same model.

## Evening rounds, 29 October 2026

The strongest evidence comes from the common API route at high effort: **both harnesses passed 8/8**, with median agent wall of **117.4 s for Codex CLI and 139.8 s for kogen-loop**. Codex had lower mean agent wall on all four tasks. Cost per pass was effectively tied at about **$0.09 each**. These are descriptive results from four tasks, not evidence of a general winner.

kogen-loop now uses its shipped default instructions in all of these evening rounds, including the experimental speed patch. Every comparison below keeps the model and effort the same within the comparison.

### Common API route, gpt-6.1-terra, high effort

Four Go tasks ran twice per arm. Both harnesses used the same API endpoint, model and effort, with an enforced read boundary, one cell at a time and balanced execution order. Loop used a protocol adapter; Codex used the endpoint directly, so client and adapter behavior remain part of the measured setup.

| Arm | Passed | Median agent wall | 90th percentile agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 139.8 s | 257.9 s | $0.0913 |
| Codex CLI | 8/8 | 117.4 s | 154.7 s | $0.0917 |

The four task pass comparisons all tied (one-sided sign p = 1). Codex had lower task-mean agent wall on 4/4 tasks (two-sided sign p = 0.125). The loop/Codex cost-per-pass ratio was 0.995. With only four task clusters, neither timing nor cost establishes superiority or equivalence.

Agent wall includes API transport and tools, but excludes setup and grading. API dollar figures use recorded upstream usage and the run's fixed rates, including cache writes; they are estimates, not invoices or subscription prices. Per-pass numerators retain every counted attempt; dry runs are excluded.

### Common API route, gpt-6.1-terra, medium effort

The completed medium round used the same four tasks, two repetitions, common endpoint and read boundary, with one cell at a time. It also included the speed patch. The tasks had already been used in the high-effort round, so changes between sections cannot be attributed to effort alone.

| Arm | Passed | Median agent wall | 90th percentile agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 94.0 s | 138.5 s | $0.0563 |
| kogen-loop speed patch | 8/8 | 94.2 s | 177.6 s | $0.0597 |
| Codex CLI | 8/8 | 98.4 s | 113.2 s | $0.0708 |

All four task pass comparisons tied for each loop arm against Codex (one-sided sign p = 1). The default loop had lower task-mean agent wall on 3/4 tasks and the speed patch on 2/4 (two-sided sign p = 0.625 and 1). Each loop arm had lower task cost on 3/4 tasks (two-sided sign p = 0.625). These small-sample differences are descriptive.

## Additional results, 30 October 2026

### Clean common API route patch screens, gpt-6.1-terra, high effort

The completed medium-effort clean-route table above was checked against its per-cell records and still matches; it is not repeated here. Two small high-effort screens also used the common API route. Each covered four tasks with one counted run per arm. Every arm passed 4/4 in both screens. The first included the unpatched loop; the second compared API changes with the speed patch.

#### Common API route — gpt-6.1-terra, high effort (first screen)

| Arm | Passed | API cost per pass |
|---|---:|---:|
| kogen-loop (shipped default) | 4/4 | $0.0963 |
| Speed patch | 4/4 | $0.1217 |
| Replay patch | 4/4 | $0.1016 |
| Batch patch | 4/4 | $0.0947 |
| Answer-end patch | 4/4 | $0.1012 |
| HTTP/2 patch | 4/4 | $0.0907 |
| Connection-reuse patch | 4/4 | $0.0866 |

#### Common API route — gpt-6.1-terra, high effort (second screen)

| Arm | Passed | Median API cost per pass |
|---|---:|---:|
| Speed patch | 4/4 | $0.0665 |
| Replay patch | 4/4 | $0.0826 |
| Batch patch | 4/4 | $0.0658 |
| Answer-end patch | 4/4 | $0.0806 |

These four-task screens are descriptive. No patch showed a reliable improvement over the unpatched loop beyond noise; the second screen compared API changes with the speed patch, and task-level results were mixed.

### Subscription route, gpt-6.1-terra, medium effort (first completed run)

| Arm | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 23/24 | 26,394 |
| Speed patch | 23/24 | 27,886 |
| Codex CLI | 24/24 | 63,968 |

### Subscription route, gpt-6.1-terra, medium effort (later completed run)

| Arm | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 22/23 graded | missing |
| Codex CLI | 24/24 | 64,717 |

One loop attempt was ungraded and lacked usage, so its cost proxy is missing. A keyword screen on the Codex record was traced to the task repository's ignore rule naming its protected evaluation folder; the recorded command did not open that folder.

### Subscription route, gpt-6.1-terra, high effort (patch screen)

| Arm | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| Speed patch | 23/24 | missing |
| Replay patch | 22/24 | missing |
| Batch patch | 23/24 | 36,703 |
| Answer-end patch | 23/24 | 33,512 |
| Connection-reuse patch | 23/24 | missing |
| HTTP/2 patch | 22/24 | missing |

### Subscription route, gpt-6.1-terra, high effort (harness screen)

| Arm | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 22/24 | missing |
| Speed patch | 23/24 | 34,563 |
| Pi | 22/24 | missing |
| OpenCode | 23/24 | missing |

These subscription tables report pass and cost only. Cost is uncached input + 0.1 × cached input + 4 × output, divided by passes across all attempts. It is an uncached-equivalent token proxy, not a dollar cost or subscription charge. Missing usage stays missing. The completed same-effort pairings had few pass differences; they do not establish a harness or patch advantage.

**Wall-time method from 30 October.** Loop-versus-Codex wall time is measured only on two dedicated cloud machines, with the arms interleaved one cell at a time on the same task. Laptop and desktop runs report pass and cost only. Earlier wall-time figures from these machines are descriptive.

**Route finding.** Loop and Codex reach the model through different endpoints and sign-in clients. From about 04:00 UTC on 30 October, loop's output rate on the same tasks and with similar output counts fell from about 110 to about 48 tokens per second, while Codex wall times stayed about the same. Small route probes measured about 45 versus 81 tokens per second. The evidence points to the route as the source of tonight's subscription wall-time gap, rather than a change in loop's code.

**Tool-use observation.** On tasks both passed, loop ran fewer shell commands and read back less tool output than Codex; it did not run more or wider tests.

### Broader corpus, different subscription routes, gpt-6.1-terra, high effort

This round used 24 Go tasks, one repetition per arm, at each effort. The two harnesses reached the model through different subscription routes, which can affect speed and token accounting. The tables therefore describe the observed combinations of harness and route.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost proxy per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/24 | 74.5 s | 144.8 s | 16,481 | 82,763 | 80.1% | 3,465 | 36,971 |
| kogen-loop speed patch | 24/24 | 78.1 s | 147.2 s | 15,497 | 83,406 | 81.4% | 3,306 | 35,513 |
| Codex CLI | 23/24 | 72.4 s | 149.6 s | 24,887 | 341,721 | 92.7% | 4,843 | 75,941 |

Paired against Codex CLI, the default loop had 1 task pass win, 1 loss and 22 ties (one-sided sign p = 0.75); the speed patch had 1 win, 0 losses and 23 ties (p = 0.5). The median paired wall change was +5.0% for the default loop and +7.2% for the speed patch (two-sided timing sign p = 0.839 and 0.541). These descriptive differences do not establish a pass or speed advantage.

The cost proxy is uncached input + 0.1 × cached input + 4 × output, summed over all attempts and divided by passes. It is not a dollar cost or a subscription charge. Route-dependent token accounting prevents attributing its differences to the harness alone. Wall in this and the following tables is whole-cell time, including setup and failed attempts but excluding hidden-test grading.

### Broader corpus, different subscription routes, gpt-6.1-terra, medium effort

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost proxy per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/24 | 62.2 s | 88.1 s | 13,411 | 46,808 | 71.3% | 2,541 | 26,914 |
| kogen-loop speed patch | 23/24 | 59.4 s | 91.2 s | 12,506 | 50,527 | 75.2% | 2,640 | 26,868 |
| Codex CLI | 22/24 | 58.7 s | 104.6 s | 21,594 | 291,645 | 92.6% | 4,018 | 64,673 |

Each loop arm had 2 task pass wins, 1 loss and 21 ties against Codex CLI (one-sided sign p = 0.5). The median paired wall change was −5.2% for the default loop and −5.3% for the speed patch (two-sided timing sign p = 0.541 and 0.064). These are descriptive observations within medium effort; they do not establish a pass or speed advantage.

### API key versus CLI sign-in, claude-sonnet-5-5, medium effort

This round used 13 Go tasks and two repetitions per arm. Loop used an API key; Claude Code used its own sign-in. These routes can affect speed and token accounting.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Dollar cost per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/26 | 48.4 s | 77.5 s | 11,486 | 52,498 | 78.1% | 5,617 | missing |
| Claude Code | 21/25 graded; 1 ungraded | 60.5 s | 86.0 s | 12,547 | 97,214 | 87.1% | 6,413 | missing |

One Claude Code attempt failed during setup, before an agent ran, and is ungraded. Its measured wall remains in the all-attempt timing. Pairing retains 25 graded task/repetition pairs across 13 tasks: 22 loop passes versus 21 Claude Code passes, with 1 task pass win, 0 losses and 12 ties (one-sided sign p = 0.5). The pass difference is descriptive. The median paired wall change was −15.5%, with lower loop task-mean wall on 12/13 tasks (two-sided sign p = 0.00342). Different routes prevent interpreting the timing difference as a harness-only advantage. Dollar costs were not recorded for these arms and remain missing.

**Evening method.** Only complete, attested rounds are included. Match attempts by task and repetition, omit pairs with an ungraded attempt, then average matched repetitions within each task. Pass wins and losses compare task pass totals over those matched repetitions; tied tasks are omitted from the exact one-sided sign test for a loop pass advantage. Timing and cost sign tests are exact and two-sided. Each task has equal weight; the median paired change is the median of task-mean ratios minus one. Wall medians and nearest-rank 90th percentiles in tables retain all counted attempts. Infrastructure failures are ungraded, and missing usage or cost stays missing.

## Scoreboard 1: kogen-loop against other agent harnesses (same model, same prompt)

All arms used gpt-6.1-terra with high reasoning effort on the same 13 tasks. Within each batch, the arms of a task ran one after the other on the same machine.

### Four harnesses (2 repetitions per task)

| Harness | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop e5054c8 | 25/26 | 73.2 s | 408.6 s | 11,841 | 29,505 | 59.9% | 2,796 | 24,791 |
| Codex CLI 0.165.0-alpha | 26/26 | 63.3 s | 101.0 s | 17,910 | 158,691 | 88.7% | 3,713 | 46,840 |
| Pi 0.73.1 | 25/25 graded; 1 ungraded | 61.4 s | 105.0 s | missing | missing | missing | missing | missing |
| OpenCode 1.19.5 | 25/26 | 97.5 s | 164.4 s | 25,563 | 172,226 | 85.2% | 4,603 | 58,641 |

\*Cost is in uncached-equivalent tokens: uncached input + 0.1 × cached input + 4 × output. Dollar cost was not recorded for these subscription runs.

kogen-loop had the lowest cost per pass among the arms with complete recorded usage. It was 47% below Codex CLI, and also had the lowest uncached input among those arms. Pi has usage for only 25 of 26 attempts, so its full per-pass usage and cost are missing. Its median wall was slower than Codex CLI and Pi. A later batch recorded 11 stalls among 153 request attempts, all before any response headers arrived, clustered in time. This later observation does not establish the cause of the earlier batch's long tail. A run of the updated loop (b8a4046) with first-byte timeouts of 90, 30 and 20 seconds saw no such stalls at all. There, all three variants passed 26/26 at a median of 57–58 s.

### Updated loop against Codex CLI in the same batch (1 repetition per task)

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop b8a4046 | 13/13 | 60.4 s | 69.0 s | 9,228 | 26,351 | 65.0% | 2,627 | 21,448 |
| Codex CLI 0.165.0 | 13/13 | 68.3 s | 79.4 s | 17,822 | 172,731 | 89.7% | 3,753 | 48,323 |

In this batch, with no request stalls, the loop was faster than Codex CLI at the median and at the 90th percentile. It also used about half the uncached input, and cost 56% less per pass.

## Scoreboard 2: Kogen's pipeline against bare agents

### Driving Claude Code, against bare Claude Code

Both arms used claude-sonnet-5-5 at medium effort and ran on the same machine, with 2 repetitions per task.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass† |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 driving Claude Code | 23/26 | 122.5 s | 202.0 s | missing‡ | missing‡ | missing‡ | missing‡ | missing‡ |
| Claude Code 2.1.312 (bare) | 24/26 | 61.9 s | 95.2 s | 11,212 | 88,973 | 87.4% | 5,879 | $0.111 |

†Dollar figures are the list-price estimates that the Claude Code client reports. They are not plan prices.

‡25 of 26 Kogen attempts reported usage and cost. Their known cost sums to $6.730; the full cost per pass is missing.

Kogen's pipeline runs two Claude Code sessions per task: one builds and an independent one reviews. It also runs the project's checks. That explains most of the extra time and cost.

### Native loop with checks and review, against Codex CLI

Both arms used gpt-6.1-terra and ran on the same machine. Kogen built at high effort and reviewed at medium; Codex ran at high effort.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 (native loop, review, checks) | 26/26 | 101.0 s | 131.7 s | 30,919 | 94,672 | 67.3% | 3,836 | 52,637 |
| Codex CLI 0.165.0-alpha (bare) | 26/26 | 58.9 s | 74.1 s | 21,870 | 169,193 | 87.1% | 3,874 | 52,099 |

In Kogen's run logs, the review and verification phases together average about 37 s, alongside a 43 s mean whole-cell gap. Review input accounts for about half of Kogen's uncached input. These observations do not isolate the cause of the gap.

## Method

- **Tasks:** the earlier scoreboards use 13 short Go tasks; the evening sections state their task and repetition counts. Tasks are graded by hidden tests omitted from the prompt and initial workspace. A grade reports final-tree test success; missing evaluations and evaluator setup failures are ungraded.
- **Prompt:** every bare harness received one prompt containing the request, the acceptance scenarios, the check commands and the protected paths. Kogen pipeline arms received the same acceptance scenarios as an Intent.
- **Isolation:** each attempt ran in a fresh Git workspace with a 3,600-second deadline. The same hidden tests graded the final tree after the agent exited.
- **Pairing:** match arms by task and repetition, then average matched repetitions within each task for task-level comparisons. Whole-cell wall time includes setup and failed attempts but excludes hidden-test grading. Shared machine load and different provider routes limit timing comparisons.
- **Client versions:**
  - Codex CLI 0.165.0-alpha.1.2 and 0.165.0;
  - Pi 0.73.1 and OpenCode 1.19.5;
  - Claude Code 2.1.312;
  - Kogen at commit 16102c97, vendoring kogen-loop e5054c8, and kogen-loop b8a4046 (from Kogen 8ee463f8);
  - the lanes harness at 7a0e22ad.

## Limits

- The tasks are short and pass rates are near the ceiling. These results say little about pass on harder work.
- Kogen's pipeline does more than a bare agent (checks and an independent review), so its time and cost cover more work.
- Isolation of the hidden tests was checked by scanning each agent's event stream. The scan found no suspects, but it is not a proof.
- The Codex CLI build was an alpha bundled with a desktop app.
- The study does not support claims about any model or product beyond this task set and setup.

## Next

Hill-climbs on both scoreboards are running as patch lanes. The patches cover review that resumes the build session, deferred and parallel checks, effort scheduling, context management, reading and tool use. Winning patches will be built into Kogen and kogen-loop, and this page will be updated.
