complete: 12/12 cells scored
Question: builder-subagents-2: with Kogen b45ba32b defaults, does an explore helper the builder is told about (hint) or must call once (required) change correctness, wrong submissions, tokens or time?
Hypothesis: exploratory: with guidance the builder uses the helper; whether that helps is open
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant  | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| off      | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
| hint     | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| required | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 3 claims (off)
false success: 0 of 4 claims (hint)
false success: 0 of 4 claims (required)
shaping outcomes:
off: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
hint: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
required: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant  | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|----------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | off      | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | hint     | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | required | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | off      | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | hint     | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | required | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | off      | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | hint     | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | required | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | off      | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | hint     | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | required | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant  | stage      | wall    | model   | tools/checks | requests |
|----------|------------|---------|---------|--------------|----------|
| off      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| off      | plan       | 0ms     | 0ms     | 0ms          | 0        |
| off      | build      | 655s    | 473s    | 182s         | 38       |
| off      | verify     | 16.3s   | 0ms     | 16.3s        | 0        |
| off      | review     | 1015.8s | 1015.8s | 0ms          | 47       |
| off      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| off      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| off      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| hint     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| hint     | plan       | 0ms     | 0ms     | 0ms          | 0        |
| hint     | build      | 548.3s  | 462.9s  | 85.4s        | 35       |
| hint     | verify     | 23s     | 0ms     | 23s          | 0        |
| hint     | review     | 890.6s  | 890.6s  | 0ms          | 38       |
| hint     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| hint     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| hint     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| required | shape      | 0ms     | 0ms     | 0ms          | 0        |
| required | plan       | 0ms     | 0ms     | 0ms          | 0        |
| required | build      | 685.4s  | 590.2s  | 95.2s        | 47       |
| required | verify     | 22.7s   | 0ms     | 22.7s        | 0        |
| required | review     | 702.7s  | 702.7s  | 0ms          | 39       |
| required | commit     | 0ms     | 0ms     | 0ms          | 0        |
| required | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| required | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| bs2-r70-1-go-r0-hint-a1           | correct          | 513.3s | 479.5s | 33.8s        | 22       | 0       | 1       | 0         | 0                    |
| bs2-r70-1-go-r0-off-a1            | correct          | 896.3s | 752.2s | 144.2s       | 30       | 0       | 1       | 0         | 0                    |
| bs2-r70-1-go-r0-required-a1       | correct          | 495s   | 451.5s | 43.5s        | 29       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-elixir-2-r0-hint-a1     | correct          | 266.6s | 236.3s | 30.3s        | 16       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-elixir-2-r0-off-a1      | workflow failure | 299.8s | 266.9s | 32.9s        | 20       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-elixir-2-r0-required-a1 | correct          | 357.4s | 314.2s | 43.2s        | 21       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-go-r0-hint-a1           | correct          | 495.6s | 452.8s | 42.8s        | 18       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-go-r0-off-a1            | correct          | 325.8s | 302.4s | 23.5s        | 18       | 0       | 1       | 0         | 0                    |
| bs2-r70-4-go-r0-required-a1       | correct          | 379.3s | 347s   | 32.3s        | 23       | 0       | 1       | 0         | 0                    |
| bs2-r70-6-elixir-2-r0-hint-a1     | correct          | 202.2s | 184.8s | 17.4s        | 17       | 0       | 1       | 0         | 0                    |
| bs2-r70-6-elixir-2-r0-off-a1      | correct          | 180.1s | 167.4s | 12.7s        | 17       | 0       | 1       | 0         | 0                    |
| bs2-r70-6-elixir-2-r0-required-a1 | correct          | 257.5s | 243.7s | 13.8s        | 21       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
hint openai: input 1.20M, cached 0.11M, output 52.0k, reasoning 21.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.25M
off openai: input 1.57M, cached 0.12M, output 54.5k, reasoning 25.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.63M
required openai: input 1.32M, cached 69.9k, output 48.6k, reasoning 16.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.37M
native usage by stage and provider:
stage build hint openai (responses): input 0.35M, cached 24.6k, output 16.3k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
stage build off openai (responses): input 0.37M, cached 73.2k, output 16.4k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
stage build required openai (responses): input 0.52M, cached 32.0k, output 20.6k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
stage review hint openai (responses): input 0.85M, cached 86.7k, output 35.7k, reasoning 18.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
stage review off openai (responses): input 1.20M, cached 51.1k, output 38.1k, reasoning 23.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.24M
stage review required openai (responses): input 0.78M, cached 37.9k, output 26.1k, reasoning 13.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.81M
stage subagent:build_helper required openai (responses): input 20.4k, cached 0, output 1.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 22.2k
native usage by attempt and provider:
attempt usage bs2-r70-1-go-r0-hint-a1 openai (responses): input 0.49M, cached 71.7k, output 18.9k, reasoning 7.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bs2-r70-1-go-r0-off-a1 openai (responses): input 0.84M, cached 60.4k, output 29.2k, reasoning 16.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.87M
attempt usage bs2-r70-1-go-r0-required-a1 openai (responses): input 0.51M, cached 37.2k, output 16.7k, reasoning 4.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
attempt usage bs2-r70-4-elixir-2-r0-hint-a1 openai (responses): input 0.20M, cached 15.0k, output 8.5k, reasoning 3.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage bs2-r70-4-elixir-2-r0-off-a1 openai (responses): input 0.28M, cached 18.3k, output 9.3k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage bs2-r70-4-elixir-2-r0-required-a1 openai (responses): input 0.27M, cached 10.5k, output 11.8k, reasoning 5.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage bs2-r70-4-go-r0-hint-a1 openai (responses): input 0.30M, cached 0, output 18.6k, reasoning 9.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage bs2-r70-4-go-r0-off-a1 openai (responses): input 0.26M, cached 20.0k, output 10.4k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage bs2-r70-4-go-r0-required-a1 openai (responses): input 0.29M, cached 7.6k, output 11.7k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage bs2-r70-6-elixir-2-r0-hint-a1 openai (responses): input 0.21M, cached 24.6k, output 6.1k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage bs2-r70-6-elixir-2-r0-off-a1 openai (responses): input 0.20M, cached 25.6k, output 5.5k, reasoning 869, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage bs2-r70-6-elixir-2-r0-required-a1 openai (responses): input 0.25M, cached 14.6k, output 8.5k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
subagent use:
hint: mean 0.00 calls per attempt, 0 of 4 attempts (0%) with at least one call; helper tokens none
required: mean 1.00 calls per attempt, 4 of 4 attempts (100%) with at least one call; helper tokens openai (responses): input 20.4k, cached 0, output 1.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 22.2k
attempt outcomes included: off: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; hint: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; required: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 4669.1s, model 4198.8s, tools/checks 470.2s, requests 252
builder settings: off openai gpt-6.1-sol reasoning.effort=medium; hint openai gpt-6.1-sol reasoning.effort=medium; required openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 12, started 12, scored 12, incorrect 0, infrastructure 0, incomplete 0
variant hint differs from off in:
  build.subagents: off -> explore
  build.subagents_guidance: none -> hint
