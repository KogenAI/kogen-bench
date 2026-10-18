complete: 24/24 cells scored
Question: baseline-variance-1: how often does the screen-kogen-2 baseline succeed over three repetitions, and does B07 succeed more often in paired blocks?
Hypothesis: the screen-kogen-2 baseline failures were partly chance; B07 is not clearly ahead
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| kogen           | 11      | 0         | 1                | 0              | 0          | 91.7%        | 0 of 11       | 0           |
| b07-output-full | 11      | 0         | 1                | 0              | 0          | 91.7%        | 0 of 11       | 0           |
false success: 0 of 11 claims (kogen)
false success: 0 of 11 claims (b07-output-full)
shaping outcomes:
kogen: shaping ready 12, shaping failed 0; correct 11 of 12
b07-output-full: shaping ready 12, shaping failed 0; correct 11 of 12
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | kogen           | 3       | 0         | 0                | 0              | 0          |
| r70-5-elixir | b07-output-full | 2       | 0         | 1                | 0              | 0          |
| r70-5-go     | kogen           | 3       | 0         | 0                | 0              | 0          |
| r70-5-go     | b07-output-full | 3       | 0         | 0                | 0              | 0          |
| r70-7-elixir | kogen           | 2       | 0         | 1                | 0              | 0          |
| r70-7-elixir | b07-output-full | 3       | 0         | 0                | 0              | 0          |
| r70-7-go     | kogen           | 3       | 0         | 0                | 0              | 0          |
| r70-7-go     | b07-output-full | 3       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| kogen           | shape      | 0ms     | 0ms     | 0ms          | 0        |
| kogen           | plan       | 147.5s  | 147.5s  | 0ms          | 12       |
| kogen           | build      | 3432.7s | 3218s   | 214.6s       | 258      |
| kogen           | verify     | 57.5s   | 0ms     | 57.5s        | 0        |
| kogen           | review     | 680.8s  | 680.8s  | 0ms          | 78       |
| kogen           | commit     | 0ms     | 0ms     | 0ms          | 0        |
| kogen           | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| kogen           | assessment | 0ms     | 0ms     | 0ms          | 0        |
| b07-output-full | shape      | 0ms     | 0ms     | 0ms          | 0        |
| b07-output-full | plan       | 126.8s  | 126.8s  | 0ms          | 12       |
| b07-output-full | build      | 3463.2s | 3270.1s | 193.1s       | 265      |
| b07-output-full | verify     | 64.5s   | 0ms     | 64.5s        | 0        |
| b07-output-full | review     | 581.2s  | 581.2s  | 0ms          | 66       |
| b07-output-full | commit     | 0ms     | 0ms     | 0ms          | 0        |
| b07-output-full | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| b07-output-full | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| bv1-r70-5-elixir-r0-b07-output-full-a1 | correct          | 417.6s | 376.4s | 41.3s        | 36       | 5       | 3       | 0         | 0                    |
| bv1-r70-5-elixir-r0-kogen-a1           | correct          | 557.6s | 538.4s | 19.3s        | 31       | 2       | 3       | 0         | 0                    |
| bv1-r70-5-elixir-r1-b07-output-full-a1 | correct          | 605.5s | 576.8s | 28.7s        | 40       | 5       | 4       | 0         | 0                    |
| bv1-r70-5-elixir-r1-kogen-a1           | correct          | 415.8s | 386.9s | 29s          | 41       | 3       | 3       | 0         | 0                    |
| bv1-r70-5-elixir-r2-b07-output-full-a1 | workflow failure | 563.3s | 527.6s | 35.7s        | 38       | 6       | 0       | 0         | 0                    |
| bv1-r70-5-elixir-r2-kogen-a1           | correct          | 495.1s | 454.5s | 40.6s        | 42       | 4       | 4       | 0         | 0                    |
| bv1-r70-5-go-r0-b07-output-full-a1     | correct          | 358.8s | 331.2s | 27.6s        | 39       | 4       | 4       | 0         | 0                    |
| bv1-r70-5-go-r0-kogen-a1               | correct          | 289.4s | 259.6s | 29.8s        | 25       | 2       | 3       | 0         | 0                    |
| bv1-r70-5-go-r1-b07-output-full-a1     | correct          | 207.2s | 191.4s | 15.8s        | 19       | 1       | 2       | 0         | 0                    |
| bv1-r70-5-go-r1-kogen-a1               | correct          | 247.5s | 233.2s | 14.3s        | 23       | 2       | 3       | 0         | 0                    |
| bv1-r70-5-go-r2-b07-output-full-a1     | correct          | 163.4s | 145.1s | 18.3s        | 17       | 1       | 2       | 0         | 0                    |
| bv1-r70-5-go-r2-kogen-a1               | correct          | 351.3s | 332s   | 19.3s        | 29       | 2       | 3       | 0         | 0                    |
| bv1-r70-7-elixir-r0-b07-output-full-a1 | correct          | 310.8s | 291.6s | 19.1s        | 21       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-elixir-r0-kogen-a1           | workflow failure | 464.8s | 419.7s | 45.1s        | 35       | 5       | 0       | 0         | 0                    |
| bv1-r70-7-elixir-r1-b07-output-full-a1 | correct          | 720s   | 655.5s | 64.5s        | 48       | 4       | 4       | 0         | 0                    |
| bv1-r70-7-elixir-r1-kogen-a1           | correct          | 635.5s | 590.8s | 44.7s        | 41       | 3       | 3       | 0         | 0                    |
| bv1-r70-7-elixir-r2-b07-output-full-a1 | correct          | 348.9s | 326.5s | 22.4s        | 25       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-elixir-r2-kogen-a1           | correct          | 414.5s | 362.6s | 51.9s        | 34       | 3       | 2       | 0         | 0                    |
| bv1-r70-7-go-r0-b07-output-full-a1     | correct          | 236.7s | 218.2s | 18.5s        | 24       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-go-r0-kogen-a1               | correct          | 208.6s | 195.2s | 13.3s        | 18       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-go-r1-b07-output-full-a1     | correct          | 229.8s | 217.4s | 12.4s        | 21       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-go-r1-kogen-a1               | correct          | 127.3s | 117.1s | 10.2s        | 10       | 0       | 1       | 0         | 0                    |
| bv1-r70-7-go-r2-b07-output-full-a1     | correct          | 132s   | 120.3s | 11.7s        | 15       | 1       | 2       | 0         | 0                    |
| bv1-r70-7-go-r2-kogen-a1               | correct          | 170.3s | 156.3s | 14s          | 19       | 1       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
b07-output-full openai: input 4.44M, cached 1.19M, output 0.10M, reasoning 2.5k, input_tokens_details.cache_write_tokens 0, total_tokens 4.54M
kogen openai: input 4.70M, cached 1.17M, output 99.9k, reasoning 2.5k, input_tokens_details.cache_write_tokens 0, total_tokens 4.80M
native usage by stage and provider:
stage build b07-output-full openai (responses): input 3.37M, cached 1.18M, output 90.9k, reasoning 504, input_tokens_details.cache_write_tokens 0, total_tokens 3.47M
stage build kogen openai (responses): input 3.46M, cached 1.16M, output 88.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.54M
stage plan b07-output-full openai (responses): input 51.6k, cached 4.1k, output 2.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 54.2k
stage plan kogen openai (responses): input 51.6k, cached 8.2k, output 2.9k, reasoning 117, input_tokens_details.cache_write_tokens 0, total_tokens 54.4k
stage review b07-output-full openai (responses): input 1.02M, cached 0, output 8.0k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.02M
stage review kogen openai (responses): input 1.19M, cached 0, output 8.9k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
native usage by attempt and provider:
attempt usage bv1-r70-5-elixir-r0-b07-output-full-a1 openai (responses): input 0.50M, cached 0.14M, output 9.2k, reasoning 184, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage bv1-r70-5-elixir-r0-kogen-a1 openai (responses): input 0.45M, cached 0.13M, output 13.0k, reasoning 295, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage bv1-r70-5-elixir-r1-b07-output-full-a1 openai (responses): input 0.67M, cached 0.24M, output 15.9k, reasoning 329, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
attempt usage bv1-r70-5-elixir-r1-kogen-a1 openai (responses): input 0.59M, cached 0.15M, output 8.7k, reasoning 382, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
attempt usage bv1-r70-5-elixir-r2-b07-output-full-a1 openai (responses): input 0.59M, cached 0.26M, output 17.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.60M
attempt usage bv1-r70-5-elixir-r2-kogen-a1 openai (responses): input 0.57M, cached 0.19M, output 11.5k, reasoning 443, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage bv1-r70-5-go-r0-b07-output-full-a1 openai (responses): input 0.44M, cached 0.11M, output 5.3k, reasoning 297, input_tokens_details.cache_write_tokens 0, total_tokens 0.45M
attempt usage bv1-r70-5-go-r0-kogen-a1 openai (responses): input 0.34M, cached 73.5k, output 7.9k, reasoning 304, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage bv1-r70-5-go-r1-b07-output-full-a1 openai (responses): input 0.19M, cached 4.6k, output 4.7k, reasoning 43, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage bv1-r70-5-go-r1-kogen-a1 openai (responses): input 0.25M, cached 11.1k, output 5.7k, reasoning 207, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage bv1-r70-5-go-r2-b07-output-full-a1 openai (responses): input 0.17M, cached 4.9k, output 5.0k, reasoning 56, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage bv1-r70-5-go-r2-kogen-a1 openai (responses): input 0.35M, cached 70.0k, output 7.4k, reasoning 84, input_tokens_details.cache_write_tokens 0, total_tokens 0.35M
attempt usage bv1-r70-7-elixir-r0-b07-output-full-a1 openai (responses): input 0.22M, cached 34.9k, output 6.3k, reasoning 118, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage bv1-r70-7-elixir-r0-kogen-a1 openai (responses): input 0.44M, cached 0.18M, output 9.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.45M
attempt usage bv1-r70-7-elixir-r1-b07-output-full-a1 openai (responses): input 0.75M, cached 0.26M, output 16.2k, reasoning 840, input_tokens_details.cache_write_tokens 0, total_tokens 0.77M
attempt usage bv1-r70-7-elixir-r1-kogen-a1 openai (responses): input 0.61M, cached 0.18M, output 13.8k, reasoning 239, input_tokens_details.cache_write_tokens 0, total_tokens 0.62M
attempt usage bv1-r70-7-elixir-r2-b07-output-full-a1 openai (responses): input 0.28M, cached 55.8k, output 6.8k, reasoning 132, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage bv1-r70-7-elixir-r2-kogen-a1 openai (responses): input 0.64M, cached 0.14M, output 10.3k, reasoning 162, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
attempt usage bv1-r70-7-go-r0-b07-output-full-a1 openai (responses): input 0.25M, cached 31.4k, output 6.1k, reasoning 114, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage bv1-r70-7-go-r0-kogen-a1 openai (responses): input 0.19M, cached 14.6k, output 4.5k, reasoning 153, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage bv1-r70-7-go-r1-b07-output-full-a1 openai (responses): input 0.23M, cached 9.6k, output 5.2k, reasoning 204, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage bv1-r70-7-go-r1-kogen-a1 openai (responses): input 89.7k, cached 4.6k, output 2.6k, reasoning 56, input_tokens_details.cache_write_tokens 0, total_tokens 92.3k
attempt usage bv1-r70-7-go-r2-b07-output-full-a1 openai (responses): input 0.15M, cached 32.5k, output 3.8k, reasoning 218, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage bv1-r70-7-go-r2-kogen-a1 openai (responses): input 0.20M, cached 17.2k, output 5.3k, reasoning 175, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt outcomes included: kogen: correct 11, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; b07-output-full: correct 11, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 8671.8s, model 8024.4s, tools/checks 647.4s, requests 691
builder settings: kogen openai gpt-6-luna reasoning.effort=low
builder settings: b07-output-full openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 24, scored 24, incorrect 0, infrastructure 0, incomplete 0
variant b07-output-full differs from kogen in:
  build.output: kogen_16k -> full
B07: exercised in 12 of 12 b07-output-full attempts
first position per task: r70-5-elixir kogen 2, b07-output-full 1 (3 repetitions, 2 variants)
first position per task: r70-5-go kogen 2, b07-output-full 1 (3 repetitions, 2 variants)
first position per task: r70-7-elixir kogen 1, b07-output-full 2 (3 repetitions, 2 variants)
first position per task: r70-7-go kogen 1, b07-output-full 2 (3 repetitions, 2 variants)
kogen: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
b07-output-full: not the Kogen profile (differs in build.output, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
kogen: repair.context = packet,diff,check_results,review_findings (extension)
kogen: repair.roles = builder (extension)
kogen: shape.critique_prompt = lab:critique (extension)
kogen: shape.critique_rounds = 1 (extension)
b07-output-full: build.output = full (extension)
b07-output-full: repair.context = packet,diff,check_results,review_findings (extension)
b07-output-full: repair.roles = builder (extension)
b07-output-full: shape.critique_prompt = lab:critique (extension)
b07-output-full: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
