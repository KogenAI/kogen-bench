complete: 8/8 cells scored
Question: With planner and builder on gpt-6-luna low, does the reviewer's model and effort decide whether review approves within 12 repairs on r70-5-go and r70-7-go?
Hypothesis: Luna low does not converge; at least one stronger reviewer setting converges on both tasks
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| rev-luna-low  | 0       | 0         | 2                | 0              | 0          | 0%           | 0 of 0        | 0           |
| rev-luna-high | 1       | 1         | 0                | 0              | 0          | 50%          | 1 of 2        | 0           |
| rev-sol-low   | 2       | 0         | 0                | 0              | 0          | 100%         | 0 of 2        | 0           |
| rev-sol-high  | 2       | 0         | 0                | 0              | 0          | 100%         | 0 of 2        | 0           |
false success: 0 of 0 claims (rev-luna-low)
false success: 1 of 2 claims (rev-luna-high)
false success: 0 of 2 claims (rev-sol-low)
false success: 0 of 2 claims (rev-sol-high)
shaping outcomes:
rev-luna-low: shaping ready 2, shaping failed 0; correct 0 of 2
rev-luna-high: shaping ready 2, shaping failed 0; correct 1 of 2
rev-sol-low: shaping ready 2, shaping failed 0; correct 2 of 2
rev-sol-high: shaping ready 2, shaping failed 0; correct 2 of 2
## Per-task outcomes
| task     | variant       | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------|---------------|---------|-----------|------------------|----------------|------------|
| r70-5-go | rev-luna-low  | 0       | 0         | 1                | 0              | 0          |
| r70-5-go | rev-luna-high | 0       | 1         | 0                | 0              | 0          |
| r70-5-go | rev-sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go | rev-sol-high  | 1       | 0         | 0                | 0              | 0          |
| r70-7-go | rev-luna-low  | 0       | 0         | 1                | 0              | 0          |
| r70-7-go | rev-luna-high | 1       | 0         | 0                | 0              | 0          |
| r70-7-go | rev-sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go | rev-sol-high  | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant       | stage      | wall    | model   | tools/checks | requests |
|---------------|------------|---------|---------|--------------|----------|
| rev-luna-low  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-low  | plan       | 21.5s   | 21.5s   | 0ms          | 2        |
| rev-luna-low  | build      | 1234.4s | 1201.1s | 33.4s        | 77       |
| rev-luna-low  | verify     | 14.4s   | 0ms     | 14.4s        | 0        |
| rev-luna-low  | review     | 420.8s  | 420.8s  | 0ms          | 31       |
| rev-luna-low  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-low  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-low  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-high | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-high | plan       | 21.1s   | 21.1s   | 0ms          | 2        |
| rev-luna-high | build      | 542.8s  | 526.2s  | 16.7s        | 36       |
| rev-luna-high | verify     | 3.4s    | 0ms     | 3.4s         | 0        |
| rev-luna-high | review     | 376.9s  | 376.9s  | 0ms          | 17       |
| rev-luna-high | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-high | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-luna-high | assessment | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-low   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-low   | plan       | 32.1s   | 32.1s   | 0ms          | 2        |
| rev-sol-low   | build      | 337.2s  | 322.1s  | 15.1s        | 19       |
| rev-sol-low   | verify     | 1.7s    | 0ms     | 1.7s         | 0        |
| rev-sol-low   | review     | 72.5s   | 72.5s   | 0ms          | 7        |
| rev-sol-low   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-low   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-low   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high  | plan       | 18.6s   | 18.6s   | 0ms          | 2        |
| rev-sol-high  | build      | 434.7s  | 406.1s  | 28.6s        | 40       |
| rev-sol-high  | verify     | 2s      | 0ms     | 2s           | 0        |
| rev-sol-high  | review     | 169.5s  | 169.5s  | 0ms          | 13       |
| rev-sol-high  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                           | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| review-convergence-1-r70-5-go-r0-rev-luna-high-a1 | incorrect        | 763.9s  | 750.4s  | 13.5s        | 45       | 5       | 6       | 0         | 0                    |
| review-convergence-1-r70-5-go-r0-rev-luna-low-a1  | workflow failure | 555.9s  | 531.7s  | 24.2s        | 46       | 12      | 13      | 0         | 0                    |
| review-convergence-1-r70-5-go-r0-rev-sol-high-a1  | correct          | 496.9s  | 473s    | 23.9s        | 45       | 2       | 3       | 0         | 0                    |
| review-convergence-1-r70-5-go-r0-rev-sol-low-a1   | correct          | 304.7s  | 295.1s  | 9.6s         | 18       | 1       | 2       | 0         | 0                    |
| review-convergence-1-r70-7-go-r0-rev-luna-high-a1 | correct          | 189.9s  | 173.8s  | 16.1s        | 10       | 0       | 1       | 0         | 0                    |
| review-convergence-1-r70-7-go-r0-rev-luna-low-a1  | workflow failure | 1145.9s | 1111.8s | 34.1s        | 64       | 12      | 14      | 0         | 0                    |
| review-convergence-1-r70-7-go-r0-rev-sol-high-a1  | correct          | 137.4s  | 121.2s  | 16.2s        | 10       | 0       | 1       | 0         | 0                    |
| review-convergence-1-r70-7-go-r0-rev-sol-low-a1   | correct          | 148.2s  | 131.6s  | 16.5s        | 10       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
rev-luna-high openai: input 0.72M, cached 0.15M, output 24.0k, reasoning 11.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.75M
rev-luna-low openai: input 1.62M, cached 0.55M, output 28.2k, reasoning 326, input_tokens_details.cache_write_tokens 0, total_tokens 1.65M
rev-sol-high openai: input 0.69M, cached 0.17M, output 14.0k, reasoning 2.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
rev-sol-low openai: input 0.28M, cached 33.5k, output 6.8k, reasoning 116, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
native usage by stage and provider:
stage build rev-luna-high openai (responses): input 0.44M, cached 0.14M, output 10.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.45M
stage build rev-luna-low openai (responses): input 1.14M, cached 0.50M, output 21.5k, reasoning 326, input_tokens_details.cache_write_tokens 0, total_tokens 1.16M
stage build rev-sol-high openai (responses): input 0.47M, cached 0.17M, output 9.5k, reasoning 101, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
stage build rev-sol-low openai (responses): input 0.16M, cached 33.5k, output 5.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
stage plan rev-luna-high openai (responses): input 8.6k, cached 0, output 552, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 9.1k
stage plan rev-luna-low openai (responses): input 8.6k, cached 0, output 470, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 9.0k
stage plan rev-sol-high openai (responses): input 8.6k, cached 0, output 422, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 9.0k
stage plan rev-sol-low openai (responses): input 8.6k, cached 0, output 362, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 8.9k
stage review rev-luna-high openai (responses): input 0.28M, cached 17.2k, output 13.1k, reasoning 11.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
stage review rev-luna-low openai (responses): input 0.47M, cached 45.6k, output 6.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
stage review rev-sol-high openai (responses): input 0.21M, cached 0, output 4.0k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
stage review rev-sol-low openai (responses): input 0.11M, cached 0, output 792, reasoning 116, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
native usage by attempt and provider:
attempt usage review-convergence-1-r70-5-go-r0-rev-luna-high-a1 openai (responses): input 0.64M, cached 0.15M, output 19.3k, reasoning 10.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
attempt usage review-convergence-1-r70-5-go-r0-rev-luna-low-a1 openai (responses): input 0.60M, cached 0.19M, output 8.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.61M
attempt usage review-convergence-1-r70-5-go-r0-rev-sol-high-a1 openai (responses): input 0.60M, cached 0.16M, output 11.3k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.61M
attempt usage review-convergence-1-r70-5-go-r0-rev-sol-low-a1 openai (responses): input 0.18M, cached 28.8k, output 4.2k, reasoning 80, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage review-convergence-1-r70-7-go-r0-rev-luna-high-a1 openai (responses): input 89.2k, cached 0, output 4.6k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 93.8k
attempt usage review-convergence-1-r70-7-go-r0-rev-luna-low-a1 openai (responses): input 1.02M, cached 0.36M, output 19.5k, reasoning 326, input_tokens_details.cache_write_tokens 0, total_tokens 1.04M
attempt usage review-convergence-1-r70-7-go-r0-rev-sol-high-a1 openai (responses): input 91.3k, cached 6.5k, output 2.7k, reasoning 313, input_tokens_details.cache_write_tokens 0, total_tokens 94.0k
attempt usage review-convergence-1-r70-7-go-r0-rev-sol-low-a1 openai (responses): input 97.4k, cached 4.7k, output 2.5k, reasoning 36, input_tokens_details.cache_write_tokens 0, total_tokens 100.0k
attempt outcomes included: rev-luna-low: correct 0, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0; rev-luna-high: correct 1, incorrect 1, workflow failure 0, infrastructure 0, incomplete 0; rev-sol-low: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; rev-sol-high: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 3742.7s, model 3588.5s, tools/checks 154.2s, requests 248
builder settings: rev-luna-low openai gpt-6-luna reasoning.effort=low
builder settings: rev-luna-high openai gpt-6-luna reasoning.effort=low
builder settings: rev-sol-low openai gpt-6-luna reasoning.effort=low
builder settings: rev-sol-high openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 1, infrastructure 0, incomplete 0
variant rev-luna-high differs from rev-luna-low in:
  roles.reviewer: openai gpt-6-luna low -> openai gpt-6-luna high
