complete: 14/14 cells scored
Question: planner-direct-1: with Kogen b2c9876b's default roles, does building directly without a planner change correctness, repairs or tokens?
Hypothesis: exploratory: the direct build matches the planned build at lower token cost
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| planned | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
| direct  | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
false success: 0 of 7 claims (planned)
false success: 0 of 7 claims (direct)
shaping outcomes:
planned: shaping ready 7, shaping failed 0; correct 7 of 7
direct: shaping ready 7, shaping failed 0; correct 7 of 7
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| env-ex       | planned | 1       | 0         | 0                | 0              | 0          |
| env-ex       | direct  | 1       | 0         | 0                | 0              | 0          |
| env-go       | planned | 1       | 0         | 0                | 0              | 0          |
| env-go       | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | planned | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | planned | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | planned | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | direct  | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | planned | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | direct  | 1       | 0         | 0                | 0              | 0          |
| sched-go     | planned | 1       | 0         | 0                | 0              | 0          |
| sched-go     | direct  | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| planned | shape      | 0ms     | 0ms     | 0ms          | 0        |
| planned | plan       | 85.7s   | 85.7s   | 0ms          | 7        |
| planned | build      | 1076.8s | 1033.3s | 43.5s        | 64       |
| planned | verify     | 21.3s   | 0ms     | 21.3s        | 0        |
| planned | review     | 196.4s  | 196.4s  | 0ms          | 20       |
| planned | commit     | 0ms     | 0ms     | 0ms          | 0        |
| planned | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| planned | assessment | 0ms     | 0ms     | 0ms          | 0        |
| direct  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| direct  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| direct  | build      | 959.8s  | 927.6s  | 32.2s        | 58       |
| direct  | verify     | 7.6s    | 0ms     | 7.6s         | 0        |
| direct  | review     | 186.6s  | 186.6s  | 0ms          | 21       |
| direct  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| direct  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| direct  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                        | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| pd1-env-ex-r0-direct-a1        | correct | 170s   | 160.2s | 9.8s         | 11       | 0       | 1       | 0         | 0                    |
| pd1-env-ex-r0-planned-a1       | correct | 238.9s | 221s   | 17.9s        | 14       | 0       | 1       | 0         | 0                    |
| pd1-env-go-r0-direct-a1        | correct | 172.7s | 163.8s | 8.8s         | 12       | 0       | 1       | 0         | 0                    |
| pd1-env-go-r0-planned-a1       | correct | 205.5s | 198.1s | 7.4s         | 13       | 0       | 1       | 0         | 0                    |
| pd1-r70-5-elixir-r0-direct-a1  | correct | 178.7s | 166.3s | 12.4s        | 12       | 0       | 1       | 0         | 0                    |
| pd1-r70-5-elixir-r0-planned-a1 | correct | 168.6s | 160.1s | 8.5s         | 12       | 0       | 1       | 0         | 0                    |
| pd1-r70-5-go-r0-direct-a1      | correct | 144.9s | 136s   | 8.9s         | 10       | 0       | 1       | 0         | 0                    |
| pd1-r70-5-go-r0-planned-a1     | correct | 208.3s | 199s   | 9.3s         | 14       | 0       | 1       | 0         | 0                    |
| pd1-r70-7-elixir-r0-direct-a1  | correct | 167.3s | 157.8s | 9.6s         | 11       | 0       | 1       | 0         | 0                    |
| pd1-r70-7-elixir-r0-planned-a1 | correct | 213.1s | 185.5s | 27.7s        | 14       | 0       | 1       | 0         | 0                    |
| pd1-r70-7-go-r0-direct-a1      | correct | 161.2s | 152.1s | 9.1s         | 11       | 0       | 1       | 0         | 0                    |
| pd1-r70-7-go-r0-planned-a1     | correct | 168.3s | 160.5s | 7.8s         | 12       | 0       | 1       | 0         | 0                    |
| pd1-sched-go-r0-direct-a1      | correct | 187.1s | 178s   | 9.2s         | 12       | 0       | 1       | 0         | 0                    |
| pd1-sched-go-r0-planned-a1     | correct | 200.3s | 191.3s | 9.1s         | 12       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
direct openai: input 0.95M, cached 14.6k, output 38.8k, reasoning 4.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.99M
planned openai: input 1.10M, cached 26.2k, output 46.4k, reasoning 5.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.14M
native usage by stage and provider:
stage build direct openai (responses): input 0.53M, cached 14.6k, output 34.6k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.56M
stage build planned openai (responses): input 0.64M, cached 26.2k, output 39.2k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.68M
stage plan planned openai (responses): input 31.9k, cached 0, output 2.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.5k
stage review direct openai (responses): input 0.42M, cached 0, output 4.2k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
stage review planned openai (responses): input 0.42M, cached 0, output 4.6k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
native usage by attempt and provider:
attempt usage pd1-env-ex-r0-direct-a1 openai (responses): input 0.14M, cached 9.5k, output 5.7k, reasoning 892, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage pd1-env-ex-r0-planned-a1 openai (responses): input 0.18M, cached 0, output 7.7k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage pd1-env-go-r0-direct-a1 openai (responses): input 0.15M, cached 0, output 5.8k, reasoning 526, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage pd1-env-go-r0-planned-a1 openai (responses): input 0.17M, cached 0, output 6.8k, reasoning 625, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage pd1-r70-5-elixir-r0-direct-a1 openai (responses): input 0.13M, cached 0, output 5.0k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage pd1-r70-5-elixir-r0-planned-a1 openai (responses): input 0.14M, cached 0, output 5.7k, reasoning 875, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage pd1-r70-5-go-r0-direct-a1 openai (responses): input 0.11M, cached 0, output 4.6k, reasoning 744, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage pd1-r70-5-go-r0-planned-a1 openai (responses): input 0.17M, cached 5.1k, output 7.1k, reasoning 615, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage pd1-r70-7-elixir-r0-direct-a1 openai (responses): input 0.13M, cached 0, output 5.6k, reasoning 692, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage pd1-r70-7-elixir-r0-planned-a1 openai (responses): input 0.17M, cached 9.3k, output 6.5k, reasoning 707, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage pd1-r70-7-go-r0-direct-a1 openai (responses): input 0.13M, cached 0, output 5.5k, reasoning 401, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage pd1-r70-7-go-r0-planned-a1 openai (responses): input 0.14M, cached 5.1k, output 5.6k, reasoning 516, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage pd1-sched-go-r0-direct-a1 openai (responses): input 0.16M, cached 5.1k, output 6.6k, reasoning 413, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage pd1-sched-go-r0-planned-a1 openai (responses): input 0.14M, cached 6.7k, output 7.1k, reasoning 585, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt outcomes included: planned: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; direct: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2585.1s, model 2429.7s, tools/checks 155.4s, requests 170
builder settings: planned openai gpt-6.1-sol reasoning.effort=medium
builder settings: direct openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 14, started 14, scored 14, incorrect 0, infrastructure 0, incomplete 0
variant direct differs from planned in:
  plan.enabled: true -> false
P01: exercised in 7 of 7 direct attempts
first position per task: env-ex planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: env-go planned 1, direct 0 (1 repetitions, 2 variants)
first position per task: r70-5-elixir planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: r70-5-go planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: r70-7-elixir planned 1, direct 0 (1 repetitions, 2 variants)
first position per task: r70-7-go planned 0, direct 1 (1 repetitions, 2 variants)
first position per task: sched-go planned 0, direct 1 (1 repetitions, 2 variants)
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
