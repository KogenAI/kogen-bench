# Head-to-head: agent harnesses on short Go tasks (30 October 2026)

Status: DESCRIPTIVE. These are baselines for a hill-climb, not a pre-registered test.

**Correction, 29 October 2026.** An attempt without an evaluation was counted as a failed test, and missing usage was included as zero in some per-pass figures. The table now separates ungraded attempts and withholds totals when usage is missing. Comparisons retain every task and repetition. Passing tests describes the final code, separately from whether the agent completed cleanly.

**Configuration note, 29 October 2026.** In the earlier rounds under Scoreboards 1 and 2, kogen-loop ran with a one-line system instruction set by the test harness instead of its own built-in default instruction, while Codex CLI, Claude Code, Pi and OpenCode each ran with their own built-in instructions. The evening rounds below run kogen-loop with its shipped default instructions, the same way the other harnesses run.

This study compares coding-agent harnesses that get the same task and the same model. It has two scoreboards:

1. **Harness against harness.** The kogen-loop harness, run bare, against Codex CLI and Claude Code. Each harness receives the same single prompt.
2. **Kogen's pipeline against a bare agent.** Kogen adds an Intent (its written statement of what the change must do, with acceptance scenarios), its own checks and an independent review. Each pipeline setup is compared with a bare agent on the same model.

## Eight tasks, both tools on the same OpenAI API key, 30 October 2026

**Summary.** On eight Go tasks, kogen-loop and Codex CLI both passed 8/8 at medium effort and 8/8 at high effort. At medium effort, kogen-loop cost **40% less per pass** ($0.1020 against $0.1698) and was cheaper on all 8 tasks (two-sided sign test p = 0.0078). Its agent wall was lower on 7 of 8 tasks, which does not reach significance (p = 0.0703). At high effort, no difference in cost or wall time was resolved on these eight tasks; a later test on 14 fresh tasks at high effort did resolve one: kogen-loop cost **about 17% less per pass** than Codex CLI ($0.0876 against $0.1053, cheaper on 13 of 14 tasks, p = 0.0018), with wall time tied (see "Fourteen fresh tasks" below). This is one run per task and tool, on tasks chosen for this comparison; it is evidence about these eight tasks, not a general result.

**Setup.** Both tools used the same OpenAI API key, the same model (gpt-6.1-terra) and the same effort within each comparison: kogen-loop b8a4046 with its shipped default instructions, and Codex CLI 0.165.0 with its own. kogen-loop reached the API through an adapter that translates its requests; Codex called the API directly. That adapter is part of what was measured. Each run had a fresh workspace, ran alone on one machine with grading included, and followed a balanced, shuffled order of tasks and tools. Every task was admitted only after its reference solution passed all hidden tests and every available wrong solution failed at least one. All responses reported the requested model and effort.

**Reruns.** Four Codex runs (one at medium, three at high) were first stopped early by a spending guard in the test harness. A further two reruns at high effort were stopped by a request-size limit in the harness, not by the provider. Both limits were removed and those Codex runs were repeated with the same task, prompt, model, effort and Codex release; every repeat finished cleanly and passed. The tables below use the repeats. They ran later than the original order, so provider or cache changes in between can affect those values. The replaced runs remain in the spending record.

### gpt-6.1-terra, medium effort, 8 tasks, one run per task and tool

| Tool | Passed | Median agent wall | Slowest agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 118.6 s | 347.1 s | $0.1020 |
| Codex CLI | 8/8 | 133.4 s | 383.3 s | $0.1698 |

### gpt-6.1-terra, high effort, 8 tasks, one run per task and tool

| Tool | Passed | Median agent wall | Slowest agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 200.3 s | 577.9 s | $0.2188 |
| Codex CLI | 8/8 | 200.4 s | 465.2 s | $0.2266 |

### Task by task, gpt-6.1-terra (kogen-loop / Codex CLI)

| Effort | Task | Passed | Agent wall | API cost |
|---|---|---|---:|---:|
| medium | `logq-go` | yes / yes | 83.5 / 134.5 s | $0.0589 / $0.1139 |
| medium | `sh-globopts-go` | yes / yes | 263.6 / 297.5 s | $0.1750 / $0.2986 |
| medium | `expr-match-go` | yes / yes | 347.1 / 383.3 s | $0.2431 / $0.3520 |
| medium | `goldmark-callouts-go` | yes / yes | 141.0 / 240.8 s | $0.1019 / $0.2294 |
| medium | `inventory-go` | yes / yes | 130.3 / 132.2 s | $0.0769 / $0.1110 |
| medium | `ledger-go` | yes / yes | 75.6 / 87.9 s | $0.0384 / $0.0644 |
| medium | `heatcal-go` | yes / yes | 94.8 / 132.4 s | $0.0495 / $0.0904 |
| medium | `sync3-go` | yes / yes | 106.9 / 98.5 s | $0.0719 / $0.0987 |
| high | `logq-go` | yes / yes | 195.0 / 185.4 s | $0.1290 / $0.1498 |
| high | `sh-globopts-go` | yes / yes | 437.8 / 421.2 s | $0.4018 / $0.3996 |
| high | `expr-match-go` | yes / yes | 577.9 / 465.2 s | $0.5632 / $0.4291 |
| high | `goldmark-callouts-go` | yes / yes | 364.0 / 331.0 s | $0.2960 / $0.3218 |
| high | `inventory-go` | yes / yes | 201.2 / 215.4 s | $0.1143 / $0.1820 |
| high | `ledger-go` | yes / yes | 105.7 / 102.0 s | $0.0539 / $0.0786 |
| high | `heatcal-go` | yes / yes | 129.7 / 173.8 s | $0.0710 / $0.1387 |
| high | `sync3-go` | yes / yes | 199.4 / 140.1 s | $0.1211 / $0.1129 |

**Comparisons, same model and same effort.** Exact two-sided sign tests over the 8 tasks; no task tied on any of these measures.

- **Medium:** kogen-loop cost less on 8/8 tasks (p = 0.0078); total cost ratio 0.600, so 39.95% lower per pass. Wall was lower on 7/8 (p = 0.0703); mean-wall ratio 0.825. Pass: no task differed (p = 1).
- **High:** kogen-loop cost less on 5/8 tasks (p = 0.727); cost ratio 0.966. Wall was lower on 2/8 (p = 0.289); mean-wall ratio 1.087. Pass: no task differed (p = 1). On 14 fresh tasks at high effort, kogen-loop later cost about 17% less per pass (13 of 14 tasks, p = 0.0018); see "Fourteen fresh tasks" below.

