incomplete: 7 of 8 cells scored
Question: reviewer-effort-weak-1: with a weak builder, does a Sol-medium reviewer-fixer rescue wrong code as often as the default Sol-high one, at lower reviewer input?
Hypothesis: exploratory: medium rescues fewer; lower reviewer input
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (7 of 8 cells scored)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| reviewer-high   | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| reviewer-medium | 2       | 0         | 1                | 1              | 0          | 66.7%        | 0 of 2        | 0           |
false success: 0 of 4 claims (reviewer-high)
false success: 0 of 2 claims (reviewer-medium)
shaping outcomes:
reviewer-high: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
reviewer-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-4-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | reviewer-medium | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | reviewer-medium | 0       | 0         | 0                | 1              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant         | stage      | elapsed time   | model  | tools/checks | requests |
|-----------------|------------|--------|--------|--------------|----------|
| reviewer-high   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | build      | 516.5s | 448.2s | 68.4s        | 35       |
| reviewer-high   | verify     | 26s    | 0ms    | 26s          | 0        |
| reviewer-high   | review     | 795.5s | 795.5s | 0ms          | 43       |
| reviewer-high   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | assessment | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | build      | 393.1s | 363.3s | 29.8s        | 32       |
| reviewer-medium | verify     | 23.2s  | 0ms    | 23.2s        | 0        |
| reviewer-medium | review     | 300.4s | 300.4s | 0ms          | 22       |
| reviewer-medium | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                  | outcome          | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rew1b-r70-4-go-r0-reviewer-high-a1       | correct          | 353.3s | 321.5s | 31.8s        | 22       | 2       | 1       | 0         | 0                    |
| rew1b-r70-4-go-r0-reviewer-medium-a1     | correct          | 223.1s | 196.2s | 26.9s        | 14       | 1       | 1       | 0         | 0                    |
| rew1b-r70-5-go-r0-reviewer-high-a1       | correct          | 286.1s | 272.1s | 14s          | 17       | 0       | 1       | 0         | 0                    |
| rew1b-r70-5-go-r0-reviewer-medium-a1     | workflow failure | 189.8s | 180.3s | 9.6s         | 15       | 5       | 0       | 0         | 0                    |
| rew1b-r70-7-elixir-r0-reviewer-high-a1   | correct          | 424.1s | 374.5s | 49.6s        | 22       | 0       | 1       | 0         | 0                    |
| rew1b-r70-7-elixir-r0-reviewer-medium-a1 | correct          | 200.4s | 169.8s | 30.6s        | 14       | 0       | 1       | 0         | 0                    |
| rew1b-r70-7-go-r0-reviewer-high-a1       | correct          | 292.7s | 275.7s | 17s          | 17       | 0       | 1       | 0         | 0                    |
| rew1b-r70-7-go-r0-reviewer-medium-a1     | infrastructure   | 124.7s | 117.4s | 7.3s         | 11       | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 1.05M, cached 0.11M, output 47.2k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.09M
reviewer-medium openai: input 0.59M, cached 78.2k, output 23.5k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 0.30M, cached 86.0k, output 17.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
stage build reviewer-medium openai (responses): input 0.30M, cached 78.2k, output 12.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
stage review reviewer-high openai (responses): input 0.74M, cached 23.7k, output 30.2k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.77M
stage review reviewer-medium openai (responses): input 0.29M, cached 0, output 10.7k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
native usage by attempt and provider:
attempt usage rew1b-r70-4-go-r0-reviewer-high-a1 openai (responses): input 0.32M, cached 33.8k, output 11.5k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
attempt usage rew1b-r70-4-go-r0-reviewer-medium-a1 openai (responses): input 0.17M, cached 0, output 7.3k, reasoning 648, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rew1b-r70-5-go-r0-reviewer-high-a1 openai (responses): input 0.20M, cached 18.4k, output 10.6k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rew1b-r70-5-go-r0-reviewer-medium-a1 openai (responses): input 0.17M, cached 40.6k, output 6.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage rew1b-r70-7-elixir-r0-reviewer-high-a1 openai (responses): input 0.31M, cached 38.5k, output 14.4k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
attempt usage rew1b-r70-7-elixir-r0-reviewer-medium-a1 openai (responses): input 0.15M, cached 21.5k, output 5.9k, reasoning 664, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rew1b-r70-7-go-r0-reviewer-high-a1 openai (responses): input 0.22M, cached 18.9k, output 10.7k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rew1b-r70-7-go-r0-reviewer-medium-a1 openai (responses): input 98.2k, cached 16.1k, output 3.7k, reasoning 208, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt outcomes included: reviewer-high: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 2, incorrect 0, workflow failure 1, infrastructure 1, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2094.2s, model 1907.3s, tools/checks 186.8s, requests 132
builder settings: reviewer-high openai gpt-6-luna reasoning.effort=low; reviewer-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 7, incorrect 0, infrastructure 1, incomplete 0
variant reviewer-medium differs from reviewer-high in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.reviewer.effort: exercised in 4 of 4 reviewer-medium attempts
first position per task: r70-4-go reviewer-high 0, reviewer-medium 1 (1 repetitions, 2 variants)
first position per task: r70-5-go reviewer-high 0, reviewer-medium 1 (1 repetitions, 2 variants)
first position per task: r70-7-elixir reviewer-high 1, reviewer-medium 0 (1 repetitions, 2 variants)
first position per task: r70-7-go reviewer-high 1, reviewer-medium 0 (1 repetitions, 2 variants)
reviewer-high: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
reviewer-medium: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.reviewer.effort, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
reviewer-high: build.helper_context = lab_helper (extension)
reviewer-high: build.helper_prompt = lab:helper (extension)
reviewer-high: build.subagents_output = 4096 (extension)
reviewer-high: build.subagents_turns = 10 (extension)
reviewer-high: plan.context = kogen_planner (extension)
reviewer-high: plan.prompt = lab:plan (extension)
reviewer-high: repair.context = packet,diff,check_results,review_findings (extension)
reviewer-high: repair.roles = builder (extension)
reviewer-high: review.timing = every_green (extension)
reviewer-high: shape.critique_prompt = lab:critique (extension)
reviewer-high: shape.critique_rounds = 1 (extension)
reviewer-high: shape.helper_context = lab_helper (extension)
reviewer-high: shape.helper_prompt = lab:helper (extension)
reviewer-high: shape.subagents_output = 4096 (extension)
reviewer-high: shape.subagents_turns = 10 (extension)
reviewer-medium: build.helper_context = lab_helper (extension)
reviewer-medium: build.helper_prompt = lab:helper (extension)
reviewer-medium: build.subagents_output = 4096 (extension)
reviewer-medium: build.subagents_turns = 10 (extension)
reviewer-medium: plan.context = kogen_planner (extension)
reviewer-medium: plan.prompt = lab:plan (extension)
reviewer-medium: repair.context = packet,diff,check_results,review_findings (extension)
reviewer-medium: repair.roles = builder (extension)
reviewer-medium: review.timing = every_green (extension)
reviewer-medium: shape.critique_prompt = lab:critique (extension)
reviewer-medium: shape.critique_rounds = 1 (extension)
reviewer-medium: shape.helper_context = lab_helper (extension)
reviewer-medium: shape.helper_prompt = lab:helper (extension)
reviewer-medium: shape.subagents_output = 4096 (extension)
reviewer-medium: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
