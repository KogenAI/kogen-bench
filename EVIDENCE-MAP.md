# Evidence map

Reviewed 2026-10-07. This map connects the spec clause inventory in the publication plan to the public benchmark record. It records what the current data can support and the measurement still needed. An implementation or conformance result shows parity with a stated contract; it does not show that the contract improves Build success.

## Reading this map

- **Empirical** means a claim about measured outcomes. The analysis status is shown beside each cited record.
- **Normative product** means a product rule or choice. It may be a current design decision without a comparative result.
- **Safety/correctness** means a behavior required for containment, integrity, or reliable state transitions. Conformance establishes implementation parity only.
- **Implementation freedom** means the spec leaves the implementation choice open or deferred.
- Claim IDs refer to [`results/claim-ledger.jsonl`](results/claim-ledger.jsonl). A row with status **INTERIM**, **CONFOUNDED**, **WITHDRAWN**, or **NOT-RUN** is not evidence of measured superiority.

The evidence map uses a locally sanitized v1.2 clause-reference snapshot in [spec/](spec/README.md). Its original cited content revision is 1118f7fc0dbb042af8c8de2ffd1b85768cf9e2a0; the upstream public sanitization revision is 30d9b25e4eefa7117121de44298fed504b429f4e. [spec/SOURCE.json](spec/SOURCE.json) records original source hashes separately from SHA-256 hashes of the published bytes. All 134 pinned v1.2 fragments linked below are locally verified against that snapshot. The decision ledger is absent, so comprehensive decision-to-clause coverage remains limited and cannot be independently verified.

## Clause map

### [1.1 Process model](#11-process-model)

**Map clause:** CLI and interaction contract.

