complete: 4/4 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen   | 2       | 0         | 2                | 0              | 0          | 50%          | 0 of 2        | 0           |
false success: 0 of 2 claims (kogen)
shaping outcomes:
kogen: shaping ready 4, shaping failed 0; correct 2 of 4
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | kogen   | 0       | 0         | 1                | 0              | 0          |
| r70-5-go     | kogen   | 0       | 0         | 1                | 0              | 0          |
| r70-7-elixir | kogen   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | kogen   | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall   | model  | tools/checks | requests |
|---------|------------|--------|--------|--------------|----------|
| kogen   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | plan       | 28s    | 28s    | 0ms          | 4        |
| kogen   | build      | 762.4s | 708.8s | 53.6s        | 63       |
| kogen   | verify     | 15.9s  | 0ms    | 15.9s        | 0        |
| kogen   | review     | 143.6s | 143.6s | 0ms          | 22       |
| kogen   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| skf-baseline-r70-5-elixir-r0-kogen-a1 | workflow failure | 432.3s | 396.9s | 35.4s        | 38       | 6       | 2       | 0         | 0                    |
| skf-baseline-r70-5-go-r0-kogen-a1     | workflow failure | 72.6s  | 67.5s  | 5.1s         | 5        | 0       | 0       | 0         | 0                    |
| skf-baseline-r70-7-elixir-r0-kogen-a1 | correct          | 232.1s | 204s   | 28.1s        | 24       | 1       | 2       | 0         | 0                    |
| skf-baseline-r70-7-go-r0-kogen-a1     | correct          | 228.5s | 212.1s | 16.4s        | 22       | 2       | 3       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen openai: input 1.16M, cached 0.25M, output 31.3k, reasoning 562, input_tokens_details.cache_write_tokens 0, total_tokens 1.19M
native usage by stage and provider:
stage build kogen openai (responses): input 0.82M, cached 0.25M, output 27.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
stage plan kogen openai (responses): input 17.2k, cached 0, output 872, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 18.1k
stage review kogen openai (responses): input 0.33M, cached 0, output 2.5k, reasoning 562, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
native usage by attempt and provider:
attempt usage skf-baseline-r70-5-elixir-r0-kogen-a1 openai (responses): input 0.57M, cached 0.18M, output 14.5k, reasoning 121, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt usage skf-baseline-r70-5-go-r0-kogen-a1 openai (responses): input 30.8k, cached 0, output 2.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 33.7k
attempt usage skf-baseline-r70-7-elixir-r0-kogen-a1 openai (responses): input 0.26M, cached 30.3k, output 6.8k, reasoning 118, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage skf-baseline-r70-7-go-r0-kogen-a1 openai (responses): input 0.30M, cached 43.0k, output 7.2k, reasoning 323, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt outcomes included: kogen: correct 2, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 965.5s, model 880.5s, tools/checks 85s, requests 89
builder settings: kogen openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 4, scored 4, incorrect 0, infrastructure 0, incomplete 0
first position per task: r70-5-elixir kogen 1 (1 repetitions, 1 variants)
first position per task: r70-5-go kogen 1 (1 repetitions, 1 variants)
first position per task: r70-7-elixir kogen 1 (1 repetitions, 1 variants)
first position per task: r70-7-go kogen 1 (1 repetitions, 1 variants)
kogen: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
kogen: repair.context = packet,diff,check_results,review_findings (extension)
kogen: repair.roles = builder (extension)
kogen: shape.critique_prompt = lab:critique (extension)
kogen: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
