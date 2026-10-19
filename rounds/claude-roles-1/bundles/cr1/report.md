complete: 35/35 cells scored
Question: claude-roles-1: how do Claude Sonnet as reviewer, Claude Haiku as builder, and an all-Sonnet setup compare with the ChatGPT roles on correctness, tokens and dollars?
Hypothesis: exploratory: descriptive comparison per role; Sol-high reference reused from rf1
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant           | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-------------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| sol-low           | 6       | 0         | 1                | 0              | 0          | 85.7%        | 0 of 6        | 0           |
| sonnet-review     | 5       | 2         | 0                | 0              | 0          | 71.4%        | 2 of 7        | 0           |
| haiku-build       | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
| luna-medium-build | 6       | 0         | 1                | 0              | 0          | 85.7%        | 0 of 6        | 0           |
| all-sonnet        | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
false success: 0 of 6 claims (sol-low)
false success: 2 of 7 claims (sonnet-review)
false success: 0 of 7 claims (haiku-build)
false success: 0 of 6 claims (luna-medium-build)
false success: 0 of 7 claims (all-sonnet)
shaping outcomes:
sol-low: shaping ready 7, shaping failed 0; correct 6 of 7
sonnet-review: shaping ready 7, shaping failed 0; correct 5 of 7
haiku-build: shaping ready 7, shaping failed 0; correct 7 of 7
luna-medium-build: shaping ready 7, shaping failed 0; correct 6 of 7
all-sonnet: shaping ready 7, shaping failed 0; correct 7 of 7
## Per-task outcomes
| task         | variant           | correct | incorrect | workflow failure | infrastructure | incomplete |
|--------------|-------------------|---------|-----------|------------------|----------------|------------|
| env-ex       | sol-low           | 0       | 0         | 1                | 0              | 0          |
| env-ex       | sonnet-review     | 0       | 1         | 0                | 0              | 0          |
| env-ex       | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| env-ex       | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| env-ex       | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| env-go       | sol-low           | 1       | 0         | 0                | 0              | 0          |
| env-go       | sonnet-review     | 1       | 0         | 0                | 0              | 0          |
| env-go       | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| env-go       | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| env-go       | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | sol-low           | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | sonnet-review     | 0       | 1         | 0                | 0              | 0          |
| r70-5-elixir | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| r70-5-elixir | luna-medium-build | 0       | 0         | 1                | 0              | 0          |
| r70-5-elixir | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | sol-low           | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | sonnet-review     | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| r70-5-go     | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | sol-low           | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | sonnet-review     | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| r70-7-elixir | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | sol-low           | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | sonnet-review     | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| r70-7-go     | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
| sched-go     | sol-low           | 1       | 0         | 0                | 0              | 0          |
| sched-go     | sonnet-review     | 1       | 0         | 0                | 0              | 0          |
| sched-go     | haiku-build       | 1       | 0         | 0                | 0              | 0          |
| sched-go     | luna-medium-build | 1       | 0         | 0                | 0              | 0          |
| sched-go     | all-sonnet        | 1       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant           | stage      | wall    | model   | tools/checks | requests |
|-------------------|------------|---------|---------|--------------|----------|
| sol-low           | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sol-low           | plan       | 82.8s   | 82.8s   | 0ms          | 7        |
| sol-low           | build      | 6815.1s | 6674.1s | 141s         | 214      |
| sol-low           | verify     | 50.9s   | 0ms     | 50.9s        | 0        |
| sol-low           | review     | 832.2s  | 832.2s  | 0ms          | 52       |
| sol-low           | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sol-low           | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sol-low           | assessment | 0ms     | 0ms     | 0ms          | 0        |
| sonnet-review     | shape      | 0ms     | 0ms     | 0ms          | 0        |
| sonnet-review     | plan       | 193.3s  | 193.3s  | 0ms          | 7        |
| sonnet-review     | build      | 3291.5s | 3193.9s | 97.6s        | 139      |
| sonnet-review     | verify     | 32.3s   | 0ms     | 32.3s        | 0        |
| sonnet-review     | review     | 260.7s  | 260.7s  | 0ms          | 23       |
| sonnet-review     | commit     | 0ms     | 0ms     | 0ms          | 0        |
| sonnet-review     | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| sonnet-review     | assessment | 0ms     | 0ms     | 0ms          | 0        |
| haiku-build       | shape      | 0ms     | 0ms     | 0ms          | 0        |
| haiku-build       | plan       | 80.4s   | 80.4s   | 0ms          | 7        |
| haiku-build       | build      | 920.8s  | 814.9s  | 105.9s       | 86       |
| haiku-build       | verify     | 20.7s   | 0ms     | 20.7s        | 0        |
| haiku-build       | review     | 555.5s  | 555.5s  | 0ms          | 34       |
| haiku-build       | commit     | 0ms     | 0ms     | 0ms          | 0        |
| haiku-build       | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| haiku-build       | assessment | 0ms     | 0ms     | 0ms          | 0        |
| luna-medium-build | shape      | 0ms     | 0ms     | 0ms          | 0        |
| luna-medium-build | plan       | 126s    | 126s    | 0ms          | 7        |
| luna-medium-build | build      | 5489.1s | 5345.8s | 143.3s       | 157      |
| luna-medium-build | verify     | 47.5s   | 0ms     | 47.5s        | 0        |
| luna-medium-build | review     | 853s    | 853s    | 0ms          | 51       |
| luna-medium-build | commit     | 0ms     | 0ms     | 0ms          | 0        |
| luna-medium-build | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| luna-medium-build | assessment | 0ms     | 0ms     | 0ms          | 0        |
| all-sonnet        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| all-sonnet        | plan       | 110.5s  | 110.5s  | 0ms          | 7        |
| all-sonnet        | build      | 445.2s  | 359s    | 86.2s        | 29       |
| all-sonnet        | verify     | 14.8s   | 0ms     | 14.8s        | 0        |
| all-sonnet        | review     | 124s    | 124s    | 0ms          | 13       |
| all-sonnet        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| all-sonnet        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| all-sonnet        | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                  | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| cr1-env-ex-r0-all-sonnet-a1              | correct          | 161.3s  | 130.6s  | 30.7s        | 9        | 1       | 3       | 0         | 0                    |
| cr1-env-ex-r0-haiku-build-a1             | correct          | 374.7s  | 331.1s  | 43.5s        | 23       | 2       | 3       | 0         | 0                    |
| cr1-env-ex-r0-luna-medium-build-a1       | correct          | 1572s   | 1516.1s | 55.9s        | 29       | 2       | 3       | 0         | 0                    |
| cr1-env-ex-r0-sol-low-a1                 | workflow failure | 1303.9s | 1245.2s | 58.7s        | 61       | 6       | 2       | 0         | 0                    |
| cr1-env-ex-r0-sonnet-review-a1           | incorrect        | 1620.5s | 1556.5s | 64s          | 49       | 4       | 4       | 0         | 0                    |
| cr1-env-go-r0-all-sonnet-a1              | correct          | 107.8s  | 98.3s   | 9.4s         | 7        | 1       | 2       | 0         | 0                    |
| cr1-env-go-r0-haiku-build-a1             | correct          | 281.7s  | 260.2s  | 21.5s        | 28       | 2       | 3       | 0         | 0                    |
| cr1-env-go-r0-luna-medium-build-a1       | correct          | 1557.1s | 1535.8s | 21.3s        | 29       | 2       | 3       | 0         | 0                    |
| cr1-env-go-r0-sol-low-a1                 | correct          | 676s    | 665s    | 11s          | 27       | 2       | 3       | 0         | 0                    |
| cr1-env-go-r0-sonnet-review-a1           | correct          | 443.4s  | 433.9s  | 9.5s         | 20       | 2       | 4       | 0         | 0                    |
| cr1-r70-5-elixir-r0-all-sonnet-a1        | correct          | 173.2s  | 138.9s  | 34.3s        | 8        | 0       | 1       | 0         | 0                    |
| cr1-r70-5-elixir-r0-haiku-build-a1       | correct          | 335.2s  | 302.9s  | 32.3s        | 21       | 1       | 2       | 0         | 0                    |
| cr1-r70-5-elixir-r0-luna-medium-build-a1 | workflow failure | 1049.2s | 1001.8s | 47.4s        | 53       | 6       | 4       | 0         | 0                    |
| cr1-r70-5-elixir-r0-sol-low-a1           | correct          | 1295.8s | 1215.5s | 80.4s        | 52       | 5       | 3       | 0         | 0                    |
| cr1-r70-5-elixir-r0-sonnet-review-a1     | incorrect        | 245.6s  | 224.9s  | 20.7s        | 17       | 1       | 2       | 0         | 0                    |
| cr1-r70-5-go-r0-all-sonnet-a1            | correct          | 69.5s   | 51.2s   | 18.2s        | 5        | 0       | 1       | 0         | 0                    |
| cr1-r70-5-go-r0-haiku-build-a1           | correct          | 149.4s  | 131.8s  | 17.7s        | 11       | 0       | 1       | 0         | 0                    |
| cr1-r70-5-go-r0-luna-medium-build-a1     | correct          | 778.5s  | 755.5s  | 23.1s        | 33       | 2       | 3       | 0         | 0                    |
| cr1-r70-5-go-r0-sol-low-a1               | correct          | 789.5s  | 769.5s  | 20s          | 32       | 3       | 4       | 0         | 0                    |
| cr1-r70-5-go-r0-sonnet-review-a1         | correct          | 376.4s  | 366.6s  | 9.8s         | 20       | 2       | 3       | 0         | 0                    |
| cr1-r70-7-elixir-r0-all-sonnet-a1        | correct          | 72.1s   | 58.2s   | 13.9s        | 5        | 0       | 1       | 0         | 0                    |
| cr1-r70-7-elixir-r0-haiku-build-a1       | correct          | 140.4s  | 122s    | 18.4s        | 12       | 0       | 1       | 0         | 0                    |
| cr1-r70-7-elixir-r0-luna-medium-build-a1 | correct          | 894.4s  | 835.4s  | 58.9s        | 34       | 4       | 4       | 0         | 0                    |
| cr1-r70-7-elixir-r0-sol-low-a1           | correct          | 1478.1s | 1451.6s | 26.5s        | 29       | 2       | 2       | 0         | 0                    |
| cr1-r70-7-elixir-r0-sonnet-review-a1     | correct          | 363s    | 341.5s  | 21.5s        | 16       | 1       | 2       | 0         | 0                    |
| cr1-r70-7-go-r0-all-sonnet-a1            | correct          | 80s     | 62.4s   | 17.6s        | 9        | 1       | 2       | 0         | 0                    |
| cr1-r70-7-go-r0-haiku-build-a1           | correct          | 177.2s  | 160s    | 17.3s        | 20       | 0       | 1       | 0         | 0                    |
| cr1-r70-7-go-r0-luna-medium-build-a1     | correct          | 191.4s  | 179.8s  | 11.6s        | 19       | 1       | 2       | 0         | 0                    |
| cr1-r70-7-go-r0-sol-low-a1               | correct          | 670.6s  | 645.1s  | 25.4s        | 32       | 3       | 4       | 0         | 0                    |
| cr1-r70-7-go-r0-sonnet-review-a1         | correct          | 369.2s  | 348.9s  | 20.4s        | 17       | 2       | 3       | 0         | 0                    |
| cr1-sched-go-r0-all-sonnet-a1            | correct          | 70.3s   | 53.8s   | 16.6s        | 6        | 0       | 1       | 0         | 0                    |
| cr1-sched-go-r0-haiku-build-a1           | correct          | 159.6s  | 142.9s  | 16.7s        | 12       | 0       | 1       | 0         | 0                    |
| cr1-sched-go-r0-luna-medium-build-a1     | correct          | 518.8s  | 500.4s  | 18.4s        | 18       | 1       | 2       | 0         | 0                    |
| cr1-sched-go-r0-sol-low-a1               | correct          | 1613.8s | 1597.2s | 16.6s        | 40       | 5       | 4       | 0         | 0                    |
| cr1-sched-go-r0-sonnet-review-a1         | correct          | 399.8s  | 375.7s  | 24.1s        | 30       | 4       | 4       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
all-sonnet anthropic: input 146, cache_read 0.37M, cache_creation 0.44M, output 63.6k, thinking 12.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.44M
haiku-build anthropic: input 186, cache_read 2.38M, cache_creation 0.27M, output 0.18M, thinking 0.11M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.27M
haiku-build openai: input 0.71M, cached 0, output 4.7k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.72M
luna-medium-build openai: input 3.03M, cached 0.62M, output 55.6k, reasoning 3.4k, input_tokens_details.cache_write_tokens 0, total_tokens 3.09M
sol-low openai: input 4.88M, cached 1.56M, output 86.0k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 4.97M
sonnet-review anthropic: input 88, cache_read 48.8k, cache_creation 0.51M, output 21.7k, thinking 14.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.51M
sonnet-review openai: input 1.80M, cached 0.58M, output 43.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.84M
native usage by stage and provider:
stage build all-sonnet anthropic (messages): input 72, cache_read 0.29M, cache_creation 0.12M, output 41.0k, thinking 4.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.12M
stage build haiku-build anthropic (messages): input 186, cache_read 2.38M, cache_creation 0.27M, output 0.18M, thinking 0.11M, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.27M
stage build luna-medium-build openai (responses): input 2.21M, cached 0.62M, output 47.3k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 2.26M
stage build sol-low openai (responses): input 4.02M, cached 1.55M, output 78.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 4.10M
stage build sonnet-review openai (responses): input 1.77M, cached 0.58M, output 41.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 1.81M
stage plan all-sonnet anthropic (messages): input 28, cache_read 0, cache_creation 46.1k, output 13.1k, thinking 456, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 46.1k
stage plan haiku-build openai (responses): input 30.3k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage plan luna-medium-build openai (responses): input 30.3k, cached 0, output 1.7k, reasoning 177, input_tokens_details.cache_write_tokens 0, total_tokens 32.0k
stage plan sol-low openai (responses): input 30.3k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage plan sonnet-review openai (responses): input 30.3k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.8k
stage review all-sonnet anthropic (messages): input 46, cache_read 81.9k, cache_creation 0.27M, output 9.4k, thinking 7.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.27M
stage review haiku-build openai (responses): input 0.68M, cached 0, output 3.2k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
stage review luna-medium-build openai (responses): input 0.79M, cached 0, output 6.6k, reasoning 1.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.80M
stage review sol-low openai (responses): input 0.83M, cached 14.7k, output 6.1k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.84M
stage review sonnet-review anthropic (messages): input 88, cache_read 48.8k, cache_creation 0.51M, output 21.7k, thinking 14.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.51M
native usage by attempt and provider:
attempt usage cr1-env-ex-r0-all-sonnet-a1 anthropic (messages): input 26, cache_read 91.7k, cache_creation 88.9k, output 13.9k, thinking 3.9k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 88.9k
attempt usage cr1-env-ex-r0-haiku-build-a1 anthropic (messages): input 30, cache_read 0.56M, cache_creation 54.3k, output 41.9k, thinking 28.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 54.3k
attempt usage cr1-env-ex-r0-haiku-build-a1 openai (responses): input 0.18M, cached 0, output 1.3k, reasoning 517, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cr1-env-ex-r0-luna-medium-build-a1 openai (responses): input 0.45M, cached 67.3k, output 6.9k, reasoning 280, input_tokens_details.cache_write_tokens 0, total_tokens 0.45M
attempt usage cr1-env-ex-r0-sol-low-a1 openai (responses): input 1.73M, cached 0.85M, output 23.6k, reasoning 42, input_tokens_details.cache_write_tokens 0, total_tokens 1.75M
attempt usage cr1-env-ex-r0-sonnet-review-a1 anthropic (messages): input 16, cache_read 0, cache_creation 0.10M, output 5.1k, thinking 3.7k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 0.10M
attempt usage cr1-env-ex-r0-sonnet-review-a1 openai (responses): input 0.81M, cached 0.34M, output 10.9k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.82M
attempt usage cr1-env-go-r0-all-sonnet-a1 anthropic (messages): input 22, cache_read 39.2k, cache_creation 85.4k, output 11.3k, thinking 2.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 85.4k
attempt usage cr1-env-go-r0-haiku-build-a1 anthropic (messages): input 40, cache_read 0.61M, cache_creation 43.7k, output 32.3k, thinking 18.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 43.7k
attempt usage cr1-env-go-r0-haiku-build-a1 openai (responses): input 0.18M, cached 0, output 1.1k, reasoning 397, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cr1-env-go-r0-luna-medium-build-a1 openai (responses): input 0.35M, cached 48.4k, output 5.2k, reasoning 299, input_tokens_details.cache_write_tokens 0, total_tokens 0.36M
attempt usage cr1-env-go-r0-sol-low-a1 openai (responses): input 0.37M, cached 59.6k, output 7.5k, reasoning 218, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage cr1-env-go-r0-sonnet-review-a1 anthropic (messages): input 14, cache_read 25.7k, cache_creation 78.5k, output 3.7k, thinking 2.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 78.5k
attempt usage cr1-env-go-r0-sonnet-review-a1 openai (responses): input 0.16M, cached 16.6k, output 4.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cr1-r70-5-elixir-r0-all-sonnet-a1 anthropic (messages): input 22, cache_read 79.2k, cache_creation 53.2k, output 9.4k, thinking 1.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 53.2k
attempt usage cr1-r70-5-elixir-r0-haiku-build-a1 anthropic (messages): input 30, cache_read 0.47M, cache_creation 50.2k, output 37.8k, thinking 26.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 50.2k
attempt usage cr1-r70-5-elixir-r0-haiku-build-a1 openai (responses): input 0.12M, cached 0, output 799, reasoning 213, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage cr1-r70-5-elixir-r0-luna-medium-build-a1 openai (responses): input 0.90M, cached 0.35M, output 13.4k, reasoning 629, input_tokens_details.cache_write_tokens 0, total_tokens 0.92M
attempt usage cr1-r70-5-elixir-r0-sol-low-a1 openai (responses): input 0.99M, cached 0.32M, output 18.7k, reasoning 232, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
attempt usage cr1-r70-5-elixir-r0-sonnet-review-a1 anthropic (messages): input 8, cache_read 0, cache_creation 44.6k, output 2.2k, thinking 1.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 44.6k
attempt usage cr1-r70-5-elixir-r0-sonnet-review-a1 openai (responses): input 0.15M, cached 31.2k, output 5.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage cr1-r70-5-go-r0-all-sonnet-a1 anthropic (messages): input 16, cache_read 20.7k, cache_creation 46.2k, output 7.0k, thinking 1.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 46.2k
attempt usage cr1-r70-5-go-r0-haiku-build-a1 anthropic (messages): input 16, cache_read 0.13M, cache_creation 30.4k, output 20.3k, thinking 12.3k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 30.4k
attempt usage cr1-r70-5-go-r0-haiku-build-a1 openai (responses): input 63.7k, cached 0, output 308, reasoning 36, input_tokens_details.cache_write_tokens 0, total_tokens 64.0k
attempt usage cr1-r70-5-go-r0-luna-medium-build-a1 openai (responses): input 0.45M, cached 55.7k, output 10.5k, reasoning 492, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage cr1-r70-5-go-r0-sol-low-a1 openai (responses): input 0.41M, cached 38.5k, output 9.4k, reasoning 134, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
attempt usage cr1-r70-5-go-r0-sonnet-review-a1 anthropic (messages): input 12, cache_read 0, cache_creation 72.9k, output 3.1k, thinking 2.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 72.9k
attempt usage cr1-r70-5-go-r0-sonnet-review-a1 openai (responses): input 0.17M, cached 24.1k, output 6.7k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cr1-r70-7-elixir-r0-all-sonnet-a1 anthropic (messages): input 16, cache_read 20.0k, cache_creation 44.6k, output 6.4k, thinking 1.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 44.6k
attempt usage cr1-r70-7-elixir-r0-haiku-build-a1 anthropic (messages): input 18, cache_read 0.13M, cache_creation 27.9k, output 16.1k, thinking 10.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 27.9k
attempt usage cr1-r70-7-elixir-r0-haiku-build-a1 openai (responses): input 57.5k, cached 0, output 361, reasoning 34, input_tokens_details.cache_write_tokens 0, total_tokens 57.9k
attempt usage cr1-r70-7-elixir-r0-luna-medium-build-a1 openai (responses): input 0.45M, cached 66.3k, output 9.8k, reasoning 1.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage cr1-r70-7-elixir-r0-sol-low-a1 openai (responses): input 0.37M, cached 59.3k, output 9.9k, reasoning 118, input_tokens_details.cache_write_tokens 0, total_tokens 0.38M
attempt usage cr1-r70-7-elixir-r0-sonnet-review-a1 anthropic (messages): input 10, cache_read 23.1k, cache_creation 47.1k, output 1.9k, thinking 1.2k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 47.1k
attempt usage cr1-r70-7-elixir-r0-sonnet-review-a1 openai (responses): input 0.12M, cached 29.2k, output 6.2k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.13M
attempt usage cr1-r70-7-go-r0-all-sonnet-a1 anthropic (messages): input 26, cache_read 75.5k, cache_creation 73.1k, output 7.7k, thinking 1.1k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 73.1k
attempt usage cr1-r70-7-go-r0-haiku-build-a1 anthropic (messages): input 34, cache_read 0.35M, cache_creation 30.3k, output 18.4k, thinking 7.4k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 30.3k
attempt usage cr1-r70-7-go-r0-haiku-build-a1 openai (responses): input 56.2k, cached 0, output 405, reasoning 60, input_tokens_details.cache_write_tokens 0, total_tokens 56.6k
attempt usage cr1-r70-7-go-r0-luna-medium-build-a1 openai (responses): input 0.21M, cached 33.2k, output 5.2k, reasoning 298, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage cr1-r70-7-go-r0-sol-low-a1 openai (responses): input 0.45M, cached 70.8k, output 8.9k, reasoning 315, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
attempt usage cr1-r70-7-go-r0-sonnet-review-a1 anthropic (messages): input 12, cache_read 0, cache_creation 69.5k, output 2.6k, thinking 1.6k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 69.5k
attempt usage cr1-r70-7-go-r0-sonnet-review-a1 openai (responses): input 0.11M, cached 26.2k, output 3.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage cr1-sched-go-r0-all-sonnet-a1 anthropic (messages): input 18, cache_read 46.9k, cache_creation 50.2k, output 7.9k, thinking 669, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 50.2k
attempt usage cr1-sched-go-r0-haiku-build-a1 anthropic (messages): input 18, cache_read 0.14M, cache_creation 28.2k, output 17.3k, thinking 9.5k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 28.2k
attempt usage cr1-sched-go-r0-haiku-build-a1 openai (responses): input 61.8k, cached 0, output 416, reasoning 139, input_tokens_details.cache_write_tokens 0, total_tokens 62.2k
attempt usage cr1-sched-go-r0-luna-medium-build-a1 openai (responses): input 0.22M, cached 5.6k, output 4.6k, reasoning 112, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage cr1-sched-go-r0-sol-low-a1 openai (responses): input 0.55M, cached 0.17M, output 8.0k, reasoning 270, input_tokens_details.cache_write_tokens 0, total_tokens 0.56M
attempt usage cr1-sched-go-r0-sonnet-review-a1 anthropic (messages): input 16, cache_read 0, cache_creation 98.3k, output 3.2k, thinking 2.0k, cache_creation.ephemeral_1h_input_tokens 0, cache_creation.ephemeral_5m_input_tokens 98.3k
attempt usage cr1-sched-go-r0-sonnet-review-a1 openai (responses): input 0.28M, cached 0.11M, output 6.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt outcomes included: sol-low: correct 6, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; sonnet-review: correct 5, incorrect 2, workflow failure 0, infrastructure 0, incomplete 0; haiku-build: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; luna-medium-build: correct 6, incorrect 0, workflow failure 1, infrastructure 0, incomplete 0; all-sonnet: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 20559.4s, model 19606.1s, tools/checks 953.3s, requests 833
builder settings: sol-low openai gpt-6-luna reasoning.effort=low
builder settings: sonnet-review openai gpt-6-luna reasoning.effort=low
builder settings: haiku-build anthropic claude-haiku-5-5 output_config.effort=medium, thinking adaptive (not equivalent)
builder settings: luna-medium-build openai gpt-6-luna reasoning.effort=medium (not equivalent)
builder settings: all-sonnet anthropic claude-sonnet-5-5 output_config.effort=medium, thinking adaptive (not equivalent)
## CMP-3 Counts and exposure
planned 35, started 35, scored 35, incorrect 2, infrastructure 0, incomplete 0
variant sonnet-review differs from sol-low in:
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
variant haiku-build differs from sol-low in:
  roles.builder: openai gpt-6-luna low -> anthropic claude-haiku-5-5 medium
  roles.builder: openai gpt-6-luna low -> anthropic claude-haiku-5-5 medium
  roles.builder: openai gpt-6-luna low -> anthropic claude-haiku-5-5 medium
