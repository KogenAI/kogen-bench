complete: 12/12 cells scored
Question: confirm-intent-short-1: on fresh tasks whose acceptance scenarios carry every tested requirement, is a short intent correct in at least as many blocks as the full prose, with no more wrong submissions and no more wrong first-green builds?
Hypothesis: short is correct in at least as many paired blocks as full, with no more wrong submissions or wrong first-green builds
Purpose: confirmation
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| full    | 6       | 0         | 0                | 0              | 0          | 100%         | 0 of 6        | 0           |
| short   | 6       | 0         | 0                | 0              | 0          | 100%         | 0 of 6        | 0           |
false success: 0 of 6 claims (full)
false success: 0 of 6 claims (short)
shaping outcomes:
full: supplied artifacts (full): representation or builder behavior with supplied artifacts; shaping is not measured
short: supplied artifacts (short): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task      | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|---------|---------|-----------|------------------|----------------|------------|
| subnet-ex | full    | 3       | 0         | 0                | 0              | 0          |
| subnet-ex | short   | 3       | 0         | 0                | 0              | 0          |
| subnet-go | full    | 3       | 0         | 0                | 0              | 0          |
| subnet-go | short   | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: summed stage time, model, tools/checks, requests
| variant | stage | summed stage time | model | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| full    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| full    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| full    | build      | 1455.6s | 1412s   | 43.6s        | 36       |
| full    | verify     | 9.6s    | 0ms     | 9.6s         | 0        |
| full    | review     | 538.9s  | 538.9s  | 0ms          | 27       |
| full    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| full    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| full    | assessment | 0ms     | 0ms     | 0ms          | 0        |
| short   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| short   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| short   | build      | 1376.4s | 1316.6s | 59.7s        | 35       |
| short   | verify     | 9.1s    | 0ms     | 9.1s         | 0        |
| short   | review     | 410.4s  | 410.4s  | 0ms          | 25       |
| short   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| short   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| short   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt | outcome | elapsed time | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cis1-subnet-ex-r0-full-a1  | correct | 373.2s | 361s   | 12.2s        | 11       | 0       | 1       | 0         | 0                    |
| cis1-subnet-ex-r0-short-a1 | correct | 298.7s | 274.2s | 24.5s        | 10       | 0       | 1       | 0         | 0                    |
| cis1-subnet-ex-r1-full-a1  | correct | 315.1s | 291.6s | 23.5s        | 11       | 0       | 1       | 0         | 0                    |
| cis1-subnet-ex-r1-short-a1 | correct | 294.8s | 271.1s | 23.7s        | 12       | 0       | 1       | 0         | 0                    |
| cis1-subnet-ex-r2-full-a1  | correct | 296.1s | 272.8s | 23.4s        | 11       | 0       | 1       | 0         | 0                    |
| cis1-subnet-ex-r2-short-a1 | correct | 290.5s | 270.2s | 20.3s        | 9        | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r0-full-a1  | correct | 415.8s | 406.3s | 9.6s         | 10       | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r0-short-a1 | correct | 242.4s | 232.4s | 10s          | 9        | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r1-full-a1  | correct | 292.8s | 285.9s | 7s           | 9        | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r1-short-a1 | correct | 369.7s | 357.7s | 12s          | 10       | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r2-full-a1  | correct | 345.3s | 333.4s | 11.8s        | 11       | 0       | 1       | 0         | 0                    |
| cis1-subnet-go-r2-short-a1 | correct | 334.1s | 321.4s | 12.7s        | 10       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
full openai: input 1.06M, cached 40.8k, output 26.6k, reasoning 2.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.09M
short openai: input 0.87M, cached 37.2k, output 22.6k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
native usage by stage and provider:
stage build full openai (responses): input 0.45M, cached 40.8k, output 20.5k, reasoning 359, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
stage build short openai (responses): input 0.39M, cached 37.2k, output 18.9k, reasoning 328, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
stage review full openai (responses): input 0.61M, cached 0, output 6.1k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
stage review short openai (responses): input 0.48M, cached 0, output 3.8k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
native usage by attempt and provider:
attempt usage cis1-subnet-ex-r0-full-a1 openai (responses): input 0.18M, cached 0, output 4.5k, reasoning 479, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cis1-subnet-ex-r0-short-a1 openai (responses): input 0.14M, cached 0, output 3.8k, reasoning 501, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage cis1-subnet-ex-r1-full-a1 openai (responses): input 0.17M, cached 11.3k, output 4.5k, reasoning 778, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cis1-subnet-ex-r1-short-a1 openai (responses): input 0.18M, cached 8.1k, output 3.9k, reasoning 223, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cis1-subnet-ex-r2-full-a1 openai (responses): input 0.18M, cached 9.9k, output 4.5k, reasoning 340, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cis1-subnet-ex-r2-short-a1 openai (responses): input 0.13M, cached 0, output 3.4k, reasoning 374, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage cis1-subnet-go-r0-full-a1 openai (responses): input 0.18M, cached 9.9k, output 4.5k, reasoning 295, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cis1-subnet-go-r0-short-a1 openai (responses): input 0.13M, cached 9.5k, output 3.2k, reasoning 268, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage cis1-subnet-go-r1-full-a1 openai (responses): input 0.16M, cached 9.9k, output 4.1k, reasoning 280, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cis1-subnet-go-r1-short-a1 openai (responses): input 0.15M, cached 0, output 3.9k, reasoning 259, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage cis1-subnet-go-r2-full-a1 openai (responses): input 0.18M, cached 0, output 4.6k, reasoning 492, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cis1-subnet-go-r2-short-a1 openai (responses): input 0.15M, cached 19.7k, output 4.4k, reasoning 232, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt outcomes included: full: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; short: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 3868.6s, model 3678s, tools/checks 190.6s, requests 123
builder settings: full openai gpt-6.1-sol reasoning.effort=medium; short openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 12, started 12, scored 12, incorrect 0, infrastructure 0, incomplete 0
variant short differs from full in:
  shape.supplied: full -> short
