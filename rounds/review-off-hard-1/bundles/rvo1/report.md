complete: 16/16 cells scored
Question: review-off-hard-1: on hard tasks, does Kogen's default Sol-medium builder send wrong code to review often enough that the Sol-high reviewer-fixer is needed, or could review be turned off for it?
Hypothesis: exploratory: some first-green builds are wrong on these tasks; review rescues some of them
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant    | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| review-on  | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
| review-off | 8       | 0         | 0                | 0              | 0          | 100%         | 0 of 8        | 0           |
false success: 0 of 8 claims (review-on)
false success: 0 of 8 claims (review-off)
shaping outcomes:
review-on: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
review-off: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task    | variant    | correct | incorrect | workflow failure | infrastructure | incomplete |
|---------|------------|---------|-----------|------------------|----------------|------------|
| cron-ex | review-on  | 2       | 0         | 0                | 0              | 0          |
| cron-ex | review-off | 2       | 0         | 0                | 0              | 0          |
| cron-go | review-on  | 2       | 0         | 0                | 0              | 0          |
| cron-go | review-off | 2       | 0         | 0                | 0              | 0          |
| vm-ex   | review-on  | 2       | 0         | 0                | 0              | 0          |
| vm-ex   | review-off | 2       | 0         | 0                | 0              | 0          |
| vm-go   | review-on  | 2       | 0         | 0                | 0              | 0          |
| vm-go   | review-off | 2       | 0         | 0                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant    | stage      | wall    | model   | tools/checks | requests |
|------------|------------|---------|---------|--------------|----------|
| review-on  | shape      | 0ms     | 0ms     | 0ms          | 0        |
| review-on  | plan       | 0ms     | 0ms     | 0ms          | 0        |
| review-on  | build      | 2191.9s | 2109.7s | 82.2s        | 79       |
| review-on  | verify     | 25.8s   | 0ms     | 25.8s        | 0        |
| review-on  | review     | 1244.3s | 1244.3s | 0ms          | 53       |
| review-on  | commit     | 0ms     | 0ms     | 0ms          | 0        |
| review-on  | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| review-on  | assessment | 0ms     | 0ms     | 0ms          | 0        |
| review-off | shape      | 0ms     | 0ms     | 0ms          | 0        |
| review-off | plan       | 0ms     | 0ms     | 0ms          | 0        |
| review-off | build      | 2516s   | 2439.6s | 76.3s        | 81       |
| review-off | verify     | 36s     | 0ms     | 36s          | 0        |
| review-off | review     | 0ms     | 0ms     | 0ms          | 0        |
| review-off | commit     | 0ms     | 0ms     | 0ms          | 0        |
| review-off | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| review-off | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                       | outcome | wall   | model  | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-------------------------------|---------|--------|--------|--------------|----------|---------|---------|-----------|----------------------|
| rvo1-cron-ex-r0-review-off-a1 | correct | 331.5s | 317.2s | 14.4s        | 10       | 0       | 0       | 0         | 0                    |
| rvo1-cron-ex-r0-review-on-a1  | correct | 292.3s | 274.7s | 17.6s        | 12       | 0       | 1       | 0         | 0                    |
| rvo1-cron-ex-r1-review-off-a1 | correct | 157s   | 136s   | 21s          | 7        | 0       | 0       | 0         | 0                    |
| rvo1-cron-ex-r1-review-on-a1  | correct | 363s   | 345.3s | 17.7s        | 19       | 0       | 1       | 0         | 0                    |
| rvo1-cron-go-r0-review-off-a1 | correct | 324.9s | 315.1s | 9.8s         | 11       | 0       | 0       | 0         | 0                    |
| rvo1-cron-go-r0-review-on-a1  | correct | 698.8s | 686.5s | 12.3s        | 18       | 0       | 1       | 0         | 0                    |
| rvo1-cron-go-r1-review-off-a1 | correct | 297.8s | 287.8s | 10s          | 8        | 0       | 0       | 0         | 0                    |
| rvo1-cron-go-r1-review-on-a1  | correct | 340.1s | 324.9s | 15.2s        | 14       | 0       | 1       | 0         | 0                    |
| rvo1-vm-ex-r0-review-off-a1   | correct | 419.4s | 392.1s | 27.3s        | 13       | 1       | 0       | 0         | 0                    |
| rvo1-vm-ex-r0-review-on-a1    | correct | 513s   | 490.6s | 22.5s        | 18       | 0       | 1       | 0         | 0                    |
| rvo1-vm-ex-r1-review-off-a1   | correct | 409.8s | 372.8s | 37s          | 12       | 0       | 0       | 0         | 0                    |
| rvo1-vm-ex-r1-review-on-a1    | correct | 460.7s | 441.2s | 19.5s        | 18       | 0       | 1       | 0         | 0                    |
| rvo1-vm-go-r0-review-off-a1   | correct | 290.9s | 280.7s | 10.2s        | 9        | 0       | 0       | 0         | 0                    |
| rvo1-vm-go-r0-review-on-a1    | correct | 387.4s | 371.7s | 15.7s        | 16       | 0       | 1       | 0         | 0                    |
| rvo1-vm-go-r1-review-off-a1   | correct | 356.2s | 338s   | 18.2s        | 11       | 0       | 0       | 0         | 0                    |
| rvo1-vm-go-r1-review-on-a1    | correct | 442s   | 418.9s | 23.1s        | 17       | 0       | 1       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
review-off openai: input 1.01M, cached 0.13M, output 55.1k, reasoning 4.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
review-on openai: input 2.11M, cached 0.10M, output 76.8k, reasoning 15.4k, input_tokens_details.cache_write_tokens 0, total_tokens 2.19M
native usage by stage and provider:
stage build review-off openai (responses): input 1.01M, cached 0.13M, output 55.1k, reasoning 4.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
stage build review-on openai (responses): input 0.98M, cached 87.6k, output 55.8k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.03M
stage review review-on openai (responses): input 1.13M, cached 16.4k, output 21.0k, reasoning 11.2k, input_tokens_details.cache_write_tokens 0, total_tokens 1.15M
native usage by attempt and provider:
attempt usage rvo1-cron-ex-r0-review-off-a1 openai (responses): input 0.11M, cached 0, output 6.2k, reasoning 612, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt usage rvo1-cron-ex-r0-review-on-a1 openai (responses): input 0.20M, cached 6.9k, output 8.8k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rvo1-cron-ex-r1-review-off-a1 openai (responses): input 77.7k, cached 30.5k, output 5.2k, reasoning 255, input_tokens_details.cache_write_tokens 0, total_tokens 82.9k
attempt usage rvo1-cron-ex-r1-review-on-a1 openai (responses): input 0.33M, cached 20.7k, output 9.6k, reasoning 1.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage rvo1-cron-go-r0-review-off-a1 openai (responses): input 0.13M, cached 13.8k, output 6.1k, reasoning 471, input_tokens_details.cache_write_tokens 0, total_tokens 0.14M
attempt usage rvo1-cron-go-r0-review-on-a1 openai (responses): input 0.33M, cached 0, output 10.8k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.34M
attempt usage rvo1-cron-go-r1-review-off-a1 openai (responses): input 93.4k, cached 17.5k, output 6.3k, reasoning 271, input_tokens_details.cache_write_tokens 0, total_tokens 99.7k
attempt usage rvo1-cron-go-r1-review-on-a1 openai (responses): input 0.23M, cached 6.9k, output 10.5k, reasoning 2.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage rvo1-vm-ex-r0-review-off-a1 openai (responses): input 0.19M, cached 26.1k, output 9.2k, reasoning 1.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage rvo1-vm-ex-r0-review-on-a1 openai (responses): input 0.25M, cached 22.9k, output 8.7k, reasoning 1.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rvo1-vm-ex-r1-review-off-a1 openai (responses): input 0.15M, cached 6.5k, output 7.5k, reasoning 600, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rvo1-vm-ex-r1-review-on-a1 openai (responses): input 0.26M, cached 13.1k, output 8.8k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.27M
attempt usage rvo1-vm-go-r0-review-off-a1 openai (responses): input 0.10M, cached 32.6k, output 6.6k, reasoning 448, input_tokens_details.cache_write_tokens 0, total_tokens 0.11M
attempt usage rvo1-vm-go-r0-review-on-a1 openai (responses): input 0.25M, cached 13.8k, output 9.3k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage rvo1-vm-go-r1-review-off-a1 openai (responses): input 0.15M, cached 6.5k, output 7.9k, reasoning 551, input_tokens_details.cache_write_tokens 0, total_tokens 0.16M
attempt usage rvo1-vm-go-r1-review-on-a1 openai (responses): input 0.27M, cached 19.6k, output 10.3k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt outcomes included: review-on: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; review-off: correct 8, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 6085s, model 5793.6s, tools/checks 291.4s, requests 213
builder settings: review-on openai gpt-6.1-sol reasoning.effort=medium; review-off openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 16, started 16, scored 16, incorrect 0, infrastructure 0, incomplete 0
variant review-off differs from review-on in:
  review.enabled: true -> false
