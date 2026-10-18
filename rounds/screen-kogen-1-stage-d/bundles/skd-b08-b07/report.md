incomplete: 4 of 8 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (4 of 8 cells scored)
## CMP-1 Correctness
| variant                       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-------------------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| b08-builder-testing-rules-off | 2       | 0         | 0                | 0              | 1          | 100%         | 0 of 2        | 0           |
| b07-output-full               | 2       | 0         | 0                | 0              | 0          | 100%         | 0 of 2        | 0           |
false success: 0 of 2 claims (b08-builder-testing-rules-off)
false success: 0 of 2 claims (b07-output-full)
shaping outcomes:
b08-builder-testing-rules-off: shaping ready 3, shaping failed 0; correct 2 of 2
b07-output-full: shaping ready 2, shaping failed 0; correct 2 of 2
## Per-task outcomes
| task      | variant                       | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|-------------------------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
| ledger-ex | b07-output-full               | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 1          |
| r70-5-go  | b07-output-full               | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | b08-builder-testing-rules-off | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | b07-output-full               | 0       | 0         | 0                | 0              | 0          |
| rate-go   | b08-builder-testing-rules-off | 1       | 0         | 0                | 0              | 0          |
| rate-go   | b07-output-full               | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant                       | stage      | wall   | model  | tools/checks | requests |
|-------------------------------|------------|--------|--------|--------------|----------|
| b08-builder-testing-rules-off | shape      | 0ms    | 0ms    | 0ms          | 0        |
| b08-builder-testing-rules-off | plan       | 23.3s  | 23.3s  | 0ms          | 3        |
| b08-builder-testing-rules-off | build      | 267s   | 242s   | 25s          | 25       |
| b08-builder-testing-rules-off | verify     | 3s     | 0ms    | 3s           | 0        |
| b08-builder-testing-rules-off | review     | 47.5s  | 47.5s  | 0ms          | 8        |
| b08-builder-testing-rules-off | commit     | 0ms    | 0ms    | 0ms          | 0        |
| b08-builder-testing-rules-off | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| b08-builder-testing-rules-off | assessment | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full               | shape      | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full               | plan       | 11.8s  | 11.8s  | 0ms          | 2        |
| b07-output-full               | build      | 233.1s | 206.3s | 26.8s        | 28       |
| b07-output-full               | verify     | 3.1s   | 0ms    | 3.1s         | 0        |
| b07-output-full               | review     | 68.9s  | 68.9s  | 0ms          | 10       |
| b07-output-full               | commit     | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full               | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full               | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                                   | outcome    | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------------------------------|------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skd-b08-b07-ledger-ex-r0-b07-output-full-a1               | correct    | 138.3s | 112.4s | 25.9s        | 17       | 1       | 2       | 0         | 0                    |
| skd-b08-b07-ledger-ex-r0-b08-builder-testing-rules-off-a1 | correct    | 133.4s | 107.1s | 26.3s        | 15       | 1       | 2       | 0         | 0                    |
| skd-b08-b07-r70-5-go-r0-b08-builder-testing-rules-off-a1  | incomplete | 108.3s | 100.3s | 8s           | 7        | 0       | 0       | 0         | 0                    |
| skd-b08-b07-rate-go-r0-b07-output-full-a1                 | correct    | 184s   | 174.6s | 9.4s         | 23       | 2       | 3       | 0         | 0                    |
| skd-b08-b07-rate-go-r0-b08-builder-testing-rules-off-a1   | correct    | 112.1s | 105.4s | 6.8s         | 14       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
b07-output-full openai: input 0.26M, cached 36.6k, output 7.8k, reasoning 261, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
b08-builder-testing-rules-off openai: input 0.18M, cached 4.7k, output 10.8k, reasoning 495, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
native usage by stage and provider:
stage build b07-output-full openai (responses): input 0.19M, cached 36.6k, output 6.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
stage build b08-builder-testing-rules-off openai (responses): input 0.12M, cached 4.7k, output 9.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
stage plan b07-output-full openai (responses): input 5.2k, cached 0, output 355, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 5.5k
stage plan b08-builder-testing-rules-off openai (responses): input 9.4k, cached 0, output 799, reasoning 259, input_tokens_details.cache_write_tokens 0, total_tokens 10.2k
stage review b07-output-full openai (responses): input 65.3k, cached 0, output 1.0k, reasoning 261, input_tokens_details.cache_write_tokens 0, total_tokens 66.3k
stage review b08-builder-testing-rules-off openai (responses): input 52.0k, cached 0, output 700, reasoning 236, input_tokens_details.cache_write_tokens 0, total_tokens 52.7k
native usage by attempt and provider:
attempt usage skd-b08-b07-ledger-ex-r0-b07-output-full-a1 openai (responses): input 99.2k, cached 8.7k, output 3.0k, reasoning 98, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage skd-b08-b07-ledger-ex-r0-b08-builder-testing-rules-off-a1 openai (responses): input 74.9k, cached 4.7k, output 3.1k, reasoning 166, input_tokens_details.cache_write_tokens 0, total_tokens 78.0k
attempt usage skd-b08-b07-r70-5-go-r0-b08-builder-testing-rules-off-a1 openai (responses): input 40.0k, cached 0, output 4.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 44.4k
attempt usage skd-b08-b07-rate-go-r0-b07-output-full-a1 openai (responses): input 0.16M, cached 27.9k, output 4.8k, reasoning 163, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage skd-b08-b07-rate-go-r0-b08-builder-testing-rules-off-a1 openai (responses): input 67.1k, cached 0, output 3.3k, reasoning 329, input_tokens_details.cache_write_tokens 0, total_tokens 70.4k
attempt outcomes included: b08-builder-testing-rules-off: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; b07-output-full: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 676.2s, model 599.8s, tools/checks 76.5s, requests 76
builder settings: b08-builder-testing-rules-off openai gpt-6-luna reasoning.effort=low
builder settings: b07-output-full openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 5, scored 4, incorrect 0, infrastructure 0, incomplete 1
variant b07-output-full differs from b08-builder-testing-rules-off in:
  build.output: kogen_16k -> full
  testing_rules.roles: shaper,planner,reviewer -> shaper,planner,builder,reviewer
B07: exercised in 2 of 2 b07-output-full attempts
B08: exercised in 2 of 2 b07-output-full attempts
first position per task: ledger-ex b08-builder-testing-rules-off 1, b07-output-full 0 (1 repetitions, 2 variants)
first position per task: r70-5-go b08-builder-testing-rules-off 1, b07-output-full 0 (1 repetitions, 2 variants)
first position per task: r70-7-go b08-builder-testing-rules-off 0, b07-output-full 1 (1 repetitions, 2 variants)
first position per task: rate-go b08-builder-testing-rules-off 0, b07-output-full 1 (1 repetitions, 2 variants)
b08-builder-testing-rules-off: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, testing_rules.roles)
b07-output-full: not the Kogen profile (differs in build.output, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
b08-builder-testing-rules-off: repair.context = packet,diff,check_results,review_findings (extension)
b08-builder-testing-rules-off: repair.roles = builder (extension)
b08-builder-testing-rules-off: shape.critique_prompt = lab:critique (extension)
b08-builder-testing-rules-off: shape.critique_rounds = 1 (extension)
b07-output-full: build.output = full (extension)
b07-output-full: repair.context = packet,diff,check_results,review_findings (extension)
b07-output-full: repair.roles = builder (extension)
b07-output-full: shape.critique_prompt = lab:critique (extension)
b07-output-full: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
