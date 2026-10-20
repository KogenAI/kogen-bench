complete: 24/24 cells scored
Question: claude-review-fix-1 run 3: on tasks not used before for this question, does Kogen's Sol-high reviewer-fixer rescue green-but-wrong code from a weak builder, and how often does wrong code still ship?
Hypothesis: replication of crf2: a strong reviewer-fixer rescues some green-but-wrong trees and approves some unchanged
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant      | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|--------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| rev-sol-high | 12      | 0         | 0                | 0              | 0          | 100%         | 0 of 12       | 0           |
| rev-sonnet   | 12      | 0         | 0                | 0              | 0          | 100%         | 0 of 12       | 0           |
false success: 0 of 12 claims (rev-sol-high)
false success: 0 of 12 claims (rev-sonnet)
shaping outcomes:
rev-sol-high: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
rev-sonnet: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task         | variant      | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|--------------|---------|-----------|------------------|----------------|------------|
| env-ex       | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| env-ex       | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
| r70-5-elixir | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| r70-5-elixir | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
| r70-5-go     | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| r70-5-go     | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
| sched-go     | rev-sol-high | 2       | 0         | 0                | 0              | 0          |
| sched-go     | rev-sonnet   | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant      | stage      | wall    | model   | tools/checks | requests |
|--------------|------------|---------|---------|--------------|----------|
| rev-sol-high | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high | plan       | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high | build      | 1232.9s | 1089s   | 143.9s       | 69       |
| rev-sol-high | verify     | 52.1s   | 0ms     | 52.1s        | 0        |
| rev-sol-high | review     | 2286.3s | 2286.3s | 0ms          | 92       |
| rev-sol-high | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-sol-high | assessment | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet   | build      | 1279.4s | 1157.9s | 121.5s       | 82       |
| rev-sonnet   | verify     | 21.6s   | 0ms     | 21.6s        | 0        |
| rev-sonnet   | review     | 138s    | 138s    | 0ms          | 23       |
| rev-sonnet   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| rev-sonnet   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                              | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|--------------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| crf3-env-ex-r0-rev-sol-high-a1       | correct | 570.4s | 548.7s | 21.7s        | 17       | 0       | 1       | 0         | 0                    |
| crf3-env-ex-r0-rev-sonnet-a1         | correct | 195.4s | 181.9s | 13.5s        | 12       | 0       | 2       | 0         | 0                    |
| crf3-env-ex-r1-rev-sol-high-a1       | correct | 474.1s | 452.5s | 21.5s        | 17       | 0       | 1       | 0         | 0                    |
| crf3-env-ex-r1-rev-sonnet-a1         | correct | 170.8s | 150s   | 20.7s        | 15       | 0       | 2       | 0         | 0                    |
| crf3-r70-5-elixir-r0-rev-sol-high-a1 | correct | 290.2s | 257.8s | 32.4s        | 14       | 0       | 1       | 0         | 0                    |
| crf3-r70-5-elixir-r0-rev-sonnet-a1   | correct | 209.7s | 192.9s | 16.8s        | 7        | 0       | 1       | 0         | 0                    |
| crf3-r70-5-elixir-r1-rev-sol-high-a1 | correct | 314.1s | 289.4s | 24.8s        | 15       | 0       | 1       | 0         | 0                    |
| crf3-r70-5-elixir-r1-rev-sonnet-a1   | correct | 118.8s | 104.8s | 13.9s        | 8        | 0       | 2       | 0         | 0                    |
| crf3-r70-5-go-r0-rev-sol-high-a1     | correct | 240.5s | 223.8s | 16.8s        | 9        | 0       | 1       | 0         | 0                    |
| crf3-r70-5-go-r0-rev-sonnet-a1       | correct | 86.3s  | 68.3s  | 18s          | 5        | 0       | 1       | 0         | 0                    |
| crf3-r70-5-go-r1-rev-sol-high-a1     | correct | 242.3s | 230.9s | 11.4s        | 12       | 0       | 1       | 0         | 0                    |
| crf3-r70-5-go-r1-rev-sonnet-a1       | correct | 79.4s  | 63.7s  | 15.8s        | 6        | 0       | 2       | 0         | 0                    |
| crf3-r70-7-elixir-r0-rev-sol-high-a1 | correct | 229s   | 208.3s | 20.7s        | 16       | 0       | 1       | 0         | 0                    |
| crf3-r70-7-elixir-r0-rev-sonnet-a1   | correct | 77.5s  | 66.5s  | 11s          | 10       | 0       | 2       | 0         | 0                    |
| crf3-r70-7-elixir-r1-rev-sol-high-a1 | correct | 325.4s | 299.2s | 26.3s        | 18       | 0       | 1       | 0         | 0                    |
| crf3-r70-7-elixir-r1-rev-sonnet-a1   | correct | 92.1s  | 75.6s  | 16.5s        | 6        | 0       | 1       | 0         | 0                    |
| crf3-r70-7-go-r0-rev-sol-high-a1     | correct | 232s   | 208.1s | 23.9s        | 10       | 0       | 1       | 0         | 0                    |
| crf3-r70-7-go-r0-rev-sonnet-a1       | correct | 178.2s | 155.6s | 22.6s        | 9        | 0       | 2       | 0         | 0                    |
| crf3-r70-7-go-r1-rev-sol-high-a1     | correct | 177.4s | 159.8s | 17.6s        | 10       | 0       | 1       | 0         | 0                    |
| crf3-r70-7-go-r1-rev-sonnet-a1       | correct | 84.1s  | 67.6s  | 16.5s        | 12       | 0       | 2       | 0         | 0                    |
| crf3-sched-go-r0-rev-sol-high-a1     | correct | 337.5s | 314s   | 23.6s        | 12       | 0       | 1       | 0         | 0                    |
| crf3-sched-go-r0-rev-sonnet-a1       | correct | 132s   | 108.7s | 23.3s        | 8        | 0       | 2       | 0         | 0                    |
| crf3-sched-go-r1-rev-sol-high-a1     | correct | 206.9s | 182.9s | 24s          | 11       | 0       | 1       | 0         | 0                    |
| crf3-sched-go-r1-rev-sonnet-a1       | correct | 83s    | 60.3s  | 22.6s        | 7        | 0       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
rev-sol-high anthropic: input 162, cache_read 1.14M, cache_creation 0.23M, output 0.19M, thinking 0.11M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.23M
rev-sol-high openai: input 1.55M, cached 92.5k, output 53.3k, reasoning 14.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.60M
rev-sonnet anthropic: input 258, cache_read 1.66M, cache_creation 0.50M, output 0.20M, thinking 0.12M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.50M
native usage by stage and provider:
stage build rev-sol-high anthropic (messages): input 162, cache_read 1.14M, cache_creation 0.23M, output 0.19M, thinking 0.11M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.23M
stage build rev-sonnet anthropic (messages): input 188, cache_read 1.44M, cache_creation 0.26M, output 0.19M, thinking 0.11M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.26M
stage review rev-sol-high openai (responses): input 1.55M, cached 92.5k, output 53.3k, reasoning 14.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.60M
stage review rev-sonnet anthropic (messages): input 70, cache_read 0.22M, cache_creation 0.25M, output 11.4k, thinking 9.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.25M
native usage by attempt and provider:
attempt usage crf3-env-ex-r0-rev-sol-high-a1 anthropic (messages): input 14, cache_read 0.13M, cache_creation 28.7k, output 26.1k, thinking 17.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 28.7k
attempt usage crf3-env-ex-r0-rev-sol-high-a1 openai (responses): input 0.22M, cached 20.6k, output 5.7k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage crf3-env-ex-r0-rev-sonnet-a1 anthropic (messages): input 28, cache_read 0.27M, cache_creation 60.5k, output 30.5k, thinking 22.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 60.5k
attempt usage crf3-env-ex-r1-rev-sol-high-a1 anthropic (messages): input 20, cache_read 0.24M, cache_creation 32.9k, output 28.6k, thinking 18.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.9k
attempt usage crf3-env-ex-r1-rev-sol-high-a1 openai (responses): input 0.13M, cached 17.7k, output 4.6k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage crf3-env-ex-r1-rev-sonnet-a1 anthropic (messages): input 34, cache_read 0.40M, cache_creation 62.6k, output 28.7k, thinking 18.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 62.6k
attempt usage crf3-r70-5-elixir-r0-rev-sol-high-a1 anthropic (messages): input 14, cache_read 0.11M, cache_creation 21.1k, output 18.8k, thinking 13.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 21.1k
attempt usage crf3-r70-5-elixir-r0-rev-sol-high-a1 openai (responses): input 0.11M, cached 25.7k, output 3.4k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage crf3-r70-5-elixir-r0-rev-sonnet-a1 anthropic (messages): input 18, cache_read 83.6k, cache_creation 45.9k, output 20.2k, thinking 14.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 45.9k
attempt usage crf3-r70-5-elixir-r1-rev-sol-high-a1 anthropic (messages): input 14, cache_read 0.13M, cache_creation 27.8k, output 25.7k, thinking 18.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 27.8k
attempt usage crf3-r70-5-elixir-r1-rev-sol-high-a1 openai (responses): input 0.16M, cached 0, output 5.6k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage crf3-r70-5-elixir-r1-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.13M, cache_creation 38.5k, output 20.7k, thinking 15.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 38.5k
attempt usage crf3-r70-5-go-r0-rev-sol-high-a1 anthropic (messages): input 10, cache_read 48.7k, cache_creation 16.1k, output 14.1k, thinking 7.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 16.1k
attempt usage crf3-r70-5-go-r0-rev-sol-high-a1 openai (responses): input 84.5k, cached 0, output 2.4k, reasoning 618, input_tokens_details.cache_write_tokens 0, total_tokens 86.9k
attempt usage crf3-r70-5-go-r0-rev-sonnet-a1 anthropic (messages): input 14, cache_read 47.1k, cache_creation 33.4k, output 14.4k, thinking 8.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 33.4k
attempt usage crf3-r70-5-go-r1-rev-sol-high-a1 anthropic (messages): input 10, cache_read 40.4k, cache_creation 23.6k, output 14.3k, thinking 8.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 23.6k
attempt usage crf3-r70-5-go-r1-rev-sol-high-a1 openai (responses): input 0.13M, cached 14.1k, output 4.2k, reasoning 1.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage crf3-r70-5-go-r1-rev-sonnet-a1 anthropic (messages): input 16, cache_read 63.3k, cache_creation 32.2k, output 12.7k, thinking 7.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.2k
attempt usage crf3-r70-7-elixir-r0-rev-sol-high-a1 anthropic (messages): input 16, cache_read 91.9k, cache_creation 21.3k, output 12.2k, thinking 6.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 21.3k
attempt usage crf3-r70-7-elixir-r0-rev-sol-high-a1 openai (responses): input 0.14M, cached 0, output 4.8k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage crf3-r70-7-elixir-r0-rev-sonnet-a1 anthropic (messages): input 24, cache_read 0.14M, cache_creation 35.0k, output 12.6k, thinking 5.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 35.0k
attempt usage crf3-r70-7-elixir-r1-rev-sol-high-a1 anthropic (messages): input 16, cache_read 0.11M, cache_creation 14.4k, output 12.6k, thinking 6.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 14.4k
attempt usage crf3-r70-7-elixir-r1-rev-sol-high-a1 openai (responses): input 0.17M, cached 0, output 4.6k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage crf3-r70-7-elixir-r1-rev-sonnet-a1 anthropic (messages): input 16, cache_read 64.6k, cache_creation 35.1k, output 13.1k, thinking 6.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 35.1k
attempt usage crf3-r70-7-go-r0-rev-sol-high-a1 anthropic (messages): input 10, cache_read 41.2k, cache_creation 9.5k, output 8.0k, thinking 2.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 9.5k
attempt usage crf3-r70-7-go-r0-rev-sol-high-a1 openai (responses): input 96.4k, cached 0, output 4.7k, reasoning 714, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage crf3-r70-7-go-r0-rev-sonnet-a1 anthropic (messages): input 22, cache_read 0.10M, cache_creation 43.1k, output 10.0k, thinking 2.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 43.1k
attempt usage crf3-r70-7-go-r1-rev-sol-high-a1 anthropic (messages): input 10, cache_read 40.3k, cache_creation 9.2k, output 8.2k, thinking 2.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 9.2k
attempt usage crf3-r70-7-go-r1-rev-sol-high-a1 openai (responses): input 97.4k, cached 0, output 4.8k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage crf3-r70-7-go-r1-rev-sonnet-a1 anthropic (messages): input 28, cache_read 0.18M, cache_creation 36.4k, output 13.0k, thinking 5.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 36.4k
attempt usage crf3-sched-go-r0-rev-sol-high-a1 anthropic (messages): input 16, cache_read 0.10M, cache_creation 14.9k, output 13.7k, thinking 5.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 14.9k
attempt usage crf3-sched-go-r0-rev-sol-high-a1 openai (responses): input 85.1k, cached 0, output 3.5k, reasoning 601, input_tokens_details.cache_write_tokens 0, total_tokens 88.6k
attempt usage crf3-sched-go-r0-rev-sonnet-a1 anthropic (messages): input 20, cache_read 0.10M, cache_creation 46.3k, output 13.8k, thinking 5.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 46.3k
attempt usage crf3-sched-go-r1-rev-sol-high-a1 anthropic (messages): input 12, cache_read 62.3k, cache_creation 13.7k, output 12.3k, thinking 5.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 13.7k
attempt usage crf3-sched-go-r1-rev-sol-high-a1 openai (responses): input 0.10M, cached 14.5k, output 5.2k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage crf3-sched-go-r1-rev-sonnet-a1 anthropic (messages): input 18, cache_read 81.0k, cache_creation 34.9k, output 12.3k, thinking 5.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 34.9k
attempt outcomes included: rev-sol-high: correct 12, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; rev-sonnet: correct 12, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 5147.2s, model 4671.2s, tools/checks 476s, requests 266
builder settings: rev-sol-high anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive; rev-sonnet anthropic claude-haiku-5-5 output_config.effort=low, thinking adaptive
## CMP-3 Counts and exposure
planned 24, started 24, scored 24, incorrect 0, infrastructure 0, incomplete 0
variant rev-sonnet differs from rev-sol-high in:
  roles.reviewer: openai gpt-6.1-sol high -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol high -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol high -> anthropic claude-sonnet-5-5 medium
