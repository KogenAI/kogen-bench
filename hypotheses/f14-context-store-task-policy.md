# F14 — Context store and task policy

**Status: INTERIM.** Current context-store observations are offline diagnostics or incomplete run summaries. They do not establish that a new physical store or bounded context packet improves live Build outcomes. The Luna-medium targeted screen, TrackLine fairness review, and complete harness-mining map are not established as completed public result cohorts.

## Hypotheses

- **H148 — New context data structure.** A new structure for code and domain knowledge may provide more bounded, explainable context than a conventional graph, retrieval-augmented generation, or vector store. Compare retrieval and downstream task outcomes using the same queries and packet budget.
- **H149 — Change-centered persistence.** Persisting changes, queries, or transformations as primary objects may handle code and requirement evolution better than storing atomic facts and edges. Compare update effort, stale-answer rate, and retrieval quality after controlled edits.
- **H150 — Bounded uncertain context.** A context store may produce bounded task packets while exposing uncertainty, stale observations, and exceptions after edits. Compare packet size, calibration, and task outcomes under controlled repository changes.
- **H151 — Targeted Luna-medium screen.** Luna medium on simpler tasks where Codex failed may reveal a lower-cost harness improvement sooner than difficult Sol tasks. Compare on frozen prior-failure tasks, with a same-task direct baseline and complete cost/effort receipts.
- **H152 — TrackLine task fairness.** TrackLine must be repaired and audited as a fair task before its results inform harness decisions. Establish task correctness, valid alternatives, reproducible setup, and grader sensitivity before scored use.
- **H153 — Harness and prompt mining.** Mining harness implementations and prompts may reveal mechanisms behind performance differences. Convert candidate mechanisms into a complete feature map and test them with isolated ablations rather than treating the inventory itself as causal evidence.

## Experiment register

The experiment rows are separate populations. Offline store retrieval, data freshness, context-compaction pilots, selected prior-failure screens, task validation, and harness inventories have different outcomes and are not pooled. Missing reproduction fields remain unrecovered in the public record.

