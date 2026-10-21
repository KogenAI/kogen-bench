complete: 24/24 cells scored
Question: confirm-reviewer-medium-2: on fresh tasks with a weak builder, does a Sol-medium reviewer-fixer rescue wrong trees as reliably as Sol high, with no more wrong submissions, at no more than 70% of its reviewer input?
Hypothesis: reviewer-medium rescues at least the same share of wrong trees as reviewer-high at most 70% of its reviewer input
Purpose: confirmation
Objective: cost_at_quality
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| reviewer-high   | 9       | 0         | 3                | 0              | 0          | 75%          | 0 of 9        | 0           |
| reviewer-medium | 11      | 0         | 1                | 0              | 0          | 91.7%        | 0 of 11       | 0           |
false success: 0 of 9 claims (reviewer-high)
false success: 0 of 11 claims (reviewer-medium)
shaping outcomes:
reviewer-high: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
reviewer-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task      | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|-----------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | reviewer-high   | 1       | 0         | 2                | 0              | 0          |
| ledger-ex | reviewer-medium | 2       | 0         | 1                | 0              | 0          |
| ledger-go | reviewer-high   | 3       | 0         | 0                | 0              | 0          |
| ledger-go | reviewer-medium | 3       | 0         | 0                | 0              | 0          |
| wrap-ex   | reviewer-high   | 2       | 0         | 1                | 0              | 0          |
| wrap-ex   | reviewer-medium | 3       | 0         | 0                | 0              | 0          |
| wrap-go   | reviewer-high   | 3       | 0         | 0                | 0              | 0          |
| wrap-go   | reviewer-medium | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| reviewer-high   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | build      | 3833.9s | 3692.7s | 141.2s       | 194      |
| reviewer-high   | verify     | 34.7s   | 0ms     | 34.7s        | 0        |
| reviewer-high   | review     | 2106.2s | 2106.2s | 0ms          | 88       |
| reviewer-high   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-high   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | build      | 4606.8s | 4495.9s | 110.8s       | 190      |
| reviewer-medium | verify     | 45.2s   | 0ms     | 45.2s        | 0        |
| reviewer-medium | review     | 1606.9s | 1606.9s | 0ms          | 85       |
| reviewer-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| crm2-ledger-ex-r0-reviewer-high-a1   | workflow failure | 1185.4s | 1158.3s | 27.1s        | 42       | 6       | 0       | 0         | 0                    |
| crm2-ledger-ex-r0-reviewer-medium-a1 | correct          | 514.5s  | 491.4s  | 23.1s        | 23       | 2       | 1       | 0         | 0                    |
| crm2-ledger-ex-r1-reviewer-high-a1   | correct          | 497.4s  | 475.7s  | 21.7s        | 22       | 0       | 1       | 0         | 0                    |
| crm2-ledger-ex-r1-reviewer-medium-a1 | workflow failure | 1232.3s | 1212.9s | 19.4s        | 38       | 5       | 0       | 0         | 0                    |
| crm2-ledger-ex-r2-reviewer-high-a1   | workflow failure | 462.5s  | 447.8s  | 14.7s        | 24       | 5       | 0       | 0         | 0                    |
| crm2-ledger-ex-r2-reviewer-medium-a1 | correct          | 1267.7s | 1231.5s | 36.2s        | 46       | 3       | 2       | 0         | 0                    |
| crm2-ledger-go-r0-reviewer-high-a1   | correct          | 702.4s  | 689.7s  | 12.7s        | 20       | 1       | 1       | 0         | 0                    |
| crm2-ledger-go-r0-reviewer-medium-a1 | correct          | 395.2s  | 377.2s  | 18s          | 20       | 2       | 1       | 0         | 0                    |
| crm2-ledger-go-r1-reviewer-high-a1   | correct          | 389.2s  | 371.4s  | 17.8s        | 17       | 1       | 1       | 0         | 0                    |
| crm2-ledger-go-r1-reviewer-medium-a1 | correct          | 855.8s  | 844.1s  | 11.6s        | 21       | 0       | 1       | 0         | 0                    |
| crm2-ledger-go-r2-reviewer-high-a1   | correct          | 526s    | 514.6s  | 11.4s        | 14       | 0       | 1       | 0         | 0                    |
| crm2-ledger-go-r2-reviewer-medium-a1 | correct          | 263.1s  | 248.8s  | 14.3s        | 11       | 0       | 1       | 0         | 0                    |
| crm2-wrap-ex-r0-reviewer-high-a1     | correct          | 399.6s  | 364s    | 35.6s        | 30       | 1       | 1       | 0         | 0                    |
| crm2-wrap-ex-r0-reviewer-medium-a1   | correct          | 199.9s  | 183.3s  | 16.5s        | 16       | 0       | 1       | 0         | 0                    |
| crm2-wrap-ex-r1-reviewer-high-a1     | correct          | 441.2s  | 404.8s  | 36.4s        | 30       | 3       | 1       | 0         | 0                    |
| crm2-wrap-ex-r1-reviewer-medium-a1   | correct          | 271.2s  | 257.9s  | 13.3s        | 27       | 3       | 1       | 0         | 0                    |
| crm2-wrap-ex-r2-reviewer-high-a1     | workflow failure | 412.6s  | 394.8s  | 17.8s        | 45       | 6       | 0       | 0         | 0                    |
| crm2-wrap-ex-r2-reviewer-medium-a1   | correct          | 256.8s  | 239.4s  | 17.5s        | 23       | 2       | 1       | 0         | 0                    |
| crm2-wrap-go-r0-reviewer-high-a1     | correct          | 518.4s  | 501.6s  | 16.8s        | 14       | 0       | 1       | 0         | 0                    |
| crm2-wrap-go-r0-reviewer-medium-a1   | correct          | 391.5s  | 376.9s  | 14.5s        | 21       | 1       | 1       | 0         | 0                    |
| crm2-wrap-go-r1-reviewer-high-a1     | correct          | 216.7s  | 205.3s  | 11.4s        | 13       | 0       | 1       | 0         | 0                    |
| crm2-wrap-go-r1-reviewer-medium-a1   | correct          | 443.7s  | 430.9s  | 12.8s        | 14       | 0       | 1       | 0         | 0                    |
| crm2-wrap-go-r2-reviewer-high-a1     | correct          | 280.6s  | 270.9s  | 9.7s         | 11       | 0       | 1       | 0         | 0                    |
| crm2-wrap-go-r2-reviewer-medium-a1   | correct          | 225.3s  | 208.3s  | 16.9s        | 15       | 1       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
reviewer-high openai: input 4.77M, cached 1.42M, output 0.14M, reasoning 15.0k, input_tokens_details.cache_write_tokens 0, total_tokens 4.91M
reviewer-medium openai: input 4.18M, cached 1.33M, output 0.12M, reasoning 5.5k, input_tokens_details.cache_write_tokens 0, total_tokens 4.30M
native usage by stage and provider:
stage build reviewer-high openai (responses): input 3.20M, cached 1.36M, output 82.9k, reasoning 97, input_tokens_details.cache_write_tokens 0, total_tokens 3.28M
stage build reviewer-medium openai (responses): input 2.85M, cached 1.27M, output 85.3k, reasoning 144, input_tokens_details.cache_write_tokens 0, total_tokens 2.93M
stage review reviewer-high openai (responses): input 1.57M, cached 61.3k, output 58.9k, reasoning 14.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.63M
stage review reviewer-medium openai (responses): input 1.33M, cached 60.9k, output 38.9k, reasoning 5.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.36M
native usage by attempt and provider:
attempt usage crm2-ledger-ex-r0-reviewer-high-a1 openai (responses): input 0.85M, cached 0.41M, output 18.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.87M
attempt usage crm2-ledger-ex-r0-reviewer-medium-a1 openai (responses): input 0.34M, cached 0.12M, output 14.9k, reasoning 909, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage crm2-ledger-ex-r1-reviewer-high-a1 openai (responses): input 0.34M, cached 86.5k, output 11.4k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage crm2-ledger-ex-r1-reviewer-medium-a1 openai (responses): input 0.98M, cached 0.38M, output 27.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
attempt usage crm2-ledger-ex-r2-reviewer-high-a1 openai (responses): input 0.39M, cached 0.13M, output 14.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage crm2-ledger-ex-r2-reviewer-medium-a1 openai (responses): input 0.78M, cached 0.39M, output 14.4k, reasoning 378, input_tokens_details.cache_write_tokens 0, total_tokens 0.80M
attempt usage crm2-ledger-go-r0-reviewer-high-a1 openai (responses): input 0.29M, cached 46.3k, output 13.0k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage crm2-ledger-go-r0-reviewer-medium-a1 openai (responses): input 0.27M, cached 24.2k, output 9.1k, reasoning 462, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage crm2-ledger-go-r1-reviewer-high-a1 openai (responses): input 0.26M, cached 40.4k, output 11.2k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage crm2-ledger-go-r1-reviewer-medium-a1 openai (responses): input 0.29M, cached 97.2k, output 11.5k, reasoning 606, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage crm2-ledger-go-r2-reviewer-high-a1 openai (responses): input 0.23M, cached 25.6k, output 10.2k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage crm2-ledger-go-r2-reviewer-medium-a1 openai (responses): input 0.16M, cached 21.4k, output 6.3k, reasoning 442, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage crm2-wrap-ex-r0-reviewer-high-a1 openai (responses): input 0.42M, cached 63.0k, output 13.8k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage crm2-wrap-ex-r0-reviewer-medium-a1 openai (responses): input 0.18M, cached 38.5k, output 6.6k, reasoning 793, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage crm2-wrap-ex-r1-reviewer-high-a1 openai (responses): input 0.45M, cached 0.14M, output 15.1k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage crm2-wrap-ex-r1-reviewer-medium-a1 openai (responses): input 0.38M, cached 50.9k, output 9.0k, reasoning 636, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
attempt usage crm2-wrap-ex-r2-reviewer-high-a1 openai (responses): input 1.10M, cached 0.47M, output 13.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.11M
attempt usage crm2-wrap-ex-r2-reviewer-medium-a1 openai (responses): input 0.29M, cached 87.6k, output 8.3k, reasoning 487, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage crm2-wrap-go-r0-reviewer-high-a1 openai (responses): input 0.16M, cached 0, output 7.8k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage crm2-wrap-go-r0-reviewer-medium-a1 openai (responses): input 0.20M, cached 47.7k, output 5.9k, reasoning 272, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage crm2-wrap-go-r1-reviewer-high-a1 openai (responses): input 0.15M, cached 13.4k, output 6.7k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage crm2-wrap-go-r1-reviewer-medium-a1 openai (responses): input 0.14M, cached 22.0k, output 5.0k, reasoning 280, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage crm2-wrap-go-r2-reviewer-high-a1 openai (responses): input 0.13M, cached 5.5k, output 6.1k, reasoning 790, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage crm2-wrap-go-r2-reviewer-medium-a1 openai (responses): input 0.14M, cached 48.8k, output 6.0k, reasoning 284, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt outcomes included: reviewer-high: correct 9, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0; reviewer-medium: correct 11, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 12348.9s, model 11901.7s, tools/checks 447.2s, requests 557
builder settings: reviewer-high openai gpt-6-luna reasoning.effort=low; reviewer-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 24, scored 24, incorrect 0, infrastructure 0, incomplete 0
variant reviewer-medium differs from reviewer-high in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.reviewer.effort: exercised in 12 of 12 reviewer-medium attempts
first position per task: ledger-ex reviewer-high 2, reviewer-medium 1 (3 repetitions, 2 variants)
first position per task: ledger-go reviewer-high 1, reviewer-medium 2 (3 repetitions, 2 variants)
first position per task: wrap-ex reviewer-high 2, reviewer-medium 1 (3 repetitions, 2 variants)
first position per task: wrap-go reviewer-high 2, reviewer-medium 1 (3 repetitions, 2 variants)
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
