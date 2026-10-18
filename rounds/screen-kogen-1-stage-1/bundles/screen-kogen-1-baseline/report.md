incomplete: 3 of 4 cells scored
Question: Does the Kogen-equivalent profile on gpt-6-luna low land between floor and ceiling on these four development tasks?
Hypothesis: at least one task is neither all correct nor all failed across the baseline cells
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (3 of 4 cells scored)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen   | 2       | 0         | 1                | 0              | 1          | 66.7%        | 0 of 2        | 0           |
false success: 0 of 2 claims (kogen)
shaping outcomes:
kogen: shaping ready 4, shaping failed 0; correct 2 of 3
## Per-task outcomes
| task      | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|---------|---------|-----------|------------------|----------------|------------|
| ledger-ex | kogen   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | kogen   | 0       | 0         | 1                | 0              | 0          |
| r70-7-go  | kogen   | 0       | 0         | 0                | 0              | 1          |
| rate-go   | kogen   | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| kogen   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| kogen   | plan       | 65.3s   | 65.3s   | 0ms          | 4        |
| kogen   | build      | 3979.7s | 3895.2s | 84.5s        | 221      |
| kogen   | verify     | 43.3s   | 0ms     | 43.3s        | 0        |
| kogen   | review     | 1249.6s | 1249.6s | 0ms          | 89       |
| kogen   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| kogen   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| kogen   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                       | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| screen-kogen-1-baseline-ledger-ex-r0-kogen-a1 | correct          | 1258.9s | 1217.3s | 41.6s        | 61       | 11      | 13      | 0         | 0                    |
| screen-kogen-1-baseline-r70-5-go-r0-kogen-a1  | workflow failure | 2090.6s | 2038.2s | 52.4s        | 127      | 28      | 30      | 0         | 0                    |
| screen-kogen-1-baseline-r70-7-go-r0-kogen-a1  | incomplete       | 1835.1s | 1781.4s | 53.7s        | 118      | 32      | 32      | 0         | 0                    |
| screen-kogen-1-baseline-rate-go-r0-kogen-a1   | correct          | 175.9s  | 173.1s  | 2.8s         | 8        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen openai: input 6.51M, cached 3.50M, output 70.1k, reasoning 993, input_tokens_details.cache_write_tokens 0, total_tokens 6.58M
native usage by stage and provider:
stage build kogen openai (responses): input 5.32M, cached 3.37M, output 51.8k, reasoning 573, input_tokens_details.cache_write_tokens 0, total_tokens 5.37M
stage plan kogen openai (responses): input 13.7k, cached 0, output 1.0k, reasoning 171, input_tokens_details.cache_write_tokens 0, total_tokens 14.8k
stage review kogen openai (responses): input 1.18M, cached 0.13M, output 17.2k, reasoning 249, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
native usage by attempt and provider:
attempt usage screen-kogen-1-baseline-ledger-ex-r0-kogen-a1 openai (responses): input 0.57M, cached 0.13M, output 12.1k, reasoning 249, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage screen-kogen-1-baseline-r70-5-go-r0-kogen-a1 openai (responses): input 3.22M, cached 1.92M, output 26.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.24M
attempt usage screen-kogen-1-baseline-r70-7-go-r0-kogen-a1 openai (responses): input 2.68M, cached 1.44M, output 29.4k, reasoning 573, input_tokens_details.cache_write_tokens 0, total_tokens 2.71M
attempt usage screen-kogen-1-baseline-rate-go-r0-kogen-a1 openai (responses): input 42.2k, cached 8.6k, output 1.8k, reasoning 171, input_tokens_details.cache_write_tokens 0, total_tokens 44.0k
attempt outcomes included: kogen: correct 2, incorrect 0, workflow failure 1, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5360.6s, model 5210s, tools/checks 150.5s, requests 314
builder settings: kogen openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 4, scored 3, incorrect 0, infrastructure 0, incomplete 1
first position per task: ledger-ex kogen 1 (1 repetitions, 1 variants)
first position per task: r70-5-go kogen 1 (1 repetitions, 1 variants)
first position per task: r70-7-go kogen 1 (1 repetitions, 1 variants)
first position per task: rate-go kogen 1 (1 repetitions, 1 variants)
kogen: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.reviewer.model, roles.shaper.effort, roles.shaper.model)
kogen: repair.context = packet,diff,check_results,review_findings (extension)
kogen: repair.roles = builder (extension)
kogen: shape.critique_prompt = lab:critique (extension)
kogen: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
