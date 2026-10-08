# F10 Agent-facing output

This page records evidence for H106–H110. Proposed output formats, traces, logs, and agent-facing rules have not passed a complete live repair comparison in the public record.

## Hypotheses and current status

| ID | Falsifiable proposition | Current evidence status |
|---|---|---|
| H106 | A compact structured format can reduce tokens while remaining easier for agents to parse than JSON, YAML, or TOML and more useful than plain text. | NOT ESTABLISHED. No complete, matched parse-and-repair comparison is published. |
| H107 | Translating tool output into a compact format, with a fallback when needed, improves agent comprehension. | NOT ESTABLISHED. No public round-trip and live task comparison is linked. |
| H108 | Compact stack traces and error reports help an agent find and fix the correct code. | NOT ESTABLISHED. No controlled trace-format repair outcome is available. |
| H109 | Structured logs improve diagnosis without removing useful detail. | NOT ESTABLISHED. No matched logging-format study is published. |
| H110 | Agent-facing output rules should include only formats and checks with measured improvements. | INTERIM. A partial output-feedback cohort exists, but does not establish a format preference or completion benefit. |

## Run and claim record

The reported x-surface observations have no exact task or cell join in the public result exports. Each reported value below remains attached to its separate claim; none is an official benchmark estimate.

| experiment_id | arm and task set | model / effort | Kogen and harness revision | host / epoch | planned / started / finished / graded / ITT | outcome | status and correction | claim ID | public receipt and raw records |
|---|---|---|---|---|---|---|---|---|---|
| x-surface-feedback-format | Feedback-format cohort; exact task and arm assignments unavailable | Compared models are reported; exact models and effort unavailable | Exact Kogen and harness revisions unavailable | Host and epoch unavailable | 16 planned / 8 completed as source-reported; scored and ITT counts not recovered | Partial cohort; no output-format claim. | INTERIM; source-reported, not reproducible from public data. | CL-WA-x-surface-reported-x-surface-feedback-format INTERIM | [round page](../rounds/x-surface/README.md), [reported data](../rounds/x-surface/reported-data.json), [claim ledger](../results/claim-ledger.jsonl) |
| x-surface-fixture-repair | Small fixture repair subset; exact task IDs unavailable | Model names, effort, and arm mapping unavailable | Exact Kogen and harness revisions unavailable | Host and epoch unavailable | Planned, started, finished, graded, and ITT counts not recovered | The models are reported tied at 2/2 versus 2/2 on this fixture subset. | INTERIM; source-reported, not reproducible from public data. | CL-WA-x-surface-reported-x-surface-fixture-repair INTERIM | [round page](../rounds/x-surface/README.md), [reported data](../rounds/x-surface/reported-data.json), [claim ledger](../results/claim-ledger.jsonl) |
| x-surface-remaining-rep | Remaining repetition in the output-feedback cohort; task ID unavailable | Model and effort unavailable | Exact Kogen and harness revisions unavailable | Host and epoch unavailable | Unrun at cited cutoff; no scored or ITT cohort | No outcome was reported for the remaining repetition. | INTERIM; source-reported, not reproducible from public data. | CL-WA-x-surface-reported-x-surface-remaining-rep INTERIM | [round page](../rounds/x-surface/README.md), [reported data](../rounds/x-surface/reported-data.json), [claim ledger](../results/claim-ledger.jsonl) |

## Design implications

The current evidence supports treating agent-facing formats and diagnostic rules as proposals. It provides no basis for making a custom compact format, transformed tool output, compressed trace, or structured logger a default on the strength of claimed agent preference.

## What this evidence does not show

The partial fixture observations do not establish parseability, comprehension, reduced token use, faster diagnosis, successful repair, or improved task completion. Synthetic validation is not an authenticated agent comparison.

## Smallest open tests

Freeze equivalent error cases and tasks, compare each output format with plain text and a common structured baseline, and record parse errors, diagnosis accuracy, repair success, tokens, wall time, and cost. Preserve a held-out set and require exact public task and run identifiers.

