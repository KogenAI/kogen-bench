complete: 16/16 cells scored
Question: review-named-defect-1 run 2: with a weak builder whose wrong code reaches review, does the named-defect rule keep Kogen's Sol-high reviewer-fixer's rescues and correctness at lower reviewer input?
Hypothesis: exploratory: rescues and correctness unchanged; reviewer input lower (rn1: -15%)
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant      | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|--------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen-review | 4       | 0         | 4                | 0              | 0          | 50%          | 0 of 4        | 0           |
| named-defect | 5       | 0         | 3                | 0              | 0          | 62.5%        | 0 of 5        | 0           |
false success: 0 of 4 claims (kogen-review)
false success: 0 of 5 claims (named-defect)
shaping outcomes:
kogen-review: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
named-defect: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant      | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|--------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | kogen-review | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | named-defect | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | kogen-review | 0       | 0         | 2                | 0              | 0          |
| r70-4-elixir-2 | named-defect | 1       | 0         | 1                | 0              | 0          |
| r70-4-go       | kogen-review | 1       | 0         | 1                | 0              | 0          |
| r70-4-go       | named-defect | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | kogen-review | 1       | 0         | 1                | 0              | 0          |
| r70-6-elixir-2 | named-defect | 0       | 0         | 2                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant      | stage      | elapsed time    | model   | tools/checks | requests |
|--------------|------------|---------|---------|--------------|----------|
| kogen-review | shape      | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | plan       | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | build      | 8584.2s | 8492.2s | 92s          | 128      |
| kogen-review | verify     | 14.6s   | 0ms     | 14.6s        | 0        |
| kogen-review | review     | 4781.7s | 4781.7s | 0ms          | 71       |
| kogen-review | commit     | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | assessment | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | shape      | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | plan       | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | build      | 9410.6s | 8359.7s | 1050.9s      | 140      |
| named-defect | verify     | 15.8s   | 0ms     | 15.8s        | 0        |
| named-defect | review     | 5784.1s | 5784.1s | 0ms          | 77       |
| named-defect | commit     | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome          | elapsed time    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rn2-r70-1-go-r0-kogen-review-a1       | correct          | 1536.6s | 1510.1s | 26.5s        | 32       | 2       | 1       | 0         | 0                    |
| rn2-r70-1-go-r0-named-defect-a1       | correct          | 1913.8s | 1887.1s | 26.8s        | 22       | 0       | 1       | 0         | 0                    |
| rn2-r70-1-go-r1-kogen-review-a1       | correct          | 3193.8s | 3171.9s | 21.9s        | 26       | 0       | 1       | 0         | 0                    |
| rn2-r70-1-go-r1-named-defect-a1       | correct          | 2188.3s | 2154.2s | 34.1s        | 36       | 1       | 1       | 0         | 0                    |
| rn2-r70-4-elixir-2-r0-kogen-review-a1 | workflow failure | 822.8s  | 814s    | 8.7s         | 18       | 6       | 0       | 0         | 0                    |
| rn2-r70-4-elixir-2-r0-named-defect-a1 | workflow failure | 3524.2s | 3509.3s | 14.9s        | 19       | 4       | 0       | 0         | 0                    |
| rn2-r70-4-elixir-2-r1-kogen-review-a1 | workflow failure | 3560s   | 3537.2s | 22.8s        | 28       | 5       | 0       | 0         | 0                    |
| rn2-r70-4-elixir-2-r1-named-defect-a1 | correct          | 2324.5s | 1387.7s | 936.8s       | 30       | 4       | 1       | 0         | 0                    |
| rn2-r70-4-go-r0-kogen-review-a1       | workflow failure | 1884.7s | 1870.9s | 13.9s        | 22       | 6       | 0       | 0         | 0                    |
| rn2-r70-4-go-r0-named-defect-a1       | correct          | 1211.9s | 1192.3s | 19.6s        | 20       | 0       | 1       | 0         | 0                    |
| rn2-r70-4-go-r1-kogen-review-a1       | correct          | 396.5s  | 384.1s  | 12.4s        | 15       | 0       | 1       | 0         | 0                    |
| rn2-r70-4-go-r1-named-defect-a1       | correct          | 1785.1s | 1770.3s | 14.8s        | 18       | 0       | 1       | 0         | 0                    |
| rn2-r70-6-elixir-2-r0-kogen-review-a1 | correct          | 760.8s  | 715.3s  | 45.5s        | 37       | 1       | 1       | 0         | 0                    |
| rn2-r70-6-elixir-2-r0-named-defect-a1 | workflow failure | 1392.5s | 1384.6s | 7.8s         | 25       | 6       | 0       | 0         | 0                    |
| rn2-r70-6-elixir-2-r1-kogen-review-a1 | workflow failure | 1278.3s | 1270.3s | 8s           | 21       | 6       | 0       | 0         | 0                    |
| rn2-r70-6-elixir-2-r1-named-defect-a1 | workflow failure | 923.7s  | 858.3s  | 65.4s        | 47       | 6       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen-review openai: input 3.43M, cached 0.71M, output 98.1k, reasoning 31.8k, input_tokens_details.cache_write_tokens 0, total_tokens 3.53M
named-defect openai: input 4.10M, cached 1.17M, output 0.12M, reasoning 34.5k, input_tokens_details.cache_write_tokens 0, total_tokens 4.22M
native usage by stage and provider:
stage build kogen-review openai (responses): input 1.65M, cached 0.62M, output 33.0k, reasoning 131, input_tokens_details.cache_write_tokens 0, total_tokens 1.68M
stage build named-defect openai (responses): input 2.29M, cached 1.00M, output 54.6k, reasoning 180, input_tokens_details.cache_write_tokens 0, total_tokens 2.35M
stage review kogen-review openai (responses): input 1.78M, cached 89.0k, output 65.1k, reasoning 31.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.85M
stage review named-defect openai (responses): input 1.81M, cached 0.17M, output 67.6k, reasoning 34.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.88M
native usage by attempt and provider:
attempt usage rn2-r70-1-go-r0-kogen-review-a1 openai (responses): input 0.70M, cached 35.6k, output 29.6k, reasoning 14.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
attempt usage rn2-r70-1-go-r0-named-defect-a1 openai (responses): input 0.44M, cached 28.5k, output 24.7k, reasoning 11.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage rn2-r70-1-go-r1-kogen-review-a1 openai (responses): input 0.57M, cached 52.7k, output 20.2k, reasoning 8.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage rn2-r70-1-go-r1-named-defect-a1 openai (responses): input 0.87M, cached 0.16M, output 24.4k, reasoning 10.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
attempt usage rn2-r70-4-elixir-2-r0-kogen-review-a1 openai (responses): input 0.22M, cached 96.5k, output 6.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rn2-r70-4-elixir-2-r0-named-defect-a1 openai (responses): input 0.22M, cached 69.1k, output 8.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rn2-r70-4-elixir-2-r1-kogen-review-a1 openai (responses): input 0.40M, cached 0.15M, output 7.2k, reasoning 516, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage rn2-r70-4-elixir-2-r1-named-defect-a1 openai (responses): input 0.48M, cached 86.3k, output 17.6k, reasoning 6.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
attempt usage rn2-r70-4-go-r0-kogen-review-a1 openai (responses): input 0.26M, cached 0.11M, output 4.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rn2-r70-4-go-r0-named-defect-a1 openai (responses): input 0.30M, cached 15.0k, output 11.8k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage rn2-r70-4-go-r1-kogen-review-a1 openai (responses): input 0.20M, cached 22.1k, output 8.7k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rn2-r70-4-go-r1-named-defect-a1 openai (responses): input 0.23M, cached 28.7k, output 9.1k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rn2-r70-6-elixir-2-r0-kogen-review-a1 openai (responses): input 0.70M, cached 0.13M, output 18.8k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
attempt usage rn2-r70-6-elixir-2-r0-named-defect-a1 openai (responses): input 0.51M, cached 0.24M, output 8.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage rn2-r70-6-elixir-2-r1-kogen-review-a1 openai (responses): input 0.38M, cached 0.12M, output 2.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage rn2-r70-6-elixir-2-r1-named-defect-a1 openai (responses): input 1.05M, cached 0.54M, output 17.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
attempt outcomes included: kogen-review: correct 4, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0; named-defect: correct 5, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 28697.5s, model 27417.7s, tools/checks 1279.9s, requests 416
builder settings: kogen-review openai gpt-6-luna reasoning.effort=low; named-defect openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant named-defect differs from kogen-review in:
  reviewer instruction: published in the round README
