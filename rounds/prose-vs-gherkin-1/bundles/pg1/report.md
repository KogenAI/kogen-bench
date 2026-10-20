complete: 20/20 cells scored
Question: prose-vs-gherkin-1: with Kogen b45ba32b's default roles and flow, how often does wrong code reach review or ship when the supplied specification is prose only instead of prose plus Gherkin scenarios?
Hypothesis: exploratory: prose-only specifications let some green-but-wrong code reach review (claude-review-fix-1); Kogen's reviewer-fixer catches part of it
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|---------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| gherkin | 10      | 0         | 0                | 0              | 1          | 100%         | 0 of 10       | 0           |
| prose   | 8       | 2         | 0                | 0              | 1          | 80%          | 2 of 10       | 0           |
false success: 0 of 10 claims (gherkin)
false success: 2 of 10 claims (prose)
shaping outcomes:
gherkin: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
prose: supplied artifacts (prose): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|---------|---------|-----------|------------------|----------------|------------|
| artifact-go    | gherkin | 2       | 0         | 0                | 0              | 0          |
| artifact-go    | prose   | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | gherkin | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | prose   | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | gherkin | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | prose   | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | gherkin | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | prose   | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | gherkin | 2       | 0         | 0                | 0              | 1          |
| r70-6-elixir-2 | prose   | 0       | 2         | 0                | 0              | 1          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant | stage      | wall    | model   | tools/checks | requests |
|---------|------------|---------|---------|--------------|----------|
| gherkin | shape      | 0ms     | 0ms     | 0ms          | 0        |
| gherkin | plan       | 0ms     | 0ms     | 0ms          | 0        |
| gherkin | build      | 2294.4s | 2183.9s | 110.5s       | 82       |
| gherkin | verify     | 23.4s   | 0ms     | 23.4s        | 0        |
| gherkin | review     | 2793.3s | 2793.3s | 0ms          | 86       |
| gherkin | commit     | 0ms     | 0ms     | 0ms          | 0        |
| gherkin | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| gherkin | assessment | 0ms     | 0ms     | 0ms          | 0        |
| prose   | shape      | 0ms     | 0ms     | 0ms          | 0        |
| prose   | plan       | 0ms     | 0ms     | 0ms          | 0        |
| prose   | build      | 3146.9s | 2943.6s | 203.3s       | 122      |
| prose   | verify     | 75.3s   | 0ms     | 75.3s        | 0        |
| prose   | review     | 1849.5s | 1849.5s | 0ms          | 61       |
| prose   | commit     | 0ms     | 0ms     | 0ms          | 0        |
| prose   | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| prose   | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                          | outcome    | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|----------------------------------|------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| pg1-artifact-go-r0-gherkin-a1    | correct    | 154.3s  | 141.8s  | 12.4s        | 10       | 0       | 1       | 0         | 0                    |
| pg1-artifact-go-r0-prose-a1      | correct    | 247.4s  | 238s    | 9.4s         | 13       | 0       | 1       | 0         | 0                    |
| pg1-artifact-go-r1-gherkin-a1    | correct    | 186.6s  | 174.7s  | 11.9s        | 8        | 0       | 1       | 0         | 0                    |
| pg1-artifact-go-r1-prose-a1      | correct    | 204.7s  | 193.6s  | 11.1s        | 14       | 0       | 1       | 0         | 0                    |
| pg1-r70-1-go-r0-gherkin-a1       | correct    | 1041.1s | 1010s   | 31.1s        | 26       | 0       | 1       | 0         | 0                    |
| pg1-r70-1-go-r0-prose-a1         | correct    | 716.1s  | 697.4s  | 18.7s        | 17       | 0       | 1       | 0         | 0                    |
| pg1-r70-1-go-r1-gherkin-a1       | correct    | 1059.7s | 1028.3s | 31.4s        | 23       | 0       | 1       | 0         | 0                    |
| pg1-r70-1-go-r1-prose-a1         | correct    | 833s    | 813.1s  | 20s          | 18       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-elixir-2-r0-gherkin-a1 | correct    | 551.7s  | 530.6s  | 21.1s        | 17       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-elixir-2-r0-prose-a1   | correct    | 573.7s  | 517.2s  | 56.6s        | 18       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-elixir-2-r1-gherkin-a1 | correct    | 464.2s  | 440.7s  | 23.5s        | 17       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-elixir-2-r1-prose-a1   | correct    | 555.5s  | 496.6s  | 59s          | 20       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-go-r0-gherkin-a1       | correct    | 545s    | 530.2s  | 14.8s        | 19       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-go-r0-prose-a1         | correct    | 386.9s  | 371.2s  | 15.7s        | 14       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-go-r1-gherkin-a1       | correct    | 615.4s  | 602.3s  | 13.1s        | 20       | 0       | 1       | 0         | 0                    |
| pg1-r70-4-go-r1-prose-a1         | correct    | 560.8s  | 535.6s  | 25.2s        | 20       | 1       | 2       | 0         | 0                    |
| pg1-r70-6-elixir-2-r0-gherkin-a1 | correct    | 264.8s  | 254.9s  | 9.8s         | 13       | 0       | 1       | 0         | 0                    |
| pg1-r70-6-elixir-2-r0-prose-a1   | incomplete | 294.1s  | 256.5s  | 37.6s        | 11       | 0       | 0       | 0         | 0                    |
| pg1-r70-6-elixir-2-r0-prose-a2   | incorrect  | 368.5s  | 328.6s  | 39.9s        | 19       | 0       | 1       | 0         | 0                    |
| pg1-r70-6-elixir-2-r1-gherkin-a1 | incomplete | 3.6s    | 0ms     | 3.6s         | 0        | 0       | 0       | 0         | 0                    |
| pg1-r70-6-elixir-2-r1-gherkin-a2 | correct    | 280.4s  | 263.6s  | 16.8s        | 15       | 0       | 1       | 0         | 0                    |
| pg1-r70-6-elixir-2-r1-prose-a1   | incorrect  | 386.4s  | 345.4s  | 41s          | 19       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
gherkin openai: input 2.67M, cached 0.24M, output 0.10M, reasoning 42.3k, input_tokens_details.cache_write_tokens 0, total_tokens 2.77M
prose openai: input 1.92M, cached 0.11M, output 95.1k, reasoning 29.7k, input_tokens_details.cache_write_tokens 0, total_tokens 2.02M
native usage by stage and provider:
stage build gherkin openai (responses): input 0.76M, cached 0.17M, output 35.5k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.79M
stage build prose openai (responses): input 0.99M, cached 89.6k, output 58.0k, reasoning 6.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.05M
stage review gherkin openai (responses): input 1.92M, cached 75.3k, output 65.3k, reasoning 38.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.98M
stage review prose openai (responses): input 0.93M, cached 23.6k, output 37.1k, reasoning 22.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.97M
native usage by attempt and provider:
attempt usage pg1-artifact-go-r0-gherkin-a1 openai (responses): input 94.4k, cached 0, output 4.1k, reasoning 222, input_tokens_details.cache_write_tokens 0, total_tokens 98.5k
attempt usage pg1-artifact-go-r0-prose-a1 openai (responses): input 0.10M, cached 8.1k, output 4.3k, reasoning 619, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage pg1-artifact-go-r1-gherkin-a1 openai (responses): input 76.1k, cached 0, output 3.7k, reasoning 273, input_tokens_details.cache_write_tokens 0, total_tokens 79.8k
attempt usage pg1-artifact-go-r1-prose-a1 openai (responses): input 0.11M, cached 3.8k, output 4.6k, reasoning 389, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage pg1-r70-1-go-r0-gherkin-a1 openai (responses): input 0.69M, cached 46.0k, output 23.3k, reasoning 11.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
attempt usage pg1-r70-1-go-r0-prose-a1 openai (responses): input 0.22M, cached 5.0k, output 14.5k, reasoning 6.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage pg1-r70-1-go-r1-gherkin-a1 openai (responses): input 0.53M, cached 57.7k, output 24.4k, reasoning 13.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.55M
attempt usage pg1-r70-1-go-r1-prose-a1 openai (responses): input 0.25M, cached 10.8k, output 13.6k, reasoning 4.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage pg1-r70-4-elixir-2-r0-gherkin-a1 openai (responses): input 0.21M, cached 20.5k, output 7.4k, reasoning 3.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage pg1-r70-4-elixir-2-r0-prose-a1 openai (responses): input 0.18M, cached 29.2k, output 10.6k, reasoning 4.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage pg1-r70-4-elixir-2-r1-gherkin-a1 openai (responses): input 0.23M, cached 38.1k, output 8.9k, reasoning 4.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage pg1-r70-4-elixir-2-r1-prose-a1 openai (responses): input 0.22M, cached 11.0k, output 11.2k, reasoning 4.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage pg1-r70-4-go-r0-gherkin-a1 openai (responses): input 0.25M, cached 19.2k, output 9.2k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage pg1-r70-4-go-r0-prose-a1 openai (responses): input 0.14M, cached 3.7k, output 8.0k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.15M
attempt usage pg1-r70-4-go-r1-gherkin-a1 openai (responses): input 0.28M, cached 0, output 10.9k, reasoning 4.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage pg1-r70-4-go-r1-prose-a1 openai (responses): input 0.22M, cached 12.5k, output 9.4k, reasoning 3.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage pg1-r70-6-elixir-2-r0-gherkin-a1 openai (responses): input 0.15M, cached 21.6k, output 4.4k, reasoning 656, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage pg1-r70-6-elixir-2-r0-prose-a1 openai (responses): input 97.9k, cached 0, output 4.8k, reasoning 327, input_tokens_details.cache_write_tokens 0, total_tokens 0.10M
attempt usage pg1-r70-6-elixir-2-r0-prose-a2 openai (responses): input 0.18M, cached 4.1k, output 6.8k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage pg1-r70-6-elixir-2-r1-gherkin-a2 openai (responses): input 0.16M, cached 39.7k, output 4.5k, reasoning 885, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage pg1-r70-6-elixir-2-r1-prose-a1 openai (responses): input 0.20M, cached 25.0k, output 7.4k, reasoning 1.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt outcomes included: gherkin: correct 10, incorrect 0, workflow failure 0, infrastructure 0, incomplete 1; prose: correct 8, incorrect 2, workflow failure 0, infrastructure 0, incomplete 1
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 10294.1s, model 9770.4s, tools/checks 523.7s, requests 351
builder settings: gherkin openai gpt-6.1-sol reasoning.effort=medium; prose openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 20, started 22, scored 20, incorrect 2, infrastructure 0, incomplete 2
variant prose differs from gherkin in:
  artifacts.gherkin: executed -> off
  shape.supplied: gherkin -> prose
