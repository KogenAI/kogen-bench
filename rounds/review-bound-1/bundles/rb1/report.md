complete: 8/8 cells scored
Question: review-bound-1: would stopping review after N rounds (N = 1, 2, 3) submit code that fails hidden tests?
Hypothesis: exploratory: the snapshot a bound would submit is graded afterwards without model calls
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| low     | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| medium  | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (low)
false success: 0 of 4 claims (medium)
shaping outcomes:
low: shaping ready 4, shaping failed 0; correct 4 of 4
medium: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-go       | low     | 1       | 0         | 0                | 0              | 0          |
| env-go       | medium  | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | low     | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | medium  | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | low     | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | medium  | 1       | 0         | 0                | 0              | 0          |
| sched-go     | low     | 1       | 0         | 0                | 0              | 0          |
| sched-go     | medium  | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| low     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| low     | plan       | 53.6s   | 53.6s   | 0ms          | 4        |
| low     | build      | 2144.6s | 2038.5s | 106.1s       | 114      |
| low     | verify     | 15.5s   | 0ms     | 15.5s        | 0        |
| low     | review     | 323.7s  | 323.7s  | 0ms          | 20       |
| low     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| low     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| low     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| medium  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| medium  | plan       | 56.6s   | 56.6s   | 0ms          | 4        |
| medium  | build      | 1387.4s | 1338.1s | 49.3s        | 69       |
| medium  | verify     | 10.1s   | 0ms     | 10.1s        | 0        |
| medium  | review     | 294.3s  | 294.3s  | 0ms          | 23       |
| medium  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| medium  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| medium  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                       | outcome | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------|---------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rb1-env-go-r0-low-a1          | correct | 1107.6s | 1077.6s | 30.1s        | 55       | 6       | 4       | 0         | 0                    |
| rb1-env-go-r0-medium-a1       | correct | 380.3s  | 360.5s  | 19.8s        | 22       | 2       | 3       | 0         | 0                    |
| rb1-r70-5-elixir-r0-low-a1    | correct | 664.5s  | 572.5s  | 92s          | 50       | 4       | 3       | 0         | 0                    |
| rb1-r70-5-elixir-r0-medium-a1 | correct | 259.6s  | 239.7s  | 19.9s        | 30       | 2       | 2       | 0         | 0                    |
| rb1-r70-5-go-r0-low-a1        | correct | 445.3s  | 435.3s  | 10s          | 19       | 1       | 2       | 0         | 0                    |
| rb1-r70-5-go-r0-medium-a1     | correct | 580.6s  | 555.5s  | 25.1s        | 23       | 1       | 2       | 0         | 0                    |
| rb1-sched-go-r0-low-a1        | correct | 347.5s  | 330.4s  | 17.1s        | 14       | 0       | 1       | 0         | 0                    |
| rb1-sched-go-r0-medium-a1     | correct | 555.8s  | 533.4s  | 22.4s        | 21       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
low openai: input 2.37M, cached 0.98M, output 38.5k, reasoning 752, input_tokens_details.cache_write_tokens 0, total_tokens 2.41M
medium openai: input 1.17M, cached 0.20M, output 29.1k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
native usage by stage and provider:
stage build low openai (responses): input 2.04M, cached 0.98M, output 34.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.07M
stage build medium openai (responses): input 0.79M, cached 0.20M, output 25.3k, reasoning 348, input_tokens_details.cache_write_tokens 0, total_tokens 0.82M
stage plan low openai (responses): input 17.2k, cached 0, output 842, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.1k
stage plan medium openai (responses): input 17.2k, cached 0, output 1.3k, reasoning 557, input_tokens_details.cache_write_tokens 0, total_tokens 18.5k
stage review low openai (responses): input 0.32M, cached 0, output 3.0k, reasoning 752, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
stage review medium openai (responses): input 0.36M, cached 0, output 2.5k, reasoning 522, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
native usage by attempt and provider:
attempt usage rb1-env-go-r0-low-a1 openai (responses): input 1.01M, cached 0.45M, output 15.4k, reasoning 303, input_tokens_details.cache_write_tokens 0, total_tokens 1.02M
attempt usage rb1-env-go-r0-medium-a1 openai (responses): input 0.28M, cached 32.3k, output 7.3k, reasoning 420, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rb1-r70-5-elixir-r0-low-a1 openai (responses): input 1.05M, cached 0.48M, output 14.2k, reasoning 300, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
attempt usage rb1-r70-5-elixir-r0-medium-a1 openai (responses): input 0.40M, cached 91.3k, output 7.3k, reasoning 267, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage rb1-r70-5-go-r0-low-a1 openai (responses): input 0.18M, cached 27.1k, output 3.5k, reasoning 53, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage rb1-r70-5-go-r0-medium-a1 openai (responses): input 0.26M, cached 48.5k, output 7.3k, reasoning 415, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rb1-sched-go-r0-low-a1 openai (responses): input 0.13M, cached 31.9k, output 5.5k, reasoning 96, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rb1-sched-go-r0-medium-a1 openai (responses): input 0.23M, cached 27.4k, output 7.2k, reasoning 325, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt outcomes included: low: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; medium: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 4341.2s, model 4104.8s, tools/checks 236.4s, requests 234
builder settings: low openai gpt-6-luna reasoning.effort=low
builder settings: medium openai gpt-6-luna reasoning.effort=medium (not equivalent)
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant medium differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna medium
  roles.planner: openai gpt-6-luna low -> openai gpt-6-luna medium
roles.builder.effort: exercised in 4 of 4 medium attempts
roles.planner.effort: exercised in 4 of 4 medium attempts
first position per task: env-go low 1, medium 0 (1 repetitions, 2 variants)
first position per task: r70-5-elixir low 1, medium 0 (1 repetitions, 2 variants)
first position per task: r70-5-go low 1, medium 0 (1 repetitions, 2 variants)
first position per task: sched-go low 0, medium 1 (1 repetitions, 2 variants)
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
