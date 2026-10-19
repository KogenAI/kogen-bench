complete: 24/24 cells scored
Question: review-bound-1: would stopping review after N rounds (N = 1, 2, 3) submit code that fails hidden tests?
Hypothesis: exploratory: the snapshot a bound would submit is graded afterwards without model calls
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| low     | 9       | 0         | 3                | 0              | 0          | 75%          | 0 of 9        | 0           |
| medium  | 12      | 0         | 0                | 0              | 0          | 100%         | 0 of 12       | 0           |
false success: 0 of 9 claims (low)
false success: 0 of 12 claims (medium)
shaping outcomes:
low: shaping ready 12, shaping failed 0; correct 9 of 12
medium: shaping ready 12, shaping failed 0; correct 12 of 12
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-go       | low     | 3       | 0         | 0                | 0              | 0          |
| env-go       | medium  | 3       | 0         | 0                | 0              | 0          |
| r70-5-elixir | low     | 0       | 0         | 3                | 0              | 0          |
| r70-5-elixir | medium  | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | low     | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | medium  | 3       | 0         | 0                | 0              | 0          |
| sched-go     | low     | 3       | 0         | 0                | 0              | 0          |
| sched-go     | medium  | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| low     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| low     | plan       | 158.4s  | 158.4s  | 0ms          | 12       |
| low     | build      | 3651.9s | 3505.4s | 146.5s       | 247      |
| low     | verify     | 56.5s   | 0ms     | 56.5s        | 0        |
| low     | review     | 470.6s  | 470.6s  | 0ms          | 56       |
| low     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| low     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| low     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| medium  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| medium  | plan       | 151.4s  | 151.4s  | 0ms          | 12       |
| medium  | build      | 7905s   | 7735.7s | 169.4s       | 275      |
| medium  | verify     | 47.8s   | 0ms     | 47.8s        | 0        |
| medium  | review     | 1671.2s | 1671.2s | 0ms          | 76       |
| medium  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| medium  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| medium  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                       | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rb2-env-go-r0-low-a1          | correct          | 238.4s  | 219.7s  | 18.7s        | 25       | 2       | 3       | 0         | 0                    |
| rb2-env-go-r0-medium-a1       | correct          | 256.4s  | 241.9s  | 14.5s        | 21       | 1       | 2       | 0         | 0                    |
| rb2-env-go-r1-low-a1          | correct          | 231.5s  | 215.5s  | 16s          | 21       | 2       | 3       | 0         | 0                    |
| rb2-env-go-r1-medium-a1       | correct          | 393s    | 368.3s  | 24.8s        | 35       | 3       | 4       | 0         | 0                    |
| rb2-env-go-r2-low-a1          | correct          | 298.4s  | 279.7s  | 18.7s        | 23       | 2       | 3       | 0         | 0                    |
| rb2-env-go-r2-medium-a1       | correct          | 286.3s  | 272.4s  | 13.9s        | 23       | 1       | 2       | 0         | 0                    |
| rb2-r70-5-elixir-r0-low-a1    | workflow failure | 474.1s  | 422s    | 52s          | 38       | 6       | 0       | 0         | 0                    |
| rb2-r70-5-elixir-r0-medium-a1 | correct          | 2311.2s | 2266.4s | 44.8s        | 37       | 4       | 2       | 0         | 0                    |
| rb2-r70-5-elixir-r1-low-a1    | workflow failure | 447.4s  | 394.9s  | 52.5s        | 35       | 6       | 3       | 0         | 0                    |
| rb2-r70-5-elixir-r1-medium-a1 | correct          | 417.9s  | 391.5s  | 26.4s        | 51       | 5       | 3       | 0         | 0                    |
| rb2-r70-5-elixir-r2-low-a1    | workflow failure | 324.6s  | 296.9s  | 27.7s        | 35       | 6       | 0       | 0         | 0                    |
| rb2-r70-5-elixir-r2-medium-a1 | correct          | 2768.2s | 2708.3s | 59.9s        | 59       | 5       | 4       | 0         | 0                    |
| rb2-r70-5-go-r0-low-a1        | correct          | 973s    | 959.7s  | 13.3s        | 17       | 1       | 2       | 0         | 0                    |
| rb2-r70-5-go-r0-medium-a1     | correct          | 260.6s  | 245.7s  | 14.9s        | 20       | 1       | 2       | 0         | 0                    |
| rb2-r70-5-go-r1-low-a1        | correct          | 277.6s  | 268.6s  | 9s           | 25       | 2       | 3       | 0         | 0                    |
| rb2-r70-5-go-r1-medium-a1     | correct          | 2137.9s | 2130s   | 8s           | 19       | 1       | 2       | 0         | 0                    |
| rb2-r70-5-go-r2-low-a1        | correct          | 285.4s  | 268.2s  | 17.1s        | 30       | 3       | 3       | 0         | 0                    |
| rb2-r70-5-go-r2-medium-a1     | correct          | 225.3s  | 211.3s  | 14s          | 20       | 1       | 2       | 0         | 0                    |
| rb2-sched-go-r0-low-a1        | correct          | 296.2s  | 272.3s  | 23.9s        | 23       | 1       | 2       | 0         | 0                    |
| rb2-sched-go-r0-medium-a1     | correct          | 245.8s  | 234.6s  | 11.2s        | 26       | 3       | 3       | 0         | 0                    |
| rb2-sched-go-r1-low-a1        | correct          | 183.1s  | 173.6s  | 9.5s         | 12       | 0       | 1       | 0         | 0                    |
| rb2-sched-go-r1-medium-a1     | correct          | 304.3s  | 282.4s  | 21.9s        | 28       | 2       | 3       | 0         | 0                    |
| rb2-sched-go-r2-low-a1        | correct          | 378.1s  | 363.4s  | 14.7s        | 31       | 3       | 4       | 0         | 0                    |
| rb2-sched-go-r2-medium-a1     | correct          | 233.9s  | 205.3s  | 28.6s        | 24       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
low openai: input 4.35M, cached 1.10M, output 86.6k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 4.43M
medium openai: input 4.92M, cached 1.24M, output 88.9k, reasoning 4.9k, input_tokens_details.cache_write_tokens 0, total_tokens 5.00M
native usage by stage and provider:
stage build low openai (responses): input 3.39M, cached 1.10M, output 76.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.47M
stage build medium openai (responses): input 3.65M, cached 1.21M, output 75.6k, reasoning 827, input_tokens_details.cache_write_tokens 0, total_tokens 3.73M
stage plan low openai (responses): input 51.7k, cached 0, output 2.6k, reasoning 114, input_tokens_details.cache_write_tokens 0, total_tokens 54.3k
stage plan medium openai (responses): input 51.7k, cached 0, output 4.5k, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 56.2k
stage review low openai (responses): input 0.91M, cached 0, output 7.1k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.91M
stage review medium openai (responses): input 1.21M, cached 31.9k, output 8.8k, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.22M
native usage by attempt and provider:
attempt usage rb2-env-go-r0-low-a1 openai (responses): input 0.29M, cached 66.4k, output 4.9k, reasoning 180, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage rb2-env-go-r0-medium-a1 openai (responses): input 0.24M, cached 11.5k, output 7.1k, reasoning 437, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rb2-env-go-r1-low-a1 openai (responses): input 0.24M, cached 44.3k, output 5.5k, reasoning 130, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage rb2-env-go-r1-medium-a1 openai (responses): input 0.46M, cached 0.12M, output 7.9k, reasoning 500, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage rb2-env-go-r2-low-a1 openai (responses): input 0.28M, cached 33.9k, output 7.5k, reasoning 372, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rb2-env-go-r2-medium-a1 openai (responses): input 0.27M, cached 62.3k, output 5.5k, reasoning 264, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rb2-r70-5-elixir-r0-low-a1 openai (responses): input 0.67M, cached 0.23M, output 9.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.68M
attempt usage rb2-r70-5-elixir-r0-medium-a1 openai (responses): input 0.50M, cached 0.18M, output 7.1k, reasoning 193, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage rb2-r70-5-elixir-r1-low-a1 openai (responses): input 0.88M, cached 0.30M, output 12.4k, reasoning 31, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
attempt usage rb2-r70-5-elixir-r1-medium-a1 openai (responses): input 0.81M, cached 0.30M, output 12.9k, reasoning 484, input_tokens_details.cache_write_tokens 0, total_tokens 0.82M
attempt usage rb2-r70-5-elixir-r2-low-a1 openai (responses): input 0.46M, cached 0.20M, output 10.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage rb2-r70-5-elixir-r2-medium-a1 openai (responses): input 1.13M, cached 0.35M, output 10.6k, reasoning 588, input_tokens_details.cache_write_tokens 0, total_tokens 1.14M
attempt usage rb2-r70-5-go-r0-low-a1 openai (responses): input 0.18M, cached 44.2k, output 6.2k, reasoning 121, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rb2-r70-5-go-r0-medium-a1 openai (responses): input 0.22M, cached 10.4k, output 7.3k, reasoning 523, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rb2-r70-5-go-r1-low-a1 openai (responses): input 0.27M, cached 36.9k, output 5.9k, reasoning 158, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage rb2-r70-5-go-r1-medium-a1 openai (responses): input 0.19M, cached 20.2k, output 4.7k, reasoning 376, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rb2-r70-5-go-r2-low-a1 openai (responses): input 0.34M, cached 69.9k, output 6.1k, reasoning 111, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage rb2-r70-5-go-r2-medium-a1 openai (responses): input 0.21M, cached 33.4k, output 5.6k, reasoning 420, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rb2-sched-go-r0-low-a1 openai (responses): input 0.26M, cached 33.5k, output 7.2k, reasoning 154, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rb2-sched-go-r0-medium-a1 openai (responses): input 0.30M, cached 60.5k, output 7.0k, reasoning 423, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage rb2-sched-go-r1-low-a1 openai (responses): input 0.11M, cached 4.7k, output 2.9k, reasoning 38, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rb2-sched-go-r1-medium-a1 openai (responses): input 0.31M, cached 34.2k, output 6.1k, reasoning 404, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage rb2-sched-go-r2-low-a1 openai (responses): input 0.37M, cached 43.4k, output 7.6k, reasoning 258, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage rb2-sched-go-r2-medium-a1 openai (responses): input 0.27M, cached 54.3k, output 7.1k, reasoning 328, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt outcomes included: low: correct 9, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0; medium: correct 12, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 14248.6s, model 13692.7s, tools/checks 555.9s, requests 678
builder settings: low openai gpt-6-luna reasoning.effort=low
builder settings: medium openai gpt-6-luna reasoning.effort=medium (not equivalent)
## CMP-3 Counts and exposure
planned 24, started 24, scored 24, incorrect 0, infrastructure 0, incomplete 0
variant medium differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna medium
  roles.planner: openai gpt-6-luna low -> openai gpt-6-luna medium
roles.builder.effort: exercised in 12 of 12 medium attempts
roles.planner.effort: exercised in 12 of 12 medium attempts
first position per task: env-go low 2, medium 1 (3 repetitions, 2 variants)
first position per task: r70-5-elixir low 1, medium 2 (3 repetitions, 2 variants)
first position per task: r70-5-go low 1, medium 2 (3 repetitions, 2 variants)
first position per task: sched-go low 2, medium 1 (3 repetitions, 2 variants)
low: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
medium: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
low: repair.context = packet,diff,check_results,review_findings (extension)
low: repair.roles = builder (extension)
low: shape.critique_prompt = lab:critique (extension)
low: shape.critique_rounds = 1 (extension)
medium: repair.context = packet,diff,check_results,review_findings (extension)
medium: repair.roles = builder (extension)
medium: shape.critique_prompt = lab:critique (extension)
medium: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
