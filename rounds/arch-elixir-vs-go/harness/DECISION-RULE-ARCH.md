# DECISION-RULE-ARCH: Elixir core + Go CLI (E) vs Go only (G)

Status: draft until the recorded prelaunch gates pass and the freeze manifest is sealed. Record this file's sha256 in RULE-SHA256.txt and hash the design and manifest at the same freeze. No scored run may start before then.

## Question
Under the specified 90-minute build plus 30-minute maintenance budgets, does E deliver materially more build-stage fault robustness at an acceptable combined token cost? E's extra language and CLI/core boundary work is intentionally inside these budgets.

## Fixed factors
- The visible base spec, protocol, Quint, Gherkin and briefs are identical except for the architecture-constraint block in DESIGN-ARCH.md §1. The maintenance prompt and extension in §4 are frozen separately and withheld until build FINAL.
- gpt-6.1-sol, effort high, in both phases; one agent per run, no reviewers or subagents. REAL-WORKFLOW, Kogen denylist and the access audit apply throughout.
- Freeze toolchains, kit/cache manifests, resource settings, harness/scorer/collector versions, prompts and receipts as specified in the design.
- Each Mac runs E1, E2, G1 and G2, giving four runs per architecture. Preassign E1/G1 and E2/G2 within each host. Do not rematch or add replacement runs after seeing outcomes.
- Freeze actual N_B, N_F and N_M, coverage, test IDs, assertions and deadlines before scored launch. N_F is approximately 12, at least 3, with all required fault scenarios covered. Record the passability evidence (implementation-free analysis per RULES 32, or both Elixir/OTP and Go witnesses 3/3 if the operator orders them) and all prefreeze drops. Follow the clean-repetition and information-isolation rules in DESIGN-ARCH.md §3.

## Measures
- F is the number of hidden fault tests passed at immutable build FINAL, out of N_F. Each test must pass both clean scoring repetitions.
- T is complete total token usage across build and maintenance through their stop points, using the frozen counting method in DESIGN-ARCH.md §5. Missing telemetry is not zero.
- Report build B/F; maintenance B/F/M and regressions; phase and combined T; LOC; wall time; CPU; build/test durations; and repair turns as defined in the design. Only build F and combined T decide.

## Outcome failures versus invalidity
- A build that does not compile, launch or implement the contract is an outcome, not a harness failure. In a functioning scorer, applicable tests that cannot complete because of the artifact fail. A missing/inoperable artifact scores zero on its applicable tests. Preserve any independently demonstrated test passes for a partially functional artifact.
- Source-audited architecture noncompliance scores F=B=0 at build FINAL, or B=F=M=0 at maintenance FINAL. It does not exclude the run. A maintenance failure does not overwrite the frozen build F. Include actual complete token usage for failures and early stops.
- Invalidate a run for wrong/missing model or effort receipts in either phase; Kogen denylist access; a real provider call made by an agent command; protected outside or cross-arm reads; access to hidden tests, witness or copies; or modification of the frozen supplied spec bundle. Adding implementation files for the supplied maintenance extension is allowed; editing its supplied requirements is not.
- Invalidate for infrastructure failure that prevents a required phase from being delivered, unrecoverable loss of build FINAL/primary scoring evidence, or incomplete/untrustworthy total token records. Agent-authored application crashes, test timeouts and installation mistakes are not infrastructure invalidity. Classify from harness/audit evidence, recording the reason independently of the score.
- Infrastructure-only scoring retries may use the identical immutable artifact and clean fixtures, following a predeclared retry policy; they must not resume the agent, change tests or discard an artifact-caused failure. Missing nondeciding measurements are reported as unavailable with reasons; they do not alone invalidate a run whose phases, F and T are intact.

## Comparison set
Report all eight runs and every invalidity. Retain a preassigned pair for the decision only if both runs are valid and have complete F and T. A valid run whose partner is invalid is excluded from deciding medians, but remains in the report. This gives E and G identical host representation.

If fewer than three complete pairs remain, return INCONCLUSIVE before evaluating the win rule. The recorded direction stands and a new preregistered rerun is proposed. Do not impute missing values or choose a favourable subset.

## Decision
For the three or four retained pairs, let mF(X) and mT(X) be medians of the corresponding architecture's F and T. With four values use the mean of the middle two; with three use the middle value. Preserve half values and compare without rounding.

E wins if and only if both hold:
1. mF(E) − mF(G) ≥ 3.
2. mT(E) ≤ 1.5 × mT(G).

Otherwise G wins. Equality at either threshold qualifies; a fault-score tie defaults to G. Compare token totals by multiplication, including when mT(G)=0, without dividing by zero. The tests' two repetitions establish repeatability, not additional independent runs.

The 3-test threshold represents 3/N_F of this frozen suite (25 percentage points when N_F=12). If mF(G)>N_F−3, E cannot meet it. It and the 1.5 cost multiplier are policy thresholds, not statistical significance or estimates of general language effects. G defaults by a prior that one language is simpler; a default when both implementations perform poorly does not establish usability or superior robustness.

## Reporting
Report all per-run measurements, pair IDs and inclusion status; numeric evaluation of both decision conditions; actual counts and per-fault-family distribution; per-host results; maintenance regressions; missing data and invalidities; passability evidence and drop reasons; and DESIGN-ARCH.md §8 disclosures. Distinguish an observed E robustness advantage, a G win by the default policy, and an inconclusive comparison. Do not extend claims beyond this model, budget, specification, suite and four-runs-per-architecture pilot.
