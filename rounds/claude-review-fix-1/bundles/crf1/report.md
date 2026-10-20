complete: 16/16 cells scored
Question: claude-review-fix-1: when a weak builder reaches review with code that passes its checks but is wrong, does the reviewer-fixer catch and fix it, and does reviewer strength matter?
Hypothesis: exploratory: some green-but-wrong submissions reach review; a stronger reviewer-fixer rescues more
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| rev-sonnet | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| rev-haiku  | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (rev-sonnet)
false success: 0 of 8 claims (rev-haiku)
shaping outcomes:
rev-sonnet: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
rev-haiku: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | rev-sonnet | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | rev-haiku  | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model  | tools/checks | requests |
|------------|------------|---------|--------|--------------|----------|
| rev-sonnet | shape      | 0ms     | 0ms    | 0ms          | 0        |
| rev-sonnet | plan       | 0ms     | 0ms    | 0ms          | 0        |
| rev-sonnet | build      | 984.3s  | 891.5s | 92.8s        | 44       |
| rev-sonnet | verify     | 11.4s   | 0ms    | 11.4s        | 0        |
| rev-sonnet | review     | 124.1s  | 124.1s | 0ms          | 13       |
| rev-sonnet | commit     | 0ms     | 0ms    | 0ms          | 0        |
| rev-sonnet | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| rev-sonnet | assessment | 0ms     | 0ms    | 0ms          | 0        |
| rev-haiku  | shape      | 0ms     | 0ms    | 0ms          | 0        |
| rev-haiku  | plan       | 0ms     | 0ms    | 0ms          | 0        |
| rev-haiku  | build      | 1004.5s | 848.5s | 156.1s       | 46       |
| rev-haiku  | verify     | 17.7s   | 0ms    | 17.7s        | 0        |
| rev-haiku  | review     | 328.1s  | 328.1s | 0ms          | 39       |
| rev-haiku  | commit     | 0ms     | 0ms    | 0ms          | 0        |
| rev-haiku  | evaluate   | 0ms     | 0ms    | 0ms          | 0        |
| rev-haiku  | assessment | 0ms     | 0ms    | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| crf1-r70-1-go-r0-rev-haiku-a1        | correct | 90.3s  | 70.3s  | 20.1s        | 5        | 0       | 1       | 0         | 0                    |
| crf1-r70-1-go-r0-rev-sonnet-a1       | correct | 101.8s | 84.5s  | 17.3s        | 4        | 0       | 1       | 0         | 0                    |
| crf1-r70-1-go-r1-rev-haiku-a1        | correct | 159s   | 133.9s | 25.1s        | 7        | 0       | 1       | 0         | 0                    |
| crf1-r70-1-go-r1-rev-sonnet-a1       | correct | 155s   | 129.7s | 25.3s        | 8        | 0       | 2       | 0         | 0                    |
| crf1-r70-4-elixir-2-r0-rev-haiku-a1  | correct | 116.3s | 102s   | 14.4s        | 7        | 0       | 1       | 0         | 0                    |
| crf1-r70-4-elixir-2-r0-rev-sonnet-a1 | correct | 103.9s | 89.4s  | 14.5s        | 8        | 0       | 2       | 0         | 0                    |
| crf1-r70-4-elixir-2-r1-rev-haiku-a1  | correct | 256.2s | 206.5s | 49.7s        | 14       | 0       | 2       | 0         | 0                    |
| crf1-r70-4-elixir-2-r1-rev-sonnet-a1 | correct | 193.7s | 176.1s | 17.6s        | 7        | 0       | 2       | 0         | 0                    |
| crf1-r70-4-go-r0-rev-haiku-a1        | correct | 210.8s | 191.7s | 19.1s        | 6        | 0       | 1       | 0         | 0                    |
| crf1-r70-4-go-r0-rev-sonnet-a1       | correct | 130.3s | 117.4s | 12.9s        | 8        | 0       | 1       | 0         | 0                    |
| crf1-r70-4-go-r1-rev-haiku-a1        | correct | 207s   | 172.2s | 34.8s        | 19       | 0       | 2       | 0         | 0                    |
| crf1-r70-4-go-r1-rev-sonnet-a1       | correct | 133.7s | 114.3s | 19.5s        | 6        | 0       | 2       | 0         | 0                    |
| crf1-r70-6-elixir-2-r0-rev-haiku-a1  | correct | 236.9s | 203.8s | 33.1s        | 14       | 0       | 1       | 0         | 0                    |
| crf1-r70-6-elixir-2-r0-rev-sonnet-a1 | correct | 189.2s | 165.5s | 23.7s        | 9        | 0       | 2       | 0         | 0                    |
| crf1-r70-6-elixir-2-r1-rev-haiku-a1  | correct | 117.2s | 96.2s  | 21s          | 13       | 0       | 2       | 0         | 0                    |
| crf1-r70-6-elixir-2-r1-rev-sonnet-a1 | correct | 156.1s | 138.7s | 17.3s        | 7        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
rev-haiku anthropic: input 202, cache_read 1.49M, cache_creation 0.35M, output 0.14M, thinking 89.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.35M
rev-sonnet anthropic: input 146, cache_read 0.83M, cache_creation 0.31M, output 0.11M, thinking 70.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.31M
native usage by stage and provider:
stage build rev-haiku anthropic (messages): input 108, cache_read 0.72M, cache_creation 0.14M, output 92.8k, thinking 58.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.14M
stage build rev-sonnet anthropic (messages): input 104, cache_read 0.73M, cache_creation 0.15M, output 99.4k, thinking 65.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.15M
stage review rev-haiku anthropic (messages): input 94, cache_read 0.77M, cache_creation 0.21M, output 43.0k, thinking 31.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.21M
stage review rev-sonnet anthropic (messages): input 42, cache_read 99.6k, cache_creation 0.17M, output 5.7k, thinking 4.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.17M
native usage by attempt and provider:
attempt usage crf1-r70-1-go-r0-rev-haiku-a1 anthropic (messages): input 14, cache_read 51.4k, cache_creation 38.2k, output 14.9k, thinking 9.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 38.2k
attempt usage crf1-r70-1-go-r0-rev-sonnet-a1 anthropic (messages): input 12, cache_read 31.3k, cache_creation 36.3k, output 11.7k, thinking 7.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 36.3k
attempt usage crf1-r70-1-go-r1-rev-haiku-a1 anthropic (messages): input 18, cache_read 98.6k, cache_creation 37.1k, output 13.2k, thinking 8.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 37.1k
attempt usage crf1-r70-1-go-r1-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.11M, cache_creation 45.6k, output 14.2k, thinking 8.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 45.6k
attempt usage crf1-r70-4-elixir-2-r0-rev-haiku-a1 anthropic (messages): input 18, cache_read 83.9k, cache_creation 37.2k, output 14.8k, thinking 11.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 37.2k
attempt usage crf1-r70-4-elixir-2-r0-rev-sonnet-a1 anthropic (messages): input 20, cache_read 98.1k, cache_creation 43.4k, output 10.7k, thinking 7.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 43.4k
attempt usage crf1-r70-4-elixir-2-r1-rev-haiku-a1 anthropic (messages): input 32, cache_read 0.25M, cache_creation 42.3k, output 17.4k, thinking 10.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 42.3k
attempt usage crf1-r70-4-elixir-2-r1-rev-sonnet-a1 anthropic (messages): input 18, cache_read 86.9k, cache_creation 32.3k, output 8.9k, thinking 6.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.3k
attempt usage crf1-r70-4-go-r0-rev-haiku-a1 anthropic (messages): input 16, cache_read 60.0k, cache_creation 42.8k, output 12.0k, thinking 9.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 42.8k
attempt usage crf1-r70-4-go-r0-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.11M, cache_creation 32.4k, output 10.4k, thinking 6.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.4k
attempt usage crf1-r70-4-go-r1-rev-haiku-a1 anthropic (messages): input 42, cache_read 0.40M, cache_creation 44.7k, output 19.6k, thinking 11.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 44.7k
attempt usage crf1-r70-4-go-r1-rev-sonnet-a1 anthropic (messages): input 16, cache_read 66.4k, cache_creation 29.0k, output 7.3k, thinking 4.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 29.0k
attempt usage crf1-r70-6-elixir-2-r0-rev-haiku-a1 anthropic (messages): input 32, cache_read 0.33M, cache_creation 66.9k, output 25.8k, thinking 17.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 66.9k
attempt usage crf1-r70-6-elixir-2-r0-rev-sonnet-a1 anthropic (messages): input 22, cache_read 0.19M, cache_creation 48.0k, output 19.9k, thinking 14.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 48.0k
attempt usage crf1-r70-6-elixir-2-r1-rev-haiku-a1 anthropic (messages): input 30, cache_read 0.22M, cache_creation 44.2k, output 18.0k, thinking 11.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 44.2k
attempt usage crf1-r70-6-elixir-2-r1-rev-sonnet-a1 anthropic (messages): input 18, cache_read 0.13M, cache_creation 46.6k, output 21.9k, thinking 15.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 46.6k
attempt outcomes included: rev-sonnet: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; rev-haiku: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 2557.5s, model 2192.2s, tools/checks 365.3s, requests 142
builder settings: rev-sonnet anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive; rev-haiku anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant rev-haiku differs from rev-sonnet in:
  roles.reviewer: anthropic claude-sonnet-5-5 medium -> anthropic claude-haiku-5-5 medium
roles.reviewer.model: exercised in 8 of 8 rev-haiku attempts
first position per task: r70-1-go rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-4-go rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 rev-sonnet 1, rev-haiku 1 (2 repetitions, 2 variants)
rev-sonnet: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.builder.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
rev-haiku: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.builder.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
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
