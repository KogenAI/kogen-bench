# Round status inventory

Statuses use the evidence in each round’s own README and files. The status column is the analysis classification and is retained for historical records. Every round README also carries a publication badge, recomputation status, and limits. `KEPT FOR AUDIT` identifies the page as a retained historical record; it does not change the analysis status. New rounds dated 2026-10-09 or later must meet the complete Standard capture gate with no protocol deviations.

Observation records what happened in these runs. Decision-grade evidence requires a pre-registered rule, adequate repeats, and complete capture that together support a decision. Production qualification is a separate, later check that the system is fit for real Kogen Builds. Nothing published here is production qualification.

DESCRIPTIVE, PILOT, INVALID, and INCOMPLETE mean observation only. VALID means the reported outcomes fit the round’s stated rule and scope; it does not by itself establish decision-grade evidence. A VALID round is decision-grade only when its own records meet all three requirements above; otherwise, its evidence remains observation only.

The LAB-01 analysis-tooling screen is published as DESCRIPTIVE (observations only, kept for audit; see its README); nothing beyond that screen is published for LAB-01.

## Rounds

| Round | Status | Reason |
| --- | --- | --- |
race1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, NO_PREREG, ENVIRONMENT — observations from one run per language on one MacBook; no pre-registered decision rule.
race2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, NO_PREREG, ENVIRONMENT — observations from individual runs on one MacBook; no pre-registered decision rule.
race3-sprint | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — wave 1 harness changed during the race; waves 2/3 used 30-minute caps; FINAL repeats and clean-copy regrade are absent.
race4 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Descriptive results only: interruptions and a restart changed the planned schedule, and some execution evidence is unavailable. The published scores describe the completed runs; they do not establish an overall language winner. The 88-case suite remains withheld because planned follow-up experiments (labelled L2 and L3 in our plans) that reuse these same test cases have not run yet; no release date is set.
race5 | DESCRIPTIVE | DESCRIPTIVE_ONLY, INVALID_CELL, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Observation-tier result: under the registered PRIMARY reading, Go had the highest observed result after the tie-zone timing comparison, with invalid-run scores retained. Alternative readings and timing methods differ; incomplete audits and historical searches limit these observations. This is not decision-grade evidence or production qualification.
race6 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Race 6 compares specification-and-tool bundles separately within Elixir and Go. Different frozen harness versions invalidate the round under the literal rule; the coordinator accepted a disclosed deviation for descriptive reporting. No overall winner is claimed.

sol-medium | DESCRIPTIVE | DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL

core4b-ksub-max | DESCRIPTIVE | DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL

rtg1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL

core4-pilots | DESCRIPTIVE | DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL

