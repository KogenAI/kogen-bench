# L2 plan specificity × builder strength

STATUS: **INTERIM**: preregistered 7 October 2026, before any scored L2 cell.

## Question

Does a more specific plan help a weaker builder more? L0 reconciled R69’s SPEC/APPROACH/ACCEPT/NONE formats on the old setup and found no clear format effect (Newcombe intervals about ±10–16 percentage points). L2 tests the interaction not measured there, with plan specificity and builder strength varied on the current setup.

## Population and arms

The six L1-admitted task variants are fixed: `r70-2-elixir`, `r70-2-go`, `r70-7-rust`, `r70-4-elixir-fe2`, `r70-4-go-fe2`, and `r70-4-ts-bun-fe2` (POOL-L2 in `the L1 POOL-L2 admission record`). Rust and Elixir run on EU; Go and TypeScript/Bun run on US. Mac Studio is reserved and excluded.

Plan specificity has three preregistered levels:

- **criteria**: concise checklist of observable requirements and completion conditions; no implementation sequence.
- **approach**: high-level architecture and key decisions, with no ordered execution recipe.
- **steps**: ordered implementation and verification steps, with no extra requirements beyond the public prompt.

For each of the six variants, one plan at each level is generated once by `gpt-6-luna` at max via `codex exec`, shown only that variant’s public `prompt.md` and public skeleton. Plans are frozen verbatim and identified by SHA-256 before any builder cell. No hidden tests, grader output, reference solution, or sealed files are supplied. Plan-generation uncached input, cached input, and output tokens are recorded separately. Planning runs use separate ephemeral CLI sessions in a fixed deterministic shuffle (seed `20261007`) of the 18 variant × level pairs; no plan is regenerated or edited after its first successful output. The 18 calls used 138,159 uncached input, 694,784 cached input, and 54,278 output tokens (887,221 total); per-plan records are in `plans/MANIFEST.json` and `plans/usage.jsonl`.

Builder strength is `gpt-6-luna` at low or max, direct Codex harness. Each frozen plan is supplied verbatim after the original prompt under a `Plan (provided)` section. For each variant × plan level × builder there are two reps: **6 × 3 × 2 × 2 = 72 planned cells**. Conditions use the same runner, sandbox, host assignment, 3,600-second cap, and zero retries. Rep 1 cells form the fixed gate cohort; rep 2 cells form the fixed bulk cohort. Each cohort has a deterministic shuffled order (seeds `20261007` and `20261008`) interleaved by task and builder; no adaptive reassignment is allowed except the preregistered futility stop.

Rule B admission controls are required for every new public variant: no-op FAIL, reference PASS, and reference core with the source skeleton front end PASS (3 × 18 = 54 controls). These are not factorial cells. Their inputs and official receipts are not staged in this prep; use the documented control scripts before any scored gate cell. The public base parity review and untouched-base build/check gates are also pending. No cell may launch until these fairness and base gates pass.

## Baselines and pairing

The no-plan comparison reuses all existing official Luna-max reps for each exact variant; their cell IDs are recorded in `BASELINES.json` and on the round page (32 valid official cells; one invalidated row is identified and excluded). Add one Luna-low no-plan rep per variant only where no official Luna-low no-plan rep exists. These runs use the original prompt without a plan section. The ledger scan found no official Luna-low no-plan cells for any of the six variants; one rep-1 cell per task is recorded with status `NOT-RUN` in `BASELINES.json`.

Primary comparison: for Luna-low, pair `steps` with `criteria` by variant and rep (12 pairs). Record wins, losses, ties, and the net paired pass difference (wins minus losses). Adoption for cheap builders requires a net gain of at least +3 of 12 pairs **and** lower total tokens per pass than criteria; otherwise findings are descriptive. Luna-max results and comparisons with no-plan baselines are descriptive interaction and calibration evidence.

## Endpoint, tokens, and analysis

The task endpoint is the official aggregate pass/fail for the full task. No hidden-suite names, test cases, diffs, reference content, or grader output enter public records. Report only aggregate counts and cell IDs.

