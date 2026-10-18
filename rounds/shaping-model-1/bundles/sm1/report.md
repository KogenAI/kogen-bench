incomplete: 18 of 24 cells scored
Question: shaping-model-1: does shaping in the attempt by gpt-6.1-sol low reach the correctness of a supplied specification where gpt-6-luna low does not?
Hypothesis: shape-sol is within one block of supplied; shape-luna is at least three blocks lower
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (18 of 24 cells scored)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| supplied   | 4       | 0         | 1                | 0              | 1          | 80%          | 0 of 4        | 0           |
| shape-luna | 0       | 0         | 8                | 0              | 0          | 0%           | 0 of 0        | 0           |
| shape-sol  | 0       | 0         | 5                | 0              | 3          | 0%           | 0 of 0        | 0           |
false success: 0 of 4 claims (supplied)
false success: 0 of 0 claims (shape-luna)
false success: 0 of 0 claims (shape-sol)
shaping outcomes:
supplied: shaping ready 6, shaping failed 0; correct 4 of 5
shape-luna: shaping ready 3, shaping failed 5 (shaping_failed); correct 0 of 8
shape-sol: shaping ready 7, shaping failed 1; correct 0 of 5
## Per-task outcomes
| task         | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | supplied   | 0       | 0         | 1                | 0              | 1          |
| r70-5-elixir | shape-luna | 0       | 0         | 2                | 0              | 0          |
| r70-5-elixir | shape-sol  | 0       | 0         | 2                | 0              | 0          |
| r70-5-go     | supplied   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | shape-luna | 0       | 0         | 2                | 0              | 0          |
| r70-5-go     | shape-sol  | 0       | 0         | 1                | 0              | 1          |
| r70-7-elixir | supplied   | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | shape-luna | 0       | 0         | 2                | 0              | 0          |
| r70-7-elixir | shape-sol  | 0       | 0         | 2                | 0              | 0          |
| r70-7-go     | supplied   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | shape-luna | 0       | 0         | 2                | 0              | 0          |
| r70-7-go     | shape-sol  | 0       | 0         | 0                | 0              | 2          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| supplied   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| supplied   | plan       | 54.8s   | 54.8s   | 0ms          | 5        |
| supplied   | build      | 1939.6s | 1850.9s | 88.7s        | 107      |
| supplied   | verify     | 29.6s   | 0ms     | 29.6s        | 0        |
| supplied   | review     | 413.3s  | 413.3s  | 0ms          | 36       |
| supplied   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| supplied   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| supplied   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| shape-luna | shape      | 717.5s  | 717.5s  | 0ms          | 35       |
| shape-luna | plan       | 83.4s   | 83.4s   | 0ms          | 3        |
| shape-luna | build      | 2548.6s | 2509.8s | 38.9s        | 104      |
| shape-luna | verify     | 18.4s   | 0ms     | 18.4s        | 0        |
| shape-luna | review     | 32.6s   | 32.6s   | 0ms          | 2        |
| shape-luna | commit     | 0ms     | 0ms     | 0ms          | 0        |
| shape-luna | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| shape-luna | assessment | 0ms     | 0ms     | 0ms          | 0        |
| shape-sol  | shape      | 2209.5s | 2209.5s | 0ms          | 35       |
| shape-sol  | plan       | 81.4s   | 81.4s   | 0ms          | 5        |
| shape-sol  | build      | 3395s   | 3309.5s | 85.5s        | 144      |
| shape-sol  | verify     | 90.4s   | 0ms     | 90.4s        | 0        |
| shape-sol  | review     | 369.9s  | 369.9s  | 0ms          | 30       |
| shape-sol  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| shape-sol  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| shape-sol  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| sm1-r70-5-elixir-r0-shape-luna-a1 | workflow failure | 493.8s  | 472.4s  | 21.4s        | 27       | 6       | 0       | 0         | 0                    |
| sm1-r70-5-elixir-r0-shape-sol-a1  | workflow failure | 1732.4s | 1678.8s | 53.6s        | 48       | 6       | 0       | 0         | 0                    |
| sm1-r70-5-elixir-r0-supplied-a1   | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 0       | 0         | 0                    |
| sm1-r70-5-elixir-r1-shape-luna-a1 | workflow failure | 120s    | 117.7s  | 2.4s         | 6        | 0       | 0       | 2         | 0                    |
| sm1-r70-5-elixir-r1-shape-sol-a1  | workflow failure | 1249.7s | 1209.5s | 40.2s        | 64       | 6       | 7       | 0         | 0                    |
| sm1-r70-5-elixir-r1-supplied-a1   | workflow failure | 584.2s  | 561.2s  | 22.9s        | 36       | 6       | 0       | 0         | 0                    |
| sm1-r70-5-go-r0-shape-luna-a1     | workflow failure | 1955.5s | 1930s   | 25.6s        | 62       | 6       | 2       | 0         | 0                    |
| sm1-r70-5-go-r0-shape-sol-a1      | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 0       | 0         | 0                    |
| sm1-r70-5-go-r1-shape-luna-a1     | workflow failure | 142.4s  | 134.5s  | 7.9s         | 4        | 0       | 0       | 0         | 0                    |
| sm1-r70-5-go-r1-shape-sol-a1      | workflow failure | 1786.9s | 1737.6s | 49.3s        | 38       | 6       | 0       | 0         | 0                    |
| sm1-r70-5-go-r1-supplied-a1       | correct          | 480.3s  | 456.2s  | 24s          | 28       | 2       | 3       | 0         | 0                    |
| sm1-r70-7-elixir-r0-shape-luna-a1 | workflow failure | 97.7s   | 95.6s   | 2.1s         | 4        | 0       | 0       | 0         | 0                    |
| sm1-r70-7-elixir-r0-shape-sol-a1  | workflow failure | 860.8s  | 838.6s  | 22.2s        | 38       | 6       | 1       | 0         | 0                    |
| sm1-r70-7-elixir-r0-supplied-a1   | correct          | 561.6s  | 521.5s  | 40.1s        | 38       | 3       | 4       | 0         | 0                    |
| sm1-r70-7-elixir-r1-shape-luna-a1 | workflow failure | 83s     | 79.6s   | 3.4s         | 6        | 0       | 0       | 1         | 0                    |
| sm1-r70-7-elixir-r1-shape-sol-a1  | workflow failure | 546.1s  | 505.8s  | 40.2s        | 26       | 6       | 0       | 0         | 0                    |
| sm1-r70-7-elixir-r1-supplied-a1   | correct          | 673.9s  | 623.6s  | 50.2s        | 37       | 3       | 4       | 0         | 0                    |
| sm1-r70-7-go-r0-shape-luna-a1     | workflow failure | 456.2s  | 429.9s  | 26.3s        | 31       | 6       | 0       | 0         | 0                    |
| sm1-r70-7-go-r0-shape-sol-a1      | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 0       | 0         | 0                    |
| sm1-r70-7-go-r0-supplied-a1       | correct          | 163.5s  | 156.3s  | 7.1s         | 9        | 0       | 1       | 0         | 0                    |
| sm1-r70-7-go-r1-shape-luna-a1     | workflow failure | 89.3s   | 83.6s   | 5.7s         | 4        | 0       | 0       | 0         | 0                    |
| sm1-r70-7-go-r1-shape-sol-a1      | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
shape-luna openai: input 2.06M, cached 0.89M, output 51.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.11M
shape-sol openai: input 3.38M, cached 1.07M, output 99.6k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 3.48M
supplied openai: input 2.12M, cached 0.58M, output 39.0k, reasoning 838, input_tokens_details.cache_write_tokens 0, total_tokens 2.16M
native usage by stage and provider:
stage build shape-luna openai (responses): input 1.79M, cached 0.87M, output 28.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.81M
stage build shape-sol openai (responses): input 2.73M, cached 1.04M, output 59.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.79M
stage build supplied openai (responses): input 1.55M, cached 0.57M, output 34.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.59M
stage plan shape-luna openai (responses): input 8.2k, cached 0, output 664, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 8.9k
stage plan shape-sol openai (responses): input 21.2k, cached 0, output 1.4k, reasoning 85, input_tokens_details.cache_write_tokens 0, total_tokens 22.6k
stage plan supplied openai (responses): input 21.5k, cached 0, output 1.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 22.6k
stage review shape-luna openai (responses): input 20.3k, cached 0, output 915, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 21.2k
stage review shape-sol openai (responses): input 0.37M, cached 23.0k, output 5.0k, reasoning 426, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
stage review supplied openai (responses): input 0.55M, cached 14.7k, output 3.1k, reasoning 838, input_tokens_details.cache_write_tokens 0, total_tokens 0.55M
stage shape shape-luna openai (responses): input 0.24M, cached 13.8k, output 21.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
stage shape shape-sol openai (responses): input 0.25M, cached 4.6k, output 34.2k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
native usage by attempt and provider:
attempt usage sm1-r70-5-elixir-r0-shape-luna-a1 openai (responses): input 0.24M, cached 41.3k, output 6.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage sm1-r70-5-elixir-r0-shape-sol-a1 openai (responses): input 0.95M, cached 0.38M, output 20.1k, reasoning 252, input_tokens_details.cache_write_tokens 0, total_tokens 0.97M
attempt usage sm1-r70-5-elixir-r1-shape-luna-a1 openai (responses): input 37.8k, cached 0, output 2.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 40.0k
attempt usage sm1-r70-5-elixir-r1-shape-sol-a1 openai (responses): input 0.88M, cached 0.17M, output 27.3k, reasoning 628, input_tokens_details.cache_write_tokens 0, total_tokens 0.90M
attempt usage sm1-r70-5-elixir-r1-supplied-a1 openai (responses): input 0.71M, cached 0.31M, output 8.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
attempt usage sm1-r70-5-go-r0-shape-luna-a1 openai (responses): input 1.23M, cached 0.65M, output 22.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.25M
attempt usage sm1-r70-5-go-r1-shape-luna-a1 openai (responses): input 28.0k, cached 0, output 4.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 32.2k
attempt usage sm1-r70-5-go-r1-shape-sol-a1 openai (responses): input 0.49M, cached 0.18M, output 16.1k, reasoning 451, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
attempt usage sm1-r70-5-go-r1-supplied-a1 openai (responses): input 0.31M, cached 52.0k, output 6.4k, reasoning 277, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage sm1-r70-7-elixir-r0-shape-luna-a1 openai (responses): input 30.5k, cached 9.2k, output 3.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.1k
attempt usage sm1-r70-7-elixir-r0-shape-sol-a1 openai (responses): input 0.77M, cached 0.24M, output 24.0k, reasoning 494, input_tokens_details.cache_write_tokens 0, total_tokens 0.79M
attempt usage sm1-r70-7-elixir-r0-supplied-a1 openai (responses): input 0.54M, cached 0.11M, output 10.9k, reasoning 290, input_tokens_details.cache_write_tokens 0, total_tokens 0.55M
attempt usage sm1-r70-7-elixir-r1-shape-luna-a1 openai (responses): input 43.6k, cached 4.6k, output 2.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 46.1k
attempt usage sm1-r70-7-elixir-r1-shape-sol-a1 openai (responses): input 0.29M, cached 94.3k, output 12.0k, reasoning 120, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage sm1-r70-7-elixir-r1-supplied-a1 openai (responses): input 0.48M, cached 98.4k, output 10.5k, reasoning 200, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage sm1-r70-7-go-r0-shape-luna-a1 openai (responses): input 0.41M, cached 0.18M, output 7.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
attempt usage sm1-r70-7-go-r0-supplied-a1 openai (responses): input 80.1k, cached 7.0k, output 2.9k, reasoning 71, input_tokens_details.cache_write_tokens 0, total_tokens 83.0k
attempt usage sm1-r70-7-go-r1-shape-luna-a1 openai (responses): input 32.3k, cached 0, output 3.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 35.7k
attempt outcomes included: supplied: correct 4, incorrect 0, workflow failure 1, infrastructure 0, incomplete 1; shape-luna: correct 0, incorrect 0, workflow failure 8, infrastructure 0, incomplete 0; shape-sol: correct 0, incorrect 0, workflow failure 5, infrastructure 0, incomplete 3
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 12077.1s, model 11632.5s, tools/checks 444.7s, requests 506
builder settings: supplied openai gpt-6-luna reasoning.effort=low
builder settings: shape-luna openai gpt-6-luna reasoning.effort=low
builder settings: shape-sol openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 22, scored 18, incorrect 0, infrastructure 0, incomplete 4
variant shape-luna differs from supplied in:
  shape.source: supplied -> generate
