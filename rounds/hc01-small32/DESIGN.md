# HC01: Rust Kogen deterministic context packet on R74 tasks

Registered 2026-10-08. **Planning only; NOT RUN.** No deployment, model call, baseline rerun, grading, or external write is authorized by these documents. All files created for this planning task are under `public-source-location-withheld`.

The recommended, operative design is **SMALL32**: four tasks × four repetitions × two arms, all on EU. **FULL120** is a predeclared alternative: the complete twelve-task R74 panel × five repetitions × two arms. Select FULL120 only in a dated execution manifest **before the first scored/model smoke cell**; otherwise SMALL32 applies. There is no result-dependent expansion from 32 to 120 and no pooling of a completed small study with a later confirmation. [DECISION-RULE.md](DECISION-RULE.md) fixes the analysis and thresholds; RUNBOOK.md (not included in this public extract) is the operator handoff.

## Question, mechanism, and prior evidence

Does enabling `build.context_packet` improve Rust Kogen's official full-suite pass rate, relative to the same binary with that setting disabled, on R74 tasks with demonstrated Kogen headroom?

The directional hypothesis is that a public, deterministic context packet helps the builder find relevant interfaces and invariants, producing more full-suite rescues than losses. The effect should be largest on tasks with low Kogen baseline success; ceiling tasks have little room to improve. This is a hypothesis about this shipped retriever, not a claim that all packets work.

- L4 final record (source location withheld): 12 packet and 12 contemporaneous controls on four outcome-selected variants; +6 passes, six paired rescues, zero losses. Packets were hand-authored semantic summaries. US controls were not interleaved, and the control amendment followed six observed packet outcomes. Treat KEEP as encouraging descriptive evidence.
- L4b final record (source location withheld): Go/TS tasks selected with ceiling risk; packet 6/9, control 6/9, two rescues and two losses; NOT CONFIRMED. This does not establish a null effect on harder tasks.
- PACKET.md (source location withheld): the Rust implementation retrieves tracked public source lines by deterministic lexical overlap with the approved Intent, with stable path/line tie breaks and exact citations. It is capped at **2,000 UTF-8 bytes**, not 2,000 tokens. It excludes specified test, acceptance, grader, fixture, secret, instruction, untracked and other disallowed paths, and appends variable bytes after the static prompt/tool prefix when a builder session is created. The filter is not a general secret scanner. Different independently shaped Intents can produce different packets; determinism is conditional on identical Intent and workspace bytes.

The public R74 round (source location withheld) is WITHDRAWN and exports zero round-specific delivery/outcome rows. Its recovered internal rows are useful selection and budget anchors, **not a verified historical efficacy comparison**. The Rust runner's READY.md (source location withheld) records 0/18 scored Rust cells and valid no-model checks at `547d89dea22505eaa309506b3c2f4889171ab336`. There is no scored Rust baseline to rank. The older recipe validation runs stopped in Shape and are not scored baselines.

## Frozen task selection and exclusions

Selection uses only the recovered internal R74 K-luna **scored** rows, excluding smoke-control rows. There are five rows per task. Include tasks below 90% full-suite success over at least five such rows, rank by success ascending, and break ties by task ID. The following four exhaust that eligible set. These are archived Elixir Kogen counts used as a proxy for Rust task difficulty, not measured Rust success rates.

| Priority | Task ID | Archived K-luna anchor | Public base commit | SMALL32 host |
| --- | --- | ---: | --- | --- |
| 1 | `elx-port-erase-account` | 0/5 | `a9eb797cd44f7e3a68cb799b16cec7c65e14001f` | EU |
| 2 | `syn-31-inbound-email-webhook` | 3/5 | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` | EU |
| 3 | `elx-port-board-publish-unpublish-public-boundary` | 4/5 | `9082caa0a17b18c670475a08ef68d417edc0afc6` | EU |
| 4 | `syn-06-migration-ticket-numbers` | 4/5 | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` | EU |

All four SMALL32 tasks run on EU, and both arms of each task/repetition pair share that host. This makes the within-HC01 comparison valid for the registered EU condition. There is **NO R74/R58 venue parity**: erase-account, board and syn-31 ran on US in R74/R58; SMALL32 deliberately runs them on EU. This venue change does not change the fixed task panel or its ITT denominator.

