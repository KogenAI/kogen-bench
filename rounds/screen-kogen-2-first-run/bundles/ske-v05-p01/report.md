incomplete: 0 of 8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 8 cells scored)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v05-feedback-raw | 0       | 0         | 0                | 0              | 1          | unavailable  | 0 of 0        | 0           |
| p01-plan-off     | 0       | 0         | 0                | 0              | 0          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (v05-feedback-raw)
false success: 0 of 0 claims (p01-plan-off)
shaping outcomes:
v05-feedback-raw: shaping ready 1, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | v05-feedback-raw | 0       | 0         | 0                | 0              | 1          |
| r70-5-elixir | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | v05-feedback-raw | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | v05-feedback-raw | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | v05-feedback-raw | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall | model | tools/checks | requests |
|------------------|------------|------|-------|--------------|----------|
| v05-feedback-raw | shape      | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | plan       | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | build      | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | verify     | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | review     | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | commit     | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| v05-feedback-raw | assessment | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | shape      | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | plan       | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | build      | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | verify     | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | review     | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | commit     | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| p01-plan-off     | assessment | 0ms  | 0ms   | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome    | wall | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|------------|------|-------|--------------|----------|---------|---------|-----------|----------------------|
| ske-v05-p01-r70-5-elixir-r0-v05-feedback-raw-a1 | incomplete | 0ms  | 0ms   | 0ms          | 0        | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
native usage by stage and provider:
native usage by attempt and provider:
attempt outcomes included: v05-feedback-raw: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; p01-plan-off: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 0ms, model 0ms, tools/checks 0ms, requests 0
builder settings: v05-feedback-raw openai gpt-6-luna reasoning.effort=low
builder settings: p01-plan-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 1, scored 0, incorrect 0, infrastructure 0, incomplete 1
variant p01-plan-off differs from v05-feedback-raw in:
  plan.enabled: true -> false
  verify.feedback: raw -> kogen
plan.enabled: not exercised
verify.feedback: not exercised
first position per task: r70-5-elixir v05-feedback-raw 1, p01-plan-off 0 (1 repetitions, 2 variants)
first position per task: r70-5-go v05-feedback-raw 1, p01-plan-off 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir v05-feedback-raw 0, p01-plan-off 1 (1 repetitions, 2 variants)
first position per task: r70-7-go v05-feedback-raw 0, p01-plan-off 1 (1 repetitions, 2 variants)
v05-feedback-raw: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, verify.feedback)
p01-plan-off: not the Kogen profile (differs in plan.enabled, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
v05-feedback-raw: repair.context = packet,diff,check_results,review_findings (extension)
v05-feedback-raw: repair.roles = builder (extension)
v05-feedback-raw: shape.critique_prompt = lab:critique (extension)
v05-feedback-raw: shape.critique_rounds = 1 (extension)
v05-feedback-raw: verify.feedback = raw (extension)
p01-plan-off: repair.context = packet,diff,check_results,review_findings (extension)
p01-plan-off: repair.roles = builder (extension)
p01-plan-off: shape.critique_prompt = lab:critique (extension)
p01-plan-off: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