C01: exercised in 8 of 8 review-off attempts
first position per task: cron-ex review-on 1, review-off 1 (2 repetitions, 2 variants)
first position per task: cron-go review-on 1, review-off 1 (2 repetitions, 2 variants)
first position per task: vm-ex review-on 1, review-off 1 (2 repetitions, 2 variants)
first position per task: vm-go review-on 1, review-off 1 (2 repetitions, 2 variants)
review-on: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
review-off: not the Kogen profile (differs in review.enabled, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
review-on: build.helper_context = lab_helper (extension)
review-on: build.helper_prompt = lab:helper (extension)
review-on: build.subagents_output = 4096 (extension)
review-on: build.subagents_turns = 10 (extension)
review-on: plan.context = kogen_planner (extension)
review-on: plan.prompt = lab:plan (extension)
review-on: repair.context = packet,diff,check_results,review_findings (extension)
review-on: repair.roles = builder (extension)
review-on: review.timing = every_green (extension)
review-on: shape.critique_prompt = lab:critique (extension)
review-on: shape.critique_rounds = 1 (extension)
review-on: shape.helper_context = lab_helper (extension)
review-on: shape.helper_prompt = lab:helper (extension)
review-on: shape.subagents_output = 4096 (extension)
review-on: shape.subagents_turns = 10 (extension)
review-off: build.helper_context = lab_helper (extension)
review-off: build.helper_prompt = lab:helper (extension)
review-off: build.subagents_output = 4096 (extension)
review-off: build.subagents_turns = 10 (extension)
review-off: plan.context = kogen_planner (extension)
review-off: plan.prompt = lab:plan (extension)
review-off: repair.context = packet,diff,check_results,review_findings (extension)
review-off: repair.roles = builder (extension)
review-off: review.timing = every_green (extension)
review-off: shape.critique_prompt = lab:critique (extension)
review-off: shape.critique_rounds = 1 (extension)
review-off: shape.helper_context = lab_helper (extension)
review-off: shape.helper_prompt = lab:helper (extension)
review-off: shape.subagents_output = 4096 (extension)
review-off: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
