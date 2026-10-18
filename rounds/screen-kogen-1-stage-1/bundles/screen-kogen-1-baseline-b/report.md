incomplete: 0 of 4 cells scored
Question: Does the Kogen-equivalent profile on gpt-6-luna low land between floor and ceiling on these four development tasks?
Hypothesis: at least one task is neither all correct nor all failed across the baseline cells
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 4 cells scored)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen   | 0       | 0         | 0                | 0              | 2          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (kogen)
shaping outcomes:
kogen: shaping ready 2, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task      | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|---------|---------|-----------|------------------|----------------|------------|
| ledger-ex | kogen   | 0       | 0         | 0                | 0              | 1          |
| r70-5-go  | kogen   | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | kogen   | 0       | 0         | 0                | 0              | 0          |
| rate-go   | kogen   | 0       | 0         | 0                | 0              | 1          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall  | model | tools/checks | requests |
|---------|------------|-------|-------|--------------|----------|
| kogen   | shape      | 0ms   | 0ms   | 0ms          | 0        |
| kogen   | plan       | 18.4s | 18.4s | 0ms          | 2        |
| kogen   | build      | 5.4s  | 5.3s  | 35ms         | 1        |
| kogen   | verify     | 0ms   | 0ms   | 0ms          | 0        |
| kogen   | review     | 0ms   | 0ms   | 0ms          | 0        |
| kogen   | commit     | 0ms   | 0ms   | 0ms          | 0        |
| kogen   | evaluate   | 0ms   | 0ms   | 0ms          | 0        |
| kogen   | assessment | 0ms   | 0ms   | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome    | wall  | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|------------|-------|-------|--------------|----------|---------|---------|-----------|----------------------|
| screen-kogen-1-baseline-b-ledger-ex-r0-kogen-a1 | incomplete | 14.2s | 12.4s | 1.8s         | 2        | 0       | 0       | 0         | 0                    |
| screen-kogen-1-baseline-b-rate-go-r0-kogen-a1   | incomplete | 12.8s | 11.3s | 1.5s         | 1        | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen openai: input 8.3k, cached 2.4k, output 448, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 8.8k
native usage by stage and provider:
stage build kogen openai (responses): input 3.2k, cached 0, output 77, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.3k
stage plan kogen openai (responses): input 5.2k, cached 2.4k, output 371, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 5.5k
native usage by attempt and provider:
attempt usage screen-kogen-1-baseline-b-ledger-ex-r0-kogen-a1 openai (responses): input 5.7k, cached 2.4k, output 230, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 6.0k
attempt usage screen-kogen-1-baseline-b-rate-go-r0-kogen-a1 openai (responses): input 2.6k, cached 0, output 218, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.8k
attempt outcomes included: kogen: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 2
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 27s, model 23.7s, tools/checks 3.3s, requests 3
builder settings: kogen openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 2, scored 0, incorrect 0, infrastructure 0, incomplete 2
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
