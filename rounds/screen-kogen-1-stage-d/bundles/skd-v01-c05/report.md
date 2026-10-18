incomplete: 3 of 8 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (3 of 8 cells scored)
## CMP-1 Correctness
| variant             | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v01-verify-off      | 0       | 0         | 1                | 0              | 1          | 0%           | 0 of 0        | 0           |
| c05-review-advisory | 2       | 0         | 0                | 0              | 0          | 100%         | 0 of 2        | 0           |
false success: 0 of 0 claims (v01-verify-off)
false success: 0 of 2 claims (c05-review-advisory)
shaping outcomes:
v01-verify-off: shaping ready 2, shaping failed 0; correct 0 of 1
c05-review-advisory: shaping ready 2, shaping failed 0; correct 2 of 2
## Per-task outcomes
| task      | variant             | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|---------------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | v01-verify-off      | 0       | 0         | 1                | 0              | 0          |
| ledger-ex | c05-review-advisory | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | v01-verify-off      | 0       | 0         | 0                | 0              | 0          |
| r70-5-go  | c05-review-advisory | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | v01-verify-off      | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | c05-review-advisory | 0       | 0         | 0                | 0              | 0          |
| rate-go   | v01-verify-off      | 0       | 0         | 0                | 0              | 1          |
| rate-go   | c05-review-advisory | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant             | stage      | wall   | model  | tools/checks | requests |
|---------------------|------------|--------|--------|--------------|----------|
| v01-verify-off      | shape      | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | plan       | 14.6s  | 14.6s  | 0ms          | 2        |
| v01-verify-off      | build      | 330.8s | 286.5s | 44.3s        | 44       |
| v01-verify-off      | verify     | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | review     | 216.7s | 216.7s | 0ms          | 40       |
| v01-verify-off      | commit     | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| v01-verify-off      | assessment | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | shape      | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | plan       | 14.7s  | 14.7s  | 0ms          | 2        |
| c05-review-advisory | build      | 122.8s | 110.2s | 12.6s        | 14       |
| c05-review-advisory | verify     | 997ms  | 0ms    | 997ms        | 0        |
| c05-review-advisory | review     | 25.8s  | 25.8s  | 0ms          | 4        |
| c05-review-advisory | commit     | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| c05-review-advisory | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skd-v01-c05-ledger-ex-r0-c05-review-advisory-a1 | correct          | 73.8s  | 65.3s  | 8.5s         | 9        | 0       | 1       | 0         | 0                    |
| skd-v01-c05-ledger-ex-r0-v01-verify-off-a1      | workflow failure | 359.3s | 330.7s | 28.6s        | 54       | 6       | 7       | 0         | 0                    |
| skd-v01-c05-rate-go-r0-c05-review-advisory-a1   | correct          | 93.9s  | 85.4s  | 8.6s         | 11       | 0       | 1       | 0         | 0                    |
| skd-v01-c05-rate-go-r0-v01-verify-off-a1        | incomplete       | 208.5s | 187.2s | 21.3s        | 32       | 4       | 4       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
c05-review-advisory openai: input 0.11M, cached 14.7k, output 4.5k, reasoning 67, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
v01-verify-off openai: input 0.64M, cached 0.13M, output 12.1k, reasoning 822, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
native usage by stage and provider:
stage build c05-review-advisory openai (responses): input 73.2k, cached 14.7k, output 3.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 76.8k
stage build v01-verify-off openai (responses): input 0.38M, cached 0.12M, output 8.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
stage plan c05-review-advisory openai (responses): input 5.2k, cached 0, output 321, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 5.5k
stage plan v01-verify-off openai (responses): input 5.2k, cached 0, output 520, reasoning 207, input_tokens_details.cache_write_tokens 0, total_tokens 5.7k
stage review c05-review-advisory openai (responses): input 26.9k, cached 0, output 548, reasoning 67, input_tokens_details.cache_write_tokens 0, total_tokens 27.5k
stage review v01-verify-off openai (responses): input 0.25M, cached 5.2k, output 3.4k, reasoning 615, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
native usage by attempt and provider:
attempt usage skd-v01-c05-ledger-ex-r0-c05-review-advisory-a1 openai (responses): input 48.8k, cached 8.8k, output 1.9k, reasoning 32, input_tokens_details.cache_write_tokens 0, total_tokens 50.6k
attempt usage skd-v01-c05-ledger-ex-r0-v01-verify-off-a1 openai (responses): input 0.43M, cached 0.10M, output 7.5k, reasoning 434, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage skd-v01-c05-rate-go-r0-c05-review-advisory-a1 openai (responses): input 56.5k, cached 5.9k, output 2.6k, reasoning 35, input_tokens_details.cache_write_tokens 0, total_tokens 59.1k
attempt usage skd-v01-c05-rate-go-r0-v01-verify-off-a1 openai (responses): input 0.21M, cached 25.9k, output 4.6k, reasoning 388, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt outcomes included: v01-verify-off: correct 0, incorrect 0, workflow failure 1, infrastructure 0, incomplete 1; c05-review-advisory: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 735.5s, model 668.5s, tools/checks 67s, requests 106
builder settings: v01-verify-off openai gpt-6-luna reasoning.effort=low
builder settings: c05-review-advisory openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 4, scored 3, incorrect 0, infrastructure 0, incomplete 1
variant c05-review-advisory differs from v01-verify-off in:
  review.effect: blocking -> advisory
  verify.enabled: false -> true
review returned changes in 2 of 2 v01-verify-off attempts
V01: exercised in 2 of 2 c05-review-advisory attempts
first position per task: ledger-ex v01-verify-off 1, c05-review-advisory 0 (1 repetitions, 2 variants)
first position per task: r70-5-go v01-verify-off 1, c05-review-advisory 0 (1 repetitions, 2 variants)
first position per task: r70-7-go v01-verify-off 0, c05-review-advisory 1 (1 repetitions, 2 variants)
first position per task: rate-go v01-verify-off 0, c05-review-advisory 1 (1 repetitions, 2 variants)
v01-verify-off: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, verify.enabled)
c05-review-advisory: not the Kogen profile (differs in review.effect, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
v01-verify-off: repair.context = packet,diff,check_results,review_findings (extension)
v01-verify-off: repair.roles = builder (extension)
v01-verify-off: shape.critique_prompt = lab:critique (extension)
v01-verify-off: shape.critique_rounds = 1 (extension)
c05-review-advisory: repair.context = packet,diff,check_results,review_findings (extension)
c05-review-advisory: repair.roles = builder (extension)
c05-review-advisory: review.effect = advisory (extension)
c05-review-advisory: shape.critique_prompt = lab:critique (extension)
c05-review-advisory: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
