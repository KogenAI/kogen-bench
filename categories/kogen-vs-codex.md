# Kogen versus Codex

Definitions: [public glossary](../rounds/GLOSSARY.md).

- [r58](../rounds/r58/README.md) — no new claim; use source report with its corrections.
- [r58b](../rounds/r58b/README.md) — no new claim; use source report with its corrections.
- [r61](../rounds/r61/README.md) — no new claim; use source report with its corrections.
- [r62](../rounds/r62/README.md) — no new claim; use source report with its corrections.
- [r62b](../rounds/r62b/README.md) — The committed ledger has 72/72 graded cells: Kogen direct-escalate 19/24, direct-shell 16/24, and staged 17/24. Base-wide formatting on elx-02/elx-04 is a documented confound for Kogen comparisons.
- [r65](../rounds/r65/README.md) — no new claim; use source report with its corrections.
- [r65b](../rounds/r65b/README.md) — Held-out and discriminator aggregates are withheld because the public outcome sources lack a reconciled classification; the format-gate confound remains documented.
- [r66](../rounds/r66/README.md) — The public cells export records 17/20 direct Sol-medium passes; historical controls and task-level comparisons are withheld because the control cell cohorts are not identified.
- [r67](../rounds/r67/README.md) — no new claim; use source report with its corrections.
- [r67b](../rounds/r67b/README.md) — no new claim; use source report with its corrections.
- [r68b](../rounds/r68b/README.md) — DESCRIPTIVE: current r68b Kogen plan-shell recorded 21/24. Public r53 cells filtered to `round=r53`, `arm=r53:lmax` (gpt-6-luna / max) recorded 21/24, and `arm=r53:sol-high` (gpt-6.1-sol / high) recorded 22/24. Kogen requested max was clamped to xhigh; these descriptive counts do not establish superiority.
- [r71](../rounds/r71/README.md) — 49 officially graded outcomes are recorded; no reconciled analysis is published, so no conclusion is drawn. The two official syn-01 smoke outcomes are recorded separately from the scored denominator.

## Additional findings, 30 October 2026

### Reasoning cost at high effort, gpt-6.1-terra

In short: at high effort, with both tools on the same OpenAI API key, kogen-loop used about twice the reasoning tokens of Codex CLI and made more model requests. Both tools passed every run. The cause is not settled.

Four Go tasks ran twice per tool (8 runs each), same model, same effort.

| Tool (gpt-6.1-terra, high effort) | Passed | Model requests | Reasoning tokens | Output tokens | API cost, total |
|---|---:|---:|---:|---:|---:|
| kogen-loop (shipped default) | 8/8 | 108 | 27,769 | 80,419 | $0.730 |
| Codex CLI | 8/8 | 90 | 14,106 | 62,018 | $0.734 |

Total cost was about the same, so the extra reasoning did not show up as a higher bill in this sample. At medium effort on the same tasks the gap was small (9,154 against 6,692 reasoning tokens; 84 against 85 requests).

A likely cause is that kogen-loop's chat path to the API does not carry the model's earlier reasoning back to it between turns, so the model re-derives some of it. This is a hypothesis. A later test on 8 tasks that carried reasoning back gave fewer requests and a lower cost per pass than the default loop, but more reasoning tokens, and no per-task difference was resolved (see the reasoning replay section on the head-to-head page). The question is unresolved. Eight runs from four tasks are descriptive; they do not show how large the effect is on other tasks, and the two efforts were run in separate sessions.

### Hard-task set: Kogen against Codex CLI alone, gpt-6.1-terra, high effort

No results yet. This describes the set and why it was built.

Earlier runs mostly passed for Codex CLI at high effort, which leaves little room to see a difference. To get tasks where a difference is possible, we selected every Go task with a recorded failure of Codex CLI at high effort whose failure was a real coding failure rather than a provider outage or setup problem. That gave 9 tasks. In their earlier Codex CLI attempts at high effort they passed 0 to 3 times in 6 to 8 attempts (one task has a single earlier attempt, a failure). Tasks with a capacity error at the provider were left out.

The planned comparison is full Kogen (it writes and approves its own spec, builds, and has an independent review) against Codex CLI alone. Both use gpt-6.1-terra at high effort, with the same prompt and the same starting files. Each task runs once per tool on one machine; three tasks also run once on a second machine, for 24 runs in total. Because the tasks were chosen for having failed before, pass rates here will be lower than on the earlier task sets, and they cannot be compared with those. The analysis is fixed in advance: a paired comparison per task with an exact sign test. With nine tasks it can only detect large differences, and small ones will be reported as inconclusive. The first runs are pending.