The p-values are not adjusted for the several comparisons. The tasks are inherited from earlier rounds and are not claimed fresh or representative. With one run per task and tool, variation within a task cannot be estimated. Equal pass counts do not show equal reliability. Agent wall includes API transport and tool use but excludes setup and grading; "slowest" is the largest of the eight runs. API cost prices the usage the provider reported at list prices (uncached input $1 per million tokens, cached input $0.05, cache writes $1.25, output $5, with the provider's higher rate for requests above 272,000 input tokens); it is an estimate, not an invoice. Cost per pass divides the summed cost of the eight runs in each table by their passes; the replaced runs are left out of it.

## Evening rounds, 29 October 2026

Within these evening rounds, the strongest evidence comes from both tools on the same OpenAI API key at high effort: **both harnesses passed 8/8**, with median agent wall of **117.4 s for Codex CLI and 139.8 s for kogen-loop**. Codex had lower mean agent wall on all four tasks. Cost per pass was effectively tied at about **$0.09 each**. These are descriptive results from four tasks, not evidence of a general winner.

kogen-loop now uses its shipped default instructions in all of these evening rounds, including the experimental speed patch. Every comparison below keeps the model and effort the same within the comparison.

### Same OpenAI API key, gpt-6.1-terra, high effort

Four Go tasks ran twice per tool. Both harnesses used the same API endpoint, model and effort, with an enforced read boundary, one run at a time and balanced execution order. Loop used a protocol adapter; Codex used the endpoint directly, so client and adapter behavior remain part of the measured setup.

| Tool | Passed | Median agent wall | 90th percentile agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 139.8 s | 257.9 s | $0.0913 |
| Codex CLI | 8/8 | 117.4 s | 154.7 s | $0.0917 |

The four task pass comparisons all tied (one-sided sign p = 1). Codex had lower task-mean agent wall on 4/4 tasks (two-sided sign p = 0.125). The loop/Codex cost-per-pass ratio was 0.995. With only four task clusters, neither timing nor cost establishes superiority or equivalence.

Agent wall includes API transport and tools, but excludes setup and grading. API dollar figures use recorded upstream usage and the run's fixed rates, including cache writes; they are estimates, not invoices or subscription prices. Per-pass numerators retain every attempt; trial runs made only to check the setup are excluded.

### Same OpenAI API key, gpt-6.1-terra, medium effort

The completed medium round used the same four tasks, two repetitions, the same API key, endpoint and read boundary, with one run at a time. It also included the speed patch. The tasks had already been used in the high-effort round, so changes between sections cannot be attributed to effort alone.

| Tool | Passed | Median agent wall | 90th percentile agent wall | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 94.0 s | 138.5 s | $0.0563 |
| kogen-loop speed patch | 8/8 | 94.2 s | 177.6 s | $0.0597 |
| Codex CLI | 8/8 | 98.4 s | 113.2 s | $0.0708 |

All four task pass comparisons tied for each loop variant against Codex (one-sided sign p = 1). The default loop had lower task-mean agent wall on 3/4 tasks and the speed patch on 2/4 (two-sided sign p = 0.625 and 1). Each loop variant had lower task cost on 3/4 tasks (two-sided sign p = 0.625). These small-sample differences are descriptive.

## Additional results, 30 October 2026

### Patch short tests on the same OpenAI API key, gpt-6.1-terra, high effort

The four-task medium-effort table above was checked against its per-run records and still matches; it is not repeated here. Two short high-effort tests also had both tools on the same OpenAI API key. Each covered four tasks with one run per setup. Every setup passed 4/4 in both tests. The first included the unpatched loop; the second compared API changes with the speed patch.

#### Same OpenAI API key — gpt-6.1-terra, high effort (first short test)

| Tool | Passed | API cost per pass |
|---|---:|---:|
| kogen-loop (shipped default) | 4/4 | $0.0963 |
| Speed patch | 4/4 | $0.1217 |
| Replay patch | 4/4 | $0.1016 |
| Batch patch | 4/4 | $0.0947 |
| Answer-end patch | 4/4 | $0.1012 |
| HTTP/2 patch | 4/4 | $0.0907 |
| Connection-reuse patch | 4/4 | $0.0866 |

#### Same OpenAI API key — gpt-6.1-terra, high effort (second short test)

| Tool | Passed | Median API cost per pass |
|---|---:|---:|
| Speed patch | 4/4 | $0.0665 |
| Replay patch | 4/4 | $0.0826 |
| Batch patch | 4/4 | $0.0658 |
| Answer-end patch | 4/4 | $0.0806 |

These four-task short tests are descriptive. No patch showed a reliable improvement over the unpatched loop beyond noise; the second test compared API changes with the speed patch, and task-level results were mixed.

### Subscription route, gpt-6.1-terra, medium effort (first completed run)

| Tool | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 23/24 | 26,394 |
| Speed patch | 23/24 | 27,886 |
| Codex CLI | 24/24 | 63,968 |

### Subscription route, gpt-6.1-terra, medium effort (later completed run)

| Tool | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 22/23 graded | missing |
| Codex CLI | 24/24 | 64,717 |

One loop attempt was ungraded and lacked usage, so its cost proxy is missing. A keyword search of the Codex record was traced to the task repository's ignore rule naming its protected evaluation folder; the recorded command did not open that folder.

### Subscription route, gpt-6.1-terra, high effort (patch short test)

| Tool | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| Speed patch | 23/24 | missing |
| Replay patch | 22/24 | missing |
| Batch patch | 23/24 | 36,703 |
| Answer-end patch | 23/24 | 33,512 |
| Connection-reuse patch | 23/24 | missing |
| HTTP/2 patch | 22/24 | missing |

### Subscription route, gpt-6.1-terra, high effort (harness short test)

| Tool | Passed | Cost proxy per pass, tokens |
|---|---:|---:|
| kogen-loop (shipped default) | 22/24 | missing |
| Speed patch | 23/24 | 34,563 |
| Pi | 22/24 | missing |
| OpenCode | 23/24 | missing |

These subscription tables report pass and cost only. Cost is uncached input + 0.1 × cached input + 4 × output, divided by passes across all attempts. It is an uncached-equivalent token proxy, not a dollar cost or subscription charge. Missing usage stays missing. The completed same-effort pairings had few pass differences; they do not establish a harness or patch advantage.

**Wall-time method from 30 October.** Loop-versus-Codex wall time is measured only on two dedicated cloud machines, with the tools interleaved one run at a time on the same task. Laptop and desktop runs report pass and cost only. Earlier wall-time figures from these machines are descriptive.

**Route finding.** Loop and Codex reach the model through different endpoints and sign-in clients. Across 496 earlier runs on two Macs, loop's measured output rate on the same tasks and with similar output counts fell from about 110 to about 48 tokens per second from about 04:00 UTC on 30 October, while Codex wall times stayed about the same. We did not find the cause. The loop program was the same during the slowdown, so a time-of-day or provider-side effect is possible, but this is unconfirmed and cannot be separated from the tools on those machines. It was no longer visible at 11:59 UTC, when a single same-machine test found loop's route and Codex's route streaming at the same rate, about 40–44 tokens per second on three machines ([routes and clients](routes-and-clients.md)). Wall-time differences between loop and Codex from the overnight subscription runs should not be read as tool differences.

**Correction, 30 October 2026.** This paragraph earlier cited small route probes of about 45 against 81 tokens per second as evidence of a route speed gap. Those were three short requests per route on one machine at one time. The larger same-machine test did not reproduce them, so they are no longer cited.

**Tool-use observation.** On tasks both passed, loop ran fewer shell commands and read back less tool output than Codex; it did not run more or wider tests.

### Broader corpus, different subscription routes, gpt-6.1-terra, high effort

This round used 24 Go tasks, one repetition per tool, at each effort. The two harnesses reached the model through different subscription routes, which can affect speed and token accounting. The tables therefore describe the observed combinations of harness and route.

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost proxy per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/24 | 74.5 s | 144.8 s | 16,481 | 82,763 | 80.1% | 3,465 | 36,971 |
| kogen-loop speed patch | 24/24 | 78.1 s | 147.2 s | 15,497 | 83,406 | 81.4% | 3,306 | 35,513 |
| Codex CLI | 23/24 | 72.4 s | 149.6 s | 24,887 | 341,721 | 92.7% | 4,843 | 75,941 |

Paired against Codex CLI, the default loop had 1 task pass win, 1 loss and 22 ties (one-sided sign p = 0.75); the speed patch had 1 win, 0 losses and 23 ties (p = 0.5). The median paired wall change was +5.0% for the default loop and +7.2% for the speed patch (two-sided timing sign p = 0.839 and 0.541). These descriptive differences do not establish a pass or speed advantage.

The cost proxy is uncached input + 0.1 × cached input + 4 × output, summed over all attempts and divided by passes. It is not a dollar cost or a subscription charge. Route-dependent token accounting prevents attributing its differences to the harness alone. Wall in this and the following tables is whole-run time, including setup and failed attempts but excluding hidden-test grading.

### Broader corpus, different subscription routes, gpt-6.1-terra, medium effort

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost proxy per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/24 | 62.2 s | 88.1 s | 13,411 | 46,808 | 71.3% | 2,541 | 26,914 |
| kogen-loop speed patch | 23/24 | 59.4 s | 91.2 s | 12,506 | 50,527 | 75.2% | 2,640 | 26,868 |
| Codex CLI | 22/24 | 58.7 s | 104.6 s | 21,594 | 291,645 | 92.6% | 4,018 | 64,673 |

Each loop variant had 2 task pass wins, 1 loss and 21 ties against Codex CLI (one-sided sign p = 0.5). The median paired wall change was −5.2% for the default loop and −5.3% for the speed patch (two-sided timing sign p = 0.541 and 0.064). These are descriptive observations within medium effort; they do not establish a pass or speed advantage.

### Subscription route, 24 tasks, same model and effort, gpt-6.1-terra, medium and high effort

**Summary.** On 24 Go tasks, kogen-loop and Codex CLI both passed every run at both efforts (24/24 each). kogen-loop used about 40% of Codex CLI's equivalent tokens per pass and used fewer on all 24 tasks at both efforts. Its wall time was 25–30% longer, but the two tools reached the model through different subscription routes, so the wall difference cannot be attributed to the tool. These runs took place between 08:13 and 11:00 UTC; the two routes' speeds were not compared directly during that window. This is one run per task and tool, so the sign tests are descriptive.

**Setup.** Route: subscription, with each tool using its own route. Model: gpt-6.1-terra. Each comparison pairs the two tools at the same effort (medium with medium, high with high). The tools alternated task by task on one cloud machine, one run at a time. All 96 runs were observed, with no setup failures.

#### Subscription route, gpt-6.1-terra, medium and high effort: pass and wall (24 tasks, one run per task and tool)

| Effort | Tool | Passed | Median wall | Median paired wall change, kogen-loop against Codex CLI | Tasks with lower wall, kogen-loop / Codex CLI (two-sided sign test) |
|---|---|---:|---:|---:|---|
| medium | kogen-loop (shipped default) | 24/24 | 81.2 s | +29.5% | 3 / 21 (p = 0.0003) |
| medium | Codex CLI | 24/24 | 66.9 s | | |
| high | kogen-loop (shipped default) | 24/24 | 101.4 s | +24.7% | 4 / 20 (p = 0.0015) |
| high | Codex CLI | 24/24 | 77.8 s | | |

**Wall time is route-confounded.** The sign-test p-values above describe the observed gap between the two route-and-tool combinations. They do not show that kogen-loop is slower.

#### Subscription route, gpt-6.1-terra, medium and high effort: tokens per pass (24 tasks, one run per task and tool)

| Effort | Tool | Equivalent tokens per pass | Uncached input per pass | Tasks with fewer equivalent tokens, kogen-loop / Codex CLI (two-sided sign test) |
|---|---|---:|---:|---|
| medium | kogen-loop (shipped default) | 32,697 | 15,493 | 24 / 0 (p < 0.0001) |
| medium | Codex CLI | 84,035 | 34,826 | |
| high | kogen-loop (shipped default) | 40,747 | 19,849 | 24 / 0 (p < 0.0001) |
| high | Codex CLI | 96,476 | 34,157 | |

Equivalent tokens are uncached input + 0.1 × cached input + 4 × output, divided by passes. They are a token proxy, not a dollar cost or a subscription charge; no dollar figures exist on this route. The median per-task change in equivalent tokens was −58.7% at medium and −60.2% at high. On uncached input alone, kogen-loop used fewer on 22 of 24 tasks at medium and 18 of 24 at high. Token accounting can differ by route, so treat the token comparison as less affected by the route than wall time, but still not a clean tool comparison.

### Subscription route probe, gpt-6.1-terra, medium effort

**Summary.** We looked for a faster route that kogen-loop could reach with its own sign-in and an honest client label, and found none: every variant streamed at about 54 tokens per second. This probe measured kogen-loop's route only. This is a small probe and it is descriptive.

**Correction, 30 October 2026.** This summary earlier said the slower wall time above looked like a fixed pace on kogen-loop's route. About two hours after this probe, a same-machine test found kogen-loop's route and Codex CLI's route streaming at the same rate, so this probe does not show that kogen-loop's route is slower ([routes and clients](routes-and-clients.md)).

**Setup.** Route: subscription sign-in used by kogen-loop. Model: gpt-6.1-terra, medium effort, no tools, the same prompt each time (343 output tokens, no reasoning tokens in every successful response). Each variant ran 10 paired requests against the current setup, alternating order, with a fresh session on every request. No other tool's client identity or credentials were used.

| Variant (gpt-6.1-terra, medium effort) | Streaming rate, median [IQR], tokens/s | Same-block current setup, tokens/s |
|---|---:|---:|
| Same endpoint, honest client label | 53.3 [51.6, 54.5] | 54.0 [53.7, 54.1] |
| Persistent WebSocket connection, honest client label | 54.3 [54.0, 54.9] | 53.6 [52.8, 54.3] |
| Subscription endpoint used by Codex CLI | refused (HTTP 401) on a single check; not retried | |

Rates are measured from the first generated text to the last byte. The WebSocket variant started producing text about 0.6 s sooner (1.86 s against 2.47 s median), which is a connection effect, not a faster stream. Neither variant reached the pre-set bar of 1.5× the median rate with non-overlapping interquartile ranges. The rate was nearly constant across 40 requests. Subscription wall comparisons should still be read by route and time period.

### Write-check patch short test, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** A patch that lets kogen-loop's file-write tool carry a known follow-up check did not change behaviour: the model never used the new option in the first three runs where it could, so the test was stopped and the patch does not advance. Every completed run passed. The comparisons below describe these runs only and do not estimate the patch's effect when it is used.

**Setup.** Route: both tools on the same OpenAI API key. Model: gpt-6.1-terra, high effort. Tasks ran one run per task and setup in a fixed order, and the test stopped after three tasks. Codex CLI had completed only the first two tasks when it stopped, so its row covers those two. The rebuilt unpatched baseline did not match the checksum recorded for the earlier build, so the baseline comparison is approximate.

| Setup (gpt-6.1-terra, high effort) | Passed | Median wall | Median model requests | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 3/3 | 380.5 s | 36 | $0.2203 |
| kogen-loop with write-check patch | 3/3 | 514.0 s | 54 | $0.3481 |
| Codex CLI (2 tasks) | 2/2 | 320.9 s | 38.5 | $0.3291 |

Against the unpatched loop, the patch had lower wall on 0 of 3 tasks, with higher output tokens and cost on all three (two-sided sign test p = 0.25 on 3 tasks, one run per task and tool). Passes tied on every task. With three tasks the sign test cannot resolve small differences, and the order and timing of single runs may also matter. The patch's new option was used in 0 of 3 runs. We did not test why the patched runs cost more, so the cause is unconfirmed; this table does not show that the patch helps or hurts.

### Reasoning replay, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** We tested whether carrying the model's earlier reasoning back to it between turns closes the reasoning gap described on the kogen-vs-codex page. On 8 Go tasks, all three setups passed every run. kogen-loop with reasoning carried back used the fewest requests and the lowest cost per pass in total, but more reasoning tokens than the default loop, and task by task it was cheaper than the default loop on only 3 of 8 tasks, so the hypothesis is not supported as stated. No difference is resolved by the per-task sign tests. This is one run per task and setup, so it is descriptive.

**Setup.** Route: both tools on the same OpenAI API key. Model: gpt-6.1-terra, high effort. Each task ran once per setup, with the setups interleaved task by task. Figures are per pass over the 8 tasks.

| Setup (gpt-6.1-terra, high effort) | Passed | Model requests | Reasoning tokens | API cost | Wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 32.2 | 2,727 | $0.225 | 296 s |
| kogen-loop with reasoning carried back | 8/8 | 20.2 | 4,117 | $0.175 | 268 s |
| Codex CLI | 8/8 | 28.8 | 4,152 | $0.236 | 273 s |

Reasoning carried back against the shipped default, task by task: cost lower on 3 tasks and higher on 5 (two-sided sign test p = 0.727); requests lower on 3, higher on 4 and tied on 1 (p = 1.0); reasoning tokens higher on 6 of 8 tasks (p = 0.289). The lower totals come mostly from one slow run of the shipped default on one task (90 requests, $0.649, 708 s); without it the per-pass gaps shrink, which is why a larger test on fresh tasks followed (next section). Against Codex CLI: requests lower on 6, higher on 1 and tied on 1 (p = 0.125); cost lower on 6 and higher on 2 (p = 0.289). With 8 tasks the sign tests cannot resolve differences of this size, so the question stays open.

### Fourteen fresh tasks, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** We re-ran the reasoning replay question on 14 Go tasks that no earlier round had used, with the sample size fixed in advance. All 42 runs passed. At high effort, kogen-loop's shipped default cost **about 17% less per pass** than Codex CLI ($0.0876 against $0.1053) and was cheaper on 13 of the 14 tasks (two-sided sign test p = 0.0018). This replaces the eight-task result above, where no cost difference was resolved at high effort. Wall time was tied. Carrying reasoning back to the model made no difference to cost against the shipped default (ratio 0.998, cheaper on 4 of 14 tasks, p = 0.18), so that change does not advance.

**Setup.** Route: both tools on the same OpenAI API key. Model: gpt-6.1-terra, high effort. Each of the 14 tasks ran once per setup, with the three setups interleaved task by task and the starting setup rotated from task to task. A short dry run on one earlier task, outside the counts, checked beforehand that all three setups ran and that reasoning was carried back. The 14 was set before any run from the spread seen in the 8-task round above; at that size the test could only resolve a large difference. Figures are per pass over the 14 tasks.

| Setup (gpt-6.1-terra, high effort) | Passed | API cost per pass | Model requests per run | Reasoning tokens per pass | Median wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 14/14 | $0.0876 | 13.2 | 2,432 | 115 s |
| kogen-loop with reasoning carried back | 14/14 | $0.0874 | 14.0 | 2,468 | 131 s |
| Codex CLI | 14/14 | $0.1053 | 14.1 | 2,157 | 112 s |

Paired by task (exact two-sided sign tests, ties dropped; first setup lower on x tasks and higher on y). kogen-loop default against Codex CLI: cost 13 and 1 (p = 0.0018); requests 8 and 4 with 2 tied (p = 0.39); wall 5 and 9 (p = 0.42); reasoning tokens 4 and 10 (p = 0.18). Reasoning carried back against the shipped default: cost 4 and 10 (p = 0.18); requests 3 and 9 with 2 tied (p = 0.15); wall 4 and 10 (p = 0.18); reasoning tokens 9 and 5 (p = 0.42). Reasoning carried back against Codex CLI: cost 13 and 1 (p = 0.0018), but wall 2 and 12 (p = 0.013).

**Limits.** One run per task and setup, so these are descriptive of these 14 tasks. The tasks are short Go tasks; one of them cost several times as much as the others. The setup order within a task was rotated, not randomised. The reasoning comparison cannot show that the two kogen-loop setups are equal, only that no advantage appeared. Reproduction pack: `reproduce/replayconf-14task-high/`.

### Batch and exec tools, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** We tried two ways of letting kogen-loop do several operations in one model request: a `batch` tool (a list of reads, searches and commands, run together) and an `exec` tool (the model writes one script that calls the other tools). On 4 fresh Go tasks, `batch` was used in every run and roughly doubled operations per request (1.9 to 3.2). It cost the same per pass as the default loop and was cheaper than Codex CLI on all 4 tasks. `exec` passed 2 of 4 and cost about six times as much per pass, so it does not advance. With 4 tasks, no difference is resolved: this is descriptive. The 12-task confirmation below replaces this short test's open question.

**Setup.** Both tools used the same OpenAI API key; model gpt-6.1-terra, high effort; one run per task and tool, with the tools interleaved task by task. The tasks were not used in earlier rounds. The default loop was rebuilt with the same toolchain as the two patched builds.

| Tool (gpt-6.1-terra, high effort) | Passed | API cost per pass | Model requests | Operations per request | Median wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 4/4 | $0.181 | 91 | 1.9 | 274 s |
| kogen-loop with `batch` | 4/4 | $0.185 | 83 | 3.2 | 259 s |
| kogen-loop with `exec` | 2/4 | $1.13 | 95 | 2.5 | 1043 s |
| Codex CLI | 4/4 | $0.239 | 114 | 1.4 | 276 s |

Paired by task (exact two-sided sign tests; the smallest possible p with 4 tasks is 0.125). `batch` against the default loop: operations per request higher on 4 of 4 tasks (p = 0.125); requests lower on 3 (p = 0.625); cost higher on 3 (p = 0.625); wall lower on 3 (p = 0.625). `batch` against Codex CLI: cost lower on 4 of 4 tasks (p = 0.125); requests lower on 3 (p = 0.625). `exec` against the default loop: cost and wall higher on 4 of 4 (p = 0.125).

**Why `exec` was stopped.** In two of its four runs, about five normal requests in, one model response ran to the 128,000-token output cap with only about 300 reasoning tokens, and the loop gave up after 25 to 30 minutes. No other tool had this in 12 runs. This `exec` sends its script as a JSON string argument; Codex's own tool sends raw JavaScript, and whether that difference causes the runaway was not tested. Both candidates were used (`batch` in 4 of 4 runs; `exec` is the only file and shell tool, so its use is automatic), so the stop rule did not fire.

**What is not separated.** Each patch also adds one sentence about batching to the loop's default instructions, so the tool and the sentence are not separated. There is one run per task, the default loop is a same-toolchain rebuild, not the earlier recorded binary, and one `exec` run's cost is counted at its upper bound because usage was not reported. Reproduction pack: `reproduce/batch-tool-short-test/`.

### Batch tool confirmation, 12 tasks, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** The 12-task confirmation replaces the short test's open question ("a larger confirmation is running"). The `batch` tool does what it was built to do: kogen-loop packs more operations into each model request (2.56 against 1.74 for the default loop, higher on 12 of 12 tasks, p < 0.001). But the number of requests and the cost per pass did not change against the default loop: cost per pass $0.1085 against $0.1101 (p = 0.39) and 184 requests against 191 (p = 1.0). **Does not advance:** the tool is neutral for cost and speed, not harmful, and is not adopted for either. Adding only the batching sentence without the tool did not lower requests either.

**Setup.** One run per task and setup, 48 runs: 12 fresh Go tasks (the count was fixed before any run) times four setups, all on the same OpenAI API key, model gpt-6.1-terra, high effort. The setups were the default kogen-loop, kogen-loop with only the batching sentence added to its instructions and no tool, kogen-loop with the `batch` tool (which also carries that sentence), and Codex CLI. Inside each task the four setups ran in an order rotated by task, one run at a time including grading by the task's hidden tests. The sentence used here says "one call" instead of "one batch call", because that setup has no `batch` tool to name. The three loop builds were made together with the same toolchain from the short test's base source. The 12 tasks were chosen by a fixed rule from tasks not used in earlier rounds and had to qualify first (the reference solution passes and known-wrong solutions fail). All 48 runs finished; none was cut, replaced or hit a provider fault, and the longest silence from the provider within a request was 23.7 s.

| Tool (gpt-6.1-terra, high effort) | Passed | API cost per pass | Model requests | Operations per request | Median wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 12/12 | $0.1101 | 191 | 1.74 | 164 s |
| kogen-loop with the sentence only | 10/12 | $0.1303 | 197 | 2.04 | 177 s |
| kogen-loop with `batch` | 12/12 | $0.1085 | 184 | 2.56 | 167 s |
| Codex CLI | 12/12 | $0.1420 | 247 | 1.55 | 177 s |

Cost is at API list prices from the gateway's per-request receipts, and per pass means total cost divided by passes. `batch` was used in all 12 of its runs: all 89 of its calls ran two or more operations.

Paired by task (exact two-sided sign tests, ties dropped; each count is tasks where the first setup was lower, then higher). `batch` against the default loop: cost per pass 4/8 (p = 0.39); requests 6/5 with 1 tie (p = 1.0); wall 5/7 (p = 0.77); operations per request 0/12 (p < 0.001). `batch` against the sentence only: cost per pass 7/5 (p = 0.77); requests 6/3 with 3 ties (p = 0.51); operations per request 1/11 (p = 0.006). The sentence only against the default loop: cost per pass 5/7 (p = 0.77); requests 6/4 with 2 ties (p = 0.75); operations per request 2/10 (p = 0.039). The sentence-only setup failed two tasks on the hidden tests, against none for the others; two failures out of 12 are not a significant difference from none (p = 0.5).

**Against Codex CLI.** The default loop and `batch` each cost less per pass than Codex CLI on 11 of 12 tasks (p = 0.006); the sentence-only setup on 9 of 12 (p = 0.15). Requests were lower than Codex CLI on 9 of 12 tasks for the default loop (p = 0.15), and 9 against 2 with 1 tie for `batch` (p = 0.065). Median wall was about the same for all four setups, and no wall comparison with Codex CLI was resolved.

**Limits.** The test was sized to resolve a 20% cut in requests: 12 tasks give power of about 0.75 for it, using the spread seen in the short test. The observed request change was about 3%, so a smaller effect cannot be ruled out, only that none was seen at this size. One run per task and setup; the within-task order was rotated, not randomised. The tool and its instruction sentence are not separated in the `batch` setup. The sentence-only setup shows the sentence alone does not lower requests, but it does not separate the two in a setup that has both. The loop builds were made again from the short test's source, so their hashes differ from the short test's builds only through an embedded source path. The 12 tasks avoid those of the next 14-task test by prediction from its selection rule, run on copies of its kits; that prediction has not yet been compared with that test's actual selection. Cost is at list prices; one host ran everything. Reproduction pack: `reproduce/batch-tool-confirm-12task/`.

### Low text verbosity, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** **Unresolved: 3 tasks, repeated 6 times each (18 blocks); the effective sample is 3 tasks.** We tested whether asking the model for low text verbosity makes kogen-loop write less. The setting was sent on every request and the provider returned it, but it changed nothing we could resolve: non-reasoning output was lower with it in 9 of 18 blocks and higher in 9 (p = 1.0), and cost per pass was lower in 4 and higher in 8 with 6 ties (p = 0.39). **Does not advance.** The earlier +10% output gap against Codex CLI did not reproduce: on these tasks both kogen-loop setups wrote less non-reasoning output than Codex CLI (14 blocks to 4 and 14 to 3, p = 0.031 and 0.013) and cost 0.70 and 0.75 times as much per pass (p = 0.023 and 0.003), even though Codex CLI also sends low verbosity. These p-values treat the 18 blocks as independent; because the blocks are repeats of 3 tasks, they overstate the evidence.

**Setup.** Three setups on the same OpenAI API key, model gpt-6.1-terra, high effort: kogen-loop with reasoning replay (the control), the same build plus one patch that sends low verbosity, and Codex CLI. There were three fresh Go tasks with 6 repetitions each, 18 blocks and 54 counted runs, after a dry run that checked the setting reached the provider. The count was fixed before any run; only three fresh task kits were left, so the blocks are repeated sessions on the same tasks, not 18 tasks. Inside each block the order of the setups was rotated and one run went at a time, including grading by the task's hidden tests. All 57 runs finished and none was cut or replaced.

| Setup (gpt-6.1-terra, high effort) | Passed | Non-reasoning output per run (tokens) | API cost per pass | Requests per run | Median wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop with reasoning replay | 12/18 | 7,016 | $0.140 | 15.2 | 125 s |
| the same with low verbosity | 12/18 | 6,688 | $0.131 | 13.9 | 129 s |
| Codex CLI | 13/18 | 8,457 | $0.187 | 18.6 | 121 s |

Paired by block (exact two-sided sign tests, ties dropped; each count is blocks where the first setup was lower, then higher). Low verbosity against the control: non-reasoning output 9/9 (p = 1.0), cost per pass 4/8 with 6 ties (p = 0.39), wall 9/9 (p = 1.0), requests 8/8 with 2 ties (p = 1.0). Low verbosity against Codex CLI: output 14/4 (p = 0.031), cost per pass 11/2 with 5 ties (p = 0.023), wall 11/7 (p = 0.48). The control against Codex CLI: output 14/3 with 1 tie (p = 0.013), cost per pass 12/1 with 5 ties (p = 0.003), wall 11/7 (p = 0.48). Neither loop setup wrote a final answer message in any run, against 193 bytes per run for Codex CLI, so there was little prose for the setting to shorten.

**The task that failed in every loop run.** One task, `revive-baseline-go`, failed in all 12 loop runs and passed in 1 of 6 Codex CLI runs (p = 0.33). Earlier rounds lost runs on this task on Linux because one copy of its kit has two fixture directories that differ only in case and cannot coexist on a case-insensitive disk. That does not apply here: this round used the copy that keeps only one of them, and the repository's own tests passed in all 18 runs of the task. Every failed run, in all three setups, failed the same single hidden test; why was not diagnosed. So the task does not separate the two loop setups (both 0 of 6), its cost ratios are costs of failed work, and all of the 6.6% lower cost per pass of the low-verbosity setup comes from it: on the two tasks that passed in every run, low verbosity cost 1.04 and 1.11 times as much as the control. Looking only at those two tasks (a check made after the results, not registered), the cost advantage over Codex CLI holds (11 blocks to 1 and 12 to 0 out of 12), but the output advantage does not (8/4, p = 0.39 and 8/3, p = 0.23).

**Limits.** The test was sized to resolve a 10% cut in non-reasoning output (power about 0.75 for 18 blocks) and could not resolve the 1 to 3% cost change expected, so a small effect cannot be ruled out. Repetitions of one task are not independent tasks. The within-block order was rotated, not randomised. One run was started by hand after the orchestrator's launch was lost, and the orchestrator was later stopped by another job's process; no run was lost, and the 8-minute gap fell between runs. One host ran everything; cost is at list prices. Reproduction pack: `reproduce/verbosity-low-eu6/`.

### Yielding shell, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** **Unresolved (5 pairs): 3 tasks, 16 of 18 planned counted cells, 5 complete task-repetition blocks, nothing significant.** We tested whether a shell that returns control after 30 s with the output so far, and lets the model wait on or stop the command later, removes the long shell waits that cost kogen-loop time on three hard tasks. Against the default shell the yielding shell used 0.26 times the shell seconds (lower in 4 pairs, higher in 1, sign test p = 0.375) and 0.49 times the agent wall (3/2, p = 1.0), with equal passes (4 of 5 each; Codex CLI 6 of 6) and equal cost per pass ($0.56 against $0.55; Codex CLI $1.35). On the shell-bound task the default shell sat in one call until the 3,600 s deadline both times it ran (it passed grading both times), while the yielding shell finished in 1,167 and 741 s with no call over 30 s. The downsides: it was slower on the review-on-demand task, made 1.15 times the requests, and 4 of its 6 cells ended on loop's 512 KB request limit (3 of them after passing).

**Setup.** Three setups on the same OpenAI API key, model gpt-6.1-terra, high effort, on one server: kogen-loop `b8a4046` with its default shell, the same source plus a patch to the shell tool (an experiment build, not a release), and Codex CLI 0.165.0. The tasks were the three of the 22-task head-to-head that had shell tails. The plan was 3 tasks x 2 repetitions x 3 setups, one cell at a time with grading, the starting setup rotated by block, after 3 dry cells. Primary measures were shell seconds and agent wall, paired by task and repetition; shell seconds for the loop setups come from the loop's own event times. The last block was cut by the spend guard: spend was $14.79 of the $15 cap and the guard's per-cell estimate ($0.62) was too low for Codex CLI cells ($1.26 to $2.17). That block (shell-bound, repetition 2) has only its Codex CLI cell, which is in Codex CLI's totals but in no paired test; nothing was imputed. The cut was by budget, not outcome, but it removed a block on the task where the default shell hit the deadline in both earlier loop cells, so the difference may be understated. The design changed once, before any counted cell: the first dry cell (default shell) passed but hit the deadline, which the first protocol treated as an infrastructure stop; deadline timeouts now count as outcomes (wall censored at 3,600 s) and shell timing comes from the loop's event times instead of receive-time stamps. That change was made after seeing that cell. Details in the pack.

| Setup, counted cells | Passed / launched (deadline timeouts) | Shell s, total | Agent wall s, mean / p90 | Requests | API cost per pass |
|---|---:|---:|---:|---:|---:|
| loop default shell | 4/5 (1) | 4,923 | 1,242 / 3,600 | 212 | $0.545 |
| loop yielding shell | 4/5 (0) | 1,266 | 615 / 741 | 243 | $0.561 |
| Codex CLI | 6/6 (0) | 3,610 | 950 / 1,527 | 777 | $1.350 |

Paired by block (5 complete blocks; exact two-sided sign tests, ties dropped; each count is blocks where the first setup was lower, then higher). Yielding against default: shell seconds 4/1 (p = 0.375), wall 3/2 (p = 1.0), cost per pass 1/4 (p = 0.375; pooled equal), requests 2/3 (p = 1.0), pass 1/1 with 3 ties. Yielding against Codex CLI: shell 4/1, wall 3/2 (ratios 0.46 and 0.68), cost 5/0 on USD (p = 0.0625). Shell seconds for Codex CLI are measured differently (command lifetimes stamped on receipt), so those comparisons are looser.

**Where it helps and where it does not.** Shell-bound: default 3,296 and 3,394 shell seconds (longest calls 941 and 1,856 s), yielding 617 and 439 s; Codex CLI on this host also spent 781 to 1,355 s in shell, so the short Codex CLI walls of the earlier round did not reproduce. Review tasks: yielding was faster on review-retry (523 against 774 s and 489 against 862 s) and slower on review-on-demand (625 against 565 s and 697 against 409 s), with about twice the requests there. 20 yields and 16 waits in the counted cells, no stops; some yielded sessions were never waited on. The request limit ended 4 of 6 yielding cells (3 had passed, 1 failed) and 1 of 6 default cells (a fail). Each setup failed one review-retry repetition.

**Limits.** Five pairs over three tasks; the shell-bound tail rests on one counted pair and one dry cell; pairs on one task are not independent. Deadline cells are censored at 3,600 s, so the wall ratio is a floor. One host; cost at list prices; order rotated, not randomised. The task kits stay private until the hill-climb ends. Reproduction pack: `reproduce/shell-yield-eu2/`.

### Patch edit tool, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** **Does not advance: an `apply_patch` edit tool did not reduce the output kogen-loop generates on edit turns (10 blocks: 5 tasks x 2 repetitions, 30 counted cells).** With the tool added, edit-turn output was lower in 3 blocks and higher in 7 (sign test p = 0.34; geometric-mean ratio 0.999 over 9 blocks). The model used the tool in 9 of 10 cells (61 calls, no errors) but made more, smaller edits and more requests (more requests in 9 of 10 blocks, p = 0.02). **Cost per pass is unresolved (4 blocks lower, 6 higher, p = 0.75).** The arm totals favour the tool ($0.164 per pass against $0.220 for the default and $0.194 for Codex CLI), but only because one default-loop cell ran away to the 128,000-token output cap and failed; without that block the tool cost 13% more ($1.51 against $1.34 over 9 passes each, a check made after the results).

**Setup.** Three setups on the same OpenAI API key, model gpt-6.1-terra, high effort, on one server, one cell at a time with grading: kogen-loop `b8a4046` with its default tools, the same source plus a patch that adds an `apply_patch` function tool (an experiment build, not a release), and Codex CLI 0.165.0. The tool takes Codex's patch format and its description is the apply_patch section of Codex's own model instructions; it is offered next to the unchanged `write_file` and shell. Primary measures, registered in advance and paired by task and repetition: output tokens on edit turns (responses with at least one edit call, reasoning included) and cost per pass. The test had power 0.79 for a 30% cut in edit-turn output and almost none for 10%. **No unused task kit was left, so the round reused five kits from earlier rounds** (the same tasks for every setup, but not fresh). 33 runs including 3 dry, $5.75 of the $9.50 cap; no run was cut, rerun or replaced.

| Setup, counted cells | Passed / launched | Edit-turn output per run | Edit turns per run | Requests per run | API cost per pass |
|---|---:|---:|---:|---:|---:|
| loop default | 9/10 | 10,497 | 8.1 | 17.4 | $0.220 |
| loop + apply_patch | 10/10 | 11,701 | 12.3 | 24.8 | $0.164 |
| Codex CLI | 10/10 | 11,865 | 8.6 | 24.7 | $0.194 |

Paired by block (10 blocks; exact two-sided sign tests, ties dropped; each count is blocks where the first setup was lower, then higher). Patch against default: edit-turn output 3/7 (p = 0.34), cost per pass 4/6 (p = 0.75), wall 5/5, requests 1/9 (p = 0.02), pass 1/0 with 9 ties. Patch against Codex CLI: edit-turn output 6/4 (p = 0.75), cost per pass 8/2 (p = 0.11), pass tied. Default against Codex CLI: cost per pass 9/1 (p = 0.02), requests 10/0 (p = 0.002).

**What the result rests on.** loop already edits through the shell on these tasks (70 of the default's 81 edit calls); the tool moved part of that work into patch calls (61 of 123 edit calls in its arm) while `write_file` and shell edits stayed in use, so edits got smaller and more frequent: 113 edit turns against 81 and 228 requests against 172 on the 9 blocks without the failed cell, with edit-turn output the same (105,548 against 104,968 tokens). By task the edit-turn ratio was 0.98, 0.83, 1.04, 1.10 and 1.10; the tool was costlier per pass on three of the five tasks (1.10 to 1.25 times). Both loop setups tie Codex CLI on edit-turn output; the default is cheaper per pass than Codex CLI. The one failed cell was `sync3-go`, repetition 1, default loop: its second request ran to the output cap with no reasoning tokens (`agent_error`, $0.65, 1,411 s), the same failure seen twice in an earlier round's exec arm.

**Limits.** Ten blocks over five tasks; repetitions of one task are not independent, and the tasks had been run before. The test could resolve only a large effect on edit-turn output, so a small effect, and the 3 to 8% cost change the lever was expected to give, cannot be ruled out or confirmed. Cost per pass hinges on one failed cell. The Codex CLI edit classification (shell-text patterns) is descriptive. One host; cost at list prices; order rotated, not randomised. The task kits stay private until the hill-climb ends. Reproduction pack: `reproduce/apply-patch-edit5/`.

### API key versus CLI sign-in, claude-sonnet-5-5, medium effort

This round used 13 Go tasks and two repetitions per tool. Loop used an API key; Claude Code used its own sign-in. These routes can affect speed and token accounting.

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Dollar cost per pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 23/26 | 48.4 s | 77.5 s | 11,486 | 52,498 | 78.1% | 5,617 | missing |
| Claude Code | 21/25 graded; 1 ungraded | 60.5 s | 86.0 s | 12,547 | 97,214 | 87.1% | 6,413 | missing |

One Claude Code attempt failed during setup, before an agent ran, and is ungraded. Its measured wall remains in the all-attempt timing. Pairing retains 25 graded task/repetition pairs across 13 tasks: 22 loop passes versus 21 Claude Code passes, with 1 task pass win, 0 losses and 12 ties (one-sided sign p = 0.5). The pass difference is descriptive. The median paired wall change was −15.5%, with lower loop task-mean wall on 12/13 tasks (two-sided sign p = 0.00342). Different routes prevent interpreting the timing difference as a harness-only advantage. Dollar costs were not recorded for these runs and remain missing.

**Evening method.** Only complete, attested rounds are included. Match attempts by task and repetition, omit pairs with an ungraded attempt, then average matched repetitions within each task. Pass wins and losses compare task pass totals over those matched repetitions; tied tasks are omitted from the exact one-sided sign test for a loop pass advantage. Timing and cost sign tests are exact and two-sided. Each task has equal weight; the median paired change is the median of task-mean ratios minus one. Wall medians and nearest-rank 90th percentiles in tables retain all attempts. Infrastructure failures are ungraded, and missing usage or cost stays missing.

## Scoreboard 1: kogen-loop against other agent harnesses (same model, same prompt)

All harnesses used gpt-6.1-terra with high reasoning effort on the same 13 tasks. Within each batch, the runs of a task ran one after the other on the same machine.

### Four harnesses (2 repetitions per task)

| Harness | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop e5054c8 | 25/26 | 73.2 s | 408.6 s | 11,841 | 29,505 | 59.9% | 2,796 | 24,791 |
| Codex CLI 0.165.0-alpha | 26/26 | 63.3 s | 101.0 s | 17,910 | 158,691 | 88.7% | 3,713 | 46,840 |
| Pi 0.73.1 | 25/25 graded; 1 ungraded | 61.4 s | 105.0 s | missing | missing | missing | missing | missing |
| OpenCode 1.19.5 | 25/26 | 97.5 s | 164.4 s | 25,563 | 172,226 | 85.2% | 4,603 | 58,641 |

\*Cost is in uncached-equivalent tokens: uncached input + 0.1 × cached input + 4 × output. Dollar cost was not recorded for these subscription runs.

kogen-loop had the lowest cost per pass among the harnesses with complete recorded usage. It was 47% below Codex CLI, and also had the lowest uncached input among those harnesses. Pi has usage for only 25 of 26 attempts, so its full per-pass usage and cost are missing. Its median wall was slower than Codex CLI and Pi. A later batch recorded 11 stalls among 153 request attempts, all before any response headers arrived, clustered in time. This later observation does not establish the cause of the earlier batch's long tail. A run of the updated loop (b8a4046) with first-byte timeouts of 90, 30 and 20 seconds saw no such stalls at all. There, all three variants passed 26/26 at a median of 57–58 s.

### Updated loop against Codex CLI in the same batch (1 repetition per task)

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop b8a4046 | 13/13 | 60.4 s | 69.0 s | 9,228 | 26,351 | 65.0% | 2,627 | 21,448 |
| Codex CLI 0.165.0 | 13/13 | 68.3 s | 79.4 s | 17,822 | 172,731 | 89.7% | 3,753 | 48,323 |

In this batch, with no request stalls, the loop was faster than Codex CLI at the median and at the 90th percentile. It also used about half the uncached input, and cost 56% less per pass.

## Scoreboard 2: Kogen's pipeline against bare agents

### Driving Claude Code, against bare Claude Code

Both setups used claude-sonnet-5-5 at medium effort and ran on the same machine, with 2 repetitions per task.

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass† |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 driving Claude Code | 23/26 | 122.5 s | 202.0 s | missing‡ | missing‡ | missing‡ | missing‡ | missing‡ |
| Claude Code 2.1.312 (bare) | 24/26 | 61.9 s | 95.2 s | 11,212 | 88,973 | 87.4% | 5,879 | $0.111 |

†Dollar figures are the list-price estimates that the Claude Code client reports. They are not plan prices.

‡25 of 26 Kogen attempts reported usage and cost. Their known cost sums to $6.730; the full cost per pass is missing.

Kogen's pipeline runs two Claude Code sessions per task: one builds and an independent one reviews. It also runs the project's checks. That explains most of the extra time and cost.

### Driving Claude Code on hard tasks, against Claude Code alone

*Corrected 31 October 2026: on some of these tasks the grader, not the agents, decided the result. See [Hard tasks: grading correction](#hard-tasks-grading-correction).*

Result, 30 October 2026: **unresolved on success (9 task pairs, one run each, all 9 tied); Kogen cost more on 8 of 9 tasks (p = 0.039).** Kogen 8744e67b driving Claude Code and Claude Code 2.1.314 on its own each passed the same 5 of 9 hard tasks (0.56, 95% interval 0.27 to 0.81) and failed the same 4. Both used claude-sonnet-5-5 at medium effort, the same Claude Code binary, one run per task and setup, on one laptop.

The nine tasks are the ones that Codex CLI at high effort had failed at least once, so they are harder than the tasks above. A task passes only when the hidden tests and the public acceptance scenarios all pass on the final tree.

| Setup | Passed | Requests | Output tokens | Cost at list price† | Cost per pass† | Total wall |
|---|---:|---:|---:|---:|---:|---:|
| Kogen driving Claude Code | 5/9 | 278 | 326,970 | $15.30 | $3.06 | 8,471 s |
| Claude Code alone | 5/9 | 243 | 215,009 | $6.31 | $1.26 | 4,979 s |

†Token counts are read from Claude Code's own session records, the same way for both setups; dollars are those tokens at Anthropic list prices, not plan prices. The test harness recorded no requests, tokens or cost for the Kogen setup, so these figures come from that separate reading rather than the harness's tables.

Paired by task, there is no task on which the two setups differ, so the exact sign test on success has nothing to count (9 ties, p = 1). On cost Kogen was higher on 8 tasks and lower on 1 (p = 0.039); on wall time the same split (p = 0.039); on requests it was higher on 6 and lower on 2, with 1 tie (p = 0.29). The one task where Kogen was cheaper and faster was `revive-baseline-go`, where its start-up check refused to build because one of the project's own tests was already failing, so it made no change; the setup alone also failed that task (99 of 962 tests passed against 0).

The test harness's own report table shows 0 of 9 for Claude Code alone. That is a labelling error in the report, not a result: it counts only builds that Kogen calls "landed", and files every cell of the other setup as a workflow failure. The grades themselves are the 5 of 9 shown above.

Limits: one run per task and setup, so nine pairs; an edge of a task or two could not show. The tasks were chosen because another agent failed them, and six of the nine come from Kogen's own code. One laptop, one model, one effort. Kogen's executor also ran Claude Code 2.1.314, a version that broke Kogen's executor hooks in other runs. Here every logged hook decision was a normal observation and no hook error appeared, but in two Kogen cells (`kogen-review-on-demand` and `kogen-review-retry`) the session record names one more shell call than the hook log holds (21 against 20 and 49 against 48), which is not explained. A later block pins Claude Code 2.1.312 for comparison. Kogen's time and cost cover shaping, an independent review and checks that a single run does not do. The task kits stay private until the hill-climb is done. Numbers, task list, per-run rows and the script that reproduces them: [`reproduce/ccs3-lm-hard-tasks/`](../reproduce/ccs3-lm-hard-tasks/README.md).

### Hard tasks: Kogen driving Codex, against Codex CLI alone

*Corrected 31 October 2026: on some of these tasks the grader, not the agents, decided the result. See [Hard tasks: grading correction](#hard-tasks-grading-correction).*

Result, 30 October 2026: **unresolved on success (9 task pairs on the laptop, 6 on the MacBook, one run each).** Kogen 18895e65 driving Codex and Codex CLI 0.166.0 on its own, both with gpt-6.1-terra at high effort, one run per task and setup. The laptop block ran 9 hard tasks and each setup passed the same 3 (0.33, 95% interval 0.12 to 0.65). The MacBook block ran 6 of those tasks and each setup passed 2 (0.33, 0.10 to 0.70), but not the same two: only Kogen passed `goose-labels-go` and `revive-baseline-go`, and only Codex alone passed `kogen-review-on-demand` and `tally-periodic-go`.

| Block | Tasks | Kogen passed | Codex alone passed | Paired test | Fisher | Wall, both measured |
|---|---:|---:|---:|---|---|---|
| Laptop | 9 | 3 | 3 | 0 discordant tasks, p = 1 | p = 1 | Kogen 7,064 s, Codex 2,728 s (8 tasks; Kogen slower on all, p = 0.0078) |
| MacBook | 6 | 2 | 2 | 2 against 2 discordant, p = 1 | p = 1 | Kogen 7,368 s, Codex 1,515 s (5 tasks; Kogen slower on all, p = 0.0625) |

The registered analysis pools the two blocks per task: Kogen's mean pass rate is higher on 2 tasks, lower on 2 and equal on 5 (mean difference 0, one-sided sign test p = 0.69). On `goose-labels-go` Codex alone was stopped at the memory cap in both blocks before it produced a final tree, so it is counted as a fail; leaving that task out does not change the picture (laptop 3 of 8 each; MacBook Kogen 1 of 5, Codex 2 of 5, p = 1). Kogen's run on `kogen-review-on-demand` on the MacBook hit the 3,600 s deadline.

The test harness's report table shows 0 correct for Codex alone in both blocks. That is a labelling error in the report, not a result: it counts only builds with the outcome `landed` or `ok` and files every finished Codex-alone cell as a workflow failure. The grades are the ones above. Usage and cost were not measured for either setup.

Limits: one run per task and setup; the tasks were chosen because Codex at high effort had failed them, and six of the nine come from Kogen's own code. One laptop and one MacBook, one model and effort. Kogen's time covers shaping, an independent review and checks that a single run does not do. The task kits stay private until the hill-climb is done. Numbers, task lists, per-run rows and the scripts that reproduce them: [`reproduce/hk3-lm-hard-tasks/`](../reproduce/hk3-lm-hard-tasks/README.md) and [`reproduce/hk3-mb-hard-tasks/`](../reproduce/hk3-mb-hard-tasks/README.md).

### Hard tasks, newer Kogen: Kogen driving Codex, against Codex CLI alone

Result, 30 October 2026: **unresolved on success (5 scored task pairs, one run each).** The laptop block of the Codex comparison above was repeated at Kogen a3ca7bc (the change that stops a build from ending early), with the same 9 tasks, model, effort, machine and Codex CLI 0.166.0. Four of the nine tasks are not scored: three never ran their acceptance suite in grading and one has a fixture that only works on macOS, so 8 of 18 cells are left out for both setups. On the other 5 tasks each setup passed the same 3 (0.60, 95% interval 0.23 to 0.88) and failed the same 2.

| Tasks scored | Kogen passed | Codex alone passed | Paired test | Fisher | Wall (Kogen / Codex) | Input / output tokens (Kogen / Codex) |
|---:|---:|---:|---|---|---|---|
| 5 | 3 | 3 | 0 discordant tasks, p = 1 | p = 1 | 7,614 s / 1,408 s (Kogen slower on all 5, p = 0.0625) | 10.95 M / 15.44 M and 75,182 / 62,722 (p = 1 and p = 0.375) |

Tokens are each setup's own record, measured for both on all 5 tasks; no cost is computed for this block (its tokens were not priced). No scored Kogen cell ended before building, so this block does not show whether the early-stop change helps; two excluded Kogen cells did end before any build request. Against the older laptop block on the same 5 tasks, Kogen has the same outcome on every task, with identical test counts; its wall time was shorter on 3 tasks and longer in total (7,614 s against 6,923 s). That comparison is descriptive: different Kogen versions, one run each. The older block scored all nine tasks, including the four that cannot be scored reliably; read its results with that in mind.

Limits: one run per task and setup, five scored pairs; an edge of a task or two could not show. The tasks were chosen because Codex at high effort had failed them. One laptop, one model and effort. Kogen's time and tokens cover shaping, an independent review and checks that a single run does not do. The task kits stay private until the hill-climb is done. Numbers, task list, per-run rows (scored and excluded) and the script that reproduces them: [`reproduce/hk4-lm-hard-tasks/`](../reproduce/hk4-lm-hard-tasks/README.md).

### Hard tasks on the MacBook: Kogen driving Claude Code, against Claude Code alone

*Corrected 31 October 2026: on some of these tasks the grader, not the agents, decided the result. See [Hard tasks: grading correction](#hard-tasks-grading-correction).*

Result, 30 October 2026: **unresolved on success and on cost (6 task pairs per block, one run each); Kogen's wall time was higher on all 6 tasks of the Opus block (p = 0.031).** Two MacBook blocks, each on 6 hard tasks, one run per task and setup, with the same fixed Claude Code 2.1.312 binary for both setups. They differ in model, effort and Kogen version, so they are not pooled.

| Block | Model, effort | Kogen | Kogen passed | Claude Code alone passed | Paired test | Fisher | Cost at list price† (Kogen / alone) | Wall (Kogen / alone) |
|---|---|---|---:|---:|---|---|---|---|
| `cco-mb` | claude-opus-5-5, high | 022ed9a0 | 2/6 (0.33, 0.10 to 0.70) | 3/6 (0.50, 0.19 to 0.81) | 1 discordant task, p = 1 | p = 1 | $24.99 / $13.40 | 9,713 s / 7,016 s |
| `ccs2-mb` | claude-sonnet-5-5, medium | c8dae5a6 | 2/6 (0.33, 0.10 to 0.70) | 2/6 (0.33, 0.10 to 0.70) | 0 discordant tasks, p = 1 | p = 1 | $7.50 / $2.33 (5 tasks priced for both) | 7,023 s / 4,918 s |

†Token counts are read from Claude Code's own session records, the same way for both setups; dollars are those tokens at Anthropic list prices, not plan prices. The test harness recorded no requests, tokens or cost for the Kogen setup, so these figures come from that separate reading.

On the Opus block the one task that differs is `kogen-review-on-demand`: Kogen's run hit the 3,600 s deadline with 291 of 298 tests passing, while Claude Code alone passed it in 3,526 s. Kogen's wall time was higher on all 6 tasks (p = 0.031) and its cost on 4 of 6 (p = 0.69). On the Sonnet block both setups hit the deadline on that task, one test short (Kogen 291 of 298, alone 297 of 298); Kogen cost more on all 5 priced tasks (p = 0.0625, the smallest p five pairs can give) and was slower on 5 of 6 (p = 0.22). The alone run that hit the deadline wrote no final usage record, so that task is left out of the cost figures.

The test harness's report table shows 0 of 6 for Claude Code alone in both blocks. That is a labelling error in the report, not a result: it counts only builds with the outcome `landed` or `ok`, and files every finished alone cell as a workflow failure. The grades are the ones above.

Limits: one run per task and setup, six pairs; one task moves a rate by 0.17. The tasks were chosen because Codex at high effort had failed them, and three of the six come from Kogen's own code. One MacBook. Kogen's time and cost cover shaping, an independent review and checks that a single run does not do. The task kits stay private until the hill-climb is done. Numbers, task lists, per-run rows and the scripts that reproduce them: [`reproduce/cco-mb-hard-tasks/`](../reproduce/cco-mb-hard-tasks/README.md) and [`reproduce/ccs2-mb-hard-tasks/`](../reproduce/ccs2-mb-hard-tasks/README.md).

### Hard tasks: what Kogen's independent review did

Result, 31 October 2026: **in these runs the review caught no defect that the grader sees, and in two cases it broke the build.** This is a count over the five hard-task blocks above, not a test of review: no setup ran without it. Across 36 Kogen cells, 29 reached a review and held 31 reviews. All 31 approved and none raised a blocking finding; 20 note-level findings in 16 reviews, none naming a defect that a failing hidden test checks.

| | Reviews | Changed the tree | Verification red afterwards | Of cells that fail a hidden test (reviews) |
|---|---:|---:|---:|---:|
| Tasks that can separate the setups | 21 | 10 | 2 | 4, all approved |
| Three tasks no setup could pass (acceptance never ran) | 10 | 2 | 0 | 3, all approved |

The two red verifications were the first review on `kogen-review-on-demand` in the Codex blocks (`hk3-lm`, `hk3-mb`): it approved with no findings but had edited the tree, and three public acceptance scenarios then failed. A second review fixed both. On `hk3-lm` the cell passed; on `hk3-mb` the repaired tree graded 298 of 298, but the cell hit its 3,600 s deadline first and was graded on the start tree. Three reviews wrote a note clearing code in the area where a hidden subtest fails, one on a discriminating task (`tally-periodic-go`, `ccs2-mb`).

Limits: a grader that sees only the final tree cannot see a defect a review fixed, and twelve reviews changed the tree; apart from `hk3-mb`'s `kogen-review-on-demand`, the tree before the review was never graded. One run per task and block, three models and two efforts, tasks chosen because another agent failed them. The confirmation, Kogen with review on against off at the same model and effort, has not been run. Counts, the per-review rows and the scripts that reproduce them: [`reproduce/hard-task-review-value/`](../reproduce/hard-task-review-value/README.md).

### Hard tasks: grading correction

Correction, 31 October 2026: **on three of the nine hard tasks, and a fourth on the laptop, the grader could not tell the setups apart.** This covers the three sections above (five blocks: `hk3-lm`, `hk3-mb`, `cco-mb`, `ccs2-mb`, `ccs3-lm`). Their text and numbers are left as published; this section says what in them was the grader's doing.

- `kogen-loop-tool-cut`, `kogen-loop-read-ledger` and `kogen-loop-parallel-calls` include public acceptance scenarios run with Cucumber. The grader never gave the scenario runner Cucumber or Node, and these task kits do not install Cucumber. The runner then reported no scenario and exited as if it had finished, so every setup in every block failed the same scenarios as "missing", whatever it built.
- `revive-baseline-go` on the laptop: a project test needs two fixture folders whose names differ only by case. The task kit was cut on a Mac, which keeps only one of them, so on Linux that test fails before any change, for every setup. Kogen's start-up check refused to build there; the bare agents' grades lost a whole test command to it.

Of the 31 tied task pairs in those sections, 14 were forced this way. The grader is repaired: it now supplies Cucumber and Node, a run that reports no scenario is an infrastructure failure rather than a set of failed tests, and on Linux it restores the lost fixture in its grading copy.

Every final tree that still exists was graded again, with no model calls. Kogen kept its final trees only in `ccs3-lm`; in the other four blocks only the bare agents' changes were stored, so most Kogen cells on these tasks cannot be regraded.

| Block | Kogen pass / fail / unknown / pending | Alone pass / fail / unknown / pending | Pairs: only Kogen / only alone / tie / open |
|---|---|---|---|
| `hk3-lm` | 3 / 4 / 2 / 0 | 4 / 3 / 0 / 2 | 0 / 0 / 6 / 3 |
| `hk3-mb` | 2 / 3 / 1 / 0 | 3 / 3 / 0 / 0 | 2 / 2 / 1 / 1 |
| `cco-mb` | 2 / 3 / 1 / 0 | 4 / 2 / 0 / 0 | 0 / 1 / 4 / 1 |
| `ccs2-mb` | 2 / 3 / 1 / 0 | 3 / 3 / 0 / 0 | 0 / 0 / 5 / 1 |
| `ccs3-lm` | 6 / 2 / 0 / 1 | 7 / 0 / 0 / 2 | 0 / 1 / 6 / 2 |

"Unknown" is a Kogen cell whose tree was not kept and whose result depended on the scenarios. "Pending" is a kept laptop tree that still needs a regrade on the laptop.

- `kogen-loop-tool-cut` passes for every tree regraded, both setups (6 trees). It was a task every setup solved, graded as one every setup failed; the four Kogen trees that were not kept passed every hidden test, so the task most likely ties everywhere. It leaves the hard set.
- `kogen-loop-parallel-calls` now separates the setups in `ccs3-lm`: Claude Code alone passes, Kogen fails one hidden test. That block is no longer a tie on every task.
- `kogen-loop-read-ledger`: the scenarios now pass for every tree. One hidden test fails on the MacBook for every tree graded there, including laptop trees that passed it on the laptop, so on the MacBook the task still cannot separate the setups.
- The laptop was busy with other work, so the laptop trees of the three scenario tasks were graded on the MacBook. Their hidden-test results match the laptop's own grades, except that one test. Five laptop trees (`kogen-loop-read-ledger` and `revive-baseline-go`) still wait for the laptop.

Success stays unresolved in every block (no block has more than two discordant tasks either way; every p = 1). It rests on fewer tasks than the sections above say: without the four affected tasks, 22 task pairs remain across the five blocks (Kogen 14 passes, the bare agents 15), not 36. With the corrected grades, the bare agents gained 6 passes and Kogen 1.

Limits: one run per task and setup; 5 Kogen cells stay unknown and 5 laptop trees are pending. Rules, per-cell rows, the grader repair and the regrade driver: [`reproduce/hard-tasks-grading-correction/`](../reproduce/hard-tasks-grading-correction/README.md).

### Native loop with checks and review, against Codex CLI

Both setups used gpt-6.1-terra and ran on the same machine. Kogen built at high effort and reviewed at medium; Codex ran at high effort.

| Tool | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 (native loop, review, checks) | 26/26 | 101.0 s | 131.7 s | 30,919 | 94,672 | 67.3% | 3,836 | 52,637 |
| Codex CLI 0.165.0-alpha (bare) | 26/26 | 58.9 s | 74.1 s | 21,870 | 169,193 | 87.1% | 3,874 | 52,099 |

In Kogen's run logs, the review and verification phases together average about 37 s, alongside a 43 s mean whole-run gap. Review input accounts for about half of Kogen's uncached input. These observations do not isolate the cause of the gap.

## Method

- **Tasks:** the earlier scoreboards use 13 short Go tasks; the evening sections state their task and repetition counts. Tasks are graded by hidden tests omitted from the prompt and initial workspace. A grade reports final-tree test success; missing evaluations and evaluator setup failures are ungraded.
- **Prompt:** every bare harness received one prompt containing the request, the acceptance scenarios, the check commands and the protected paths. Kogen pipeline setups received the same acceptance scenarios as an Intent.
- **Isolation:** each attempt ran in a fresh Git workspace with a 3,600-second deadline. The same hidden tests graded the final tree after the agent exited.
- **Package installs, from 30 October:** some tasks install npm packages for their acceptance tooling. On the laptop and desktop test machines, the test harness now prepares each locked set of packages once, before any run, and gives every run its own copy. No run spends its time downloading packages, and a slow download can no longer exhaust the 120-second limit on Kogen's start-up checks. In a fault test where npm hung, the old harness refused both test tasks at that limit; the new one passed the start-up checks in 6 to 54 s without calling npm. The prepared copies matched fresh installs file for file on the three tasks compared. If a start-up check still runs out of time, the harness now postpones that task until the other tasks' runs have finished and then retries it, instead of stopping the whole batch; a task that still times out is reported as an infrastructure gap and the batch as incomplete. Kogen itself and its time limits are unchanged.
- **Pairing:** match tools by task and repetition, then average matched repetitions within each task for task-level comparisons. Whole-run wall time includes setup and failed attempts but excludes hidden-test grading. Shared machine load and different provider routes limit timing comparisons.
- **Client versions:**
  - Codex CLI 0.165.0-alpha.1.2 and 0.165.0;
  - Pi 0.73.1 and OpenCode 1.19.5;
  - Claude Code 2.1.312;
  - Kogen at commit 16102c97, vendoring kogen-loop e5054c8, and kogen-loop b8a4046 (from Kogen 8ee463f8);
  - the test harness at 7a0e22ad.

## Limits

- The tasks are short and pass rates are near the ceiling. These results say little about pass on harder work. The hard-task sections above are the exception, with six to nine tasks and one run each.
- Kogen's pipeline does more than a bare agent (checks and an independent review), so its time and cost cover more work.
- Isolation of the hidden tests was checked by scanning each agent's event stream. The scan found no suspects, but it is not a proof.
- The Codex CLI build was an alpha bundled with a desktop app.
- The study does not support claims about any model or product beyond this task set and setup.

## Next

Hill-climbs on both scoreboards are running as separate patch runs. The patches cover review that resumes the build session, deferred and parallel checks, effort scheduling, context management, reading and tool use. Winning patches will be built into Kogen and kogen-loop, and this page will be updated.