variant luna-medium-build differs from sol-low in:
  roles.builder: openai gpt-6-luna low -> openai gpt-6-luna medium
variant all-sonnet differs from sol-low in:
  roles.builder: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.builder: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.builder: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.planner: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.planner: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.planner: openai gpt-6-luna low -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
  roles.reviewer: openai gpt-6.1-sol low -> anthropic claude-sonnet-5-5 medium
roles.reviewer.effort: exercised in 7 of 7 sonnet-review attempts
roles.reviewer.model: exercised in 7 of 7 sonnet-review attempts
roles.reviewer.provider: exercised in 7 of 7 sonnet-review attempts
roles.builder.effort: exercised in 7 of 7 haiku-build attempts
roles.builder.model: exercised in 7 of 7 haiku-build attempts
roles.builder.provider: exercised in 7 of 7 haiku-build attempts
roles.builder.effort: exercised in 7 of 7 luna-medium-build attempts
roles.builder.effort: exercised in 7 of 7 all-sonnet attempts
roles.builder.model: exercised in 7 of 7 all-sonnet attempts
roles.builder.provider: exercised in 7 of 7 all-sonnet attempts
roles.planner.effort: exercised in 7 of 7 all-sonnet attempts
roles.planner.model: exercised in 7 of 7 all-sonnet attempts
roles.planner.provider: exercised in 7 of 7 all-sonnet attempts
roles.reviewer.effort: exercised in 7 of 7 all-sonnet attempts
roles.reviewer.model: exercised in 7 of 7 all-sonnet attempts
roles.reviewer.provider: exercised in 7 of 7 all-sonnet attempts
first position per task: env-ex sol-low 0, sonnet-review 0, haiku-build 1, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
first position per task: env-go sol-low 0, sonnet-review 1, haiku-build 0, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
first position per task: r70-5-elixir sol-low 0, sonnet-review 0, haiku-build 1, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
first position per task: r70-5-go sol-low 0, sonnet-review 0, haiku-build 0, luna-medium-build 0, all-sonnet 1 (1 repetitions, 5 variants)
first position per task: r70-7-elixir sol-low 0, sonnet-review 0, haiku-build 1, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
first position per task: r70-7-go sol-low 1, sonnet-review 0, haiku-build 0, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
first position per task: sched-go sol-low 0, sonnet-review 0, haiku-build 1, luna-medium-build 0, all-sonnet 0 (1 repetitions, 5 variants)
sol-low: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
sonnet-review: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
haiku-build: not the Kogen profile (differs in roles.builder.model, roles.builder.provider, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
luna-medium-build: not the Kogen profile (differs in roles.builder.model, roles.planner.effort, roles.planner.model, roles.reviewer.effort, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
all-sonnet: not the Kogen profile (differs in roles.builder.model, roles.builder.provider, roles.planner.model, roles.planner.provider, roles.reviewer.effort, roles.reviewer.model, roles.reviewer.provider, roles.shaper.effort, roles.shaper.model, stop.max_repairs, stop.max_tokens)
experimental stop: every variant has stop.max_repairs = 6, stop.max_tokens = 100000; no variant matches the Kogen profile configuration
sol-low: repair.context = packet,diff,check_results,review_findings (extension)
sol-low: repair.roles = builder (extension)
sol-low: shape.critique_prompt = lab:critique (extension)
sol-low: shape.critique_rounds = 1 (extension)
sonnet-review: repair.context = packet,diff,check_results,review_findings (extension)
sonnet-review: repair.roles = builder (extension)
sonnet-review: shape.critique_prompt = lab:critique (extension)
sonnet-review: shape.critique_rounds = 1 (extension)
haiku-build: repair.context = packet,diff,check_results,review_findings (extension)
haiku-build: repair.roles = builder (extension)
haiku-build: shape.critique_prompt = lab:critique (extension)
haiku-build: shape.critique_rounds = 1 (extension)
luna-medium-build: repair.context = packet,diff,check_results,review_findings (extension)
luna-medium-build: repair.roles = builder (extension)
luna-medium-build: shape.critique_prompt = lab:critique (extension)
luna-medium-build: shape.critique_rounds = 1 (extension)
all-sonnet: repair.context = packet,diff,check_results,review_findings (extension)
all-sonnet: repair.roles = builder (extension)
all-sonnet: shape.critique_prompt = lab:critique (extension)
all-sonnet: shape.critique_rounds = 1 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