Token definition for every planner and builder invocation: uncached input + cached input + output; total = their sum. Record all three components. Each builder cell’s full total includes the supplied plan in its prompt. Charge plan generation once per frozen variant × level and add those planner tokens to the corresponding plan-level total before computing tokens per pass; do not multiply planner generation cost by the number of builders or reps. Use total builder + planner tokens divided by official passes. For the primary `steps` vs `criteria` cost comparison, report both totals and passes across Luna-low cells, with plan-generation cost included. Do not combine tokens with wall time.

Report every officially graded cell. Missing, invalidated, interrupted, or ungraded cells remain explicitly labeled; no imputation. Only `VALID`, `CONFOUNDED`, `INVALID`, `INTERIM`, `WITHDRAWN`, and `NOT-RUN` labels are used. A condition comparison is `CONFOUNDED` if model, effort, prompt other than the plan section, skeleton commit, runner, sandbox, cap, retries, host assignment, or official grade provenance differs. Any protocol deviation is disclosed before interpretation.

## Sequence and stopping

Before any bulk release, satisfy every item in `the round release checklist` and Rule B. The first scored gate cohort is rep 1 for every variant × plan level × builder combination (36 cells), plus the six new no-plan Luna-low cells. This exercises each distinct deployed plan prompt through the actual sandbox; all must receive official grades through the authorized MacBook pipeline before rep-2 bulk release. Existing official Luna-max no-plan cells provide the no-plan max arm. L2 does not authorize worker-side grading, and this prep job authorizes no cell launch or grade; the gate and bulk plans remain unreleased.

After the first rep of all Luna-low cells across the six variants is officially graded, stop Luna-low rep 2 if steps and criteria differ by at most one pass in aggregate and none of the six variants changes pass/fail between the two levels. Record remaining cells `NOT-RUN` and the result `INTERIM`. This is a futility rule, not a success finding. Do not replace stopped cells.

## Provenance

Variant IDs will be `r70-<task>-<stack>[-fe2]-l2<level>`, where level is `criteria`, `approach`, or `steps`. Each keeps the source variant’s public skeleton and `base_sha`; only `prompt.md` changes. Public trees receive new committed base SHAs before deployment. Sealed bundles are copied in the explicitly authorized AUTHOR ROLE, verified by hashes only, and their contents are never read or printed. Exact SHAs, planner/builder CLI and harness versions, task and cell IDs, commands, plan hashes, and data file names belong in the round page reproduce block.

## Known limitations

There are six heterogeneous task variants and two reps per factorial condition. The study estimates an interaction over this admitted pool; it is not a general model ranking. Historic no-plan Luna-max cells are unrandomized and serve as descriptive baselines. The L0 null result is context, not evidence that these plan levels are equivalent.

## Amendment 1 (7 Oct 2026, before rep 2): frozen-plan pilot

L2 is a pilot on 18 frozen plans: one plan for each task × level. Plan specificity is bundled with the content of that single plan, so this design does not isolate a general effect of plan specificity from plan quality or establish a general plan-detail interaction.

The primary comparison remains the preregistered Luna-low steps-versus-criteria screen across 12 task × rep pairs. The +3 net-pass threshold is an operational screen, not confirmatory evidence: its most favorable minimal case is three discordant wins, zero losses, and nine ties, which gives one-sided sign-test p = 0.125 among the three non-tied pairs. The low-versus-max comparison is descriptive only; no interaction estimator is specified.

The 7 October proposal named a Sol planner and dollars per pass. The final frozen design uses a Luna-max planner so plan generation is fixed within the Luna builder family while builder effort varies; it reports tokens per pass because the retained records contain token usage but no pinned price schedule for a supported dollar-per-pass estimate. Tokens are resource counts, not a money ranking.

Report planning economics both ways. For the amortized view, charge each recorded plan-generation token total once and allocate it over that frozen plan's four planned uses (two builders × two reps). For the one-off view, charge the full plan-generation total to the corresponding task-level result rather than spreading it across reps, builders, or tasks. Keep uncached input, cached input, and output separate and show their sum; calculate tokens per pass only when official outcomes exist.

Follow-up confirmation requires independently generated plans on new tasks and contemporaneous no-plan arms. This amendment changes no planned cells, futility rule, admission/parity gates, or release gates. No cell is launched or graded by this amendment.
