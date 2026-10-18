complete: 18/18 cells scored
Question: confirm-builder-effort-1: on fresh tasks, is gpt-6-luna medium at least as often correct as low with at most 85% of its input?
Hypothesis: medium is correct in at least as many paired blocks as low with at most 85% of its total input
Purpose: confirmation
Objective: cost_at_quality
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| low     | 6       | 0         | 3                | 0              | 0          | 66.7%        | 0 of 6        | 0           |
| medium  | 6       | 0         | 3                | 0              | 0          | 66.7%        | 0 of 6        | 0           |
false success: 0 of 6 claims (low)
false success: 0 of 6 claims (medium)
shaping outcomes:
low: shaping ready 9, shaping failed 0; correct 6 of 9
medium: shaping ready 9, shaping failed 0; correct 6 of 9
## Per-task outcomes
| task     | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------|---------|---------|-----------|------------------|----------------|------------|
| env-ex   | low     | 0       | 0         | 3                | 0              | 0          |
| env-ex   | medium  | 0       | 0         | 3                | 0              | 0          |
| env-go   | low     | 3       | 0         | 0                | 0              | 0          |
| env-go   | medium  | 3       | 0         | 0                | 0              | 0          |
| sched-go | low     | 3       | 0         | 0                | 0              | 0          |
| sched-go | medium  | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| low     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| low     | plan       | 94.1s   | 94.1s   | 0ms          | 9        |
| low     | build      | 3048.5s | 2899.2s | 149.3s       | 265      |
| low     | verify     | 55.4s   | 0ms     | 55.4s        | 0        |
| low     | review     | 416.8s  | 416.8s  | 0ms          | 46       |
| low     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| low     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| low     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| medium  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| medium  | plan       | 144.3s  | 144.3s  | 0ms          | 9        |
| medium  | build      | 2585s   | 2449.1s | 135.9s       | 215      |
| medium  | verify     | 57s     | 0ms     | 57s          | 0        |
| medium  | review     | 471.8s  | 471.8s  | 0ms          | 52       |
| medium  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| medium  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| medium  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                    | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cbe1-env-ex-r0-low-a1      | workflow failure | 367.5s | 339.8s | 27.7s        | 30       | 6       | 0       | 0         | 0                    |
| cbe1-env-ex-r0-medium-a1   | workflow failure | 523.4s | 486.5s | 36.9s        | 40       | 6       | 1       | 0         | 0                    |
| cbe1-env-ex-r1-low-a1      | workflow failure | 812.4s | 740.3s | 72.1s        | 55       | 6       | 2       | 0         | 0                    |
| cbe1-env-ex-r1-medium-a1   | workflow failure | 261.2s | 219s   | 42.3s        | 30       | 6       | 1       | 0         | 0                    |
| cbe1-env-ex-r2-low-a1      | workflow failure | 518.1s | 465.8s | 52.3s        | 45       | 6       | 1       | 0         | 0                    |
| cbe1-env-ex-r2-medium-a1   | workflow failure | 630.4s | 565.6s | 64.8s        | 47       | 6       | 5       | 0         | 0                    |
| cbe1-env-go-r0-low-a1      | correct          | 269.7s | 257.3s | 12.3s        | 27       | 2       | 3       | 0         | 0                    |
| cbe1-env-go-r0-medium-a1   | correct          | 249.7s | 236s   | 13.7s        | 17       | 1       | 2       | 0         | 0                    |
| cbe1-env-go-r1-low-a1      | correct          | 368s   | 347.9s | 20.1s        | 34       | 3       | 4       | 0         | 0                    |
| cbe1-env-go-r1-medium-a1   | correct          | 354.5s | 333.2s | 21.3s        | 30       | 2       | 3       | 0         | 0                    |
| cbe1-env-go-r2-low-a1      | correct          | 328.6s | 310.9s | 17.7s        | 30       | 2       | 3       | 0         | 0                    |
| cbe1-env-go-r2-medium-a1   | correct          | 365s   | 348.7s | 16.3s        | 29       | 2       | 3       | 0         | 0                    |
| cbe1-sched-go-r0-low-a1    | correct          | 263s   | 244.2s | 18.8s        | 26       | 2       | 3       | 0         | 0                    |
| cbe1-sched-go-r0-medium-a1 | correct          | 311.6s | 296.4s | 15.2s        | 28       | 3       | 2       | 0         | 0                    |
| cbe1-sched-go-r1-low-a1    | correct          | 341.2s | 323.1s | 18.1s        | 30       | 3       | 3       | 0         | 0                    |
| cbe1-sched-go-r1-medium-a1 | correct          | 289.8s | 279.1s | 10.7s        | 29       | 3       | 2       | 0         | 0                    |
| cbe1-sched-go-r2-low-a1    | correct          | 394.5s | 380.9s | 13.7s        | 43       | 3       | 4       | 0         | 0                    |
| cbe1-sched-go-r2-medium-a1 | correct          | 320.5s | 300.7s | 19.9s        | 26       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
low openai: input 5.48M, cached 2.01M, output 83.9k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 5.56M
medium openai: input 4.06M, cached 1.20M, output 81.2k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 4.14M
native usage by stage and provider:
stage build low openai (responses): input 4.66M, cached 1.99M, output 75.0k, reasoning 29, input_tokens_details.cache_write_tokens 0, total_tokens 4.74M
stage build medium openai (responses): input 3.17M, cached 1.19M, output 71.1k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 3.24M
stage plan low openai (responses): input 39.3k, cached 0, output 2.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 41.3k
stage plan medium openai (responses): input 39.3k, cached 4.2k, output 2.7k, reasoning 865, input_tokens_details.cache_write_tokens 0, total_tokens 42.0k
stage review low openai (responses): input 0.77M, cached 16.8k, output 6.9k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
stage review medium openai (responses): input 0.85M, cached 0, output 7.4k, reasoning 978, input_tokens_details.cache_write_tokens 0, total_tokens 0.86M
native usage by attempt and provider:
attempt usage cbe1-env-ex-r0-low-a1 openai (responses): input 0.50M, cached 0.19M, output 9.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage cbe1-env-ex-r0-medium-a1 openai (responses): input 0.87M, cached 0.39M, output 12.2k, reasoning 116, input_tokens_details.cache_write_tokens 0, total_tokens 0.88M
attempt usage cbe1-env-ex-r1-low-a1 openai (responses): input 1.59M, cached 0.83M, output 19.3k, reasoning 60, input_tokens_details.cache_write_tokens 0, total_tokens 1.61M
attempt usage cbe1-env-ex-r1-medium-a1 openai (responses): input 0.43M, cached 0.15M, output 6.9k, reasoning 239, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage cbe1-env-ex-r2-low-a1 openai (responses): input 0.97M, cached 0.43M, output 12.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.98M
attempt usage cbe1-env-ex-r2-medium-a1 openai (responses): input 0.82M, cached 0.29M, output 12.3k, reasoning 637, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
attempt usage cbe1-env-go-r0-low-a1 openai (responses): input 0.33M, cached 45.4k, output 5.4k, reasoning 166, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
attempt usage cbe1-env-go-r0-medium-a1 openai (responses): input 0.19M, cached 22.9k, output 6.8k, reasoning 592, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage cbe1-env-go-r1-low-a1 openai (responses): input 0.47M, cached 0.14M, output 6.8k, reasoning 250, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt usage cbe1-env-go-r1-medium-a1 openai (responses): input 0.38M, cached 0.14M, output 9.0k, reasoning 619, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
attempt usage cbe1-env-go-r2-low-a1 openai (responses): input 0.40M, cached 84.7k, output 8.2k, reasoning 222, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage cbe1-env-go-r2-medium-a1 openai (responses): input 0.35M, cached 33.5k, output 8.2k, reasoning 483, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage cbe1-sched-go-r0-low-a1 openai (responses): input 0.31M, cached 71.9k, output 7.0k, reasoning 231, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage cbe1-sched-go-r0-medium-a1 openai (responses): input 0.34M, cached 42.4k, output 8.0k, reasoning 328, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage cbe1-sched-go-r1-low-a1 openai (responses): input 0.34M, cached 89.5k, output 5.8k, reasoning 213, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage cbe1-sched-go-r1-medium-a1 openai (responses): input 0.35M, cached 68.5k, output 8.9k, reasoning 177, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage cbe1-sched-go-r2-low-a1 openai (responses): input 0.57M, cached 0.13M, output 9.4k, reasoning 294, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt usage cbe1-sched-go-r2-medium-a1 openai (responses): input 0.32M, cached 67.3k, output 8.9k, reasoning 630, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
attempt outcomes included: low: correct 6, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0; medium: correct 6, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 6969.3s, model 6475.3s, tools/checks 493.9s, requests 596
builder settings: low openai gpt-6-luna reasoning.effort=low
builder settings: medium openai gpt-6-luna reasoning.effort=medium (not equivalent)
## CMP-3 Counts and exposure
planned 18, started 18, scored 18, incorrect 0, infrastructure 0, incomplete 0
variant medium differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna medium
  roles.planner: openai gpt-6-luna low -> openai gpt-6-luna medium
roles.builder.effort: exercised in 9 of 9 medium attempts
roles.planner.effort: exercised in 9 of 9 medium attempts
first position per task: env-ex low 1, medium 2 (3 repetitions, 2 variants)
first position per task: env-go low 2, medium 1 (3 repetitions, 2 variants)
first position per task: sched-go low 1, medium 2 (3 repetitions, 2 variants)
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
