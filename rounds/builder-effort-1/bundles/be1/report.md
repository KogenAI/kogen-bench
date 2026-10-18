complete: 16/16 cells scored
Question: builder-effort-1: with planner and builder on gpt-6-luna medium instead of low, are attempts as often correct with fewer repairs and fewer tokens?
Hypothesis: medium is correct as often as low with at most 80% of its input
Purpose: development
Objective: cost_at_quality
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| low     | 6       | 0         | 2                | 0              | 0          | 75%          | 0 of 6        | 0           |
| medium  | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 6 claims (low)
false success: 0 of 8 claims (medium)
shaping outcomes:
low: shaping ready 8, shaping failed 0; correct 6 of 8
medium: shaping ready 8, shaping failed 0; correct 8 of 8
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | low     | 1       | 0         | 1                | 0              | 0          |
| r70-5-elixir | medium  | 2       | 0         | 0                | 0              | 0          |
| r70-5-go     | low     | 2       | 0         | 0                | 0              | 0          |
| r70-5-go     | medium  | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | low     | 1       | 0         | 1                | 0              | 0          |
| r70-7-elixir | medium  | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | low     | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | medium  | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| low     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| low     | plan       | 106.7s  | 106.7s  | 0ms          | 8        |
| low     | build      | 2145.9s | 2040.6s | 105.4s       | 174      |
| low     | verify     | 35.5s   | 0ms     | 35.5s        | 0        |
| low     | review     | 311.6s  | 311.6s  | 0ms          | 42       |
| low     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| low     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| low     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| medium  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| medium  | plan       | 79.2s   | 79.2s   | 0ms          | 8        |
| medium  | build      | 1822.3s | 1671.1s | 151.2s       | 161      |
| medium  | verify     | 22s     | 0ms     | 22s          | 0        |
| medium  | review     | 384s    | 384s    | 0ms          | 34       |
| medium  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| medium  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| medium  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                       | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| be1-r70-5-elixir-r0-low-a1    | correct          | 484.6s | 462.1s | 22.4s        | 37       | 3       | 3       | 0         | 0                    |
| be1-r70-5-elixir-r0-medium-a1 | correct          | 290.3s | 273.7s | 16.6s        | 29       | 2       | 2       | 0         | 0                    |
| be1-r70-5-elixir-r1-low-a1    | workflow failure | 386.4s | 360.9s | 25.5s        | 32       | 6       | 1       | 0         | 0                    |
| be1-r70-5-elixir-r1-medium-a1 | correct          | 570s   | 523.8s | 46.2s        | 44       | 2       | 3       | 0         | 0                    |
| be1-r70-5-go-r0-low-a1        | correct          | 247.4s | 239.2s | 8.2s         | 17       | 1       | 2       | 0         | 0                    |
| be1-r70-5-go-r0-medium-a1     | correct          | 261.9s | 239.7s | 22.2s        | 20       | 1       | 2       | 0         | 0                    |
| be1-r70-5-go-r1-low-a1        | correct          | 370.8s | 347.1s | 23.7s        | 35       | 3       | 4       | 0         | 0                    |
| be1-r70-5-go-r1-medium-a1     | correct          | 264.8s | 240.4s | 24.3s        | 20       | 1       | 2       | 0         | 0                    |
| be1-r70-7-elixir-r0-low-a1    | workflow failure | 490.3s | 459s   | 31.4s        | 39       | 6       | 2       | 0         | 0                    |
| be1-r70-7-elixir-r0-medium-a1 | correct          | 297s   | 270.2s | 26.8s        | 25       | 1       | 2       | 0         | 0                    |
| be1-r70-7-elixir-r1-low-a1    | correct          | 362.7s | 328.2s | 34.4s        | 32       | 1       | 2       | 0         | 0                    |
| be1-r70-7-elixir-r1-medium-a1 | correct          | 316s   | 277.2s | 38.8s        | 32       | 2       | 2       | 0         | 0                    |
| be1-r70-7-go-r0-low-a1        | correct          | 202s   | 177.5s | 24.6s        | 22       | 2       | 2       | 0         | 0                    |
| be1-r70-7-go-r0-medium-a1     | correct          | 165.3s | 142.6s | 22.8s        | 10       | 0       | 1       | 0         | 0                    |
| be1-r70-7-go-r1-low-a1        | correct          | 101.6s | 84.8s  | 16.8s        | 10       | 0       | 1       | 0         | 0                    |
| be1-r70-7-go-r1-medium-a1     | correct          | 185.1s | 166.7s | 18.5s        | 23       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
low openai: input 3.43M, cached 1.00M, output 65.8k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 3.49M
medium openai: input 2.67M, cached 0.65M, output 54.2k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 2.73M
native usage by stage and provider:
stage build low openai (responses): input 2.75M, cached 0.99M, output 59.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.81M
stage build medium openai (responses): input 2.12M, cached 0.65M, output 47.2k, reasoning 995, input_tokens_details.cache_write_tokens 0, total_tokens 2.16M
stage plan low openai (responses): input 34.4k, cached 8.2k, output 1.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 36.3k
stage plan medium openai (responses): input 34.4k, cached 0, output 2.4k, reasoning 764, input_tokens_details.cache_write_tokens 0, total_tokens 36.8k
stage review low openai (responses): input 0.65M, cached 0, output 5.0k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
stage review medium openai (responses): input 0.52M, cached 0, output 4.6k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
native usage by attempt and provider:
attempt usage be1-r70-5-elixir-r0-low-a1 openai (responses): input 0.60M, cached 0.19M, output 15.9k, reasoning 228, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
attempt usage be1-r70-5-elixir-r0-medium-a1 openai (responses): input 0.37M, cached 97.3k, output 7.0k, reasoning 195, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage be1-r70-5-elixir-r1-low-a1 openai (responses): input 0.48M, cached 0.16M, output 9.6k, reasoning 27, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage be1-r70-5-elixir-r1-medium-a1 openai (responses): input 0.82M, cached 0.37M, output 12.0k, reasoning 397, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
attempt usage be1-r70-5-go-r0-low-a1 openai (responses): input 0.17M, cached 30.0k, output 4.0k, reasoning 47, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage be1-r70-5-go-r0-medium-a1 openai (responses): input 0.20M, cached 34.8k, output 6.7k, reasoning 517, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage be1-r70-5-go-r1-low-a1 openai (responses): input 0.42M, cached 0.11M, output 8.2k, reasoning 278, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage be1-r70-5-go-r1-medium-a1 openai (responses): input 0.20M, cached 35.6k, output 6.1k, reasoning 294, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage be1-r70-7-elixir-r0-low-a1 openai (responses): input 1.00M, cached 0.37M, output 11.3k, reasoning 198, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
attempt usage be1-r70-7-elixir-r0-medium-a1 openai (responses): input 0.33M, cached 20.2k, output 6.2k, reasoning 284, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage be1-r70-7-elixir-r1-low-a1 openai (responses): input 0.42M, cached 94.3k, output 8.2k, reasoning 104, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage be1-r70-7-elixir-r1-medium-a1 openai (responses): input 0.44M, cached 55.4k, output 7.9k, reasoning 712, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage be1-r70-7-go-r0-low-a1 openai (responses): input 0.24M, cached 43.0k, output 5.9k, reasoning 166, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage be1-r70-7-go-r0-medium-a1 openai (responses): input 84.6k, cached 0, output 3.2k, reasoning 261, input_tokens_details.cache_write_tokens 0, total_tokens 87.7k
attempt usage be1-r70-7-go-r1-low-a1 openai (responses): input 92.0k, cached 0, output 2.7k, reasoning 77, input_tokens_details.cache_write_tokens 0, total_tokens 94.7k
attempt usage be1-r70-7-go-r1-medium-a1 openai (responses): input 0.23M, cached 43.9k, output 5.1k, reasoning 146, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt outcomes included: low: correct 6, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0; medium: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 4996.2s, model 4593.1s, tools/checks 403.1s, requests 427
builder settings: low openai gpt-6-luna reasoning.effort=low
builder settings: medium openai gpt-6-luna reasoning.effort=medium (not equivalent)
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant medium differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna medium
  roles.planner: openai gpt-6-luna low -> openai gpt-6-luna medium
roles.builder.effort: exercised in 8 of 8 medium attempts
roles.planner.effort: exercised in 8 of 8 medium attempts
first position per task: r70-5-elixir low 1, medium 1 (2 repetitions, 2 variants)
first position per task: r70-5-go low 1, medium 1 (2 repetitions, 2 variants)
first position per task: r70-7-elixir low 1, medium 1 (2 repetitions, 2 variants)
first position per task: r70-7-go low 1, medium 1 (2 repetitions, 2 variants)
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
