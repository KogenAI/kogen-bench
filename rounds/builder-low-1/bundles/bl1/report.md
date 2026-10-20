complete: 16/16 cells scored
Question: builder-low-1: with Kogen b45ba32b defaults and prose plus Gherkin specifications, does a Sol-low builder keep the default Sol-medium builder's correctness on the harder tasks at less input?
Hypothesis: exploratory: Sol low matches Sol medium on these tasks (repair-cost-1: Sol low was the cheapest builder at 7/7) at lower cost
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| sol-medium | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| sol-low    | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (sol-medium)
false success: 0 of 8 claims (sol-low)
shaping outcomes:
sol-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
sol-low: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | sol-medium | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | sol-low    | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | sol-medium | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | sol-low    | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | sol-medium | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | sol-low    | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | sol-medium | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | sol-low    | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| sol-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| sol-medium | build      | 1765.2s | 1662.9s | 102.3s       | 67       |
| sol-medium | verify     | 21.5s   | 0ms     | 21.5s        | 0        |
| sol-medium | review     | 2854.6s | 2854.6s | 0ms          | 80       |
| sol-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
| sol-low    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-low    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| sol-low    | build      | 1441.2s | 1312.5s | 128.7s       | 49       |
| sol-low    | verify     | 26.7s   | 0ms     | 26.7s        | 0        |
| sol-low    | review     | 3087.7s | 3087.7s | 0ms          | 90       |
| sol-low    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-low    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-low    | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                             | outcome | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------|---------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| bl1-r70-1-go-r0-sol-low-a1          | correct | 1277.1s | 1221.7s | 55.4s        | 25       | 0       | 1       | 0         | 0                    |
| bl1-r70-1-go-r0-sol-medium-a1       | correct | 866s    | 833.6s  | 32.3s        | 20       | 0       | 1       | 0         | 0                    |
| bl1-r70-1-go-r1-sol-low-a1          | correct | 893.7s  | 876.1s  | 17.6s        | 20       | 0       | 1       | 0         | 0                    |
| bl1-r70-1-go-r1-sol-medium-a1       | correct | 1325.5s | 1293.6s | 31.9s        | 26       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-elixir-2-r0-sol-low-a1    | correct | 541s    | 516.4s  | 24.7s        | 16       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-elixir-2-r0-sol-medium-a1 | correct | 329.8s  | 312.1s  | 17.7s        | 13       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-elixir-2-r1-sol-low-a1    | correct | 266.3s  | 247.4s  | 18.9s        | 12       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-elixir-2-r1-sol-medium-a1 | correct | 433.5s  | 414.5s  | 19s          | 14       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-go-r0-sol-low-a1          | correct | 462.8s  | 445.2s  | 17.6s        | 15       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-go-r0-sol-medium-a1       | correct | 466.4s  | 450s    | 16.3s        | 18       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-go-r1-sol-low-a1          | correct | 437.4s  | 421.2s  | 16.2s        | 15       | 0       | 1       | 0         | 0                    |
| bl1-r70-4-go-r1-sol-medium-a1       | correct | 737.8s  | 721s    | 16.8s        | 23       | 0       | 1       | 0         | 0                    |
| bl1-r70-6-elixir-2-r0-sol-low-a1    | correct | 352s    | 328.3s  | 23.8s        | 17       | 0       | 1       | 0         | 0                    |
| bl1-r70-6-elixir-2-r0-sol-medium-a1 | correct | 322.2s  | 306s    | 16.2s        | 16       | 0       | 1       | 0         | 0                    |
| bl1-r70-6-elixir-2-r1-sol-low-a1    | correct | 366.2s  | 343.9s  | 22.2s        | 19       | 0       | 1       | 0         | 0                    |
| bl1-r70-6-elixir-2-r1-sol-medium-a1 | correct | 202.3s  | 186.6s  | 15.6s        | 17       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
sol-low openai: input 2.33M, cached 84.2k, output 96.0k, reasoning 45.0k, input_tokens_details.cache_write_tokens 0, total_tokens 2.43M
sol-medium openai: input 2.42M, cached 0.11M, output 95.1k, reasoning 41.6k, input_tokens_details.cache_write_tokens 0, total_tokens 2.52M
native usage by stage and provider:
stage build sol-low openai (responses): input 0.41M, cached 16.9k, output 16.0k, reasoning 711, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
stage build sol-medium openai (responses): input 0.65M, cached 84.7k, output 28.7k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.68M
stage review sol-low openai (responses): input 1.92M, cached 67.3k, output 80.0k, reasoning 44.3k, input_tokens_details.cache_write_tokens 0, total_tokens 2.00M
stage review sol-medium openai (responses): input 1.77M, cached 24.8k, output 66.4k, reasoning 37.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.84M
native usage by attempt and provider:
attempt usage bl1-r70-1-go-r0-sol-low-a1 openai (responses): input 0.67M, cached 32.8k, output 29.9k, reasoning 18.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
attempt usage bl1-r70-1-go-r0-sol-medium-a1 openai (responses): input 0.44M, cached 30.5k, output 21.3k, reasoning 10.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage bl1-r70-1-go-r1-sol-low-a1 openai (responses): input 0.39M, cached 0, output 16.6k, reasoning 8.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage bl1-r70-1-go-r1-sol-medium-a1 openai (responses): input 0.63M, cached 20.2k, output 23.3k, reasoning 11.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
attempt usage bl1-r70-4-elixir-2-r0-sol-low-a1 openai (responses): input 0.24M, cached 19.3k, output 10.2k, reasoning 5.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage bl1-r70-4-elixir-2-r0-sol-medium-a1 openai (responses): input 0.16M, cached 5.1k, output 6.7k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage bl1-r70-4-elixir-2-r1-sol-low-a1 openai (responses): input 0.15M, cached 5.1k, output 5.9k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage bl1-r70-4-elixir-2-r1-sol-medium-a1 openai (responses): input 0.18M, cached 0, output 9.2k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage bl1-r70-4-go-r0-sol-low-a1 openai (responses): input 0.20M, cached 5.0k, output 11.0k, reasoning 4.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage bl1-r70-4-go-r0-sol-medium-a1 openai (responses): input 0.25M, cached 0, output 10.2k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage bl1-r70-4-go-r1-sol-low-a1 openai (responses): input 0.19M, cached 0, output 6.7k, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage bl1-r70-4-go-r1-sol-medium-a1 openai (responses): input 0.36M, cached 10.0k, output 13.3k, reasoning 5.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage bl1-r70-6-elixir-2-r0-sol-low-a1 openai (responses): input 0.24M, cached 15.2k, output 7.6k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage bl1-r70-6-elixir-2-r0-sol-medium-a1 openai (responses): input 0.19M, cached 25.7k, output 5.1k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage bl1-r70-6-elixir-2-r1-sol-low-a1 openai (responses): input 0.25M, cached 6.8k, output 8.1k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage bl1-r70-6-elixir-2-r1-sol-medium-a1 openai (responses): input 0.21M, cached 18.0k, output 5.8k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt outcomes included: sol-medium: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; sol-low: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 9280.2s, model 8917.7s, tools/checks 362.4s, requests 286
builder settings: sol-medium openai gpt-6.1-sol reasoning.effort=medium; sol-low openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant sol-low differs from sol-medium in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6.1-sol low
roles.builder.effort: exercised in 8 of 8 sol-low attempts
first position per task: r70-1-go sol-medium 1, sol-low 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 sol-medium 1, sol-low 1 (2 repetitions, 2 variants)
first position per task: r70-4-go sol-medium 1, sol-low 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 sol-medium 1, sol-low 1 (2 repetitions, 2 variants)
sol-medium: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
sol-low: not the Kogen profile (differs in roles.builder.effort, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
sol-medium: build.helper_context = lab_helper (extension)
sol-medium: build.helper_prompt = lab:helper (extension)
sol-medium: build.subagents_output = 4096 (extension)
sol-medium: build.subagents_turns = 10 (extension)
sol-medium: plan.context = kogen_planner (extension)
sol-medium: plan.prompt = lab:plan (extension)
sol-medium: repair.context = packet,diff,check_results,review_findings (extension)
sol-medium: repair.roles = builder (extension)
sol-medium: review.timing = every_green (extension)
sol-medium: shape.critique_prompt = lab:critique (extension)
sol-medium: shape.critique_rounds = 1 (extension)
sol-medium: shape.helper_context = lab_helper (extension)
sol-medium: shape.helper_prompt = lab:helper (extension)
sol-medium: shape.subagents_output = 4096 (extension)
sol-medium: shape.subagents_turns = 10 (extension)
sol-low: build.helper_context = lab_helper (extension)
sol-low: build.helper_prompt = lab:helper (extension)
sol-low: build.subagents_output = 4096 (extension)
sol-low: build.subagents_turns = 10 (extension)
sol-low: plan.context = kogen_planner (extension)
sol-low: plan.prompt = lab:plan (extension)
sol-low: repair.context = packet,diff,check_results,review_findings (extension)
sol-low: repair.roles = builder (extension)
sol-low: review.timing = every_green (extension)
sol-low: shape.critique_prompt = lab:critique (extension)
sol-low: shape.critique_rounds = 1 (extension)
sol-low: shape.helper_context = lab_helper (extension)
sol-low: shape.helper_prompt = lab:helper (extension)
sol-low: shape.subagents_output = 4096 (extension)
sol-low: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
