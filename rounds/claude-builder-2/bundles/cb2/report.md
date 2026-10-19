incomplete: 11 of 12 cells scored
Question: claude-builder-2: on harder tasks, do Claude Haiku 5.5 and Claude Sonnet 5.5 builders match Kogen's default gpt-6.1-sol medium builder, and at what cost?
Hypothesis: exploratory: cr1's 7/7 for both Claude builders was at the ceiling; harder tasks may separate them
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (11 of 12 cells scored)
## CMP-1 Correctness
| variant      | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|--------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| sol-medium   | 3       | 0         | 1                | 0              | 0          | 75%          | 0 of 3        | 0           |
| haiku-build  | 2       | 0         | 1                | 1              | 0          | 66.7%        | 0 of 2        | 0           |
| sonnet-build | 1       | 0         | 3                | 0              | 0          | 25%          | 0 of 1        | 0           |
false success: 0 of 3 claims (sol-medium)
false success: 0 of 2 claims (haiku-build)
false success: 0 of 1 claims (sonnet-build)
shaping outcomes:
sol-medium: shaping ready 4, shaping failed 0; correct 3 of 4
haiku-build: shaping ready 4, shaping failed 0; correct 2 of 3
sonnet-build: shaping ready 4, shaping failed 0; correct 1 of 4
## Per-task outcomes
| task         | variant      | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|--------------|---------|-----------|------------------|----------------|------------|
| r70-1-go     | sol-medium   | 0       | 0         | 1                | 0              | 0          |
| r70-1-go     | haiku-build  | 1       | 0         | 0                | 0              | 0          |
| r70-1-go     | sonnet-build | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir | sol-medium   | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir | haiku-build  | 0       | 0         | 0                | 1              | 0          |
| r70-4-elixir | sonnet-build | 0       | 0         | 1                | 0              | 0          |
| r70-4-go     | sol-medium   | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | haiku-build  | 0       | 0         | 1                | 0              | 0          |
| r70-4-go     | sonnet-build | 0       | 0         | 1                | 0              | 0          |
| r70-6-elixir | sol-medium   | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | haiku-build  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | sonnet-build | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant      | stage      | wall     | model   | tools/checks | requests |
|--------------|------------|----------|---------|--------------|----------|
| sol-medium   | shape      | 0ms      | 0ms     | 0ms          | 0        |
| sol-medium   | plan       | 0ms      | 0ms     | 0ms          | 0        |
| sol-medium   | build      | 1047.8s  | 918.7s  | 129.1s       | 75       |
| sol-medium   | verify     | 33.8s    | 0ms     | 33.8s        | 0        |
| sol-medium   | review     | 730.1s   | 730.1s  | 0ms          | 42       |
| sol-medium   | commit     | 0ms      | 0ms     | 0ms          | 0        |
| sol-medium   | evaluate   | 0ms      | 0ms     | 0ms          | 0        |
| sol-medium   | assessment | 0ms      | 0ms     | 0ms          | 0        |
| haiku-build  | shape      | 0ms      | 0ms     | 0ms          | 0        |
| haiku-build  | plan       | 0ms      | 0ms     | 0ms          | 0        |
| haiku-build  | build      | 10305.5s | 578s    | 9727.5s      | 67       |
| haiku-build  | verify     | 30.3s    | 0ms     | 30.3s        | 0        |
| haiku-build  | review     | 832.1s   | 832.1s  | 0ms          | 49       |
| haiku-build  | commit     | 0ms      | 0ms     | 0ms          | 0        |
| haiku-build  | evaluate   | 0ms      | 0ms     | 0ms          | 0        |
| haiku-build  | assessment | 0ms      | 0ms     | 0ms          | 0        |
| sonnet-build | shape      | 0ms      | 0ms     | 0ms          | 0        |
| sonnet-build | plan       | 0ms      | 0ms     | 0ms          | 0        |
| sonnet-build | build      | 480.9s   | 325.7s  | 155.2s       | 59       |
| sonnet-build | verify     | 33s      | 0ms     | 33s          | 0        |
| sonnet-build | review     | 1489.5s  | 1489.5s | 0ms          | 82       |
| sonnet-build | commit     | 0ms      | 0ms     | 0ms          | 0        |
| sonnet-build | evaluate   | 0ms      | 0ms     | 0ms          | 0        |
| sonnet-build | assessment | 0ms      | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                             | outcome          | wall     | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------------|------------------|----------|--------|--------------|----------|---------|---------|-----------|----------------------|
| cb2-r70-1-go-r0-haiku-build-a1      | correct          | 10139.1s | 485.1s | 9654s        | 38       | 4       | 5       | 0         | 0                    |
| cb2-r70-1-go-r0-sol-medium-a1       | workflow failure | 1007.9s  | 917.2s | 90.7s        | 59       | 6       | 7       | 0         | 0                    |
| cb2-r70-1-go-r0-sonnet-build-a1     | workflow failure | 628.8s   | 593.1s | 35.8s        | 42       | 6       | 7       | 0         | 0                    |
| cb2-r70-4-elixir-r0-haiku-build-a1  | infrastructure   | 193.6s   | 165.5s | 28s          | 11       | 1       | 1       | 0         | 0                    |
| cb2-r70-4-elixir-r0-sol-medium-a1   | correct          | 358.5s   | 312.6s | 45.9s        | 26       | 3       | 3       | 0         | 0                    |
| cb2-r70-4-elixir-r0-sonnet-build-a1 | workflow failure | 637.9s   | 536.4s | 101.5s       | 43       | 6       | 7       | 0         | 0                    |
| cb2-r70-4-go-r0-haiku-build-a1      | workflow failure | 624.2s   | 555.9s | 68.3s        | 43       | 6       | 7       | 0         | 0                    |
| cb2-r70-4-go-r0-sol-medium-a1       | correct          | 314.1s   | 285.4s | 28.6s        | 20       | 1       | 2       | 0         | 0                    |
| cb2-r70-4-go-r0-sonnet-build-a1     | workflow failure | 439s     | 408.2s | 30.7s        | 31       | 6       | 6       | 0         | 0                    |
| cb2-r70-6-elixir-r0-haiku-build-a1  | correct          | 229.3s   | 203.6s | 25.6s        | 24       | 1       | 2       | 0         | 0                    |
| cb2-r70-6-elixir-r0-sol-medium-a1   | correct          | 145s     | 133.6s | 11.4s        | 12       | 0       | 1       | 0         | 0                    |
| cb2-r70-6-elixir-r0-sonnet-build-a1 | correct          | 317.3s   | 277.6s | 39.7s        | 25       | 3       | 4       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
haiku-build anthropic: input 142, cache_read 1.90M, cache_creation 0.21M, output 0.12M, thinking 74.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.21M
haiku-build openai: input 1.04M, cached 0, output 27.3k, reasoning 20.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
sol-medium openai: input 2.05M, cached 0.18M, output 58.6k, reasoning 28.0k, input_tokens_details.cache_write_tokens 0, total_tokens 2.11M
sonnet-build anthropic: input 126, cache_read 1.03M, cache_creation 98.7k, output 40.2k, thinking 6.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 98.7k
sonnet-build openai: input 1.57M, cached 35.2k, output 53.2k, reasoning 40.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.63M
native usage by stage and provider:
stage build haiku-build anthropic (messages): input 142, cache_read 1.90M, cache_creation 0.21M, output 0.12M, thinking 74.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.21M
stage build sol-medium openai (responses): input 1.08M, cached 0.13M, output 32.0k, reasoning 7.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.11M
stage build sonnet-build anthropic (messages): input 126, cache_read 1.03M, cache_creation 98.7k, output 40.2k, thinking 6.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 98.7k
stage review haiku-build openai (responses): input 1.04M, cached 0, output 27.3k, reasoning 20.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.07M
stage review sol-medium openai (responses): input 0.98M, cached 46.0k, output 26.6k, reasoning 21.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.00M
stage review sonnet-build openai (responses): input 1.57M, cached 35.2k, output 53.2k, reasoning 40.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.63M
native usage by attempt and provider:
attempt usage cb2-r70-1-go-r0-haiku-build-a1 anthropic (messages): input 46, cache_read 0.75M, cache_creation 90.8k, output 45.4k, thinking 23.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 90.8k
attempt usage cb2-r70-1-go-r0-haiku-build-a1 openai (responses): input 0.41M, cached 0, output 9.8k, reasoning 7.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.41M
attempt usage cb2-r70-1-go-r0-sol-medium-a1 openai (responses): input 1.29M, cached 0.11M, output 34.0k, reasoning 17.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.33M
attempt usage cb2-r70-1-go-r0-sonnet-build-a1 anthropic (messages): input 36, cache_read 0.31M, cache_creation 28.2k, output 14.5k, thinking 2.8k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 28.2k
attempt usage cb2-r70-1-go-r0-sonnet-build-a1 openai (responses): input 0.51M, cached 0, output 18.3k, reasoning 14.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
attempt usage cb2-r70-4-elixir-r0-haiku-build-a1 anthropic (messages): input 16, cache_read 0.14M, cache_creation 32.5k, output 19.6k, thinking 14.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 32.5k
attempt usage cb2-r70-4-elixir-r0-haiku-build-a1 openai (responses): input 65.3k, cached 0, output 1.4k, reasoning 917, input_tokens_details.cache_write_tokens 0, total_tokens 66.7k
attempt usage cb2-r70-4-elixir-r0-sol-medium-a1 openai (responses): input 0.35M, cached 35.1k, output 10.0k, reasoning 5.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage cb2-r70-4-elixir-r0-sonnet-build-a1 anthropic (messages): input 46, cache_read 0.41M, cache_creation 26.4k, output 10.0k, thinking 1.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 26.4k
attempt usage cb2-r70-4-elixir-r0-sonnet-build-a1 openai (responses): input 0.38M, cached 15.0k, output 16.6k, reasoning 12.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage cb2-r70-4-go-r0-haiku-build-a1 anthropic (messages): input 42, cache_read 0.55M, cache_creation 48.3k, output 32.9k, thinking 19.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 48.3k
attempt usage cb2-r70-4-go-r0-haiku-build-a1 openai (responses): input 0.45M, cached 0, output 13.7k, reasoning 10.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage cb2-r70-4-go-r0-sol-medium-a1 openai (responses): input 0.26M, cached 9.7k, output 9.8k, reasoning 4.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage cb2-r70-4-go-r0-sonnet-build-a1 anthropic (messages): input 20, cache_read 0.12M, cache_creation 20.4k, output 6.7k, thinking 712, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 20.4k
attempt usage cb2-r70-4-go-r0-sonnet-build-a1 openai (responses): input 0.39M, cached 0, output 11.2k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage cb2-r70-6-elixir-r0-haiku-build-a1 anthropic (messages): input 38, cache_read 0.46M, cache_creation 41.8k, output 25.9k, thinking 16.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 41.8k
attempt usage cb2-r70-6-elixir-r0-haiku-build-a1 openai (responses): input 0.12M, cached 0, output 2.3k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage cb2-r70-6-elixir-r0-sol-medium-a1 openai (responses): input 0.15M, cached 25.5k, output 4.7k, reasoning 698, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage cb2-r70-6-elixir-r0-sonnet-build-a1 anthropic (messages): input 24, cache_read 0.19M, cache_creation 23.8k, output 9.0k, thinking 1.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 23.8k
attempt usage cb2-r70-6-elixir-r0-sonnet-build-a1 openai (responses): input 0.29M, cached 20.2k, output 7.1k, reasoning 5.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt outcomes included: sol-medium: correct 3, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; haiku-build: correct 2, incorrect 0, workflow failure 1, infrastructure 1, incomplete 0; sonnet-build: correct 1, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 15034.5s, model 4874.2s, tools/checks 10160.3s, requests 374
builder settings: sol-medium openai gpt-6.1-sol reasoning.effort=medium
builder settings: haiku-build anthropic claude-haiku-5-5 output_config.effort=medium, thinking adaptive (not equivalent)
builder settings: sonnet-build anthropic claude-sonnet-5-5 output_config.effort=medium, thinking adaptive (not equivalent)
## CMP-3 Counts and exposure
planned 12, started 12, scored 11, incorrect 0, infrastructure 1, incomplete 0
variant haiku-build differs from sol-medium in:
  roles.builder: openai gpt-6.1-sol medium -> anthropic claude-haiku-5-5 medium
  roles.builder: openai gpt-6.1-sol medium -> anthropic claude-haiku-5-5 medium
