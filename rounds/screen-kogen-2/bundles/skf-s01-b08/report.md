complete: 8/8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant                       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-------------------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| s01-shaping-generated         | 0       | 0         | 4                | 0              | 0          | 0%           | 0 of 0        | 0           |
| b08-builder-testing-rules-off | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 0 claims (s01-shaping-generated)
false success: 0 of 4 claims (b08-builder-testing-rules-off)
shaping outcomes:
s01-shaping-generated: shaping ready 3, shaping failed 1 (shaping_failed); correct 0 of 4
b08-builder-testing-rules-off: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task         | variant                       | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-------------------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | s01-shaping-generated         | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | s01-shaping-generated         | 0       | 0         | 1                | 0              | 0          |
| r70-5-go     | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | s01-shaping-generated         | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | s01-shaping-generated         | 0       | 0         | 1                | 0              | 0          |
| r70-7-go     | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant                       | stage      | wall    | model   | tools/checks | requests |
|-------------------------------|------------|---------|---------|--------------|----------|
| s01-shaping-generated         | shape      | 215.4s  | 215.4s  | 0ms          | 12       |
| s01-shaping-generated         | plan       | 21.8s   | 21.8s   | 0ms          | 3        |
| s01-shaping-generated         | build      | 458.4s  | 418.6s  | 39.8s        | 66       |
| s01-shaping-generated         | verify     | 23.3s   | 0ms     | 23.3s        | 0        |
| s01-shaping-generated         | review     | 0ms     | 0ms     | 0ms          | 0        |
| s01-shaping-generated         | commit     | 0ms     | 0ms     | 0ms          | 0        |
| s01-shaping-generated         | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| s01-shaping-generated         | assessment | 0ms     | 0ms     | 0ms          | 0        |
| b08-builder-testing-rules-off | shape      | 0ms     | 0ms     | 0ms          | 0        |
| b08-builder-testing-rules-off | plan       | 26.3s   | 26.3s   | 0ms          | 4        |
| b08-builder-testing-rules-off | build      | 1767.1s | 1707.4s | 59.7s        | 85       |
| b08-builder-testing-rules-off | verify     | 26.2s   | 0ms     | 26.2s        | 0        |
| b08-builder-testing-rules-off | review     | 199.7s  | 199.7s  | 0ms          | 36       |
| b08-builder-testing-rules-off | commit     | 0ms     | 0ms     | 0ms          | 0        |
| b08-builder-testing-rules-off | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| b08-builder-testing-rules-off | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                                      | outcome          | wall   | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------------------------------|------------------|--------|---------|--------------|----------|---------|---------|-----------|----------------------|
| skf-s01-b08-r70-5-elixir-r0-b08-builder-testing-rules-off-a1 | correct          | 1265s  | 1215.3s | 49.7s        | 46       | 6       | 3       | 0         | 0                    |
| skf-s01-b08-r70-5-elixir-r0-s01-shaping-generated-a1         | workflow failure | 302.5s | 260.4s  | 42.1s        | 38       | 6       | 0       | 0         | 0                    |
| skf-s01-b08-r70-5-go-r0-b08-builder-testing-rules-off-a1     | correct          | 298.8s | 281.1s  | 17.7s        | 31       | 2       | 3       | 0         | 0                    |
| skf-s01-b08-r70-5-go-r0-s01-shaping-generated-a1             | workflow failure | 175.8s | 156.8s  | 19.1s        | 22       | 6       | 0       | 0         | 0                    |
| skf-s01-b08-r70-7-elixir-r0-b08-builder-testing-rules-off-a1 | correct          | 339s   | 312.9s  | 26.1s        | 33       | 2       | 3       | 0         | 0                    |
| skf-s01-b08-r70-7-elixir-r0-s01-shaping-generated-a1         | workflow failure | 61.6s  | 58.2s   | 3.4s         | 4        | 0       | 0       | 0         | 0                    |
| skf-s01-b08-r70-7-go-r0-b08-builder-testing-rules-off-a1     | correct          | 140.2s | 124.1s  | 16.1s        | 15       | 1       | 2       | 0         | 0                    |
| skf-s01-b08-r70-7-go-r0-s01-shaping-generated-a1             | workflow failure | 201s   | 180.4s  | 20.5s        | 17       | 6       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
b08-builder-testing-rules-off openai: input 1.46M, cached 0.30M, output 33.6k, reasoning 561, input_tokens_details.cache_write_tokens 0, total_tokens 1.49M
s01-shaping-generated openai: input 1.03M, cached 0.29M, output 21.5k, reasoning 22, input_tokens_details.cache_write_tokens 0, total_tokens 1.05M
native usage by stage and provider:
stage build b08-builder-testing-rules-off openai (responses): input 0.91M, cached 0.28M, output 29.6k, reasoning 66, input_tokens_details.cache_write_tokens 0, total_tokens 0.94M
stage build s01-shaping-generated openai (responses): input 0.94M, cached 0.27M, output 11.1k, reasoning 22, input_tokens_details.cache_write_tokens 0, total_tokens 0.95M
stage plan b08-builder-testing-rules-off openai (responses): input 17.2k, cached 0, output 831, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.0k
stage plan s01-shaping-generated openai (responses): input 9.7k, cached 0, output 731, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 10.5k
stage review b08-builder-testing-rules-off openai (responses): input 0.53M, cached 14.7k, output 3.2k, reasoning 495, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
stage shape s01-shaping-generated openai (responses): input 77.2k, cached 14.2k, output 9.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 86.9k
native usage by attempt and provider:
attempt usage skf-s01-b08-r70-5-elixir-r0-b08-builder-testing-rules-off-a1 openai (responses): input 0.58M, cached 0.13M, output 8.5k, reasoning 241, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage skf-s01-b08-r70-5-elixir-r0-s01-shaping-generated-a1 openai (responses): input 0.57M, cached 0.21M, output 7.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt usage skf-s01-b08-r70-5-go-r0-b08-builder-testing-rules-off-a1 openai (responses): input 0.35M, cached 71.8k, output 10.0k, reasoning 97, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage skf-s01-b08-r70-5-go-r0-s01-shaping-generated-a1 openai (responses): input 0.19M, cached 52.7k, output 4.9k, reasoning 22, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage skf-s01-b08-r70-7-elixir-r0-b08-builder-testing-rules-off-a1 openai (responses): input 0.40M, cached 97.4k, output 10.7k, reasoning 114, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage skf-s01-b08-r70-7-elixir-r0-s01-shaping-generated-a1 openai (responses): input 29.1k, cached 7.2k, output 2.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.6k
attempt usage skf-s01-b08-r70-7-go-r0-b08-builder-testing-rules-off-a1 openai (responses): input 0.13M, cached 0, output 4.3k, reasoning 109, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage skf-s01-b08-r70-7-go-r0-s01-shaping-generated-a1 openai (responses): input 0.24M, cached 14.5k, output 7.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt outcomes included: s01-shaping-generated: correct 0, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0; b08-builder-testing-rules-off: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2783.8s, model 2589.2s, tools/checks 194.6s, requests 206
builder settings: s01-shaping-generated openai gpt-6-luna reasoning.effort=low
builder settings: b08-builder-testing-rules-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant b08-builder-testing-rules-off differs from s01-shaping-generated in:
  shape.source: generate -> supplied
  testing_rules.roles: shaper,planner,builder,reviewer -> shaper,planner,reviewer
B08: exercised in 4 of 4 b08-builder-testing-rules-off attempts
MODE: exercised in 4 of 4 b08-builder-testing-rules-off attempts
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
