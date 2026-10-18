incomplete: 4 of 8 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (4 of 8 cells scored)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| v05-feedback-raw | 2       | 0         | 0                | 0              | 1          | 100%         | 0 of 2        | 0           |
| p01-plan-off     | 2       | 0         | 0                | 0              | 0          | 100%         | 0 of 2        | 0           |
false success: 0 of 2 claims (v05-feedback-raw)
false success: 0 of 2 claims (p01-plan-off)
shaping outcomes:
v05-feedback-raw: shaping ready 3, shaping failed 0; correct 2 of 2
p01-plan-off: shaping ready 2, shaping failed 0; correct 2 of 2
## Per-task outcomes
| task      | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|------------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | v05-feedback-raw | 1       | 0         | 0                | 0              | 0          |
| ledger-ex | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
| r70-5-go  | v05-feedback-raw | 0       | 0         | 0                | 0              | 1          |
| r70-5-go  | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | v05-feedback-raw | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | p01-plan-off     | 0       | 0         | 0                | 0              | 0          |
| rate-go   | v05-feedback-raw | 1       | 0         | 0                | 0              | 0          |
| rate-go   | p01-plan-off     | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall   | model  | tools/checks | requests |
|------------------|------------|--------|--------|--------------|----------|
| v05-feedback-raw | shape      | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | plan       | 20.9s  | 20.9s  | 0ms          | 3        |
| v05-feedback-raw | build      | 346.4s | 316.4s | 30s          | 43       |
| v05-feedback-raw | verify     | 3.4s   | 0ms    | 3.4s         | 0        |
| v05-feedback-raw | review     | 76.6s  | 76.6s  | 0ms          | 11       |
| v05-feedback-raw | commit     | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| v05-feedback-raw | assessment | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | shape      | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | plan       | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | build      | 185.3s | 165.3s | 20s          | 22       |
| p01-plan-off     | verify     | 2s     | 0ms    | 2s           | 0        |
| p01-plan-off     | review     | 45.9s  | 45.9s  | 0ms          | 9        |
| p01-plan-off     | commit     | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| p01-plan-off     | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                      | outcome    | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------------|------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skd-v05-p01-ledger-ex-r0-p01-plan-off-a1     | correct    | 135s   | 120s   | 15.1s        | 16       | 1       | 2       | 0         | 0                    |
| skd-v05-p01-ledger-ex-r0-v05-feedback-raw-a1 | correct    | 179.3s | 157.7s | 21.5s        | 22       | 2       | 3       | 0         | 0                    |
| skd-v05-p01-r70-5-go-r0-v05-feedback-raw-a1  | incomplete | 101.3s | 90.3s  | 10.9s        | 12       | 1       | 1       | 0         | 0                    |
| skd-v05-p01-rate-go-r0-p01-plan-off-a1       | correct    | 102s   | 91.2s  | 10.8s        | 15       | 1       | 2       | 0         | 0                    |
| skd-v05-p01-rate-go-r0-v05-feedback-raw-a1   | correct    | 174.5s | 165.8s | 8.7s         | 23       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
p01-plan-off openai: input 0.23M, cached 49.8k, output 5.9k, reasoning 108, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
v05-feedback-raw openai: input 0.40M, cached 73.1k, output 11.9k, reasoning 246, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
native usage by stage and provider:
stage build p01-plan-off openai (responses): input 0.17M, cached 49.8k, output 5.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
stage build v05-feedback-raw openai (responses): input 0.31M, cached 70.7k, output 10.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.32M
stage plan v05-feedback-raw openai (responses): input 9.4k, cached 2.4k, output 575, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 10.0k
stage review p01-plan-off openai (responses): input 54.9k, cached 0, output 694, reasoning 108, input_tokens_details.cache_write_tokens 0, total_tokens 55.6k
stage review v05-feedback-raw openai (responses): input 79.1k, cached 0, output 1.3k, reasoning 246, input_tokens_details.cache_write_tokens 0, total_tokens 80.4k
native usage by attempt and provider:
attempt usage skd-v05-p01-ledger-ex-r0-p01-plan-off-a1 openai (responses): input 0.15M, cached 44.5k, output 3.4k, reasoning 63, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage skd-v05-p01-ledger-ex-r0-v05-feedback-raw-a1 openai (responses): input 0.14M, cached 19.5k, output 4.3k, reasoning 163, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage skd-v05-p01-r70-5-go-r0-v05-feedback-raw-a1 openai (responses): input 96.7k, cached 4.9k, output 2.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 99.6k
attempt usage skd-v05-p01-rate-go-r0-p01-plan-off-a1 openai (responses): input 82.7k, cached 5.2k, output 2.5k, reasoning 45, input_tokens_details.cache_write_tokens 0, total_tokens 85.2k
attempt usage skd-v05-p01-rate-go-r0-v05-feedback-raw-a1 openai (responses): input 0.16M, cached 48.8k, output 4.8k, reasoning 83, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt outcomes included: v05-feedback-raw: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; p01-plan-off: correct 2, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 692s, model 625s, tools/checks 67s, requests 88
builder settings: v05-feedback-raw openai gpt-6-luna reasoning.effort=low
builder settings: p01-plan-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 5, scored 4, incorrect 0, infrastructure 0, incomplete 1
variant p01-plan-off differs from v05-feedback-raw in:
  plan.enabled: true -> false
  verify.feedback: raw -> kogen
P01: exercised in 2 of 2 p01-plan-off attempts
V05: exercised in 2 of 2 p01-plan-off attempts
first position per task: ledger-ex v05-feedback-raw 1, p01-plan-off 0 (1 repetitions, 2 variants)
first position per task: r70-5-go v05-feedback-raw 1, p01-plan-off 0 (1 repetitions, 2 variants)
first position per task: r70-7-go v05-feedback-raw 0, p01-plan-off 1 (1 repetitions, 2 variants)
first position per task: rate-go v05-feedback-raw 0, p01-plan-off 1 (1 repetitions, 2 variants)
v05-feedback-raw: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens, verify.feedback)
p01-plan-off: not the Kogen profile (differs in plan.enabled, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
v05-feedback-raw: repair.context = packet,diff,check_results,review_findings (extension)
v05-feedback-raw: repair.roles = builder (extension)
v05-feedback-raw: shape.critique_prompt = lab:critique (extension)
v05-feedback-raw: shape.critique_rounds = 1 (extension)
v05-feedback-raw: verify.feedback = raw (extension)
p01-plan-off: repair.context = packet,diff,check_results,review_findings (extension)
p01-plan-off: repair.roles = builder (extension)
p01-plan-off: shape.critique_prompt = lab:critique (extension)
p01-plan-off: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