cache-key-api-v4 | VALID | NONE
cache-key-backend-v4 | VALID | NONE
cache-replay-mechanism | DESCRIPTIVE | CONDITIONS_MISMATCH, INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL
campfire-lane1 | INCOMPLETE | NOT_EXECUTED, RAW_EVIDENCE_MISSING
campfire-lane2 | INCOMPLETE | NOT_EXECUTED, RAW_EVIDENCE_MISSING
candidate-counterfactual | DESCRIPTIVE | POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING
claim-b-rerun-1 | INVALID | CONFOUNDED_ASSIGNMENT, OUTCOME_CROSSWALK_MISSING
claim-b-screen-1 | INVALID | OUTCOME_CLASSIFICATION_INVALID, OUTCOME_CROSSWALK_MISSING
confirm-combined-1 | INCOMPLETE | DENOMINATOR_UNVERIFIED, PARTIAL_CAPTURE
ctx-store | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
e06-context | PILOT | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING, UNMATCHED_CONDITIONS
e09-tidewave | PILOT | INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
frontier | INCOMPLETE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING
grok-frontier | INCOMPLETE | NOT_EXECUTED, RAW_EVIDENCE_MISSING
hard1-calibrate-1 | INVALID | OUTCOME_CLASSIFICATION_UNRESOLVED, OUTCOME_CROSSWALK_MISSING
harness-compare-1 | DESCRIPTIVE | OUTCOME_CROSSWALK_MISSING, RAW_EVIDENCE_MISSING, TASK_VALIDITY_UNRESOLVED
harness-pick-2026-09-29 | DESCRIPTIVE | OUTCOME_CROSSWALK_MISSING, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
hc-1 | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL
hc-2 | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL
hc-3 | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL
hc-4 | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL
hc01-small32 | INCOMPLETE | INCOMPLETE_EXECUTION, RAW_EVIDENCE_PARTIAL
intent-coverage-audit | DESCRIPTIVE | POST_HOC_AUDIT, RAW_EVIDENCE_MISSING
jev-route-ctx | DESCRIPTIVE | POST_HOC_DIAGNOSTIC, RAW_EVIDENCE_MISSING
jev-triage-ctx | INCOMPLETE | INCOMPLETE_EXECUTION, PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING
kh-climb | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
kh-compare-2026-09-29 | INVALID | COHORT_MISMATCH, OUTCOME_GRADES_MISSING
kogen-rs-ladder-luna-r74x | DESCRIPTIVE | PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING, DECISION_RULE_NOT_APPLIED
l0-reconcile | VALID | NONE (limits: EVIDENCE_INCOMPLETE, PRE_REGISTRATION_NOT_APPLICABLE)
l1-task-grader-trust | VALID | NONE
l2-plan-specificity | VALID | NONE
l3-repair | DESCRIPTIVE | REGISTERED_THRESHOLD_NOT_MET
l3b-repair-vs-continue | VALID | NONE (limits: RAW_EVIDENCE_PARTIAL, PRE_REGISTRATION_TIMING_OPERATOR_REPORTED; KEEP scoped to eight selected failures)
l4-context-packet | DESCRIPTIVE | CONDITIONS_MISMATCH, POST_HOC_AMENDMENT
l4b-confirm | VALID | NONE (limits: RELEASE_EVIDENCE_MISSING)
l5-sol-comparators | DESCRIPTIVE | CONDITIONS_MISMATCH, DESCRIPTIVE_ONLY_RULE, HISTORICAL_DATA_PRECEDES_REGISTRATION
l6-auditor-replay | VALID | NONE
lang-sol-replication | DESCRIPTIVE | DECISION_RULE_UNDEFINED, CONDITIONS_MISMATCH
llm-latency-long | DESCRIPTIVE | CONDITIONS_MISMATCH, INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING
llm-latency-short | DESCRIPTIVE | CONDITIONS_MISMATCH, PRE_REGISTRATION_MISSING
night-2026-10-01 | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
offline-aa-bo3 | DESCRIPTIVE | POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING
offline-contract-audit | DESCRIPTIVE | POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING
offline-review | DESCRIPTIVE | POST_HOC_AUDIT, RAW_EVIDENCE_MISSING
offline-review3 | INCOMPLETE | INCOMPLETE_EXECUTION, RAW_EVIDENCE_MISSING
overstrict-replay | DESCRIPTIVE | POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING
pilot73 | DESCRIPTIVE | NO_PUBLIC_CELLS, PRE_REGISTRATION_MISSING
r1 | INVALID | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_CROSSWALK, PRE_REGISTRATION
r10 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r11 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r12 | INVALID | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_CROSSWALK, PRE_REGISTRATION
r13 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r14 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r15 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r16 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r17 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r18 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r19 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r2 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r20 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r21 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r22 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r23 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r24 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r25 | DESCRIPTIVE | NONE
r26 | DESCRIPTIVE | NONE
r27 | DESCRIPTIVE | NONE
r28 | INVALID | NONE
r29 | DESCRIPTIVE | NONE
r3 | INVALID | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_CROSSWALK, PRE_REGISTRATION
r30 | DESCRIPTIVE | NONE
r31 | INVALID | NONE
r32 | DESCRIPTIVE | NONE
r32a | INCOMPLETE | NONE
r32b | DESCRIPTIVE | NONE
r33 | DESCRIPTIVE | NONE
r34 | DESCRIPTIVE | NONE
r34b | DESCRIPTIVE | NONE
r35 | DESCRIPTIVE | NONE
r36 | INVALID | NONE
r37 | INVALID | NONE
r37c | DESCRIPTIVE | NONE
r38 | DESCRIPTIVE | NONE
r39 | INVALID | NONE
r39b | DESCRIPTIVE | NONE
r4 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r40 | DESCRIPTIVE | NONE
r41 | INVALID | NONE
r42 | INVALID | NONE
r43 | DESCRIPTIVE | NONE
r44 | DESCRIPTIVE | NONE
r45 | INVALID | NONE
r46 | DESCRIPTIVE | NONE
r47 | DESCRIPTIVE | NONE
r48 | DESCRIPTIVE | NONE
r48b | DESCRIPTIVE | NONE
r49 | INVALID | NONE
r49b | DESCRIPTIVE | NONE
r5 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r50 | INCOMPLETE | DENOMINATOR, DESIGN, NO_PREREG
r51 | INCOMPLETE | DENOMINATOR, ENVIRONMENT, NO_PREREG
r52 | PILOT | ENVIRONMENT, NO_PREREG, PILOT
r53 | INVALID | NO_PREREG, OUTCOME_MISMATCH, UNMATCHED_EFFORT
r53b | INCOMPLETE | CROSSWALK, DESIGN, NO_PREREG
r54 | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r55 | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r56 | INVALID | FILTER, NO_PREREG, OUTCOME_MISMATCH
r56b | INCOMPLETE | CROSSWALK, DESIGN, NO_PREREG
r56c | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r56d | INCOMPLETE | CROSSWALK, DESIGN, NO_PREREG
r56p2 | INCOMPLETE | CROSSWALK, DESIGN, NO_PREREG
r57 | INVALID | ARM_MAPPING, EVIDENCE, NO_PREREG
r57-studio | PILOT | NO_OUTCOME, NO_PREREG, SMOKE_ONLY
r57-t90-studio | PILOT | NO_OUTCOME, NO_PREREG, SMOKE_ONLY
r57b | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r57c | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r57d | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r57e | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r58 | PILOT | NO_PREREG, OUTCOME_CLASSIFICATION, PILOT
r58b | INVALID | NOT_SCORED, NO_PREREG, UNMATCHED_ROW
r58x-studio | PILOT | DESIGN_CHANGE, EVIDENCE_PARTIAL, NO_PREREG
r59 | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r6 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r60 | INVALID | ARM_MAPPING, DESIGN, NO_PREREG
r60b | INVALID | ARM_MAPPING, DESIGN, NO_PREREG
r61 | INVALID | CROSSWALK, NO_PREREG, OUTCOME_CLASSIFICATION
r62 | INVALID | CROSSWALK, NO_PREREG, OUTCOME_CLASSIFICATION
r62b | INVALID | COMPARATOR, NO_PREREG, UNMATCHED_CONDITIONS
r63 | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r63b | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r64 | DESCRIPTIVE | ENVIRONMENT, NO_PREREG_EVIDENCE, RECIPE
r64b | INCOMPLETE | CROSSWALK, DESIGN, NO_PREREG
r64c | DESCRIPTIVE | CROSSWALK, NO_PREREG_EVIDENCE, RECIPE
r64d | DESCRIPTIVE | DESIGN, ENVIRONMENT, NO_PREREG
r64e | INCOMPLETE | DESIGN, ENVIRONMENT, NO_PREREG
r65 | INVALID | NOT_SCORED, NO_PREREG, RECIPE
r65b | INVALID | NOT_SCORED, NO_PREREG, UNMATCHED_CONDITIONS
r66 | DESCRIPTIVE | COHORT, DENOMINATOR, NO_PREREG
r67 | INVALID | CROSSWALK, NO_CANDIDATE, NO_PREREG
r67b | INVALID | CROSSWALK, INCOMPLETE_CAPTURE, NO_PREREG
r68 | INCOMPLETE | DESIGN, NO_PREREG, TASK_MISMATCH
r68b | DESCRIPTIVE | COMPARATOR, NO_PREREG, UNMATCHED_EFFORT
r69 | INVALID | ARM_MAPPING, CROSSWALK, NO_PREREG
r7 | INVALID | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_MISMATCH, PRE_REGISTRATION
r70 | INCOMPLETE | INCOMPLETE_EXECUTION, NO_PREREG
r70-compile | DESCRIPTIVE | DESCRIPTIVE_ONLY, EVIDENCE_SCOPE, NO_PREREG
r70-rve | INVALID | EVIDENCE, NO_PREREG_EVIDENCE, UNMATCHED_CONDITIONS
r70-rve-ext | VALID | NONE (limits: NO_PREREG_EVIDENCE, PARTIAL_PREREG, SCOPE)
r70-rve-rerun | DESCRIPTIVE | SENSITIVITY_ONLY, SEPARATE_COHORTS, UNMATCHED_CONDITIONS
r70-rve-task8v2 | INCOMPLETE | NO_OUTCOME, NO_SCORED_RESULTS, SMOKE_GATE
r70-rve2 | INVALID | TASK_MISMATCH, CONDITIONS_MISMATCH, RAW_EVIDENCE_PARTIAL
r70-rve3 | INVALID | OUTCOME_CLASSIFICATION_INVALID, RAW_EVIDENCE_PARTIAL
r70-spot1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL, SMALL_SAMPLE
r70-task8 | PILOT | NO_OUTCOME, NO_SCORED_RESULTS, SMOKE_ONLY
r71 | INCOMPLETE | CONTROL_ROWS, INCOMPLETE_EXECUTION, NO_PREREG
r72 | INCOMPLETE | CROSSWALK, INCOMPLETE_EXECUTION, NO_PREREG_EVIDENCE
r73 | INCOMPLETE | NOT_RUN, NO_OUTCOME
r74 | INCOMPLETE | INCOMPLETE_EVIDENCE, NO_PUBLIC_CELLS, WITHDRAWN
r8 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
r9 | DESCRIPTIVE | ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION
rails-catalogue | DESCRIPTIVE | OUTCOME_CROSSWALK_MISSING, PRE_REGISTRATION_MISSING
rz1 | VALID | NONE (limits: OPERATIONAL_PAUSE, PUBLIC_SUITES, RELEASE_EVIDENCE_PARTIAL)
studio-kogen | DESCRIPTIVE | PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING
studio-kogen-80a4 | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
stack-oneshot-conformance | DESCRIPTIVE | CONDITIONS_MISMATCH, RAW_EVIDENCE_MISSING
studio-shaper-pilot | PILOT | NO_SCORED_CELLS, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
t100-cache-lane | INCOMPLETE | NOT_EXECUTED, RAW_EVIDENCE_MISSING
t98-cache-smoke | PILOT | PILOT_N1, PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING
unmapped | INVALID | COHORT_OWNERSHIP_UNRESOLVED, OUTCOME_CROSSWALK_MISSING, PRE_REGISTRATION_MISSING
x-compaction | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-context | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-continuation | INCOMPLETE | NOT_EXECUTED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-ladder | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-minikogen | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-mining | DESCRIPTIVE | DENOMINATOR_MISMATCH, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-models | DESCRIPTIVE | COHORTS_NOT_POOLABLE, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-parallel | DESCRIPTIVE | PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING, SMALL_SAMPLE
x-race | DESCRIPTIVE | ARITHMETIC_UNRECOMPUTABLE, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-recovery | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-review | DESCRIPTIVE | DENOMINATOR_MISMATCH, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-roles | DESCRIPTIVE | DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING
x-surface | INCOMPLETE | INCOMPLETE_EXECUTION, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING

