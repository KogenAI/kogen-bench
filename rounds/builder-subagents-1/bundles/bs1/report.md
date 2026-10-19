complete: 12/12 cells scored
Question: builder-subagents-1: with Kogen b2c9876b defaults, does an explore helper or a delegate helper (Luna low) change the builder's correctness, wrong submissions, tokens or time?
Hypothesis: exploratory: helpers cut the builder's own input without changing correctness
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant  | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| off      | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
| explore  | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| delegate | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 3 claims (off)
false success: 0 of 4 claims (explore)
false success: 0 of 4 claims (delegate)
shaping outcomes:
off: shaping ready 4, shaping failed 0; correct 3 of 4
explore: shaping ready 4, shaping failed 0; correct 4 of 4
delegate: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task           | variant  | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|----------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | off      | 0       | 0         | 1                | 0              | 0          |
| r70-1-go       | explore  | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | delegate | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | off      | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | explore  | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | delegate | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | off      | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | explore  | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | delegate | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | off      | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | explore  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | delegate | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant  | stage      | wall    | model   | tools/checks | requests |
|----------|------------|---------|---------|--------------|----------|
| off      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| off      | plan       | 0ms     | 0ms     | 0ms          | 0        |
| off      | build      | 3359.7s | 3266.4s | 93.3s        | 90       |
| off      | verify     | 18.5s   | 0ms     | 18.5s        | 0        |
| off      | review     | 2207.8s | 2207.8s | 0ms          | 55       |
| off      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| off      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| off      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| explore  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| explore  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| explore  | build      | 1948.8s | 1855.8s | 93s          | 65       |
| explore  | verify     | 40.7s   | 0ms     | 40.7s        | 0        |
| explore  | review     | 1175.7s | 1175.7s | 0ms          | 41       |
| explore  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| explore  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| explore  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| delegate | shape      | 0ms     | 0ms     | 0ms          | 0        |
| delegate | plan       | 0ms     | 0ms     | 0ms          | 0        |
| delegate | build      | 3285.2s | 3186.8s | 98.4s        | 86       |
| delegate | verify     | 25.3s   | 0ms     | 25.3s        | 0        |
| delegate | review     | 1553.7s | 1553.7s | 0ms          | 39       |
| delegate | commit     | 0ms     | 0ms     | 0ms          | 0        |
| delegate | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| delegate | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| bs1-r70-1-go-r0-delegate-a1       | correct          | 1887.3s | 1844.8s | 42.5s        | 48       | 3       | 4       | 0         | 0                    |
| bs1-r70-1-go-r0-explore-a1        | correct          | 705s    | 660.6s  | 44.4s        | 43       | 4       | 5       | 0         | 0                    |
| bs1-r70-1-go-r0-off-a1            | workflow failure | 2589.9s | 2543.5s | 46.3s        | 68       | 6       | 7       | 0         | 0                    |
| bs1-r70-4-elixir-2-r0-delegate-a1 | correct          | 1207.9s | 1141.9s | 66s          | 32       | 3       | 4       | 0         | 0                    |
| bs1-r70-4-elixir-2-r0-explore-a1  | correct          | 1243.4s | 1165.8s | 77.6s        | 31       | 3       | 4       | 0         | 0                    |
| bs1-r70-4-elixir-2-r0-off-a1      | correct          | 649.5s  | 619.2s  | 30.3s        | 15       | 1       | 2       | 0         | 0                    |
| bs1-r70-4-go-r0-delegate-a1       | correct          | 1246.3s | 1228.5s | 17.8s        | 32       | 3       | 4       | 0         | 0                    |
| bs1-r70-4-go-r0-explore-a1        | correct          | 696s    | 682.1s  | 13.9s        | 20       | 1       | 2       | 0         | 0                    |
| bs1-r70-4-go-r0-off-a1            | correct          | 2023.8s | 1987.1s | 36.7s        | 49       | 6       | 7       | 0         | 0                    |
| bs1-r70-6-elixir-2-r0-delegate-a1 | correct          | 550.1s  | 525.4s  | 24.7s        | 13       | 0       | 1       | 0         | 0                    |
| bs1-r70-6-elixir-2-r0-explore-a1  | correct          | 543.6s  | 522.9s  | 20.6s        | 12       | 0       | 1       | 0         | 0                    |
| bs1-r70-6-elixir-2-r0-off-a1      | correct          | 344.9s  | 324.3s  | 20.6s        | 13       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
delegate openai: input 2.16M, cached 0.12M, output 61.1k, reasoning 30.1k, input_tokens_details.cache_write_tokens 0, total_tokens 2.22M
explore openai: input 1.76M, cached 0.16M, output 53.5k, reasoning 25.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.82M
off openai: input 2.90M, cached 0.33M, output 86.6k, reasoning 48.4k, input_tokens_details.cache_write_tokens 0, total_tokens 2.98M
native usage by stage and provider:
stage build delegate openai (responses): input 1.33M, cached 0.12M, output 34.4k, reasoning 8.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.36M
stage build explore openai (responses): input 0.87M, cached 0.12M, output 27.8k, reasoning 4.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.90M
stage build off openai (responses): input 1.59M, cached 0.26M, output 44.5k, reasoning 13.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.63M
stage review delegate openai (responses): input 0.83M, cached 0, output 26.7k, reasoning 21.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.86M
stage review explore openai (responses): input 0.89M, cached 47.1k, output 25.7k, reasoning 20.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.92M
stage review off openai (responses): input 1.31M, cached 63.0k, output 42.0k, reasoning 35.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.35M
native usage by attempt and provider:
attempt usage bs1-r70-1-go-r0-delegate-a1 openai (responses): input 1.05M, cached 84.2k, output 25.8k, reasoning 12.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
attempt usage bs1-r70-1-go-r0-explore-a1 openai (responses): input 0.88M, cached 92.2k, output 25.4k, reasoning 13.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.90M
attempt usage bs1-r70-1-go-r0-off-a1 openai (responses): input 1.72M, cached 0.27M, output 43.5k, reasoning 23.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.77M
attempt usage bs1-r70-4-elixir-2-r0-delegate-a1 openai (responses): input 0.49M, cached 31.4k, output 15.6k, reasoning 9.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bs1-r70-4-elixir-2-r0-explore-a1 openai (responses): input 0.48M, cached 28.4k, output 13.8k, reasoning 7.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage bs1-r70-4-elixir-2-r0-off-a1 openai (responses): input 0.18M, cached 0, output 7.9k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage bs1-r70-4-go-r0-delegate-a1 openai (responses): input 0.45M, cached 9.1k, output 14.6k, reasoning 8.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage bs1-r70-4-go-r0-explore-a1 openai (responses): input 0.26M, cached 33.0k, output 9.2k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage bs1-r70-4-go-r0-off-a1 openai (responses): input 0.82M, cached 59.8k, output 30.9k, reasoning 19.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.86M
attempt usage bs1-r70-6-elixir-2-r0-delegate-a1 openai (responses): input 0.17M, cached 0, output 5.0k, reasoning 654, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage bs1-r70-6-elixir-2-r0-explore-a1 openai (responses): input 0.15M, cached 10.1k, output 5.0k, reasoning 753, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage bs1-r70-6-elixir-2-r0-off-a1 openai (responses): input 0.16M, cached 0, output 4.3k, reasoning 643, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt outcomes included: off: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; explore: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; delegate: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 13687.5s, model 13246.2s, tools/checks 441.4s, requests 376
builder settings: off openai gpt-6.1-sol reasoning.effort=medium
builder settings: explore openai gpt-6.1-sol reasoning.effort=medium
builder settings: delegate openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 12, started 12, scored 12, incorrect 0, infrastructure 0, incomplete 0
variant explore differs from off in:
  build.subagents: off -> explore
