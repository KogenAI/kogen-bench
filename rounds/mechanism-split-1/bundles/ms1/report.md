incomplete: 8 of 18 cells scored
Question: mechanism-split-1: with a weak builder, is the new flow's advantage over the earlier flow due to review-and-fix (vs builder repairs on review findings) or to stopping verification at the first failed gate (vs running all checks)?
Hypothesis: exploratory: review-and-fix carries most of the advantage; verification stopping early changes cost more than correctness
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (8 of 18 cells scored)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| new        | 2       | 0         | 0                | 0              | 1          | 100%         | 0 of 2        | 0           |
| old-review | 3       | 0         | 0                | 0              | 0          | 100%         | 0 of 3        | 0           |
| run-all    | 2       | 0         | 1                | 0              | 0          | 66.7%        | 0 of 2        | 0           |
false success: 0 of 2 claims (new)
false success: 0 of 3 claims (old-review)
false success: 0 of 2 claims (run-all)
shaping outcomes:
new: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
old-review: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
run-all: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------|---------|-----------|------------------|----------------|------------|
| env-ex       | new        | 0       | 0         | 0                | 0              | 0          |
| env-ex       | old-review | 0       | 0         | 0                | 0              | 0          |
| env-ex       | run-all    | 0       | 0         | 0                | 0              | 0          |
| r70-5-elixir | new        | 0       | 0         | 0                | 0              | 1          |
| r70-5-elixir | old-review | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | run-all    | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | new        | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | old-review | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | run-all    | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | new        | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | old-review | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | run-all    | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | new        | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | old-review | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | run-all    | 1       | 0         | 0                | 0              | 0          |
| sched-go     | new        | 0       | 0         | 0                | 0              | 0          |
| sched-go     | old-review | 0       | 0         | 0                | 0              | 0          |
| sched-go     | run-all    | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| new        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| new        | plan       | 0ms     | 0ms     | 0ms          | 0        |
| new        | build      | 304.9s  | 293.2s  | 11.7s        | 23       |
| new        | verify     | 5s      | 0ms     | 5s           | 0        |
| new        | review     | 426.1s  | 426.1s  | 0ms          | 23       |
| new        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| new        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| new        | assessment | 0ms     | 0ms     | 0ms          | 0        |
| old-review | shape      | 0ms     | 0ms     | 0ms          | 0        |
| old-review | plan       | 0ms     | 0ms     | 0ms          | 0        |
| old-review | build      | 637.2s  | 620.2s  | 16.9s        | 55       |
| old-review | verify     | 13.4s   | 0ms     | 13.4s        | 0        |
| old-review | review     | 498.8s  | 498.8s  | 0ms          | 33       |
| old-review | commit     | 0ms     | 0ms     | 0ms          | 0        |
| old-review | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| old-review | assessment | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | build      | 3920.4s | 3891.9s | 28.5s        | 150      |
| run-all    | verify     | 12.5s   | 0ms     | 12.5s        | 0        |
| run-all    | review     | 286.4s  | 286.4s  | 0ms          | 18       |
| run-all    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall    | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|---------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ms1-r70-5-elixir-r0-new-a1        | incomplete       | 190.9s  | 176.9s | 14.1s        | 13       | 1       | 0       | 0         | 0                    |
| ms1-r70-5-elixir-r0-old-review-a1 | correct          | 546.5s  | 514.6s | 31.9s        | 37       | 5       | 4       | 0         | 0                    |
| ms1-r70-5-elixir-r0-run-all-a1    | correct          | 365.6s  | 334.6s | 31s          | 29       | 2       | 1       | 0         | 0                    |
| ms1-r70-5-go-r0-new-a1            | correct          | 276.5s  | 265s   | 11.5s        | 14       | 0       | 1       | 0         | 0                    |
| ms1-r70-5-go-r0-old-review-a1     | correct          | 419.6s  | 407.2s | 12.4s        | 36       | 3       | 4       | 0         | 0                    |
| ms1-r70-5-go-r0-run-all-a1        | workflow failure | 3610.9s | 3603s  | 7.9s         | 122      | 0       | 0       | 0         | 0                    |
| ms1-r70-7-go-r0-new-a1            | correct          | 289.8s  | 277.4s | 12.4s        | 19       | 0       | 1       | 0         | 0                    |
| ms1-r70-7-go-r0-old-review-a1     | correct          | 206.6s  | 197.3s | 9.3s         | 15       | 1       | 2       | 0         | 0                    |
| ms1-r70-7-go-r0-run-all-a1        | correct          | 264.5s  | 240.8s | 23.8s        | 17       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
new openai: input 0.57M, cached 64.3k, output 26.7k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
old-review openai: input 1.23M, cached 0.15M, output 36.9k, reasoning 11.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.27M
run-all openai: input 10.22M, cached 4.30M, output 0.17M, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 10.39M
native usage by stage and provider:
stage build new openai (responses): input 0.19M, cached 51.8k, output 10.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
stage build old-review openai (responses): input 0.68M, cached 0.15M, output 21.6k, reasoning 566, input_tokens_details.cache_write_tokens 0, total_tokens 0.70M
stage build run-all openai (responses): input 9.93M, cached 4.30M, output 0.16M, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 10.09M
stage review new openai (responses): input 0.37M, cached 12.4k, output 15.9k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
stage review old-review openai (responses): input 0.55M, cached 0, output 15.3k, reasoning 10.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.57M
stage review run-all openai (responses): input 0.29M, cached 0, output 11.0k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
native usage by attempt and provider:
attempt usage ms1-r70-5-elixir-r0-new-a1 openai (responses): input 0.13M, cached 46.5k, output 6.2k, reasoning 459, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage ms1-r70-5-elixir-r0-old-review-a1 openai (responses): input 0.58M, cached 50.2k, output 17.5k, reasoning 5.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
attempt usage ms1-r70-5-elixir-r0-run-all-a1 openai (responses): input 0.36M, cached 53.9k, output 11.6k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage ms1-r70-5-go-r0-new-a1 openai (responses): input 0.20M, cached 0, output 10.3k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage ms1-r70-5-go-r0-old-review-a1 openai (responses): input 0.49M, cached 74.0k, output 12.7k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage ms1-r70-5-go-r0-run-all-a1 openai (responses): input 9.65M, cached 4.24M, output 0.15M, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 9.80M
attempt usage ms1-r70-7-go-r0-new-a1 openai (responses): input 0.24M, cached 17.8k, output 10.2k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage ms1-r70-7-go-r0-old-review-a1 openai (responses): input 0.16M, cached 29.7k, output 6.8k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage ms1-r70-7-go-r0-run-all-a1 openai (responses): input 0.21M, cached 0, output 9.1k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt outcomes included: new: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; old-review: correct 3, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; run-all: correct 2, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 6171s, model 6016.6s, tools/checks 154.5s, requests 302
builder settings: new openai gpt-6-luna reasoning.effort=low; old-review openai gpt-6-luna reasoning.effort=low; run-all openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 18, started 9, scored 8, incorrect 0, infrastructure 0, incomplete 1
variant old-review differs from new in:
  review.context: kogen_reviewer -> kogen_reviewer_fd0cdcfb
  review.effect: stop -> builder_repair
  review.tools: fix -> read_only
