incomplete: 0 of 8 cells scored
Question: Stage d of screen-kogen-1: how do single Kogen levers change correctness and cost on gpt-6-luna low with a Sol-low reviewer?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 8 cells scored)
## CMP-1 Correctness
| variant          | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| c01-review-off   | 0       | 0         | 0                | 0              | 0          | unavailable  | 0 of 0        | 0           |
| r02-repair-fresh | 0       | 0         | 0                | 0              | 0          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (c01-review-off)
false success: 0 of 0 claims (r02-repair-fresh)
## Per-task outcomes
| task      | variant          | correct | incorrect | workflow failure | infrastructure | incomplete |
|-----------|------------------|---------|-----------|------------------|----------------|------------|
| ledger-ex | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| ledger-ex | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
| r70-5-go  | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| r70-5-go  | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| r70-7-go  | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
| rate-go   | c01-review-off   | 0       | 0         | 0                | 0              | 0          |
| rate-go   | r02-repair-fresh | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant          | stage      | wall | model | tools/checks | requests |
|------------------|------------|------|-------|--------------|----------|
| c01-review-off   | shape      | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | plan       | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | build      | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | verify     | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | review     | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | commit     | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| c01-review-off   | assessment | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | shape      | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | plan       | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | build      | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | verify     | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | review     | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | commit     | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | evaluate   | 0ms  | 0ms   | 0ms          | 0        |
| r02-repair-fresh | assessment | 0ms  | 0ms   | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt | outcome | wall | model | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------|---------|------|-------|--------------|----------|---------|---------|-----------|----------------------|
native usage by variant and provider (wire format kept separate):
native usage by stage and provider:
native usage by attempt and provider:
attempt outcomes included: c01-review-off: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; r02-repair-fresh: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 0ms, model 0ms, tools/checks 0ms, requests 0
builder settings: c01-review-off openai gpt-6-luna reasoning.effort=low
builder settings: r02-repair-fresh openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 0, scored 0, incorrect 0, infrastructure 0, incomplete 0
variant r02-repair-fresh differs from c01-review-off in:
  repair.conversation: continue -> fresh
  review.enabled: false -> true
review.enabled: not exercised
repair.conversation: not exercised
first position per task: ledger-ex c01-review-off 1, r02-repair-fresh 0 (1 repetitions, 2 variants)
first position per task: r70-5-go c01-review-off 1, r02-repair-fresh 0 (1 repetitions, 2 variants)
first position per task: r70-7-go c01-review-off 0, r02-repair-fresh 1 (1 repetitions, 2 variants)
first position per task: rate-go c01-review-off 0, r02-repair-fresh 1 (1 repetitions, 2 variants)
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
