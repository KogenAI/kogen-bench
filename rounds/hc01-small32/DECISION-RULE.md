# HC01 frozen decision rule

Registered 2026-10-08, before any HC01 cell. **Planning only; NOT RUN.** This rule governs [DESIGN.md](DESIGN.md). SMALL32 is the default; FULL120 must be selected and fully funded in a dated manifest before the first model/scored smoke cell. There is one confirmatory ON-versus-OFF comparison, no new Codex cells, no efficacy interim look, no result-dependent sample expansion and no post-data threshold changes.

## Population and ITT

SMALL32: four frozen below-ceiling tasks, four repetitions per arm, 16 pairs / **32 assigned cells**. All four tasks run on EU, with both arms of each task/repetition pair sharing that host; this supports the within-HC01 comparison for the registered EU condition. There is **NO R74/R58 venue parity**: erase-account, board and syn-31 ran on US in R74/R58. Erase-account remains in SMALL32 because the archived Sol/high results (3/3 in R58 and 4/5 in another check), Sol/medium (2/5) and Luna/max (0/3) indicate real Luna headroom rather than a task defect; it is expected to dominate failures in both arms under ITT. FULL120: all twelve frozen R74 tasks, five repetitions per arm, 60 pairs / **120 assigned cells**. The target is the finite selected task panel at this binary, recipe and execution window; it is not the task catalogue or a causal estimate of baseline-difficulty moderation.

At first release, the entire selected plan enters ITT. Keep every assigned cell under its assigned boolean, even if the setting was not exposed, Build was never reached, the packet was empty, a run timed out, the provider/runner/setup failed or the wrong model ran. There are **no primary exclusions, model retries or replacements**. Proven environment faults remain failures in primary ITT and receive an evidence label. A later diagnostic rerun is outside the cohort and cannot replace a primary grade. A proven grading transport failure may be repaired by regrading the same immutable candidate, with both receipts retained.

For cell `(t,s,a)`, define `Y=1` only for a valid official full-suite pass on the registered suite with correct task/base/prompt, arm and model receipts; otherwise `Y=0`. An unstarted/missing cell is 0 in the conservative ledger but remains `NOT_RUN`/`MISSING` in lifecycle counts. Do not turn missing test or token counters into measured zeros. Non-delivery has a documented failure outcome. All assignments must be terminal and reconciled before a final KEEP; unresolved grades or incomplete execution produce INCOMPLETE regardless of an interim numeric result.

## Primary estimand and exact test

For each task, let `D_t = mean_s(Y_ON − Y_OFF)`. The primary effect is `D = mean_t(D_t)`, with equal task weights. A rescue is `Y_OFF=0, Y_ON=1`; a loss is `Y_OFF=1, Y_ON=0`. Let their counts be `R` and `L`. Equal planned repetitions imply `D = (R−L)/N_pairs`, including failed assignments.

Test the directional null of no ON advantage with the **one-sided exact paired McNemar test**:

`p_plus = Pr[Binomial(R+L, 0.5) >= R]`

Set `p_plus=1` if there are no discordant pairs. Use the inclusive binomial tail, no mid-p, continuity correction or asymptotic replacement. This paired test replaces PACKET.md's unpaired task-stratified CMH proposal because this design deliberately matches cells by task/repetition. It assumes independent pairs and exchangeable discordance direction under the null within tasks; pairing does not claim identical provider randomness. Compute the reverse-direction `p_minus` with L in the tail only for the predeclared harm category. One superiority comparison needs no Holm correction.

Report a descriptive paired task-stratified bootstrap interval for D: resample N_t complete ON/OFF pairs with replacement **within each task**, preserve equal task weights, 10,000 draws, Python `random.Random(74)`. Sort the draws; report nearest-rank 2.5th/97.5th percentiles (1-based ranks 250 and 9,750), and the one-sided lower 5th percentile (rank 500). Do not resample arms separately or use this coarse small-sample interval instead of the exact decision test. It is conditional on the selected panel, not uncertainty over unseen tasks.

## Thresholds fixed before data

| Requirement | SMALL32 | FULL120 |
| --- | --- | --- |
| Practical minimum D | **+0.20** (20 percentage points) | **+0.10** (10 percentage points) |
| Superiority test | `p_plus < 0.05` | `p_plus < 0.05` |
| Per-task full-pass regression guard | ON passes at least OFF passes − 1, on **every** task | Same |
| Hidden-test regression guard | On every task, ON mean official `tests_passed` at least OFF mean − 1 | Same |