MODE: exercised in 6 of 6 short attempts
first position per task: subnet-ex full 1, short 2 (3 repetitions, 2 variants)
first position per task: subnet-go full 2, short 1 (3 repetitions, 2 variants)
full: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
short: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
full: build.helper_context = lab_helper (extension)
full: build.helper_prompt = lab:helper (extension)
full: build.subagents_output = 4096 (extension)
full: build.subagents_turns = 10 (extension)
full: plan.context = kogen_planner (extension)
full: plan.prompt = lab:plan (extension)
full: repair.context = packet,diff,check_results,review_findings (extension)
full: repair.roles = builder (extension)
full: review.timing = every_green (extension)
full: shape.critique_prompt = lab:critique (extension)
full: shape.critique_rounds = 1 (extension)
full: shape.helper_context = lab_helper (extension)
full: shape.helper_prompt = lab:helper (extension)
full: shape.subagents_output = 4096 (extension)
full: shape.subagents_turns = 10 (extension)
short: build.helper_context = lab_helper (extension)
short: build.helper_prompt = lab:helper (extension)
short: build.subagents_output = 4096 (extension)
short: build.subagents_turns = 10 (extension)
short: plan.context = kogen_planner (extension)
short: plan.prompt = lab:plan (extension)
short: repair.context = packet,diff,check_results,review_findings (extension)
short: repair.roles = builder (extension)
short: review.timing = every_green (extension)
short: shape.critique_prompt = lab:critique (extension)
short: shape.critique_rounds = 1 (extension)
short: shape.helper_context = lab_helper (extension)
short: shape.helper_prompt = lab:helper (extension)
short: shape.subagents_output = 4096 (extension)
short: shape.subagents_turns = 10 (extension)