roles.reviewer.effort: exercised in 12 of 12 rev-sonnet attempts
roles.reviewer.model: exercised in 12 of 12 rev-sonnet attempts
roles.reviewer.provider: exercised in 12 of 12 rev-sonnet attempts
first position per task: env-ex rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
first position per task: r70-5-elixir rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
first position per task: r70-5-go rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
first position per task: r70-7-elixir rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
first position per task: r70-7-go rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
first position per task: sched-go rev-sol-high 1, rev-sonnet 1 (2 repetitions, 2 variants)
rev-sol-high: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.builder.model, roles.builder.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
rev-sonnet: not the Kogen profile (differs in artifacts.gherkin, roles.builder.effort, roles.builder.model, roles.builder.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
rev-sol-high: build.helper_context = lab_helper (extension)
rev-sol-high: build.helper_prompt = lab:helper (extension)
rev-sol-high: build.subagents_output = 4096 (extension)
rev-sol-high: build.subagents_turns = 10 (extension)
rev-sol-high: plan.context = kogen_planner (extension)
rev-sol-high: plan.prompt = lab:plan (extension)
rev-sol-high: repair.context = packet,diff,check_results,review_findings (extension)
rev-sol-high: repair.roles = builder (extension)
rev-sol-high: review.timing = every_green (extension)
rev-sol-high: shape.critique_prompt = lab:critique (extension)
rev-sol-high: shape.critique_rounds = 1 (extension)
rev-sol-high: shape.helper_context = lab_helper (extension)
rev-sol-high: shape.helper_prompt = lab:helper (extension)
rev-sol-high: shape.subagents_output = 4096 (extension)
rev-sol-high: shape.subagents_turns = 10 (extension)
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
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
