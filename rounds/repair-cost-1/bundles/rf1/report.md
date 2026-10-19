complete: 28/28 cells scored
Question: repair-cost-1: with a Sol-high reviewer, which repair setup reaches equal correctness at the lowest total cost with a median of at most 2 repairs?
Hypothesis: exploratory: a Sol-high fixer or a stronger builder cuts repairs; review-limit counterfactuals compared with Sol-low pooled results
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant   | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| low       | 5       | 0         | 2                | 0              | 0          | 71.4%        | 0 of 5        | 0           |
| fixer     | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
| luna-high | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
| sol-low   | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
false success: 0 of 5 claims (low)
false success: 0 of 7 claims (fixer)
false success: 0 of 7 claims (luna-high)
false success: 0 of 7 claims (sol-low)
shaping outcomes:
low: shaping ready 7, shaping failed 0; correct 5 of 7
fixer: shaping ready 7, shaping failed 0; correct 7 of 7
luna-high: shaping ready 7, shaping failed 0; correct 7 of 7
sol-low: shaping ready 7, shaping failed 0; correct 7 of 7
## Per-task outcomes
| task         | variant   | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------|---------|-----------|------------------|----------------|------------|
| env-ex       | low       | 0       | 0         | 1                | 0              | 0          |
| env-ex       | fixer     | 1       | 0         | 0                | 0              | 0          |
| env-ex       | luna-high | 1       | 0         | 0                | 0              | 0          |
| env-ex       | sol-low   | 1       | 0         | 0                | 0              | 0          |
| env-go       | low       | 1       | 0         | 0                | 0              | 0          |
| env-go       | fixer     | 1       | 0         | 0                | 0              | 0          |
| env-go       | luna-high | 1       | 0         | 0                | 0              | 0          |
| env-go       | sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | low       | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | fixer     | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | luna-high | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | low       | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | fixer     | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | luna-high | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | low       | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | fixer     | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | luna-high | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | sol-low   | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | low       | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | fixer     | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | luna-high | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | sol-low   | 1       | 0         | 0                | 0              | 0          |
| sched-go     | low       | 1       | 0         | 0                | 0              | 0          |
| sched-go     | fixer     | 1       | 0         | 0                | 0              | 0          |
| sched-go     | luna-high | 1       | 0         | 0                | 0              | 0          |
| sched-go     | sol-low   | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant   | stage      | wall    | model   | tools/checks | requests |
|-----------|------------|---------|---------|--------------|----------|
| low       | shape      | 0ms     | 0ms     | 0ms          | 0        |
| low       | plan       | 65.1s   | 65.1s   | 0ms          | 7        |
| low       | build      | 3875.1s | 3732.9s | 142.2s       | 193      |
| low       | verify     | 46.8s   | 0ms     | 46.8s        | 0        |
| low       | review     | 1393s   | 1393s   | 0ms          | 71       |
| low       | commit     | 0ms     | 0ms     | 0ms          | 0        |
| low       | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| low       | assessment | 0ms     | 0ms     | 0ms          | 0        |
| fixer     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fixer     | plan       | 164.7s  | 164.7s  | 0ms          | 7        |
| fixer     | build      | 1491.8s | 1327s   | 164.8s       | 74       |
| fixer     | verify     | 31.2s   | 0ms     | 31.2s        | 0        |
| fixer     | review     | 1082.4s | 1082.4s | 0ms          | 62       |
| fixer     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fixer     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fixer     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| luna-high | shape      | 0ms     | 0ms     | 0ms          | 0        |
| luna-high | plan       | 93.5s   | 93.5s   | 0ms          | 7        |
| luna-high | build      | 3189s   | 3031.1s | 157.9s       | 171      |
| luna-high | verify     | 32.2s   | 0ms     | 32.2s        | 0        |
| luna-high | review     | 1002.6s | 1002.6s | 0ms          | 64       |
| luna-high | commit     | 0ms     | 0ms     | 0ms          | 0        |
| luna-high | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| luna-high | assessment | 0ms     | 0ms     | 0ms          | 0        |
| sol-low   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-low   | plan       | 71s     | 71s     | 0ms          | 7        |
| sol-low   | build      | 1263s   | 1196.5s | 66.6s        | 44       |
| sol-low   | verify     | 11.2s   | 0ms     | 11.2s        | 0        |
| sol-low   | review     | 430.3s  | 430.3s  | 0ms          | 29       |
| sol-low   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-low   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-low   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                          | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rf1-env-ex-r0-fixer-a1           | correct          | 612.7s  | 540.7s  | 72s          | 35       | 2       | 2       | 0         | 0                    |
| rf1-env-ex-r0-low-a1             | workflow failure | 1277.9s | 1199.7s | 78.2s        | 61       | 6       | 3       | 0         | 0                    |
| rf1-env-ex-r0-luna-high-a1       | correct          | 1225.2s | 1132.9s | 92.2s        | 72       | 4       | 5       | 0         | 0                    |
| rf1-env-ex-r0-sol-low-a1         | correct          | 590.5s  | 572.2s  | 18.3s        | 12       | 0       | 1       | 0         | 0                    |
| rf1-env-go-r0-fixer-a1           | correct          | 632.4s  | 611.4s  | 21.1s        | 29       | 2       | 2       | 0         | 0                    |
| rf1-env-go-r0-low-a1             | correct          | 567.9s  | 548.3s  | 19.6s        | 37       | 2       | 3       | 0         | 0                    |
| rf1-env-go-r0-luna-high-a1       | correct          | 444.8s  | 424.6s  | 20.2s        | 23       | 1       | 2       | 0         | 0                    |
| rf1-env-go-r0-sol-low-a1         | correct          | 227s    | 209.7s  | 17.3s        | 10       | 0       | 1       | 0         | 0                    |
| rf1-r70-5-elixir-r0-fixer-a1     | correct          | 585.8s  | 561.4s  | 24.3s        | 30       | 1       | 2       | 0         | 0                    |
| rf1-r70-5-elixir-r0-low-a1       | workflow failure | 629.8s  | 605s    | 24.9s        | 45       | 6       | 3       | 0         | 0                    |
| rf1-r70-5-elixir-r0-luna-high-a1 | correct          | 704s    | 677.1s  | 26.9s        | 33       | 1       | 2       | 0         | 0                    |
| rf1-r70-5-elixir-r0-sol-low-a1   | correct          | 200.8s  | 188.4s  | 12.4s        | 10       | 0       | 1       | 0         | 0                    |
| rf1-r70-5-go-r0-fixer-a1         | correct          | 354.6s  | 332.6s  | 21.9s        | 26       | 2       | 2       | 0         | 0                    |
| rf1-r70-5-go-r0-low-a1           | correct          | 275s    | 269.3s  | 5.7s         | 18       | 1       | 2       | 0         | 0                    |
| rf1-r70-5-go-r0-luna-high-a1     | correct          | 532.8s  | 516.7s  | 16.1s        | 35       | 2       | 3       | 0         | 0                    |
| rf1-r70-5-go-r0-sol-low-a1       | correct          | 145s    | 135.2s  | 9.8s         | 11       | 0       | 1       | 0         | 0                    |
| rf1-r70-7-elixir-r0-fixer-a1     | correct          | 931s    | 885.4s  | 45.6s        | 33       | 2       | 2       | 0         | 0                    |
| rf1-r70-7-elixir-r0-low-a1       | correct          | 1488.2s | 1420.7s | 67.5s        | 64       | 5       | 3       | 0         | 0                    |
| rf1-r70-7-elixir-r0-luna-high-a1 | correct          | 527.8s  | 490.4s  | 37.4s        | 35       | 2       | 3       | 0         | 0                    |
| rf1-r70-7-elixir-r0-sol-low-a1   | correct          | 161.1s  | 138.8s  | 22.3s        | 11       | 0       | 1       | 0         | 0                    |
| rf1-r70-7-go-r0-fixer-a1         | correct          | 507.4s  | 481.7s  | 25.7s        | 39       | 3       | 4       | 0         | 0                    |
| rf1-r70-7-go-r0-low-a1           | correct          | 147.9s  | 135.2s  | 12.7s        | 11       | 0       | 1       | 0         | 0                    |
| rf1-r70-7-go-r0-luna-high-a1     | correct          | 450.2s  | 432.1s  | 18.1s        | 23       | 1       | 2       | 0         | 0                    |
| rf1-r70-7-go-r0-sol-low-a1       | correct          | 360.7s  | 344.1s  | 16.5s        | 17       | 1       | 2       | 0         | 0                    |
| rf1-sched-go-r0-fixer-a1         | correct          | 737.3s  | 718.7s  | 18.6s        | 38       | 3       | 3       | 0         | 0                    |
| rf1-sched-go-r0-low-a1           | correct          | 1032.1s | 1012.7s | 19.4s        | 35       | 3       | 4       | 0         | 0                    |
| rf1-sched-go-r0-luna-high-a1     | correct          | 465.2s  | 453.4s  | 11.8s        | 21       | 0       | 1       | 0         | 0                    |
| rf1-sched-go-r0-sol-low-a1       | correct          | 121.4s  | 109.3s  | 12s          | 9        | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
fixer openai: input 3.42M, cached 85.4k, output 72.9k, reasoning 15.2k, input_tokens_details.cache_write_tokens 0, total_tokens 3.49M
low openai: input 4.78M, cached 1.43M, output 81.8k, reasoning 13.5k, input_tokens_details.cache_write_tokens 0, total_tokens 4.86M
luna-high openai: input 3.81M, cached 0.90M, output 94.8k, reasoning 26.7k, input_tokens_details.cache_write_tokens 0, total_tokens 3.90M
sol-low openai: input 0.85M, cached 0, output 28.3k, reasoning 5.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.88M
native usage by stage and provider:
stage build fixer openai (responses): input 0.68M, cached 70.1k, output 29.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
stage build low openai (responses): input 3.53M, cached 1.43M, output 59.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 3.59M
stage build luna-high openai (responses): input 2.59M, cached 0.89M, output 74.5k, reasoning 14.2k, input_tokens_details.cache_write_tokens 0, total_tokens 2.67M
stage build sol-low openai (responses): input 0.34M, cached 0, output 19.7k, reasoning 73, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
stage plan fixer openai (responses): input 30.3k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage plan low openai (responses): input 30.3k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage plan luna-high openai (responses): input 30.3k, cached 8.3k, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage plan sol-low openai (responses): input 30.3k, cached 0, output 1.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.9k
stage repair fixer openai (responses): input 1.62M, cached 15.2k, output 24.3k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.65M
stage review fixer openai (responses): input 1.08M, cached 0, output 17.4k, reasoning 11.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.09M
stage review low openai (responses): input 1.22M, cached 0, output 20.8k, reasoning 13.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.24M
stage review luna-high openai (responses): input 1.18M, cached 0, output 18.8k, reasoning 12.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.20M
stage review sol-low openai (responses): input 0.49M, cached 0, output 7.0k, reasoning 5.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
native usage by attempt and provider:
attempt usage rf1-env-ex-r0-fixer-a1 openai (responses): input 0.58M, cached 5.8k, output 12.2k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage rf1-env-ex-r0-low-a1 openai (responses): input 1.27M, cached 0.40M, output 13.9k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.28M
attempt usage rf1-env-ex-r0-luna-high-a1 openai (responses): input 1.41M, cached 0.47M, output 20.5k, reasoning 7.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.43M
attempt usage rf1-env-ex-r0-sol-low-a1 openai (responses): input 0.13M, cached 0, output 4.5k, reasoning 804, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rf1-env-go-r0-fixer-a1 openai (responses): input 0.47M, cached 16.3k, output 13.9k, reasoning 3.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage rf1-env-go-r0-low-a1 openai (responses): input 0.50M, cached 0.11M, output 12.1k, reasoning 2.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage rf1-env-go-r0-luna-high-a1 openai (responses): input 0.28M, cached 48.8k, output 9.6k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rf1-env-go-r0-sol-low-a1 openai (responses): input 0.10M, cached 0, output 4.4k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rf1-r70-5-elixir-r0-fixer-a1 openai (responses): input 0.42M, cached 20.4k, output 12.6k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.44M
attempt usage rf1-r70-5-elixir-r0-low-a1 openai (responses): input 0.81M, cached 0.30M, output 13.5k, reasoning 2.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.83M
attempt usage rf1-r70-5-elixir-r0-luna-high-a1 openai (responses): input 0.57M, cached 0.13M, output 19.9k, reasoning 3.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage rf1-r70-5-elixir-r0-sol-low-a1 openai (responses): input 0.11M, cached 0, output 4.4k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rf1-r70-5-go-r0-fixer-a1 openai (responses): input 0.36M, cached 4.9k, output 7.1k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.37M
attempt usage rf1-r70-5-go-r0-low-a1 openai (responses): input 0.20M, cached 0, output 6.1k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rf1-r70-5-go-r0-luna-high-a1 openai (responses): input 0.52M, cached 0.11M, output 14.5k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.53M
attempt usage rf1-r70-5-go-r0-sol-low-a1 openai (responses): input 0.11M, cached 0, output 3.7k, reasoning 828, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rf1-r70-7-elixir-r0-fixer-a1 openai (responses): input 0.48M, cached 6.3k, output 9.1k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage rf1-r70-7-elixir-r0-low-a1 openai (responses): input 1.43M, cached 0.57M, output 19.7k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.45M
attempt usage rf1-r70-7-elixir-r0-luna-high-a1 openai (responses): input 0.49M, cached 92.7k, output 11.4k, reasoning 3.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.50M
attempt usage rf1-r70-7-elixir-r0-sol-low-a1 openai (responses): input 0.11M, cached 0, output 3.3k, reasoning 303, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage rf1-r70-7-go-r0-fixer-a1 openai (responses): input 0.56M, cached 0, output 9.3k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.57M
attempt usage rf1-r70-7-go-r0-low-a1 openai (responses): input 99.5k, cached 0, output 2.7k, reasoning 338, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage rf1-r70-7-go-r0-luna-high-a1 openai (responses): input 0.28M, cached 5.6k, output 10.4k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage rf1-r70-7-go-r0-sol-low-a1 openai (responses): input 0.20M, cached 0, output 4.5k, reasoning 846, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rf1-sched-go-r0-fixer-a1 openai (responses): input 0.54M, cached 31.9k, output 8.7k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.55M
attempt usage rf1-sched-go-r0-low-a1 openai (responses): input 0.47M, cached 56.6k, output 13.9k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.49M
attempt usage rf1-sched-go-r0-luna-high-a1 openai (responses): input 0.26M, cached 36.9k, output 8.4k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rf1-sched-go-r0-sol-low-a1 openai (responses): input 89.7k, cached 0, output 3.6k, reasoning 458, input_tokens_details.cache_write_tokens 0, total_tokens 93.2k
attempt outcomes included: low: correct 5, incorrect 0, workflow failure 2, infrastructure 0, incomplete 0; fixer: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; luna-high: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; sol-low: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 15936.3s, model 15147.9s, tools/checks 788.4s, requests 823
builder settings: low openai gpt-6-luna reasoning.effort=low
builder settings: fixer openai gpt-6-luna reasoning.effort=low
builder settings: luna-high openai gpt-6-luna reasoning.effort=high (not equivalent)
builder settings: sol-low openai gpt-6.1-sol reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 28, started 28, scored 28, incorrect 0, infrastructure 0, incomplete 0
variant fixer differs from low in:
  repair.context: packet,diff,check_results,review_findings -> packet,diff,changed_files,check_results,review_findings
  repair.conversation: continue -> fresh
  repair.roles: builder -> fixer