luna-medium | DESCRIPTIVE | INCOMPLETE_EXECUTION, RAW_EVIDENCE_PARTIAL

gleam | DESCRIPTIVE | RAW_EVIDENCE_PARTIAL, SMALL_SAMPLE

shape1-wave1 | DESCRIPTIVE | RAW_EVIDENCE_PARTIAL, PROTOCOL_DEVIATION

## Counts per status

VALID: 10
DESCRIPTIVE: 142
PILOT: 10
INVALID: 37
INCOMPLETE: 37

## Counts per reason code

ARITHMETIC_UNRECOMPUTABLE: 1
ARM_MAPPING: 4
ARM_RECIPE: 24
CEILING: 1
COHORT: 1
COHORTS_NOT_POOLABLE: 1
COHORT_MISMATCH: 1
COHORT_OWNERSHIP_UNRESOLVED: 1
COMPARATOR: 2
CONDITIONS_MISMATCH: 8
CONFOUNDED_ASSIGNMENT: 1
CONTROL_ROWS: 1
CROSSWALK: 12
DECISION_RULE: 24
DECISION_RULE_NOT_APPLIED: 1
DECISION_RULE_UNDEFINED: 1
DECLARED_AMENDMENTS: 1
DENOMINATOR: 3
DENOMINATOR_MISMATCH: 2
DENOMINATOR_UNRESOLVED: 9
DENOMINATOR_UNVERIFIED: 1
DESCRIPTIVE_ONLY: 16
DESCRIPTIVE_ONLY_RULE: 1
DESIGN: 21
DESIGN_CHANGE: 1
ENVIRONMENT: 41
EVIDENCE: 2
EVIDENCE_PARTIAL: 1
EVIDENCE_SCOPE: 1
FILTER: 1
HISTORICAL_DATA_PRECEDES_REGISTRATION: 1
INCOMPLETE_CAPTURE: 10
INCOMPLETE_EVIDENCE: 1
INCOMPLETE_EXECUTION: 11
INVALID_CELL: 1
NOT_EXECUTED: 5
NOT_RUN: 1
NOT_SCORED: 3
NO_CANDIDATE: 1
NO_OUTCOME: 5
NO_PREREG: 46
NO_PREREG_EVIDENCE: 4
NO_PUBLIC_CELLS: 2
NO_SCORED_CELLS: 1
NO_SCORED_RESULTS: 2
OUTCOME_CLASSIFICATION: 3
OUTCOME_CLASSIFICATION_INVALID: 2
OUTCOME_CLASSIFICATION_UNRESOLVED: 1
OUTCOME_CROSSWALK: 3
OUTCOME_CROSSWALK_MISSING: 7
OUTCOME_GRADES_MISSING: 1
OUTCOME_MISMATCH: 3
PARTIAL_CAPTURE: 1
PILOT: 2
PILOT_N1: 1
POST_HOC_AMENDMENT: 1
POST_HOC_ANALYSIS: 4
POST_HOC_AUDIT: 2
POST_HOC_DIAGNOSTIC: 1
PRE_REGISTRATION: 24
PRE_REGISTRATION_MISSING: 32
PRE_REGISTRATION_UNPROVEN: 5
PROTOCOL_DEVIATION: 9
RAW_EVIDENCE_MISSING: 40
RAW_EVIDENCE_PARTIAL: 16
RECIPE: 3
REGISTERED_THRESHOLD_NOT_MET: 1
SENSITIVITY_ONLY: 1
SEPARATE_COHORTS: 1
SMALL_SAMPLE: 4
SMOKE_GATE: 1
SMOKE_ONLY: 3
TASK_MISMATCH: 2
TASK_VALIDITY_UNRESOLVED: 1
UNMATCHED_CONDITIONS: 5
UNMATCHED_EFFORT: 2
UNMATCHED_ROW: 1
WITHDRAWN: 1

