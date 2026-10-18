complete: 8/8 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| b07-output-full | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| a03-gherkin-off | 0       | 0         | 4                | 0              | 0          | 0%           | 0 of 0        | 0           |
false success: 0 of 4 claims (b07-output-full)
false success: 0 of 0 claims (a03-gherkin-off)
shaping outcomes:
b07-output-full: shaping ready 4, shaping failed 0; correct 4 of 4
a03-gherkin-off: shaping ready 4, shaping failed 0; correct 0 of 4
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | b07-output-full | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
| r70-5-go     | b07-output-full | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | b07-output-full | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
| r70-7-go     | b07-output-full | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall   | model  | tools/checks | requests |
|-----------------|------------|--------|--------|--------------|----------|
| b07-output-full | shape      | 0ms    | 0ms    | 0ms          | 0        |
| b07-output-full | plan       | 30.2s  | 30.2s  | 0ms          | 4        |
| b07-output-full | build      | 733.9s | 665.7s | 68.2s        | 80       |
| b07-output-full | verify     | 21.9s  | 0ms    | 21.9s        | 0        |
| b07-output-full | review     | 145.5s | 145.5s | 0ms          | 23       |
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
| attempt                                        | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skf-b07-a03-r70-5-elixir-r0-a03-gherkin-off-a1 | workflow failure | 4.2s   | 0ms    | 4.2s         | 0        | 0       | 0       | 0         | 0                    |
| skf-b07-a03-r70-5-elixir-r0-b07-output-full-a1 | correct          | 409.8s | 349.6s | 60.2s        | 45       | 4       | 3       | 0         | 0                    |
| skf-b07-a03-r70-5-go-r0-a03-gherkin-off-a1     | workflow failure | 7.9s   | 0ms    | 7.9s         | 0        | 0       | 0       | 0         | 0                    |
| skf-b07-a03-r70-5-go-r0-b07-output-full-a1     | correct          | 173.4s | 160.3s | 13.1s        | 20       | 1       | 2       | 0         | 0                    |
| skf-b07-a03-r70-7-elixir-r0-a03-gherkin-off-a1 | workflow failure | 4.2s   | 0ms    | 4.2s         | 0        | 0       | 0       | 0         | 0                    |
| skf-b07-a03-r70-7-elixir-r0-b07-output-full-a1 | correct          | 234.4s | 213.5s | 20.9s        | 25       | 2       | 2       | 0         | 0                    |
| skf-b07-a03-r70-7-go-r0-a03-gherkin-off-a1     | workflow failure | 7.9s   | 0ms    | 7.9s         | 0        | 0       | 0       | 0         | 0                    |
| skf-b07-a03-r70-7-go-r0-b07-output-full-a1     | correct          | 142.2s | 117.9s | 24.3s        | 17       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
b07-output-full openai: input 1.42M, cached 0.32M, output 26.2k, reasoning 718, input_tokens_details.cache_write_tokens 0, total_tokens 1.45M
native usage by stage and provider:
stage build b07-output-full openai (responses): input 1.05M, cached 0.32M, output 22.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
stage plan b07-output-full openai (responses): input 17.2k, cached 0, output 947, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.1k
stage review b07-output-full openai (responses): input 0.35M, cached 0, output 2.5k, reasoning 718, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
native usage by attempt and provider:
attempt usage skf-b07-a03-r70-5-elixir-r0-b07-output-full-a1 openai (responses): input 0.72M, cached 0.24M, output 10.3k, reasoning 321, input_tokens_details.cache_write_tokens 0, total_tokens 0.73M
attempt usage skf-b07-a03-r70-5-go-r0-b07-output-full-a1 openai (responses): input 0.18M, cached 22.7k, output 5.2k, reasoning 50, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage skf-b07-a03-r70-7-elixir-r0-b07-output-full-a1 openai (responses): input 0.35M, cached 63.9k, output 7.4k, reasoning 174, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage skf-b07-a03-r70-7-go-r0-b07-output-full-a1 openai (responses): input 0.18M, cached 0, output 3.4k, reasoning 173, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt outcomes included: b07-output-full: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; a03-gherkin-off: correct 0, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 984.1s, model 841.3s, tools/checks 142.8s, requests 107
builder settings: b07-output-full openai gpt-6-luna reasoning.effort=low
builder settings: a03-gherkin-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant a03-gherkin-off differs from b07-output-full in:
  artifacts.gherkin: executed -> off
  build.output: full -> kogen_16k
  shape.supplied: gherkin -> prose
A03: exercised in 4 of 4 a03-gherkin-off attempts
B07: exercised in 4 of 4 a03-gherkin-off attempts
MODE: exercised in 4 of 4 a03-gherkin-off attempts
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
