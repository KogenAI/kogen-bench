complete: 12/12 cells scored
Question: review-fix-1: does Kogen's review-and-fix flow keep correctness against the earlier builder-repair loop, at what cost, and does a Sol-medium reviewer-fixer do as well as Sol high?
Hypothesis: exploratory: review-and-fix matches builder-repair with fewer rounds; Sol medium matches Sol high (fixer-model-1)
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| new             | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| weak-new        | 2       | 0         | 2                | 0              | 0          | 50%          | 0 of 2        | 0           |
| weak-new-medium | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
false success: 0 of 4 claims (new)
false success: 0 of 2 claims (weak-new)
false success: 0 of 3 claims (weak-new-medium)
shaping outcomes:
new: shaping ready 4, shaping failed 0; correct 4 of 4
weak-new: shaping ready 4, shaping failed 0; correct 2 of 4
weak-new-medium: shaping ready 4, shaping failed 0; correct 3 of 4
## Per-task outcomes
| task           | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | new             | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | weak-new        | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | weak-new-medium | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | new             | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | weak-new        | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | weak-new-medium | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | new             | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | weak-new        | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | weak-new-medium | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | new             | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | weak-new        | 0       | 0         | 1                | 0              | 0          |
| r70-6-elixir-2 | weak-new-medium | 0       | 0         | 1                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| new             | shape      | 0ms     | 0ms     | 0ms          | 0        |
| new             | plan       | 0ms     | 0ms     | 0ms          | 0        |
| new             | build      | 839s    | 723.9s  | 115.1s       | 36       |
| new             | verify     | 11.9s   | 0ms     | 11.9s        | 0        |
| new             | review     | 1193.2s | 1193.2s | 0ms          | 34       |
| new             | commit     | 0ms     | 0ms     | 0ms          | 0        |
| new             | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| new             | assessment | 0ms     | 0ms     | 0ms          | 0        |
| weak-new        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| weak-new        | plan       | 0ms     | 0ms     | 0ms          | 0        |
| weak-new        | build      | 1366.8s | 1248.3s | 118.4s       | 63       |
| weak-new        | verify     | 41s     | 0ms     | 41s          | 0        |
| weak-new        | review     | 1418.1s | 1418.1s | 0ms          | 38       |
| weak-new        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| weak-new        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| weak-new        | assessment | 0ms     | 0ms     | 0ms          | 0        |
| weak-new-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| weak-new-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| weak-new-medium | build      | 843.7s  | 799.5s  | 44.2s        | 60       |
| weak-new-medium | verify     | 33.1s   | 0ms     | 33.1s        | 0        |
| weak-new-medium | review     | 895.8s  | 895.8s  | 0ms          | 30       |
| weak-new-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| weak-new-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| weak-new-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                  | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rv1-r70-1-go-r0-new-a1                   | correct          | 961.6s | 870.1s | 91.4s        | 20       | 0       | 1       | 0         | 0                    |
| rv1-r70-1-go-r0-weak-new-a1              | correct          | 833.6s | 748.2s | 85.4s        | 28       | 0       | 1       | 0         | 0                    |
| rv1-r70-1-go-r0-weak-new-medium-a1       | correct          | 546.5s | 529.1s | 17.4s        | 22       | 1       | 1       | 0         | 0                    |
| rv1-r70-4-elixir-2-r0-new-a1             | correct          | 317.6s | 292.9s | 24.7s        | 16       | 0       | 1       | 0         | 0                    |
| rv1-r70-4-elixir-2-r0-weak-new-a1        | workflow failure | 369.5s | 346.8s | 22.7s        | 17       | 6       | 0       | 0         | 0                    |
| rv1-r70-4-elixir-2-r0-weak-new-medium-a1 | correct          | 425.5s | 393.2s | 32.3s        | 21       | 1       | 1       | 0         | 0                    |
| rv1-r70-4-go-r0-new-a1                   | correct          | 487.3s | 474.3s | 12.9s        | 18       | 0       | 1       | 0         | 0                    |
| rv1-r70-4-go-r0-weak-new-a1              | correct          | 946.6s | 928.8s | 17.8s        | 22       | 0       | 1       | 0         | 0                    |
| rv1-r70-4-go-r0-weak-new-medium-a1       | correct          | 520.4s | 506.1s | 14.4s        | 16       | 0       | 1       | 0         | 0                    |
| rv1-r70-6-elixir-2-r0-new-a1             | correct          | 299.8s | 279.7s | 20.1s        | 16       | 0       | 1       | 0         | 0                    |
| rv1-r70-6-elixir-2-r0-weak-new-a1        | workflow failure | 704.4s | 642.6s | 61.8s        | 34       | 6       | 0       | 0         | 0                    |
| rv1-r70-6-elixir-2-r0-weak-new-medium-a1 | workflow failure | 306.2s | 266.9s | 39.2s        | 31       | 6       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
new openai: input 1.08M, cached 54.0k, output 49.9k, reasoning 23.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.13M
weak-new openai: input 2.01M, cached 0.41M, output 61.5k, reasoning 19.4k, input_tokens_details.cache_write_tokens 0, total_tokens 2.07M
weak-new-medium openai: input 1.21M, cached 0.30M, output 32.0k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.25M
native usage by stage and provider:
stage build new openai (responses): input 0.36M, cached 33.9k, output 16.8k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
stage build weak-new openai (responses): input 1.05M, cached 0.32M, output 24.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
stage build weak-new-medium openai (responses): input 0.77M, cached 0.29M, output 16.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
stage review new openai (responses): input 0.72M, cached 20.1k, output 33.1k, reasoning 20.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.76M
stage review weak-new openai (responses): input 0.96M, cached 96.0k, output 36.8k, reasoning 19.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.00M
stage review weak-new-medium openai (responses): input 0.45M, cached 12.7k, output 15.5k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
native usage by attempt and provider:
attempt usage rv1-r70-1-go-r0-new-a1 openai (responses): input 0.42M, cached 37.0k, output 24.8k, reasoning 13.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.45M
attempt usage rv1-r70-1-go-r0-weak-new-a1 openai (responses): input 0.71M, cached 59.6k, output 23.9k, reasoning 11.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
attempt usage rv1-r70-1-go-r0-weak-new-medium-a1 openai (responses): input 0.26M, cached 50.6k, output 10.1k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rv1-r70-4-elixir-2-r0-new-a1 openai (responses): input 0.21M, cached 0, output 7.5k, reasoning 3.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rv1-r70-4-elixir-2-r0-weak-new-a1 openai (responses): input 0.20M, cached 52.2k, output 7.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rv1-r70-4-elixir-2-r0-weak-new-medium-a1 openai (responses): input 0.25M, cached 6.8k, output 7.3k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rv1-r70-4-go-r0-new-a1 openai (responses): input 0.24M, cached 5.0k, output 10.9k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rv1-r70-4-go-r0-weak-new-a1 openai (responses): input 0.34M, cached 55.4k, output 17.0k, reasoning 7.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage rv1-r70-4-go-r0-weak-new-medium-a1 openai (responses): input 0.18M, cached 5.0k, output 6.2k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rv1-r70-6-elixir-2-r0-new-a1 openai (responses): input 0.20M, cached 12.0k, output 6.7k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rv1-r70-6-elixir-2-r0-weak-new-a1 openai (responses): input 0.76M, cached 0.25M, output 13.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
attempt usage rv1-r70-6-elixir-2-r0-weak-new-medium-a1 openai (responses): input 0.53M, cached 0.24M, output 8.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
attempt outcomes included: new: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; weak-new: correct 2, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0; weak-new-medium: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 6719s, model 6278.8s, tools/checks 440.2s, requests 261
builder settings: new openai gpt-6.1-sol reasoning.effort=medium
builder settings: weak-new openai gpt-6-luna reasoning.effort=low (not equivalent)
builder settings: weak-new-medium openai gpt-6-luna reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 12, started 12, scored 12, incorrect 0, infrastructure 0, incomplete 0
variant weak-new differs from new in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
variant weak-new-medium differs from new in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.builder.effort: exercised in 4 of 4 weak-new attempts
roles.builder.model: exercised in 4 of 4 weak-new attempts
roles.builder.effort: exercised in 4 of 4 weak-new-medium attempts
roles.builder.model: exercised in 4 of 4 weak-new-medium attempts
roles.reviewer.effort: exercised in 4 of 4 weak-new-medium attempts
first position per task: r70-1-go new 0, weak-new 0, weak-new-medium 1 (1 repetitions, 3 variants)
first position per task: r70-4-elixir-2 new 0, weak-new 0, weak-new-medium 1 (1 repetitions, 3 variants)
first position per task: r70-4-go new 1, weak-new 0, weak-new-medium 0 (1 repetitions, 3 variants)
first position per task: r70-6-elixir-2 new 1, weak-new 0, weak-new-medium 0 (1 repetitions, 3 variants)
new: not the Kogen profile (differs in stop.max_repairs, stop.max_tokens)
weak-new: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_repairs, stop.max_tokens)
weak-new-medium: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.reviewer.effort, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
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
weak-new: build.helper_context = lab_helper (extension)
weak-new: build.helper_prompt = lab:helper (extension)
weak-new: build.subagents_output = 4096 (extension)
weak-new: build.subagents_turns = 10 (extension)
weak-new: plan.context = kogen_planner (extension)
weak-new: plan.prompt = lab:plan (extension)
weak-new: repair.context = packet,diff,check_results,review_findings (extension)
weak-new: repair.roles = builder (extension)
weak-new: review.timing = every_green (extension)
weak-new: shape.critique_prompt = lab:critique (extension)
weak-new: shape.critique_rounds = 1 (extension)
weak-new: shape.helper_context = lab_helper (extension)
weak-new: shape.helper_prompt = lab:helper (extension)
weak-new: shape.subagents_output = 4096 (extension)
weak-new: shape.subagents_turns = 10 (extension)
weak-new-medium: build.helper_context = lab_helper (extension)
weak-new-medium: build.helper_prompt = lab:helper (extension)
weak-new-medium: build.subagents_output = 4096 (extension)
weak-new-medium: build.subagents_turns = 10 (extension)
weak-new-medium: plan.context = kogen_planner (extension)
weak-new-medium: plan.prompt = lab:plan (extension)
weak-new-medium: repair.context = packet,diff,check_results,review_findings (extension)
weak-new-medium: repair.roles = builder (extension)
weak-new-medium: review.timing = every_green (extension)
weak-new-medium: shape.critique_prompt = lab:critique (extension)
weak-new-medium: shape.critique_rounds = 1 (extension)
weak-new-medium: shape.helper_context = lab_helper (extension)
weak-new-medium: shape.helper_prompt = lab:helper (extension)
weak-new-medium: shape.subagents_output = 4096 (extension)
weak-new-medium: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
