complete: 16/16 cells scored
Question: reviewer-polish-1: with the default Sol-medium builder, does a Sol-medium reviewer-fixer edit correct trees more often than Sol high, and does that cancel its reviewer-input saving?
Hypothesis: exploratory: medium edits more correct trees; reviewer input not lower
Purpose: development
Objective: correctness
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
| reviewer-high   | build      | 2196.1s | 2144.3s | 51.8s        | 66       |
| reviewer-high   | verify     | 21.5s   | 0ms     | 21.5s        | 0        |
| reviewer-high   | review     | 711.1s  | 711.1s  | 0ms          | 38       |
| reviewer-high   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | build      | 2206.1s | 2149.9s | 56.3s        | 65       |
| reviewer-medium | verify     | 28.1s   | 0ms     | 28.1s        | 0        |
| reviewer-medium | review     | 463s    | 463s    | 0ms          | 38       |
| reviewer-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rp1-deps-ex-r0-reviewer-high-a1       | correct | 294.8s | 272.2s | 22.6s        | 13       | 0       | 1       | 0         | 0                    |
| rp1-deps-ex-r0-reviewer-medium-a1     | correct | 289.9s | 245.2s | 44.7s        | 14       | 0       | 1       | 0         | 0                    |
| rp1-deps-ex-r1-reviewer-high-a1       | correct | 218.8s | 200.8s | 17.9s        | 12       | 0       | 1       | 0         | 0                    |
| rp1-deps-ex-r1-reviewer-medium-a1     | correct | 194.7s | 180.3s | 14.4s        | 12       | 0       | 1       | 0         | 0                    |
| rp1-deps-go-r0-reviewer-high-a1       | correct | 382.1s | 369.3s | 12.8s        | 11       | 0       | 1       | 0         | 0                    |
| rp1-deps-go-r0-reviewer-medium-a1     | correct | 339.1s | 327.5s | 11.7s        | 10       | 0       | 1       | 0         | 0                    |
| rp1-deps-go-r1-reviewer-high-a1       | correct | 425.7s | 416.3s | 9.3s         | 14       | 0       | 1       | 0         | 0                    |
| rp1-deps-go-r1-reviewer-medium-a1     | correct | 376.8s | 367.3s | 9.5s         | 12       | 0       | 1       | 0         | 0                    |
| rp1-interval-ex-r0-reviewer-high-a1   | correct | 439.1s | 416.3s | 22.7s        | 16       | 1       | 1       | 0         | 0                    |
| rp1-interval-ex-r0-reviewer-medium-a1 | correct | 395.1s | 378.8s | 16.3s        | 13       | 0       | 1       | 0         | 0                    |
| rp1-interval-ex-r1-reviewer-high-a1   | correct | 406.8s | 392.4s | 14.4s        | 12       | 0       | 1       | 0         | 0                    |
| rp1-interval-ex-r1-reviewer-medium-a1 | correct | 389.7s | 376.5s | 13.1s        | 15       | 0       | 1       | 0         | 0                    |
| rp1-interval-go-r0-reviewer-high-a1   | correct | 431s   | 419.9s | 11.1s        | 14       | 0       | 1       | 0         | 0                    |
| rp1-interval-go-r0-reviewer-medium-a1 | correct | 350.9s | 342.7s | 8.2s         | 13       | 0       | 1       | 0         | 0                    |
| rp1-interval-go-r1-reviewer-high-a1   | correct | 376.4s | 368.1s | 8.2s         | 12       | 0       | 1       | 0         | 0                    |
| rp1-interval-go-r1-reviewer-medium-a1 | correct | 405.6s | 394.6s | 11s          | 14       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 1.20M, cached 0.12M, output 43.6k, reasoning 6.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.24M
reviewer-medium openai: input 1.15M, cached 0.14M, output 37.4k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.18M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 0.62M, cached 0.11M, output 34.4k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.66M
stage build reviewer-medium openai (responses): input 0.60M, cached 0.13M, output 34.6k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.64M
stage review reviewer-high openai (responses): input 0.58M, cached 15.9k, output 9.3k, reasoning 4.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
stage review reviewer-medium openai (responses): input 0.54M, cached 13.6k, output 2.8k, reasoning 912, input_tokens_details.cache_write_tokens 0, total_tokens 0.55M
native usage by attempt and provider:
attempt usage rp1-deps-ex-r0-reviewer-high-a1 openai (responses): input 0.15M, cached 16.9k, output 5.1k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rp1-deps-ex-r0-reviewer-medium-a1 openai (responses): input 0.16M, cached 23.9k, output 4.8k, reasoning 688, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rp1-deps-ex-r1-reviewer-high-a1 openai (responses): input 0.13M, cached 11.3k, output 5.6k, reasoning 850, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rp1-deps-ex-r1-reviewer-medium-a1 openai (responses): input 0.13M, cached 5.6k, output 4.0k, reasoning 410, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rp1-deps-go-r0-reviewer-high-a1 openai (responses): input 0.13M, cached 5.6k, output 5.9k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rp1-deps-go-r0-reviewer-medium-a1 openai (responses): input 0.11M, cached 5.6k, output 4.0k, reasoning 158, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rp1-deps-go-r1-reviewer-high-a1 openai (responses): input 0.16M, cached 12.4k, output 5.9k, reasoning 775, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rp1-deps-go-r1-reviewer-medium-a1 openai (responses): input 0.13M, cached 5.6k, output 4.9k, reasoning 271, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rp1-interval-ex-r0-reviewer-high-a1 openai (responses): input 0.20M, cached 50.4k, output 5.5k, reasoning 762, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rp1-interval-ex-r0-reviewer-medium-a1 openai (responses): input 0.15M, cached 42.4k, output 4.9k, reasoning 371, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage rp1-interval-ex-r1-reviewer-high-a1 openai (responses): input 0.13M, cached 11.5k, output 4.6k, reasoning 600, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage rp1-interval-ex-r1-reviewer-medium-a1 openai (responses): input 0.17M, cached 17.3k, output 4.7k, reasoning 313, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rp1-interval-go-r0-reviewer-high-a1 openai (responses): input 0.16M, cached 8.7k, output 5.6k, reasoning 663, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rp1-interval-go-r0-reviewer-medium-a1 openai (responses): input 0.14M, cached 41.3k, output 4.7k, reasoning 268, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage rp1-interval-go-r1-reviewer-high-a1 openai (responses): input 0.14M, cached 5.8k, output 5.3k, reasoning 652, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rp1-interval-go-r1-reviewer-medium-a1 openai (responses): input 0.16M, cached 0, output 5.5k, reasoning 316, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt outcomes included: reviewer-high: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5716.3s, model 5468.2s, tools/checks 248.1s, requests 207
builder settings: reviewer-high openai gpt-6.1-sol reasoning.effort=medium; reviewer-medium openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant reviewer-medium differs from reviewer-high in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.reviewer.effort: exercised in 8 of 8 reviewer-medium attempts
first position per task: deps-ex reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: deps-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: interval-ex reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
first position per task: interval-go reviewer-high 1, reviewer-medium 1 (2 repetitions, 2 variants)
reviewer-high: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
reviewer-medium: not the Kogen profile (differs in roles.reviewer.effort, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
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