| experiment_id | Arm; task set; model/effort | Revision; host/epoch | planned / started / finished / graded / ITT n | Outcome and status | Correction or supersession | Claim ID and public receipt |
|---|---|---|---|---|---|---|
| `ctx-store-ranked-paths` (H148–H150) | Five stores across eight retrieval queries; no model-backed Build arm or model/effort. Exact query IDs are not recovered. | No Kogen coding harness revision applies; offline study, no public host or epoch record. | Store/query counts are source-reported; cell lifecycle and ITT are not applicable to this offline query study. | The stores are reported tied on ranked paths. **Source-reported, not reproducible from public data.** Offline retrieval is not Build success. | Keep this retrieval comparison separate from the freshness audit and from live Builds. | [`CL-WA-ctx-store-reported-ctx-store-ranked-paths`](../results/claim-ledger.jsonl) (**INTERIM**); [ctx-store page](../rounds/ctx-store/README.md); [reported data](../rounds/ctx-store/reported-data.json). |
| `ctx-store-recall` (H148–H150) | Failure-cause queries; exact IDs and store-level rows are not published; no model/effort. | Offline; no Kogen harness commit or host epoch. | Query denominator and underlying row records are not published. | Mean recall@10 is reported as 0.217. **Source-reported, not reproducible from public data.** | This is a retrieval metric and does not establish downstream task success. | [`CL-WA-ctx-store-reported-ctx-store-recall`](../results/claim-ledger.jsonl) (**INTERIM**); [reported data](../rounds/ctx-store/reported-data.json). |
| `ctx-store-freshness` (H149–H150) | Separate freshness audit; no Build arm or model/effort. | Offline; no Kogen coding harness revision or host epoch reported. | 4,266 records and 25 checks are reported; no run-cell lifecycle or ITT. | 25/25 freshness checks are reported as passing. **Source-reported, not reproducible from public data.** This is not a Build-success measure. | Do not combine with ranked-path or recall metrics. | [`CL-WA-ctx-store-reported-ctx-store-freshness`](../results/claim-ledger.jsonl) (**INTERIM**); [reported data](../rounds/ctx-store/reported-data.json). |
| x-context and admission guard (adjacent to H148–H150) | Context preparation/admission on a development cohort; exact arm/task mapping, model, and effort are not recovered. | Kogen/harness revision and host/epoch not recovered. | Planned, started, finished, graded, and ITT counts are not recovered. | Summary describes the comparison as inconclusive and lists an admission guard as a transfer candidate; no treatment effect is published. **Source-reported, not reproducible from public data.** | An admission candidate is not a validated context-store result. | [`CL-WA-x-context-reported-x-context`](../results/claim-ledger.jsonl) (**INTERIM**); [x-context page](../rounds/x-context/README.md); [reported data](../rounds/x-context/reported-data.json). |
| e06 forced-compaction pilot (adjacent to H150) | One pilot cell with forced context compaction; exact task, model, and effort are not recovered. No adjacent control. | Exact Kogen/harness revision and host/epoch not recovered. | One pilot cell reported run; no matched control, common grade cohort, or ITT contrast. | Six effective compactions are reported in the single pilot. **Source-reported, not reproducible from public data.** No causal compaction effect can be estimated. | Keep separate from store retrieval and any later context comparison. | [e06-context page](../rounds/e06-context/README.md); [reported data](../rounds/e06-context/reported-data.json). |
| R74 frontier lane (adjacent to H151) | Kogen Luna and Sol-high arms on tasks selected from prior Codex failures; exact task IDs and effective per-stage effort are not recovered. This is not the proposed Luna-medium simpler-task screen. | Kogen [`cde7a380455e9793cb1fc8315791bc9beffb863b`](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b); exact harness commit unavailable; final host/epoch join unavailable. | 70 cells were prepared/released in conflicting source summaries; a later trim reportedly avoided 60 unstarted cells. Started, finished, graded, and ITT totals remain unresolved. Figures are **source-reported, not reproducible from public data**. | Final active-storage result not verified; **INTERIM, no efficacy claim**. | Do not use an earlier 0/70 checkpoint as final closure. The frontier screen is not evidence for Luna medium. | [`CL-WA-frontier-lifecycle-and-outcome`](../results/claim-ledger.jsonl); [frontier page](../rounds/frontier/README.md). |
| TrackLine task fairness review (H152) | No public task-correction or fairness-audit cohort identified. Task IDs, model/effort, and grader checks are not recovered for a completed audit. | No corrected task revision, harness pin, or host/epoch receipt identified. | Not established as a scored or completed fairness audit. | No fairness result is available to support a TrackLine-based harness conclusion. **NO EMPIRICAL EVIDENCE.** | A TrackLine task name appearing in a run is not evidence that the task or grader passed a fairness audit. | No claim ID assigned; [research census](../research/README.md) lists the study status. |
| x-mining harness inventory (H153) | Mixed contestant observations across harnesses and versions; no single model/effort arm or task cohort. | Mixed revisions and versions; no single host/epoch. | Inventory reports 2,608 observations: 2,152 PASS, 295 FAIL, 54 INFRA, and 107 PENDING. A separate usage audit reports 124/2,649 missing usage; the denominators are distinct. These quantities are **source-reported, not reproducible from public data**. | Inventory only; no complete feature-to-ablation map or causal explanation. X09 is a separate diagnostic. | Do not turn mixed-version observations or mining into a harness performance ranking. | [x-mining page](../rounds/x-mining/README.md); [reported data](../rounds/x-mining/reported-data.json). |

## Design implications

- Keep query-level retrieval quality, freshness after edits, uncertainty calibration, packet size, and live Build success as separate outcomes.
- Treat store and context packet choices as open implementation decisions until a matched Build comparison is available.
- Correct and audit tasks before using their grades to rank a harness; keep task validity separate from model performance.
- Treat mining as hypothesis generation. Publish a feature-to-implementation map and then run isolated, preregistered ablations.

## Explicit non-implications

- A tie on ranked paths does not establish equivalence among stores or failure to improve Build completion.
- A freshness audit does not establish stale-context resistance in a live agent workflow.
- A context-compaction pilot without a matched control does not show that compaction helps or harms.
- The frontier lane is not a Luna-medium test, and its incomplete final status does not imply zero efficacy.
- A mixed-version harness inventory does not identify the cause of performance differences.
- A benchmark task does not become fair merely because it is public or has appeared in a run.

## Smallest open tests

- Publish the query-by-store matrix and exact query IDs, then test uncertainty and stale-answer handling after controlled file/requirement edits.
- Compare bounded packets against a conventional retrieval baseline on matched live Builds, with exact task, prompt, model/effort, Kogen/harness revision, cost, and ITT receipts.
- Audit and repair TrackLine with blind valid alternatives and wrong-solution controls before launching scored comparison cells.
- Build a public feature-to-ablation map from the mining inventory, select one mechanism at a time, and test it on a held-out task panel.

