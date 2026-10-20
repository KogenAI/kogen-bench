complete: 12/12 cells scored
Question: mechanism-split-1 run 2 (review-fix-2 tasks): with a weak builder, is the new flow's advantage over the earlier flow due to review-and-fix (vs builder repairs on review findings) or to stopping verification at the first failed gate (vs running all checks)?
Hypothesis: exploratory: review-and-fix carries most of the advantage; verification stopping early changes cost more than correctness
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| new        | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| old-review | 0       | 0         | 4                | 0              | 0          | 0%           | 0 of 0        | 0           |
| run-all    | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
false success: 0 of 4 claims (new)
false success: 0 of 0 claims (old-review)
false success: 0 of 3 claims (run-all)
shaping outcomes:
new: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
old-review: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
run-all: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | new        | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-1-go       | run-all    | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | new        | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | run-all    | 0       | 0         | 1                | 0              | 0          |
| r70-4-go       | new        | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-4-go       | run-all    | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | new        | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | old-review | 0       | 0         | 1                | 0              | 0          |
| r70-6-elixir-2 | run-all    | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| new        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| new        | plan       | 0ms     | 0ms     | 0ms          | 0        |
| new        | build      | 611.5s  | 533.1s  | 78.4s        | 55       |
| new        | verify     | 16.4s   | 0ms     | 16.4s        | 0        |
| new        | review     | 1128.6s | 1128.6s | 0ms          | 48       |
| new        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| new        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| new        | assessment | 0ms     | 0ms     | 0ms          | 0        |
| old-review | shape      | 0ms     | 0ms     | 0ms          | 0        |
| old-review | plan       | 0ms     | 0ms     | 0ms          | 0        |
| old-review | build      | 1085.7s | 1073.9s | 11.8s        | 96       |
| old-review | verify     | 4.8s    | 0ms     | 4.8s         | 0        |
| old-review | review     | 700.6s  | 700.6s  | 0ms          | 40       |
| old-review | commit     | 0ms     | 0ms     | 0ms          | 0        |
| old-review | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| old-review | assessment | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | build      | 1712.6s | 1637.2s | 75.4s        | 63       |
| run-all    | verify     | 41.8s   | 0ms     | 41.8s        | 0        |
| run-all    | review     | 1125.7s | 1125.7s | 0ms          | 49       |
| run-all    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| run-all    | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                             | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| ms2-r70-1-go-r0-new-a1              | correct          | 561.4s  | 531.2s  | 30.2s        | 21       | 0       | 1       | 0         | 0                    |
| ms2-r70-1-go-r0-old-review-a1       | workflow failure | 618.5s  | 605s    | 13.5s        | 44       | 6       | 4       | 0         | 0                    |
| ms2-r70-1-go-r0-run-all-a1          | correct          | 653.9s  | 622.1s  | 31.8s        | 24       | 0       | 1       | 0         | 0                    |
| ms2-r70-4-elixir-2-r0-new-a1        | correct          | 390.2s  | 365.5s  | 24.7s        | 24       | 2       | 1       | 0         | 0                    |
| ms2-r70-4-elixir-2-r0-old-review-a1 | workflow failure | 245.3s  | 234.4s  | 10.9s        | 21       | 6       | 0       | 0         | 0                    |
| ms2-r70-4-elixir-2-r0-run-all-a1    | workflow failure | 329.3s  | 284.1s  | 45.2s        | 27       | 6       | 0       | 0         | 0                    |
| ms2-r70-4-go-r0-new-a1              | correct          | 312.3s  | 299s    | 13.4s        | 22       | 2       | 1       | 0         | 0                    |
| ms2-r70-4-go-r0-old-review-a1       | workflow failure | 776s    | 762.2s  | 13.8s        | 52       | 6       | 7       | 0         | 0                    |
| ms2-r70-4-go-r0-run-all-a1          | correct          | 417.1s  | 399.5s  | 17.6s        | 19       | 1       | 1       | 0         | 0                    |
| ms2-r70-6-elixir-2-r0-new-a1        | correct          | 520.1s  | 465.9s  | 54.2s        | 36       | 2       | 1       | 0         | 0                    |
| ms2-r70-6-elixir-2-r0-old-review-a1 | workflow failure | 183.4s  | 172.9s  | 10.5s        | 19       | 6       | 0       | 0         | 0                    |
| ms2-r70-6-elixir-2-r0-run-all-a1    | correct          | 1510.6s | 1457.1s | 53.5s        | 42       | 4       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
new openai: input 1.55M, cached 0.22M, output 58.6k, reasoning 18.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.61M
old-review openai: input 2.14M, cached 0.53M, output 55.8k, reasoning 14.4k, input_tokens_details.cache_write_tokens 0, total_tokens 2.19M
run-all openai: input 2.00M, cached 0.37M, output 64.0k, reasoning 19.6k, input_tokens_details.cache_write_tokens 0, total_tokens 2.06M
native usage by stage and provider:
stage build new openai (responses): input 0.59M, cached 0.16M, output 16.6k, reasoning 81, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
stage build old-review openai (responses): input 1.47M, cached 0.53M, output 35.1k, reasoning 87, input_tokens_details.cache_write_tokens 0, total_tokens 1.50M
stage build run-all openai (responses): input 0.87M, cached 0.34M, output 23.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.89M
stage review new openai (responses): input 0.97M, cached 57.6k, output 42.0k, reasoning 18.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
stage review old-review openai (responses): input 0.67M, cached 0, output 20.7k, reasoning 14.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
stage review run-all openai (responses): input 1.13M, cached 21.0k, output 40.8k, reasoning 19.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.17M
native usage by attempt and provider:
attempt usage ms2-r70-1-go-r0-new-a1 openai (responses): input 0.45M, cached 51.2k, output 19.6k, reasoning 9.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage ms2-r70-1-go-r0-old-review-a1 openai (responses): input 0.75M, cached 0.21M, output 19.7k, reasoning 3.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.77M
attempt usage ms2-r70-1-go-r0-run-all-a1 openai (responses): input 0.55M, cached 9.6k, output 23.2k, reasoning 10.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.57M
attempt usage ms2-r70-4-elixir-2-r0-new-a1 openai (responses): input 0.29M, cached 12.0k, output 12.8k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage ms2-r70-4-elixir-2-r0-old-review-a1 openai (responses): input 0.29M, cached 0.10M, output 7.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage ms2-r70-4-elixir-2-r0-run-all-a1 openai (responses): input 0.42M, cached 0.16M, output 8.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage ms2-r70-4-go-r0-new-a1 openai (responses): input 0.26M, cached 39.7k, output 10.5k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage ms2-r70-4-go-r0-old-review-a1 openai (responses): input 0.77M, cached 0.11M, output 24.2k, reasoning 10.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.79M
attempt usage ms2-r70-4-go-r0-run-all-a1 openai (responses): input 0.32M, cached 10.0k, output 15.1k, reasoning 6.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
attempt usage ms2-r70-6-elixir-2-r0-new-a1 openai (responses): input 0.55M, cached 0.12M, output 15.7k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.57M
attempt usage ms2-r70-6-elixir-2-r0-old-review-a1 openai (responses): input 0.33M, cached 98.4k, output 4.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage ms2-r70-6-elixir-2-r0-run-all-a1 openai (responses): input 0.71M, cached 0.19M, output 17.5k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
attempt outcomes included: new: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; old-review: correct 0, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0; run-all: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 6518.2s, model 6198.9s, tools/checks 319.2s, requests 351
builder settings: new openai gpt-6-luna reasoning.effort=low; old-review openai gpt-6-luna reasoning.effort=low; run-all openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 12, started 12, scored 12, incorrect 0, infrastructure 0, incomplete 0
variant old-review differs from new in:
  review.context: kogen_reviewer -> kogen_reviewer_fd0cdcfb
  review.effect: stop -> builder_repair
  review.tools: fix -> read_only
variant run-all differs from new in:
  verify.continue: stop_at_first -> run_all
C03: exercised in 4 of 4 old-review attempts
review.effect: not exercised
C09: exercised in 4 of 4 old-review attempts
V07: exercised in 4 of 4 run-all attempts
first position per task: r70-1-go new 0, old-review 0, run-all 1 (1 repetitions, 3 variants)
first position per task: r70-4-elixir-2 new 1, old-review 0, run-all 0 (1 repetitions, 3 variants)
first position per task: r70-4-go new 0, old-review 1, run-all 0 (1 repetitions, 3 variants)
first position per task: r70-6-elixir-2 new 1, old-review 0, run-all 0 (1 repetitions, 3 variants)
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