variant shape-sol differs from supplied in:
  roles.shaper: openai gpt-6-luna low -> openai gpt-6.1-sol low
  shape.source: supplied -> generate
MODE: exercised in 3 of 8 shape-luna attempts
MODE: exercised in 7 of 8 shape-sol attempts
roles.shaper.model: exercised in 8 of 8 shape-sol attempts
first position per task: r70-5-elixir supplied 0, shape-luna 1, shape-sol 1 (2 repetitions, 3 variants)
first position per task: r70-5-go supplied 0, shape-luna 1, shape-sol 1 (2 repetitions, 3 variants)
first position per task: r70-7-elixir supplied 1, shape-luna 0, shape-sol 1 (2 repetitions, 3 variants)
first position per task: r70-7-go supplied 1, shape-luna 1, shape-sol 0 (2 repetitions, 3 variants)
supplied: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
shape-luna: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
shape-sol: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
supplied: repair.context = packet,diff,check_results,review_findings (extension)
supplied: repair.roles = builder (extension)
supplied: shape.critique_prompt = lab:critique (extension)
supplied: shape.critique_rounds = 1 (extension)
shape-luna: repair.context = packet,diff,check_results,review_findings (extension)
shape-luna: repair.roles = builder (extension)
shape-luna: shape.critique_prompt = lab:critique (extension)
shape-luna: shape.critique_rounds = 1 (extension)
shape-sol: repair.context = packet,diff,check_results,review_findings (extension)
shape-sol: repair.roles = builder (extension)
shape-sol: shape.critique_prompt = lab:critique (extension)
shape-sol: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
