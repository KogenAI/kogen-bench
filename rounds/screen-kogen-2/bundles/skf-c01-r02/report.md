complete: 8/8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| c01-review-off   | 1       | 3         | 0                | 0              | 0          | 25%          | 3 of 4        | 0           |
| r02-repair-fresh | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 3 of 4 claims (c01-review-off)
false success: 0 of 4 claims (r02-repair-fresh)
shaping outcomes:
c01-review-off: shaping ready 4, shaping failed 0; correct 1 of 4
r02-repair-fresh: shaping ready 4, shaping failed 0; correct 4 of 4
## Per-task outcomes
| task         | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | c01-review-off   | 0       | 1         | 0                | 0              | 0          |
| r70-5-elixir | r02-repair-fresh | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | c01-review-off   | 0       | 1         | 0                | 0              | 0          |
| r70-5-go     | r02-repair-fresh | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | c01-review-off   | 0       | 1         | 0                | 0              | 0          |
| r70-7-elixir | r02-repair-fresh | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | c01-review-off   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | r02-repair-fresh | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall   | model  | tools/checks | requests |
|------------------|------------|--------|--------|--------------|----------|
| c01-review-off   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| c01-review-off   | plan       | 35s    | 35s    | 0ms          | 4        |
| c01-review-off   | build      | 422.6s | 370.4s | 52.2s        | 40       |
| c01-review-off   | verify     | 10.4s  | 0ms    | 10.4s        | 0        |
| c01-review-off   | review     | 0ms    | 0ms    | 0ms          | 0        |
| c01-review-off   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| c01-review-off   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| c01-review-off   | assessment | 0ms    | 0ms    | 0ms          | 0        |
| r02-repair-fresh | shape      | 0ms    | 0ms    | 0ms          | 0        |
| r02-repair-fresh | plan       | 30.5s  | 30.5s  | 0ms          | 4        |
| r02-repair-fresh | build      | 391.5s | 307.6s | 83.9s        | 32       |
| r02-repair-fresh | verify     | 25.6s  | 0ms    | 25.6s        | 0        |
| r02-repair-fresh | review     | 241.3s | 241.3s | 0ms          | 39       |
| r02-repair-fresh | commit     | 0ms    | 0ms    | 0ms          | 0        |
| r02-repair-fresh | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| r02-repair-fresh | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome   | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|-----------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skf-c01-r02-r70-5-elixir-r0-c01-review-off-a1   | incorrect | 151s   | 133.1s | 17.9s        | 13       | 1       | 0       | 0         | 0                    |
| skf-c01-r02-r70-5-elixir-r0-r02-repair-fresh-a1 | correct   | 475.4s | 421.1s | 54.3s        | 54       | 4       | 3       | 0         | 0                    |
| skf-c01-r02-r70-5-go-r0-c01-review-off-a1       | incorrect | 82.1s  | 66.4s  | 15.7s        | 6        | 0       | 0       | 0         | 0                    |
| skf-c01-r02-r70-5-go-r0-r02-repair-fresh-a1     | correct   | 176.4s | 158s   | 18.4s        | 20       | 1       | 2       | 0         | 0                    |
| skf-c01-r02-r70-7-elixir-r0-c01-review-off-a1   | incorrect | 183.2s | 142s   | 41.2s        | 19       | 1       | 0       | 0         | 0                    |
| skf-c01-r02-r70-7-elixir-r0-r02-repair-fresh-a1 | correct   | 409s   | 369.1s | 39.9s        | 47       | 3       | 4       | 0         | 0                    |
| skf-c01-r02-r70-7-go-r0-c01-review-off-a1       | correct   | 71.8s  | 63.8s  | 7.9s         | 6        | 0       | 0       | 0         | 0                    |
| skf-c01-r02-r70-7-go-r0-r02-repair-fresh-a1     | correct   | 275.5s | 255.6s | 19.9s        | 35       | 3       | 4       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
c01-review-off openai: input 0.39M, cached 86.3k, output 14.6k, reasoning 295, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
r02-repair-fresh openai: input 1.79M, cached 0.21M, output 36.6k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.83M
native usage by stage and provider:
stage build c01-review-off openai (responses): input 0.37M, cached 82.2k, output 13.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
stage build r02-repair-fresh openai (responses): input 0.24M, cached 42.0k, output 11.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
stage plan c01-review-off openai (responses): input 17.2k, cached 4.1k, output 1.1k, reasoning 295, input_tokens_details.cache_write_tokens 0, total_tokens 18.3k
stage plan r02-repair-fresh openai (responses): input 17.2k, cached 8.2k, output 941, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.1k
stage repair r02-repair-fresh openai (responses): input 0.95M, cached 0.14M, output 20.4k, reasoning 86, input_tokens_details.cache_write_tokens 0, total_tokens 0.97M
stage review r02-repair-fresh openai (responses): input 0.59M, cached 14.8k, output 3.9k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
native usage by attempt and provider:
attempt usage skf-c01-r02-r70-5-elixir-r0-c01-review-off-a1 openai (responses): input 0.11M, cached 4.1k, output 5.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage skf-c01-r02-r70-5-elixir-r0-r02-repair-fresh-a1 openai (responses): input 0.60M, cached 74.9k, output 13.5k, reasoning 244, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
attempt usage skf-c01-r02-r70-5-go-r0-c01-review-off-a1 openai (responses): input 37.6k, cached 7.0k, output 2.6k, reasoning 124, input_tokens_details.cache_write_tokens 0, total_tokens 40.2k
attempt usage skf-c01-r02-r70-5-go-r0-r02-repair-fresh-a1 openai (responses): input 0.21M, cached 19.8k, output 5.0k, reasoning 60, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage skf-c01-r02-r70-7-elixir-r0-c01-review-off-a1 openai (responses): input 0.21M, cached 70.5k, output 4.5k, reasoning 171, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage skf-c01-r02-r70-7-elixir-r0-r02-repair-fresh-a1 openai (responses): input 0.59M, cached 93.6k, output 11.1k, reasoning 407, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
attempt usage skf-c01-r02-r70-7-go-r0-c01-review-off-a1 openai (responses): input 39.4k, cached 4.6k, output 2.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 41.7k
attempt usage skf-c01-r02-r70-7-go-r0-r02-repair-fresh-a1 openai (responses): input 0.40M, cached 19.5k, output 7.1k, reasoning 376, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt outcomes included: c01-review-off: correct 1, incorrect 3, workflow failure 0, infrastructure 0, incomplete 0; r02-repair-fresh: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 1824.3s, model 1609.3s, tools/checks 215.1s, requests 200
builder settings: c01-review-off openai gpt-6-luna reasoning.effort=low
builder settings: r02-repair-fresh openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 3, infrastructure 0, incomplete 0
variant r02-repair-fresh differs from c01-review-off in:
  repair.conversation: continue -> fresh
  review.enabled: false -> true
C01: exercised in 4 of 4 r02-repair-fresh attempts
R02: exercised in 4 of 4 r02-repair-fresh attempts
first position per task: r70-5-elixir c01-review-off 1, r02-repair-fresh 0 (1 repetitions, 2 variants)
first position per task: r70-5-go c01-review-off 1, r02-repair-fresh 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir c01-review-off 0, r02-repair-fresh 1 (1 repetitions, 2 variants)
first position per task: r70-7-go c01-review-off 0, r02-repair-fresh 1 (1 repetitions, 2 variants)
c01-review-off: not the Kogen profile (differs in review.enabled, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
r02-repair-fresh: not the Kogen profile (differs in repair.conversation, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
c01-review-off: repair.context = packet,diff,check_results,review_findings (extension)
c01-review-off: repair.roles = builder (extension)
c01-review-off: shape.critique_prompt = lab:critique (extension)
c01-review-off: shape.critique_rounds = 1 (extension)
r02-repair-fresh: repair.context = packet,diff,check_results,review_findings (extension)
r02-repair-fresh: repair.conversation = fresh (extension)
r02-repair-fresh: repair.roles = builder (extension)
r02-repair-fresh: shape.critique_prompt = lab:critique (extension)
r02-repair-fresh: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
