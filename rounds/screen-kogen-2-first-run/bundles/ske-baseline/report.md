incomplete: 0 of 4 cells scored
Question: screen-kogen-2: how do single Kogen levers change correctness and cost on harder tasks with the stage-d configuration?
Hypothesis: exploratory screening; removing verification (V01) lowers correctness
Purpose: screening
Objective: correctness
Rule: descriptive
Decision: none yet (0 of 4 cells scored)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen   | 0       | 0         | 0                | 1              | 1          | unavailable  | 0 of 0        | 0           |
false success: 0 of 0 claims (kogen)
shaping outcomes:
kogen: shaping ready 2, shaping failed 0; correct 0 of 0
## Per-task outcomes
| task         | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | kogen   | 0       | 0         | 0                | 1              | 0          |
| r70-5-go     | kogen   | 0       | 0         | 0                | 0              | 0          |
| r70-7-elixir | kogen   | 0       | 0         | 0                | 0              | 1          |
| r70-7-go     | kogen   | 0       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall   | model  | tools/checks | requests |
|---------|------------|--------|--------|--------------|----------|
| kogen   | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | plan       | 13.8s  | 13.8s  | 0ms          | 2        |
| kogen   | build      | 109.3s | 102.7s | 6.6s         | 11       |
| kogen   | verify     | 1.5s   | 0ms    | 1.5s         | 0        |
| kogen   | review     | 228s   | 228s   | 0ms          | 1        |
| kogen   | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen   | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome        | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|----------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ske-baseline-r70-5-elixir-r0-kogen-a1 | infrastructure | 331.6s | 320.4s | 11.2s        | 11       | 0       | 0       | 0         | 0                    |
| ske-baseline-r70-7-elixir-r0-kogen-a1 | incomplete     | 26.5s  | 24.1s  | 2.3s         | 3        | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen openai: input 0.49M, cached 75.6k, output 4.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
native usage by stage and provider:
stage build kogen openai (responses): input 0.42M, cached 75.6k, output 3.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
stage plan kogen openai (responses): input 68.7k, cached 0, output 420, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 69.1k
native usage by attempt and provider:
attempt usage ske-baseline-r70-5-elixir-r0-kogen-a1 openai (responses): input 0.38M, cached 75.6k, output 3.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.39M
attempt usage ske-baseline-r70-7-elixir-r0-kogen-a1 openai (responses): input 0.11M, cached 0, output 828, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt outcomes included: kogen: correct 0, incorrect 0, workflow failure 0, infrastructure 1, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 358.1s, model 344.6s, tools/checks 13.5s, requests 14
builder settings: kogen openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 4, started 2, scored 0, incorrect 0, infrastructure 1, incomplete 1
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
