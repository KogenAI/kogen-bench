incomplete: 7 of 8 cells scored
Question: mechanism-split-1 run 2b (second repetition, review-fix-2 tasks): with a weak builder, is the new flow's advantage over the earlier flow due to review-and-fix (vs builder repairs on review findings) or to stopping verification at the first failed gate (vs running all checks)?
Hypothesis: exploratory: review-and-fix carries most of the advantage; verification stopping early changes cost more than correctness
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (7 of 8 cells scored)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| new        | 2       | 0         | 1                | 1              | 0          | 66.7%        | 0 of 2        | 0           |
| old-review | 1       | 0         | 3                | 0              | 0          | 25%          | 0 of 1        | 1           |
false success: 0 of 2 claims (new)
false success: 0 of 1 claims (old-review)
shaping outcomes:
new: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
old-review: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | new        | 0       | 0         | 0                | 1              | 0          |
| r70-1-go       | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | new        | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-4-go       | new        | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | old-review | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | new        | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | old-review | 0       | 0         | 1                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| new        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| new        | plan       | 0ms     | 0ms     | 0ms          | 0        |
| new        | build      | 2446.9s | 2387.3s | 59.6s        | 63       |
| new        | verify     | 7.1s    | 0ms     | 7.1s         | 0        |
| new        | review     | 378.9s  | 378.9s  | 0ms          | 22       |
| new        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| new        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| new        | assessment | 0ms     | 0ms     | 0ms          | 0        |
| old-review | shape      | 0ms     | 0ms     | 0ms          | 0        |
| old-review | plan       | 0ms     | 0ms     | 0ms          | 0        |
| old-review | build      | 1087.2s | 1030.3s | 56.8s        | 88       |
| old-review | verify     | 24.5s   | 0ms     | 24.5s        | 0        |
| old-review | review     | 1182.6s | 1182.6s | 0ms          | 60       |
| old-review | commit     | 0ms     | 0ms     | 0ms          | 0        |
| old-review | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| old-review | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| ms2b-r70-1-go-r0-new-a1              | infrastructure   | 22.4s   | 14.5s   | 7.9s         | 3        | 0       | 0       | 0         | 0                    |
| ms2b-r70-1-go-r0-old-review-a1       | workflow failure | 774.7s  | 759.6s  | 15.1s        | 46       | 6       | 5       | 0         | 0                    |
| ms2b-r70-4-elixir-2-r0-new-a1        | workflow failure | 1108.3s | 1089.4s | 18.9s        | 23       | 4       | 0       | 0         | 0                    |
| ms2b-r70-4-elixir-2-r0-old-review-a1 | workflow failure | 737.3s  | 666.7s  | 70.6s        | 47       | 6       | 6       | 0         | 0                    |
| ms2b-r70-4-go-r0-new-a1              | correct          | 304.9s  | 293.7s  | 11.3s        | 19       | 3       | 1       | 0         | 0                    |
| ms2b-r70-4-go-r0-old-review-a1       | correct          | 512s    | 501.3s  | 10.7s        | 30       | 4       | 5       | 0         | 0                    |
| ms2b-r70-6-elixir-2-r0-new-a1        | correct          | 1426.3s | 1368.6s | 57.8s        | 40       | 4       | 1       | 0         | 0                    |
| ms2b-r70-6-elixir-2-r0-old-review-a1 | workflow failure | 302.1s  | 285.3s  | 16.8s        | 25       | 6       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
new openai: input 1.29M, cached 0.32M, output 31.1k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.32M
old-review openai: input 2.39M, cached 0.38M, output 69.2k, reasoning 25.6k, input_tokens_details.cache_write_tokens 0, total_tokens 2.46M
native usage by stage and provider:
stage build new openai (responses): input 0.87M, cached 0.31M, output 17.5k, reasoning 345, input_tokens_details.cache_write_tokens 0, total_tokens 0.88M
stage build old-review openai (responses): input 1.37M, cached 0.37M, output 34.0k, reasoning 103, input_tokens_details.cache_write_tokens 0, total_tokens 1.40M
stage review new openai (responses): input 0.42M, cached 13.7k, output 13.6k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
stage review old-review openai (responses): input 1.02M, cached 15.1k, output 35.2k, reasoning 25.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
native usage by attempt and provider:
attempt usage ms2b-r70-1-go-r0-new-a1 openai (responses): input 12.0k, cached 5.6k, output 109, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 12.2k
attempt usage ms2b-r70-1-go-r0-old-review-a1 openai (responses): input 0.81M, cached 0.16M, output 24.2k, reasoning 8.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.83M
attempt usage ms2b-r70-4-elixir-2-r0-new-a1 openai (responses): input 0.25M, cached 78.3k, output 4.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage ms2b-r70-4-elixir-2-r0-old-review-a1 openai (responses): input 0.69M, cached 0.13M, output 19.9k, reasoning 9.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
attempt usage ms2b-r70-4-go-r0-new-a1 openai (responses): input 0.22M, cached 20.7k, output 10.3k, reasoning 2.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage ms2b-r70-4-go-r0-old-review-a1 openai (responses): input 0.40M, cached 6.7k, output 16.2k, reasoning 7.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage ms2b-r70-6-elixir-2-r0-new-a1 openai (responses): input 0.81M, cached 0.22M, output 15.8k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.82M
attempt usage ms2b-r70-6-elixir-2-r0-old-review-a1 openai (responses): input 0.50M, cached 85.6k, output 9.0k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt outcomes included: new: correct 2, incorrect 0, workflow failure 1, infrastructure 1, incomplete 0; old-review: correct 1, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5188.3s, model 4979.1s, tools/checks 209.2s, requests 233
builder settings: new openai gpt-6-luna reasoning.effort=low; old-review openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 7, incorrect 0, infrastructure 1, incomplete 0
variant old-review differs from new in:
  review.context: kogen_reviewer -> kogen_reviewer_fd0cdcfb
  review.effect: stop -> builder_repair
  review.tools: fix -> read_only