A03: exercised in 11 of 11 prose attempts
MODE: exercised in 11 of 11 prose attempts
first position per task: artifact-go gherkin 1, prose 1 (2 repetitions, 2 variants)
first position per task: r70-1-go gherkin 1, prose 1 (2 repetitions, 2 variants)
first position per task: r70-4-elixir-2 gherkin 1, prose 1 (2 repetitions, 2 variants)
first position per task: r70-4-go gherkin 1, prose 1 (2 repetitions, 2 variants)
first position per task: r70-6-elixir-2 gherkin 1, prose 1 (2 repetitions, 2 variants)
gherkin: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
prose: not the Kogen profile (differs in artifacts.gherkin, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
gherkin: build.helper_context = lab_helper (extension)
gherkin: build.helper_prompt = lab:helper (extension)
gherkin: build.subagents_output = 4096 (extension)
gherkin: build.subagents_turns = 10 (extension)
gherkin: plan.context = kogen_planner (extension)
gherkin: plan.prompt = lab:plan (extension)
gherkin: repair.context = packet,diff,check_results,review_findings (extension)
gherkin: repair.roles = builder (extension)
gherkin: review.timing = every_green (extension)
gherkin: shape.critique_prompt = lab:critique (extension)
gherkin: shape.critique_rounds = 1 (extension)
gherkin: shape.helper_context = lab_helper (extension)
gherkin: shape.helper_prompt = lab:helper (extension)
gherkin: shape.subagents_output = 4096 (extension)
gherkin: shape.subagents_turns = 10 (extension)
prose: build.helper_context = lab_helper (extension)
prose: build.helper_prompt = lab:helper (extension)
prose: build.subagents_output = 4096 (extension)
prose: build.subagents_turns = 10 (extension)
prose: plan.context = kogen_planner (extension)
prose: plan.prompt = lab:plan (extension)
prose: repair.context = packet,diff,check_results,review_findings (extension)
prose: repair.roles = builder (extension)
prose: review.timing = every_green (extension)
prose: shape.critique_prompt = lab:critique (extension)
prose: shape.critique_rounds = 1 (extension)
prose: shape.helper_context = lab_helper (extension)
prose: shape.helper_prompt = lab:helper (extension)
prose: shape.subagents_output = 4096 (extension)
prose: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
