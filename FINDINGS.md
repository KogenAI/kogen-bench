# Findings

These sections are an entry point into the public evidence. Each summarizes the hypothesis family and its round pages; round pages remain the authority for run history. Where a joined result is unavailable, the fields say “not recorded.” No source-reported headline is repeated here as a verified result.

## F01 Shape, Intent and plan

**Hypothesis:** H01–H15 ask whether shaping, plans, probes, and stage choices improve completion or cost under defined conditions. The public record does not establish a shaping effect or a Build guarantee.

**What ran:** R69 and R71 have interim stage and Intent records; R72 is a separate descriptive ladder comparison; R73 is not run; R74 is withdrawn. The L3 repair lane is **DESCRIPTIVE**: two rescues among six selected failed implementations, with per-test preservation unverified. R69's L0 reconciliation reconstructs 400 assigned and 396 included ITT rows; 150 of 327 internal grades exact-join the refreshed 2026-10-07 public outcome export by `cell_id`, so [CL-WA-r69-source-reported-denominator-variants](results/claim-ledger.jsonl) remains **INTERIM**. Offline Intent, test-quality, and saved-candidate audits are different units from live Builds.

**Result:** The L3 **DESCRIPTIVE** round records 2/6 repairs rescued, below its three-rescue threshold; preservation is unmeasured, environment evidence is absent, and rule chronology is unproven. [CL-L3-REPAIR-RESCUE-RATE](results/claim-ledger.jsonl) is **STATUS_ONLY** because the CSV summary does not include per-test pass sets or independent grade receipts. No reconciled H01–H15 shaping cohort is recorded. Status remains round-specific: R69/R71/R72 are interim, R73 is not run, and R74 is withdrawn.

**What it does not show:** The L3 result does not establish that repair increases completion over restarting or preserves each previously passing test. These records also do not establish that added Intent detail always helps, that a witness guarantees a successful Build, or that shaping is worth its cost.

