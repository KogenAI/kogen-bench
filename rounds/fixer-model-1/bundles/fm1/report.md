incomplete: 19 of 24 cells scored
Question: fixer-model-1: with a weak builder and a Sol-high reviewer, does a cheaper fixer (Sol medium, Sol low, Luna medium) keep the Sol-high fixer's correctness at lower cost?
Hypothesis: exploratory: Sol medium matches Sol high; Sol low and Luna medium need more repairs
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (19 of 24 cells scored)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| fix-sol-high    | 4       | 0         | 0                | 0              | 1          | 100%         | 0 of 4        | 0           |
| fix-sol-medium  | 4       | 0         | 1                | 0              | 0          | 80%          | 0 of 4        | 0           |
| fix-sol-low     | 4       | 0         | 1                | 0              | 1          | 80%          | 0 of 4        | 0           |
| fix-luna-medium | 2       | 0         | 3                | 0              | 0          | 40%          | 0 of 2        | 0           |
false success: 0 of 4 claims (fix-sol-high)
false success: 0 of 4 claims (fix-sol-medium)
false success: 0 of 4 claims (fix-sol-low)
false success: 0 of 2 claims (fix-luna-medium)
shaping outcomes:
fix-sol-high: shaping ready 5, shaping failed 0; correct 4 of 4
fix-sol-medium: shaping ready 5, shaping failed 0; correct 4 of 5
fix-sol-low: shaping ready 6, shaping failed 0; correct 4 of 5
fix-luna-medium: shaping ready 5, shaping failed 0; correct 2 of 5
## Per-task outcomes
| task         | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-----------------|---------|-----------|------------------|----------------|------------|
| env-ex       | fix-sol-high    | 0       | 0         | 0                | 0              | 0          |
| env-ex       | fix-sol-medium  | 0       | 0         | 0                | 0              | 0          |
| env-ex       | fix-sol-low     | 0       | 0         | 0                | 0              | 1          |
| env-ex       | fix-luna-medium | 0       | 0         | 0                | 0              | 0          |
| r70-1-go     | fix-sol-high    | 0       | 0         | 0                | 0              | 1          |
| r70-1-go     | fix-sol-medium  | 0       | 0         | 1                | 0              | 0          |
| r70-1-go     | fix-sol-low     | 1       | 0         | 0                | 0              | 0          |
| r70-1-go     | fix-luna-medium | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir | fix-sol-high    | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir | fix-sol-medium  | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir | fix-sol-low     | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir | fix-luna-medium | 0       | 0         | 1                | 0              | 0          |
| r70-4-go     | fix-sol-high    | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | fix-sol-medium  | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | fix-sol-low     | 1       | 0         | 0                | 0              | 0          |
| r70-4-go     | fix-luna-medium | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | fix-sol-high    | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | fix-sol-medium  | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | fix-sol-low     | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | fix-luna-medium | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | fix-sol-high    | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | fix-sol-medium  | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | fix-sol-low     | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir | fix-luna-medium | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| fix-sol-high    | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-high    | plan       | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-high    | build      | 662.6s  | 305.8s  | 356.7s       | 28       |
| fix-sol-high    | verify     | 73.6s   | 0ms     | 73.6s        | 0        |
| fix-sol-high    | review     | 1233.6s | 1233.6s | 0ms          | 64       |
| fix-sol-high    | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-high    | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-high    | assessment | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-medium  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-medium  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-medium  | build      | 595.1s  | 332.1s  | 263s         | 33       |
| fix-sol-medium  | verify     | 67.4s   | 0ms     | 67.4s        | 0        |
| fix-sol-medium  | review     | 964.7s  | 964.7s  | 0ms          | 54       |
| fix-sol-medium  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-medium  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-medium  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-low     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-low     | plan       | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-low     | build      | 1841.1s | 1533.3s | 307.8s       | 50       |
| fix-sol-low     | verify     | 91.2s   | 0ms     | 91.2s        | 0        |
| fix-sol-low     | review     | 1285.1s | 1285.1s | 0ms          | 76       |
| fix-sol-low     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-low     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fix-sol-low     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| fix-luna-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| fix-luna-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| fix-luna-medium | build      | 1268.2s | 367.6s  | 900.6s       | 32       |
| fix-luna-medium | verify     | 47s     | 0ms     | 47s          | 0        |
| fix-luna-medium | review     | 1313.8s | 1313.8s | 0ms          | 70       |
| fix-luna-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| fix-luna-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| fix-luna-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| fm1-env-ex-r0-fix-sol-low-a1           | incomplete       | 1456.7s | 1420.7s | 36s          | 37       | 3       | 3       | 0         | 0                    |
| fm1-r70-1-go-r0-fix-luna-medium-a1     | workflow failure | 2478.1s | 1812.2s | 666s         | 80       | 6       | 6       | 0         | 0                    |
| fm1-r70-1-go-r0-fix-sol-high-a1        | incomplete       | 1629.5s | 1546.1s | 83.4s        | 38       | 3       | 3       | 0         | 0                    |
| fm1-r70-1-go-r0-fix-sol-low-a1         | correct          | 727.3s  | 653s    | 74.3s        | 55       | 5       | 5       | 0         | 0                    |
| fm1-r70-1-go-r0-fix-sol-medium-a1      | workflow failure | 832.9s  | 721.9s  | 110.9s       | 55       | 6       | 6       | 0         | 0                    |
| fm1-r70-4-elixir-r0-fix-luna-medium-a1 | workflow failure | 1113.1s | 970.2s  | 143s         | 80       | 6       | 6       | 0         | 0                    |
| fm1-r70-4-elixir-r0-fix-sol-high-a1    | correct          | 1025.1s | 798.5s  | 226.6s       | 62       | 6       | 6       | 0         | 0                    |
| fm1-r70-4-elixir-r0-fix-sol-low-a1     | workflow failure | 827.2s  | 649.4s  | 177.8s       | 49       | 6       | 6       | 0         | 0                    |
| fm1-r70-4-elixir-r0-fix-sol-medium-a1  | correct          | 298.8s  | 261.7s  | 37.1s        | 21       | 2       | 2       | 0         | 0                    |
| fm1-r70-4-go-r0-fix-luna-medium-a1     | workflow failure | 332.5s  | 298.7s  | 33.8s        | 30       | 3       | 2       | 0         | 0                    |
| fm1-r70-4-go-r0-fix-sol-high-a1        | correct          | 553.1s  | 465.4s  | 87.7s        | 40       | 4       | 4       | 0         | 0                    |
| fm1-r70-4-go-r0-fix-sol-low-a1         | correct          | 492.6s  | 416.3s  | 76.3s        | 33       | 3       | 4       | 0         | 0                    |
| fm1-r70-4-go-r0-fix-sol-medium-a1      | correct          | 728.8s  | 585.6s  | 143.3s       | 51       | 5       | 5       | 0         | 0                    |
| fm1-r70-5-elixir-r0-fix-luna-medium-a1 | correct          | 622.1s  | 574s    | 48.1s        | 46       | 4       | 3       | 0         | 0                    |
| fm1-r70-5-elixir-r0-fix-sol-high-a1    | correct          | 514.2s  | 491.4s  | 22.8s        | 27       | 2       | 3       | 0         | 0                    |
| fm1-r70-5-elixir-r0-fix-sol-low-a1     | correct          | 291.2s  | 273.2s  | 18.1s        | 19       | 1       | 1       | 0         | 0                    |
| fm1-r70-5-elixir-r0-fix-sol-medium-a1  | correct          | 345.4s  | 315.8s  | 29.6s        | 25       | 2       | 2       | 0         | 0                    |
| fm1-r70-6-elixir-r0-fix-luna-medium-a1 | correct          | 748.6s  | 667.7s  | 80.9s        | 76       | 5       | 3       | 0         | 0                    |
| fm1-r70-6-elixir-r0-fix-sol-high-a1    | correct          | 436.1s  | 404.2s  | 31.9s        | 27       | 2       | 2       | 0         | 0                    |
| fm1-r70-6-elixir-r0-fix-sol-low-a1     | correct          | 416.8s  | 375.5s  | 41.3s        | 33       | 4       | 4       | 0         | 0                    |
| fm1-r70-6-elixir-r0-fix-sol-medium-a1  | correct          | 263.6s  | 233.5s  | 30s          | 27       | 2       | 2       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
fix-luna-medium openai: input 5.63M, cached 0.81M, output 0.10M, reasoning 35.5k, input_tokens_details.cache_write_tokens 0, total_tokens 5.74M
fix-sol-high openai: input 3.67M, cached 0.26M, output 86.2k, reasoning 36.0k, input_tokens_details.cache_write_tokens 0, total_tokens 3.76M
fix-sol-low openai: input 3.72M, cached 0.13M, output 90.4k, reasoning 33.9k, input_tokens_details.cache_write_tokens 0, total_tokens 3.81M
fix-sol-medium openai: input 3.05M, cached 80.5k, output 68.5k, reasoning 27.3k, input_tokens_details.cache_write_tokens 0, total_tokens 3.11M
native usage by stage and provider:
stage build fix-luna-medium openai (responses): input 0.25M, cached 44.5k, output 13.6k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
stage build fix-sol-high openai (responses): input 0.20M, cached 51.3k, output 9.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.21M
stage build fix-sol-low openai (responses): input 0.45M, cached 77.2k, output 20.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
stage build fix-sol-medium openai (responses): input 0.25M, cached 31.7k, output 11.0k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
stage repair fix-luna-medium openai (responses): input 4.11M, cached 0.75M, output 50.0k, reasoning 5.6k, input_tokens_details.cache_write_tokens 0, total_tokens 4.16M
stage repair fix-sol-high openai (responses): input 2.19M, cached 0.14M, output 41.3k, reasoning 9.3k, input_tokens_details.cache_write_tokens 0, total_tokens 2.23M
stage repair fix-sol-low openai (responses): input 1.79M, cached 19.3k, output 26.2k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 1.82M
stage repair fix-sol-medium openai (responses): input 1.74M, cached 29.3k, output 24.4k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 1.76M
stage review fix-luna-medium openai (responses): input 1.27M, cached 14.2k, output 41.2k, reasoning 29.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.31M
stage review fix-sol-high openai (responses): input 1.28M, cached 67.3k, output 35.1k, reasoning 26.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.31M
stage review fix-sol-low openai (responses): input 1.47M, cached 37.6k, output 44.0k, reasoning 32.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.52M
stage review fix-sol-medium openai (responses): input 1.06M, cached 19.5k, output 33.1k, reasoning 24.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.09M
native usage by attempt and provider:
attempt usage fm1-env-ex-r0-fix-sol-low-a1 openai (responses): input 0.61M, cached 35.2k, output 15.3k, reasoning 4.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.63M
attempt usage fm1-r70-1-go-r0-fix-luna-medium-a1 openai (responses): input 1.51M, cached 0.22M, output 27.1k, reasoning 10.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.53M
attempt usage fm1-r70-1-go-r0-fix-sol-high-a1 openai (responses): input 0.88M, cached 93.4k, output 22.6k, reasoning 8.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.91M
attempt usage fm1-r70-1-go-r0-fix-sol-low-a1 openai (responses): input 0.94M, cached 10.8k, output 21.1k, reasoning 7.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.96M
attempt usage fm1-r70-1-go-r0-fix-sol-medium-a1 openai (responses): input 1.09M, cached 19.5k, output 23.9k, reasoning 9.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.11M
attempt usage fm1-r70-4-elixir-r0-fix-luna-medium-a1 openai (responses): input 1.34M, cached 0.13M, output 31.9k, reasoning 12.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.37M
attempt usage fm1-r70-4-elixir-r0-fix-sol-high-a1 openai (responses): input 1.14M, cached 66.2k, output 25.8k, reasoning 13.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.16M
attempt usage fm1-r70-4-elixir-r0-fix-sol-low-a1 openai (responses): input 0.82M, cached 9.7k, output 20.5k, reasoning 11.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
attempt usage fm1-r70-4-elixir-r0-fix-sol-medium-a1 openai (responses): input 0.32M, cached 39.0k, output 8.3k, reasoning 4.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.33M
attempt usage fm1-r70-4-go-r0-fix-luna-medium-a1 openai (responses): input 0.39M, cached 45.7k, output 9.6k, reasoning 3.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage fm1-r70-4-go-r0-fix-sol-high-a1 openai (responses): input 0.61M, cached 0, output 14.8k, reasoning 6.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.63M
attempt usage fm1-r70-4-go-r0-fix-sol-low-a1 openai (responses): input 0.49M, cached 4.9k, output 13.9k, reasoning 5.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.51M
attempt usage fm1-r70-4-go-r0-fix-sol-medium-a1 openai (responses): input 0.79M, cached 6.7k, output 18.4k, reasoning 8.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.81M
attempt usage fm1-r70-5-elixir-r0-fix-luna-medium-a1 openai (responses): input 0.85M, cached 0.12M, output 16.5k, reasoning 4.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.87M
attempt usage fm1-r70-5-elixir-r0-fix-sol-high-a1 openai (responses): input 0.39M, cached 42.6k, output 13.4k, reasoning 5.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage fm1-r70-5-elixir-r0-fix-sol-low-a1 openai (responses): input 0.28M, cached 41.0k, output 7.7k, reasoning 612, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage fm1-r70-5-elixir-r0-fix-sol-medium-a1 openai (responses): input 0.37M, cached 15.4k, output 11.0k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage fm1-r70-6-elixir-r0-fix-luna-medium-a1 openai (responses): input 1.55M, cached 0.30M, output 19.6k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 1.57M
attempt usage fm1-r70-6-elixir-r0-fix-sol-high-a1 openai (responses): input 0.64M, cached 59.8k, output 9.5k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.65M
attempt usage fm1-r70-6-elixir-r0-fix-sol-low-a1 openai (responses): input 0.57M, cached 32.6k, output 11.9k, reasoning 4.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.58M
attempt usage fm1-r70-6-elixir-r0-fix-sol-medium-a1 openai (responses): input 0.47M, cached 0, output 6.9k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt outcomes included: fix-sol-high: correct 4, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; fix-sol-medium: correct 4, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; fix-sol-low: correct 4, incorrect 0, workflow failure 1, infrastructure 0, incomplete 1; fix-luna-medium: correct 2, incorrect 0, workflow failure 3, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 16133.8s, model 13934.9s, tools/checks 2198.9s, requests 911
builder settings: fix-sol-high openai gpt-6-luna reasoning.effort=low
builder settings: fix-sol-medium openai gpt-6-luna reasoning.effort=low
builder settings: fix-sol-low openai gpt-6-luna reasoning.effort=low
builder settings: fix-luna-medium openai gpt-6-luna reasoning.effort=low
## CMP-3 Counts and exposure
planned 24, started 21, scored 19, incorrect 0, infrastructure 0, incomplete 2
variant fix-sol-medium differs from fix-sol-high in:
  roles.fixer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
