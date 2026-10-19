complete: 24/24 cells scored
Question: review-independence-1: does a reviewer that sees the builder's conversation approve earlier and let more wrong code through?
Hypothesis: exploratory: shared review approves earlier; wrong submissions may rise
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| fresh   | 11      | 0         | 1                | 0              | 2          | 91.7%        | 0 of 11       | 0           |
| shared  | 8       | 0         | 4                | 0              | 1          | 66.7%        | 0 of 8        | 0           |
false success: 0 of 11 claims (fresh)
false success: 0 of 8 claims (shared)
shaping outcomes:
fresh: shaping ready 14, shaping failed 0; correct 11 of 12
shared: shaping ready 13, shaping failed 0; correct 8 of 12
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-go       | fresh   | 3       | 0         | 0                | 0              | 0          |
| env-go       | shared  | 2       | 0         | 1                | 0              | 0          |
| r70-5-elixir | fresh   | 2       | 0         | 1                | 0              | 2          |
| r70-5-elixir | shared  | 1       | 0         | 2                | 0              | 1          |
| r70-5-go     | fresh   | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | shared  | 3       | 0         | 0                | 0              | 0          |
| sched-go     | fresh   | 3       | 0         | 0                | 0              | 0          |
| sched-go     | shared  | 2       | 0         | 1                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| fresh   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fresh   | plan       | 218.1s  | 218.1s  | 0ms          | 12       |
| fresh   | build      | 6768.8s | 6591.3s | 177.5s       | 270      |
| fresh   | verify     | 45.9s   | 0ms     | 45.9s        | 0        |
| fresh   | review     | 1219.5s | 1219.5s | 0ms          | 67       |
| fresh   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fresh   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fresh   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| shared  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| shared  | plan       | 237s    | 237s    | 0ms          | 12       |
| shared  | build      | 7025.1s | 6868.7s | 156.3s       | 289      |
| shared  | verify     | 53.9s   | 0ms     | 53.9s        | 0        |
| shared  | review     | 763.5s  | 763.5s  | 0ms          | 39       |
| shared  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| shared  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| shared  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                       | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| ri2-env-go-r0-fresh-a1        | correct          | 562.9s  | 541.5s  | 21.4s        | 22       | 2       | 3       | 0         | 0                    |
| ri2-env-go-r0-shared-a1       | correct          | 665.9s  | 643.9s  | 21.9s        | 27       | 3       | 3       | 0         | 0                    |
| ri2-env-go-r1-fresh-a1        | correct          | 1786.9s | 1763.3s | 23.6s        | 36       | 2       | 2       | 0         | 0                    |
| ri2-env-go-r1-shared-a1       | workflow failure | 755.2s  | 726.9s  | 28.3s        | 33       | 6       | 6       | 0         | 0                    |
| ri2-env-go-r2-fresh-a1        | correct          | 782.4s  | 755.5s  | 27s          | 32       | 2       | 3       | 0         | 0                    |
| ri2-env-go-r2-shared-a1       | correct          | 2712.4s | 2675.2s | 37.2s        | 74       | 6       | 6       | 0         | 0                    |
| ri2-r70-5-elixir-r0-fresh-a1  | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 0       | 0         | 0                    |
| ri2-r70-5-elixir-r0-fresh-a2  | workflow failure | 323.4s  | 274.6s  | 48.8s        | 40       | 6       | 0       | 0         | 0                    |
| ri2-r70-5-elixir-r0-shared-a1 | workflow failure | 943.5s  | 894.3s  | 49.2s        | 46       | 6       | 4       | 0         | 0                    |
| ri2-r70-5-elixir-r1-fresh-a1  | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 0       | 0         | 0                    |
| ri2-r70-5-elixir-r1-fresh-a2  | correct          | 506.3s  | 467.5s  | 38.9s        | 50       | 4       | 2       | 0         | 0                    |
| ri2-r70-5-elixir-r1-shared-a1 | workflow failure | 334.9s  | 300.3s  | 34.6s        | 39       | 6       | 1       | 0         | 0                    |
| ri2-r70-5-elixir-r2-fresh-a1  | correct          | 315.8s  | 287.7s  | 28.1s        | 31       | 2       | 3       | 0         | 0                    |
| ri2-r70-5-elixir-r2-shared-a1 | incomplete       | 0ms     | 0ms     | 0ms          | 0        | 0       | 2       | 0         | 0                    |
| ri2-r70-5-elixir-r2-shared-a2 | correct          | 249.5s  | 227.4s  | 22.1s        | 20       | 2       | 3       | 0         | 0                    |
| ri2-r70-5-go-r0-fresh-a1      | correct          | 684.9s  | 660.1s  | 24.8s        | 33       | 2       | 3       | 0         | 0                    |
| ri2-r70-5-go-r0-shared-a1     | correct          | 454.2s  | 429.2s  | 25s          | 21       | 2       | 3       | 0         | 0                    |
| ri2-r70-5-go-r1-fresh-a1      | correct          | 553.4s  | 538.8s  | 14.6s        | 27       | 3       | 4       | 0         | 0                    |
| ri2-r70-5-go-r1-shared-a1     | correct          | 656.5s  | 636.6s  | 19.9s        | 28       | 2       | 3       | 0         | 0                    |
| ri2-r70-5-go-r2-fresh-a1      | correct          | 442.1s  | 421.4s  | 20.7s        | 17       | 1       | 2       | 0         | 0                    |
| ri2-r70-5-go-r2-shared-a1     | correct          | 404.6s  | 387s    | 17.6s        | 18       | 2       | 3       | 0         | 0                    |
| ri2-sched-go-r0-fresh-a1      | correct          | 1370.2s | 1352.2s | 18s          | 18       | 1       | 2       | 0         | 0                    |
| ri2-sched-go-r0-shared-a1     | workflow failure | 247s    | 239.9s  | 7.1s         | 7        | 0       | 0       | 0         | 0                    |
| ri2-sched-go-r1-fresh-a1      | correct          | 490.8s  | 471.4s  | 19.5s        | 23       | 1       | 2       | 0         | 0                    |
| ri2-sched-go-r1-shared-a1     | correct          | 515.9s  | 498.4s  | 17.5s        | 17       | 1       | 2       | 0         | 0                    |
| ri2-sched-go-r2-fresh-a1      | correct          | 513.5s  | 494.9s  | 18.6s        | 20       | 1       | 2       | 0         | 0                    |
| ri2-sched-go-r2-shared-a1     | correct          | 218.2s  | 210.1s  | 8.1s         | 10       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
fresh openai: input 4.74M, cached 1.04M, output 86.2k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 4.83M
shared openai: input 6.23M, cached 2.21M, output 0.11M, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 6.34M
native usage by stage and provider:
stage build fresh openai (responses): input 3.62M, cached 1.04M, output 75.5k, reasoning 166, input_tokens_details.cache_write_tokens 0, total_tokens 3.69M
stage build shared openai (responses): input 4.92M, cached 2.20M, output 96.1k, reasoning 138, input_tokens_details.cache_write_tokens 0, total_tokens 5.01M
stage plan fresh openai (responses): input 51.7k, cached 0, output 2.9k, reasoning 258, input_tokens_details.cache_write_tokens 0, total_tokens 54.6k
stage plan shared openai (responses): input 51.7k, cached 4.1k, output 2.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 54.3k
stage review fresh openai (responses): input 1.07M, cached 0, output 7.8k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.08M
stage review shared openai (responses): input 1.26M, cached 0, output 9.9k, reasoning 938, input_tokens_details.cache_write_tokens 0, total_tokens 1.27M
native usage by attempt and provider:
attempt usage ri2-env-go-r0-fresh-a1 openai (responses): input 0.28M, cached 39.0k, output 8.2k, reasoning 141, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage ri2-env-go-r0-shared-a1 openai (responses): input 0.36M, cached 68.0k, output 6.0k, reasoning 99, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage ri2-env-go-r1-fresh-a1 openai (responses): input 0.53M, cached 0.14M, output 6.9k, reasoning 194, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
attempt usage ri2-env-go-r1-shared-a1 openai (responses): input 0.50M, cached 96.8k, output 10.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage ri2-env-go-r2-fresh-a1 openai (responses): input 0.40M, cached 0.11M, output 7.7k, reasoning 255, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage ri2-env-go-r2-shared-a1 openai (responses): input 2.08M, cached 1.13M, output 31.1k, reasoning 316, input_tokens_details.cache_write_tokens 0, total_tokens 2.11M
attempt usage ri2-r70-5-elixir-r0-fresh-a2 openai (responses): input 0.78M, cached 0.23M, output 6.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
attempt usage ri2-r70-5-elixir-r0-shared-a1 openai (responses): input 1.00M, cached 0.38M, output 12.9k, reasoning 58, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
attempt usage ri2-r70-5-elixir-r1-fresh-a2 openai (responses): input 0.84M, cached 0.29M, output 14.1k, reasoning 198, input_tokens_details.cache_write_tokens 0, total_tokens 0.85M
attempt usage ri2-r70-5-elixir-r1-shared-a1 openai (responses): input 0.78M, cached 0.32M, output 8.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.79M
attempt usage ri2-r70-5-elixir-r2-fresh-a1 openai (responses): input 0.37M, cached 78.8k, output 8.6k, reasoning 242, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage ri2-r70-5-elixir-r2-shared-a2 openai (responses): input 0.28M, cached 8.6k, output 7.6k, reasoning 209, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage ri2-r70-5-go-r0-fresh-a1 openai (responses): input 0.36M, cached 40.7k, output 6.4k, reasoning 173, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage ri2-r70-5-go-r0-shared-a1 openai (responses): input 0.29M, cached 39.3k, output 7.8k, reasoning 51, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage ri2-r70-5-go-r1-fresh-a1 openai (responses): input 0.30M, cached 29.8k, output 4.6k, reasoning 328, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage ri2-r70-5-go-r1-shared-a1 openai (responses): input 0.37M, cached 94.5k, output 8.3k, reasoning 117, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage ri2-r70-5-go-r2-fresh-a1 openai (responses): input 0.22M, cached 4.9k, output 6.4k, reasoning 187, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage ri2-r70-5-go-r2-shared-a1 openai (responses): input 0.23M, cached 13.4k, output 6.2k, reasoning 95, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage ri2-sched-go-r0-fresh-a1 openai (responses): input 0.19M, cached 25.5k, output 5.9k, reasoning 349, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage ri2-sched-go-r0-shared-a1 openai (responses): input 44.1k, cached 11.4k, output 2.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 46.6k
attempt usage ri2-sched-go-r1-fresh-a1 openai (responses): input 0.24M, cached 21.8k, output 4.6k, reasoning 80, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage ri2-sched-go-r1-shared-a1 openai (responses): input 0.21M, cached 30.8k, output 4.5k, reasoning 55, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage ri2-sched-go-r2-fresh-a1 openai (responses): input 0.22M, cached 19.6k, output 6.4k, reasoning 61, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage ri2-sched-go-r2-shared-a1 openai (responses): input 87.8k, cached 11.4k, output 3.3k, reasoning 76, input_tokens_details.cache_write_tokens 0, total_tokens 91.1k
attempt outcomes included: fresh: correct 11, incorrect 0, workflow failure 1, infrastructure 0, incomplete 2; shared: correct 8, incorrect 0, workflow failure 4, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 16490.6s, model 15898.2s, tools/checks 592.5s, requests 689
builder settings: fresh openai gpt-6-luna reasoning.effort=low
builder settings: shared openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 27, scored 24, incorrect 0, infrastructure 0, incomplete 3
variant shared differs from fresh in:
  review.independence: fresh -> shared
C04: exercised in 13 of 13 shared attempts
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
