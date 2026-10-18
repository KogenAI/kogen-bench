complete: 4/4 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| a03-gherkin-off | 2       | 0         | 2                | 0              | 0          | 50%          | 0 of 2        | 0           |
false success: 0 of 2 claims (a03-gherkin-off)
shaping outcomes:
a03-gherkin-off: shaping ready 4, shaping failed 0; correct 2 of 4
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
| r70-5-go     | a03-gherkin-off | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | a03-gherkin-off | 0       | 0         | 1                | 0              | 0          |
| r70-7-go     | a03-gherkin-off | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| a03-gherkin-off | shape      | 0ms     | 0ms     | 0ms          | 0        |
| a03-gherkin-off | plan       | 37.6s   | 37.6s   | 0ms          | 4        |
| a03-gherkin-off | build      | 1567.6s | 1478.9s | 88.7s        | 155      |
| a03-gherkin-off | verify     | 29.7s   | 0ms     | 29.7s        | 0        |
| a03-gherkin-off | review     | 238.2s  | 238.2s  | 0ms          | 34       |
| a03-gherkin-off | commit     | 0ms     | 0ms     | 0ms          | 0        |
| a03-gherkin-off | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| a03-gherkin-off | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                    | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skf-a03-r70-5-elixir-r0-a03-gherkin-off-a1 | workflow failure | 872.6s | 812.4s | 60.2s        | 78       | 6       | 3       | 0         | 0                    |
| skf-a03-r70-5-go-r0-a03-gherkin-off-a1     | correct          | 273s   | 255.8s | 17.2s        | 27       | 2       | 3       | 0         | 0                    |
| skf-a03-r70-7-elixir-r0-a03-gherkin-off-a1 | workflow failure | 457.2s | 418.1s | 39.1s        | 59       | 6       | 3       | 0         | 0                    |
| skf-a03-r70-7-go-r0-a03-gherkin-off-a1     | correct          | 286.7s | 268.4s | 18.3s        | 29       | 3       | 4       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
a03-gherkin-off openai: input 3.45M, cached 1.56M, output 58.7k, reasoning 817, input_tokens_details.cache_write_tokens 0, total_tokens 3.50M
native usage by stage and provider:
stage build a03-gherkin-off openai (responses): input 3.08M, cached 1.56M, output 52.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.14M
stage plan a03-gherkin-off openai (responses): input 13.5k, cached 0, output 1.4k, reasoning 156, input_tokens_details.cache_write_tokens 0, total_tokens 14.9k
stage review a03-gherkin-off openai (responses): input 0.35M, cached 0, output 4.5k, reasoning 661, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
native usage by attempt and provider:
attempt usage skf-a03-r70-5-elixir-r0-a03-gherkin-off-a1 openai (responses): input 2.06M, cached 1.13M, output 29.1k, reasoning 80, input_tokens_details.cache_write_tokens 0, total_tokens 2.09M
attempt usage skf-a03-r70-5-go-r0-a03-gherkin-off-a1 openai (responses): input 0.28M, cached 37.8k, output 8.9k, reasoning 110, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage skf-a03-r70-7-elixir-r0-a03-gherkin-off-a1 openai (responses): input 0.83M, cached 0.35M, output 11.7k, reasoning 315, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
attempt usage skf-a03-r70-7-go-r0-a03-gherkin-off-a1 openai (responses): input 0.28M, cached 46.3k, output 9.0k, reasoning 312, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt outcomes included: a03-gherkin-off: correct 2, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 1889.5s, model 1754.7s, tools/checks 134.8s, requests 193
builder settings: a03-gherkin-off openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 4, scored 4, incorrect 0, infrastructure 0, incomplete 0
first position per task: r70-5-elixir a03-gherkin-off 1 (1 repetitions, 1 variants)
first position per task: r70-5-go a03-gherkin-off 1 (1 repetitions, 1 variants)
first position per task: r70-7-elixir a03-gherkin-off 1 (1 repetitions, 1 variants)
first position per task: r70-7-go a03-gherkin-off 1 (1 repetitions, 1 variants)
a03-gherkin-off: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
a03-gherkin-off: repair.context = packet,diff,check_results,review_findings (extension)
a03-gherkin-off: repair.roles = builder (extension)
a03-gherkin-off: shape.critique_prompt = lab:critique (extension)
a03-gherkin-off: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