Use exact fractions for D and guards; do not round to cross a threshold. The smallest possible superiority pattern in SMALL32 is 5 rescues / 0 losses: D=31.25%, p=.03125. Four rescues / 0 losses fails at p=.0625. In FULL120, the practical margin requires at least six net rescues; 6/0 yields D=10%, p=.015625. These are observed decision boundaries, not the 80%-power effects.

For the hidden-test guard, use the same frozen suite and official test-count definition within each task. Documented non-delivery or no-test terminal execution failure contributes **effective tests_passed=0**, explicitly marked as an ITT convention rather than an observed count. Missing counts on a delivered candidate require reconciliation; they cannot clear the guard. Changed/shortened suite totals, required skipped tests, selective patch filtering, wrong public inputs, packet contamination or unverifiable arm propagation cannot earn KEEP, even if a reported pass total looks favorable.

Apply these categories in this order:

1. **INVALID** if the packet/public-input contract, fixed-arm comparison, frozen suite or scientific registration was compromised. Still publish conservative ITT and faults; do not claim confirmation.
2. **INCOMPLETE** if any assigned run is unstarted/unfinished, any delivered candidate lacks its official grade, or outcome/decision receipts cannot be reconciled. Report the fixed full denominator; no partial-cohort KEEP.
3. **DROP — REGRESSION** if either per-task guard fails, or if D<0 and `p_minus < .05`.
4. **KEEP — SELECTED PANEL** only if D meets the applicable practical minimum, `p_plus < .05`, both regression guards clear, and validity/completeness checks clear.
5. **NOT CONFIRMED** otherwise. Retain the feature as opt-in pending further evidence; a nonsignificant result is not proof of no benefit. SMALL32 is intentionally weak for modest improvements.

KEEP supports retaining this packet implementation for the measured use case; it does not authorize turning the setting on by default or claim all-task superiority. FULL120 KEEP concerns the full registered panel, whereas SMALL32 KEEP concerns only the four selected tasks. Do not use success in a post-hoc subgroup, exposure-only analysis or comparison with archived Codex to upgrade the primary verdict.

## Secondary measurements and controls

Report per-task rates and net differences, all R/L pairs, official `tests_passed/tests_total`, Build reachability and packet exposure, model/effort violations, host/order/load, wall time and complete tokens. Use `total = uncached_input + cached_input + output` for all stages/calls; reasoning is already part of output. Report mean/total token and wall ratios ON/OFF and token/pass and wall/pass, including failures. Cost and time are secondary and do not override the registered efficacy rule. There is no dollar or alternate composite metric.

Use the frozen one-shot `grade_cell.sh` route (the `poll.py` Studio wrapper; `night_grade.py` SHA-256 `4f35bbe96e506e0f651472d13c345562ade659c10faa96c25c8fb2c20f9b40e0`) with the official unique ID and no validation envelope. Studio grading windows never overlap webstack measurement; queue grades while measurement is active, delay both grades in a pair, and never reroute them. The lane provides the 3,500-second internal deadline and 30-minute setup timeout; the runner provides the 4,800-second outer cap. Apply all limits identically to both arms.

Missing token receipts remain unknown, with counts by arm and lower-bound totals. Do not bill failed calls as zero. Confirmatory execution must satisfy the shared release/record gates before bulk release; undeclared accounting gaps block it. Existing Codex baseline/grade receipts may be reused only as labeled historical context, with round, model, effort, base, cap, date, venue and runner fingerprints. Incomplete provenance means unavailable context, never permission to rerun a baseline. Archived R74 Codex token normalization is unverified; do not manufacture normalized historical costs.

## Stopping, fallback and disclosure

The first assigned EU syn06 OFF/ON pair supplies the two Kogen arm smokes, stays in ITT and must be officially graded before bulk release. Operator inspection is limited to operational validity, role pins, public-data provenance and artifact/grade handoff. Task pass/fail does not determine continuation, task replacement or extra repetitions. No pass-based futility stop, saturation stop or interim superiority claim is allowed.

Pause admission for disk/load/login/egress or other operational gate failures. Keep assignments and order. If the identical protocol cannot resume, close as INCOMPLETE or INVALID as applicable; do not rescue the result with a replacement cohort. After the first model call, material binary/config/packet/grade changes require ending this registration and a new independent study.

FULL120 is a budget alternative chosen before data, not an adaptive second look. A later full-panel study following SMALL32 must have a new dated registration and fresh Kogen cells; report SMALL32 separately. Neither repeats Codex. Publish all assigned rows and this frozen rule even for DROP, NOT CONFIRMED, INVALID or INCOMPLETE.
