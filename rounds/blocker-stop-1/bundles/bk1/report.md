complete: 12/12 cells scored
Question: blocker-stop-1: with a weak builder and Kogen b2c9876b's review-and-fix, does the builder's blocker stop end hopeless attempts earlier and cheaper than a six-repair limit, without giving up on attempts that would have succeeded?
Hypothesis: exploratory: the blocker stop ends failing attempts sooner; it may also give up on some solvable ones
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| blocker | 6       | 0         | 0                | 0              | 0          | 100%         | 0 of 6        | 0           |
| cap6    | 6       | 0         | 0                | 0              | 2          | 100%         | 0 of 6        | 0           |
false success: 0 of 6 claims (blocker)
false success: 0 of 6 claims (cap6)
shaping outcomes:
blocker: shaping ready 6, shaping failed 0; correct 6 of 6
cap6: shaping ready 8, shaping failed 0; correct 6 of 6
## Per-task outcomes
| task           | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|---------|---------|-----------|------------------|----------------|------------|
| env-ex         | blocker | 1       | 0         | 0                | 0              | 0          |
| env-ex         | cap6    | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | blocker | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | cap6    | 1       | 0         | 0                | 0              | 1          |
| r70-4-elixir-2 | blocker | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | cap6    | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | blocker | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | cap6    | 1       | 0         | 0                | 0              | 1          |
| r70-5-elixir   | blocker | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir   | cap6    | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | blocker | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | cap6    | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| blocker | shape      | 0ms     | 0ms     | 0ms          | 0        |
| blocker | plan       | 0ms     | 0ms     | 0ms          | 0        |
| blocker | build      | 1039.2s | 888.6s  | 150.6s       | 64       |
| blocker | verify     | 52.9s   | 0ms     | 52.9s        | 0        |
| blocker | review     | 2191.1s | 2191.1s | 0ms          | 75       |
| blocker | commit     | 0ms     | 0ms     | 0ms          | 0        |
| blocker | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| blocker | assessment | 0ms     | 0ms     | 0ms          | 0        |
| cap6    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| cap6    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| cap6    | build      | 1502.8s | 1369.6s | 133.2s       | 116      |
| cap6    | verify     | 60.5s   | 0ms     | 60.5s        | 0        |
| cap6    | review     | 2172.2s | 2172.2s | 0ms          | 81       |
| cap6    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| cap6    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| cap6    | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                          | outcome    | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------|------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| bk1-env-ex-r0-blocker-a1         | correct    | 410.3s | 381.2s | 29.1s        | 29       | 4       | 1       | 0         | 0                    |
| bk1-env-ex-r0-cap6-a1            | correct    | 450.5s | 412.9s | 37.6s        | 31       | 2       | 1       | 0         | 0                    |
| bk1-r70-1-go-r0-blocker-a1       | correct    | 832.3s | 805s   | 27.3s        | 22       | 1       | 1       | 0         | 0                    |
| bk1-r70-1-go-r0-cap6-a1          | incomplete | 538.5s | 528.4s | 10.1s        | 13       | 1       | 0       | 0         | 0                    |
| bk1-r70-1-go-r0-cap6-a2          | correct    | 584.1s | 558.2s | 25.9s        | 27       | 3       | 1       | 0         | 0                    |
| bk1-r70-4-elixir-2-r0-blocker-a1 | correct    | 658.4s | 553.9s | 104.5s       | 26       | 1       | 1       | 0         | 0                    |
| bk1-r70-4-elixir-2-r0-cap6-a1    | correct    | 506.7s | 454.8s | 51.9s        | 30       | 1       | 1       | 0         | 0                    |
| bk1-r70-4-go-r0-blocker-a1       | correct    | 723.5s | 706.7s | 16.8s        | 18       | 0       | 1       | 0         | 0                    |
| bk1-r70-4-go-r0-cap6-a1          | incomplete | 479s   | 469s   | 10s          | 15       | 0       | 0       | 0         | 0                    |
| bk1-r70-4-go-r0-cap6-a2          | correct    | 305s   | 290.3s | 14.7s        | 22       | 1       | 1       | 0         | 0                    |
| bk1-r70-5-elixir-r0-blocker-a1   | correct    | 267s   | 237.2s | 29.8s        | 14       | 0       | 1       | 0         | 0                    |
| bk1-r70-5-elixir-r0-cap6-a1      | correct    | 475.1s | 431.5s | 43.6s        | 31       | 4       | 1       | 0         | 0                    |
| bk1-r70-6-elixir-2-r0-blocker-a1 | correct    | 428.2s | 395.7s | 32.5s        | 30       | 2       | 1       | 0         | 0                    |
| bk1-r70-6-elixir-2-r0-cap6-a1    | correct    | 448.3s | 396.6s | 51.7s        | 28       | 3       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
blocker openai: input 2.42M, cached 0.30M, output 99.0k, reasoning 37.0k, input_tokens_details.cache_write_tokens 0, total_tokens 2.52M
cap6 openai: input 3.04M, cached 0.35M, output 0.13M, reasoning 36.5k, input_tokens_details.cache_write_tokens 0, total_tokens 3.17M
native usage by stage and provider:
stage build blocker openai (responses): input 0.75M, cached 0.20M, output 26.6k, reasoning 225, input_tokens_details.cache_write_tokens 0, total_tokens 0.78M
stage build cap6 openai (responses): input 1.52M, cached 0.31M, output 45.6k, reasoning 733, input_tokens_details.cache_write_tokens 0, total_tokens 1.56M
stage review blocker openai (responses): input 1.67M, cached 96.4k, output 72.3k, reasoning 36.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.74M
stage review cap6 openai (responses): input 1.53M, cached 38.8k, output 82.0k, reasoning 35.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.61M
native usage by attempt and provider:
attempt usage bk1-env-ex-r0-blocker-a1 openai (responses): input 0.49M, cached 76.0k, output 14.9k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
attempt usage bk1-env-ex-r0-cap6-a1 openai (responses): input 0.50M, cached 90.9k, output 16.1k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bk1-r70-1-go-r0-blocker-a1 openai (responses): input 0.51M, cached 48.5k, output 23.9k, reasoning 12.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
attempt usage bk1-r70-1-go-r0-cap6-a1 openai (responses): input 0.15M, cached 8.1k, output 13.9k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage bk1-r70-1-go-r0-cap6-a2 openai (responses): input 0.47M, cached 52.5k, output 24.0k, reasoning 9.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage bk1-r70-4-elixir-2-r0-blocker-a1 openai (responses): input 0.48M, cached 49.3k, output 24.0k, reasoning 12.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
attempt usage bk1-r70-4-elixir-2-r0-cap6-a1 openai (responses): input 0.41M, cached 61.3k, output 18.5k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.43M
attempt usage bk1-r70-4-go-r0-blocker-a1 openai (responses): input 0.24M, cached 32.0k, output 10.9k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage bk1-r70-4-go-r0-cap6-a1 openai (responses): input 0.17M, cached 0, output 10.9k, reasoning 2.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage bk1-r70-4-go-r0-cap6-a2 openai (responses): input 0.30M, cached 12.8k, output 11.1k, reasoning 4.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage bk1-r70-5-elixir-r0-blocker-a1 openai (responses): input 0.22M, cached 11.8k, output 9.8k, reasoning 3.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage bk1-r70-5-elixir-r0-cap6-a1 openai (responses): input 0.49M, cached 44.2k, output 17.0k, reasoning 2.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bk1-r70-6-elixir-2-r0-blocker-a1 openai (responses): input 0.49M, cached 79.1k, output 15.4k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bk1-r70-6-elixir-2-r0-cap6-a1 openai (responses): input 0.56M, cached 76.4k, output 16.0k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt outcomes included: blocker: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; cap6: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 2
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 7106.9s, model 6621.5s, tools/checks 485.4s, requests 336
builder settings: blocker openai gpt-6-luna reasoning.effort=low
builder settings: cap6 openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 12, started 14, scored 12, incorrect 0, infrastructure 0, incomplete 2
variant cap6 differs from blocker in:
  build.tools: shell,read_file,finish,report_blocker -> shell,read_file,finish
  stop.max_repairs: <absent> -> 6
