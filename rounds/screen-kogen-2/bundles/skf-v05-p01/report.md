complete: 8/8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v05-feedback-raw | 2       | 0         | 2                | 0              | 0          | 50%          | 0 of 2        | 0           |
| p01-plan-off     | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 2 claims (v05-feedback-raw)
false success: 0 of 4 claims (p01-plan-off)
shaping outcomes:
v05-feedback-raw: shaping ready 4, shaping failed 0; correct 2 of 4
p01-plan-off: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task         | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | v05-feedback-raw | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | v05-feedback-raw | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | v05-feedback-raw | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | v05-feedback-raw | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall   | model  | tools/checks | requests |
|------------------|------------|--------|--------|--------------|----------|
| v05-feedback-raw | shape      | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | plan       | 27.7s  | 27.7s  | 0ms          | 4        |
| v05-feedback-raw | build      | 973.7s | 913.8s | 59.9s        | 103      |
| v05-feedback-raw | verify     | 22.6s  | 0ms    | 22.6s        | 0        |
| v05-feedback-raw | review     | 182.5s | 182.5s | 0ms          | 28       |
| v05-feedback-raw | commit     | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | assessment | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | shape      | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | plan       | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | build      | 947.3s | 904.8s | 42.5s        | 87       |
| p01-plan-off     | verify     | 15.1s  | 0ms    | 15.1s        | 0        |
| p01-plan-off     | review     | 157.3s | 157.3s | 0ms          | 25       |
| p01-plan-off     | commit     | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skf-v05-p01-r70-5-elixir-r0-p01-plan-off-a1     | correct          | 211.9s | 194.5s | 17.4s        | 24       | 2       | 3       | 0         | 0                    |
| skf-v05-p01-r70-5-elixir-r0-v05-feedback-raw-a1 | workflow failure | 362.8s | 335.9s | 26.9s        | 39       | 6       | 3       | 0         | 0                    |
| skf-v05-p01-r70-5-go-r0-p01-plan-off-a1         | correct          | 319.5s | 308s   | 11.5s        | 23       | 1       | 2       | 0         | 0                    |
| skf-v05-p01-r70-5-go-r0-v05-feedback-raw-a1     | correct          | 182.6s | 173.1s | 9.5s         | 25       | 2       | 3       | 0         | 0                    |
| skf-v05-p01-r70-7-elixir-r0-p01-plan-off-a1     | correct          | 455.4s | 419.7s | 35.7s        | 49       | 5       | 3       | 0         | 0                    |
| skf-v05-p01-r70-7-elixir-r0-v05-feedback-raw-a1 | workflow failure | 569.4s | 517.7s | 51.7s        | 58       | 6       | 4       | 0         | 0                    |
| skf-v05-p01-r70-7-go-r0-p01-plan-off-a1         | correct          | 147.8s | 139.9s | 7.8s         | 16       | 1       | 2       | 0         | 0                    |
| skf-v05-p01-r70-7-go-r0-v05-feedback-raw-a1     | correct          | 107.8s | 97.4s  | 10.4s        | 13       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
p01-plan-off openai: input 1.87M, cached 0.59M, output 36.5k, reasoning 851, input_tokens_details.cache_write_tokens 0, total_tokens 1.90M
v05-feedback-raw openai: input 2.21M, cached 0.78M, output 35.9k, reasoning 692, input_tokens_details.cache_write_tokens 0, total_tokens 2.25M
native usage by stage and provider:
stage build p01-plan-off openai (responses): input 1.49M, cached 0.59M, output 33.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.52M
stage build v05-feedback-raw openai (responses): input 1.76M, cached 0.78M, output 31.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.79M
stage plan v05-feedback-raw openai (responses): input 17.2k, cached 0, output 869, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.1k
stage review p01-plan-off openai (responses): input 0.38M, cached 0, output 3.0k, reasoning 851, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
stage review v05-feedback-raw openai (responses): input 0.43M, cached 0, output 3.1k, reasoning 692, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
native usage by attempt and provider:
attempt usage skf-v05-p01-r70-5-elixir-r0-p01-plan-off-a1 openai (responses): input 0.28M, cached 54.7k, output 6.1k, reasoning 400, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage skf-v05-p01-r70-5-elixir-r0-v05-feedback-raw-a1 openai (responses): input 0.64M, cached 0.19M, output 10.9k, reasoning 204, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
attempt usage skf-v05-p01-r70-5-go-r0-p01-plan-off-a1 openai (responses): input 0.30M, cached 74.1k, output 12.9k, reasoning 158, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage skf-v05-p01-r70-5-go-r0-v05-feedback-raw-a1 openai (responses): input 0.27M, cached 49.9k, output 4.6k, reasoning 199, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage skf-v05-p01-r70-7-elixir-r0-p01-plan-off-a1 openai (responses): input 1.10M, cached 0.45M, output 12.9k, reasoning 202, input_tokens_details.cache_write_tokens 0, total_tokens 1.12M
attempt usage skf-v05-p01-r70-7-elixir-r0-v05-feedback-raw-a1 openai (responses): input 1.19M, cached 0.53M, output 17.3k, reasoning 229, input_tokens_details.cache_write_tokens 0, total_tokens 1.21M
attempt usage skf-v05-p01-r70-7-go-r0-p01-plan-off-a1 openai (responses): input 0.18M, cached 4.6k, output 4.5k, reasoning 91, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage skf-v05-p01-r70-7-go-r0-v05-feedback-raw-a1 openai (responses): input 0.12M, cached 6.1k, output 3.2k, reasoning 60, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt outcomes included: v05-feedback-raw: correct 2, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0; p01-plan-off: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2357.1s, model 2186.1s, tools/checks 171s, requests 247
builder settings: v05-feedback-raw openai gpt-6-luna reasoning.effort=low
builder settings: p01-plan-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant p01-plan-off differs from v05-feedback-raw in:
  plan.enabled: true -> false
  verify.feedback: raw -> kogen
P01: exercised in 4 of 4 p01-plan-off attempts
V05: exercised in 4 of 4 p01-plan-off attempts
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