- **Source heading anchors:** [spec/01-cli.md#11-process-model](spec/01-cli.md#11-process-model); [spec/01-cli.md#12-command-tree-fixed](spec/01-cli.md#12-command-tree-fixed); [spec/01-cli.md#13-argument-grammar](spec/01-cli.md#13-argument-grammar); [spec/01-cli.md#14-help-pages](spec/01-cli.md#14-help-pages); [spec/01-cli.md#15-exit-codes-and-error-lines](spec/01-cli.md#15-exit-codes-and-error-lines); [spec/01-cli.md#16-project-resolution-all-project-commands](spec/01-cli.md#16-project-resolution-all-project-commands); [spec/01-cli.md#17-commands](spec/01-cli.md#17-commands); [spec/01-cli.md#171-intent-shape](spec/01-cli.md#171-intent-shape); [spec/01-cli.md#172-intent-approve---by-](spec/01-cli.md#172-intent-approve---by-); [spec/01-cli.md#173-intent-remove---force](spec/01-cli.md#173-intent-remove---force); [spec/01-cli.md#174-queue-start---detach-and-queue-stop](spec/01-cli.md#174-queue-start---detach-and-queue-stop); [spec/01-cli.md#175-status---watch---json](spec/01-cli.md#175-status---watch---json); [spec/01-cli.md#176-provider-](spec/01-cli.md#176-provider-); [spec/01-cli.md#177-version](spec/01-cli.md#177-version); [spec/01-cli.md#18-signals-and-deprecations](spec/01-cli.md#18-signals-and-deprecations)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Normative product; safety/correctness for exit and state-reporting behavior.
- **Evidence and status:** **NO EMPIRICAL EVIDENCE** for improved agent success or user experience. The `cli-dx-v2`, `ax-and-cli-v3`, and `shaping-ux` entries in [`research/README.md`](research/README.md) are study-index records, not outcome receipts. Related hypotheses: H18, H24, H106–H110, H147.
- **Unresolved measurement:** A paired usability and task-success comparison of the specified headless command surface against alternatives, with the same task, model, effort, and tool access.

### [2.1 Intent `.kogen/intents/<slug>/intent.md`](#21-intent-kogenintentsintentmd)

**Map clause:** Intent, hashes, lint, and project config.

- **Source heading anchors:** [spec/02-formats.md#21-intent-kogenintentsintentmd](spec/02-formats.md#21-intent-kogenintentsintentmd); [spec/02-formats.md#211-slug](spec/02-formats.md#211-slug); [spec/02-formats.md#212-grammar](spec/02-formats.md#212-grammar); [spec/02-formats.md#213-hashes](spec/02-formats.md#213-hashes); [spec/02-formats.md#22-lint](spec/02-formats.md#22-lint); [spec/02-formats.md#23-project-config-kogenprojectyaml](spec/02-formats.md#23-project-config-kogenprojectyaml)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for parsing and hash behavior; empirical for any claim that Intent detail changes Build outcomes.
- **Evidence and status:** [R69](rounds/r69/README.md) and [R71](rounds/r71/README.md) are **INTERIM**. `CL-WA-r69-public-export-coverage` (**INTERIM**) and `CL-WA-r71-public-export-coverage` (**INTERIM**) record export coverage, not an effect estimate. The `intent-format-v3`, `intent-decomposition`, and `test-integrity` entries in [`research/README.md`](research/README.md) do not supply a reconciled comparative claim. Related hypotheses: H07, H70, H80, H86, H89.
- **Unresolved measurement:** Reconcile the registered Intent-detail contrast to exact cell IDs and official grades; separately test parser/hash conformance and any task-success effect.

### [2.4 Acceptance tests and stack adapters](#24-acceptance-tests-and-stack-adapters)

**Map clause:** Acceptance ledger, adapters, and findings.

- **Source heading anchors:** [spec/02-formats.md#24-acceptance-tests-and-stack-adapters](spec/02-formats.md#24-acceptance-tests-and-stack-adapters); [spec/02-formats.md#241-contract](spec/02-formats.md#241-contract); [spec/02-formats.md#242-adapter-interface](spec/02-formats.md#242-adapter-interface); [spec/02-formats.md#243-built-in-adapters](spec/02-formats.md#243-built-in-adapters); [spec/02-formats.md#244-findings-and-identities](spec/02-formats.md#244-findings-and-identities); [spec/02-formats.md#245-shape-artefacts](spec/02-formats.md#245-shape-artefacts)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for ledger interpretation and adapter behavior; empirical for detection and repair benefit.
- **Evidence and status:** [R55](rounds/r55/README.md) and [R70](rounds/r70/README.md) are **INTERIM** for the questions needed here. The Intent coverage, over-strict replay, and candidate counterfactual records are offline diagnostics: `CL-WA-intent-coverage-audit-reported-observation` (**INTERIM**), `CL-WA-overstrict-replay-reported-observation` (**INTERIM**), and `CL-WA-candidate-counterfactual-reported-observation` (**INTERIM**). No prospective live repair effect is established. Related hypotheses: H62–H74, H80, H89, H142.
- **Unresolved measurement:** Test adapter parity, true-defect detection, false blocks, and whether a repair loop improves official task outcomes on a prospective cohort.

### [2.5 Approval, protection and refs](#25-approval-protection-and-refs)

**Map clause:** Approval, journal, cache, and status state.

- **Source heading anchors:** [spec/02-formats.md#25-approval-protection-and-refs](spec/02-formats.md#25-approval-protection-and-refs); [spec/02-formats.md#251-approval-commit-on-refskogenintents-origin](spec/02-formats.md#251-approval-commit-on-refskogenintents-origin); [spec/02-formats.md#252-protected-manifest](spec/02-formats.md#252-protected-manifest); [spec/02-formats.md#253-refs-origin](spec/02-formats.md#253-refs-origin); [spec/02-formats.md#254-landing-commit](spec/02-formats.md#254-landing-commit); [spec/02-formats.md#26-strict-yaml-subset](spec/02-formats.md#26-strict-yaml-subset); [spec/02-formats.md#27-kogen](spec/02-formats.md#27-kogen); [spec/02-formats.md#28-run-dir-and-journal](spec/02-formats.md#28-run-dir-and-journal); [spec/02-formats.md#29-setup-cache](spec/02-formats.md#29-setup-cache); [spec/02-formats.md#210-build-report-status---json](spec/02-formats.md#210-build-report-status---json); [spec/02-formats.md#211-status-derivation](spec/02-formats.md#211-status-derivation)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for approvals, hashes, journal transitions, and state reporting; normative product for the chosen formats and workflow.
- **Evidence and status:** **NO EMPIRICAL EVIDENCE** for comparative Build benefit. The `intent-lifecycle`, `merging-v2`, and `isolation` entries in [`research/README.md`](research/README.md) are study-index records. Existing state and approval conformance cases are parity checks, not outcome studies. Related hypotheses: H16, H17, H65, H145.
- **Unresolved measurement:** Fault-injection and recovery tests for state integrity, plus a separate comparative test only where the product claims a success, reliability, or throughput benefit.

### [3.0 Rules](#30-rules)

**Map clause:** Shaping, approval, and witness.

- **Source heading anchors:** [spec/03-build.md#30-rules](spec/03-build.md#30-rules); [spec/03-build.md#32-shaping-intent-shape](spec/03-build.md#32-shaping-intent-shape); [spec/03-build.md#321-conversations](spec/03-build.md#321-conversations); [spec/03-build.md#322-pre-steps](spec/03-build.md#322-pre-steps); [spec/03-build.md#323-validation-each-pass-in-order](spec/03-build.md#323-validation-each-pass-in-order); [spec/03-build.md#324-repair-message-exact](spec/03-build.md#324-repair-message-exact); [spec/03-build.md#325-results](spec/03-build.md#325-results); [spec/03-build.md#326-concerns-and-progress](spec/03-build.md#326-concerns-and-progress); [spec/03-build.md#327-witness-path-target-contract-pending-measurement](spec/03-build.md#327-witness-path-target-contract-pending-measurement); [spec/03-build.md#328-assumption-recheck](spec/03-build.md#328-assumption-recheck); [spec/03-build.md#33-approval-checks](spec/03-build.md#33-approval-checks)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Normative product for the phase boundary; empirical for shaping and witness effects; safety/correctness for approval enforcement.
- **Evidence and status:** [R69](rounds/r69/README.md) and [R71](rounds/r71/README.md) are **INTERIM**; [R73](rounds/r73/README.md) is **NOT-RUN**. Offline coverage, over-strict, and candidate records carry **INTERIM** claims: `CL-WA-intent-coverage-audit-reported-observation`, `CL-WA-overstrict-replay-reported-observation`, and `CL-WA-candidate-counterfactual-reported-observation`. The records do not establish a Build guarantee or a causal shaping effect. Related hypotheses: H01–H15, H75, H87, H117–H124, H140–H144.
- **Unresolved measurement:** A registered same-task comparison of shaped and unshaped Intents with exact ITT denominators; a separate prospective witness study measuring post-approval failure, end-to-end completion, and witness cost.

### [3.1 The recipe: `ladder`](#31-the-recipe-ladder)

**Map clause:** Ladder, rungs, retries, and completion.

- **Source heading anchors:** [spec/03-build.md#31-the-recipe-ladder](spec/03-build.md#31-the-recipe-ladder); [spec/03-build.md#34-build-orchestration](spec/03-build.md#34-build-orchestration); [spec/03-build.md#35-the-rung-machine](spec/03-build.md#35-the-rung-machine); [spec/03-build.md#36-developer-messages](spec/03-build.md#36-developer-messages)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Empirical for model, effort, ladder, retry, and cost claims; normative product for budgets and route rules.
- **Evidence and status:** [R49](rounds/r49/README.md), [R49b](rounds/r49b/README.md), [R53](rounds/r53/README.md), [R56](rounds/r56/README.md), [R64](rounds/r64/README.md), [R65](rounds/r65/README.md), [R65b](rounds/r65b/README.md), [R66](rounds/r66/README.md), [R68b](rounds/r68b/README.md), [R72](rounds/r72/README.md), [R74](rounds/r74/README.md), and [hc-1](rounds/hc-1/README.md)–[hc-4](rounds/hc-4/README.md) retain separate cohorts. R49, R49b, R65, R65b, and hc-1–hc-4 are **INTERIM**; R68b is **CONFOUNDED**; `CL-WA-r53-public-export-coverage`, `CL-WA-r56-public-export-coverage`, `CL-WA-r64-public-export-coverage`, `CL-WA-r69-public-export-coverage`, `CL-WA-r70-public-export-coverage`, and `CL-WA-r71-public-export-coverage` are **INTERIM**; `CL-WA-r72-lifecycle-and-outcome` is **INTERIM**; R74 is **WITHDRAWN** (`CL-WA-r74-public-export-coverage`, **WITHDRAWN**). Historical comparison summaries `CL-H111-historical-staged-and-direct-comparison` and `CL-H112-historical-route-cost-frontier` are **INTERIM**, `source-reported, not reproducible from public data**. These statuses do not support a pooled ladder or superiority claim. Related hypotheses: H39–H50, H75–H90, H111–H116, H129, H131–H139, H143.
- **Unresolved measurement:** A closed, current-version, same-model comparison of direct and staged routes with exact tasks, effort, effective settings, ITT, cost semantics, and predeclared stopping and analysis rules.

### [3.7 Verification and base-relative checks](#37-verification-and-base-relative-checks)

**Map clause:** Verification and feedback.

- **Source heading anchors:** [spec/03-build.md#37-verification-and-base-relative-checks](spec/03-build.md#37-verification-and-base-relative-checks); [spec/03-build.md#371-composition](spec/03-build.md#371-composition); [spec/03-build.md#372-status-of-each-check-and-excusing](spec/03-build.md#372-status-of-each-check-and-excusing); [spec/03-build.md#373-feedback](spec/03-build.md#373-feedback); [spec/03-build.md#374-advice-that-does-not-change-the-gate](spec/03-build.md#374-advice-that-does-not-change-the-gate)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for checking the final tree; empirical for check selection, false-block rates, and repair benefit.
- **Evidence and status:** [R37](rounds/r37/README.md) is **INVALID**; [R56](rounds/r56/README.md) and [R67b](rounds/r67b/README.md) are **INTERIM**. Offline diagnostics `CL-WA-overstrict-replay-reported-observation` and `CL-WA-candidate-counterfactual-reported-observation` are **INTERIM** and do not represent official ITT outcomes. [X-surface](rounds/x-surface/README.md) is **INTERIM**; its format and fixture claims `CL-WA-x-surface-reported-x-surface-feedback-format` and `CL-WA-x-surface-reported-x-surface-fixture-repair` are **INTERIM**. Related hypotheses: H62–H74, H106–H110.
- **Unresolved measurement:** A prospective last-edit gate study with seeded valid alternatives and known defects, measuring detection, false blocks, repair success, time, and official outcome.

### [3.8 Verdict, audit, selection](#38-verdict-audit-selection)

**Map clause:** Review, auditor, and candidate selection.

- **Source heading anchors:** [spec/03-build.md#38-verdict-audit-selection](spec/03-build.md#38-verdict-audit-selection); [spec/03-build.md#381-verdicts](spec/03-build.md#381-verdicts); [spec/03-build.md#382-build-auditor](spec/03-build.md#382-build-auditor); [spec/03-build.md#383-selector](spec/03-build.md#383-selector)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Empirical for reviewer/auditor accuracy and candidate-selection outcomes; safety/correctness for deterministic selection rules.
- **Evidence and status:** Offline reviewer and selector records are **INTERIM**: `CL-WA-offline-review-reported-observation`, `CL-WA-offline-review3-reported-observation`, `CL-WA-offline-contract-audit-reported-observation`, and `CL-WA-offline-aa-bo3-reported-observation`. [R67b](rounds/r67b/README.md) is **INTERIM**. The offline records do not establish live Build benefit. Related hypotheses: H67–H69, H73, H125–H128.
- **Unresolved measurement:** Calibrate reviewer and auditor precision, recall, false veto/demotion, and selector regret on frozen controls, then measure the policy prospectively in live Builds.

### [3.9 Commit and landing](#39-commit-and-landing)

**Map clause:** Landing, recovery, and queue.

- **Source heading anchors:** [spec/03-build.md#39-commit-and-landing](spec/03-build.md#39-commit-and-landing); [spec/03-build.md#391-commit](spec/03-build.md#391-commit); [spec/03-build.md#392-moved-base](spec/03-build.md#392-moved-base); [spec/03-build.md#393-cas](spec/03-build.md#393-cas); [spec/03-build.md#394-protection-during-a-build](spec/03-build.md#394-protection-during-a-build); [spec/03-build.md#310-recovery](spec/03-build.md#310-recovery); [spec/03-build.md#311-queue-and-drain](spec/03-build.md#311-queue-and-drain)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for rebase, compare-and-swap landing, process recovery, and queue state; empirical for reliability or throughput claims.
- **Evidence and status:** The `merging-v2`, `build-reliability`, and `drain-runtime` entries in [`research/README.md`](research/README.md) are study-index records; conformance cases check parity. No controlled comparative reliability or queue-throughput claim is available in the public record. Related hypotheses: H16, H17, H65, H82, H89, H145–H147.
- **Unresolved measurement:** Fault-injection coverage for concurrent updates, crashes, cancellation, and recovery; a paired reliability/throughput study if the spec claims an improvement over another policy.

### [4.1 Provider port and test seams](#41-provider-port-and-test-seams)

**Map clause:** Provider protocol, streaming, retries, tools, and fake provider.

- **Source heading anchors:** [spec/04-provider.md#41-provider-port-and-test-seams](spec/04-provider.md#41-provider-port-and-test-seams); [spec/04-provider.md#42-chatgpt-responses-wire](spec/04-provider.md#42-chatgpt-responses-wire); [spec/04-provider.md#43-streaming](spec/04-provider.md#43-streaming); [spec/04-provider.md#44-error-classes](spec/04-provider.md#44-error-classes); [spec/04-provider.md#45-deadlines-retries-waits-fallback](spec/04-provider.md#45-deadlines-retries-waits-fallback); [spec/04-provider.md#46-logins-and-credentials](spec/04-provider.md#46-logins-and-credentials); [spec/04-provider.md#47-tools](spec/04-provider.md#47-tools); [spec/04-provider.md#48-fake-provider-conformance](spec/04-provider.md#48-fake-provider-conformance); [spec/04-provider.md#481-endpoints](spec/04-provider.md#481-endpoints); [spec/04-provider.md#482-roles-and-turns](spec/04-provider.md#482-roles-and-turns); [spec/04-provider.md#483-script-steps-json-lines](spec/04-provider.md#483-script-steps-json-lines)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for protocol and retry behavior; empirical for claims about harness, tool surface, latency, or task outcomes.
- **Evidence and status:** [Harness comparison](rounds/harness-compare-1/README.md) is **INTERIM**. [Short](rounds/llm-latency-short/README.md) and [long](rounds/llm-latency-long/README.md) latency records are **DESCRIPTIVE** client-visible timing, not task success. [X-surface](rounds/x-surface/README.md) is **INTERIM** with no agent-output format claim. [Grok frontier](rounds/grok-frontier/README.md) is **NOT-RUN**. Synthetic validation and conformance do not establish an authenticated provider comparison. Related hypotheses: H19–H38, H106–H110, H137–H138.
- **Unresolved measurement:** Authenticated, current-version provider and tool-surface comparisons with matched task, model, effort, retry policy, request accounting, venue, and official grade; test protocol edge cases separately from task efficacy.

### [4.9 Provider requests and prompt caching](#49-provider-requests-and-prompt-caching)

**Map clause:** Cache key, stable prefix, accounting, and checkpoint.

- **Source heading anchors:** [spec/04-provider.md#49-provider-requests-and-prompt-caching](spec/04-provider.md#49-provider-requests-and-prompt-caching); [spec/04-provider.md#491-conversation-key](spec/04-provider.md#491-conversation-key); [spec/04-provider.md#492-byte-stable-prefix](spec/04-provider.md#492-byte-stable-prefix); [spec/04-provider.md#493-tool-result-budget](spec/04-provider.md#493-tool-result-budget); [spec/04-provider.md#494-the-upstream-cut-and-continuation](spec/04-provider.md#494-the-upstream-cut-and-continuation); [spec/04-provider.md#495-usage](spec/04-provider.md#495-usage); [spec/04-provider.md#496-opt-in-context-checkpoint](spec/04-provider.md#496-opt-in-context-checkpoint)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for cache-key and counter semantics; empirical for cache-hit and cost claims.
- **Evidence and status:** [R54](rounds/r54/README.md) is **INTERIM**; [R74](rounds/r74/README.md) is **WITHDRAWN**; [T98 cache smoke](rounds/t98-cache-smoke/README.md) is **INTERIM** (`CL-WA-t98-cache-smoke-reported-observation`, **INTERIM**) and below its stated gate. The [cache replay mechanism](rounds/cache-replay-mechanism/README.md) is **INTERIM** and publishes sanitized request counters; 12 assigned attempts did not dispatch, and the backend run used a different authentication source from the design. It is **DESCRIPTIVE** and does not establish an endpoint effect or cache gate. [T100](rounds/t100-cache-lane/README.md) is **NOT-RUN** (`CL-WA-t100-cache-lane-reported-observation`, **NOT-RUN**). Historical cross-harness values remain **INTERIM** and `source-reported, not reproducible from public data`: `CL-H115-historical-cache-hit-comparison` and `CL-H116-historical-cache-change`. Offline context-store observations are not Build outcomes: [context store](rounds/ctx-store/README.md) is **INTERIM** (`CL-WA-ctx-store-reported-ctx-store-ranked-paths`, **INTERIM**). Historical definitions and epochs are not reconciled to T98. Related hypotheses: H51–H61, H115–H116, H134, H148–H150.
- **Unresolved measurement:** Repeat cache telemetry with a frozen request set, identical token definitions, matched authentication source and venue, and public request-level records; verify any cache gate independently.

### [4.10 Grok provider](#410-grok-provider)

**Map clause:** Grok provider.

- **Source heading anchors:** [spec/04-provider.md#410-grok-provider](spec/04-provider.md#410-grok-provider); [spec/04-provider.md#4101-selection](spec/04-provider.md#4101-selection); [spec/04-provider.md#4102-sign-in](spec/04-provider.md#4102-sign-in); [spec/04-provider.md#4103-request](spec/04-provider.md#4103-request)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Normative product for provider availability; empirical for provider benefit and Build performance.
- **Evidence and status:** [R7](rounds/r7/README.md) is a separate Grok planning arm; [Grok frontier](rounds/grok-frontier/README.md) is **NOT-RUN**. The T99 wire-case receipt is not represented by a public round record in this worktree. No authenticated native-provider benefit claim is established. The build-pick, planner, and frontier roles remain separate. Related hypotheses: H37–H38, H47–H48, H131–H136.
- **Unresolved measurement:** A current authenticated native-provider smoke and a separate matched Build comparison, with role, model, effort, cost accounting, and task cohort fixed in advance.

### [5.1 Process custody (success-relevant: deadlines, hangs, ARG_MAX)](#51-process-custody-success-relevant-deadlines-hangs-arg_max)

**Map clause:** Custody, environment, sandbox, and workspace.

- **Source heading anchors:** [spec/05-sandbox-custody.md#51-process-custody-success-relevant-deadlines-hangs-arg_max](spec/05-sandbox-custody.md#51-process-custody-success-relevant-deadlines-hangs-arg_max); [spec/05-sandbox-custody.md#52-environment](spec/05-sandbox-custody.md#52-environment); [spec/05-sandbox-custody.md#53-sandbox](spec/05-sandbox-custody.md#53-sandbox); [spec/05-sandbox-custody.md#54-workspaces-and-git](spec/05-sandbox-custody.md#54-workspaces-and-git); [spec/05-sandbox-custody.md#55-black-box-behaviours](spec/05-sandbox-custody.md#55-black-box-behaviours)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for process custody, isolation, and containment; empirical for fault-recovery reliability or workspace superiority.
- **Evidence and status:** [R67](rounds/r67/README.md) is **INVALID** and [R69](rounds/r69/README.md) is **INTERIM** for benchmark outcomes. The `isolation` and `build-reliability` entries in [`research/README.md`](research/README.md) are index records. The public record does not establish a cross-design workspace or sandbox reliability advantage. Related hypotheses: H16–H17, H65, H81–H84, H89, H145–H146.
- **Unresolved measurement:** Adversarial fault-injection tests for process death, escaped children, workspace contamination, and recovery; compare workspace designs only with identical task and verification conditions.

### [6.1 Out of core v1](#61-out-of-core-v1)

**Map clause:** Deferred scope and non-goals.

- **Source heading anchors:** [spec/06-non-goals.md#61-out-of-core-v1](spec/06-non-goals.md#61-out-of-core-v1); [spec/06-non-goals.md#62-left-to-the-implementer](spec/06-non-goals.md#62-left-to-the-implementer); [spec/06-non-goals.md#63-never](spec/06-non-goals.md#63-never)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Normative product; implementation freedom where a capability is deferred.
- **Evidence and status:** **NO EMPIRICAL EVIDENCE** that deferred parallel Builds, task splitting, a second witness, or additional providers are ineffective. Related questions include H29, H37, H94–H97, H100–H105, H130, H146, and H148–H153. Product deferral is not a measured negative result. H148–H153 remain research topics with no current spec clause identified in the assigned inventory.
- **Unresolved measurement:** For any deferred capability promoted to a product decision, define a separate paired test and success criterion before implementation or efficacy claims.

### [C.1 Definition](#c1-definition)

**Map clause:** Conformance cases and Quint classification.

- **Source heading anchors:** [spec/CONFORMANCE.md#c1-definition](spec/CONFORMANCE.md#c1-definition); [spec/CONFORMANCE.md#c2-freeze-rule](spec/CONFORMANCE.md#c2-freeze-rule); [spec/CONFORMANCE.md#c3-harness](spec/CONFORMANCE.md#c3-harness); [spec/CONFORMANCE.md#case-file](spec/CONFORMANCE.md#case-file); [spec/CONFORMANCE.md#c4-profiles](spec/CONFORMANCE.md#c4-profiles); [spec/CONFORMANCE.md#c5-cases](spec/CONFORMANCE.md#c5-cases); [spec/CONFORMANCE.md#cli-1](spec/CONFORMANCE.md#cli-1); [spec/CONFORMANCE.md#state-2](spec/CONFORMANCE.md#state-2); [spec/CONFORMANCE.md#approval-172-25-33](spec/CONFORMANCE.md#approval-172-25-33); [spec/CONFORMANCE.md#shape-32](spec/CONFORMANCE.md#shape-32); [spec/CONFORMANCE.md#build-34311](spec/CONFORMANCE.md#build-34311); [spec/CONFORMANCE.md#ladder-31-38](spec/CONFORMANCE.md#ladder-31-38); [spec/CONFORMANCE.md#provider-4](spec/CONFORMANCE.md#provider-4); [spec/CONFORMANCE.md#custody-55](spec/CONFORMANCE.md#custody-55); [spec/CONFORMANCE.md#format-data-files](spec/CONFORMANCE.md#format-data-files); [spec/CONFORMANCE.md#exunit-243](spec/CONFORMANCE.md#exunit-243); [spec/CONFORMANCE.md#c6-comparing-implementations](spec/CONFORMANCE.md#c6-comparing-implementations); [spec/CONFORMANCE.md#appendix-a-the-kt-fixture](spec/CONFORMANCE.md#appendix-a-the-kt-fixture); [spec/CONFORMANCE-v1.2-CASES.md#p1-conversation-key-is-present-and-stable](spec/CONFORMANCE-v1.2-CASES.md#p1-conversation-key-is-present-and-stable); [spec/CONFORMANCE-v1.2-CASES.md#p2-thread-identity-changes-with-the-rung-build-cache-affinity-does-not](spec/CONFORMANCE-v1.2-CASES.md#p2-thread-identity-changes-with-the-rung-build-cache-affinity-does-not); [spec/CONFORMANCE-v1.2-CASES.md#p3-prompt-prefix-is-byte-identical-from-turn-2](spec/CONFORMANCE-v1.2-CASES.md#p3-prompt-prefix-is-byte-identical-from-turn-2); [spec/CONFORMANCE-v1.2-CASES.md#p4-completion-is-finish-not-text](spec/CONFORMANCE-v1.2-CASES.md#p4-completion-is-finish-not-text); [spec/CONFORMANCE-v1.2-CASES.md#p5-tool-result-budget](spec/CONFORMANCE-v1.2-CASES.md#p5-tool-result-budget); [spec/CONFORMANCE-v1.2-CASES.md#p6-responses-and-lite-shapes](spec/CONFORMANCE-v1.2-CASES.md#p6-responses-and-lite-shapes); [spec/CONFORMANCE-v1.2-CASES.md#p7-upstream-cut-continues-the-turn](spec/CONFORMANCE-v1.2-CASES.md#p7-upstream-cut-continues-the-turn); [spec/CONFORMANCE-v1.2-CASES.md#p8-deadlines-and-retries](spec/CONFORMANCE-v1.2-CASES.md#p8-deadlines-and-retries); [spec/CONFORMANCE-v1.2-CASES.md#p9-usage](spec/CONFORMANCE-v1.2-CASES.md#p9-usage); [spec/CONFORMANCE-v1.2-CASES.md#p10-grok-wire](spec/CONFORMANCE-v1.2-CASES.md#p10-grok-wire); [spec/CONFORMANCE-v1.2-CASES.md#p11-scheduling-and-status](spec/CONFORMANCE-v1.2-CASES.md#p11-scheduling-and-status); [spec/CONFORMANCE-v1.2-CASES.md#p12-rails-detection](spec/CONFORMANCE-v1.2-CASES.md#p12-rails-detection); [spec/CONFORMANCE-v1.2-CASES.md#p13-checkpoint-epoch](spec/CONFORMANCE-v1.2-CASES.md#p13-checkpoint-epoch); [spec/quint/CLASSIFICATION.md#prose-sections](spec/quint/CLASSIFICATION.md#prose-sections); [spec/quint/CLASSIFICATION.md#quint-slices](spec/quint/CLASSIFICATION.md#quint-slices); [spec/quint/CLASSIFICATION.md#deferred-work-and-promotion-evidence](spec/quint/CLASSIFICATION.md#deferred-work-and-promotion-evidence)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Safety/correctness for implementation parity; implementation freedom for the placement of untested or optional behavior.
- **Evidence and status:** `executable-specs`, `kogen-core-spec`, and Quint entries are listed in [`research/README.md`](research/README.md); the census is an index, not a verification receipt. [R70](rounds/r70/README.md), [R70 rerun](rounds/r70-rve-rerun/README.md), and [R70 extension](rounds/r70-rve-ext/README.md) concern language implementation cohorts and are not conformance evidence. No public record establishes semantic equivalence of the Quint translation or a task-success benefit from conformance. Related hypotheses: H91–H99.
- **Unresolved measurement:** Publish the exact frozen suite revision and cases, verify spec-to-implementation semantics and the Quint translation, and keep parity results separate from any live agent-success comparison.

### [Sources and precedence](#sources-and-precedence)

**Map clause:** Sources and precedence.

- **Source heading anchors:** [spec/README.md#sources-and-precedence](spec/README.md#sources-and-precedence)

- **Spec revision / decision reference:** v1.2 (pinned fragment locally verified); section-level D references are listed in the source classification. **Last reviewed:** 2026-10-07.
- **Type:** Normative source precedence and historical record; empirical only where a cited benchmark claim is attached.
- **Evidence and status:** [R53](rounds/r53/README.md), [R56](rounds/r56/README.md), [R57](rounds/r57/README.md), [R64](rounds/r64/README.md), [R69](rounds/r69/README.md), [R70](rounds/r70/README.md), [R71](rounds/r71/README.md), [R72](rounds/r72/README.md), [R74](rounds/r74/README.md), and [T98](rounds/t98-cache-smoke/README.md) remain separate by cohort and status. Their coverage and denominator rows are **INTERIM** unless a cited claim says otherwise; R74 remains **WITHDRAWN**. Historical source claims in `CL-WA-r53-source-reported-denominator-variants`, `CL-WA-r56-source-reported-denominator-variants`, `CL-WA-r57-source-reported-denominator-variants`, `CL-WA-r64-source-reported-denominator-variants`, `CL-WA-r69-source-reported-denominator-variants`, `CL-WA-r70-source-reported-denominator-variants`, `CL-WA-r71-source-reported-denominator-variants`, and `CL-WA-r74-source-reported-denominator-variants` are **INTERIM** or **WITHDRAWN** as recorded in the ledger. Repeated summary percentages are not additional experiments. Related hypotheses: H86–H90, H111–H116.
- **Unresolved measurement:** Reconcile each cited claim to immutable cell IDs, official grades, exact cohort, current harness/Kogen revision, model/effort, accounting definition, and registered analysis rule; preserve corrections and superseded cohorts in the provenance record.

## Decision-ID coverage

Every v1.2 clause fragment linked above is locally verified against the published snapshot. The source classification's section-level D references are present, but the underlying decision ledger is absent, so comprehensive decision-to-clause coverage remains limited and cannot be independently verified. Product decisions with no measured claim should retain an explicit **NORMATIVE** or **NO EMPIRICAL EVIDENCE** label.
