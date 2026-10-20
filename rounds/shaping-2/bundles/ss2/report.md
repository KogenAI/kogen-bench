incomplete: 15 of 16 cells scored
Question: shaping-2: with Kogen b45ba32b's shaping, does generated shaping lead to correct builds as often as a supplied specification, and does a shaper helper (hint or required) change that or its cost?
Hypothesis: exploratory: generated shaping is viable with Sol high (shape-default-1, Lab-only); a helper may cut shaping retries
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (15 of 16 cells scored)
## CMP-1 Correctness
| variant   | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| generated | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| supplied  | 3       | 0         | 0                | 1              | 0          | 100%         | 0 of 3        | 0           |
| hint      | 3       | 1         | 0                | 1              | 0          | 75%          | 1 of 4        | 0           |
| required  | 2       | 2         | 0                | 0              | 0          | 50%          | 2 of 4        | 0           |
false success: 0 of 4 claims (generated)
false success: 0 of 3 claims (supplied)
false success: 1 of 4 claims (hint)
false success: 2 of 4 claims (required)
shaping outcomes:
generated: shaping ready 4, shaping failed 0; correct 4 of 4
supplied: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
hint: shaping ready 4, shaping failed 0; correct 3 of 4
required: shaping ready 4, shaping failed 0; correct 2 of 4
## Per-task outcomes
| task           | variant   | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|-----------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | generated | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | hint      | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | required  | 0       | 1         | 0                | 0              | 0          |
| r70-4-elixir-2 | generated | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | hint      | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | required  | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | generated | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | supplied  | 0       | 0         | 0                | 1              | 0          |
| r70-4-go       | hint      | 1       | 0         | 0                | 1              | 0          |
| r70-4-go       | required  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | generated | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | supplied  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | hint      | 0       | 1         | 0                | 0              | 0          |
| r70-6-elixir-2 | required  | 0       | 1         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant   | stage      | wall    | model   | tools/checks | requests |
|-----------|------------|---------|---------|--------------|----------|
| generated | shape      | 2049.4s | 2049.4s | 0ms          | 47       |
| generated | plan       | 0ms     | 0ms     | 0ms          | 0        |
| generated | build      | 611.5s  | 483.7s  | 127.7s       | 37       |
| generated | verify     | 29.1s   | 0ms     | 29.1s        | 0        |
| generated | review     | 721.5s  | 721.5s  | 0ms          | 38       |
| generated | commit     | 0ms     | 0ms     | 0ms          | 0        |
| generated | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| generated | assessment | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | build      | 594.4s  | 529.1s  | 65.3s        | 38       |
| supplied  | verify     | 12.7s   | 0ms     | 12.7s        | 0        |
| supplied  | review     | 654.2s  | 654.2s  | 0ms          | 32       |
| supplied  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| supplied  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| hint      | shape      | 2326s   | 2326s   | 0ms          | 54       |
| hint      | plan       | 0ms     | 0ms     | 0ms          | 0        |
| hint      | build      | 668.1s  | 588.4s  | 79.7s        | 42       |
| hint      | verify     | 34.8s   | 0ms     | 34.8s        | 0        |
| hint      | review     | 1173s   | 1173s   | 0ms          | 43       |
| hint      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| hint      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| hint      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| required  | shape      | 2790s   | 2790s   | 0ms          | 61       |
| required  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| required  | build      | 681.3s  | 598.9s  | 82.4s        | 41       |
| required  | verify     | 26.8s   | 0ms     | 26.8s        | 0        |
| required  | review     | 562s    | 562s    | 0ms          | 29       |
| required  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| required  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| required  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                            | outcome        | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------|----------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| ss2-r70-1-go-r0-generated-a1       | correct        | 1090.5s | 1064.3s | 26.2s        | 31       | 0       | 1       | 0         | 0                    |
| ss2-r70-1-go-r0-hint-a1            | correct        | 1656.7s | 1601.5s | 55.2s        | 39       | 0       | 1       | 0         | 0                    |
| ss2-r70-1-go-r0-required-a1        | incorrect      | 1559.6s | 1530.3s | 29.3s        | 55       | 1       | 1       | 0         | 0                    |
| ss2-r70-1-go-r0-supplied-a1        | correct        | 594.2s  | 556s    | 38.2s        | 25       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-elixir-2-r0-generated-a1 | correct        | 742.8s  | 688.3s  | 54.5s        | 28       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-elixir-2-r0-hint-a1      | correct        | 795.6s  | 765.4s  | 30.3s        | 34       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-elixir-2-r0-required-a1  | correct        | 870.8s  | 818.4s  | 52.4s        | 34       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-elixir-2-r0-supplied-a1  | correct        | 276.2s  | 251.3s  | 24.9s        | 16       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-go-r0-generated-a1       | correct        | 952.2s  | 894.3s  | 57.9s        | 34       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-go-r0-hint-a1            | infrastructure | 171.5s  | 167.6s  | 3.9s         | 12       | 0       | 0       | 0         | 0                    |
| ss2-r70-4-go-r0-hint-a2            | correct        | 772.4s  | 745.8s  | 26.6s        | 31       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-go-r0-required-a1        | correct        | 864.4s  | 831.2s  | 33.2s        | 31       | 0       | 1       | 0         | 0                    |
| ss2-r70-4-go-r0-supplied-a1        | infrastructure | 197.1s  | 183.5s  | 13.7s        | 13       | 0       | 0       | 0         | 0                    |
| ss2-r70-6-elixir-2-r0-generated-a1 | correct        | 639.8s  | 607.7s  | 32s          | 29       | 0       | 1       | 0         | 0                    |
| ss2-r70-6-elixir-2-r0-hint-a1      | incorrect      | 957.6s  | 938.4s  | 19.1s        | 36       | 1       | 1       | 0         | 0                    |
| ss2-r70-6-elixir-2-r0-required-a1  | incorrect      | 942.4s  | 931.9s  | 10.5s        | 33       | 0       | 1       | 0         | 0                    |
| ss2-r70-6-elixir-2-r0-supplied-a1  | correct        | 208s    | 192.5s  | 15.5s        | 16       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
generated openai: input 2.20M, cached 0.17M, output 0.12M, reasoning 32.7k, input_tokens_details.cache_write_tokens 0, total_tokens 2.33M
hint openai: input 2.78M, cached 0.15M, output 0.16M, reasoning 51.7k, input_tokens_details.cache_write_tokens 0, total_tokens 2.94M
required openai: input 2.49M, cached 0.11M, output 0.16M, reasoning 37.6k, input_tokens_details.cache_write_tokens 0, total_tokens 2.65M
supplied openai: input 1.03M, cached 28.5k, output 37.9k, reasoning 13.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
native usage by stage and provider:
stage build generated openai (responses): input 0.47M, cached 19.3k, output 15.7k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
stage build hint openai (responses): input 0.62M, cached 21.0k, output 19.5k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.63M
stage build required openai (responses): input 0.64M, cached 0, output 18.6k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.66M
stage build supplied openai (responses): input 0.37M, cached 28.5k, output 16.6k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
stage review generated openai (responses): input 0.96M, cached 0.12M, output 22.2k, reasoning 11.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.98M
stage review hint openai (responses): input 1.40M, cached 41.9k, output 40.3k, reasoning 25.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.44M
stage review required openai (responses): input 0.74M, cached 15.9k, output 17.8k, reasoning 10.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.76M
stage review supplied openai (responses): input 0.66M, cached 0, output 21.3k, reasoning 11.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.68M
stage shape generated openai (responses): input 0.77M, cached 33.8k, output 86.6k, reasoning 19.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.86M
stage shape hint openai (responses): input 0.73M, cached 86.8k, output 97.7k, reasoning 23.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.83M
stage shape required openai (responses): input 1.08M, cached 90.0k, output 0.12M, reasoning 25.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.19M
stage subagent:shape_helper hint openai (responses): input 22.6k, cached 0, output 4.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 26.7k
stage subagent:shape_helper required openai (responses): input 29.4k, cached 0, output 3.1k, reasoning 484, input_tokens_details.cache_write_tokens 0, total_tokens 32.5k
native usage by attempt and provider:
attempt usage ss2-r70-1-go-r0-generated-a1 openai (responses): input 0.68M, cached 52.4k, output 41.7k, reasoning 10.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
attempt usage ss2-r70-1-go-r0-hint-a1 openai (responses): input 1.13M, cached 21.5k, output 63.5k, reasoning 25.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.19M
attempt usage ss2-r70-1-go-r0-required-a1 openai (responses): input 1.02M, cached 40.3k, output 57.3k, reasoning 15.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.08M
attempt usage ss2-r70-1-go-r0-supplied-a1 openai (responses): input 0.52M, cached 22.5k, output 18.5k, reasoning 7.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
attempt usage ss2-r70-4-elixir-2-r0-generated-a1 openai (responses): input 0.43M, cached 33.9k, output 26.5k, reasoning 9.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage ss2-r70-4-elixir-2-r0-hint-a1 openai (responses): input 0.51M, cached 31.2k, output 29.4k, reasoning 9.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
attempt usage ss2-r70-4-elixir-2-r0-required-a1 openai (responses): input 0.47M, cached 30.2k, output 30.6k, reasoning 6.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage ss2-r70-4-elixir-2-r0-supplied-a1 openai (responses): input 0.21M, cached 0, output 8.3k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage ss2-r70-4-go-r0-generated-a1 openai (responses): input 0.63M, cached 46.2k, output 32.4k, reasoning 9.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.66M
attempt usage ss2-r70-4-go-r0-hint-a1 openai (responses): input 58.2k, cached 0, output 5.7k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 63.8k
attempt usage ss2-r70-4-go-r0-hint-a2 openai (responses): input 0.40M, cached 32.6k, output 25.7k, reasoning 8.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage ss2-r70-4-go-r0-required-a1 openai (responses): input 0.41M, cached 5.0k, output 30.9k, reasoning 8.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage ss2-r70-4-go-r0-supplied-a1 openai (responses): input 0.13M, cached 0, output 5.1k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ss2-r70-6-elixir-2-r0-generated-a1 openai (responses): input 0.46M, cached 38.1k, output 23.9k, reasoning 4.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt usage ss2-r70-6-elixir-2-r0-hint-a1 openai (responses): input 0.68M, cached 64.3k, output 37.3k, reasoning 7.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
attempt usage ss2-r70-6-elixir-2-r0-required-a1 openai (responses): input 0.59M, cached 30.3k, output 37.9k, reasoning 6.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
attempt usage ss2-r70-6-elixir-2-r0-supplied-a1 openai (responses): input 0.17M, cached 6.0k, output 6.0k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
subagent use:
hint: mean 0.60 calls per attempt, 3 of 5 attempts (60%) with at least one call; helper tokens openai (responses): input 22.6k, cached 0, output 4.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 26.7k
required: mean 1.25 calls per attempt, 4 of 4 attempts (100%) with at least one call; helper tokens openai (responses): input 29.4k, cached 0, output 3.1k, reasoning 484, input_tokens_details.cache_write_tokens 0, total_tokens 32.5k
attempt outcomes included: generated: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; supplied: correct 3, incorrect 0, workflow failure 0, infrastructure 1, incomplete 0; hint: correct 3, incorrect 1, workflow failure 0, infrastructure 1, incomplete 0; required: correct 2, incorrect 2, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 13291.8s, model 12768.5s, tools/checks 523.4s, requests 497
builder settings: generated openai gpt-6.1-sol reasoning.effort=medium; supplied openai gpt-6.1-sol reasoning.effort=medium; hint openai gpt-6.1-sol reasoning.effort=medium; required openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 16, started 17, scored 15, incorrect 3, infrastructure 2, incomplete 0
variant supplied differs from generated in:
  shape.source: generate -> supplied
  shape.supplied:  -> gherkin
