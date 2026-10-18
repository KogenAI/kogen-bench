complete: 4/4 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen   | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (kogen)
shaping outcomes:
kogen: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task      | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|---------|---------|-----------|------------------|----------------|------------|
| ledger-ex | kogen   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | kogen   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go  | kogen   | 1       | 0         | 0                | 0              | 0          |
| rate-go   | kogen   | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall   | model  | tools/checks | requests |
|---------|------------|--------|--------|--------------|----------|
| kogen   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | plan       | 30s    | 30s    | 0ms          | 4        |
| kogen   | build      | 524.8s | 490.4s | 34.5s        | 57       |
| kogen   | verify     | 4.5s   | 0ms    | 4.5s         | 0        |
| kogen   | review     | 102.6s | 102.6s | 0ms          | 18       |
| kogen   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                            | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skd-baseline-ledger-ex-r0-kogen-a1 | correct | 93.8s  | 85.9s  | 8s           | 12       | 0       | 1       | 0         | 0                    |
| skd-baseline-r70-5-go-r0-kogen-a1  | correct | 275.7s | 263.3s | 12.4s        | 30       | 3       | 3       | 0         | 0                    |
| skd-baseline-r70-7-go-r0-kogen-a1  | correct | 179.1s | 163.9s | 15.2s        | 22       | 1       | 2       | 0         | 0                    |
| skd-baseline-rate-go-r0-kogen-a1   | correct | 124.2s | 109.9s | 14.3s        | 15       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen openai: input 0.76M, cached 0.16M, output 19.8k, reasoning 546, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
native usage by stage and provider:
stage build kogen openai (responses): input 0.52M, cached 0.16M, output 17.2k, reasoning 77, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
stage plan kogen openai (responses): input 13.7k, cached 0, output 950, reasoning 145, input_tokens_details.cache_write_tokens 0, total_tokens 14.7k
stage review kogen openai (responses): input 0.22M, cached 0, output 1.7k, reasoning 324, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
native usage by attempt and provider:
attempt usage skd-baseline-ledger-ex-r0-kogen-a1 openai (responses): input 67.6k, cached 7.8k, output 2.6k, reasoning 110, input_tokens_details.cache_write_tokens 0, total_tokens 70.3k
attempt usage skd-baseline-r70-5-go-r0-kogen-a1 openai (responses): input 0.35M, cached 91.8k, output 8.7k, reasoning 33, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage skd-baseline-r70-7-go-r0-kogen-a1 openai (responses): input 0.25M, cached 46.1k, output 5.2k, reasoning 195, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage skd-baseline-rate-go-r0-kogen-a1 openai (responses): input 93.3k, cached 13.7k, output 3.2k, reasoning 208, input_tokens_details.cache_write_tokens 0, total_tokens 96.5k
attempt outcomes included: kogen: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 672.8s, model 622.9s, tools/checks 49.9s, requests 79
builder settings: kogen openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 4, scored 4, incorrect 0, infrastructure 0, incomplete 0
first position per task: ledger-ex kogen 1 (1 repetitions, 1 variants)
first position per task: r70-5-go kogen 1 (1 repetitions, 1 variants)
first position per task: r70-7-go kogen 1 (1 repetitions, 1 variants)
first position per task: rate-go kogen 1 (1 repetitions, 1 variants)
kogen: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
kogen: repair.context = packet,diff,check_results,review_findings (extension)
kogen: repair.roles = builder (extension)
kogen: shape.critique_prompt = lab:critique (extension)
kogen: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
