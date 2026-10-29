# Head-to-head: agent harnesses on short Go tasks (29 October 2026)

Status: DESCRIPTIVE. These are baselines for a hill-climb, not a pre-registered test.

This study compares coding-agent harnesses that get the same task and the same model. It has two scoreboards:

1. **Harness against harness.** The kogen-loop harness, run bare, against Codex CLI and Claude Code. Each harness receives the same single prompt.
2. **Kogen's pipeline against a bare agent.** Kogen adds an Intent, its own checks and an independent review. Each pipeline arm is compared with a bare agent on the same model.

## Scoreboard 1: kogen-loop against Codex CLI (same model, same prompt)

Both arms used gpt-6.1-terra with high reasoning effort and ran on the same machine. For each task the two arms ran one after the other, with 2 repetitions per task.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| kogen-loop e5054c8 | 26/26 | 72.3 s | 116.7 s | 9,285 | 27,008 | 65.6% | 2,793 | 22,228 |
| Codex CLI 0.165.0-alpha | 25/26 | 61.1 s | 83.8 s | 18,637 | 154,036 | 87.9% | 3,891 | 47,741 |

\*Cost is in uncached-equivalent tokens: uncached input + 0.1 × cached input + 4 × output. This model has no list price in the study.

Per task (13 tasks, comparing medians):
- Codex was faster on 12 tasks and kogen-loop on 1.
- kogen-loop cost less on 12 tasks and Codex on 1.

In short:
- kogen-loop passed one more attempt.
- It used 82% less input and 50% less uncached input, and wrote 28% less output.
- It cost 53% less per pass.
- It was 18% slower at the median.

Cached share is lower for kogen-loop because its total input is much smaller, not because it re-sends more. Uncached input per pass is the cache measure that matters here.

## Scoreboard 2: Kogen's pipeline against bare agents

### Driving Claude Code, against bare Claude Code

Both arms used claude-sonnet-5-5 at medium effort and ran on the same machine, with 2 repetitions per task.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass† |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 driving Claude Code | 23/26 | 122.5 s | 202.0 s | 46,269 | 262,115 | 82.3% | 8,597 | $0.293‡ |
| Claude Code 2.1.312 (bare) | 24/26 | 61.9 s | 95.2 s | 11,212 | 88,973 | 87.4% | 5,879 | $0.111 |

†Dollar figures are the list-price estimates that the Claude Code client reports. They are not plan prices.

‡25 of 26 Kogen cells reported a cost.

Kogen's pipeline runs two Claude Code sessions per task: one builds and an independent one reviews. It also runs the project's checks. That explains most of the extra time and cost.

### Native loop with checks and review, against Codex CLI

Both arms used gpt-6.1-terra and ran on the same machine. Kogen built at high effort and reviewed at medium; Codex ran at high effort.

| Arm | Passed | Median wall | 90th percentile wall | Uncached input per pass | Total input per pass | Cached share | Output per pass | Cost per pass* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kogen 16102c97 (native loop, review, checks) | 26/26 | 101.0 s | 131.7 s | 30,919 | 94,672 | 67.3% | 3,836 | 52,637 |
| Codex CLI 0.165.0-alpha (bare) | 26/26 | 58.9 s | 74.1 s | 21,870 | 169,193 | 87.1% | 3,874 | 52,099 |

In Kogen's run logs, the review step and its verification account for about 37 s of the 43 s mean gap. The review session always starts with a cold prompt cache, and that accounts for about half of Kogen's uncached input.

## Method

- **Tasks:** 13 short Go tasks, each graded by hidden tests that the agent never sees. Each arm ran each task twice.
- **Prompt:** every bare harness received one prompt containing the request, the acceptance scenarios, the check commands and the protected paths. Kogen pipeline arms received the same acceptance scenarios as an Intent.
- **Isolation:** each attempt ran in a fresh Git workspace with a 3,600-second deadline. The same hidden tests graded the final tree after the agent exited.
- **Pairing:** for each task, the arms of a pair ran one after the other on the same machine. Wall times are comparable only within a pair.
- **Client versions:**
  - Codex CLI 0.165.0-alpha.1.2;
  - Claude Code 2.1.312;
  - Kogen at commit 16102c97, vendoring kogen-loop e5054c8;
  - the lanes harness at 7a0e22ad.

## Limits

- The tasks are short and pass rates are near the ceiling. These results say little about pass on harder work.
- Kogen's pipeline does more than a bare agent (checks and an independent review), so its time and cost cover more work.
- Isolation of the hidden tests was checked by scanning each agent's event stream. The scan found no suspects, but it is not a proof.
- The Codex CLI build was an alpha bundled with a desktop app.
- The study does not support claims about any model or product beyond this task set and setup.

## Next

Hill-climbs on both scoreboards are running as patch lanes. The patches cover review that resumes the build session, deferred and parallel checks, effort scheduling, context management, reading and tool use. Winning patches will be built into Kogen and kogen-loop, and this page will be updated.
