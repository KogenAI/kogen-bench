complete: 8/8 cells scored
Question: reviewer-effort-weak-1: with a weak builder, does a Sol-medium reviewer-fixer rescue wrong code as often as the default Sol-high one, at lower reviewer input?
Hypothesis: exploratory: medium rescues fewer; lower reviewer input
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| reviewer-high   | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| reviewer-medium | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (reviewer-high)
false success: 0 of 4 claims (reviewer-medium)
shaping outcomes:
reviewer-high: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
reviewer-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-4-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | reviewer-high   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant         | stage      | elapsed time   | model  | tools/checks | requests |
|-----------------|------------|--------|--------|--------------|----------|
| reviewer-high   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | build      | 521.1s | 451.3s | 69.8s        | 39       |
| reviewer-high   | verify     | 29.6s  | 0ms    | 29.6s        | 0        |
| reviewer-high   | review     | 916.8s | 916.8s | 0ms          | 45       |
| reviewer-high   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | assessment | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | build      | 380.8s | 360.7s | 20.2s        | 33       |
| reviewer-medium | verify     | 13.4s  | 0ms    | 13.4s        | 0        |
| reviewer-medium | review     | 443.1s | 443.1s | 0ms          | 33       |
| reviewer-medium | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                 | outcome | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rew1-r70-4-go-r0-reviewer-high-a1       | correct | 432.1s | 382.5s | 49.6s        | 21       | 0       | 1       | 0         | 0                    |
| rew1-r70-4-go-r0-reviewer-medium-a1     | correct | 187.6s | 166.8s | 20.8s        | 12       | 0       | 1       | 0         | 0                    |
| rew1-r70-5-go-r0-reviewer-high-a1       | correct | 277.2s | 266.6s | 10.5s        | 16       | 1       | 1       | 0         | 0                    |
| rew1-r70-5-go-r0-reviewer-medium-a1     | correct | 220.9s | 207.9s | 13.1s        | 19       | 1       | 1       | 0         | 0                    |
| rew1-r70-7-elixir-r0-reviewer-high-a1   | correct | 455.4s | 412.8s | 42.6s        | 27       | 1       | 1       | 0         | 0                    |
| rew1-r70-7-elixir-r0-reviewer-medium-a1 | correct | 271.9s | 261.7s | 10.2s        | 22       | 0       | 1       | 0         | 0                    |
| rew1-r70-7-go-r0-reviewer-high-a1       | correct | 320.4s | 306.1s | 14.2s        | 20       | 0       | 1       | 0         | 0                    |
| rew1-r70-7-go-r0-reviewer-medium-a1     | correct | 176.5s | 167.4s | 9.1s         | 13       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 1.18M, cached 0.13M, output 52.6k, reasoning 11.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.23M
reviewer-medium openai: input 0.79M, cached 0.11M, output 27.8k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.82M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 0.36M, cached 83.2k, output 16.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
stage build reviewer-medium openai (responses): input 0.30M, cached 78.5k, output 12.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
stage review reviewer-high openai (responses): input 0.82M, cached 44.2k, output 36.2k, reasoning 11.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.85M
stage review reviewer-medium openai (responses): input 0.49M, cached 28.2k, output 15.5k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
native usage by attempt and provider:
attempt usage rew1-r70-4-go-r0-reviewer-high-a1 openai (responses): input 0.37M, cached 46.3k, output 14.5k, reasoning 5.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
attempt usage rew1-r70-4-go-r0-reviewer-medium-a1 openai (responses): input 0.14M, cached 10.0k, output 5.9k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rew1-r70-5-go-r0-reviewer-high-a1 openai (responses): input 0.20M, cached 5.2k, output 10.6k, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rew1-r70-5-go-r0-reviewer-medium-a1 openai (responses): input 0.22M, cached 25.6k, output 6.7k, reasoning 452, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rew1-r70-7-elixir-r0-reviewer-high-a1 openai (responses): input 0.36M, cached 62.3k, output 15.7k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage rew1-r70-7-elixir-r0-reviewer-medium-a1 openai (responses): input 0.28M, cached 48.9k, output 9.3k, reasoning 351, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rew1-r70-7-go-r0-reviewer-high-a1 openai (responses): input 0.25M, cached 13.4k, output 11.7k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rew1-r70-7-go-r0-reviewer-medium-a1 openai (responses): input 0.15M, cached 22.1k, output 5.9k, reasoning 253, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt outcomes included: reviewer-high: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2341.9s, model 2171.8s, tools/checks 170.1s, requests 150
builder settings: reviewer-high openai gpt-6-luna reasoning.effort=low; reviewer-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
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
