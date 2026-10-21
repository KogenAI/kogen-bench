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
| artifact-go  | kogen-default | 1       | 0         | 0                | 0              | 0          |
| artifact-go  | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | cheap         | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | kogen-default | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | cheap         | 1       | 0         | 0                | 0              | 0          |
| rate-go      | kogen-default | 1       | 0         | 0                | 0              | 0          |
| rate-go      | cheap         | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant       | stage      | wall   | model  | tools/checks | requests |
|---------------|------------|--------|--------|--------------|----------|
| kogen-default | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | plan       | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | build      | 777.3s | 755.3s | 22.1s        | 29       |
| kogen-default | verify     | 3.6s   | 0ms    | 3.6s         | 0        |
| kogen-default | review     | 342.5s | 342.5s | 0ms          | 15       |
| kogen-default | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | assessment | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | shape      | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | plan       | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | build      | 571.3s | 560.4s | 10.9s        | 20       |
| cheap         | verify     | 4.7s   | 0ms    | 4.7s         | 0        |
| cheap         | review     | 435.8s | 435.8s | 0ms          | 16       |
| cheap         | commit     | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cp2-artifact-go-r0-cheap-a1          | correct | 254.1s | 241.5s | 12.6s        | 9        | 0       | 1       | 0         | 0                    |
| cp2-artifact-go-r0-kogen-default-a1  | correct | 209.8s | 193.7s | 16.1s        | 12       | 0       | 1       | 0         | 0                    |
| cp2-r70-5-elixir-r0-cheap-a1         | correct | 320.2s | 312.1s | 8.2s         | 10       | 0       | 1       | 0         | 0                    |
| cp2-r70-5-elixir-r0-kogen-default-a1 | correct | 337.9s | 322s   | 15.9s        | 12       | 0       | 1       | 0         | 0                    |
| cp2-r70-5-go-r0-cheap-a1             | correct | 325.4s | 315.6s | 9.8s         | 11       | 0       | 1       | 0         | 0                    |
| cp2-r70-5-go-r0-kogen-default-a1     | correct | 373.8s | 365.2s | 8.6s         | 13       | 0       | 1       | 0         | 0                    |
| cp2-rate-go-r0-cheap-a1              | correct | 131.3s | 127.1s | 4.2s         | 6        | 0       | 1       | 0         | 0                    |
| cp2-rate-go-r0-kogen-default-a1      | correct | 221.4s | 216.9s | 4.5s         | 7        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
cheap openai: input 0.33M, cached 5.9k, output 11.0k, reasoning 535, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
kogen-default openai: input 0.41M, cached 25.0k, output 16.2k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
native usage by stage and provider:
stage build cheap openai (responses): input 0.14M, cached 5.9k, output 8.1k, reasoning 65, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
stage build kogen-default openai (responses): input 0.24M, cached 13.2k, output 13.5k, reasoning 738, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
stage review cheap openai (responses): input 0.19M, cached 0, output 2.9k, reasoning 470, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
stage review kogen-default openai (responses): input 0.18M, cached 11.8k, output 2.8k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
native usage by attempt and provider:
attempt usage cp2-artifact-go-r0-cheap-a1 openai (responses): input 73.8k, cached 5.9k, output 2.6k, reasoning 73, input_tokens_details.cache_write_tokens 0, total_tokens 76.4k
attempt usage cp2-artifact-go-r0-kogen-default-a1 openai (responses): input 0.11M, cached 4.9k, output 3.8k, reasoning 266, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage cp2-r70-5-elixir-r0-cheap-a1 openai (responses): input 0.10M, cached 0, output 3.2k, reasoning 241, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage cp2-r70-5-elixir-r0-kogen-default-a1 openai (responses): input 0.12M, cached 11.8k, output 5.6k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage cp2-r70-5-go-r0-cheap-a1 openai (responses): input 0.11M, cached 0, output 4.1k, reasoning 183, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage cp2-r70-5-go-r0-kogen-default-a1 openai (responses): input 0.14M, cached 8.3k, output 5.2k, reasoning 784, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage cp2-rate-go-r0-cheap-a1 openai (responses): input 36.9k, cached 0, output 1.2k, reasoning 38, input_tokens_details.cache_write_tokens 0, total_tokens 38.2k
attempt usage cp2-rate-go-r0-kogen-default-a1 openai (responses): input 45.3k, cached 0, output 1.6k, reasoning 88, input_tokens_details.cache_write_tokens 0, total_tokens 46.9k
attempt outcomes included: kogen-default: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; cheap: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2173.9s, model 2094s, tools/checks 79.9s, requests 80
builder settings: kogen-default openai gpt-6.1-sol reasoning.effort=medium; cheap openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 8, started 8, scored 8, incorrect 0, infrastructure 0, incomplete 0
variant cheap differs from kogen-default in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6.1-sol low
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.builder.effort: exercised in 4 of 4 cheap attempts
roles.reviewer.effort: exercised in 4 of 4 cheap attempts
first position per task: artifact-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: r70-5-elixir kogen-default 1, cheap 0 (1 repetitions, 2 variants)
first position per task: r70-5-go kogen-default 0, cheap 1 (1 repetitions, 2 variants)
first position per task: rate-go kogen-default 1, cheap 0 (1 repetitions, 2 variants)
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