variant luna-high differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna high
variant sol-low differs from low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6.1-sol low
R02: exercised in 7 of 7 fixer attempts
R03: exercised in 7 of 7 fixer attempts
R04: exercised in 7 of 7 fixer attempts
roles.builder.effort: exercised in 7 of 7 luna-high attempts
roles.builder.model: exercised in 7 of 7 sol-low attempts
first position per task: env-ex low 0, fixer 1, luna-high 0, sol-low 0 (1 repetitions, 4 variants)
first position per task: env-go low 1, fixer 0, luna-high 0, sol-low 0 (1 repetitions, 4 variants)
first position per task: r70-5-elixir low 0, fixer 0, luna-high 0, sol-low 1 (1 repetitions, 4 variants)
first position per task: r70-5-go low 0, fixer 1, luna-high 0, sol-low 0 (1 repetitions, 4 variants)
first position per task: r70-7-elixir low 0, fixer 0, luna-high 1, sol-low 0 (1 repetitions, 4 variants)
first position per task: r70-7-go low 1, fixer 0, luna-high 0, sol-low 0 (1 repetitions, 4 variants)
first position per task: sched-go low 0, fixer 0, luna-high 1, sol-low 0 (1 repetitions, 4 variants)
low: not the Kogen profile (differs in roles.builder.effort, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, roles.planner.effort, roles.planner.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
fixer: not the Kogen profile (differs in repair.context, repair.conversation, repair.roles, roles.builder.effort, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, roles.planner.effort, roles.planner.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
luna-high: not the Kogen profile (differs in roles.builder.effort, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, roles.planner.effort, roles.planner.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
sol-low: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, roles.planner.effort, roles.planner.model, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
low: repair.context = packet,diff,check_results,review_findings (extension)
low: repair.roles = builder (extension)
low: shape.critique_prompt = lab:critique (extension)
low: shape.critique_rounds = 1 (extension)
fixer: repair.context = packet,diff,changed_files,check_results,review_findings (extension)
fixer: repair.conversation = fresh (extension)
fixer: repair.roles = fixer (extension)
fixer: shape.critique_prompt = lab:critique (extension)
fixer: shape.critique_rounds = 1 (extension)
luna-high: repair.context = packet,diff,check_results,review_findings (extension)
luna-high: repair.roles = builder (extension)
luna-high: shape.critique_prompt = lab:critique (extension)
luna-high: shape.critique_rounds = 1 (extension)
sol-low: repair.context = packet,diff,check_results,review_findings (extension)
sol-low: repair.roles = builder (extension)
sol-low: shape.critique_prompt = lab:critique (extension)
sol-low: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
