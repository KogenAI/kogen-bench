complete: 24/24 cells scored
Question: review-timing-1: with review only after the first green pass, does a Luna-low reviewer match the Sol-low every-green reviewer, and at what cost?
Hypothesis: luna-first is within one block of sol-every at no more than 80% of its input
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| sol-every  | 7       | 0         | 1                | 1              | 1          | 87.5%        | 0 of 7        | 0           |
| sol-first  | 6       | 2         | 0                | 0              | 1          | 75%          | 2 of 8        | 0           |
| luna-first | 3       | 5         | 0                | 0              | 2          | 37.5%        | 5 of 8        | 0           |
false success: 0 of 7 claims (sol-every)
false success: 2 of 8 claims (sol-first)
false success: 5 of 8 claims (luna-first)
shaping outcomes:
sol-every: shaping ready 10, shaping failed 0; correct 7 of 8
sol-first: shaping ready 9, shaping failed 0; correct 6 of 8
luna-first: shaping ready 10, shaping failed 0; correct 3 of 8
## Per-task outcomes
| task         | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|------------|---------|-----------|------------------|----------------|------------|
| r70-5-elixir | sol-every  | 1       | 0         | 1                | 0              | 1          |
| r70-5-elixir | sol-first  | 1       | 1         | 0                | 0              | 1          |
| r70-5-elixir | luna-first | 0       | 2         | 0                | 0              | 0          |
| r70-5-go     | sol-every  | 2       | 0         | 0                | 1              | 0          |
| r70-5-go     | sol-first  | 1       | 1         | 0                | 0              | 0          |
| r70-5-go     | luna-first | 0       | 2         | 0                | 0              | 0          |
| r70-7-elixir | sol-every  | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | sol-first  | 2       | 0         | 0                | 0              | 0          |
| r70-7-elixir | luna-first | 1       | 1         | 0                | 0              | 1          |
| r70-7-go     | sol-every  | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | sol-first  | 2       | 0         | 0                | 0              | 0          |
| r70-7-go     | luna-first | 2       | 0         | 0                | 0              | 1          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| sol-every  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-every  | plan       | 155s    | 155s    | 0ms          | 10       |
| sol-every  | build      | 2644.1s | 2497s   | 147.1s       | 208      |
| sol-every  | verify     | 37.3s   | 0ms     | 37.3s        | 0        |
| sol-every  | review     | 359.9s  | 359.9s  | 0ms          | 47       |
| sol-every  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-every  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-every  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| sol-first  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-first  | plan       | 122.3s  | 122.3s  | 0ms          | 9        |
| sol-first  | build      | 1987s   | 1865.3s | 121.7s       | 168      |
| sol-first  | verify     | 35.3s   | 0ms     | 35.3s        | 0        |
| sol-first  | review     | 168.1s  | 168.1s  | 0ms          | 19       |
| sol-first  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-first  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-first  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| luna-first | shape      | 0ms     | 0ms     | 0ms          | 0        |
| luna-first | plan       | 78.8s   | 78.8s   | 0ms          | 10       |
| luna-first | build      | 2048s   | 1940s   | 108s         | 161      |
| luna-first | verify     | 27.5s   | 0ms     | 27.5s        | 0        |
| luna-first | review     | 93.6s   | 93.6s   | 0ms          | 9        |
| luna-first | commit     | 0ms     | 0ms     | 0ms          | 0        |
| luna-first | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| luna-first | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rt1-r70-5-elixir-r0-luna-first-a1 | incorrect        | 347.7s | 332.8s | 14.9s        | 24       | 2       | 1       | 0         | 0                    |
| rt1-r70-5-elixir-r0-sol-every-a1  | incomplete       | 361s   | 338.4s | 22.6s        | 29       | 3       | 2       | 0         | 0                    |
| rt1-r70-5-elixir-r0-sol-every-a2  | correct          | 596.9s | 561.7s | 35.2s        | 56       | 6       | 5       | 0         | 0                    |
| rt1-r70-5-elixir-r0-sol-first-a1  | incorrect        | 539.7s | 507.2s | 32.6s        | 36       | 5       | 1       | 0         | 0                    |
| rt1-r70-5-elixir-r1-luna-first-a1 | incorrect        | 211.3s | 189.7s | 21.5s        | 14       | 1       | 1       | 0         | 0                    |
| rt1-r70-5-elixir-r1-sol-every-a1  | workflow failure | 721.6s | 688.3s | 33.3s        | 45       | 6       | 2       | 0         | 0                    |
| rt1-r70-5-elixir-r1-sol-first-a1  | incomplete       | 316.4s | 288.9s | 27.5s        | 33       | 6       | 0       | 0         | 0                    |
| rt1-r70-5-elixir-r1-sol-first-a2  | correct          | 323.3s | 301.3s | 22s          | 33       | 3       | 1       | 0         | 0                    |
| rt1-r70-5-go-r0-luna-first-a1     | incorrect        | 250.7s | 240.7s | 10s          | 16       | 1       | 1       | 0         | 0                    |
| rt1-r70-5-go-r0-sol-every-a1      | correct          | 247.5s | 230s   | 17.5s        | 20       | 1       | 2       | 0         | 0                    |
| rt1-r70-5-go-r0-sol-first-a1      | correct          | 220.7s | 204s   | 16.7s        | 18       | 1       | 1       | 0         | 0                    |
| rt1-r70-5-go-r1-luna-first-a1     | incorrect        | 162.4s | 139.5s | 23s          | 14       | 1       | 1       | 0         | 0                    |
| rt1-r70-5-go-r1-sol-every-a1      | infrastructure   | 295.5s | 266.8s | 28.7s        | 32       | 3       | 3       | 0         | 0                    |
| rt1-r70-5-go-r1-sol-every-a2      | correct          | 218.5s | 190.8s | 27.8s        | 23       | 1       | 2       | 0         | 0                    |
| rt1-r70-5-go-r1-sol-first-a1      | incorrect        | 164.8s | 140.1s | 24.7s        | 14       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-elixir-r0-luna-first-a1 | correct          | 386.8s | 363.4s | 23.4s        | 34       | 4       | 1       | 0         | 0                    |
| rt1-r70-7-elixir-r0-sol-every-a1  | correct          | 178s   | 164.9s | 13.2s        | 16       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-elixir-r0-sol-first-a1  | correct          | 239.1s | 226.5s | 12.6s        | 18       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-elixir-r1-luna-first-a1 | incomplete       | 242.3s | 219.6s | 22.7s        | 24       | 1       | 0       | 0         | 0                    |
| rt1-r70-7-elixir-r1-luna-first-a2 | incorrect        | 181.6s | 155.7s | 25.8s        | 14       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-elixir-r1-sol-every-a1  | correct          | 359.5s | 331.3s | 28.3s        | 24       | 1       | 2       | 0         | 0                    |
| rt1-r70-7-elixir-r1-sol-first-a1  | correct          | 261.7s | 229.5s | 32.1s        | 18       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-go-r0-luna-first-a1     | correct          | 229.6s | 203.5s | 26.1s        | 15       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-go-r0-sol-every-a1      | correct          | 185.6s | 162.8s | 22.8s        | 9        | 0       | 1       | 0         | 0                    |
| rt1-r70-7-go-r0-sol-first-a1      | correct          | 166.6s | 144.3s | 22.3s        | 11       | 0       | 1       | 0         | 0                    |
| rt1-r70-7-go-r1-luna-first-a1     | incomplete       | 165.8s | 158.9s | 6.9s         | 12       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-go-r1-luna-first-a2     | correct          | 119.2s | 108.6s | 10.6s        | 13       | 1       | 1       | 0         | 0                    |
| rt1-r70-7-go-r1-sol-every-a1      | correct          | 86.7s  | 77.1s  | 9.6s         | 11       | 0       | 1       | 0         | 0                    |
| rt1-r70-7-go-r1-sol-first-a1      | correct          | 127.2s | 113.9s | 13.3s        | 15       | 1       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
luna-first openai: input 1.92M, cached 0.52M, output 62.6k, reasoning 178, input_tokens_details.cache_write_tokens 0, total_tokens 1.98M
sol-every openai: input 4.13M, cached 1.27M, output 89.2k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 4.22M
sol-first openai: input 2.45M, cached 0.60M, output 60.0k, reasoning 411, input_tokens_details.cache_write_tokens 0, total_tokens 2.51M
native usage by stage and provider:
stage build luna-first openai (responses): input 1.74M, cached 0.51M, output 56.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.80M
stage build sol-every openai (responses): input 3.38M, cached 1.26M, output 81.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.46M
stage build sol-first openai (responses): input 2.13M, cached 0.58M, output 54.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.18M
stage plan luna-first openai (responses): input 43.0k, cached 8.2k, output 2.4k, reasoning 178, input_tokens_details.cache_write_tokens 0, total_tokens 45.4k
stage plan sol-every openai (responses): input 43.0k, cached 12.3k, output 2.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 45.1k
stage plan sol-first openai (responses): input 38.7k, cached 16.4k, output 1.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 40.5k
stage review luna-first openai (responses): input 0.14M, cached 0, output 3.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
stage review sol-every openai (responses): input 0.71M, cached 0, output 5.9k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
stage review sol-first openai (responses): input 0.28M, cached 0, output 3.3k, reasoning 411, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
native usage by attempt and provider:
attempt usage rt1-r70-5-elixir-r0-luna-first-a1 openai (responses): input 0.29M, cached 56.4k, output 10.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage rt1-r70-5-elixir-r0-sol-every-a1 openai (responses): input 0.43M, cached 75.9k, output 11.6k, reasoning 160, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage rt1-r70-5-elixir-r0-sol-every-a2 openai (responses): input 1.24M, cached 0.59M, output 19.6k, reasoning 403, input_tokens_details.cache_write_tokens 0, total_tokens 1.26M
attempt usage rt1-r70-5-elixir-r0-sol-first-a1 openai (responses): input 0.50M, cached 0.17M, output 13.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage rt1-r70-5-elixir-r1-luna-first-a1 openai (responses): input 0.18M, cached 17.8k, output 6.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rt1-r70-5-elixir-r1-sol-every-a1 openai (responses): input 0.92M, cached 0.38M, output 22.6k, reasoning 167, input_tokens_details.cache_write_tokens 0, total_tokens 0.94M
attempt usage rt1-r70-5-elixir-r1-sol-first-a1 openai (responses): input 0.46M, cached 0.14M, output 8.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage rt1-r70-5-elixir-r1-sol-first-a2 openai (responses): input 0.53M, cached 0.13M, output 10.6k, reasoning 142, input_tokens_details.cache_write_tokens 0, total_tokens 0.54M
attempt usage rt1-r70-5-go-r0-luna-first-a1 openai (responses): input 0.15M, cached 40.4k, output 6.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage rt1-r70-5-go-r0-sol-every-a1 openai (responses): input 0.20M, cached 37.0k, output 6.2k, reasoning 61, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rt1-r70-5-go-r0-sol-first-a1 openai (responses): input 0.16M, cached 43.4k, output 4.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rt1-r70-5-go-r1-luna-first-a1 openai (responses): input 0.12M, cached 18.9k, output 3.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage rt1-r70-5-go-r1-sol-every-a1 openai (responses): input 0.35M, cached 73.7k, output 5.4k, reasoning 245, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage rt1-r70-5-go-r1-sol-every-a2 openai (responses): input 0.27M, cached 28.9k, output 6.4k, reasoning 64, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rt1-r70-5-go-r1-sol-first-a1 openai (responses): input 0.12M, cached 35.5k, output 4.8k, reasoning 48, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage rt1-r70-7-elixir-r0-luna-first-a1 openai (responses): input 0.45M, cached 0.19M, output 9.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage rt1-r70-7-elixir-r0-sol-every-a1 openai (responses): input 0.20M, cached 23.2k, output 5.1k, reasoning 37, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
attempt usage rt1-r70-7-elixir-r0-sol-first-a1 openai (responses): input 0.18M, cached 36.7k, output 6.0k, reasoning 49, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage rt1-r70-7-elixir-r1-luna-first-a1 openai (responses): input 0.24M, cached 78.0k, output 6.3k, reasoning 178, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rt1-r70-7-elixir-r1-luna-first-a2 openai (responses): input 0.13M, cached 41.3k, output 6.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rt1-r70-7-elixir-r1-sol-every-a1 openai (responses): input 0.33M, cached 38.0k, output 7.3k, reasoning 59, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage rt1-r70-7-elixir-r1-sol-first-a1 openai (responses): input 0.26M, cached 15.5k, output 5.4k, reasoning 24, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rt1-r70-7-go-r0-luna-first-a1 openai (responses): input 0.14M, cached 16.1k, output 5.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rt1-r70-7-go-r0-sol-every-a1 openai (responses): input 86.1k, cached 11.6k, output 2.8k, reasoning 96, input_tokens_details.cache_write_tokens 0, total_tokens 88.9k
attempt usage rt1-r70-7-go-r0-sol-first-a1 openai (responses): input 98.0k, cached 0, output 2.5k, reasoning 47, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage rt1-r70-7-go-r1-luna-first-a1 openai (responses): input 0.11M, cached 18.3k, output 5.3k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rt1-r70-7-go-r1-luna-first-a2 openai (responses): input 0.11M, cached 36.2k, output 3.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rt1-r70-7-go-r1-sol-every-a1 openai (responses): input 0.10M, cached 4.6k, output 2.3k, reasoning 73, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage rt1-r70-7-go-r1-sol-first-a1 openai (responses): input 0.15M, cached 29.7k, output 3.1k, reasoning 101, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt outcomes included: sol-every: correct 7, incorrect 0, workflow failure 1, infrastructure 1, incomplete 1; sol-first: correct 6, incorrect 2, workflow failure 0, infrastructure 0, incomplete 1; luna-first: correct 3, incorrect 5, workflow failure 0, infrastructure 0, incomplete 2
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 7907.6s, model 7280.2s, tools/checks 627.5s, requests 641
builder settings: sol-every openai gpt-6-luna reasoning.effort=low
builder settings: sol-first openai gpt-6-luna reasoning.effort=low
builder settings: luna-first openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 29, scored 24, incorrect 7, infrastructure 1, incomplete 4
variant sol-first differs from sol-every in:
  review.timing: every_green -> first_green
