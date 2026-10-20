complete: 20/20 cells scored
Question: claude-review-fix-1 run 2 (prose specification, no scenarios): when a weak builder reaches review with code that passes its checks but is wrong, does the reviewer-fixer catch and fix it, and does reviewer strength matter?
Hypothesis: exploratory: some green-but-wrong submissions reach review; a stronger reviewer-fixer rescues more
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| rev-sonnet | 8       | 2         | 0                | 0              | 0          | 80%          | 2 of 10       | 0           |
| rev-haiku  | 7       | 2         | 1                | 0              | 0          | 70%          | 2 of 9        | 0           |
false success: 2 of 10 claims (rev-sonnet)
false success: 2 of 9 claims (rev-haiku)
shaping outcomes:
rev-sonnet: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
rev-haiku: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|------------|---------|-----------|------------------|----------------|------------|
| artifact-go    | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| artifact-go    | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | rev-haiku  | 0       | 1         | 1                | 0              | 0          |
| r70-4-elixir-2 | rev-sonnet | 1       | 1         | 0                | 0              | 0          |
| r70-4-elixir-2 | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | rev-haiku  | 1       | 1         | 0                | 0              | 0          |
| r70-6-elixir-2 | rev-sonnet | 1       | 1         | 0                | 0              | 0          |
| r70-6-elixir-2 | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| rev-sonnet | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet | plan       | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet | build      | 1208.9s | 1117.3s | 91.6s        | 61       |
| rev-sonnet | verify     | 17.7s   | 0ms     | 17.7s        | 0        |
| rev-sonnet | review     | 137.9s  | 137.9s  | 0ms          | 22       |
| rev-sonnet | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet | assessment | 0ms     | 0ms     | 0ms          | 0        |
| rev-haiku  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-haiku  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| rev-haiku  | build      | 1217.2s | 1086s   | 131.3s       | 62       |
| rev-haiku  | verify     | 28.7s   | 0ms     | 28.7s        | 0        |
| rev-haiku  | review     | 606.5s  | 606.5s  | 0ms          | 41       |
| rev-haiku  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-haiku  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-haiku  | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| crf2-artifact-go-r0-rev-haiku-a1     | correct          | 52s    | 35.2s  | 16.8s        | 6        | 0       | 1       | 0         | 0                    |
| crf2-artifact-go-r0-rev-sonnet-a1    | correct          | 44.7s  | 28.1s  | 16.6s        | 6        | 0       | 1       | 0         | 0                    |
| crf2-artifact-go-r1-rev-haiku-a1     | correct          | 68s    | 54.8s  | 13.2s        | 8        | 0       | 1       | 0         | 0                    |
| crf2-artifact-go-r1-rev-sonnet-a1    | correct          | 35.5s  | 23.4s  | 12.1s        | 7        | 0       | 2       | 0         | 0                    |
| crf2-r70-1-go-r0-rev-haiku-a1        | incorrect        | 267.1s | 247.4s | 19.7s        | 12       | 0       | 1       | 0         | 0                    |
| crf2-r70-1-go-r0-rev-sonnet-a1       | correct          | 131.6s | 110.8s | 20.8s        | 8        | 0       | 1       | 0         | 0                    |
| crf2-r70-1-go-r1-rev-haiku-a1        | workflow failure | 144.7s | 118.6s | 26.1s        | 8        | 0       | 1       | 0         | 0                    |
| crf2-r70-1-go-r1-rev-sonnet-a1       | correct          | 90.5s  | 76.2s  | 14.3s        | 8        | 0       | 1       | 0         | 0                    |
| crf2-r70-4-elixir-2-r0-rev-haiku-a1  | correct          | 293.8s | 269.4s | 24.4s        | 14       | 0       | 1       | 0         | 0                    |
| crf2-r70-4-elixir-2-r0-rev-sonnet-a1 | incorrect        | 147s   | 128.4s | 18.6s        | 7        | 0       | 2       | 0         | 0                    |
| crf2-r70-4-elixir-2-r1-rev-haiku-a1  | correct          | 351.2s | 309.7s | 41.5s        | 19       | 0       | 1       | 0         | 0                    |
| crf2-r70-4-elixir-2-r1-rev-sonnet-a1 | correct          | 313.4s | 293.1s | 20.3s        | 11       | 0       | 2       | 0         | 0                    |
| crf2-r70-4-go-r0-rev-haiku-a1        | incorrect        | 120.8s | 99.5s  | 21.3s        | 9        | 0       | 1       | 0         | 0                    |
| crf2-r70-4-go-r0-rev-sonnet-a1       | correct          | 139.7s | 120.3s | 19.4s        | 11       | 0       | 2       | 0         | 0                    |
| crf2-r70-4-go-r1-rev-haiku-a1        | correct          | 178.3s | 158s   | 20.2s        | 11       | 0       | 1       | 0         | 0                    |
| crf2-r70-4-go-r1-rev-sonnet-a1       | correct          | 186.4s | 168s   | 18.4s        | 6        | 0       | 2       | 0         | 0                    |
| crf2-r70-6-elixir-2-r0-rev-haiku-a1  | correct          | 176.2s | 166.3s | 9.8s         | 6        | 0       | 1       | 0         | 0                    |
| crf2-r70-6-elixir-2-r0-rev-sonnet-a1 | incorrect        | 145.3s | 133.5s | 11.7s        | 11       | 0       | 1       | 0         | 0                    |
| crf2-r70-6-elixir-2-r1-rev-haiku-a1  | correct          | 251.5s | 233.5s | 18s          | 10       | 0       | 1       | 0         | 0                    |
| crf2-r70-6-elixir-2-r1-rev-sonnet-a1 | correct          | 185.5s | 173.2s | 12.3s        | 8        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
rev-haiku anthropic: input 246, cache_read 1.51M, cache_creation 0.41M, output 0.20M, thinking 0.12M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.41M
rev-sonnet anthropic: input 206, cache_read 1.06M, cache_creation 0.33M, output 0.13M, thinking 66.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.33M
native usage by stage and provider:
stage build rev-haiku anthropic (messages): input 144, cache_read 0.90M, cache_creation 0.18M, output 0.14M, thinking 72.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.18M
stage build rev-sonnet anthropic (messages): input 142, cache_read 0.83M, cache_creation 0.15M, output 0.12M, thinking 61.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.15M
stage review rev-haiku anthropic (messages): input 102, cache_read 0.61M, cache_creation 0.22M, output 62.4k, thinking 47.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.22M
stage review rev-sonnet anthropic (messages): input 64, cache_read 0.22M, cache_creation 0.18M, output 7.5k, thinking 4.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.18M
native usage by attempt and provider:
attempt usage crf2-artifact-go-r0-rev-haiku-a1 anthropic (messages): input 16, cache_read 52.4k, cache_creation 21.6k, output 5.6k, thinking 1.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 21.6k
attempt usage crf2-artifact-go-r0-rev-sonnet-a1 anthropic (messages): input 16, cache_read 40.5k, cache_creation 26.8k, output 4.8k, thinking 909, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 26.8k
attempt usage crf2-artifact-go-r1-rev-haiku-a1 anthropic (messages): input 20, cache_read 82.2k, cache_creation 23.6k, output 6.7k, thinking 1.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 23.6k
attempt usage crf2-artifact-go-r1-rev-sonnet-a1 anthropic (messages): input 18, cache_read 62.5k, cache_creation 19.0k, output 4.1k, thinking 575, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 19.0k
attempt usage crf2-r70-1-go-r0-rev-haiku-a1 anthropic (messages): input 28, cache_read 0.19M, cache_creation 37.9k, output 16.6k, thinking 7.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 37.9k
attempt usage crf2-r70-1-go-r0-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.11M, cache_creation 36.5k, output 12.2k, thinking 4.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 36.5k
attempt usage crf2-r70-1-go-r1-rev-haiku-a1 anthropic (messages): input 20, cache_read 0.10M, cache_creation 45.6k, output 17.3k, thinking 9.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 45.6k
attempt usage crf2-r70-1-go-r1-rev-sonnet-a1 anthropic (messages): input 20, cache_read 97.8k, cache_creation 33.5k, output 13.2k, thinking 5.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 33.5k
attempt usage crf2-r70-4-elixir-2-r0-rev-haiku-a1 anthropic (messages): input 32, cache_read 0.23M, cache_creation 52.2k, output 27.3k, thinking 16.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 52.2k
attempt usage crf2-r70-4-elixir-2-r0-rev-sonnet-a1 anthropic (messages): input 18, cache_read 74.5k, cache_creation 29.5k, output 11.4k, thinking 5.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 29.5k
attempt usage crf2-r70-4-elixir-2-r1-rev-haiku-a1 anthropic (messages): input 42, cache_read 0.34M, cache_creation 41.6k, output 23.8k, thinking 14.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 41.6k
attempt usage crf2-r70-4-elixir-2-r1-rev-sonnet-a1 anthropic (messages): input 26, cache_read 0.17M, cache_creation 36.7k, output 17.0k, thinking 9.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 36.7k
attempt usage crf2-r70-4-go-r0-rev-haiku-a1 anthropic (messages): input 22, cache_read 0.11M, cache_creation 40.3k, output 15.1k, thinking 8.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 40.3k
attempt usage crf2-r70-4-go-r0-rev-sonnet-a1 anthropic (messages): input 26, cache_read 0.14M, cache_creation 34.6k, output 12.4k, thinking 5.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 34.6k
attempt usage crf2-r70-4-go-r1-rev-haiku-a1 anthropic (messages): input 26, cache_read 0.15M, cache_creation 35.2k, output 19.2k, thinking 11.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 35.2k
attempt usage crf2-r70-4-go-r1-rev-sonnet-a1 anthropic (messages): input 16, cache_read 58.8k, cache_creation 32.0k, output 12.8k, thinking 7.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.0k
attempt usage crf2-r70-6-elixir-2-r0-rev-haiku-a1 anthropic (messages): input 16, cache_read 80.3k, cache_creation 52.7k, output 34.3k, thinking 25.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 52.7k
attempt usage crf2-r70-6-elixir-2-r0-rev-sonnet-a1 anthropic (messages): input 26, cache_read 0.16M, cache_creation 37.9k, output 20.1k, thinking 12.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 37.9k
attempt usage crf2-r70-6-elixir-2-r1-rev-haiku-a1 anthropic (messages): input 24, cache_read 0.18M, cache_creation 56.3k, output 34.9k, thinking 24.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 56.3k
attempt usage crf2-r70-6-elixir-2-r1-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.14M, cache_creation 45.5k, output 23.3k, thinking 14.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 45.5k
attempt outcomes included: rev-sonnet: correct 8, incorrect 2, workflow failure 0, infrastructure 0, incomplete 0; rev-haiku: correct 7, incorrect 2, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 3323s, model 2947.6s, tools/checks 375.4s, requests 186
builder settings: rev-sonnet anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive; rev-haiku anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive
## CMP-3 Counts and exposure
planned 20, started 20, scored 20, incorrect 4, infrastructure 0, incomplete 0
variant rev-haiku differs from rev-sonnet in:
  roles.reviewer: anthropic claude-sonnet-5-5 medium -> anthropic claude-haiku-5-5 medium