fv-pilot-2026-10-10 | DESCRIPTIVE | CEILING, SMALL_SAMPLE, DECLARED_AMENDMENTS, INCOMPLETE_CAPTURE — four tasks, three repeats per arm; both arms 12/12.
l1-model-effort | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — One planned run per condition and language; the US host retired mid-experiment, one arm was interrupted, and one was not run. No winner is claimed.
arch-elixir-vs-go | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — inconclusive under both readings; zero complete pairs.
lab01-analysis-tooling-screen | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — one observation per language per set; no official grades; incomplete execution metadata; set 2 plots were not retained.
containment-small-eu | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 57 of 66 selected observations valid; 9 b cells invalid; all 33 c2 cells NOT-RUN; one EU host and three repetitions.
containment-small-eu-v2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 92 supported valid observations, 6 unsupported z resource limits, 1 invalid c2 environment-secret repetition; one test server and one kernel.
containment-small-eu-helper | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — observation-only 11-fixture comparison; 92 of 102 selected rows started and finished; unequal configurations and incomplete source capture.
review-convergence-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab screening, two tasks, one attempt per reviewer setting; no official grades.
screen-kogen-1-stage-d | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab one-lever screen stopped at a ceiling; 24 attempts, one per cell; no official grades.
screen-kogen-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab one-lever screen on four tasks, one attempt per cell; baseline 2 of 4; no official grades.
screen-kogen-1-stage-1 | INVALID | PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab baseline runs invalidated by a mid-run Lab rebuild and an external kill; interrupted; no official grades.
screen-kogen-2-first-run | INVALID | PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab screen stopped after nine attempts; a task-conversion error leaked installed packages into the model inputs; no official grades.
baseline-variance-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab development run, twelve pairs; the screen's gains did not repeat; no official grades.
review-timing-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab development run, eight triples; reviewing once let wrong code through; no official grades.
shaping-model-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab development run; specifications written in the attempt never led to a correct build; stopped by a Lab crash with the decision reached; no official grades.
builder-effort-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab development run, eight pairs; medium builder effort used fewer repairs and less input; no official grades.
confirm-builder-effort-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Kogen Lab confirmation on three new tasks, nine pairs; medium builder effort used 74% of the input at equal correctness; no official grades.
repair-stop-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab run on one task, three pairs; no correct attempt needed more than six repairs; no official grades.
review-bound-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab run on four tasks, eight attempts; review limits of one and two rounds would have submitted wrong code; no official grades.
review-bound-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab run on four tasks, 24 attempts; with the first round, a one-round review limit would have submitted wrong code in 8 of 32 attempts; no official grades.
retention-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab run on four tasks, twelve pairs; trimming old builder tool output saved 3% of input at equal correctness; no official grades.
review-independence-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab run on four tasks, twelve pairs; a reviewer shown the builder's conversation was correct in 8 of 12 against 11 of 12 and used 131% of the input; invalid first run kept; no official grades.
repair-cost-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on seven tasks, one attempt per setting; low-effort builder 5 of 7 with a median of 3 repairs; a fixer in the reviewer's model, a high-effort builder and a Sol builder 7 of 7 with medians of 2, 1 and 0; no official grades.
planner-direct-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on seven tasks, one attempt per setting, at a Kogen commit where Lab's equivalence is not measured; planner on and off in Lab both 7 of 7 with no repairs, planner off at 87% of the input; no official grades.
claude-roles-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on seven tasks, one attempt per setting, with one comparison reused from another round; a Claude Sonnet reviewer approved wrong code in 2 of 7, Claude Haiku as builder and an all-Sonnet setting 7 of 7 against 6 of 7 for the baseline; no official grades.
fixer-model-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen stopped at its input budget, 19 of 24 attempts scored, one attempt per setting; on the four tasks the baseline finished, a Sol medium fixer was correct in 4 of 4 at 70% of the input and a Luna medium fixer in 2 of 4; review-limit counterfactuals not graded; no official grades.
planner-direct-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four harder tasks, one attempt per setting, at a Kogen commit where Lab's equivalence is not measured; planner on and off in Lab both 4 of 4, planner off at 90% of the input, nearly all of the difference from one task; the run's budget guard failed soon after the start; no official grades.
claude-builder-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four harder tasks, one attempt per setting; the GPT-6.1 Sol builder 3 of 4, Claude Haiku builder 2 of 3 scored (one attempt without an outcome), Claude Sonnet builder 1 of 4; hung commands killed by hand and two untrusted evaluations disclosed; no official grades.
builder-subagents-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four tasks, one attempt per setting, in which the builder was offered a helper tool and called it 0 times, so no helper ran; no official grades.
review-fix-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four tasks, one attempt per setting, covering the new review flow only; 9 of 12 correct, 3 stopped at the repair cap before review, the earlier loop not run; no official grades.
shape-default-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four tasks, one attempt per setting, on a build whose shaping differs from Kogen's; supplied specification 4 of 4, generated shaping 3 of 4; no official grades.
blocker-stop-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on six tasks, one attempt per setting, inconclusive because neither stop was used; two attempts interrupted by a mistaken stop and run again; no official grades.
claude-review-fix-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen with two repetitions per task and small counts, on an approximate build, using one weak builder and three reviewers; in two prose-specification runs the reviewers fixed 4 of 8 wrong builds (Sonnet 3 of 5, Sol high 1 of 1, Haiku 0 of 2), and run 1 with supplied scenarios was inconclusive; no official grades.
builder-subagents-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four tasks, one attempt per setting, on an approximate build; the hint setting never called the helper and one attempt ended on a Lab commit failure; no official grades.
repeat-screen-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen with two repetitions per task, stopped at 19 of 24 attempts (2 interrupted, 3 never started); all 19 scored attempts correct, so the settings are not separated on correctness; no official grades.
review-fix-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Kogen Lab screen on four tasks, one attempt per setting, on an approximate build, comparing whole flows; interrupted and continued, with an accidental kill, a usage-limit stop and two provider refusals; no official grades.
shaping-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — one attempt per task and setting; generated shaping 4 of 4, supplied specification 3 of 3 scored with one infrastructure cell not re-run; helper settings had 3 wrong submissions against 0 without a helper; no official grades.
prose-vs-gherkin-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the default-builder run scored Gherkin 10/10 and prose 8/10, with two wrong prose submissions caused by an omitted key-order requirement; the weak-builder follow-up scored 4/4 in each setting and rescued six wrong trees; no official grades.
mechanism-split-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the initial screen stopped at its 12M-token budget with 8 of 18 attempts scored and was inconclusive; follow-up screens scored the new flow 6 of 7 and the reverted review loop 1 of 8, with 7 repair-cap stops and 3 already-correct code states; no official grades.
review-named-defect-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the original screen scored 6 of 8 in each setting; the weak-builder follow-up scored 4 of 8 and 5 of 8, had seven cap stops and one rescue, with no wrong submissions; no official grades.
builder-low-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — two repetitions per task; both builder settings scored 8 of 8 with no repairs or wrong submissions; builder input fell about 38% (651,878 to 407,155 tokens) while total input fell 4%; no official grades.
reviewer-effort-weak-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 24 attempts started and 23 scored across three runs; Sol high rescued 11/11 wrong trees and Sol medium 6/6 with thinner rescue evidence; review stage time (Lab bundle) was 2,619 s for high and 1,173 s for medium (about 55% less); no official grades.
cheap-profile-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — three runs on eight development tasks; both profiles scored 12 of 12, total input fell 37%, and the sum of recorded stage times fell 32%; run 3 added four tasks: 4/4 correct per profile, eight attempts total, with about 20.9% less input; no wrong code reached review; no official grades.
confirm-cheap-profile-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — fresh-task confirmation, eight task–repetition pairs, each tested with both profiles; both profiles correct in all eight, but lower-cost input was about 95.8% of default against a 75% rule; UNRESOLVED; no official grades.
reviewer-polish-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — development screen, eight attempts per reviewer; medium edited one already-correct tree against high's two and used about 6% less reviewer input; no wrong code reached review; no official grades.
confirm-reviewer-medium-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — fresh-task confirmation, eight attempts per reviewer; high rescued 4 of 4 wrong trees and medium 3 of 3, but medium had fewer than the four required; 56% of high's reviewer input; UNRESOLVED; no official grades.
confirm-reviewer-medium-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — second fresh-task confirmation, twelve attempts per reviewer; four builder stops before review; high rescued 4 of 4 wrong trees and medium 5 of 5, but medium used about 84.4% of high's reviewer input; UNRESOLVED; no official grades.
review-off-hard-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — development screen, 16 of 16 scored; no first-green errors among 16 against a four-error informative threshold, so NOT INFORMATIVE; approximate Lab run, no official grades.
intent-short-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — a 16-attempt development screen, both arms 8/8 correct with no wrong submissions, stops, provider refusals, or wrong first-green builds; the short arm used 19% less input; fixed decision SHORT HOLDS.
confirm-intent-short-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — a fresh-task screen scored 12 of 12 across six paired blocks; full and short were each correct in 6/6, with no wrong submissions, stops, refusals, or wrong first-green builds; short used 18% less input; the protocol's fixed decision is CONFIRMED.
review-off-hard-1-kogen | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — a one-repetition re-run of the review-off screen on real Kogen: real Kogen at b45ba32b scored 4 of 4 correct with and without review, as the Lab screen did; skipping review used 57% less input and about 45% less time, and no first-green build was wrong; no decision rule applied, development tasks, no official grades.
chatgpt-session-cache-1 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — a 24-cell comparison of real Kogen with and without a `session_id` header on a ChatGPT subscription: cached share 16% to 89% (build) and 6% to 84% (review), 12 of 12 correct in each lane, list-price cost down 67%, the rule written before the run met; one model, route and host, no official grades; plus a single-request probe (observation) and a descriptive usage-meter measurement.
review-value-2 | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 26 seeded defect cases, three Claude review settings, 234 cells: review as configured committed a wrong tree in 5 of 77 valid cells, the low-effort review in 6 of 78 and the Haiku review in 1 of 66 (11 cells lost); lighter or no review is not supported by the data; development tasks, author-made defects, no official grades; five linked pages including an OpenAI confirmation.
review-value-2-clean | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 90 cells of correct code across three review settings; all 90 committed a correct tree and no review sent a build back; no official grades.
review-value-2-natural-off | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 84 builds with review off, 79 finished; 78 correct at the first green tree and 1 wrong (upper bound 5.9% against the 2% the fixed rule asked for); 5 builds lost to a builder-stage stop; no official grades.
review-value-2-natural-reviewed | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — 126 builds; committed trees wrong in 0 of 41 (Sonnet medium), 0 of 42 (Sonnet low) and 2 of 42 (Haiku); low effort cost 6.5% more per build, Haiku 38% less but 45% slower; no official grades.
review-value-2-openai | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the same 26 seeded cases with GPT-6.1 Sol at high effort as reviewer, 78 cells: 0 committed wrong (upper bound 3.8% per cell), including both cases a Sonnet reviewer let through; $0.2053 per cell; no lighter or no-review arm; no official grades.
long-tasks-reset-fix-1-before | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the older Kogen version on four long tasks: 8 cells, 0 passed all hidden tests; 265 repeated reads after context resets; no decision rule, one machine.
long-tasks-reset-fix-1-after | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the fixed Kogen version on the same tasks: repeated reads after resets fell from 265 to 9; 0 of 10 cells passed all hidden tests (open result); no decision rule, different machines.
long-tasks-reset-fix-1-after-studio | DESCRIPTIVE | DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — two more repetitions of one long task on the fixed Kogen version: 0 of 2 passed all hidden tests; no decision rule.
