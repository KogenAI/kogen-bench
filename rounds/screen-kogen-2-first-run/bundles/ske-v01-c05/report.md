incomplete: 0 of 8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 8 cells scored)
## CMP-1 Correctness
| variant             | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v01-verify-off      | 0       | 0         | 0                | 1              | 0          | unavailable  | 0 of 0        | 0           |
| c05-review-advisory | 0       | 0         | 0                | 0              | 1          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (v01-verify-off)
false success: 0 of 0 claims (c05-review-advisory)
shaping outcomes:
v01-verify-off: shaping ready 1, shaping failed 0; correct 0 of 0
c05-review-advisory: shaping ready 1, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant             | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | v01-verify-off      | 0       | 0         | 0                | 1              | 0          |
| r70-5-elixir | c05-review-advisory | 0       | 0         | 0                | 0              | 1          |
| r70-5-go     | v01-verify-off      | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | c05-review-advisory | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | v01-verify-off      | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | c05-review-advisory | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | v01-verify-off      | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | c05-review-advisory | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant             | stage      | wall   | model  | tools/checks | requests |
|---------------------|------------|--------|--------|--------------|----------|
| v01-verify-off      | shape      | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | plan       | 8.9s   | 8.9s   | 0ms          | 1        |
| v01-verify-off      | build      | 115.1s | 108.5s | 6.5s         | 8        |
| v01-verify-off      | verify     | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | review     | 224.6s | 224.6s | 0ms          | 1        |
| v01-verify-off      | commit     | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | assessment | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | shape      | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | plan       | 7.2s   | 7.2s   | 0ms          | 1        |
| c05-review-advisory | build      | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | verify     | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | review     | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | commit     | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                            | outcome        | wall   | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------------------|----------------|--------|-------|--------------|----------|---------|---------|-----------|----------------------|
| ske-v01-c05-r70-5-elixir-r0-c05-review-advisory-a1 | incomplete     | 9.5s   | 7.2s  | 2.3s         | 1        | 0       | 0       | 0         | 0                    |
| ske-v01-c05-r70-5-elixir-r0-v01-verify-off-a1      | infrastructure | 351.1s | 342s  | 9s           | 10       | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
c05-review-advisory openai: input 34.3k, cached 0, output 219, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.5k
v01-verify-off openai: input 0.34M, cached 38.0k, output 4.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
native usage by stage and provider:
stage build v01-verify-off openai (responses): input 0.31M, cached 38.0k, output 4.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
stage plan c05-review-advisory openai (responses): input 34.3k, cached 0, output 219, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.5k
stage plan v01-verify-off openai (responses): input 34.3k, cached 0, output 269, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.6k
native usage by attempt and provider:
attempt usage ske-v01-c05-r70-5-elixir-r0-c05-review-advisory-a1 openai (responses): input 34.3k, cached 0, output 219, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.5k
attempt usage ske-v01-c05-r70-5-elixir-r0-v01-verify-off-a1 openai (responses): input 0.34M, cached 38.0k, output 4.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt outcomes included: v01-verify-off: correct 0, incorrect 0, workflow failure 0, infrastructure 1, incomplete 0; c05-review-advisory: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 360.6s, model 349.2s, tools/checks 11.3s, requests 11
builder settings: v01-verify-off openai gpt-6-luna reasoning.effort=low
builder settings: c05-review-advisory openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 2, scored 0, incorrect 0, infrastructure 1, incomplete 1
variant c05-review-advisory differs from v01-verify-off in:
  review.effect: blocking -> advisory
  verify.enabled: false -> true
review.effect: not exercised (no review returned changes)
V01: exercised in 1 of 1 c05-review-advisory attempts
first position per task: r70-5-elixir v01-verify-off 1, c05-review-advisory 0 (1 repetitions, 2 variants)
first position per task: r70-5-go v01-verify-off 1, c05-review-advisory 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir v01-verify-off 0, c05-review-advisory 1 (1 repetitions, 2 variants)
first position per task: r70-7-go v01-verify-off 0, c05-review-advisory 1 (1 repetitions, 2 variants)
v01-verify-off: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, verify.enabled)
c05-review-advisory: not the Kogen profile (differs in review.effect, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
v01-verify-off: repair.context = packet,diff,check_results,review_findings (extension)
v01-verify-off: repair.roles = builder (extension)
v01-verify-off: shape.critique_prompt = lab:critique (extension)
v01-verify-off: shape.critique_rounds = 1 (extension)
c05-review-advisory: repair.context = packet,diff,check_results,review_findings (extension)
c05-review-advisory: repair.roles = builder (extension)
c05-review-advisory: review.effect = advisory (extension)
c05-review-advisory: shape.critique_prompt = lab:critique (extension)
c05-review-advisory: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
