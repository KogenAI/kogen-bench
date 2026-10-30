# Head-to-head: agent harnesses on short Go tasks (30 October 2026)

Status: DESCRIPTIVE. These are baselines for a hill-climb, not a pre-registered test.

**Correction, 29 October 2026.** An attempt without an evaluation was counted as a failed test, and missing usage was included as zero in some per-pass figures. The table now separates ungraded attempts and withholds totals when usage is missing. Comparisons retain every task and repetition. Passing tests describes the final code, separately from whether the agent completed cleanly.

**Configuration note, 29 October 2026.** In the earlier rounds under Scoreboards 1 and 2, kogen-loop ran with a one-line system instruction set by the test harness instead of its own built-in default instruction, while Codex CLI, Claude Code, Pi and OpenCode each ran with their own built-in instructions. The evening rounds below run kogen-loop with its shipped default instructions, the same way the other harnesses run.

This study compares coding-agent harnesses that get the same task and the same model. It has two scoreboards:

1. **Harness against harness.** The kogen-loop harness, run bare, against Codex CLI and Claude Code. Each harness receives the same single prompt.
2. **Kogen's pipeline against a bare agent.** Kogen adds an Intent (its written statement of what the change must do, with acceptance scenarios), its own checks and an independent review. Each pipeline setup is compared with a bare agent on the same model.

## Eight tasks, both tools on the same OpenAI API key, 30 October 2026

**Summary.** On eight Go tasks, kogen-loop and Codex CLI both passed 8/8 at medium effort and 8/8 at high effort. At medium effort, kogen-loop cost **40% less per pass** ($0.1020 against $0.1698) and was cheaper on all 8 tasks (two-sided sign test p = 0.0078). Its agent wall was lower on 7 of 8 tasks, which does not reach significance (p = 0.0703). At high effort, no difference in cost or wall time was resolved. This is one run per task and tool, on tasks chosen for this comparison; it is evidence about these eight tasks, not a general result.

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
- **High:** kogen-loop cost less on 5/8 tasks (p = 0.727); cost ratio 0.966. Wall was lower on 2/8 (p = 0.289); mean-wall ratio 1.087. Pass: no task differed (p = 1).

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

**Route finding.** Loop and Codex reach the model through different endpoints and sign-in clients. From about 04:00 UTC on 30 October, loop's output rate on the same tasks and with similar output counts fell from about 110 to about 48 tokens per second, while Codex wall times stayed about the same. Small route probes measured about 45 versus 81 tokens per second. The evidence points to the route as the source of tonight's subscription wall-time gap, rather than a change in loop's code.

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

**Summary.** On 24 Go tasks, kogen-loop and Codex CLI both passed every run at both efforts (24/24 each). kogen-loop used about 40% of Codex CLI's equivalent tokens per pass and used fewer on all 24 tasks at both efforts. Its wall time was 25–30% longer, but the two tools reached the model through different subscription routes, so the wall difference cannot be attributed to the tool. This is one run per task and tool, so the sign tests are descriptive.

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

**Summary.** We looked for a faster route that kogen-loop could reach with its own sign-in and an honest client label, and found none. Every variant streamed at about 54 tokens per second, so the slower wall time above looks like a fixed pace on kogen-loop's route rather than something in its request handling. This is a small probe and it is descriptive.

**Setup.** Route: subscription sign-in used by kogen-loop. Model: gpt-6.1-terra, medium effort, no tools, the same prompt each time (343 output tokens, no reasoning tokens in every successful response). Each variant ran 10 paired requests against the current setup, alternating order, with a fresh session on every request. No other tool's client identity or credentials were used.

| Variant (gpt-6.1-terra, medium effort) | Streaming rate, median [IQR], tokens/s | Same-block current setup, tokens/s |
|---|---:|---:|
| Same endpoint, honest client label | 53.3 [51.6, 54.5] | 54.0 [53.7, 54.1] |
| Persistent WebSocket connection, honest client label | 54.3 [54.0, 54.9] | 53.6 [52.8, 54.3] |
| Subscription endpoint used by Codex CLI | refused (HTTP 401) on a single check; not retried | |