variant delegate differs from off in:
  build.subagents: off -> delegate
  build.subagents_paths:  -> test/**
B10: exercised in 4 of 4 explore attempts
B10: exercised in 4 of 4 delegate attempts
first position per task: r70-1-go off 0, explore 0, delegate 1 (1 repetitions, 3 variants)
first position per task: r70-4-elixir-2 off 0, explore 0, delegate 1 (1 repetitions, 3 variants)
first position per task: r70-4-go off 0, explore 0, delegate 1 (1 repetitions, 3 variants)
first position per task: r70-6-elixir-2 off 0, explore 1, delegate 0 (1 repetitions, 3 variants)
off: not the Kogen profile (differs in review.effect, review.tools, roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_repairs, stop.max_tokens)
explore: not the Kogen profile (differs in build.subagents, review.effect, review.tools, roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_repairs, stop.max_tokens)
delegate: not the Kogen profile (differs in build.subagents, build.subagents_paths, review.effect, review.tools, roles.build_helper.effort, roles.build_helper.model, roles.build_helper.provider, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
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
explore: build.helper_context = lab_helper (extension)
explore: build.helper_prompt = lab:helper (extension)
explore: build.subagents = explore (extension)
explore: build.subagents_output = 4096 (extension)
explore: build.subagents_turns = 10 (extension)
explore: plan.context = kogen_planner (extension)
explore: plan.prompt = lab:plan (extension)
explore: repair.context = packet,diff,check_results,review_findings (extension)
explore: repair.roles = builder (extension)
explore: review.timing = every_green (extension)
explore: shape.critique_prompt = lab:critique (extension)
explore: shape.critique_rounds = 1 (extension)
explore: shape.helper_context = lab_helper (extension)
explore: shape.helper_prompt = lab:helper (extension)
explore: shape.subagents_output = 4096 (extension)
explore: shape.subagents_turns = 10 (extension)
delegate: build.helper_context = lab_helper (extension)
delegate: build.helper_prompt = lab:helper (extension)
delegate: build.subagents = delegate (extension)
delegate: build.subagents_output = 4096 (extension)
delegate: build.subagents_paths = test/** (extension)
delegate: build.subagents_turns = 10 (extension)
delegate: plan.context = kogen_planner (extension)
delegate: plan.prompt = lab:plan (extension)
delegate: repair.context = packet,diff,check_results,review_findings (extension)
delegate: repair.roles = builder (extension)
delegate: review.timing = every_green (extension)
delegate: shape.critique_prompt = lab:critique (extension)
delegate: shape.critique_rounds = 1 (extension)
delegate: shape.helper_context = lab_helper (extension)
delegate: shape.helper_prompt = lab:helper (extension)
delegate: shape.subagents_output = 4096 (extension)
delegate: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