C03: exercised in 4 of 4 old-review attempts
review.effect: not exercised
C09: exercised in 4 of 4 old-review attempts
first position per task: r70-1-go new 1, old-review 0 (1 repetitions, 2 variants)
first position per task: r70-4-elixir-2 new 1, old-review 0 (1 repetitions, 2 variants)
first position per task: r70-4-go new 0, old-review 1 (1 repetitions, 2 variants)
first position per task: r70-6-elixir-2 new 0, old-review 1 (1 repetitions, 2 variants)
new: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
old-review: not the Kogen profile (differs in review.context, review.effect, review.tools, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
new: build.helper_context = lab_helper (extension)
new: build.helper_prompt = lab:helper (extension)
new: build.subagents_output = 4096 (extension)
new: build.subagents_turns = 10 (extension)
new: plan.context = kogen_planner (extension)
new: plan.prompt = lab:plan (extension)
new: repair.context = packet,diff,check_results,review_findings (extension)
new: repair.roles = builder (extension)
new: review.timing = every_green (extension)
new: shape.critique_prompt = lab:critique (extension)
new: shape.critique_rounds = 1 (extension)
new: shape.helper_context = lab_helper (extension)
new: shape.helper_prompt = lab:helper (extension)
new: shape.subagents_output = 4096 (extension)
new: shape.subagents_turns = 10 (extension)
old-review: build.helper_context = lab_helper (extension)
old-review: build.helper_prompt = lab:helper (extension)
old-review: build.subagents_output = 4096 (extension)
old-review: build.subagents_turns = 10 (extension)
old-review: plan.context = kogen_planner (extension)
old-review: plan.prompt = lab:plan (extension)
old-review: repair.context = packet,diff,check_results,review_findings (extension)
old-review: repair.roles = builder (extension)
old-review: review.timing = every_green (extension)
old-review: shape.critique_prompt = lab:critique (extension)
old-review: shape.critique_rounds = 1 (extension)
old-review: shape.helper_context = lab_helper (extension)
old-review: shape.helper_prompt = lab:helper (extension)
old-review: shape.subagents_output = 4096 (extension)
old-review: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
