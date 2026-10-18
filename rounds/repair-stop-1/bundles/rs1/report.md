complete: 6/6 cells scored
Question: repair-stop-1: on env-ex, does allowing 12 repairs instead of 6 turn stopped attempts into correct submissions?
Hypothesis: exploratory: the review keeps rejecting green code, so more repairs do not help
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| stop6   | 0       | 0         | 3                | 0              | 0          | 0%           | 0 of 0        | 0           |
| stop12  | 3       | 0         | 0                | 0              | 0          | 100%         | 0 of 3        | 0           |
false success: 0 of 0 claims (stop6)
false success: 0 of 3 claims (stop12)
shaping outcomes:
stop6: shaping ready 3, shaping failed 0; correct 0 of 3
stop12: shaping ready 3, shaping failed 0; correct 3 of 3
## Per-task outcomes
| task   | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------|---------|---------|-----------|------------------|----------------|------------|
| env-ex | stop6   | 0       | 0         | 3                | 0              | 0          |
| env-ex | stop12  | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| stop6   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| stop6   | plan       | 42.8s   | 42.8s   | 0ms          | 3        |
| stop6   | build      | 1972.5s | 1914.8s | 57.6s        | 96       |
| stop6   | verify     | 50.4s   | 0ms     | 50.4s        | 0        |
| stop6   | review     | 265.6s  | 265.6s  | 0ms          | 16       |
| stop6   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| stop6   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| stop6   | assessment | 0ms     | 0ms     | 0ms          | 0        |
| stop12  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| stop12  | plan       | 45.3s   | 45.3s   | 0ms          | 3        |
| stop12  | build      | 2856.2s | 2772.8s | 83.4s        | 135      |
| stop12  | verify     | 43.4s   | 0ms     | 43.4s        | 0        |
| stop12  | review     | 531.5s  | 531.5s  | 0ms          | 25       |
| stop12  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| stop12  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| stop12  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                 | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rs1-env-ex-r0-stop12-a1 | correct          | 1263.7s | 1207.6s | 56.1s        | 57       | 5       | 4       | 0         | 0                    |
| rs1-env-ex-r0-stop6-a1  | workflow failure | 679.7s  | 639.2s  | 40.6s        | 39       | 6       | 3       | 0         | 0                    |
| rs1-env-ex-r1-stop12-a1 | correct          | 1100.7s | 1058.6s | 42s          | 55       | 6       | 5       | 0         | 0                    |
| rs1-env-ex-r1-stop6-a1  | workflow failure | 757.2s  | 720.4s  | 36.8s        | 30       | 6       | 1       | 0         | 0                    |
| rs1-env-ex-r2-stop12-a1 | correct          | 1132.2s | 1083.3s | 48.9s        | 51       | 5       | 3       | 0         | 0                    |
| rs1-env-ex-r2-stop6-a1  | workflow failure | 915.6s  | 863.7s  | 51.9s        | 46       | 6       | 5       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
stop12 openai: input 3.39M, cached 1.38M, output 45.0k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 3.43M
stop6 openai: input 1.76M, cached 0.61M, output 30.8k, reasoning 891, input_tokens_details.cache_write_tokens 0, total_tokens 1.79M
native usage by stage and provider:
stage build stop12 openai (responses): input 2.94M, cached 1.38M, output 39.2k, reasoning 411, input_tokens_details.cache_write_tokens 0, total_tokens 2.98M
stage build stop6 openai (responses): input 1.50M, cached 0.61M, output 24.7k, reasoning 421, input_tokens_details.cache_write_tokens 0, total_tokens 1.52M
stage plan stop12 openai (responses): input 13.3k, cached 0, output 813, reasoning 209, input_tokens_details.cache_write_tokens 0, total_tokens 14.1k
stage plan stop6 openai (responses): input 13.3k, cached 0, output 1.0k, reasoning 367, input_tokens_details.cache_write_tokens 0, total_tokens 14.3k
stage review stop12 openai (responses): input 0.43M, cached 0, output 5.0k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
stage review stop6 openai (responses): input 0.25M, cached 0, output 5.0k, reasoning 103, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
native usage by attempt and provider:
attempt usage rs1-env-ex-r0-stop12-a1 openai (responses): input 1.17M, cached 0.46M, output 18.0k, reasoning 750, input_tokens_details.cache_write_tokens 0, total_tokens 1.18M
attempt usage rs1-env-ex-r0-stop6-a1 openai (responses): input 0.68M, cached 0.26M, output 11.7k, reasoning 119, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
attempt usage rs1-env-ex-r1-stop12-a1 openai (responses): input 1.20M, cached 0.51M, output 15.1k, reasoning 607, input_tokens_details.cache_write_tokens 0, total_tokens 1.22M
attempt usage rs1-env-ex-r1-stop6-a1 openai (responses): input 0.44M, cached 0.14M, output 8.8k, reasoning 96, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage rs1-env-ex-r2-stop12-a1 openai (responses): input 1.02M, cached 0.40M, output 11.9k, reasoning 272, input_tokens_details.cache_write_tokens 0, total_tokens 1.03M
attempt usage rs1-env-ex-r2-stop6-a1 openai (responses): input 0.65M, cached 0.21M, output 10.4k, reasoning 676, input_tokens_details.cache_write_tokens 0, total_tokens 0.66M
attempt outcomes included: stop6: correct 0, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0; stop12: correct 3, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5849s, model 5572.8s, tools/checks 276.3s, requests 278
builder settings: stop6 openai gpt-6-luna reasoning.effort=medium
builder settings: stop12 openai gpt-6-luna reasoning.effort=medium
## CMP-3 Counts and exposure
planned 6, started 6, scored 6, incorrect 0, infrastructure 0, incomplete 0
variant stop12 differs from stop6 in:
  stop.max_repairs: 6 -> 12
stop.max_repairs: not exercised
first position per task: env-ex stop6 1, stop12 2 (3 repetitions, 2 variants)
stop6: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
stop12: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000, stop.max_repairs = 12; no variant matches the Kogen profile configuration
stop6: repair.context = packet,diff,check_results,review_findings (extension)
stop6: repair.roles = builder (extension)
stop6: shape.critique_prompt = lab:critique (extension)
stop6: shape.critique_rounds = 1 (extension)
stop12: repair.context = packet,diff,check_results,review_findings (extension)
stop12: repair.roles = builder (extension)
stop12: shape.critique_prompt = lab:critique (extension)
stop12: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
