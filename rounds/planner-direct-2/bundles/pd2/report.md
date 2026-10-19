complete: 8/8 cells scored
Question: planner-direct-2: with Kogen b2c9876b's default roles, does building directly without a planner change correctness, repairs or tokens?
Hypothesis: exploratory: the direct build matches the planned build at lower token cost
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| planned | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| direct  | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (planned)
false success: 0 of 4 claims (direct)
shaping outcomes:
planned: shaping ready 4, shaping failed 0; correct 4 of 4
direct: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| r70-1-go     | planned | 1       | 0         | 0                | 0              | 0          |
| r70-1-go     | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir | planned | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | planned | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | planned | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | direct  | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model  | tools/checks | requests |
|---------|------------|---------|--------|--------------|----------|
| planned | shape      | 0ms     | 0ms    | 0ms          | 0        |
| planned | plan       | 47.5s   | 47.5s  | 0ms          | 4        |
| planned | build      | 995.5s  | 896.4s | 99.1s        | 83       |
| planned | verify     | 32.8s   | 0ms    | 32.8s        | 0        |
| planned | review     | 949.1s  | 949.1s | 0ms          | 44       |
| planned | commit     | 0ms     | 0ms    | 0ms          | 0        |
| planned | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| planned | assessment | 0ms     | 0ms    | 0ms          | 0        |
| direct  | shape      | 0ms     | 0ms    | 0ms          | 0        |
| direct  | plan       | 0ms     | 0ms    | 0ms          | 0        |
| direct  | build      | 1036.6s | 956.6s | 80s          | 80       |
| direct  | verify     | 19.9s   | 0ms    | 19.9s        | 0        |
| direct  | review     | 764.1s  | 764.1s | 0ms          | 38       |
| direct  | commit     | 0ms     | 0ms    | 0ms          | 0        |
| direct  | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| direct  | assessment | 0ms     | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                        | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| pd2-r70-1-go-r0-direct-a1      | correct | 626.6s | 602.4s | 24.1s        | 37       | 3       | 4       | 0         | 0                    |
| pd2-r70-1-go-r0-planned-a1     | correct | 556.7s | 529.2s | 27.5s        | 36       | 3       | 4       | 0         | 0                    |
| pd2-r70-4-elixir-r0-direct-a1  | correct | 657.7s | 597.6s | 60.1s        | 40       | 3       | 4       | 0         | 0                    |
| pd2-r70-4-elixir-r0-planned-a1 | correct | 904.9s | 811.5s | 93.4s        | 54       | 6       | 6       | 0         | 0                    |
| pd2-r70-4-go-r0-direct-a1      | correct | 377.8s | 358.1s | 19.6s        | 25       | 2       | 3       | 0         | 0                    |
| pd2-r70-4-go-r0-planned-a1     | correct | 392.8s | 375s   | 17.8s        | 25       | 2       | 3       | 0         | 0                    |
| pd2-r70-6-elixir-r0-direct-a1  | correct | 181.1s | 162.6s | 18.5s        | 16       | 0       | 1       | 0         | 0                    |
| pd2-r70-6-elixir-r0-planned-a1 | correct | 192.2s | 177.3s | 14.9s        | 16       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
direct openai: input 1.94M, cached 0.18M, output 59.5k, reasoning 29.8k, input_tokens_details.cache_write_tokens 0, total_tokens 2.00M
planned openai: input 2.16M, cached 0.21M, output 64.8k, reasoning 32.8k, input_tokens_details.cache_write_tokens 0, total_tokens 2.23M
native usage by stage and provider:
stage build direct openai (responses): input 1.12M, cached 0.14M, output 32.1k, reasoning 7.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.16M
stage build planned openai (responses): input 1.15M, cached 0.21M, output 29.0k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.18M
stage plan planned openai (responses): input 18.4k, cached 0, output 1.7k, reasoning 67, input_tokens_details.cache_write_tokens 0, total_tokens 20.1k
stage review direct openai (responses): input 0.82M, cached 44.7k, output 27.4k, reasoning 22.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.85M
stage review planned openai (responses): input 0.99M, cached 0, output 34.0k, reasoning 28.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.02M
native usage by attempt and provider:
attempt usage pd2-r70-1-go-r0-direct-a1 openai (responses): input 0.72M, cached 97.8k, output 21.7k, reasoning 10.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.74M
attempt usage pd2-r70-1-go-r0-planned-a1 openai (responses): input 0.68M, cached 46.7k, output 18.8k, reasoning 7.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
attempt usage pd2-r70-4-elixir-r0-direct-a1 openai (responses): input 0.68M, cached 68.1k, output 20.9k, reasoning 12.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
attempt usage pd2-r70-4-elixir-r0-planned-a1 openai (responses): input 0.92M, cached 0.11M, output 27.1k, reasoning 17.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.94M
attempt usage pd2-r70-4-go-r0-direct-a1 openai (responses): input 0.34M, cached 0, output 11.8k, reasoning 6.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage pd2-r70-4-go-r0-planned-a1 openai (responses): input 0.36M, cached 38.0k, output 12.9k, reasoning 6.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage pd2-r70-6-elixir-r0-direct-a1 openai (responses): input 0.20M, cached 16.8k, output 5.2k, reasoning 672, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage pd2-r70-6-elixir-r0-planned-a1 openai (responses): input 0.21M, cached 11.9k, output 5.9k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt outcomes included: planned: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; direct: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 3889.8s, model 3613.7s, tools/checks 276.1s, requests 249
builder settings: planned openai gpt-6.1-sol reasoning.effort=medium
builder settings: direct openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant direct differs from planned in:
  plan.enabled: true -> false
P01: exercised in 4 of 4 direct attempts
first position per task: r70-1-go planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: r70-4-elixir planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: r70-4-go planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: r70-6-elixir planned 0, direct 1 (1 repetitions, 2 variants)
planned: not the Kogen profile (differs in stop.max_repairs, stop.max_tokens)
direct: not the Kogen profile (differs in plan.enabled, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
planned: repair.context = packet,diff,check_results,review_findings (extension)
planned: repair.roles = builder (extension)
planned: shape.critique_prompt = lab:critique (extension)
planned: shape.critique_rounds = 1 (extension)
direct: repair.context = packet,diff,check_results,review_findings (extension)
direct: repair.roles = builder (extension)
direct: shape.critique_prompt = lab:critique (extension)
direct: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
