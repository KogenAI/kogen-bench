incomplete: 1 of 24 cells scored
Question: review-independence-1: does a reviewer that sees the builder's conversation approve earlier and let more wrong code through?
Hypothesis: exploratory: shared review approves earlier; wrong submissions may rise
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (1 of 24 cells scored)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| fresh   | 1       | 0         | 0                | 0              | 5          | 100%         | 0 of 1        | 0           |
| shared  | 0       | 0         | 0                | 2              | 1          | unavailable  | 0 of 0        | 0           |
false success: 0 of 1 claims (fresh)
false success: 0 of 0 claims (shared)
shaping outcomes:
fresh: shaping ready 6, shaping failed 0; correct 1 of 1
shared: shaping ready 3, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-go       | fresh   | 1       | 0         | 0                | 0              | 2          |
| env-go       | shared  | 0       | 0         | 0                | 1              | 1          |
| r70-5-elixir | fresh   | 0       | 0         | 0                | 0              | 0          |
| r70-5-elixir | shared  | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | fresh   | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | shared  | 0       | 0         | 0                | 0              | 0          |
| sched-go     | fresh   | 0       | 0         | 0                | 0              | 3          |
| sched-go     | shared  | 0       | 0         | 0                | 1              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model  | tools/checks | requests |
|---------|------------|---------|--------|--------------|----------|
| fresh   | shape      | 0ms     | 0ms    | 0ms          | 0        |
| fresh   | plan       | 55.3s   | 55.3s  | 0ms          | 5        |
| fresh   | build      | 1039.6s | 994s   | 45.5s        | 75       |
| fresh   | verify     | 4.5s    | 0ms    | 4.5s         | 0        |
| fresh   | review     | 85.1s   | 85.1s  | 0ms          | 9        |
| fresh   | commit     | 0ms     | 0ms    | 0ms          | 0        |
| fresh   | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| fresh   | assessment | 0ms     | 0ms    | 0ms          | 0        |
| shared  | shape      | 0ms     | 0ms    | 0ms          | 0        |
| shared  | plan       | 23.5s   | 23.5s  | 0ms          | 3        |
| shared  | build      | 346.5s  | 343.5s | 3s           | 19       |
| shared  | verify     | 1s      | 0ms    | 1s           | 0        |
| shared  | review     | 3.8s    | 3.8s   | 0ms          | 2        |
| shared  | commit     | 0ms     | 0ms    | 0ms          | 0        |
| shared  | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| shared  | assessment | 0ms     | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                   | outcome        | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------|----------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ri1-env-go-r0-fresh-a1    | incomplete     | 289.2s | 268.8s | 20.5s        | 21       | 3       | 3       | 0         | 0                    |
| ri1-env-go-r1-fresh-a1    | incomplete     | 134.6s | 124.7s | 10s          | 12       | 1       | 1       | 0         | 0                    |
| ri1-env-go-r1-shared-a1   | infrastructure | 139s   | 131.5s | 7.5s         | 9        | 0       | 0       | 0         | 0                    |
| ri1-env-go-r2-fresh-a1    | correct        | 244.1s | 228.3s | 15.8s        | 16       | 1       | 2       | 0         | 0                    |
| ri1-env-go-r2-shared-a1   | incomplete     | 19.1s  | 15.5s  | 3.6s         | 2        | 0       | 0       | 0         | 0                    |
| ri1-sched-go-r0-fresh-a1  | incomplete     | 256.9s | 243.6s | 13.3s        | 21       | 2       | 1       | 0         | 0                    |
| ri1-sched-go-r1-fresh-a1  | incomplete     | 5.6s   | 0ms    | 5.6s         | 0        | 0       | 0       | 0         | 0                    |
| ri1-sched-go-r1-shared-a1 | infrastructure | 234.5s | 223.8s | 10.7s        | 13       | 0       | 0       | 0         | 0                    |
| ri1-sched-go-r2-fresh-a1  | incomplete     | 291.6s | 269.1s | 22.5s        | 19       | 1       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
fresh openai: input 0.92M, cached 0.20M, output 29.8k, reasoning 464, input_tokens_details.cache_write_tokens 0, total_tokens 0.95M
shared openai: input 0.16M, cached 29.1k, output 8.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
native usage by stage and provider:
stage build fresh openai (responses): input 0.75M, cached 0.20M, output 27.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
stage build shared openai (responses): input 0.14M, cached 29.1k, output 7.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
stage plan fresh openai (responses): input 21.8k, cached 4.2k, output 1.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 22.8k
stage plan shared openai (responses): input 13.1k, cached 0, output 599, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 13.7k
stage review fresh openai (responses): input 0.15M, cached 0, output 1.7k, reasoning 464, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
native usage by attempt and provider:
attempt usage ri1-env-go-r0-fresh-a1 openai (responses): input 0.24M, cached 55.9k, output 6.6k, reasoning 337, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage ri1-env-go-r1-fresh-a1 openai (responses): input 93.2k, cached 11.6k, output 2.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 96.2k
attempt usage ri1-env-go-r1-shared-a1 openai (responses): input 60.7k, cached 29.1k, output 3.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 64.3k
attempt usage ri1-env-go-r2-fresh-a1 openai (responses): input 0.17M, cached 26.0k, output 5.6k, reasoning 127, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage ri1-env-go-r2-shared-a1 openai (responses): input 9.6k, cached 0, output 356, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 9.9k
attempt usage ri1-sched-go-r0-fresh-a1 openai (responses): input 0.22M, cached 63.6k, output 7.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage ri1-sched-go-r1-shared-a1 openai (responses): input 86.8k, cached 0, output 4.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 91.2k
attempt usage ri1-sched-go-r2-fresh-a1 openai (responses): input 0.20M, cached 43.4k, output 7.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt outcomes included: fresh: correct 1, incorrect 0, workflow failure 0, infrastructure 0, incomplete 5; shared: correct 0, incorrect 0, workflow failure 0, infrastructure 2, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 1614.7s, model 1505.2s, tools/checks 109.5s, requests 113
builder settings: fresh openai gpt-6-luna reasoning.effort=low
builder settings: shared openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 9, scored 1, incorrect 0, infrastructure 2, incomplete 6
variant shared differs from fresh in:
  review.independence: fresh -> shared
C04: exercised in 3 of 3 shared attempts
first position per task: env-go fresh 2, shared 1 (3 repetitions, 2 variants)
first position per task: r70-5-elixir fresh 1, shared 2 (3 repetitions, 2 variants)
first position per task: r70-5-go fresh 1, shared 2 (3 repetitions, 2 variants)
first position per task: sched-go fresh 2, shared 1 (3 repetitions, 2 variants)
fresh: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
shared: not the Kogen profile (differs in review.independence, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
fresh: repair.context = packet,diff,check_results,review_findings (extension)
fresh: repair.roles = builder (extension)
fresh: shape.critique_prompt = lab:critique (extension)
fresh: shape.critique_rounds = 1 (extension)
shared: repair.context = packet,diff,check_results,review_findings (extension)
shared: repair.roles = builder (extension)
shared: review.independence = shared (extension)
shared: shape.critique_prompt = lab:critique (extension)
shared: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