variant rev-sol-low differs from rev-luna-low in:
  roles.reviewer: openai gpt-6-luna low -> openai gpt-6.1-sol low
variant rev-sol-high differs from rev-luna-low in:
  roles.reviewer: openai gpt-6-luna low -> openai gpt-6.1-sol high
  roles.reviewer: openai gpt-6-luna low -> openai gpt-6.1-sol high
roles.reviewer.effort: exercised in 2 of 2 rev-luna-high attempts
roles.reviewer.model: exercised in 2 of 2 rev-sol-low attempts
roles.reviewer.effort: exercised in 2 of 2 rev-sol-high attempts
roles.reviewer.model: exercised in 2 of 2 rev-sol-high attempts
first position per task: r70-5-go rev-luna-low 1, rev-luna-high 0, rev-sol-low 0, rev-sol-high 0 (1 repetitions, 4 variants)
first position per task: r70-7-go rev-luna-low 0, rev-luna-high 1, rev-sol-low 0, rev-sol-high 0 (1 repetitions, 4 variants)
rev-luna-low: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.reviewer.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs)
rev-luna-high: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs)
rev-sol-low: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs)
rev-sol-high: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs)
experimental stop: every variant has stop.max_repairs = 12; no variant matches the Kogen profile configuration
rev-luna-low: repair.context = packet,diff,check_results,review_findings (extension)
rev-luna-low: repair.roles = builder (extension)
rev-luna-low: shape.critique_prompt = lab:critique (extension)
rev-luna-low: shape.critique_rounds = 1 (extension)
rev-luna-high: repair.context = packet,diff,check_results,review_findings (extension)
rev-luna-high: repair.roles = builder (extension)
rev-luna-high: shape.critique_prompt = lab:critique (extension)
rev-luna-high: shape.critique_rounds = 1 (extension)
rev-sol-low: repair.context = packet,diff,check_results,review_findings (extension)
rev-sol-low: repair.roles = builder (extension)
rev-sol-low: shape.critique_prompt = lab:critique (extension)
rev-sol-low: shape.critique_rounds = 1 (extension)
rev-sol-high: repair.context = packet,diff,check_results,review_findings (extension)
rev-sol-high: repair.roles = builder (extension)
rev-sol-high: shape.critique_prompt = lab:critique (extension)
rev-sol-high: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
