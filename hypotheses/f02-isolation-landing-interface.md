# F02 — Isolation, landing and interface

Coverage: H16–H18. The propositions below turn product questions into observable comparisons. No controlled superiority study is identified in the current public evidence. The research census provides topic navigation only; it does not state that a study tested or resolved a hypothesis.

## Hypotheses

| ID | Falsifiable proposition | Current state |
|---|---|---|
| H16 | Under matched concurrent project workloads, worktree, copy-on-write, or another isolation design reduces cross-project interference and failure without unacceptable setup or Build-time cost. | NOT ESTABLISHED; no matched design comparison. |
| H17 | Rebase-based landing produces fewer unwanted base-history changes or recovery errors than automatic merge while remaining within a declared time and conflict budget. | NOT ESTABLISHED; no comparative reliability or cost study. |
| H18 | A headless command-driven Shaping interface improves external-driver completion, latency, or error recovery over a Kogen TUI under the same tasks. | NOT ESTABLISHED; no measured usability or runtime comparison. |

## Experiment register

| experiment_id | Arm / task set | Model / effort | Revision; host / epoch | Planned / started / finished / graded / ITT n | Outcome, status, correction or supersession | Claim ID | Public receipt |
|---|---|---|---|---|---|---|---|
| `isolation` | Workspace design research; no controlled arm or task set is linked in the public census. | Not applicable / not recovered. | Not recovered. | Not reported. | Research-index metadata only; no measured workspace winner. | No claim ID assigned. | [research census](../research/README.md) |
| `merging-v2` | Rebase/merge design research; no public paired task or fault-injection cohort is linked. | Not applicable / not recovered. | Not recovered. | Not reported. | Research-index metadata only; no comparative landing result. | No claim ID assigned. | [research census](../research/README.md) |
| `shaping-ux` | Command interface study; no public Kogen-TUI comparison or assigned user/task population is linked. | Not applicable / not recovered. | Not recovered. | Not reported. | Research-index metadata only; no measured interface advantage. | No claim ID assigned. | [research census](../research/README.md) |

## Design implications

Treat isolation, landing, and CLI interaction as product and reliability choices unless a controlled comparison is published. A correctness contract or implementation-conformance case can show that a selected design behaves as specified; it cannot show that the design improves benchmark completion or usability.

## What this evidence does not show

No public sample size, outcome, or comparison establishes that worktrees outperform copy-on-write, that rebase is better than merge, or that a headless interface is easier or faster than a TUI. Historical failure analysis and topic-level research listings are not comparative efficacy evidence.

## Smallest open tests

For isolation, inject concurrent conflicting writes into the same pinned project set and compare corruption, recovery, setup time, and completion. For landing, replay the same concurrent change set through rebase and automatic merge and score conflicts, base changes, and recovery cost. For the interface, give external drivers the same fixed shaping tasks and compare completion, errors, and elapsed time across CLI and TUI.
