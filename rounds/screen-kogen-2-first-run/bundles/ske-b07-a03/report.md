incomplete: 0 of 8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 8 cells scored)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| b07-output-full | 0       | 0         | 0                | 0              | 1          | unavailable  | 0 of 0        | 0           |
| a03-gherkin-off | 0       | 0         | 0                | 0              | 0          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (b07-output-full)
false success: 0 of 0 claims (a03-gherkin-off)
shaping outcomes:
b07-output-full: shaping ready 1, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | b07-output-full | 0       | 0         | 0                | 0              | 1          |
| r70-5-elixir | a03-gherkin-off | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | b07-output-full | 0       | 0         | 0                | 0              | 0          |
| r70-5-go     | a03-gherkin-off | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | b07-output-full | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | a03-gherkin-off | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | b07-output-full | 0       | 0         | 0                | 0              | 0          |
| r70-7-go     | a03-gherkin-off | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall   | model  | tools/checks | requests |
|-----------------|------------|--------|--------|--------------|----------|
| b07-output-full | shape      | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full | plan       | 8.2s   | 8.2s   | 0ms          | 1        |
| b07-output-full | build      | 124.7s | 113.3s | 11.4s        | 10       |
| b07-output-full | verify     | 2.8s   | 0ms    | 2.8s         | 0        |
| b07-output-full | review     | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full | commit     | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full | assessment | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | shape      | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | plan       | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | build      | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | verify     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | review     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | commit     | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| a03-gherkin-off | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                        | outcome    | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------------|------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ske-b07-a03-r70-5-elixir-r0-b07-output-full-a1 | incomplete | 140.5s | 121.5s | 19s          | 11       | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
b07-output-full openai: input 0.43M, cached 0.11M, output 4.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
native usage by stage and provider:
stage build b07-output-full openai (responses): input 0.40M, cached 75.6k, output 4.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
stage plan b07-output-full openai (responses): input 34.3k, cached 34.2k, output 261, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 34.6k
native usage by attempt and provider:
attempt usage ske-b07-a03-r70-5-elixir-r0-b07-output-full-a1 openai (responses): input 0.43M, cached 0.11M, output 4.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt outcomes included: b07-output-full: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; a03-gherkin-off: correct 0, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 140.5s, model 121.5s, tools/checks 19s, requests 11
builder settings: b07-output-full openai gpt-6-luna reasoning.effort=low
builder settings: a03-gherkin-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 1, scored 0, incorrect 0, infrastructure 0, incomplete 1
variant a03-gherkin-off differs from b07-output-full in:
  artifacts.gherkin: executed -> off
  build.output: full -> kogen_16k
  shape.supplied: gherkin -> prose
artifacts.gherkin: not exercised
build.output: not exercised
shape.supplied: not exercised
first position per task: r70-5-elixir b07-output-full 1, a03-gherkin-off 0 (1 repetitions, 2 variants)
first position per task: r70-5-go b07-output-full 1, a03-gherkin-off 0 (1 repetitions, 2 variants)
first position per task: r70-7-elixir b07-output-full 0, a03-gherkin-off 1 (1 repetitions, 2 variants)
first position per task: r70-7-go b07-output-full 0, a03-gherkin-off 1 (1 repetitions, 2 variants)
b07-output-full: not the Kogen profile (differs in build.output, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
a03-gherkin-off: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
b07-output-full: build.output = full (extension)
b07-output-full: repair.context = packet,diff,check_results,review_findings (extension)
b07-output-full: repair.roles = builder (extension)
b07-output-full: shape.critique_prompt = lab:critique (extension)
b07-output-full: shape.critique_rounds = 1 (extension)
a03-gherkin-off: repair.context = packet,diff,check_results,review_findings (extension)
a03-gherkin-off: repair.roles = builder (extension)
a03-gherkin-off: shape.critique_prompt = lab:critique (extension)
a03-gherkin-off: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