SMALL32 excludes the other eight R74 tasks for archived ceiling success (each 5/5): `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `syn-01-live-ticket-filters`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, and `syn-24-csv-import`. Do not substitute the six-task runner-readiness panel: several of its tasks are at archived ceiling and it omits erase-account.

Keep erase-account in the panel. Its failure history is evidence of real Luna headroom, not a task defect: Codex Sol/high scored 3/3 in R58 and 4/5 in the other archived check, Sol/medium 2/5, and Luna/max 0/3. It is expected to dominate failures in both arms under ITT; those outcomes stay in their assigned arms and are not a basis for exclusion.

Before launch, also exclude from execution eligibility any task whose public base/prompt/setup cannot be reproduced, whose official grading route cannot be fixed, or whose required runtime cannot be exposed in the sandbox. If any of the four fails this check, SMALL32 is **blocked before release**: publish the reason and a new pre-data design rather than silently replacing it or reducing the denominator. A historical 0/5 or a known Shape failure is not itself grounds for exclusion. After release there are no outcome-based task exclusions, saturation stops, empty-packet exclusions, or replacement tasks.

## Prerequisites and launch order

Before any model call, run a no-model EU preflight for erase-account and board: verify the task-specific warm dependency inputs are present and usable, execute the Elixir setup against the frozen public bases, and check each task's declared ports from `recovery-2026-10-02/new-tasks/`. Verify the trackline base `f8b3035` and its setup/runtime are available on EU. Record commands, exit status, dependency/setup fingerprints and port checks in the preflight receipt. A failed preflight blocks release until repaired and re-reviewed before data.

After that no-model preflight, complete these gates in order before releasing HC01 scored cells:

1. Merge the KRS-GATEFAIL fix and verify at least one Rust Kogen cell passes the Build gate.
2. Repin the dedicated lane to a packet-capable build with the opt-in switch and sandbox fixes, including R6/R7 parity for the lane validators, arm aliases, setting propagation and exposure receipts.
3. Run Tier 1 first, then run the frozen SMALL32 plan. Tier 1 is estimated at about **6–18 EU hours**; SMALL32 at about **10.7–32 EU hours**. The Tier 1 ordering does not change SMALL32's assigned-cell denominator, analysis or decision thresholds.

FULL120 deliberately includes the eight ceiling tasks as regression controls and changes the estimand to the full R74 panel. Their bases are `adb5cbc11e33143bcc0153dc966f1f2ee8846d7d` for elx-02/04/07/12; `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` for syn-01/24; `3087c509b88c3e9b351b24fcb56de3668cdf0c0b` for syn-15; and `43b6cdcd44bf08d6cd2d2edebdb24c36356513c1` for syn-20. Use original R74 venue assignments: EU elx-04/12 and syn-06/15/24 (50 cells); US the other seven tasks (70 cells). Freeze all task metadata, public prompt hashes, setup hashes and suite identities before either design starts.

## Arms and execution pins

| Arm | Setting in generated `.kogen/project.yaml` | Treatment |
| --- | --- | --- |
| OFF | `build.context_packet: false` | No packet generation or insertion |
| ON | `build.context_packet: true` | Frozen deterministic generator and insertion policy |

Both arms use **one identical release binary and source commit**. This replaces PACKET.md's parent-versus-child proposal, which would confound packet exposure with other code differences. Default/unset must behave like false, but write the boolean explicitly in both scored arms. Do not supply hand-authored summaries or modify the public task prompt.

The inspected packet worktree snapshot `6d9ed2ce33cbb86c562aeda3ab701b43cf9c35fe` inserts packets unconditionally and its build schema does not yet accept `context_packet`. The deployed `547d89d` lane likewise is not a verified ON/OFF experiment adapter. **Neither snapshot is launch-ready for this protocol.** Before execution, freeze a packet-capable commit with the opt-in switch, the deployed sandbox compatibility fixes, and the documented packet algorithm. Validate false/unset equivalence, true insertion, size/provenance filtering and unchanged static prefix with no model calls. Record the full source SHA, clean tree, build/lock/toolchain fingerprints and binary SHA in the execution manifest; copy one build to both hosts if FULL120 is chosen. Changes to retrieval, content limits, stages or other behavior require a new pre-data registration, not a quiet repin.

Use the runner's frozen `ladder-luna` recipe: builder/rung2/rung3 `gpt-6-luna/max`; shaper, fallback_shaper, planner, auditor, reviewer and context `gpt-6.1-sol/high`; `KOGEN_BENCH_NO_FALLBACK=1`. As resolved in `RECIPE.json` and the recipe report, there is no distinct edge-test-writer role; leave optional `build.edge_tests` unset in both arms. Do not invent a role mapping. Verify actual request receipts, not just configured roles.

Copy the existing lane into a dedicated HC01 execution lane in a future execution task. Its present validators pin `547d89d` and a single harness name; they must be repinned together and support distinct OFF/ON aliases, explicit setting propagation and packet exposure receipts. One task and one arm per spec. Freeze a `PLAN.json` with unique official IDs, pair IDs and specs, and a matching launcher dry-run receipt. This planning task does not create or edit that execution lane.

## Repetitions, randomisation and interleaving

SMALL32 uses repetitions 1–4; FULL120 uses 1–5. Pair by `(task ID, repetition)`, with fresh independent runs in both arms. The benchmark seed remains 74; scheduling uses Python `random.Random(20261008)`. A repetition is an independent trial label, **not a promised provider RNG seed**. If an actual provider seed is supported, freeze its mapping before launch and use the same value in both members; otherwise record `provider_seed: unsupported`. No shared shaped Intent, plan, conversation, cache identity, or successful candidate between paired cells.

For SMALL32, start from task aliases `[syn06, erase, syn31, board]`; for each repetition shuffle that list, then draw `getrandbits(1)` per task (0 = OFF first, 1 = ON first). Move syn06's first pair to the front of repetition 1 without changing its already drawn arm order. The resulting EU queue is frozen here:

| Repetition | Ordered task pairs and within-pair order |
| --- | --- |
| 1 | syn06 OFF→ON; board OFF→ON; erase ON→OFF; syn31 OFF→ON |
| 2 | erase OFF→ON; board ON→OFF; syn31 ON→OFF; syn06 ON→OFF |
| 3 | syn31 ON→OFF; syn06 ON→OFF; board OFF→ON; erase OFF→ON |
| 4 | syn31 OFF→ON; syn06 OFF→ON; erase ON→OFF; board OFF→ON |

For FULL120, start from the lexicographically sorted twelve task IDs and apply the same shuffle/coin procedure over five repetitions. Preserve each task's host; filter each repetition into the two host queues. Move the syn06 repetition-1 pair to the front of EU and start that pair before any US cell. Freeze the resulting complete order in the execution manifest before launch.

Run both members consecutively on the same host before starting another pair; do not run all ON cells followed by all OFF cells. One model cell **host-wide** at a time on each 2-vCPU host, counting other rounds; no concurrent build, model job or local grading. Existing read-only dependency caches may be warm, but isolate per-cell worktrees, HOME, conversation IDs and writable caches. Record provider routing/cache metadata, order, wall time, load and pauses.

The Studio grading route shares time with webstack measurement: grading windows never overlap a webstack measurement. Grades queue while a measurement is active; delay pair grading and keep it on the frozen route, never reroute it.

SMALL32 is EU-only to avoid making the first experiment depend on US disk reclamation; preflight must verify all four task bases and runtimes on EU. FULL120 is EU-first, with US queued below **7,000,000,000 free bytes** (at least that floor plus measured space for one cell is required to admit a pair). Never switch a half-run pair's host. Do not migrate tasks after seeing outcomes; prolonged admission failure produces an incomplete round rather than selective scheduling.

## ITT and primary outcome

At first scored-cell release, assign the **entire** selected design: 32 or 120 cells. Every assignment remains in its arm and denominator. A full-suite pass requires an official grade on the frozen suite plus valid model/arm/prompt/base receipts. Model, provider, runner, setup, Shape, timeout, empty delivery, missing grade and wrong-model failures are not dropped. Cells that never reach Build or receive an empty packet stay in ON under ITT. Report assigned, started, finished, officially graded, not run, missing and failed counts separately. No model reruns or replacements in the primary cohort, including for environment faults; their evidence remains visible. Regrading the same immutable patch after a proven grading transport fault does not create a model cell.

Unstarted or unresolved assignments receive 0 in the conservative ITT table and retain their lifecycle labels. An interrupted or incompletely reconciled cohort cannot earn KEEP. Freeze the final data only when every assignment has an official grade or documented terminal non-delivery/failure; unresolved grading is INCOMPLETE. Report an exposure-only analysis and archived-baseline comparisons only as descriptive sensitivities.

The primary metric is the equal-task-weighted difference in official full-suite pass rates, **ON minus OFF**. With equal repetitions it equals `(rescues − losses) / number_of_pairs`. Partial test passes and self-reported Kogen success are not full-suite passes. See the exact test, practical margins and regression rules in DECISION-RULE.md.

## Minimum detectable effect and budget

Choose a narrowly decisive experiment rather than implying that a tiny sample resolves modest gains. SMALL32 is the smallest balanced four-task design, with an integer number of repetitions, that can reach 80% power under the following explicit planning model. It can decisively detect an L4-sized large effect, not a routine 10-point gain.

Planning assumptions: archived control probabilities for the four tasks are `(0, .6, .8, .8)`, independent fresh runs conditional on task; treatment lifts each to `p_ON = p_OFF + f(1 − p_OFF)`. Thus the selected-panel difference is `.45f`. The full panel adds eight probabilities of 1, giving `.15f`. For a pair, rescue probability is `(1 − p_OFF)p_ON`, loss probability is `p_OFF(1 − p_ON)`, and tie probability is the remainder. Convolve this three-outcome distribution over the fixed tasks/repetitions and sum probabilities satisfying the exact test and practical margin. These are **scenario estimates**, not estimates of the actual Rust effect. Regression/validity gates can reduce power further.

| Design | Pairs / cells | 80% power effect under that model | Typical serialized run time (20–60 min/cell) | Total tokens at archived mean, then +10% allowance |
| --- | ---: | --- | --- | --- |
| Four tasks × 3 reps × 2 | 12 / 24 | Unattainable: even ON=100% gives only 74.5% power | 8–24 host-hours | 33.1M → 36.4M |
| **SMALL32: four tasks × 4 reps × 2** | **16 / 32** | **39.7 percentage points** (OFF≈55%, ON≈94.7%) | **10.7–32 EU-hours** | **44.1M → 48.5M** |
| FULL120: twelve tasks × 5 reps × 2 | 60 / 120 | 12.3 points (OFF≈85%, ON≈97.3%) | 40–120 host-hours; two admitted hosts ≈23.3–70 elapsed hours | 115.1M → 126.6M |

For SMALL32, effects of 18, 27, 36 and 40.5 points have about 16%, 36%, 66% and 83% power. For FULL120, 6, 9, 12 and 13.5 points have about 19%, 45%, 77% and 91% power. FULL120's near-ceiling estimate agrees with the 12–13-point anchor in PACKET/R74 only under those assumptions. At a homogeneous 50% control baseline, 60 pairs instead need about **23.5 points** for 80% power under independent runs. Correlation, provider drift, task dependence and unstable five-row anchors can change all of these figures. Four selected tasks do not establish population-wide efficacy or a low-versus-high-baseline interaction.

With 16 pairs, the least significant one-sided discordance pattern is five rescues and zero losses (`p=.03125`), a +31.25-point observed difference; four rescues alone yield `p=.0625`. FULL120's +10-point practical threshold requires at least six net rescues; six rescues/zero losses give `p=.015625`. Losses can require substantially more rescues. Test granularity is not an 80%-power MDE.

Use one token vector throughout: **uncached input + cached input + output**; total is their sum. Reasoning is included in output and must not be added again; cache-write is separate. Count every stage, failed call and internal retry, not only builder tokens. The runner already exports this definition in `usage.json` and request receipts. Existing Codex normalization is disputed in R74's notes; preserve those raw counters and do not infer comparative costs from them.

Budget anchors recomputed from the pinned internal R74 scored K-luna rows:

| Population | Cells | Mean uncached / cached / output per cell | Mean total | P90 total | Maximum total |
| --- | ---: | --- | ---: | ---: | ---: |
| Four selected tasks | 20 | 811,715 / 523,149 / 43,434 | 1,378,298 | 1,835,070 | 4,109,362 |
| Full panel | 60 | 596,948 / 322,722 / 39,705 | 959,375 | 1,670,831 | 4,109,362 |

SMALL32 therefore projects about 26.0M uncached, 16.7M cached and 1.4M output tokens. FULL120 projects 71.6M, 38.7M and 4.8M respectively. Reserve roughly **65M total tokens for SMALL32** or **221M for FULL120** using P90 per-cell usage plus 10%; neither is a guaranteed upper bound. At the observed maximum on every cell, usage would be 131.5M or 493.1M before allowance. The packet's direct size is small, but repeated conversation input and changed behavior can amplify it; do not estimate the total experiment as packet size × cell count. No new authoring-model budget or Codex baseline budget is needed.

These are resource planning envelopes, not interim stopping boundaries. Reserve the complete cohort before release; do not stop on pass counts or measured cost/pass. If a real resource limit prevents completion, halt safely, preserve every assignment and report INCOMPLETE. The lane supplies the 3,500-second internal deadline and 30-minute setup timeout; the runner supplies the 4,800-second outer cap. Freeze all three limits unchanged in both arms, keep runner retries at zero, and report which limit fired. The outer-cap bound is 42.7 serialized host-hours for SMALL32 or 160 for FULL120, before grading/queue delays; old estimates based on four concurrent jobs per host do not apply.

## Controls, grading and reporting

Keep public prompt/base/setup, binary, recipe/stages, provider, model/effort, sandbox/egress, tool schema/order, retry/deadline policy, dependency state and grade route fixed. Verify generated YAML differs only in the boolean; retain normalized config fingerprints and actual packet hashes/byte counts/source-tree fingerprints. Packet source audits must use public inputs only. Log Build reachability, packet nonempty/exposed status and builder-session count so a Shape bottleneck cannot be mistaken for a tested builder mechanism. Do not optimize the generator after examining any HC01 results.

Freeze the grading route as **`grade_cell.sh` one-shot** (the `poll.py` Studio wrapper; `night_grade.py` SHA-256 `4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0`), using the official unique ID and **no validation envelope**. Freeze the task resolver, suite versions and grader fingerprints before launch. Historical suite/hash equality is unproved; the primary comparison needs equality between the two new arms. R70 Linux grades are not a substitute. No sealed suite, failure name, reference solution or grader content enters a model workspace or packet.

Every delivered candidate, including red/self-reported failed candidates, goes once through that route with its official unique opaque grading ID and no validation envelope. Validate `COMPLETE.json`, exact task/base/pair metadata and immutable patch hash. Remove only preregistered runner setup artifacts (`.kogen/project.yaml` and `.setup-compile.log`) using the same audited patch filter in both arms; preserve both original and filtered hashes. Grade empty/setup-only deliveries as failures, not successful fixes. Terminal runs with no candidate retain failure receipts. Compare hidden test totals with the frozen expected suite; an official full pass must run the complete suite with no missing/skipped required tests. Blind arm labels to graders where practical. If a Studio webstack measurement is active, queue the grades until it ends; delay both grades in the pair and never reroute either one.

Follow the release checklist (source location withheld). The first two assigned EU syn06 cells are the two **Kogen** arm smokes and remain in ITT; bulk release requires official grade/handoff and record validation, not task success. Reuse any needed existing Codex smoke receipt. **Never re-run an existing Codex baseline**, including as a new smoke, ceiling guard or top-up. If historical Codex records cannot be joined, mark that descriptive comparison unavailable; do not regenerate them. No Codex arm contributes to this primary comparison.

Publish the entire assigned-cell ledger, strict-validation result, aggregate and task pass rates, rescues/losses, tests passed/total, exposure counts, token vectors, all-stage token/pass and wall/pass, timing/host/order circumstances and every fault. Ratios with zero passes are infinite/undefined, not zero. Record missing token counters as unknown, never zero, and label totals lower bounds when appropriate. Missing outcome/decision fields block KEEP. No USD estimate is registered; any later dollar conversion needs dated price sources and a fixed method.

## Input snapshot and registration custody

Read-only inputs are the SOT L4/L4b/R74 records, `public-source-location-withheld`, and the recovery `levers/kogen-rs-runner/`, `levers/kogen-rs-r74recipe/`, and `levers/r74/` directories. The execution manifest must include the SHA-256 of all three HC01 documents and may fill mechanical pins, exact IDs and resource receipts without changing the scientific rule. The source snapshot anchors are:

| Input | SHA-256 |
| --- | --- |
| `public-source-location-withheld` | `4342ef155281cf647ebda6acbbd5e11245581eb57d0f2a0baea1647f27254ea1` |
| Recovery `levers/r74/run-records.jsonl` | `daa3d4d2beb1f1f4e4e2acd0b8a054e7a6a5c9e140b8e6001bb11c756e0fed29` |
| Recovery `levers/kogen-rs-runner/RECIPE.json` | `6b3982e49633024715eb83ffc5d7726fd6e1b53e52167308d07bb2c24b6cff18` |
| Recovery `levers/kogen-rs-runner/READY.md` | `844e647edda49baabec411eb638ac2feccccdbf1959ae37fd077269784f60b5d` |

Recompute archived selection/budget anchors by filtering the JSONL on `arm == "kogen-ladder-luna-r74"` and `itt.cohort == "scored"`; group by `task.id`, count `outcome == "pass"`, and sum `tokens.total.input`, `cached_input`, and `output`. Use nearest-rank P90. This produces 60 rows, with 20 on the four selected tasks. Preserve WITHDRAWN in any citation of R74.

## Amendment log

- **2026-10-08 — pre-launch operator review.** Fixed the grading route to one-shot `grade_cell.sh` with an official ID and no validation envelope; added Studio/webstack time-sharing; documented EU-only SMALL32 pairing and the absence of R74/R58 venue parity; added the EU no-model Elixir/dependency/ports preflight; ordered the KRS-GATEFAIL, packet-capable lane and Tier 1 prerequisites; clarified time-limit ownership, resource estimates, erase-account headroom evidence and its ITT treatment. No HC01 outcome data were known when this amendment was made.