variant sonnet-build differs from sol-medium in:
  roles.builder: openai gpt-6.1-sol medium -> anthropic claude-sonnet-5-5 medium
  roles.builder: openai gpt-6.1-sol medium -> anthropic claude-sonnet-5-5 medium
roles.builder.model: exercised in 4 of 4 haiku-build attempts
roles.builder.provider: exercised in 4 of 4 haiku-build attempts
roles.builder.model: exercised in 4 of 4 sonnet-build attempts
roles.builder.provider: exercised in 4 of 4 sonnet-build attempts
first position per task: r70-1-go sol-medium 0, haiku-build 1, sonnet-build 0 (1 repetitions, 3 variants)
first position per task: r70-4-elixir sol-medium 0, haiku-build 1, sonnet-build 0 (1 repetitions, 3 variants)
first position per task: r70-4-go sol-medium 0, haiku-build 0, sonnet-build 1 (1 repetitions, 3 variants)
first position per task: r70-6-elixir sol-medium 0, haiku-build 0, sonnet-build 1 (1 repetitions, 3 variants)
sol-medium: not the Kogen profile (differs in plan.enabled, stop.max_repairs, stop.max_tokens)
haiku-build: not the Kogen profile (differs in plan.enabled, roles.builder.model, roles.builder.provider, stop.max_repairs, stop.max_tokens)
sonnet-build: not the Kogen profile (differs in plan.enabled, roles.builder.model, roles.builder.provider, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
sol-medium: repair.context = packet,diff,check_results,review_findings (extension)
sol-medium: repair.roles = builder (extension)
sol-medium: shape.critique_prompt = lab:critique (extension)
sol-medium: shape.critique_rounds = 1 (extension)
haiku-build: repair.context = packet,diff,check_results,review_findings (extension)
haiku-build: repair.roles = builder (extension)
haiku-build: shape.critique_prompt = lab:critique (extension)
haiku-build: shape.critique_rounds = 1 (extension)
sonnet-build: repair.context = packet,diff,check_results,review_findings (extension)
sonnet-build: repair.roles = builder (extension)
sonnet-build: shape.critique_prompt = lab:critique (extension)
sonnet-build: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
