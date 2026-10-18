incomplete: 1 of 8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (1 of 8 cells scored)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| c01-review-off   | 0       | 1         | 0                | 0              | 0          | 0%           | 1 of 1        | 0           |
| r02-repair-fresh | 0       | 0         | 0                | 0              | 1          | unavailable  | 0 of 0        | 0           |
false success: 1 of 1 claims (c01-review-off)
false success: 0 of 0 claims (r02-repair-fresh)
shaping outcomes:
c01-review-off: shaping ready 1, shaping failed 0; correct 0 of 1
r02-repair-fresh: shaping ready 1, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | c01-review-off   | 0       | 1         | 0                | 0              | 0          |
| r70-5-elixir | r02-repair-fresh | 0       | 0         | 0                | 0              | 1          |
| r70-5-go     | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall   | model | tools/checks | requests |
|------------------|------------|--------|-------|--------------|----------|
| c01-review-off   | shape      | 0ms    | 0ms   | 0ms          | 0        |
| c01-review-off   | plan       | 8.7s   | 8.7s  | 0ms          | 1        |
| c01-review-off   | build      | 124.3s | 116s  | 8.3s         | 10       |
| c01-review-off   | verify     | 2.4s   | 0ms   | 2.4s         | 0        |
| c01-review-off   | review     | 0ms    | 0ms   | 0ms          | 0        |
| c01-review-off   | commit     | 0ms    | 0ms   | 0ms          | 0        |
| c01-review-off   | evaluate   | 0ms    | 0ms   | 0ms          | 0        |
| c01-review-off   | assessment | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | shape      | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | plan       | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | build      | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | verify     | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | review     | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | commit     | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | evaluate   | 0ms    | 0ms   | 0ms          | 0        |
| r02-repair-fresh | assessment | 0ms    | 0ms   | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                         | outcome    | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------------------|------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ske-c01-r02-r70-5-elixir-r0-c01-review-off-a1   | incorrect  | 139.1s | 124.6s | 14.5s        | 11       | 0       | 0       | 0         | 0                    |
| ske-c01-r02-r70-5-elixir-r0-r02-repair-fresh-a1 | incomplete | 0ms    | 0ms    | 0ms          | 0        | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
c01-review-off openai: input 0.42M, cached 73.2k, output 5.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
native usage by stage and provider:
stage build c01-review-off openai (responses): input 0.39M, cached 73.2k, output 4.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
stage plan c01-review-off openai (responses): input 34.3k, cached 0, output 289, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.6k
native usage by attempt and provider:
attempt usage ske-c01-r02-r70-5-elixir-r0-c01-review-off-a1 openai (responses): input 0.42M, cached 73.2k, output 5.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt outcomes included: c01-review-off: correct 0, incorrect 1, workflow failure 0, infrastructure 0, incomplete 0; r02-repair-fresh: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 139.1s, model 124.6s, tools/checks 14.5s, requests 11
builder settings: c01-review-off openai gpt-6-luna reasoning.effort=low
builder settings: r02-repair-fresh openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 2, scored 1, incorrect 1, infrastructure 0, incomplete 1
variant r02-repair-fresh differs from c01-review-off in:
  repair.conversation: continue -> fresh
  review.enabled: false -> true
review.enabled: not exercised
repair.conversation: not exercised
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
