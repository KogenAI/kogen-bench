incomplete: 0 of 8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 8 cells scored)
## CMP-1 Correctness
| variant                       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-------------------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| s01-shaping-generated         | 0       | 0         | 0                | 0              | 1          | unavailable  | 0 of 0        | 0           |
| b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (s01-shaping-generated)
false success: 0 of 0 claims (b08-builder-testing-rules-off)
shaping outcomes:
s01-shaping-generated: shaping ready 1, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant                       | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-------------------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | s01-shaping-generated         | 0       | 0         | 0                | 0              | 1          |
| r70-5-elixir | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | s01-shaping-generated         | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | s01-shaping-generated         | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | s01-shaping-generated         | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant                       | stage      | wall | model | tools/checks | requests |
|-------------------------------|------------|------|-------|--------------|----------|
| s01-shaping-generated         | shape      | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | plan       | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | build      | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | verify     | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | review     | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | commit     | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| s01-shaping-generated         | assessment | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | shape      | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | plan       | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | build      | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | verify     | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | review     | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | commit     | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| b08-builder-testing-rules-off | assessment | 0ms  | 0ms   | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                              | outcome    | wall | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------------------|------------|------|-------|--------------|----------|---------|---------|-----------|----------------------|
| ske-s01-b08-r70-5-elixir-r0-s01-shaping-generated-a1 | incomplete | 0ms  | 0ms   | 0ms          | 0        | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
native usage by stage and provider:
native usage by attempt and provider:
attempt outcomes included: s01-shaping-generated: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; b08-builder-testing-rules-off: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 0ms, model 0ms, tools/checks 0ms, requests 0
builder settings: s01-shaping-generated openai gpt-6-luna reasoning.effort=low
builder settings: b08-builder-testing-rules-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 1, scored 0, incorrect 0, infrastructure 0, incomplete 1
variant b08-builder-testing-rules-off differs from s01-shaping-generated in:
  shape.source: generate -> supplied
  testing_rules.roles: shaper,planner,builder,reviewer -> shaper,planner,reviewer
testing_rules.roles: not exercised
shape.source: not exercised
first position per task: r70-5-elixir s01-shaping-generated 1, b08-builder-testing-rules-off 0 (1 repetitions, 2 variants)
first position per task: r70-5-go s01-shaping-generated 1, b08-builder-testing-rules-off 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir s01-shaping-generated 0, b08-builder-testing-rules-off 1 (1 repetitions, 2 variants)
first position per task: r70-7-go s01-shaping-generated 0, b08-builder-testing-rules-off 1 (1 repetitions, 2 variants)
s01-shaping-generated: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
b08-builder-testing-rules-off: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, testing_rules.roles)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
s01-shaping-generated: repair.context = packet,diff,check_results,review_findings (extension)
s01-shaping-generated: repair.roles = builder (extension)
s01-shaping-generated: shape.critique_prompt = lab:critique (extension)
s01-shaping-generated: shape.critique_rounds = 1 (extension)
b08-builder-testing-rules-off: repair.context = packet,diff,check_results,review_findings (extension)
b08-builder-testing-rules-off: repair.roles = builder (extension)
b08-builder-testing-rules-off: shape.critique_prompt = lab:critique (extension)
b08-builder-testing-rules-off: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