variant luna-first differs from sol-every in:
  review.timing: every_green -> first_green
  roles.reviewer: openai gpt-6.1-sol low -> openai gpt-6-luna low
C06: exercised in 9 of 9 sol-first attempts
C06: exercised in 10 of 10 luna-first attempts
roles.reviewer.model: exercised in 10 of 10 luna-first attempts
first position per task: r70-5-elixir sol-every 0, sol-first 1, luna-first 1 (2 repetitions, 3 variants)
first position per task: r70-5-go sol-every 0, sol-first 1, luna-first 1 (2 repetitions, 3 variants)
first position per task: r70-7-elixir sol-every 1, sol-first 0, luna-first 1 (2 repetitions, 3 variants)
first position per task: r70-7-go sol-every 1, sol-first 1, luna-first 0 (2 repetitions, 3 variants)
sol-every: not the Kogen profile (differs in roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
sol-first: not the Kogen profile (differs in review.timing, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
luna-first: not the Kogen profile (differs in review.timing, roles.builder.effort, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.reviewer.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
sol-every: repair.context = packet,diff,check_results,review_findings (extension)
sol-every: repair.roles = builder (extension)
sol-every: shape.critique_prompt = lab:critique (extension)
sol-every: shape.critique_rounds = 1 (extension)
sol-first: repair.context = packet,diff,check_results,review_findings (extension)
sol-first: repair.roles = builder (extension)
sol-first: review.timing = first_green (extension)
sol-first: shape.critique_prompt = lab:critique (extension)
sol-first: shape.critique_rounds = 1 (extension)
luna-first: repair.context = packet,diff,check_results,review_findings (extension)
luna-first: repair.roles = builder (extension)
luna-first: review.timing = first_green (extension)
luna-first: shape.critique_prompt = lab:critique (extension)
luna-first: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
