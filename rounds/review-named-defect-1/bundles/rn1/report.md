complete: 16/16 cells scored
Question: review-named-defect-1: does telling Kogen's Sol-high reviewer-fixer to edit only to fix a defect it can name cut polish edits and reviewer input without losing rescues or adding wrong submissions?
Hypothesis: exploratory: fewer polish edits and less reviewer input; rescues unchanged
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant      | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|--------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen-review | 6       | 2         | 0                | 0              | 0          | 75%          | 2 of 8        | 0           |
| named-defect | 6       | 2         | 0                | 0              | 0          | 75%          | 2 of 8        | 0           |
false success: 2 of 8 claims (kogen-review)
false success: 2 of 8 claims (named-defect)
shaping outcomes:
kogen-review: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
named-defect: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant      | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|--------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | kogen-review | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | named-defect | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | kogen-review | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | named-defect | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | kogen-review | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | named-defect | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | kogen-review | 0       | 2         | 0                | 0              | 0          |
| r70-6-elixir-2 | named-defect | 0       | 2         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant      | stage      | wall    | model   | tools/checks | requests |
|--------------|------------|---------|---------|--------------|----------|
| kogen-review | shape      | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | plan       | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | build      | 1715s   | 1475.1s | 239.9s       | 92       |
| kogen-review | verify     | 81.3s   | 0ms     | 81.3s        | 0        |
| kogen-review | review     | 1167s   | 1167s   | 0ms          | 61       |
| kogen-review | commit     | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| kogen-review | assessment | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | shape      | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | plan       | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | build      | 1458.2s | 1281.4s | 176.9s       | 85       |
| named-defect | verify     | 88.3s   | 0ms     | 88.3s        | 0        |
| named-defect | review     | 834s    | 834s    | 0ms          | 58       |
| named-defect | commit     | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| named-defect | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                               | outcome   | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|---------------------------------------|-----------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rn1-r70-1-go-r0-kogen-review-a1       | correct   | 582.9s | 539.4s | 43.5s        | 23       | 0       | 1       | 0         | 0                    |
| rn1-r70-1-go-r0-named-defect-a1       | correct   | 310.8s | 292s   | 18.8s        | 16       | 0       | 1       | 0         | 0                    |
| rn1-r70-1-go-r1-kogen-review-a1       | correct   | 441s   | 409.7s | 31.3s        | 24       | 0       | 1       | 0         | 0                    |
| rn1-r70-1-go-r1-named-defect-a1       | correct   | 365.2s | 342.6s | 22.6s        | 20       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-elixir-2-r0-kogen-review-a1 | correct   | 363.8s | 304.7s | 59.2s        | 19       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-elixir-2-r0-named-defect-a1 | correct   | 367.7s | 301.5s | 66.2s        | 22       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-elixir-2-r1-kogen-review-a1 | correct   | 422.8s | 348.2s | 74.6s        | 20       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-elixir-2-r1-named-defect-a1 | correct   | 324s   | 260s   | 64s          | 17       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-go-r0-kogen-review-a1       | correct   | 361.7s | 319.7s | 42s          | 18       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-go-r0-named-defect-a1       | correct   | 267.7s | 230.4s | 37.2s        | 17       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-go-r1-kogen-review-a1       | correct   | 311.8s | 295s   | 16.8s        | 15       | 0       | 1       | 0         | 0                    |
| rn1-r70-4-go-r1-named-defect-a1       | correct   | 288.4s | 273.7s | 14.8s        | 16       | 0       | 1       | 0         | 0                    |
| rn1-r70-6-elixir-2-r0-kogen-review-a1 | incorrect | 222.1s | 199.2s | 23s          | 14       | 0       | 1       | 0         | 0                    |
| rn1-r70-6-elixir-2-r0-named-defect-a1 | incorrect | 216s   | 187.9s | 28.1s        | 15       | 0       | 1       | 0         | 0                    |
| rn1-r70-6-elixir-2-r1-kogen-review-a1 | incorrect | 295.2s | 226.2s | 69s          | 20       | 0       | 1       | 0         | 0                    |
| rn1-r70-6-elixir-2-r1-named-defect-a1 | incorrect | 281s   | 227.2s | 53.7s        | 20       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
kogen-review openai: input 1.89M, cached 0.18M, output 93.9k, reasoning 34.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.98M
named-defect openai: input 1.65M, cached 0.12M, output 72.2k, reasoning 20.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.72M
native usage by stage and provider:
stage build kogen-review openai (responses): input 0.81M, cached 0.14M, output 54.0k, reasoning 8.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.87M
stage build named-defect openai (responses): input 0.73M, cached 0.12M, output 45.2k, reasoning 6.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
stage review kogen-review openai (responses): input 1.08M, cached 38.8k, output 39.8k, reasoning 25.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.12M
stage review named-defect openai (responses): input 0.92M, cached 0, output 27.1k, reasoning 14.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.95M
native usage by attempt and provider:
attempt usage rn1-r70-1-go-r0-kogen-review-a1 openai (responses): input 0.39M, cached 33.7k, output 19.1k, reasoning 9.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage rn1-r70-1-go-r0-named-defect-a1 openai (responses): input 0.22M, cached 6.9k, output 10.4k, reasoning 2.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rn1-r70-1-go-r1-kogen-review-a1 openai (responses): input 0.36M, cached 33.5k, output 14.8k, reasoning 4.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage rn1-r70-1-go-r1-named-defect-a1 openai (responses): input 0.27M, cached 33.0k, output 11.9k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rn1-r70-4-elixir-2-r0-kogen-review-a1 openai (responses): input 0.20M, cached 25.0k, output 11.2k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rn1-r70-4-elixir-2-r0-named-defect-a1 openai (responses): input 0.24M, cached 14.1k, output 10.2k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rn1-r70-4-elixir-2-r1-kogen-review-a1 openai (responses): input 0.22M, cached 14.8k, output 12.5k, reasoning 5.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rn1-r70-4-elixir-2-r1-named-defect-a1 openai (responses): input 0.18M, cached 18.6k, output 8.9k, reasoning 3.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rn1-r70-4-go-r0-kogen-review-a1 openai (responses): input 0.21M, cached 7.4k, output 10.9k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage rn1-r70-4-go-r0-named-defect-a1 openai (responses): input 0.18M, cached 3.7k, output 7.7k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rn1-r70-4-go-r1-kogen-review-a1 openai (responses): input 0.17M, cached 3.7k, output 11.2k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage rn1-r70-4-go-r1-named-defect-a1 openai (responses): input 0.18M, cached 11.1k, output 9.7k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rn1-r70-6-elixir-2-r0-kogen-review-a1 openai (responses): input 0.14M, cached 24.7k, output 7.1k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage rn1-r70-6-elixir-2-r0-named-defect-a1 openai (responses): input 0.15M, cached 17.7k, output 6.4k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rn1-r70-6-elixir-2-r1-kogen-review-a1 openai (responses): input 0.20M, cached 37.2k, output 7.0k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rn1-r70-6-elixir-2-r1-named-defect-a1 openai (responses): input 0.22M, cached 17.9k, output 7.0k, reasoning 993, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt outcomes included: kogen-review: correct 6, incorrect 2, workflow failure 0, infrastructure 0, incomplete 0; named-defect: correct 6, incorrect 2, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5422.1s, model 4757.4s, tools/checks 664.6s, requests 296
builder settings: kogen-review openai gpt-6.1-sol reasoning.effort=medium; named-defect openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 4, infrastructure 0, incomplete 0
variant named-defect differs from kogen-review in:
  review.prompt: kogen -> [absolute path]
