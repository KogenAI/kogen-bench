complete: 8/8 cells scored
Question: cheap-profile-1: does a Sol-low builder with a Sol-medium reviewer-fixer keep Kogen's default correctness on the harder tasks at a much lower total input?
Hypothesis: exploratory: same correctness, total input at least 25% lower
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen-default | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
| cheap         | 4       | 0         | 0                | 0              | 0          | 100%         | 0 of 4        | 0           |
false success: 0 of 4 claims (kogen-default)
false success: 0 of 4 claims (cheap)
shaping outcomes:
kogen-default: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
cheap: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant       | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|---------------|---------|-----------|------------------|----------------|------------|
| r70-1-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-1-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: elapsed time, model, tools/checks, requests
| variant       | stage      | elapsed time   | model  | tools/checks | requests |
|---------------|------------|--------|--------|--------------|----------|
| kogen-default | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | plan       | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | build      | 598.8s | 528.4s | 70.5s        | 37       |
| kogen-default | verify     | 24.3s  | 0ms    | 24.3s        | 0        |
| kogen-default | review     | 676.4s | 676.4s | 0ms          | 34       |
| kogen-default | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | assessment | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | shape      | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | plan       | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | build      | 331.7s | 290.8s | 40.9s        | 27       |
| cheap         | verify     | 11.2s  | 0ms    | 11.2s        | 0        |
| cheap         | review     | 385.2s | 385.2s | 0ms          | 28       |
| cheap         | commit     | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome | elapsed time   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cp1-r70-1-go-r0-cheap-a1             | correct | 260.4s | 241s   | 19.4s        | 16       | 0       | 1       | 0         | 0                    |
| cp1-r70-1-go-r0-kogen-default-a1     | correct | 521.1s | 490.3s | 30.8s        | 24       | 0       | 1       | 0         | 0                    |
| cp1-r70-4-go-r0-cheap-a1             | correct | 161.2s | 142.6s | 18.6s        | 14       | 0       | 1       | 0         | 0                    |
| cp1-r70-4-go-r0-kogen-default-a1     | correct | 359.7s | 325.5s | 34.1s        | 20       | 0       | 1       | 0         | 0                    |
| cp1-r70-7-elixir-r0-cheap-a1         | correct | 146s   | 126.1s | 19.9s        | 12       | 0       | 1       | 0         | 0                    |
| cp1-r70-7-elixir-r0-kogen-default-a1 | correct | 224.5s | 190.4s | 34s          | 13       | 0       | 1       | 0         | 0                    |
| cp1-r70-7-go-r0-cheap-a1             | correct | 178.8s | 166.3s | 12.5s        | 13       | 0       | 1       | 0         | 0                    |
| cp1-r70-7-go-r0-kogen-default-a1     | correct | 212.7s | 198.5s | 14.2s        | 14       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
cheap openai: input 0.63M, cached 27.9k, output 22.7k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
kogen-default openai: input 1.16M, cached 36.1k, output 44.2k, reasoning 15.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
native usage by stage and provider:
stage build cheap openai (responses): input 0.21M, cached 27.9k, output 9.3k, reasoning 238, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
stage build kogen-default openai (responses): input 0.35M, cached 20.1k, output 18.9k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
stage review cheap openai (responses): input 0.42M, cached 0, output 13.4k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
stage review kogen-default openai (responses): input 0.80M, cached 16.0k, output 25.3k, reasoning 13.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.83M
native usage by attempt and provider:
attempt usage cp1-r70-1-go-r0-cheap-a1 openai (responses): input 0.22M, cached 20.1k, output 8.2k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage cp1-r70-1-go-r0-kogen-default-a1 openai (responses): input 0.57M, cached 21.6k, output 17.9k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage cp1-r70-4-go-r0-cheap-a1 openai (responses): input 0.16M, cached 0, output 4.6k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cp1-r70-4-go-r0-kogen-default-a1 openai (responses): input 0.28M, cached 14.5k, output 12.6k, reasoning 4.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage cp1-r70-7-elixir-r0-cheap-a1 openai (responses): input 0.12M, cached 7.8k, output 4.1k, reasoning 229, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage cp1-r70-7-elixir-r0-kogen-default-a1 openai (responses): input 0.15M, cached 0, output 6.8k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cp1-r70-7-go-r0-cheap-a1 openai (responses): input 0.13M, cached 0, output 5.9k, reasoning 209, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage cp1-r70-7-go-r0-kogen-default-a1 openai (responses): input 0.15M, cached 0, output 6.8k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt outcomes included: kogen-default: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; cheap: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; elapsed time 2064.3s, model 1880.8s, tools/checks 183.5s, requests 126
builder settings: kogen-default openai gpt-6.1-sol reasoning.effort=medium; cheap openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant cheap differs from kogen-default in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6.1-sol low
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.builder.effort: exercised in 4 of 4 cheap attempts
roles.reviewer.effort: exercised in 4 of 4 cheap attempts
first position per task: r70-1-go kogen-default 1, cheap 0 (1 repetitions, 2 variants)
first position per task: r70-4-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-7-elixir kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-7-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
kogen-default: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
cheap: not the Kogen profile (differs in roles.builder.effort, roles.reviewer.effort, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
kogen-default: build.helper_context = lab_helper (extension)
kogen-default: build.helper_prompt = lab:helper (extension)
kogen-default: build.subagents_output = 4096 (extension)
kogen-default: build.subagents_turns = 10 (extension)
kogen-default: plan.context = kogen_planner (extension)
kogen-default: plan.prompt = lab:plan (extension)
kogen-default: repair.context = packet,diff,check_results,review_findings (extension)
kogen-default: repair.roles = builder (extension)
kogen-default: review.timing = every_green (extension)
kogen-default: shape.critique_prompt = lab:critique (extension)
kogen-default: shape.critique_rounds = 1 (extension)
kogen-default: shape.helper_context = lab_helper (extension)
kogen-default: shape.helper_prompt = lab:helper (extension)
kogen-default: shape.subagents_output = 4096 (extension)
kogen-default: shape.subagents_turns = 10 (extension)
cheap: build.helper_context = lab_helper (extension)
cheap: build.helper_prompt = lab:helper (extension)
cheap: build.subagents_output = 4096 (extension)
cheap: build.subagents_turns = 10 (extension)
cheap: plan.context = kogen_planner (extension)
cheap: plan.prompt = lab:plan (extension)
cheap: repair.context = packet,diff,check_results,review_findings (extension)
cheap: repair.roles = builder (extension)
cheap: review.timing = every_green (extension)
cheap: shape.critique_prompt = lab:critique (extension)
cheap: shape.critique_rounds = 1 (extension)
cheap: shape.helper_context = lab_helper (extension)
cheap: shape.helper_prompt = lab:helper (extension)
cheap: shape.subagents_output = 4096 (extension)
cheap: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