Rates are measured from the first generated text to the last byte. The WebSocket variant started producing text about 0.6 s sooner (1.86 s against 2.47 s median), which is a connection effect, not a faster stream. Neither variant reached the pre-set bar of 1.5× the median rate with non-overlapping interquartile ranges. The rate was nearly constant across 40 requests, which fits a fixed per-stream pace set by the provider rather than load. Whether kogen-loop's sign-in client can be given access to the faster route is a question for the provider. Until it is answered, subscription wall comparisons should be read by route and time period.

### Write-check patch short test, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** A patch that lets kogen-loop's file-write tool carry a known follow-up check did not change behaviour: the model never used the new option in the first three runs where it could, so the test was stopped and the patch does not advance. Every completed run passed. The comparisons below describe these runs only and do not estimate the patch's effect when it is used.

**Setup.** Route: both tools on the same OpenAI API key. Model: gpt-6.1-terra, high effort. Tasks ran one run per task and setup in a fixed order, and the test stopped after three tasks. Codex CLI had completed only the first two tasks when it stopped, so its row covers those two. The rebuilt unpatched baseline did not match the checksum recorded for the earlier build, so the baseline comparison is approximate.

| Setup (gpt-6.1-terra, high effort) | Passed | Median wall | Median model requests | API cost per pass |
|---|---:|---:|---:|---:|
| kogen-loop (shipped default) | 3/3 | 380.5 s | 36 | $0.2203 |
| kogen-loop with write-check patch | 3/3 | 514.0 s | 54 | $0.3481 |
| Codex CLI (2 tasks) | 2/2 | 320.9 s | 38.5 | $0.3291 |

Against the unpatched loop, the patch had lower wall on 0 of 3 tasks, with higher output tokens and cost on all three (two-sided sign test p = 0.25 on 3 tasks). Passes tied on every task. With three tasks the sign test cannot resolve small differences. The patch's new option was used in 0 of 3 runs, so the extra requests and cost reflect run-to-run variation, not the patch's intended mechanism.

### Reasoning replay, same OpenAI API key, gpt-6.1-terra, high effort

**Summary.** We tested whether carrying the model's earlier reasoning back to it between turns closes the reasoning gap described on the kogen-vs-codex page. On 8 Go tasks, all three setups passed every run. kogen-loop with reasoning carried back used the fewest requests and the lowest cost per pass in total, but more reasoning tokens than the default loop, and task by task it was cheaper than the default loop on only 3 of 8 tasks, so the hypothesis is not supported as stated. No difference is resolved by the per-task sign tests. This is one run per task and setup, so it is descriptive.

**Setup.** Route: both tools on the same OpenAI API key. Model: gpt-6.1-terra, high effort. Each task ran once per setup, with the setups interleaved task by task. Figures are per pass over the 8 tasks.

| Setup (gpt-6.1-terra, high effort) | Passed | Model requests | Reasoning tokens | API cost | Wall |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 32.2 | 2,727 | $0.225 | 296 s |
| kogen-loop with reasoning carried back | 8/8 | 20.2 | 4,117 | $0.175 | 268 s |
| Codex CLI | 8/8 | 28.8 | 4,152 | $0.236 | 273 s |

Reasoning carried back against the shipped default, task by task: cost lower on 3 tasks and higher on 5 (two-sided sign test p = 0.727); requests lower on 3, higher on 4 and tied on 1 (p = 1.0); reasoning tokens higher on 6 of 8 tasks (p = 0.289). The lower totals come mostly from one slow run of the shipped default on one task (90 requests, $0.649, 708 s); without it the per-pass gaps shrink, which is why a larger test on fresh tasks is planned. Against Codex CLI: requests lower on 6, higher on 1 and tied on 1 (p = 0.125); cost lower on 6 and higher on 2 (p = 0.289). With 8 tasks the sign tests cannot resolve differences of this size, so the question stays open.

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

- The tasks are short and pass rates are near the ceiling. These results say little about pass on harder work.
- Kogen's pipeline does more than a bare agent (checks and an independent review), so its time and cost cover more work.
- Isolation of the hidden tests was checked by scanning each agent's event stream. The scan found no suspects, but it is not a proof.
- The Codex CLI build was an alpha bundled with a desktop app.
- The study does not support claims about any model or product beyond this task set and setup.

## Next

Hill-climbs on both scoreboards are running as separate patch runs. The patches cover review that resumes the build session, deferred and parallel checks, effort scheduling, context management, reading and tool use. Winning patches will be built into Kogen and kogen-loop, and this page will be updated.
