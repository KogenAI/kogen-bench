complete: 8/8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant             | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v01-verify-off      | 0       | 0         | 4                | 0              | 0          | 0%           | 0 of 0        | 0           |
| c05-review-advisory | 1       | 3         | 0                | 0              | 0          | 25%          | 3 of 4        | 0           |
false success: 0 of 0 claims (v01-verify-off)
false success: 3 of 4 claims (c05-review-advisory)
shaping outcomes:
v01-verify-off: shaping ready 4, shaping failed 0; correct 0 of 4
c05-review-advisory: shaping ready 4, shaping failed 0; correct 1 of 4
## Per-task outcomes
| task         | variant             | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | v01-verify-off      | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | c05-review-advisory | 0       | 1         | 0                | 0              | 0          |
| r70-5-go     | v01-verify-off      | 0       | 0         | 1                | 0              | 0          |
| r70-5-go     | c05-review-advisory | 0       | 1         | 0                | 0              | 0          |
| r70-7-elixir | v01-verify-off      | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | c05-review-advisory | 0       | 1         | 0                | 0              | 0          |
| r70-7-go     | v01-verify-off      | 0       | 0         | 1                | 0              | 0          |
| r70-7-go     | c05-review-advisory | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant             | stage      | wall    | model   | tools/checks | requests |
|---------------------|------------|---------|---------|--------------|----------|
| v01-verify-off      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| v01-verify-off      | plan       | 29.8s   | 29.8s   | 0ms          | 4        |
| v01-verify-off      | build      | 1963.3s | 1883.7s | 79.6s        | 125      |
| v01-verify-off      | verify     | 0ms     | 0ms     | 0ms          | 0        |
| v01-verify-off      | review     | 630.5s  | 630.5s  | 0ms          | 94       |
| v01-verify-off      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| v01-verify-off      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| v01-verify-off      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| c05-review-advisory | shape      | 0ms     | 0ms     | 0ms          | 0        |
| c05-review-advisory | plan       | 25.4s   | 25.4s   | 0ms          | 4        |
| c05-review-advisory | build      | 528.2s  | 498.7s  | 29.5s        | 55       |
| c05-review-advisory | verify     | 9.3s    | 0ms     | 9.3s         | 0        |
| c05-review-advisory | review     | 48.9s   | 48.9s   | 0ms          | 5        |
| c05-review-advisory | commit     | 0ms     | 0ms     | 0ms          | 0        |
| c05-review-advisory | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| c05-review-advisory | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                            | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| skf-v01-c05-r70-5-elixir-r0-c05-review-advisory-a1 | incorrect        | 154.1s  | 139.7s  | 14.3s        | 15       | 1       | 1       | 0         | 0                    |
| skf-v01-c05-r70-5-elixir-r0-v01-verify-off-a1      | workflow failure | 536.7s  | 498.6s  | 38.1s        | 63       | 6       | 7       | 0         | 0                    |
| skf-v01-c05-r70-5-go-r0-c05-review-advisory-a1     | incorrect        | 193.9s  | 180.3s  | 13.6s        | 21       | 3       | 1       | 0         | 0                    |
| skf-v01-c05-r70-5-go-r0-v01-verify-off-a1          | workflow failure | 448.6s  | 432s    | 16.6s        | 58       | 6       | 7       | 0         | 0                    |
| skf-v01-c05-r70-7-elixir-r0-c05-review-advisory-a1 | incorrect        | 161.4s  | 148.2s  | 13.3s        | 16       | 1       | 1       | 0         | 0                    |
| skf-v01-c05-r70-7-elixir-r0-v01-verify-off-a1      | workflow failure | 1268.5s | 1246.7s | 21.8s        | 51       | 6       | 7       | 0         | 0                    |
| skf-v01-c05-r70-7-go-r0-c05-review-advisory-a1     | correct          | 115.7s  | 104.9s  | 10.8s        | 12       | 0       | 1       | 0         | 0                    |
| skf-v01-c05-r70-7-go-r0-v01-verify-off-a1          | workflow failure | 386.6s  | 366.7s  | 19.9s        | 51       | 6       | 7       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
c05-review-advisory openai: input 0.66M, cached 0.17M, output 19.8k, reasoning 201, input_tokens_details.cache_write_tokens 0, total_tokens 0.68M
v01-verify-off openai: input 3.35M, cached 0.93M, output 43.6k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 3.39M
native usage by stage and provider:
stage build c05-review-advisory openai (responses): input 0.56M, cached 0.17M, output 17.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
stage build v01-verify-off openai (responses): input 1.89M, cached 0.85M, output 31.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.92M
stage plan c05-review-advisory openai (responses): input 17.2k, cached 0, output 811, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.0k
stage plan v01-verify-off openai (responses): input 17.2k, cached 4.1k, output 829, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.0k
stage review c05-review-advisory openai (responses): input 75.6k, cached 0, output 1.3k, reasoning 201, input_tokens_details.cache_write_tokens 0, total_tokens 76.9k
stage review v01-verify-off openai (responses): input 1.44M, cached 75.6k, output 11.0k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.45M
native usage by attempt and provider:
attempt usage skf-v01-c05-r70-5-elixir-r0-c05-review-advisory-a1 openai (responses): input 0.14M, cached 45.2k, output 5.1k, reasoning 25, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage skf-v01-c05-r70-5-elixir-r0-v01-verify-off-a1 openai (responses): input 1.14M, cached 0.32M, output 14.7k, reasoning 554, input_tokens_details.cache_write_tokens 0, total_tokens 1.15M
attempt usage skf-v01-c05-r70-5-go-r0-c05-review-advisory-a1 openai (responses): input 0.22M, cached 49.8k, output 6.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage skf-v01-c05-r70-5-go-r0-v01-verify-off-a1 openai (responses): input 0.80M, cached 0.23M, output 11.7k, reasoning 655, input_tokens_details.cache_write_tokens 0, total_tokens 0.81M
attempt usage skf-v01-c05-r70-7-elixir-r0-c05-review-advisory-a1 openai (responses): input 0.20M, cached 49.4k, output 5.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage skf-v01-c05-r70-7-elixir-r0-v01-verify-off-a1 openai (responses): input 0.72M, cached 0.24M, output 8.3k, reasoning 640, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
attempt usage skf-v01-c05-r70-7-go-r0-c05-review-advisory-a1 openai (responses): input 0.11M, cached 26.8k, output 3.6k, reasoning 176, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage skf-v01-c05-r70-7-go-r0-v01-verify-off-a1 openai (responses): input 0.69M, cached 0.15M, output 9.0k, reasoning 901, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
attempt outcomes included: v01-verify-off: correct 0, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0; c05-review-advisory: correct 1, incorrect 3, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 3265.5s, model 3117.1s, tools/checks 148.4s, requests 287
builder settings: v01-verify-off openai gpt-6-luna reasoning.effort=low
builder settings: c05-review-advisory openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 3, infrastructure 0, incomplete 0
variant c05-review-advisory differs from v01-verify-off in:
  review.effect: blocking -> advisory
  verify.enabled: false -> true
review returned changes in 4 of 4 v01-verify-off attempts
V01: exercised in 4 of 4 c05-review-advisory attempts
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