variant run-all differs from new in:
  verify.continue: stop_at_first -> run_all
C03: exercised in 3 of 3 old-review attempts
review.effect: not exercised
C09: exercised in 3 of 3 old-review attempts
V07: exercised in 3 of 3 run-all attempts
first position per task: env-ex new 0, old-review 0, run-all 1 (1 repetitions, 3 variants)
first position per task: r70-5-elixir new 0, old-review 1, run-all 0 (1 repetitions, 3 variants)
first position per task: r70-5-go new 1, old-review 0, run-all 0 (1 repetitions, 3 variants)
first position per task: r70-7-elixir new 0, old-review 1, run-all 0 (1 repetitions, 3 variants)
first position per task: r70-7-go new 0, old-review 0, run-all 1 (1 repetitions, 3 variants)
first position per task: sched-go new 0, old-review 1, run-all 0 (1 repetitions, 3 variants)
new: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
old-review: not the Kogen profile (differs in review.context, review.effect, review.tools, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
run-all: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds, verify.continue)
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
run-all: build.helper_context = lab_helper (extension)
run-all: build.helper_prompt = lab:helper (extension)
run-all: build.subagents_output = 4096 (extension)
run-all: build.subagents_turns = 10 (extension)
run-all: plan.context = kogen_planner (extension)
run-all: plan.prompt = lab:plan (extension)
run-all: repair.context = packet,diff,check_results,review_findings (extension)
run-all: repair.roles = builder (extension)
run-all: review.timing = every_green (extension)
run-all: shape.critique_prompt = lab:critique (extension)
run-all: shape.critique_rounds = 1 (extension)
run-all: shape.helper_context = lab_helper (extension)
run-all: shape.helper_prompt = lab:helper (extension)
run-all: shape.subagents_output = 4096 (extension)
run-all: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
