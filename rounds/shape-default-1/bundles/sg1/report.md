complete: 8/8 cells scored
Question: shape-default-1: with Kogen b2c9876b defaults, does generated shaping by the Sol-high shaper lead to correct builds as often as a supplied Gherkin specification, and at what cost?
Hypothesis: exploratory: generated shaping failed with low-effort shapers; the default Sol-high shaper may make it viable
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant   | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| supplied  | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| generated | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
false success: 0 of 4 claims (supplied)
false success: 0 of 3 claims (generated)
shaping outcomes:
supplied: shaping ready 4, shaping failed 0; correct 4 of 4
generated: shaping ready 3, shaping failed 1 (shaping_failed); correct 3 of 4
## Per-task outcomes
| task           | variant   | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|-----------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | generated | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | generated | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | generated | 0       | 0         | 1                | 0              | 0          |
| r70-6-elixir-2 | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | generated | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant   | stage      | wall    | model   | tools/checks | requests |
|-----------|------------|---------|---------|--------------|----------|
| supplied  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | build      | 474.5s  | 436.4s  | 38.1s        | 34       |
| supplied  | verify     | 11.3s   | 0ms     | 11.3s        | 0        |
| supplied  | review     | 639.2s  | 639.2s  | 0ms          | 35       |
| supplied  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| generated | shape      | 1762.7s | 1762.7s | 0ms          | 37       |
| generated | plan       | 0ms     | 0ms     | 0ms          | 0        |
| generated | build      | 462.5s  | 391.3s  | 71.2s        | 29       |
| generated | verify     | 29.5s   | 0ms     | 29.5s        | 0        |
| generated | review     | 612.5s  | 612.5s  | 0ms          | 29       |
| generated | commit     | 0ms     | 0ms     | 0ms          | 0        |
| generated | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| generated | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                            | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| sg1-r70-1-go-r0-generated-a1       | correct          | 1036.8s | 1000.4s | 36.4s        | 29       | 0       | 1       | 1         | 0                    |
| sg1-r70-1-go-r0-supplied-a1        | correct          | 438.5s  | 415.1s  | 23.4s        | 19       | 0       | 1       | 0         | 0                    |
| sg1-r70-4-elixir-2-r0-generated-a1 | correct          | 715s    | 671.6s  | 43.3s        | 28       | 0       | 1       | 0         | 0                    |
| sg1-r70-4-elixir-2-r0-supplied-a1  | correct          | 281.8s  | 263.2s  | 18.6s        | 19       | 0       | 1       | 0         | 0                    |
| sg1-r70-4-go-r0-generated-a1       | workflow failure | 533.2s  | 527.6s  | 5.6s         | 10       | 0       | 0       | 0         | 0                    |
| sg1-r70-4-go-r0-supplied-a1        | correct          | 258.8s  | 242.7s  | 16.1s        | 15       | 0       | 1       | 0         | 0                    |
| sg1-r70-6-elixir-2-r0-generated-a1 | correct          | 601.1s  | 566.8s  | 34.3s        | 28       | 0       | 1       | 1         | 0                    |
| sg1-r70-6-elixir-2-r0-supplied-a1  | correct          | 170s    | 154.6s  | 15.3s        | 16       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
generated openai: input 1.65M, cached 46.5k, output 0.12M, reasoning 43.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.77M
supplied openai: input 1.05M, cached 85.2k, output 43.1k, reasoning 17.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.09M
native usage by stage and provider:
stage build generated openai (responses): input 0.41M, cached 0, output 14.5k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
stage build supplied openai (responses): input 0.34M, cached 52.0k, output 16.8k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
stage review generated openai (responses): input 0.86M, cached 22.7k, output 25.6k, reasoning 15.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
stage review supplied openai (responses): input 0.71M, cached 33.3k, output 26.4k, reasoning 15.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.74M
stage shape generated openai (responses): input 0.39M, cached 23.8k, output 81.8k, reasoning 25.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
native usage by attempt and provider:
attempt usage sg1-r70-1-go-r0-generated-a1 openai (responses): input 0.67M, cached 6.9k, output 44.7k, reasoning 17.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
attempt usage sg1-r70-1-go-r0-supplied-a1 openai (responses): input 0.38M, cached 22.5k, output 17.8k, reasoning 8.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage sg1-r70-4-elixir-2-r0-generated-a1 openai (responses): input 0.45M, cached 22.7k, output 28.8k, reasoning 12.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt usage sg1-r70-4-elixir-2-r0-supplied-a1 openai (responses): input 0.28M, cached 15.9k, output 10.0k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage sg1-r70-4-go-r0-generated-a1 openai (responses): input 0.12M, cached 10.2k, output 24.8k, reasoning 7.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage sg1-r70-4-go-r0-supplied-a1 openai (responses): input 0.20M, cached 34.8k, output 9.9k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage sg1-r70-6-elixir-2-r0-generated-a1 openai (responses): input 0.41M, cached 6.7k, output 23.7k, reasoning 5.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage sg1-r70-6-elixir-2-r0-supplied-a1 openai (responses): input 0.19M, cached 12.0k, output 5.4k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt outcomes included: supplied: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; generated: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 4035.1s, model 3842s, tools/checks 193.1s, requests 164
builder settings: supplied openai gpt-6.1-sol reasoning.effort=medium
builder settings: generated openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant generated differs from supplied in:
  shape.source: supplied -> generate
  shape.supplied: gherkin -> 
MODE: exercised in 3 of 4 generated attempts
first position per task: r70-1-go supplied 1, generated 0 (1 repetitions, 2 variants)
first position per task: r70-4-elixir-2 supplied 0, generated 1 (1 repetitions, 2 variants)
first position per task: r70-4-go supplied 1, generated 0 (1 repetitions, 2 variants)
first position per task: r70-6-elixir-2 supplied 0, generated 1 (1 repetitions, 2 variants)
supplied: not the Kogen profile (differs in stop.max_command_seconds, stop.max_wall_seconds)
generated: not the Kogen profile (differs in stop.max_command_seconds, stop.max_wall_seconds)
experimental stop: every variant has stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
supplied: build.helper_context = lab_helper (extension)
supplied: build.helper_prompt = lab:helper (extension)
supplied: build.subagents_output = 4096 (extension)
supplied: build.subagents_turns = 10 (extension)
supplied: plan.context = kogen_planner (extension)
supplied: plan.prompt = lab:plan (extension)
supplied: repair.context = packet,diff,check_results,review_findings (extension)
supplied: repair.roles = builder (extension)
supplied: review.timing = every_green (extension)
supplied: shape.critique_prompt = lab:critique (extension)
supplied: shape.critique_rounds = 1 (extension)
supplied: shape.helper_context = lab_helper (extension)
supplied: shape.helper_prompt = lab:helper (extension)
supplied: shape.subagents_output = 4096 (extension)
supplied: shape.subagents_turns = 10 (extension)
generated: build.helper_context = lab_helper (extension)
generated: build.helper_prompt = lab:helper (extension)
generated: build.subagents_output = 4096 (extension)
generated: build.subagents_turns = 10 (extension)
generated: plan.context = kogen_planner (extension)
generated: plan.prompt = lab:plan (extension)
generated: repair.context = packet,diff,check_results,review_findings (extension)
generated: repair.roles = builder (extension)
generated: review.timing = every_green (extension)
generated: shape.critique_prompt = lab:critique (extension)
generated: shape.critique_rounds = 1 (extension)
generated: shape.helper_context = lab_helper (extension)
generated: shape.helper_prompt = lab:helper (extension)
generated: shape.subagents_output = 4096 (extension)
generated: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
