complete: 16/16 cells scored
Question: intent-short-1: when the acceptance scenarios carry every tested requirement, does a short intent with no rules keep Kogen's correctness against the full prose?
Hypothesis: exploratory: short holds (no more wrong or stopped attempts)
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| full    | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| short   | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (full)
false success: 0 of 8 claims (short)
shaping outcomes:
full: supplied artifacts (full): representation or builder behavior with supplied artifacts; shaping is not measured
short: supplied artifacts (short): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task        | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|-------------|---------|---------|-----------|------------------|----------------|------------|
| deps-ex     | full    | 2       | 0         | 0                | 0              | 0          |
| deps-ex     | short   | 2       | 0         | 0                | 0              | 0          |
| deps-go     | full    | 2       | 0         | 0                | 0              | 0          |
| deps-go     | short   | 2       | 0         | 0                | 0              | 0          |
| interval-ex | full    | 2       | 0         | 0                | 0              | 0          |
| interval-ex | short   | 2       | 0         | 0                | 0              | 0          |
| interval-go | full    | 2       | 0         | 0                | 0              | 0          |
| interval-go | short   | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: summed stage time, model, tools/checks, requests
| variant | stage | summed stage time | model | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| full    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| full    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| full    | build      | 1619.6s | 1556s   | 63.6s        | 49       |
| full    | verify     | 13.7s   | 0ms     | 13.7s        | 0        |
| full    | review     | 731.4s  | 731.4s  | 0ms          | 35       |
| full    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| full    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| full    | assessment | 0ms     | 0ms     | 0ms          | 0        |
| short   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| short   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| short   | build      | 1593.4s | 1513.2s | 80.2s        | 49       |
| short   | verify     | 11.5s   | 0ms     | 11.5s        | 0        |
| short   | review     | 652.8s  | 652.8s  | 0ms          | 31       |
| short   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| short   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| short   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt | outcome | elapsed time | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| is1-deps-ex-r0-full-a1      | correct | 263.1s | 243.4s | 19.7s        | 10       | 0       | 1       | 0         | 0                    |
| is1-deps-ex-r0-short-a1     | correct | 173.8s | 151.6s | 22.2s        | 10       | 0       | 1       | 0         | 0                    |
| is1-deps-ex-r1-full-a1      | correct | 205.4s | 183.3s | 22.1s        | 11       | 0       | 1       | 0         | 0                    |
| is1-deps-ex-r1-short-a1     | correct | 276.8s | 255.8s | 21s          | 10       | 0       | 1       | 0         | 0                    |
| is1-deps-go-r0-full-a1      | correct | 387.8s | 376.8s | 11s          | 11       | 0       | 1       | 0         | 0                    |
| is1-deps-go-r0-short-a1     | correct | 309.4s | 299.5s | 9.9s         | 10       | 0       | 1       | 0         | 0                    |
| is1-deps-go-r1-full-a1      | correct | 209.9s | 199.5s | 10.4s        | 10       | 0       | 1       | 0         | 0                    |
| is1-deps-go-r1-short-a1     | correct | 288.7s | 278.5s | 10.2s        | 10       | 0       | 1       | 0         | 0                    |
| is1-interval-ex-r0-full-a1  | correct | 333.7s | 317s   | 16.7s        | 11       | 0       | 1       | 0         | 0                    |
| is1-interval-ex-r0-short-a1 | correct | 271.2s | 249.6s | 21.6s        | 9        | 0       | 1       | 0         | 0                    |
| is1-interval-ex-r1-full-a1  | correct | 411.2s | 400.5s | 10.7s        | 11       | 0       | 1       | 0         | 0                    |
| is1-interval-ex-r1-short-a1 | correct | 344.1s | 323.1s | 20.9s        | 10       | 0       | 1       | 0         | 0                    |
| is1-interval-go-r0-full-a1  | correct | 259.2s | 249.2s | 10s          | 10       | 0       | 1       | 0         | 0                    |
| is1-interval-go-r0-short-a1 | correct | 317.2s | 306.5s | 10.7s        | 10       | 0       | 1       | 0         | 0                    |
| is1-interval-go-r1-full-a1  | correct | 330.1s | 317.7s | 12.5s        | 10       | 0       | 1       | 0         | 0                    |
| is1-interval-go-r1-short-a1 | correct | 311s   | 301.4s | 9.6s         | 11       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
full openai: input 1.26M, cached 43.9k, output 32.8k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.29M
short openai: input 1.02M, cached 62.2k, output 27.7k, reasoning 3.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.05M
native usage by stage and provider:
stage build full openai (responses): input 0.56M, cached 43.9k, output 25.6k, reasoning 691, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
stage build short openai (responses): input 0.49M, cached 44.4k, output 21.5k, reasoning 989, input_tokens_details.cache_write_tokens 0, total_tokens 0.52M
stage review full openai (responses): input 0.70M, cached 0, output 7.2k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
stage review short openai (responses): input 0.53M, cached 17.8k, output 6.2k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
native usage by attempt and provider:
attempt usage is1-deps-ex-r0-full-a1 openai (responses): input 0.15M, cached 0, output 3.8k, reasoning 495, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage is1-deps-ex-r0-short-a1 openai (responses): input 0.13M, cached 7.4k, output 3.1k, reasoning 575, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage is1-deps-ex-r1-full-a1 openai (responses): input 0.17M, cached 12.5k, output 4.0k, reasoning 701, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage is1-deps-ex-r1-short-a1 openai (responses): input 0.13M, cached 10.8k, output 2.9k, reasoning 442, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage is1-deps-go-r0-full-a1 openai (responses): input 0.17M, cached 11.8k, output 4.6k, reasoning 535, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage is1-deps-go-r0-short-a1 openai (responses): input 0.13M, cached 0, output 3.9k, reasoning 772, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage is1-deps-go-r1-full-a1 openai (responses): input 0.15M, cached 0, output 4.0k, reasoning 318, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage is1-deps-go-r1-short-a1 openai (responses): input 0.12M, cached 0, output 3.4k, reasoning 508, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage is1-interval-ex-r0-full-a1 openai (responses): input 0.16M, cached 0, output 4.1k, reasoning 438, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage is1-interval-ex-r0-short-a1 openai (responses): input 0.12M, cached 0, output 3.4k, reasoning 278, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage is1-interval-ex-r1-full-a1 openai (responses): input 0.16M, cached 11.1k, output 4.4k, reasoning 440, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage is1-interval-ex-r1-short-a1 openai (responses): input 0.13M, cached 18.9k, output 3.4k, reasoning 276, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage is1-interval-go-r0-full-a1 openai (responses): input 0.15M, cached 8.4k, output 3.9k, reasoning 281, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage is1-interval-go-r0-short-a1 openai (responses): input 0.13M, cached 17.8k, output 3.4k, reasoning 247, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage is1-interval-go-r1-full-a1 openai (responses): input 0.15M, cached 0, output 4.1k, reasoning 301, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage is1-interval-go-r1-short-a1 openai (responses): input 0.14M, cached 7.3k, output 4.2k, reasoning 647, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt outcomes included: full: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; short: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 4692.8s, model 4453.5s, tools/checks 239.3s, requests 164
builder settings: full openai gpt-6.1-sol reasoning.effort=medium; short openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant short differs from full in:
  shape.supplied: full -> short
MODE: exercised in 8 of 8 short attempts
first position per task: deps-ex full 1, short 1 (2 repetitions, 2 variants)
first position per task: deps-go full 1, short 1 (2 repetitions, 2 variants)
first position per task: interval-ex full 1, short 1 (2 repetitions, 2 variants)
first position per task: interval-go full 1, short 1 (2 repetitions, 2 variants)
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