B03: exercised in 8 of 8 cap6 attempts
stop.max_repairs: not exercised
first position per task: env-ex blocker 0, cap6 1 (1 repetitions, 2 variants)
first position per task: r70-1-go blocker 1, cap6 0 (1 repetitions, 2 variants)
first position per task: r70-4-elixir-2 blocker 0, cap6 1 (1 repetitions, 2 variants)
first position per task: r70-4-go blocker 1, cap6 0 (1 repetitions, 2 variants)
first position per task: r70-5-elixir blocker 0, cap6 1 (1 repetitions, 2 variants)
first position per task: r70-6-elixir-2 blocker 1, cap6 0 (1 repetitions, 2 variants)
blocker: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_wall_seconds)
cap6: not the Kogen profile (differs in build.tools, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_wall_seconds = 3600, stop.max_command_seconds = 900, stop.max_repairs = 6; no variant matches the Kogen profile configuration
blocker: build.helper_context = lab_helper (extension)
blocker: build.helper_prompt = lab:helper (extension)
blocker: build.subagents_output = 4096 (extension)
blocker: build.subagents_turns = 10 (extension)
blocker: plan.context = kogen_planner (extension)
blocker: plan.prompt = lab:plan (extension)
blocker: repair.context = packet,diff,check_results,review_findings (extension)
blocker: repair.roles = builder (extension)
blocker: review.timing = every_green (extension)
blocker: shape.critique_prompt = lab:critique (extension)
blocker: shape.critique_rounds = 1 (extension)
blocker: shape.helper_context = lab_helper (extension)
blocker: shape.helper_prompt = lab:helper (extension)
blocker: shape.subagents_output = 4096 (extension)
blocker: shape.subagents_turns = 10 (extension)
cap6: build.helper_context = lab_helper (extension)
cap6: build.helper_prompt = lab:helper (extension)
cap6: build.subagents_output = 4096 (extension)
cap6: build.subagents_turns = 10 (extension)
cap6: plan.context = kogen_planner (extension)
cap6: plan.prompt = lab:plan (extension)
cap6: repair.context = packet,diff,check_results,review_findings (extension)
cap6: repair.roles = builder (extension)
cap6: review.timing = every_green (extension)
cap6: shape.critique_prompt = lab:critique (extension)
cap6: shape.critique_rounds = 1 (extension)
cap6: shape.helper_context = lab_helper (extension)
cap6: shape.helper_prompt = lab:helper (extension)
cap6: shape.subagents_output = 4096 (extension)
cap6: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