variant required differs from off in:
  build.subagents: off -> explore
  build.subagents_guidance: none -> hint
  build.subagents_required: false -> true
B10: exercised in 4 of 4 hint attempts
B11: exercised in 4 of 4 hint attempts
B10: exercised in 4 of 4 required attempts
B11: exercised in 4 of 4 required attempts
first position per task: r70-1-go off 1, hint 0, required 0 (1 repetitions, 3 variants)
first position per task: r70-4-elixir-2 off 1, hint 0, required 0 (1 repetitions, 3 variants)
first position per task: r70-4-go off 1, hint 0, required 0 (1 repetitions, 3 variants)
first position per task: r70-6-elixir-2 off 0, hint 0, required 1 (1 repetitions, 3 variants)
off: not the Kogen profile (differs in roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_command_seconds, stop.max_wall_seconds)
hint: not the Kogen profile (differs in build.subagents, build.subagents_guidance, roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_command_seconds, stop.max_wall_seconds)
required: not the Kogen profile (differs in build.subagents, build.subagents_guidance, build.subagents_required, roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_command_seconds, stop.max_wall_seconds)
experimental stop: every variant has stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
off: build.helper_context = lab_helper (extension)
off: build.helper_prompt = lab:helper (extension)
off: build.subagents_output = 4096 (extension)
off: build.subagents_turns = 10 (extension)
off: plan.context = kogen_planner (extension)
off: plan.prompt = lab:plan (extension)
off: repair.context = packet,diff,check_results,review_findings (extension)
off: repair.roles = builder (extension)
off: review.timing = every_green (extension)
off: shape.critique_prompt = lab:critique (extension)
off: shape.critique_rounds = 1 (extension)
off: shape.helper_context = lab_helper (extension)
off: shape.helper_prompt = lab:helper (extension)
off: shape.subagents_output = 4096 (extension)
off: shape.subagents_turns = 10 (extension)
hint: build.helper_context = lab_helper (extension)
hint: build.helper_prompt = lab:helper (extension)
hint: build.subagents = explore (extension)
hint: build.subagents_guidance = hint (extension)
hint: build.subagents_output = 4096 (extension)
hint: build.subagents_turns = 10 (extension)
hint: plan.context = kogen_planner (extension)
hint: plan.prompt = lab:plan (extension)
hint: repair.context = packet,diff,check_results,review_findings (extension)
hint: repair.roles = builder (extension)
hint: review.timing = every_green (extension)
hint: shape.critique_prompt = lab:critique (extension)
hint: shape.critique_rounds = 1 (extension)
hint: shape.helper_context = lab_helper (extension)
hint: shape.helper_prompt = lab:helper (extension)
hint: shape.subagents_output = 4096 (extension)
hint: shape.subagents_turns = 10 (extension)
required: build.helper_context = lab_helper (extension)
required: build.helper_prompt = lab:helper (extension)
required: build.subagents = explore (extension)
required: build.subagents_guidance = hint (extension)
required: build.subagents_output = 4096 (extension)
required: build.subagents_required = true (extension)
required: build.subagents_turns = 10 (extension)
required: plan.context = kogen_planner (extension)
required: plan.prompt = lab:plan (extension)
required: repair.context = packet,diff,check_results,review_findings (extension)
required: repair.roles = builder (extension)
required: review.timing = every_green (extension)
required: shape.critique_prompt = lab:critique (extension)
required: shape.critique_rounds = 1 (extension)
required: shape.helper_context = lab_helper (extension)
required: shape.helper_prompt = lab:helper (extension)
required: shape.subagents_output = 4096 (extension)
required: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