variant fix-sol-low differs from fix-sol-high in:
  roles.fixer: openai gpt-6.1-sol high -> openai gpt-6.1-sol low
variant fix-luna-medium differs from fix-sol-high in:
  roles.fixer: openai gpt-6.1-sol high -> openai gpt-6-luna medium
  roles.fixer: openai gpt-6.1-sol high -> openai gpt-6-luna medium
roles.fixer.effort: exercised in 5 of 5 fix-sol-medium attempts
roles.fixer.effort: exercised in 6 of 6 fix-sol-low attempts
roles.fixer.effort: exercised in 5 of 5 fix-luna-medium attempts
roles.fixer.model: exercised in 5 of 5 fix-luna-medium attempts
first position per task: env-ex fix-sol-high 0, fix-sol-medium 0, fix-sol-low 1, fix-luna-medium 0 (1 repetitions, 4 variants)
first position per task: r70-1-go fix-sol-high 0, fix-sol-medium 1, fix-sol-low 0, fix-luna-medium 0 (1 repetitions, 4 variants)
first position per task: r70-4-elixir fix-sol-high 0, fix-sol-medium 0, fix-sol-low 0, fix-luna-medium 1 (1 repetitions, 4 variants)
first position per task: r70-4-go fix-sol-high 1, fix-sol-medium 0, fix-sol-low 0, fix-luna-medium 0 (1 repetitions, 4 variants)
first position per task: r70-5-elixir fix-sol-high 0, fix-sol-medium 0, fix-sol-low 0, fix-luna-medium 1 (1 repetitions, 4 variants)
first position per task: r70-6-elixir fix-sol-high 0, fix-sol-medium 1, fix-sol-low 0, fix-luna-medium 0 (1 repetitions, 4 variants)
fix-sol-high: not the Kogen profile (differs in plan.enabled, repair.context, repair.conversation, repair.roles, roles.builder.effort, roles.builder.model, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, stop.max_repairs, stop.max_tokens)
fix-sol-medium: not the Kogen profile (differs in plan.enabled, repair.context, repair.conversation, repair.roles, roles.builder.effort, roles.builder.model, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, stop.max_repairs, stop.max_tokens)
fix-sol-low: not the Kogen profile (differs in plan.enabled, repair.context, repair.conversation, repair.roles, roles.builder.effort, roles.builder.model, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, stop.max_repairs, stop.max_tokens)
fix-luna-medium: not the Kogen profile (differs in plan.enabled, repair.context, repair.conversation, repair.roles, roles.builder.effort, roles.builder.model, roles.fixer.effort, roles.fixer.model, roles.fixer.provider, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
fix-sol-high: repair.context = packet,diff,changed_files,check_results,review_findings (extension)
fix-sol-high: repair.conversation = fresh (extension)
fix-sol-high: repair.roles = fixer (extension)
fix-sol-high: shape.critique_prompt = lab:critique (extension)
fix-sol-high: shape.critique_rounds = 1 (extension)
fix-sol-medium: repair.context = packet,diff,changed_files,check_results,review_findings (extension)
fix-sol-medium: repair.conversation = fresh (extension)
fix-sol-medium: repair.roles = fixer (extension)
fix-sol-medium: shape.critique_prompt = lab:critique (extension)
fix-sol-medium: shape.critique_rounds = 1 (extension)
fix-sol-low: repair.context = packet,diff,changed_files,check_results,review_findings (extension)
fix-sol-low: repair.conversation = fresh (extension)
fix-sol-low: repair.roles = fixer (extension)
fix-sol-low: shape.critique_prompt = lab:critique (extension)
fix-sol-low: shape.critique_rounds = 1 (extension)
fix-luna-medium: repair.context = packet,diff,changed_files,check_results,review_findings (extension)
fix-luna-medium: repair.conversation = fresh (extension)
fix-luna-medium: repair.roles = fixer (extension)
fix-luna-medium: shape.critique_prompt = lab:critique (extension)
fix-luna-medium: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
