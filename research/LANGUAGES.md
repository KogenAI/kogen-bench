# Kogen language round: early elimination

AI coding agents (GPT-6 Luna at maximum effort) build the same tasks in Go, Rust, TypeScript and Elixir, and each attempt is scored by hidden tests the agent never sees. Elixir is out. Rust, Go and TypeScript are still being compared in a final round.

## Same tasks, all four languages

| Language | Passed | Rate |
|---|---:|---:|
| Rust | 15 of 18 | 83% |
| TypeScript | 15 of 18 | 83% |
| Go | 12 of 18 | 67% |
| Elixir | 7 of 18 | 39% |

18 attempts per language: the [original comparison](https://bench.kogen.dev/rounds/r70/) (10), the [extension](https://bench.kogen.dev/rounds/r70-rve-ext/) (6) and a two-task check on 9 October (2).

[Why Elixir was dropped: Rust vs Elixir evidence](https://bench.kogen.dev/languages/rust-vs-elixir/)

The final round, on harder Kogen-like tasks, is running. Results will be added here.

Limits: small samples, one model, and the runs differ in design (the original comparison wasn't registered in advance).

## 9–10 October rounds

These rounds report descriptive results only; shape1 used an earlier runner and grader configuration. Race 4 reports descriptive results and does not select an overall language winner. Any later selection requires its own published decision rule and results. Race 5 is descriptive. Go wins the coordinator-interpreted registered PRIMARY comparison, which retains scores from invalid runs. Alternative readings and timing methods are reported as sensitivities; incomplete audits and historical searches limit the conclusion. ([Race 5](../rounds/race5/README.md)). Race 6 is a descriptive spec-format pilot comparing prose, + Quint, + Gherkin, and both for Elixir and Go ([Race 6](../rounds/race6/README.md)). Races 1 and 2 used an unpatched spec and suite that described Kogen as a Rust program. The Race 1 specification also included prototype implementations in Rust, Go and Elixir (`spec/quint/prototype/impls/`), but none in TypeScript or Gleam; this may have favoured those three arms. A check of these runs for harness defects is pending; scores may be revised if it finds any. Published rounds: [Race 1](../rounds/race1/), [Race 2](../rounds/race2/), [core4-pilots](../rounds/core4-pilots/), [core4b-ksub-max](../rounds/core4b-ksub-max/), [Sol medium](../rounds/sol-medium/), [Luna medium](../rounds/luna-medium/), [Gleam](../rounds/gleam/), and [shape1 wave 1](../rounds/shape1-wave1/) and [Race 4](../rounds/race4/README.md).