roles.reviewer.model: exercised in 10 of 10 rev-haiku attempts
first position per task: artifact-go rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-1-go rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-4-go rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
rev-sonnet: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.builder.model, roles.builder.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
rev-haiku: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.builder.model, roles.builder.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
rev-sonnet: build.helper_context = lab_helper (extension)
rev-sonnet: build.helper_prompt = lab:helper (extension)
rev-sonnet: build.subagents_output = 4096 (extension)
rev-sonnet: build.subagents_turns = 10 (extension)
rev-sonnet: plan.context = kogen_planner (extension)
rev-sonnet: plan.prompt = lab:plan (extension)
rev-sonnet: repair.context = packet,diff,check_results,review_findings (extension)
rev-sonnet: repair.roles = builder (extension)
rev-sonnet: review.timing = every_green (extension)
rev-sonnet: shape.critique_prompt = lab:critique (extension)
rev-sonnet: shape.critique_rounds = 1 (extension)
rev-sonnet: shape.helper_context = lab_helper (extension)
rev-sonnet: shape.helper_prompt = lab:helper (extension)
rev-sonnet: shape.subagents_output = 4096 (extension)
rev-sonnet: shape.subagents_turns = 10 (extension)
rev-haiku: build.helper_context = lab_helper (extension)
rev-haiku: build.helper_prompt = lab:helper (extension)
rev-haiku: build.subagents_output = 4096 (extension)
rev-haiku: build.subagents_turns = 10 (extension)
rev-haiku: plan.context = kogen_planner (extension)
rev-haiku: plan.prompt = lab:plan (extension)
rev-haiku: repair.context = packet,diff,check_results,review_findings (extension)
rev-haiku: repair.roles = builder (extension)
rev-haiku: review.timing = every_green (extension)
rev-haiku: shape.critique_prompt = lab:critique (extension)
rev-haiku: shape.critique_rounds = 1 (extension)
rev-haiku: shape.helper_context = lab_helper (extension)
rev-haiku: shape.helper_prompt = lab:helper (extension)
rev-haiku: shape.subagents_output = 4096 (extension)
rev-haiku: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
