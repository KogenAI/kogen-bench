# F09 Campfire and web stacks

This page records evidence for H100–H105. The web-stack and porting propositions remain design questions; a withdrawn runtime lane provides no performance result.

## Hypotheses and current status

| ID | Falsifiable proposition | Current evidence status |
|---|---|---|
| H100 | A parity-checked Elixir/Phoenix implementation can approach or beat the selected Rust implementation on a matched Campfire feature. | NOT ESTABLISHED. Both public Campfire lanes were withdrawn before formal cells. |
| H101 | A small representative feature can be compared fairly across stacks using SQLite, matched optimization, and disabled caching. | NOT ESTABLISHED. No qualifying matched feature cohort ran. |
| H102 | A stronger Exqlite or Ecto implementation changes the relative runtime result. | NOT ESTABLISHED. No public matched adapter or implementation comparison is available. |
| H103 | Throughput measurements reject implementations that drop messages or otherwise fail correctness. | NOT ESTABLISHED. No public correctness-control results are available for the Campfire comparison. |
| H104 | The chosen feature is representative, reviewable, and suitable for a public web-stack benchmark. | NOT ESTABLISHED. No completed public review of the feature-selection rule is linked. |
| H105 | Rails agent tasks can be ported to Elixir or Rust so agent performance can be compared on equivalent tasks. | NOT ESTABLISHED. The public Elixir-port round does not establish a matched cross-stack agent comparison. |

## Run and claim record

For Campfire, a formal cell is an execution in the proposed comparison, separate from preparation smokes. No Kogen Build was run, so Kogen commit is not applicable. The planned formal populations below are not observed outcomes.

| experiment_id | arm and task set | model / effort | Kogen and harness revision | host / epoch | planned / started / finished / graded / ITT | outcome | status and correction | claim ID | public receipt and raw records |
|---|---|---|---|---|---|---|---|---|---|
| campfire-lane1 | Runtime comparison design; exact feature arm and task set are in the withdrawal receipt | No model execution in formal lane | Kogen not applicable; separate benchmark-driver commit not recorded | Not applicable | 30 / 0 / 0 / 0 / 0 formal cells | No formal comparison cell ran. | WITHDRAWN before formal execution; no efficacy claim. | CL-WA-campfire-lane1-formal-cell-lifecycle WITHDRAWN | [round page](../rounds/campfire-lane1/README.md), [claim ledger](../results/claim-ledger.jsonl) |
| campfire-lane2 | Revised runtime comparison design; exact feature arm and task set are in the withdrawal receipt | No model execution in formal lane | Kogen not applicable; separate benchmark-driver commit not recorded | Not applicable | 50 / 0 / 0 / 0 / 0 formal cells; preparation smokes are separate | No formal comparison cell ran. | WITHDRAWN before formal execution; no efficacy claim. | CL-WA-campfire-lane2-formal-cell-lifecycle WITHDRAWN | [round page](../rounds/campfire-lane2/README.md), [claim ledger](../results/claim-ledger.jsonl) |
| R55 Elixir task ports | Five Rails-derived tasks with direct Codex arms; exact task IDs and exported arm labels are in the round receipt | Luna max and Sol high are recorded in the source summary; exact builds are unavailable | No Kogen Build revision established for these direct model builds | US and EU public host labels; epoch balance not established | Planned allocation is not derivable; public run-record delivery table is available; official ITT is not reconciled to the research summary | Task-level captured deliveries exist, but this does not compare Elixir application throughput with Rust or demonstrate equivalence to an unchanged Rails task. | INTERIM; corrections and task mapping remain in the round receipt. | No B1 claim ID assigned | [R55 page](../rounds/r55/README.md), [run-record export](../results/run-records/index.json), [result export](../results/cells.jsonl) |

## Design implications

The withdrawn Campfire lanes are status records, not null performance results. R55 concerns agent work on Elixir task ports, not a server-runtime comparison. Keep those study questions separate.

## What this evidence does not show

The available records do not establish runtime or web-stack superiority, matched feature parity, message-delivery correctness, a representative feature set, or cross-stack agent equivalence. A reported external performance result would use a different setup and is not evidence from these public lanes.

## Smallest open tests

Freeze a minimal feature and acceptance suite before implementation; use the same database, optimization, cache policy, and load profile; verify message counts and semantics before measuring throughput. For agent task ports, publish source revision, task and grader identities and require equivalent task behavior before comparing stacks.