C02: exercised in 8 of 8 named-defect attempts
first position per task: r70-1-go kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-4-go kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
kogen-review: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
named-defect: not the Kogen profile (differs in the reviewer instruction, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
kogen-review: build.helper_context = lab_helper (extension)
kogen-review: build.helper_prompt = lab:helper (extension)
kogen-review: build.subagents_output = 4096 (extension)
kogen-review: build.subagents_turns = 10 (extension)
kogen-review: plan.context = kogen_planner (extension)
kogen-review: plan.prompt = lab:plan (extension)
kogen-review: repair.context = packet,diff,check_results,review_findings (extension)
kogen-review: repair.roles = builder (extension)
kogen-review: review.timing = every_green (extension)
kogen-review: shape.critique_prompt = lab:critique (extension)
kogen-review: shape.critique_rounds = 1 (extension)
kogen-review: shape.helper_context = lab_helper (extension)
kogen-review: shape.helper_prompt = lab:helper (extension)
kogen-review: shape.subagents_output = 4096 (extension)
kogen-review: shape.subagents_turns = 10 (extension)
named-defect: build.helper_context = lab_helper (extension)
named-defect: build.helper_prompt = lab:helper (extension)
named-defect: build.subagents_output = 4096 (extension)
named-defect: build.subagents_turns = 10 (extension)
named-defect: plan.context = kogen_planner (extension)
named-defect: plan.prompt = lab:plan (extension)
named-defect: repair.context = packet,diff,check_results,review_findings (extension)
named-defect: repair.roles = builder (extension)
named-defect: review.timing = every_green (extension)
named-defect: shape.critique_prompt = lab:critique (extension)
named-defect: shape.critique_rounds = 1 (extension)
named-defect: shape.helper_context = lab_helper (extension)
named-defect: shape.helper_prompt = lab:helper (extension)
named-defect: shape.subagents_output = 4096 (extension)
named-defect: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
