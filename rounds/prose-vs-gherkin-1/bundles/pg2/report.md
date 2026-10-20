complete: 8/8 cells scored
Question: prose-vs-gherkin-1 run 2: with a weak builder and complete prose, do Gherkin scenarios reduce wrong or stopped attempts under Kogen's defaults?
Hypothesis: exploratory: the prose arm has more wrong or stopped attempts
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| gherkin | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| prose   | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (gherkin)
false success: 0 of 4 claims (prose)
shaping outcomes:
gherkin: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
prose: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| r70-4-go     | gherkin | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | prose   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | gherkin | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | prose   | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | gherkin | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | prose   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | gherkin | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | prose   | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant | stage      | elapsed time   | model  | tools/checks | requests |
|---------|------------|--------|--------|--------------|----------|
| gherkin | shape      | 0ms    | 0ms    | 0ms          | 0        |
| gherkin | plan       | 0ms    | 0ms    | 0ms          | 0        |
| gherkin | build      | 484.8s | 413.1s | 71.7s        | 34       |
| gherkin | verify     | 27.7s  | 0ms    | 27.7s        | 0        |
| gherkin | review     | 795s   | 795s   | 0ms          | 40       |
| gherkin | commit     | 0ms    | 0ms    | 0ms          | 0        |
| gherkin | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| gherkin | assessment | 0ms    | 0ms    | 0ms          | 0        |
| prose   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| prose   | plan       | 0ms    | 0ms    | 0ms          | 0        |
| prose   | build      | 528.1s | 445.2s | 82.9s        | 40       |
| prose   | verify     | 31.4s  | 0ms    | 31.4s        | 0        |
| prose   | review     | 865.6s | 865.6s | 0ms          | 39       |
| prose   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| prose   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| prose   | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                        | outcome | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| pg2-r70-4-go-r0-gherkin-a1     | correct | 348.4s | 299.8s | 48.6s        | 20       | 0       | 1       | 0         | 0                    |
| pg2-r70-4-go-r0-prose-a1       | correct | 398.4s | 335.4s | 63s          | 16       | 0       | 1       | 0         | 0                    |
| pg2-r70-5-go-r0-gherkin-a1     | correct | 354s   | 341.2s | 12.7s        | 20       | 0       | 1       | 0         | 0                    |
| pg2-r70-5-go-r0-prose-a1       | correct | 306.5s | 290.1s | 16.4s        | 19       | 0       | 1       | 0         | 0                    |
| pg2-r70-7-elixir-r0-gherkin-a1 | correct | 327.7s | 282.3s | 45.4s        | 19       | 0       | 1       | 0         | 0                    |
| pg2-r70-7-elixir-r0-prose-a1   | correct | 342.6s | 308.7s | 33.9s        | 21       | 1       | 1       | 0         | 0                    |
| pg2-r70-7-go-r0-gherkin-a1     | correct | 294.8s | 284.8s | 10s          | 15       | 0       | 1       | 0         | 0                    |
| pg2-r70-7-go-r0-prose-a1       | correct | 392.6s | 376.6s | 16s          | 23       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
gherkin openai: input 0.98M, cached 0.10M, output 46.1k, reasoning 8.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.03M
prose openai: input 0.89M, cached 88.3k, output 51.6k, reasoning 10.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.94M
native usage by stage and provider:
stage build gherkin openai (responses): input 0.29M, cached 37.1k, output 15.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
stage build prose openai (responses): input 0.30M, cached 60.8k, output 16.4k, reasoning 215, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
stage review gherkin openai (responses): input 0.69M, cached 65.2k, output 30.9k, reasoning 8.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
stage review prose openai (responses): input 0.59M, cached 27.5k, output 35.2k, reasoning 10.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
native usage by attempt and provider:
attempt usage pg2-r70-4-go-r0-gherkin-a1 openai (responses): input 0.31M, cached 33.3k, output 11.2k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage pg2-r70-4-go-r0-prose-a1 openai (responses): input 0.17M, cached 14.2k, output 13.7k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage pg2-r70-5-go-r0-gherkin-a1 openai (responses): input 0.25M, cached 27.6k, output 13.2k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage pg2-r70-5-go-r0-prose-a1 openai (responses): input 0.21M, cached 0, output 11.0k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage pg2-r70-7-elixir-r0-gherkin-a1 openai (responses): input 0.23M, cached 29.4k, output 10.2k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage pg2-r70-7-elixir-r0-prose-a1 openai (responses): input 0.23M, cached 28.9k, output 11.9k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage pg2-r70-7-go-r0-gherkin-a1 openai (responses): input 0.19M, cached 11.9k, output 11.5k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage pg2-r70-7-go-r0-prose-a1 openai (responses): input 0.28M, cached 45.2k, output 15.0k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt outcomes included: gherkin: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; prose: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2765s, model 2518.9s, tools/checks 246.1s, requests 153
builder settings: gherkin openai gpt-6-luna reasoning.effort=low; prose openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant prose differs from gherkin in:
  artifacts.gherkin: executed -> off
  shape.supplied: gherkin -> prose
A03: exercised in 4 of 4 prose attempts
MODE: exercised in 4 of 4 prose attempts
first position per task: r70-4-go gherkin 1, prose 0 (1 repetitions, 2 variants)
first position per task: r70-5-go gherkin 1, prose 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir gherkin 1, prose 0 (1 repetitions, 2 variants)
first position per task: r70-7-go gherkin 1, prose 0 (1 repetitions, 2 variants)
gherkin: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
prose: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
gherkin: build.helper_context = lab_helper (extension)
gherkin: build.helper_prompt = lab:helper (extension)
gherkin: build.subagents_output = 4096 (extension)
gherkin: build.subagents_turns = 10 (extension)
gherkin: plan.context = kogen_planner (extension)
gherkin: plan.prompt = lab:plan (extension)
gherkin: repair.context = packet,diff,check_results,review_findings (extension)
gherkin: repair.roles = builder (extension)
gherkin: review.timing = every_green (extension)
gherkin: shape.critique_prompt = lab:critique (extension)
gherkin: shape.critique_rounds = 1 (extension)
gherkin: shape.helper_context = lab_helper (extension)
gherkin: shape.helper_prompt = lab:helper (extension)
gherkin: shape.subagents_output = 4096 (extension)
gherkin: shape.subagents_turns = 10 (extension)
prose: build.helper_context = lab_helper (extension)
prose: build.helper_prompt = lab:helper (extension)
prose: build.subagents_output = 4096 (extension)
prose: build.subagents_turns = 10 (extension)
prose: plan.context = kogen_planner (extension)
prose: plan.prompt = lab:plan (extension)
prose: repair.context = packet,diff,check_results,review_findings (extension)
prose: repair.roles = builder (extension)
prose: review.timing = every_green (extension)
prose: shape.critique_prompt = lab:critique (extension)
prose: shape.critique_rounds = 1 (extension)
prose: shape.helper_context = lab_helper (extension)
prose: shape.helper_prompt = lab:helper (extension)
prose: shape.subagents_output = 4096 (extension)
prose: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
