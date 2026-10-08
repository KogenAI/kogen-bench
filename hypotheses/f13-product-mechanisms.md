# F13 — Late-September product mechanisms

**Status: NO EMPIRICAL EFFICACY EVIDENCE.** These propositions concern product routes and workflow mechanisms. The public record does not contain controlled comparisons that establish the claimed success, cost, reliability, or operator benefit. Product choices may still be recorded as decisions, but they are not benchmark findings.

## Hypotheses

- **H140 — Cross-harness route.** Claude as the primary builder with Codex adversarial review may outperform an agent-only route on completion quality or cost. Compare the full route with a matched single-harness control.
- **H141 — Jev audit during Shaping.** A controller-guaranteed Jev audit during Shaping may catch feasibility or context errors before approval. Compare audit findings, false alarms, and downstream Build outcomes with the audit disabled.
- **H142 — Vertical integration.** Building and integrating the same requested feature may reduce wasted or brittle partial implementations compared with plumbing work that is not tied to an end-to-end Intent. Compare completion and rework on matched tasks.
- **H143 — Stashed work reuse.** Reusing valid existing work may reduce Build time without increasing correctness failures. Compare against a clean-start control with the same acceptance suite.
- **H144 — Shaping preflight.** A bounded, low-cost preflight audit may verify material risks before longer Shaping work. Compare audit cost, detected risks, false blocks, and Build outcomes against a matched no-preflight control.
- **H145 — Build reliability.** Reliability changes may prevent repeated costly cycles and classify environment failures separately from semantic failures. Compare retries, successful completion, and total cost under injected and naturally occurring failure classes.
- **H146 — Parallel Builds on a second Mac.** A second Mac may raise throughput while preserving Build ownership and verification. Compare serial and parallel operation on the same eligible workload, including coordination, queue, and grading time.
- **H147 — Build status and alerts.** Showing current stage/check state and offering a completion alert may reduce unattended waiting and missed failures. Measure detection time, missed events, and operator wait; this is not a model pass-rate hypothesis.

## Experiment register

“Not established” is an evidence status, not a claim that a product feature does not exist. Reproduction metadata is reported only when a public round record supplies it; other fields remain unrecovered.

| experiment_id | Arm; task set; model/effort | Revision; host/epoch | planned / started / finished / graded / ITT n | Outcome and status | Correction or supersession | Claim ID and public receipt |
|---|---|---|---|---|---|---|
| H140 cross-harness adversarial roles | No matched cross-harness outcome arm identified; task IDs and models/effort are not available in the public evidence index. | Harness/Kogen revisions, host, and epoch not identified. | Not established. | No controlled success or cost result; **NO EMPIRICAL EVIDENCE**. | An implementation or named Intent is not evidence of comparative benefit. | No claim ID assigned; [research census](../research/README.md) lists the topic without a scored public receipt. |
| H141 controller-guaranteed shaping audit | No exact audit-on/audit-off Build comparison identified; task, auditor model/effort, and audit policy not recovered. | Revisions, host, and epoch not identified. | Not established. | No isolated audit benefit or false-alarm measurement; **NO EMPIRICAL EVIDENCE**. | Jev routing/triage diagnostics are separate from an integrated Shaping audit. | No claim ID assigned; [Jev route context](../rounds/jev-route-ctx/README.md) and [Jev triage context](../rounds/jev-triage-ctx/README.md) are adjacent diagnostics, not this treatment. |
| H142 same-Intent vertical integration | No matched vertical-vs-plumbing task cohort identified; models and effort not recovered. | Revisions, host, and epoch not identified. | Not established. | No outcome comparison; **NO EMPIRICAL EVIDENCE**. | A rescope or implementation request is not a measured integration effect. | No claim ID assigned; [research census](../research/README.md). |
| H143 existing-stash reuse | No controlled reuse-vs-clean-start Build comparison identified; task and model/effort not recovered. | Revisions, host, and epoch not identified. | Not established. | No validated time or correctness effect; **NO EMPIRICAL EVIDENCE**. | No pass or wall result can be inferred from whether a stash was available. | No claim ID assigned; [research census](../research/README.md). |
| H144 shaping preflight audit | No matched preflight-on/off comparison identified; no cost, risk-detection, or downstream Build measure is available. | Revisions, host, and epoch not identified. | Not established as an efficacy cohort. | No evidence that the audit is cheap, bounded, or improves completion; **NO EMPIRICAL EVIDENCE**. | A failed Build after a preflight design does not estimate the audit's effect. | No claim ID assigned; [research census](../research/README.md). |
| H145 Build reliability and failure classification | [x-recovery](../rounds/x-recovery/README.md) has a fault/checkpoint record, but the per-arm extraction is not reconciled. Models/effort and task IDs are not recovered here. | Exact revision, host, and epoch by arm not established. | Not established as a joined comparison. | The public summary does not yield a reliability or cost effect; **INTERIM, no efficacy claim**. | Keep fault-injection, scripted-provider checks, and live model-backed Builds separate. | No H145 claim ID assigned in the claim ledger; [x-recovery](../rounds/x-recovery/README.md), [research census](../research/README.md). |
| x-parallel planned-DAG pilot (adjacent to H146) | Solo vs planned DAG on two reported tasks; per-cell model/effort and task IDs are not recovered. | Kogen/harness revisions and host epoch are not recovered. | Two tasks × two repetitions per arm is source-reported; exact lifecycle and ITT counts are not joined. | Both arms are reported at 4/4 passes; the planned DAG is reported at about 1.4× wall and 1.9× requests. **Source-reported, not reproducible from public data.** The pilot did not test the proposed second-Mac workflow. | Retain as a small topology diagnostic, not a throughput or ownership-safety result. | [x-parallel page](../rounds/x-parallel/README.md); [reported data](../rounds/x-parallel/reported-data.json). |
| H147 status and completion alert | No status/alert-on vs control cohort; no measured user or Build outcome. | Revisions, host, and epoch not identified. | Not established. | No measured reduction in waiting or missed failures; **NO EMPIRICAL EVIDENCE**. | The x-surface feedback-format study is not a stage/status/alert test. | No claim ID assigned; [x-surface](../rounds/x-surface/README.md) is adjacent only. |

## Design implications

- Record product constraints such as Build ownership, required verification, and truthful status as **normative product** or **safety/correctness** decisions where appropriate.
- Keep empirical claims separate from implementation completion, roadmap requests, and operational anecdotes.
- For workflow features, measure the outcome named by the hypothesis: success and cost for route changes, defect detection for audits, reliability under faults, and operator detection/wait for status and alerts.

## Explicit non-implications

- The absence of a comparative result does not disprove a mechanism or require removing a product feature.
- A small parallel-DAG pilot does not establish second-host throughput, correct ownership, or verification safety.
- Manually trying an alert does not show that it improves detection or reduces waiting.
- A preflight failure does not show that preflight is beneficial or harmful.

## Smallest open tests

- For H140–H144, preregister a small matched pilot with immutable task IDs, exact harness and Kogen commits, model/effort per role, a no-feature control, explicit cost/time endpoints, and complete grades.
- For H145, inject known transport, timeout, setup, and semantic failures; verify classification and measure total retries/cost before comparing a live cohort.
- For H146, compare the same parallelizable workload under serial and second-Mac operation, with per-Build ownership and verification receipts.
- For H147, measure alert delivery, missed failures, and operator detection time in a blinded or randomized status-display comparison.