C02: exercised in 8 of 8 named-defect attempts
first position per task: r70-1-go kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-4-go kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 kogen-review 1, named-defect 1 (2 repetitions, 2 variants)
kogen-review: not the Kogen profile (differs in artifacts.gherkin, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
named-defect: not the Kogen profile (differs in artifacts.gherkin, review.prompt, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
kogen-review: build.helper_context = lab_helper (extension)
kogen-review: build.helper_prompt = lab:helper (extension)
kogen-review: build.subagents_output = 4096 (extension)
kogen-review: build.subagents_turns = 10 (extension)
kogen-review: plan.context = kogen_planner (extension)
kogen-review: plan.prompt = lab:plan (extension)
kogen-review: repair.context = packet,diff,check_results,review_findings (extension)
kogen-review: repair.roles = builder (extension)
kogen-review: review.timing = every_green (extension)
kogen-review: shape.critique_prompt = lab:critique (extension)
kogen-review: shape.critique_rounds = 1 (extension)
kogen-review: shape.helper_context = lab_helper (extension)
kogen-review: shape.helper_prompt = lab:helper (extension)
kogen-review: shape.subagents_output = 4096 (extension)
kogen-review: shape.subagents_turns = 10 (extension)
named-defect: build.helper_context = lab_helper (extension)
named-defect: build.helper_prompt = lab:helper (extension)
named-defect: build.subagents_output = 4096 (extension)
named-defect: build.subagents_turns = 10 (extension)
named-defect: plan.context = kogen_planner (extension)
named-defect: plan.prompt = lab:plan (extension)
named-defect: repair.context = packet,diff,check_results,review_findings (extension)
named-defect: repair.roles = builder (extension)
named-defect: review.timing = every_green (extension)
named-defect: shape.critique_prompt = lab:critique (extension)
named-defect: shape.critique_rounds = 1 (extension)
named-defect: shape.helper_context = lab_helper (extension)
named-defect: shape.helper_prompt = lab:helper (extension)
named-defect: shape.subagents_output = 4096 (extension)
named-defect: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