**Evidence:** [F01 hypothesis page](hypotheses/f01-shape-intent-plan.md), [L3 repair](rounds/l3-repair/README.md), [L3 status-only claim](results/claim-ledger.jsonl), [R69](rounds/r69/README.md), [L0 reconciliation](rounds/l0-reconcile/README.md), [R71](rounds/r71/README.md), [R72](rounds/r72/README.md), [R73](rounds/r73/README.md), [R74](rounds/r74/README.md), [Intent coverage audit](rounds/intent-coverage-audit/README.md), [over-strict replay](rounds/overstrict-replay/README.md), [candidate counterfactual](rounds/candidate-counterfactual/README.md). Spec map: [Intent](EVIDENCE-MAP.md#21-intent-kogenintentsintentmd) and [Shaping and approval](EVIDENCE-MAP.md#30-rules).

## F02 Isolation, landing and interface

**Hypothesis:** H16–H18 ask whether workspace isolation, rebase-based landing, or a command interface improves reliability or usability. The family page identifies these as product and reliability choices without a controlled superiority study.

**What ran:** The public family page lists isolation, merging, and shaping-interface research, but no controlled public round with a matched outcome cohort is identified.

**Result:** Numerator/denominator: not recorded. Unit: workspace interference, landing errors, or interface task outcomes. Date: not recorded. Status: no comparative efficacy result identified.

**What it does not show:** A specified correctness contract or implementation-conformance case does not show that the design improves task completion or usability.

**Evidence:** [F02 hypothesis page](hypotheses/f02-isolation-landing-interface.md); its experiment register links the available topic-level records and states their limits. Spec map: [CLI and interaction](EVIDENCE-MAP.md#11-process-model), [approval and refs](EVIDENCE-MAP.md#25-approval-protection-and-refs), and [landing](EVIDENCE-MAP.md#39-commit-and-landing).

## F03 Harness and loop

**Hypothesis:** H19–H38 ask how harness, tool surface, prompt, loop, and helper topology affect success, time, and cost. No general harness or loop winner is established.

**What ran:** The September harness-pick and kh-compare captures, claim-B and combined panels, the kh climb, and exploratory role, surface, race, and parallel records have separate task sets and incomplete outcome joins. The formal Grok frontier is not run.

**Result:** Numerator/denominator: no exact public grade join is available for the recent captured harness panels. Unit: official task pass. Date: not recorded as a common scored cohort date. Status: interim or confounded by round; no general winner.

**What it does not show:** Captured deliveries, exploratory summaries, and scripted checks do not establish that any harness, tool surface, or helper topology improves scored Builds.

**Evidence:** [F03 hypothesis page](hypotheses/f03-harness-loop.md), [harness-pick](rounds/harness-pick-2026-09-29/README.md), [kh-compare](rounds/kh-compare-2026-09-29/README.md), [claim-B screen](rounds/claim-b-screen-1/README.md), [claim-B rerun](rounds/claim-b-rerun-1/README.md), [combined panel](rounds/confirm-combined-1/README.md), [kh climb](rounds/kh-climb/README.md), [Grok frontier](rounds/grok-frontier/README.md). Spec map: [ladder recipe](EVIDENCE-MAP.md#31-the-recipe-ladder) and [provider port](EVIDENCE-MAP.md#41-provider-port-and-test-seams).

## F04 Models, efforts and routing

**Hypothesis:** H39–H50 ask whether model, effort, role allocation, or routing changes the completion-cost-time frontier. The evidence is panel-specific and does not establish a default model or route.

**What ran:** The family page links exploratory model and ladder records, historical model/effort rounds, and offline route diagnostics. R66 lacks its historical high-effort anchor cohort; R68b records an effort clamp; R72 and R74 remain separate.

**Result:** Numerator/denominator: not recorded for a complete matched model-and-effort frontier. Unit: official Build pass, cost, or wall time. Date: no common comparison date recorded. Status: interim, confounded, or withdrawn by round.

**What it does not show:** Offline route agreement and separate historical cohorts do not establish that escalation or task-text routing improves live Build outcomes.

**Evidence:** [F04 hypothesis page](hypotheses/f04-models-routing.md), [R66](rounds/r66/README.md), [R68b](rounds/r68b/README.md), [R72](rounds/r72/README.md), [R74](rounds/r74/README.md), [Jev route context](rounds/jev-route-ctx/README.md), [Jev triage context](rounds/jev-triage-ctx/README.md), [model screen](rounds/x-models/README.md), [ladder inventory](rounds/x-ladder/README.md). Spec map: [ladder recipe](EVIDENCE-MAP.md#31-the-recipe-ladder), [Grok provider](EVIDENCE-MAP.md#410-grok-provider), and [provider port](EVIDENCE-MAP.md#41-provider-port-and-test-seams).

## F05 Context, Jev and cache

**Hypothesis:** H51–H61 ask whether caching, context preparation, compaction, or code inspection reduces cost or improves downstream outcomes. The available records do not establish those live Build benefits.

**What ran:** R54 records an interim context handoff comparison; Jev and Tidewave pages are offline or partial diagnostics; T98 is a cache smoke and T100 is not run. Language cohorts remain separate from cache and context measures.

**Result:** Numerator/denominator: not recorded for a reconciled Build-success contrast. Unit: cache requests, context diagnostics, and official Build passes are separate. Date: no matched request or Build date is recorded. Status: interim diagnostics; T98 is telemetry only and T100 is not run.

**What it does not show:** The cache smoke does not establish a cache-fix effect on success, time, or cost; route agreement and context retrieval do not establish better Builds.

**Evidence:** [F05 hypothesis page](hypotheses/f05-context-cache-jev.md), [R54](rounds/r54/README.md), [T98 cache smoke](rounds/t98-cache-smoke/README.md), [T100 cache lane](rounds/t100-cache-lane/README.md), [E06 context](rounds/e06-context/README.md), [E09 Tidewave](rounds/e09-tidewave/README.md), [Jev route context](rounds/jev-route-ctx/README.md), [Jev triage context](rounds/jev-triage-ctx/README.md). Spec map: [provider requests and prompt caching](EVIDENCE-MAP.md#49-provider-requests-and-prompt-caching).

## F06 Checks, review and recovery

**Hypothesis:** H62–H74 ask whether checks, review, and recovery improve defect detection or completion at acceptable cost. The public page treats false blocks and test quality as risks to measure; it does not qualify a default veto or repair policy.

**What ran:** L6 adds an offline, request-scoped auditor replay with 79 valid verdicts from 80 requests ([CL-L6-AUDITOR-ADVISORY-REPLAY](results/claim-ledger.jsonl)); neither auditor met both predeclared targets. L3b is **VALID** for its registered rule (REPAIR minus CONTINUE rescues = 2, threshold ≥2); its KEEP applies to these eight selected failures only, with arm counts on the round page. Other records include offline review and contract audits, offline best-of analysis, over-strict test replay, and saved-candidate counterfactuals.

**Result:** L3b's observed difference for the selected failures is conditional on a private per-test no-regression check; it does not validate a general KEEP policy. Most scored cells lack Standard records, host captures followed execution, rule timing is unproven, and deviation and exposure are disclosed on the round page. No reconciled prospective review Build comparison is recorded. Unit: offline audit cases and candidate counterfactuals remain separate from official Build passes. Status: descriptive or interim; no general live efficacy estimate.

**What it does not show:** Offline counts do not establish that a reviewer improves acceptance, that checks preserve defect detection while reducing time, or that recovery increases completion.

**Evidence:** [F06 hypothesis page](hypotheses/f06-checks-review-recovery.md), [L3b repair vs continue](rounds/l3b-repair-vs-continue/README.md), [L6 auditor replay](rounds/l6-auditor-replay/README.md), [L6 status-only claim](results/claim-ledger.jsonl), [offline review](rounds/offline-review/README.md), [offline review 3](rounds/offline-review3/README.md), [offline contract audit](rounds/offline-contract-audit/README.md), [offline A/A selection analysis](rounds/offline-aa-bo3/README.md), [over-strict replay](rounds/overstrict-replay/README.md), [candidate counterfactual](rounds/candidate-counterfactual/README.md), [recovery inventory](rounds/x-recovery/README.md). Spec map: [acceptance tests](EVIDENCE-MAP.md#24-acceptance-tests-and-stack-adapters), [verification](EVIDENCE-MAP.md#37-verification-and-base-relative-checks), and [review and selection](EVIDENCE-MAP.md#38-verdict-audit-selection).

## F07 Tasks, grading and method

**Hypothesis:** H75–H90 cover task selection, grading, registration, ITT, host balance, and reporting. Method requirements and incomplete records do not establish a broad Kogen advantage or a validated allocation policy.

**What ran:** Hill-climb pages record development iterations; the night record is documentary; task and grade audits cover separate populations. Guard cells, stopped slots, official grades, and counterfactual outcomes remain distinct.

**Result:** Numerator/denominator: not recorded for a single balanced, reconciled cohort across these method questions. Unit: task, grade, host, or allocation diagnostic, depending on the study. Date: no shared result date recorded. Status: interim, invalid, or descriptive by round.

**What it does not show:** A development climb or a cross-stack sample does not establish that a lever caused an outcome or that a task set represents work beyond the selected tasks.

**Evidence:** [F07 hypothesis page](hypotheses/f07-tasks-method.md), [hc-1](rounds/hc-1/README.md), [hc-2](rounds/hc-2/README.md), [hc-3](rounds/hc-3/README.md), [hc-4](rounds/hc-4/README.md), [night record](rounds/night-2026-10-01/README.md), [R70 original language cohort](rounds/r70-rve/README.md), [R70 rerun](rounds/r70-rve-rerun/README.md). Spec map: [sources and precedence](EVIDENCE-MAP.md#sources-and-precedence).

## F08 Language and executable spec

Cross-round review: [Rust versus Elixir evidence synthesis](research/RUST-VS-ELIXIR-EVIDENCE.md).

**Hypothesis:** H91–H99 ask whether language or executable specifications change runtime, parity, or task outcomes. The records inform a bounded product choice but do not establish a broad language effect.

**What ran:** The stack one-shot conformance round compares the planned Rust, Go, and TypeScript builds at their first recorded post-build conformance snapshots. It is **DESCRIPTIVE** because suite versions, spec revisions, hosts, and gate timing differ. The Sol-medium language replication adds 27 new cells and 31 reused cells; its task-equal rates are a post-hoc sensitivity analysis ([CL-SOL-LANG-REPLICATION-POSTHOC-EQUAL-TASK](results/claim-ledger.jsonl), **STATUS_ONLY**). Other R70 original, fixed-skeleton rerun, extension, compile-time, and task-eight smoke records are distinct cohorts.

**Result:** Source-reported, not reproducible from public data: one-shot snapshots show Rust at 76/196 cases (38.8%), Go at 61/236 on the historical macOS v1.2 suite and 76/278 on Linux v1.3, and TypeScript at 90/244 recorded case rows before its partial run stopped. The later Rust INT6 and final v1.3 results are separate from the one-shot comparison. In the related Sol-medium replication, raw totals were Rust 18/20, Go 18/20, and TS-Bun 15/18. Its post-hoc equal-task mean is Rust 90.3%, Go 88.9%, and TS-Bun 83.3%; [CL-SOL-LANG-REPLICATION-POSTHOC-EQUAL-TASK](results/claim-ledger.jsonl) is **STATUS_ONLY**. Rust conformed most by pass fraction in the one-shot snapshots and is top or tied-top across the recorded measures; the evidence does not support a matched causal language effect. Kogen continues in Rust.

**What it does not show:** The records do not establish that Rust is broadly superior to the other tested languages or that executable specifications improve agent completion. Different suite sizes and spec revisions, the partial TypeScript run, Go/TypeScript access to Rust reference code, different hosts, and different gate timing limit the stack comparison. The Sol-medium result has a separate status and limits; its pooled language comparison is not justified.

**Evidence:** [Stack one-shot conformance](rounds/stack-oneshot-conformance/README.md), [Sol-medium language replication](rounds/lang-sol-replication/README.md), [post-hoc equal-task claim](results/claim-ledger.jsonl), [F08 hypothesis page](hypotheses/f08-language-spec.md), [R70 original language cohort](rounds/r70-rve/README.md), [R70 rerun](rounds/r70-rve-rerun/README.md), [R70 extension](rounds/r70-rve-ext/README.md), [R70 compile-time record](rounds/r70-compile/README.md), and [R70 task-eight smoke](rounds/r70-task8/README.md). Spec map: [acceptance tests and stack adapters](EVIDENCE-MAP.md#24-acceptance-tests-and-stack-adapters) and [sources and precedence](EVIDENCE-MAP.md#sources-and-precedence).

## F09 Campfire and web stacks

**Hypothesis:** H100–H105 ask whether equivalent web-stack implementations can be compared on correctness and performance, and whether agent task ports can be compared fairly. The Campfire lanes were withdrawn before formal execution.

**What ran:** The Campfire lane pages preserve design and withdrawal records; the Elixir task-port record concerns agent task work rather than a server-runtime comparison.

**Result:** Numerator/denominator: no formal scored cell result is recorded for the withdrawn lanes. Unit: matched web-stack outcome. Date: not recorded. Status: WITHDRAWN for both Campfire lanes.

**What it does not show:** The records do not establish runtime superiority, feature parity, message-delivery correctness, or cross-stack agent equivalence.

**Evidence:** [F09 hypothesis page](hypotheses/f09-campfire-webstacks.md), [Campfire lane 1](rounds/campfire-lane1/README.md), [Campfire lane 2](rounds/campfire-lane2/README.md), [R55](rounds/r55/README.md). Spec map: [deferred scope and non-goals](EVIDENCE-MAP.md#61-out-of-core-v1).

## F10 Agent-facing output

**Hypothesis:** H106–H110 ask whether compact formats, transformed tool output, or structured diagnostics improve parsing, diagnosis, repair, or task completion. The formats remain proposals without a matched live repair result.

**What ran:** The family page records partial output-feedback observations and synthetic checks; the cited surface cohort is incomplete and does not measure a complete repair comparison.

**Result:** Numerator/denominator: not recorded for matched parse-and-repair outcomes. Unit: parse errors, diagnosis, repair, or Build completion. Date: not recorded as a complete comparison date. Status: partial/interim; no format winner established.

**What it does not show:** Partial fixtures and synthetic validation do not establish comprehension, lower token use, faster diagnosis, or improved task completion.

**Evidence:** [F10 hypothesis page](hypotheses/f10-agent-output.md), [surface feedback record](rounds/x-surface/README.md). Spec map: [CLI and interaction](EVIDENCE-MAP.md#11-process-model) and [verification feedback](EVIDENCE-MAP.md#37-verification-and-base-relative-checks).

## F11 Claimed cross-cutting results

**Hypothesis:** H111–H116 are historical claims spanning other experiments. They require reconciliation to their original cohorts and are not additional experiments.

**What ran:** The family page separates historical model-route summaries, R72 populations, R70 language cohorts and the Sol-medium replication, cache summaries, the T98 smoke, and the T100 lane. These cohorts are not pooled.

**Result:** Numerator/denominator: no single reconciled numerator or denominator applies across the claims. Unit: task passes, cost, wall time, language outcomes, and cache requests differ. Date: claim-specific; no common date recorded. Status: interim, confounded, descriptive, withdrawn, or not run by underlying round.

**What it does not show:** Repeated headline percentages do not create new experimental observations or establish a current-version advantage.

**Evidence:** [F11 hypothesis page](hypotheses/f11-claim-reconciliation.md), [R72](rounds/r72/README.md), [R70 original language cohort](rounds/r70-rve/README.md), [Sol-medium language replication](rounds/lang-sol-replication/README.md), [post-hoc equal-task claim](results/claim-ledger.jsonl), [T98 cache smoke](rounds/t98-cache-smoke/README.md), [R74](rounds/r74/README.md), [T100 cache lane](rounds/t100-cache-lane/README.md). Spec map: [sources and precedence](EVIDENCE-MAP.md#sources-and-precedence).

## F12 Explicit lever and recipe arms

**Hypothesis:** H117–H139 ask whether specific flags, stage recipes, or bundles affect completion, cost, or time. A flag or recipe name alone does not establish that a distinct arm ran.

**What ran:** The lever register distinguishes bundled historical records, R51 planning arms, the R54 context handoff, R56 and R57 comparisons, cascade rounds, hill-climb iterations, R72, and withdrawn R74. L0 reconstructs R57's scoped 311-row pooled population and R72's P1 and partial P3 counts; R72's rows do not match the canonical public outcome export, and one planned R57 slot remains unidentified. See [CL-WA-r57-source-reported-denominator-variants](results/claim-ledger.jsonl) (**INTERIM**) and [CL-WA-r72-lifecycle-and-outcome](results/claim-ledger.jsonl) (**INTERIM**). The cohorts remain separate.

**Result:** Numerator/denominator: not recorded for a complete, attributable lever-by-lever comparison. Unit: official Build pass, cost, and wall time. Date: no common comparison date recorded. Status: many levers are not established as distinct runs; the linked rounds remain interim, descriptive, or withdrawn as noted on their pages.

**What it does not show:** A bundled or source-reported result does not establish a transferable isolated-factor effect for a named flag or recipe.

**Evidence:** [F12 hypothesis and lever register](hypotheses/f12-lever-recipes.md), [R51](rounds/r51/README.md), [R54](rounds/r54/README.md), [R56](rounds/r56/README.md), [R57](rounds/r57/README.md), [L0 reconciliation](rounds/l0-reconcile/README.md), [R49](rounds/r49/README.md), [R49b](rounds/r49b/README.md), [hc-1](rounds/hc-1/README.md), [R72](rounds/r72/README.md), [R74](rounds/r74/README.md). Spec map: [Shaping rules](EVIDENCE-MAP.md#30-rules), [ladder recipe](EVIDENCE-MAP.md#31-the-recipe-ladder), and [prompt caching](EVIDENCE-MAP.md#49-provider-requests-and-prompt-caching).

## F13 Late-September product mechanisms

**Hypothesis:** H140–H147 concern cross-harness review, audits, reuse, reliability, parallel Builds, and status alerts. The family page records no controlled efficacy result for these product mechanisms.

**What ran:** Related records include recovery diagnostics, a planned-DAG topology pilot, and surface-feedback observations. They do not instantiate the proposed audits, second-host workflow, or alert-on/control comparisons.

**Result:** Numerator/denominator: not recorded for a controlled outcome cohort. Unit: reliability, throughput, defect detection, or operator detection time, depending on the proposition. Date: not recorded. Status: no empirical efficacy evidence; adjacent diagnostics remain separate.

**What it does not show:** A topology pilot does not establish second-host throughput, Build ownership, or verification safety; implementation or use alone is not a measured benefit.

**Evidence:** [F13 hypothesis page](hypotheses/f13-product-mechanisms.md), [recovery diagnostics](rounds/x-recovery/README.md), [parallel topology pilot](rounds/x-parallel/README.md), [surface feedback record](rounds/x-surface/README.md), [Jev route context](rounds/jev-route-ctx/README.md), [Jev triage context](rounds/jev-triage-ctx/README.md). Spec map: [landing and recovery](EVIDENCE-MAP.md#39-commit-and-landing), [process custody](EVIDENCE-MAP.md#51-process-custody-success-relevant-deadlines-hangs-arg_max), and [deferred scope](EVIDENCE-MAP.md#61-out-of-core-v1).

## F14 Context-store and task policy

**Hypothesis:** H148–H153 ask whether context stores, task fairness checks, or harness mining improve retrieval or downstream Builds. Offline retrieval observations do not show that a novel context store improves Build success.

**What ran:** The public pages cover offline store retrieval and freshness, an incomplete context-preparation cohort, a forced-compaction pilot, an interim frontier lane, and a mixed-version harness inventory.

**Result:** Numerator/denominator: not recorded for a matched live Build comparison. Unit: offline retrieval, freshness, and inventory measures are separate from official Build passes. Date: no common result date recorded. Status: interim or source-reported offline diagnostic; no context-store efficacy result.

**What it does not show:** Retrieval ties, freshness checks, or mixed-version inventory do not establish better live task completion or identify a causal harness feature.

**Evidence:** [F14 hypothesis page](hypotheses/f14-context-store-task-policy.md), [context store](rounds/ctx-store/README.md), [context cohort](rounds/x-context/README.md), [E06 context](rounds/e06-context/README.md), [frontier](rounds/frontier/README.md), [harness mining](rounds/x-mining/README.md). Spec map: [deferred scope and implementation freedom](EVIDENCE-MAP.md#61-out-of-core-v1).
