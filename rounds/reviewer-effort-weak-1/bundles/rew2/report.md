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
| task     | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-4-go | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| r70-4-go | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| r70-5-go | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| r70-5-go | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant         | stage      | elapsed time   | model  | tools/checks | requests |
|-----------------|------------|--------|--------|--------------|----------|
| reviewer-high   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | build      | 382s   | 312.4s | 69.5s        | 33       |
| reviewer-high   | verify     | 25.6s  | 0ms    | 25.6s        | 0        |
| reviewer-high   | review     | 907s   | 907s   | 0ms          | 39       |
| reviewer-high   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-high   | assessment | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | shape      | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | plan       | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | build      | 219.8s | 181.6s | 38.1s        | 17       |
| reviewer-medium | verify     | 18.9s  | 0ms    | 18.9s        | 0        |
| reviewer-medium | review     | 429.5s | 429.5s | 0ms          | 30       |
| reviewer-medium | commit     | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| reviewer-medium | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                             | outcome | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rew2-r70-4-go-r0-reviewer-high-a1   | correct | 312.4s | 277.8s | 34.6s        | 17       | 0       | 1       | 0         | 0                    |
| rew2-r70-4-go-r0-reviewer-medium-a1 | correct | 171s   | 148.8s | 22.2s        | 11       | 0       | 1       | 0         | 0                    |
| rew2-r70-4-go-r1-reviewer-high-a1   | correct | 475.3s | 425.4s | 49.9s        | 27       | 3       | 1       | 0         | 0                    |
| rew2-r70-4-go-r1-reviewer-medium-a1 | correct | 204.2s | 171.6s | 32.6s        | 16       | 0       | 1       | 0         | 0                    |
| rew2-r70-5-go-r0-reviewer-high-a1   | correct | 306.1s | 291.7s | 14.4s        | 15       | 0       | 1       | 0         | 0                    |
| rew2-r70-5-go-r0-reviewer-medium-a1 | correct | 143.2s | 133.8s | 9.4s         | 10       | 0       | 1       | 0         | 0                    |
| rew2-r70-5-go-r1-reviewer-high-a1   | correct | 240.1s | 224.6s | 15.5s        | 13       | 0       | 1       | 0         | 0                    |
| rew2-r70-5-go-r1-reviewer-medium-a1 | correct | 171.1s | 156.9s | 14.2s        | 10       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 0.97M, cached 0.17M, output 46.1k, reasoning 13.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
reviewer-medium openai: input 0.55M, cached 64.9k, output 21.7k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.57M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 0.27M, cached 0.13M, output 10.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
stage build reviewer-medium openai (responses): input 0.13M, cached 64.9k, output 6.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
stage review reviewer-high openai (responses): input 0.70M, cached 40.4k, output 35.9k, reasoning 13.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
stage review reviewer-medium openai (responses): input 0.42M, cached 0, output 15.6k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
native usage by attempt and provider:
attempt usage rew2-r70-4-go-r0-reviewer-high-a1 openai (responses): input 0.24M, cached 33.0k, output 10.2k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rew2-r70-4-go-r0-reviewer-medium-a1 openai (responses): input 0.13M, cached 10.0k, output 5.3k, reasoning 659, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage rew2-r70-4-go-r1-reviewer-high-a1 openai (responses): input 0.33M, cached 70.0k, output 16.0k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage rew2-r70-4-go-r1-reviewer-medium-a1 openai (responses): input 0.18M, cached 33.7k, output 5.6k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rew2-r70-5-go-r0-reviewer-high-a1 openai (responses): input 0.22M, cached 38.9k, output 11.3k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage rew2-r70-5-go-r0-reviewer-medium-a1 openai (responses): input 0.12M, cached 10.6k, output 4.9k, reasoning 377, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage rew2-r70-5-go-r1-reviewer-high-a1 openai (responses): input 0.17M, cached 23.7k, output 8.6k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage rew2-r70-5-go-r1-reviewer-medium-a1 openai (responses): input 0.12M, cached 10.6k, output 5.9k, reasoning 280, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt outcomes included: reviewer-high: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2023.3s, model 1830.6s, tools/checks 192.8s, requests 119
builder settings: reviewer-high openai gpt-6-luna reasoning.effort=low; reviewer-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant reviewer-medium differs from reviewer-high in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.reviewer.effort: exercised in 4 of 4 reviewer-medium attempts
first position per task: r70-4-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: r70-5-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
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
