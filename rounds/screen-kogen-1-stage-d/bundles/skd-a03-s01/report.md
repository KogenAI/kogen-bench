incomplete: 5 of 8 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (5 of 8 cells scored)
## CMP-1 Correctness
| variant               | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| a03-gherkin-off       | 0       | 0         | 3                | 0              | 0          | 0%           | 0 of 0        | 0           |
| s01-shaping-generated | 2       | 0         | 0                | 0              | 1          | 100%         | 0 of 2        | 0           |
false success: 0 of 0 claims (a03-gherkin-off)
false success: 0 of 2 claims (s01-shaping-generated)
shaping outcomes:
a03-gherkin-off: shaping ready 0, shaping failed 3 (shaping_failed); correct 0 of 3
s01-shaping-generated: shaping ready 3, shaping failed 0; correct 2 of 2
## Per-task outcomes
| task      | variant               | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|-----------------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | a03-gherkin-off       | 0       | 0         | 1                | 0              | 0          |
| ledger-ex | s01-shaping-generated | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | a03-gherkin-off       | 0       | 0         | 1                | 0              | 0          |
| r70-5-go  | s01-shaping-generated | 0       | 0         | 0                | 0              | 1          |
| r70-7-go  | a03-gherkin-off       | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | s01-shaping-generated | 0       | 0         | 0                | 0              | 0          |
| rate-go   | a03-gherkin-off       | 0       | 0         | 1                | 0              | 0          |
| rate-go   | s01-shaping-generated | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant               | stage      | wall   | model  | tools/checks | requests |
|-----------------------|------------|--------|--------|--------------|----------|
| a03-gherkin-off       | shape      | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | plan       | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | build      | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | verify     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | review     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | commit     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off       | assessment | 0ms    | 0ms    | 0ms          | 0        |
| s01-shaping-generated | shape      | 223.6s | 223.6s | 0ms          | 13       |
| s01-shaping-generated | plan       | 19.4s  | 19.4s  | 0ms          | 3        |
| s01-shaping-generated | build      | 260.1s | 249.8s | 10.3s        | 28       |
| s01-shaping-generated | verify     | 4.9s   | 0ms    | 4.9s         | 0        |
| s01-shaping-generated | review     | 77.4s  | 77.4s  | 0ms          | 13       |
| s01-shaping-generated | commit     | 0ms    | 0ms    | 0ms          | 0        |
| s01-shaping-generated | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| s01-shaping-generated | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                           | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skd-a03-s01-ledger-ex-r0-a03-gherkin-off-a1       | workflow failure | 2.1s   | 0ms    | 2.1s         | 0        | 0       | 0       | 0         | 0                    |
| skd-a03-s01-ledger-ex-r0-s01-shaping-generated-a1 | correct          | 327.5s | 311s   | 16.5s        | 31       | 3       | 4       | 0         | 0                    |
| skd-a03-s01-r70-5-go-r0-a03-gherkin-off-a1        | workflow failure | 5.7s   | 0ms    | 5.7s         | 0        | 0       | 0       | 0         | 0                    |
| skd-a03-s01-r70-5-go-r0-s01-shaping-generated-a1  | incomplete       | 102.8s | 97.1s  | 5.7s         | 5        | 0       | 0       | 0         | 0                    |
| skd-a03-s01-rate-go-r0-a03-gherkin-off-a1         | workflow failure | 1.5s   | 0ms    | 1.5s         | 0        | 0       | 0       | 0         | 0                    |
| skd-a03-s01-rate-go-r0-s01-shaping-generated-a1   | correct          | 166.1s | 162.1s | 4.1s         | 21       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
s01-shaping-generated openai: input 0.42M, cached 57.6k, output 20.9k, reasoning 345, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
native usage by stage and provider:
stage build s01-shaping-generated openai (responses): input 0.21M, cached 43.5k, output 8.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
stage plan s01-shaping-generated openai (responses): input 8.1k, cached 0, output 513, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 8.6k
stage review s01-shaping-generated openai (responses): input 95.9k, cached 0, output 1.3k, reasoning 345, input_tokens_details.cache_write_tokens 0, total_tokens 97.1k
stage shape s01-shaping-generated openai (responses): input 0.11M, cached 14.1k, output 10.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
native usage by attempt and provider:
attempt usage skd-a03-s01-ledger-ex-r0-s01-shaping-generated-a1 openai (responses): input 0.24M, cached 25.1k, output 11.0k, reasoning 300, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage skd-a03-s01-r70-5-go-r0-s01-shaping-generated-a1 openai (responses): input 34.3k, cached 0, output 4.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 38.7k
attempt usage skd-a03-s01-rate-go-r0-s01-shaping-generated-a1 openai (responses): input 0.14M, cached 32.5k, output 5.3k, reasoning 45, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt outcomes included: a03-gherkin-off: correct 0, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0; s01-shaping-generated: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 605.8s, model 570.2s, tools/checks 35.5s, requests 57
builder settings: a03-gherkin-off openai gpt-6-luna reasoning.effort=low
builder settings: s01-shaping-generated openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 6, scored 5, incorrect 0, infrastructure 0, incomplete 1
variant s01-shaping-generated differs from a03-gherkin-off in:
  artifacts.gherkin: off -> executed
  shape.source: supplied -> generate
  shape.supplied: prose -> gherkin
acceptance ran in 3 of 3 s01-shaping-generated attempts
MODE: exercised in 3 of 3 s01-shaping-generated attempts
first position per task: ledger-ex a03-gherkin-off 1, s01-shaping-generated 0 (1 repetitions, 2 variants)
first position per task: r70-5-go a03-gherkin-off 1, s01-shaping-generated 0 (1 repetitions, 2 variants)
first position per task: r70-7-go a03-gherkin-off 0, s01-shaping-generated 1 (1 repetitions, 2 variants)
first position per task: rate-go a03-gherkin-off 0, s01-shaping-generated 1 (1 repetitions, 2 variants)
a03-gherkin-off: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
s01-shaping-generated: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
a03-gherkin-off: repair.context = packet,diff,check_results,review_findings (extension)
a03-gherkin-off: repair.roles = builder (extension)
a03-gherkin-off: shape.critique_prompt = lab:critique (extension)
a03-gherkin-off: shape.critique_rounds = 1 (extension)
s01-shaping-generated: repair.context = packet,diff,check_results,review_findings (extension)
s01-shaping-generated: repair.roles = builder (extension)
s01-shaping-generated: shape.critique_prompt = lab:critique (extension)
s01-shaping-generated: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
