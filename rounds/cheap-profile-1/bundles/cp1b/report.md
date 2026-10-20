complete: 8/8 cells scored
Question: cheap-profile-1: does a Sol-low builder with a Sol-medium reviewer-fixer keep Kogen's default correctness on the harder tasks at a much lower total input?
Hypothesis: exploratory: same correctness, total input at least 25% lower
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen-default | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| cheap         | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (kogen-default)
false success: 0 of 4 claims (cheap)
shaping outcomes:
kogen-default: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
cheap: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant       | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------------|---------|-----------|------------------|----------------|------------|
| r70-1-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-1-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant       | stage      | elapsed time   | model  | tools/checks | requests |
|---------------|------------|--------|--------|--------------|----------|
| kogen-default | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | plan       | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | build      | 603.9s | 492.6s | 111.4s       | 34       |
| kogen-default | verify     | 21.6s  | 0ms    | 21.6s        | 0        |
| kogen-default | review     | 662.7s | 662.7s | 0ms          | 35       |
| kogen-default | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | assessment | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | shape      | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | plan       | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | build      | 324.8s | 286.4s | 38.4s        | 27       |
| cheap         | verify     | 12.6s  | 0ms    | 12.6s        | 0        |
| cheap         | review     | 417.9s | 417.9s | 0ms          | 32       |
| cheap         | commit     | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cp1b-r70-1-go-r0-cheap-a1             | correct | 270.1s | 248.6s | 21.5s        | 14       | 0       | 1       | 0         | 0                    |
| cp1b-r70-1-go-r0-kogen-default-a1     | correct | 532.4s | 470s   | 62.4s        | 22       | 0       | 1       | 0         | 0                    |
| cp1b-r70-4-go-r0-cheap-a1             | correct | 181.6s | 159.9s | 21.6s        | 17       | 0       | 1       | 0         | 0                    |
| cp1b-r70-4-go-r0-kogen-default-a1     | correct | 328.2s | 297.2s | 31s          | 17       | 0       | 1       | 0         | 0                    |
| cp1b-r70-7-elixir-r0-cheap-a1         | correct | 159.8s | 142.6s | 17.3s        | 14       | 0       | 1       | 0         | 0                    |
| cp1b-r70-7-elixir-r0-kogen-default-a1 | correct | 223.4s | 186.7s | 36.7s        | 13       | 0       | 1       | 0         | 0                    |
| cp1b-r70-7-go-r0-cheap-a1             | correct | 162.9s | 153.2s | 9.8s         | 14       | 0       | 1       | 0         | 0                    |
| cp1b-r70-7-go-r0-kogen-default-a1     | correct | 218.8s | 201.5s | 17.3s        | 17       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
cheap openai: input 0.69M, cached 44.2k, output 23.7k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
kogen-default openai: input 1.06M, cached 60.4k, output 43.8k, reasoning 13.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.11M
native usage by stage and provider:
stage build cheap openai (responses): input 0.21M, cached 0, output 9.3k, reasoning 306, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
stage build kogen-default openai (responses): input 0.32M, cached 35.6k, output 18.6k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
stage review cheap openai (responses): input 0.48M, cached 44.2k, output 14.4k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
stage review kogen-default openai (responses): input 0.74M, cached 24.8k, output 25.2k, reasoning 12.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.77M
native usage by attempt and provider:
attempt usage cp1b-r70-1-go-r0-cheap-a1 openai (responses): input 0.19M, cached 18.4k, output 9.1k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage cp1b-r70-1-go-r0-kogen-default-a1 openai (responses): input 0.46M, cached 30.5k, output 18.5k, reasoning 7.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt usage cp1b-r70-4-go-r0-cheap-a1 openai (responses): input 0.20M, cached 11.8k, output 4.9k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage cp1b-r70-4-go-r0-kogen-default-a1 openai (responses): input 0.24M, cached 0, output 11.0k, reasoning 4.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage cp1b-r70-7-elixir-r0-cheap-a1 openai (responses): input 0.16M, cached 14.0k, output 4.7k, reasoning 392, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cp1b-r70-7-elixir-r0-kogen-default-a1 openai (responses): input 0.15M, cached 10.8k, output 7.1k, reasoning 865, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cp1b-r70-7-go-r0-cheap-a1 openai (responses): input 0.14M, cached 0, output 5.0k, reasoning 271, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage cp1b-r70-7-go-r0-kogen-default-a1 openai (responses): input 0.20M, cached 19.2k, output 7.3k, reasoning 998, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt outcomes included: kogen-default: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; cheap: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2077.3s, model 1859.6s, tools/checks 217.6s, requests 128
builder settings: kogen-default openai gpt-6.1-sol reasoning.effort=medium; cheap openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant cheap differs from kogen-default in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6.1-sol low
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.builder.effort: exercised in 4 of 4 cheap attempts
roles.reviewer.effort: exercised in 4 of 4 cheap attempts
first position per task: r70-1-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-4-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-7-elixir kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-7-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
kogen-default: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
cheap: not the Kogen profile (differs in roles.builder.effort, roles.reviewer.effort, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
kogen-default: build.helper_context = lab_helper (extension)
kogen-default: build.helper_prompt = lab:helper (extension)
kogen-default: build.subagents_output = 4096 (extension)
kogen-default: build.subagents_turns = 10 (extension)
kogen-default: plan.context = kogen_planner (extension)
kogen-default: plan.prompt = lab:plan (extension)
kogen-default: repair.context = packet,diff,check_results,review_findings (extension)
kogen-default: repair.roles = builder (extension)
kogen-default: review.timing = every_green (extension)
kogen-default: shape.critique_prompt = lab:critique (extension)
kogen-default: shape.critique_rounds = 1 (extension)
kogen-default: shape.helper_context = lab_helper (extension)
kogen-default: shape.helper_prompt = lab:helper (extension)
kogen-default: shape.subagents_output = 4096 (extension)
kogen-default: shape.subagents_turns = 10 (extension)
cheap: build.helper_context = lab_helper (extension)
cheap: build.helper_prompt = lab:helper (extension)
cheap: build.subagents_output = 4096 (extension)
cheap: build.subagents_turns = 10 (extension)
cheap: plan.context = kogen_planner (extension)
cheap: plan.prompt = lab:plan (extension)
cheap: repair.context = packet,diff,check_results,review_findings (extension)
cheap: repair.roles = builder (extension)
cheap: review.timing = every_green (extension)
cheap: shape.critique_prompt = lab:critique (extension)
cheap: shape.critique_rounds = 1 (extension)
cheap: shape.helper_context = lab_helper (extension)
cheap: shape.helper_prompt = lab:helper (extension)
cheap: shape.subagents_output = 4096 (extension)
cheap: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
