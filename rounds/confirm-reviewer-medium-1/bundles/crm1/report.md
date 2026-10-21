complete: 16/16 cells scored
Question: confirm-reviewer-medium-1: on fresh tasks with a weak builder, does a Sol-medium reviewer-fixer rescue wrong trees as reliably as Sol high, with no more wrong submissions, at no more than 70% of its reviewer input?
Hypothesis: reviewer-medium rescues at least the same share of wrong trees as reviewer-high at most 70% of its reviewer input
Purpose: confirmation
Objective: cost_at_quality
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| reviewer-high   | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| reviewer-medium | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (reviewer-high)
false success: 0 of 8 claims (reviewer-medium)
shaping outcomes:
reviewer-high: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
reviewer-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task        | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|-------------|-----------------|---------|-----------|------------------|----------------|------------|
| deps-ex     | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| deps-ex     | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| deps-go     | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| deps-go     | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| interval-ex | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| interval-ex | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| interval-go | reviewer-high   | 2       | 0         | 0                | 0              | 0          |
| interval-go | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| reviewer-high   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | build      | 2358.4s | 2130.9s | 227.5s       | 71       |
| reviewer-high   | verify     | 31s     | 0ms     | 31s          | 0        |
| reviewer-high   | review     | 2427.1s | 2427.1s | 0ms          | 78       |
| reviewer-high   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | build      | 1894.1s | 1850.4s | 43.7s        | 65       |
| reviewer-medium | verify     | 28s     | 0ms     | 28s          | 0        |
| reviewer-medium | review     | 1410s   | 1410s   | 0ms          | 52       |
| reviewer-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| crm1-deps-ex-r0-reviewer-high-a1       | correct | 586.2s | 548.1s | 38.1s        | 23       | 1       | 2       | 0         | 0                    |
| crm1-deps-ex-r0-reviewer-medium-a1     | correct | 469.3s | 455.3s | 14s          | 16       | 0       | 1       | 0         | 0                    |
| crm1-deps-ex-r1-reviewer-high-a1       | correct | 888.4s | 697s   | 191.4s       | 28       | 1       | 1       | 0         | 0                    |
| crm1-deps-ex-r1-reviewer-medium-a1     | correct | 458.7s | 434.7s | 23.9s        | 28       | 4       | 1       | 0         | 0                    |
| crm1-deps-go-r0-reviewer-high-a1       | correct | 441s   | 432.1s | 8.9s         | 13       | 0       | 1       | 0         | 0                    |
| crm1-deps-go-r0-reviewer-medium-a1     | correct | 297.7s | 287.2s | 10.5s        | 11       | 0       | 1       | 0         | 0                    |
| crm1-deps-go-r1-reviewer-high-a1       | correct | 386s   | 373s   | 13s          | 12       | 0       | 1       | 0         | 0                    |
| crm1-deps-go-r1-reviewer-medium-a1     | correct | 402.6s | 378.1s | 24.5s        | 11       | 0       | 1       | 0         | 0                    |
| crm1-interval-ex-r0-reviewer-high-a1   | correct | 653s   | 633.5s | 19.5s        | 21       | 0       | 1       | 0         | 0                    |
| crm1-interval-ex-r0-reviewer-medium-a1 | correct | 485.3s | 469.6s | 15.7s        | 14       | 0       | 1       | 0         | 0                    |
| crm1-interval-ex-r1-reviewer-high-a1   | correct | 770.3s | 755.9s | 14.4s        | 21       | 2       | 1       | 0         | 0                    |
| crm1-interval-ex-r1-reviewer-medium-a1 | correct | 483.7s | 471.5s | 12.2s        | 16       | 0       | 1       | 0         | 0                    |
| crm1-interval-go-r0-reviewer-high-a1   | correct | 530.9s | 520s   | 10.9s        | 14       | 0       | 1       | 0         | 0                    |
| crm1-interval-go-r0-reviewer-medium-a1 | correct | 403s   | 395.1s | 7.9s         | 10       | 0       | 1       | 0         | 0                    |
| crm1-interval-go-r1-reviewer-high-a1   | correct | 606.8s | 598.4s | 8.4s         | 17       | 1       | 1       | 0         | 0                    |
| crm1-interval-go-r1-reviewer-medium-a1 | correct | 378.5s | 368.8s | 9.7s         | 11       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 2.00M, cached 0.26M, output 76.9k, reasoning 13.5k, input_tokens_details.cache_write_tokens 0, total_tokens 2.08M
reviewer-medium openai: input 1.46M, cached 0.25M, output 46.1k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.51M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 0.69M, cached 0.20M, output 31.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
stage build reviewer-medium openai (responses): input 0.73M, cached 0.22M, output 27.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.76M
stage review reviewer-high openai (responses): input 1.31M, cached 59.6k, output 45.6k, reasoning 13.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.36M
stage review reviewer-medium openai (responses): input 0.73M, cached 25.5k, output 18.8k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.75M
native usage by attempt and provider:
attempt usage crm1-deps-ex-r0-reviewer-high-a1 openai (responses): input 0.36M, cached 86.7k, output 11.2k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage crm1-deps-ex-r0-reviewer-medium-a1 openai (responses): input 0.18M, cached 11.3k, output 6.6k, reasoning 376, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage crm1-deps-ex-r1-reviewer-high-a1 openai (responses): input 0.40M, cached 27.5k, output 12.8k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage crm1-deps-ex-r1-reviewer-medium-a1 openai (responses): input 0.48M, cached 0.15M, output 9.8k, reasoning 218, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage crm1-deps-go-r0-reviewer-high-a1 openai (responses): input 0.16M, cached 12.2k, output 7.0k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage crm1-deps-go-r0-reviewer-medium-a1 openai (responses): input 0.12M, cached 6.4k, output 4.9k, reasoning 237, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage crm1-deps-go-r1-reviewer-high-a1 openai (responses): input 0.14M, cached 23.7k, output 7.4k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage crm1-deps-go-r1-reviewer-medium-a1 openai (responses): input 0.11M, cached 16.9k, output 5.4k, reasoning 178, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage crm1-interval-ex-r0-reviewer-high-a1 openai (responses): input 0.27M, cached 8.4k, output 10.1k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage crm1-interval-ex-r0-reviewer-medium-a1 openai (responses): input 0.15M, cached 21.8k, output 5.1k, reasoning 123, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage crm1-interval-ex-r1-reviewer-high-a1 openai (responses): input 0.29M, cached 81.4k, output 11.1k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage crm1-interval-ex-r1-reviewer-medium-a1 openai (responses): input 0.20M, cached 30.6k, output 4.6k, reasoning 247, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage crm1-interval-go-r0-reviewer-high-a1 openai (responses): input 0.18M, cached 0, output 7.0k, reasoning 923, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage crm1-interval-go-r0-reviewer-medium-a1 openai (responses): input 0.10M, cached 11.5k, output 4.3k, reasoning 158, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage crm1-interval-go-r1-reviewer-high-a1 openai (responses): input 0.19M, cached 23.9k, output 10.1k, reasoning 988, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage crm1-interval-go-r1-reviewer-medium-a1 openai (responses): input 0.12M, cached 0, output 5.5k, reasoning 115, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt outcomes included: reviewer-high: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 8241.3s, model 7818.4s, tools/checks 422.9s, requests 266
builder settings: reviewer-high openai gpt-6-luna reasoning.effort=low; reviewer-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant reviewer-medium differs from reviewer-high in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.reviewer.effort: exercised in 8 of 8 reviewer-medium attempts
first position per task: deps-ex reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: deps-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: interval-ex reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: interval-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
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