variant hint differs from generated in:
  shape.subagents: off -> explore
  shape.subagents_guidance: none -> hint
variant required differs from generated in:
  shape.subagents: off -> explore
  shape.subagents_guidance: none -> hint
  shape.subagents_required: false -> true
MODE: exercised in 4 of 4 supplied attempts
S11: exercised in 5 of 5 hint attempts
S12: exercised in 5 of 5 hint attempts
S11: exercised in 4 of 4 required attempts
S12: exercised in 4 of 4 required attempts
first position per task: r70-1-go generated 0, supplied 1, hint 0, required 0 (1 repetitions, 4 variants)
first position per task: r70-4-elixir-2 generated 0, supplied 0, hint 0, required 1 (1 repetitions, 4 variants)
first position per task: r70-4-go generated 0, supplied 0, hint 1, required 0 (1 repetitions, 4 variants)
first position per task: r70-6-elixir-2 generated 0, supplied 1, hint 0, required 0 (1 repetitions, 4 variants)
generated: not the Kogen profile (differs in roles.shape_helper.effort, roles.shape_helper.model, roles.shape_helper.provider, stop.max_command_seconds, stop.max_wall_seconds)
supplied: not the Kogen profile (differs in roles.shape_helper.effort, roles.shape_helper.model, roles.shape_helper.provider, stop.max_command_seconds, stop.max_wall_seconds)
hint: not the Kogen profile (differs in roles.shape_helper.effort, roles.shape_helper.model, roles.shape_helper.provider, shape.subagents, shape.subagents_guidance, stop.max_command_seconds, stop.max_wall_seconds)
required: not the Kogen profile (differs in roles.shape_helper.effort, roles.shape_helper.model, roles.shape_helper.provider, shape.subagents, shape.subagents_guidance, shape.subagents_required, stop.max_command_seconds, stop.max_wall_seconds)
experimental stop: every variant has stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
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
hint: build.helper_context = lab_helper (extension)
hint: build.helper_prompt = lab:helper (extension)
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
hint: shape.subagents = explore (extension)
hint: shape.subagents_guidance = hint (extension)
hint: shape.subagents_output = 4096 (extension)
hint: shape.subagents_turns = 10 (extension)
required: build.helper_context = lab_helper (extension)
required: build.helper_prompt = lab:helper (extension)
required: build.subagents_output = 4096 (extension)
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
required: shape.subagents = explore (extension)
required: shape.subagents_guidance = hint (extension)
required: shape.subagents_output = 4096 (extension)
required: shape.subagents_required = true (extension)
required: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
