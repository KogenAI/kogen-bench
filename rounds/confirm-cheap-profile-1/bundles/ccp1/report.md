complete: 16/16 cells scored
Question: confirm-cheap-profile-1: on fresh tasks, is the Sol-low builder plus Sol-medium reviewer-fixer correct in as many blocks as Kogen's defaults, with no more wrong submissions, at no more than 75% of their total input?
Hypothesis: cheap is correct in at least as many paired blocks as kogen-default with at most 75% of its total input
Purpose: confirmation
Objective: cost_at_quality
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant       | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen-default | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| cheap         | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (kogen-default)
false success: 0 of 8 claims (cheap)
shaping outcomes:
kogen-default: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
cheap: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task        | variant       | correct | incorrect | workflow failure | infrastructure | incomplete |
|-------------|---------------|---------|-----------|------------------|----------------|------------|
| deps-ex     | kogen-default | 2       | 0         | 0                | 0              | 0          |
| deps-ex     | cheap         | 2       | 0         | 0                | 0              | 0          |
| deps-go     | kogen-default | 2       | 0         | 0                | 0              | 0          |
| deps-go     | cheap         | 2       | 0         | 0                | 0              | 0          |
| interval-ex | kogen-default | 2       | 0         | 0                | 0              | 0          |
| interval-ex | cheap         | 2       | 0         | 0                | 0              | 0          |
| interval-go | kogen-default | 2       | 0         | 0                | 0              | 0          |
| interval-go | cheap         | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant       | stage      | wall   | model  | tools/checks | requests |
|---------------|------------|--------|--------|--------------|----------|
| kogen-default | shape      | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | plan       | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | build      | 976.9s | 913s   | 63.9s        | 61       |
| kogen-default | verify     | 11.7s  | 0ms    | 11.7s        | 0        |
| kogen-default | review     | 289.3s | 289.3s | 0ms          | 35       |
| kogen-default | commit     | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| kogen-default | assessment | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | shape      | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | plan       | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | build      | 565.2s | 525.6s | 39.6s        | 45       |
| cheap         | verify     | 20.3s  | 0ms    | 20.3s        | 0        |
| cheap         | review     | 423.2s | 423.2s | 0ms          | 49       |
| cheap         | commit     | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | evaluate   | 0ms    | 0ms    | 0ms          | 0        |
| cheap         | assessment | 0ms    | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| ccp1-deps-ex-r0-cheap-a1             | correct | 131.8s | 119.1s | 12.7s        | 14       | 0       | 1       | 0         | 0                    |
| ccp1-deps-ex-r0-kogen-default-a1     | correct | 175.9s | 153.1s | 22.8s        | 14       | 0       | 1       | 0         | 0                    |
| ccp1-deps-ex-r1-cheap-a1             | correct | 117.8s | 105.4s | 12.4s        | 12       | 0       | 1       | 0         | 0                    |
| ccp1-deps-ex-r1-kogen-default-a1     | correct | 166.5s | 153.4s | 13.1s        | 16       | 0       | 2       | 0         | 0                    |
| ccp1-deps-go-r0-cheap-a1             | correct | 124s   | 113s   | 11s          | 11       | 0       | 1       | 0         | 0                    |
| ccp1-deps-go-r0-kogen-default-a1     | correct | 175.8s | 166.8s | 9s           | 11       | 0       | 1       | 0         | 0                    |
| ccp1-deps-go-r1-cheap-a1             | correct | 150s   | 139.2s | 10.9s        | 13       | 0       | 1       | 0         | 0                    |
| ccp1-deps-go-r1-kogen-default-a1     | correct | 173.9s | 164.1s | 9.8s         | 12       | 0       | 1       | 0         | 0                    |
| ccp1-interval-ex-r0-cheap-a1         | correct | 128.5s | 114.6s | 13.8s        | 11       | 0       | 1       | 0         | 0                    |
| ccp1-interval-ex-r0-kogen-default-a1 | correct | 161s   | 141s   | 20s          | 12       | 0       | 1       | 0         | 0                    |
| ccp1-interval-ex-r1-cheap-a1         | correct | 115.3s | 108.4s | 7s           | 10       | 0       | 1       | 0         | 0                    |
| ccp1-interval-ex-r1-kogen-default-a1 | correct | 150.9s | 139.9s | 11.1s        | 10       | 0       | 1       | 0         | 0                    |
| ccp1-interval-go-r0-cheap-a1         | correct | 137.8s | 126.4s | 11.5s        | 11       | 0       | 1       | 0         | 0                    |
| ccp1-interval-go-r0-kogen-default-a1 | correct | 142.3s | 134.3s | 7.9s         | 11       | 0       | 1       | 0         | 0                    |
| ccp1-interval-go-r1-cheap-a1         | correct | 132.1s | 122.9s | 9.3s         | 12       | 0       | 1       | 0         | 0                    |
| ccp1-interval-go-r1-kogen-default-a1 | correct | 158.3s | 149.6s | 8.8s         | 10       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
cheap openai: input 1.03M, cached 24.1k, output 32.3k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
kogen-default openai: input 1.08M, cached 37.4k, output 42.9k, reasoning 5.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.12M
native usage by stage and provider:
stage build cheap openai (responses): input 0.35M, cached 11.4k, output 19.1k, reasoning 36, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
stage build kogen-default openai (responses): input 0.57M, cached 24.7k, output 35.3k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
stage review cheap openai (responses): input 0.68M, cached 12.7k, output 13.2k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
stage review kogen-default openai (responses): input 0.51M, cached 12.7k, output 7.6k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.52M
native usage by attempt and provider:
attempt usage ccp1-deps-ex-r0-cheap-a1 openai (responses): input 0.16M, cached 0, output 3.9k, reasoning 290, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage ccp1-deps-ex-r0-kogen-default-a1 openai (responses): input 0.16M, cached 23.9k, output 5.4k, reasoning 781, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage ccp1-deps-ex-r1-cheap-a1 openai (responses): input 0.13M, cached 5.6k, output 3.4k, reasoning 163, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ccp1-deps-ex-r1-kogen-default-a1 openai (responses): input 0.17M, cached 0, output 5.2k, reasoning 533, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage ccp1-deps-go-r0-cheap-a1 openai (responses): input 0.12M, cached 12.7k, output 3.9k, reasoning 164, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage ccp1-deps-go-r0-kogen-default-a1 openai (responses): input 0.13M, cached 0, output 6.4k, reasoning 585, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ccp1-deps-go-r1-cheap-a1 openai (responses): input 0.14M, cached 0, output 4.5k, reasoning 386, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage ccp1-deps-go-r1-kogen-default-a1 openai (responses): input 0.14M, cached 0, output 6.0k, reasoning 830, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage ccp1-interval-ex-r0-cheap-a1 openai (responses): input 0.12M, cached 0, output 3.9k, reasoning 137, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ccp1-interval-ex-r0-kogen-default-a1 openai (responses): input 0.13M, cached 7.7k, output 4.7k, reasoning 609, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ccp1-interval-ex-r1-cheap-a1 openai (responses): input 0.11M, cached 5.8k, output 4.0k, reasoning 160, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage ccp1-interval-ex-r1-kogen-default-a1 openai (responses): input 0.11M, cached 0, output 5.5k, reasoning 805, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage ccp1-interval-go-r0-cheap-a1 openai (responses): input 0.12M, cached 0, output 4.5k, reasoning 184, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage ccp1-interval-go-r0-kogen-default-a1 openai (responses): input 0.12M, cached 5.8k, output 4.9k, reasoning 515, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage ccp1-interval-go-r1-cheap-a1 openai (responses): input 0.13M, cached 0, output 4.3k, reasoning 138, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage ccp1-interval-go-r1-kogen-default-a1 openai (responses): input 0.11M, cached 0, output 4.8k, reasoning 446, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt outcomes included: kogen-default: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; cheap: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2342.1s, model 2151.2s, tools/checks 191s, requests 190
builder settings: kogen-default openai gpt-6.1-sol reasoning.effort=medium; cheap openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant cheap differs from kogen-default in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6.1-sol low
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
roles.builder.effort: exercised in 8 of 8 cheap attempts
roles.reviewer.effort: exercised in 8 of 8 cheap attempts
first position per task: deps-ex kogen-default 1, cheap 1 (2 repetitions, 2 variants)
first position per task: deps-go kogen-default 1, cheap 1 (2 repetitions, 2 variants)
first position per task: interval-ex kogen-default 1, cheap 1 (2 repetitions, 2 variants)
first position per task: interval-go kogen-default 1, cheap 1 (2 repetitions, 2 variants)
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
