complete: 24/24 cells scored
Question: retention-1: does trimming old tool results from the builder conversation cut input without losing correctness?
Hypothesis: exploratory: trim6 uses at most 80% of full input at equal correctness
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| full    | 10      | 0         | 2                | 1              | 0          | 83.3%        | 0 of 10       | 0           |
| trim6   | 10      | 0         | 2                | 0              | 0          | 83.3%        | 0 of 10       | 0           |
false success: 0 of 10 claims (full)
false success: 0 of 10 claims (trim6)
shaping outcomes:
full: shaping ready 13, shaping failed 0; correct 10 of 12
trim6: shaping ready 12, shaping failed 0; correct 10 of 12
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-go       | full    | 3       | 0         | 0                | 0              | 0          |
| env-go       | trim6   | 1       | 0         | 2                | 0              | 0          |
| r70-5-elixir | full    | 1       | 0         | 2                | 1              | 0          |
| r70-5-elixir | trim6   | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | full    | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | trim6   | 3       | 0         | 0                | 0              | 0          |
| sched-go     | full    | 3       | 0         | 0                | 0              | 0          |
| sched-go     | trim6   | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| full    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| full    | plan       | 127.4s  | 127.4s  | 0ms          | 13       |
| full    | build      | 4870.1s | 4666.6s | 203.5s       | 305      |
| full    | verify     | 46.9s   | 0ms     | 46.9s        | 0        |
| full    | review     | 610.6s  | 610.6s  | 0ms          | 75       |
| full    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| full    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| full    | assessment | 0ms     | 0ms     | 0ms          | 0        |
| trim6   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| trim6   | plan       | 140.3s  | 140.3s  | 0ms          | 12       |
| trim6   | build      | 4403.6s | 4231.8s | 171.8s       | 349      |
| trim6   | verify     | 42.9s   | 0ms     | 42.9s        | 0        |
| trim6   | review     | 534.7s  | 534.7s  | 0ms          | 64       |
| trim6   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| trim6   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| trim6   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                      | outcome          | wall   | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------|------------------|--------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rt2-env-go-r0-full-a1        | correct          | 312.8s | 298.1s  | 14.7s        | 24       | 2       | 3       | 0         | 0                    |
| rt2-env-go-r0-trim6-a1       | workflow failure | 885.4s | 844.9s  | 40.5s        | 71       | 6       | 0       | 0         | 0                    |
| rt2-env-go-r1-full-a1        | correct          | 303.2s | 286.3s  | 16.9s        | 26       | 1       | 2       | 0         | 0                    |
| rt2-env-go-r1-trim6-a1       | workflow failure | 154.5s | 147.1s  | 7.4s         | 8        | 0       | 0       | 0         | 0                    |
| rt2-env-go-r2-full-a1        | correct          | 307.9s | 291.9s  | 16s          | 27       | 2       | 3       | 0         | 0                    |
| rt2-env-go-r2-trim6-a1       | correct          | 634.8s | 616.9s  | 17.9s        | 53       | 6       | 6       | 0         | 0                    |
| rt2-r70-5-elixir-r0-full-a1  | correct          | 418.6s | 355.3s  | 63.3s        | 42       | 4       | 3       | 0         | 0                    |
| rt2-r70-5-elixir-r0-trim6-a1 | correct          | 659.4s | 610.4s  | 49s          | 55       | 5       | 3       | 0         | 0                    |
| rt2-r70-5-elixir-r1-full-a1  | workflow failure | 498s   | 467.3s  | 30.6s        | 37       | 6       | 3       | 0         | 0                    |
| rt2-r70-5-elixir-r1-trim6-a1 | correct          | 387.2s | 372.9s  | 14.3s        | 38       | 3       | 4       | 0         | 0                    |
| rt2-r70-5-elixir-r2-full-a1  | infrastructure   | 1092s  | 1083.3s | 8.7s         | 17       | 2       | 1       | 0         | 0                    |
| rt2-r70-5-elixir-r2-full-a2  | workflow failure | 729.2s | 689.4s  | 39.8s        | 70       | 6       | 2       | 0         | 0                    |
| rt2-r70-5-elixir-r2-trim6-a1 | correct          | 627.1s | 590.3s  | 36.8s        | 59       | 3       | 3       | 0         | 0                    |
| rt2-r70-5-go-r0-full-a1      | correct          | 403.9s | 385.3s  | 18.5s        | 32       | 3       | 4       | 0         | 0                    |
| rt2-r70-5-go-r0-trim6-a1     | correct          | 394.6s | 376.3s  | 18.3s        | 32       | 2       | 3       | 0         | 0                    |
| rt2-r70-5-go-r1-full-a1      | correct          | 418.6s | 391.6s  | 26.9s        | 31       | 3       | 3       | 0         | 0                    |
| rt2-r70-5-go-r1-trim6-a1     | correct          | 241.7s | 231.8s  | 10s          | 21       | 1       | 2       | 0         | 0                    |
| rt2-r70-5-go-r2-full-a1      | correct          | 226.9s | 208.4s  | 18.5s        | 15       | 1       | 2       | 0         | 0                    |
| rt2-r70-5-go-r2-trim6-a1     | correct          | 308.3s | 291.4s  | 16.9s        | 22       | 2       | 3       | 0         | 0                    |
| rt2-sched-go-r0-full-a1      | correct          | 485s   | 460s    | 25.1s        | 32       | 1       | 2       | 0         | 0                    |
| rt2-sched-go-r0-trim6-a1     | correct          | 271.9s | 253.5s  | 18.5s        | 19       | 1       | 2       | 0         | 0                    |
| rt2-sched-go-r1-full-a1      | correct          | 278.3s | 260s    | 18.3s        | 17       | 1       | 2       | 0         | 0                    |
| rt2-sched-go-r1-trim6-a1     | correct          | 327.5s | 301.7s  | 25.9s        | 21       | 1       | 2       | 0         | 0                    |
| rt2-sched-go-r2-full-a1      | correct          | 254.5s | 227.7s  | 26.8s        | 23       | 1       | 2       | 0         | 0                    |
| rt2-sched-go-r2-trim6-a1     | correct          | 297.6s | 269.6s  | 28s          | 26       | 2       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
full openai: input 6.22M, cached 1.99M, output 0.12M, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 6.34M
trim6 openai: input 5.89M, cached 0.68M, output 0.13M, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 6.01M
native usage by stage and provider:
stage build full openai (responses): input 4.97M, cached 1.98M, output 0.10M, reasoning 198, input_tokens_details.cache_write_tokens 0, total_tokens 5.08M
stage build trim6 openai (responses): input 4.81M, cached 0.67M, output 0.12M, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 4.93M
stage plan full openai (responses): input 56.0k, cached 8.2k, output 3.0k, reasoning 247, input_tokens_details.cache_write_tokens 0, total_tokens 59.0k
stage plan trim6 openai (responses): input 51.7k, cached 12.5k, output 2.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 54.2k
stage review full openai (responses): input 1.19M, cached 0, output 9.9k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
stage review trim6 openai (responses): input 1.02M, cached 0, output 9.0k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.03M
native usage by attempt and provider:
attempt usage rt2-env-go-r0-full-a1 openai (responses): input 0.28M, cached 47.5k, output 8.8k, reasoning 178, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rt2-env-go-r0-trim6-a1 openai (responses): input 1.21M, cached 0.19M, output 20.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.23M
attempt usage rt2-env-go-r1-full-a1 openai (responses): input 0.31M, cached 61.1k, output 6.9k, reasoning 83, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage rt2-env-go-r1-trim6-a1 openai (responses): input 55.3k, cached 9.2k, output 4.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 59.8k
attempt usage rt2-env-go-r2-full-a1 openai (responses): input 0.34M, cached 23.9k, output 6.3k, reasoning 213, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage rt2-env-go-r2-trim6-a1 openai (responses): input 0.73M, cached 74.1k, output 16.7k, reasoning 434, input_tokens_details.cache_write_tokens 0, total_tokens 0.75M
attempt usage rt2-r70-5-elixir-r0-full-a1 openai (responses): input 0.69M, cached 0.15M, output 11.6k, reasoning 215, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
attempt usage rt2-r70-5-elixir-r0-trim6-a1 openai (responses): input 0.88M, cached 97.3k, output 16.3k, reasoning 274, input_tokens_details.cache_write_tokens 0, total_tokens 0.90M
attempt usage rt2-r70-5-elixir-r1-full-a1 openai (responses): input 0.56M, cached 0.19M, output 13.2k, reasoning 198, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt usage rt2-r70-5-elixir-r1-trim6-a1 openai (responses): input 0.50M, cached 48.6k, output 13.0k, reasoning 622, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage rt2-r70-5-elixir-r2-full-a1 openai (responses): input 0.15M, cached 28.5k, output 6.0k, reasoning 69, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rt2-r70-5-elixir-r2-full-a2 openai (responses): input 2.15M, cached 1.25M, output 24.2k, reasoning 48, input_tokens_details.cache_write_tokens 0, total_tokens 2.17M
attempt usage rt2-r70-5-elixir-r2-trim6-a1 openai (responses): input 1.02M, cached 0.14M, output 19.7k, reasoning 217, input_tokens_details.cache_write_tokens 0, total_tokens 1.04M
attempt usage rt2-r70-5-go-r0-full-a1 openai (responses): input 0.41M, cached 76.3k, output 8.8k, reasoning 335, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage rt2-r70-5-go-r0-trim6-a1 openai (responses): input 0.38M, cached 29.2k, output 9.7k, reasoning 142, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
attempt usage rt2-r70-5-go-r1-full-a1 openai (responses): input 0.36M, cached 39.9k, output 8.3k, reasoning 158, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage rt2-r70-5-go-r1-trim6-a1 openai (responses): input 0.21M, cached 9.5k, output 5.2k, reasoning 97, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rt2-r70-5-go-r2-full-a1 openai (responses): input 0.15M, cached 14.8k, output 4.8k, reasoning 88, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rt2-r70-5-go-r2-trim6-a1 openai (responses): input 0.22M, cached 23.7k, output 5.9k, reasoning 209, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rt2-sched-go-r0-full-a1 openai (responses): input 0.40M, cached 90.8k, output 9.8k, reasoning 101, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage rt2-sched-go-r0-trim6-a1 openai (responses): input 0.21M, cached 4.7k, output 4.3k, reasoning 122, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rt2-sched-go-r1-full-a1 openai (responses): input 0.17M, cached 4.1k, output 3.6k, reasoning 331, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rt2-sched-go-r1-trim6-a1 openai (responses): input 0.22M, cached 18.9k, output 5.0k, reasoning 136, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rt2-sched-go-r2-full-a1 openai (responses): input 0.26M, cached 18.4k, output 5.3k, reasoning 126, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rt2-sched-go-r2-trim6-a1 openai (responses): input 0.25M, cached 28.4k, output 7.2k, reasoning 185, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt outcomes included: full: correct 10, incorrect 0, workflow failure 2, infrastructure 1, incomplete 0; trim6: correct 10, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 10918.8s, model 10311.4s, tools/checks 607.4s, requests 818
builder settings: full openai gpt-6-luna reasoning.effort=low
builder settings: trim6 openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 25, scored 24, incorrect 0, infrastructure 1, incomplete 0
variant trim6 differs from full in:
  build.retention: full -> trim_tool_results
  build.retention_keep: 20 -> 6
B06: exercised in 12 of 12 trim6 attempts
first position per task: env-go full 2, trim6 1 (3 repetitions, 2 variants)
first position per task: r70-5-elixir full 1, trim6 2 (3 repetitions, 2 variants)
first position per task: r70-5-go full 1, trim6 2 (3 repetitions, 2 variants)
first position per task: sched-go full 2, trim6 1 (3 repetitions, 2 variants)
full: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
trim6: not the Kogen profile (differs in build.retention, build.retention_keep, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
full: repair.context = packet,diff,check_results,review_findings (extension)
full: repair.roles = builder (extension)
full: shape.critique_prompt = lab:critique (extension)
full: shape.critique_rounds = 1 (extension)
trim6: build.retention = trim_tool_results (extension)
trim6: repair.context = packet,diff,check_results,review_findings (extension)
trim6: repair.roles = builder (extension)
trim6: shape.critique_prompt = lab:critique (extension)
trim6: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
