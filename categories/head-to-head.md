# Head-to-head: agent harnesses on short Go tasks (29 October 2026)

Status: DESCRIPTIVE. These are baselines for a hill-climb, not a pre-registered test.

**Correction, 29 October 2026.** An attempt without an evaluation was counted as a failed test, and missing usage was included as zero in some per-pass figures. The table now separates ungraded attempts and withholds totals when usage is missing. Comparisons retain every task and repetition. Passing tests describes the final code, separately from whether the agent completed cleanly.

**Configuration note, 29 October 2026.** In every round on this page, kogen-loop ran with a one-line system instruction set by the test harness instead of its own built-in default instruction, while Codex CLI, Claude Code, Pi and OpenCode each ran with their own built-in instructions. Later rounds run kogen-loop with its built-in default, the same way the other harnesses run.

This study compares coding-agent harnesses that get the same task and the same model. It has two scoreboards:

1. **Harness against harness.** The kogen-loop harness, run bare, against Codex CLI and Claude Code. Each harness receives the same single prompt.
2. **Kogen's pipeline against a bare agent.** Kogen adds an Intent, its own checks and an independent review. Each pipeline arm is compared with a bare agent on the same model.

## Scoreboard 1: kogen-loop against other agent harnesses (same model, same prompt)

All arms used gpt-6.1-terra with high reasoning effort on the same 13 tasks. Within each batch, the arms of a task ran one after the other on the same machine.

### Four harnesses (2 repetitions per task)

| Harness | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop e5054c8 | 25/26 | 73.2 s | 408.6 s | 11,841 | 29,505 | 59.9% | 2,796 | 24,791 |
| Codex CLI 0.165.0-alpha | 26/26 | 63.3 s | 101.0 s | 17,910 | 158,691 | 88.7% | 3,713 | 46,840 |
| Pi 0.73.1 | 25/25 graded; 1 ungraded | 61.4 s | 105.0 s | missing | missing | missing | missing | missing |
| OpenCode 1.19.5 | 25/26 | 97.5 s | 164.4 s | 25,563 | 172,226 | 85.2% | 4,603 | 58,641 |

\*Cost is in uncached-equivalent tokens: uncached input + 0.1 × cached input + 4 × output. This model has no list price in the study.

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

- **Tasks:** 13 short Go tasks, graded by hidden tests omitted from the prompt and initial workspace. Tables state whether each arm ran once or twice per task. A grade reports final-tree test success; missing evaluations and evaluator setup failures are ungraded.
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
