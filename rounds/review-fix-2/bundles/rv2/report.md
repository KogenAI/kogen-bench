complete: 16/16 cells scored
Question: review-fix-2: does Kogen b45ba32b's flow (review-and-fix, no planner, stop at first failed gate) keep correctness against the earlier flow (builder repairs on review findings, planner, run all checks), and at what cost?
Hypothesis: exploratory: the new flow matches the old at lower cost; with a weak builder the reviewer-fixer may rescue attempts the old loop loses
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none (descriptive)
## CMP-1 Correctness
| variant  | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|----------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| new      | 4       | 0         | 0                | 1              | 0          | 100%         | 0 of 4        | 0           |
| old      | 4       | 0         | 0                | 1              | 1          | 100%         | 0 of 4        | 0           |
| weak-new | 4       | 0         | 0                | 1              | 0          | 100%         | 0 of 4        | 0           |
| weak-old | 0       | 0         | 4                | 0              | 0          | 0%           | 0 of 0        | 1           |
false success: 0 of 4 claims (new)
false success: 0 of 4 claims (old)
false success: 0 of 4 claims (weak-new)
false success: 0 of 0 claims (weak-old)
shaping outcomes:
new: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
old: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
weak-new: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
weak-old: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant  | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|----------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | new      | 1       | 0         | 0                | 0              | 0          |
| r70-1-go       | old      | 1       | 0         | 0                | 1              | 1          |
| r70-1-go       | weak-new | 1       | 0         | 0                | 1              | 0          |
| r70-1-go       | weak-old | 0       | 0         | 1                | 0              | 0          |
| r70-4-elixir-2 | new      | 1       | 0         | 0                | 1              | 0          |
| r70-4-elixir-2 | old      | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | weak-new | 1       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | weak-old | 0       | 0         | 1                | 0              | 0          |
| r70-4-go       | new      | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | old      | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | weak-new | 1       | 0         | 0                | 0              | 0          |
| r70-4-go       | weak-old | 0       | 0         | 1                | 0              | 0          |
| r70-6-elixir-2 | new      | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | old      | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | weak-new | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | weak-old | 0       | 0         | 1                | 0              | 0          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant  | stage      | wall    | model   | tools/checks | requests |
|----------|------------|---------|---------|--------------|----------|
| new      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| new      | plan       | 0ms     | 0ms     | 0ms          | 0        |
| new      | build      | 787.4s  | 723.7s  | 63.7s        | 42       |
| new      | verify     | 11.3s   | 0ms     | 11.3s        | 0        |
| new      | review     | 1165.5s | 1165.5s | 0ms          | 43       |
| new      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| new      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| new      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| old      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| old      | plan       | 80.4s   | 80.4s   | 0ms          | 6        |
| old      | build      | 2041.7s | 1959.9s | 81.8s        | 119      |
| old      | verify     | 24.9s   | 0ms     | 24.9s        | 0        |
| old      | review     | 908.4s  | 908.4s  | 0ms          | 42       |
| old      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| old      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| old      | assessment | 0ms     | 0ms     | 0ms          | 0        |
| weak-new | shape      | 0ms     | 0ms     | 0ms          | 0        |
| weak-new | plan       | 0ms     | 0ms     | 0ms          | 0        |
| weak-new | build      | 909.9s  | 786s    | 123.9s       | 69       |
| weak-new | verify     | 17.5s   | 0ms     | 17.5s        | 0        |
| weak-new | review     | 1557.8s | 1557.8s | 0ms          | 58       |
| weak-new | commit     | 0ms     | 0ms     | 0ms          | 0        |
| weak-new | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| weak-new | assessment | 0ms     | 0ms     | 0ms          | 0        |
| weak-old | shape      | 0ms     | 0ms     | 0ms          | 0        |
| weak-old | plan       | 54.6s   | 54.6s   | 0ms          | 4        |
| weak-old | build      | 1620.8s | 1579.4s | 41.3s        | 135      |
| weak-old | verify     | 36.6s   | 0ms     | 36.6s        | 0        |
| weak-old | review     | 1077.4s | 1077.4s | 0ms          | 55       |
| weak-old | commit     | 0ms     | 0ms     | 0ms          | 0        |
| weak-old | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| weak-old | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                           | outcome          | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|-----------------------------------|------------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| rv2-r70-1-go-r0-new-a1            | correct          | 588.5s  | 557.2s  | 31.3s        | 25       | 0       | 1       | 0         | 0                    |
| rv2-r70-1-go-r0-old-a1            | incomplete       | 581.8s  | 564.1s  | 17.7s        | 31       | 2       | 2       | 0         | 0                    |
| rv2-r70-1-go-r0-old-a2            | infrastructure   | 302.2s  | 283.6s  | 18.6s        | 17       | 1       | 1       | 0         | 0                    |
| rv2-r70-1-go-r0-old-a3            | correct          | 1132.4s | 1079.2s | 53.2s        | 51       | 4       | 5       | 0         | 0                    |
| rv2-r70-1-go-r0-weak-new-a1       | infrastructure   | 97.3s   | 84.8s   | 12.5s        | 8        | 0       | 0       | 0         | 0                    |
| rv2-r70-1-go-r0-weak-new-a2       | correct          | 812.5s  | 790.2s  | 22.3s        | 23       | 0       | 1       | 0         | 0                    |
| rv2-r70-1-go-r0-weak-old-a1       | workflow failure | 543.9s  | 530.6s  | 13.3s        | 46       | 6       | 3       | 0         | 0                    |
| rv2-r70-4-elixir-2-r0-new-a1      | infrastructure   | 54.8s   | 44.2s   | 10.5s        | 4        | 0       | 0       | 0         | 0                    |
| rv2-r70-4-elixir-2-r0-new-a2      | correct          | 794.3s  | 768.4s  | 25.8s        | 20       | 0       | 1       | 0         | 0                    |
| rv2-r70-4-elixir-2-r0-old-a1      | correct          | 301.9s  | 282s    | 19.9s        | 19       | 1       | 2       | 0         | 0                    |
| rv2-r70-4-elixir-2-r0-weak-new-a1 | correct          | 863.9s  | 760.1s  | 103.8s       | 45       | 5       | 1       | 0         | 0                    |
| rv2-r70-4-elixir-2-r0-weak-old-a1 | workflow failure | 707.5s  | 671.8s  | 35.6s        | 47       | 6       | 4       | 0         | 0                    |
| rv2-r70-4-go-r0-new-a1            | correct          | 306.8s  | 291s    | 15.7s        | 17       | 0       | 1       | 0         | 0                    |
| rv2-r70-4-go-r0-old-a1            | correct          | 538.4s  | 517.4s  | 21s          | 30       | 3       | 4       | 0         | 0                    |
| rv2-r70-4-go-r0-weak-new-a1       | correct          | 271.5s  | 257.5s  | 14s          | 13       | 0       | 1       | 0         | 0                    |
| rv2-r70-4-go-r0-weak-old-a1       | workflow failure | 628.2s  | 606.6s  | 21.6s        | 44       | 6       | 6       | 0         | 0                    |
| rv2-r70-6-elixir-2-r0-new-a1      | correct          | 247.2s  | 228.3s  | 18.9s        | 19       | 0       | 1       | 0         | 0                    |
| rv2-r70-6-elixir-2-r0-old-a1      | correct          | 238.5s  | 222.5s  | 16.1s        | 19       | 0       | 1       | 0         | 0                    |
| rv2-r70-6-elixir-2-r0-weak-new-a1 | correct          | 476.1s  | 451.2s  | 24.8s        | 38       | 5       | 1       | 0         | 0                    |
| rv2-r70-6-elixir-2-r0-weak-old-a1 | workflow failure | 939.4s  | 902.4s  | 37s          | 57       | 6       | 3       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
new openai: input 1.35M, cached 0.15M, output 52.0k, reasoning 22.9k, input_tokens_details.cache_write_tokens 0, total_tokens 1.40M
old openai: input 2.99M, cached 0.40M, output 96.3k, reasoning 39.9k, input_tokens_details.cache_write_tokens 0, total_tokens 3.09M
weak-new openai: input 2.13M, cached 0.33M, output 65.3k, reasoning 20.8k, input_tokens_details.cache_write_tokens 0, total_tokens 2.20M
weak-old openai: input 3.42M, cached 0.95M, output 84.3k, reasoning 23.5k, input_tokens_details.cache_write_tokens 0, total_tokens 3.51M
native usage by stage and provider:
stage build new openai (responses): input 0.40M, cached 85.8k, output 17.6k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.42M
stage build old openai (responses): input 1.93M, cached 0.40M, output 65.4k, reasoning 18.1k, input_tokens_details.cache_write_tokens 0, total_tokens 2.00M
stage build weak-new openai (responses): input 0.91M, cached 0.24M, output 20.4k, reasoning 763, input_tokens_details.cache_write_tokens 0, total_tokens 0.93M
stage build weak-old openai (responses): input 2.43M, cached 0.95M, output 49.8k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 2.48M
stage plan old openai (responses): input 28.6k, cached 0, output 2.4k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 31.0k
stage plan weak-old openai (responses): input 18.8k, cached 0, output 1.5k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 20.3k
stage review new openai (responses): input 0.95M, cached 60.9k, output 34.4k, reasoning 20.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.98M
stage review old openai (responses): input 1.03M, cached 0, output 28.5k, reasoning 21.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.06M
stage review weak-new openai (responses): input 1.22M, cached 88.1k, output 44.9k, reasoning 20.1k, input_tokens_details.cache_write_tokens 0, total_tokens 1.27M
stage review weak-old openai (responses): input 0.98M, cached 0, output 32.9k, reasoning 23.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.01M
native usage by attempt and provider:
attempt usage rv2-r70-1-go-r0-new-a1 openai (responses): input 0.57M, cached 52.2k, output 22.0k, reasoning 10.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.59M
attempt usage rv2-r70-1-go-r0-old-a1 openai (responses): input 0.61M, cached 84.5k, output 20.9k, reasoning 9.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.63M
attempt usage rv2-r70-1-go-r0-old-a2 openai (responses): input 0.22M, cached 33.8k, output 10.7k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage rv2-r70-1-go-r0-old-a3 openai (responses): input 1.19M, cached 0.16M, output 32.5k, reasoning 14.7k, input_tokens_details.cache_write_tokens 0, total_tokens 1.23M
attempt usage rv2-r70-1-go-r0-weak-new-a1 openai (responses): input 60.9k, cached 0, output 2.8k, reasoning 140, input_tokens_details.cache_write_tokens 0, total_tokens 63.7k
attempt usage rv2-r70-1-go-r0-weak-new-a2 openai (responses): input 0.46M, cached 26.6k, output 15.8k, reasoning 6.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.47M
attempt usage rv2-r70-1-go-r0-weak-old-a1 openai (responses): input 0.70M, cached 0.19M, output 17.8k, reasoning 5.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.71M
attempt usage rv2-r70-4-elixir-2-r0-new-a1 openai (responses): input 22.4k, cached 0, output 1.4k, reasoning 199, input_tokens_details.cache_write_tokens 0, total_tokens 23.8k
attempt usage rv2-r70-4-elixir-2-r0-new-a2 openai (responses): input 0.30M, cached 37.6k, output 11.4k, reasoning 5.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.31M
attempt usage rv2-r70-4-elixir-2-r0-old-a1 openai (responses): input 0.25M, cached 31.1k, output 8.3k, reasoning 3.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rv2-r70-4-elixir-2-r0-weak-new-a1 openai (responses): input 0.73M, cached 0.17M, output 23.3k, reasoning 8.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.75M
attempt usage rv2-r70-4-elixir-2-r0-weak-old-a1 openai (responses): input 0.67M, cached 0.13M, output 18.7k, reasoning 6.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
attempt usage rv2-r70-4-go-r0-new-a1 openai (responses): input 0.23M, cached 22.7k, output 10.4k, reasoning 5.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage rv2-r70-4-go-r0-old-a1 openai (responses): input 0.46M, cached 64.1k, output 18.0k, reasoning 8.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.48M
attempt usage rv2-r70-4-go-r0-weak-new-a1 openai (responses): input 0.16M, cached 0, output 10.5k, reasoning 4.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.17M
attempt usage rv2-r70-4-go-r0-weak-old-a1 openai (responses): input 0.62M, cached 77.4k, output 21.2k, reasoning 8.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.64M
attempt usage rv2-r70-6-elixir-2-r0-new-a1 openai (responses): input 0.24M, cached 34.2k, output 6.9k, reasoning 1.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage rv2-r70-6-elixir-2-r0-old-a1 openai (responses): input 0.25M, cached 24.4k, output 5.9k, reasoning 611, input_tokens_details.cache_write_tokens 0, total_tokens 0.26M
attempt usage rv2-r70-6-elixir-2-r0-weak-new-a1 openai (responses): input 0.72M, cached 0.13M, output 13.0k, reasoning 2.0k, input_tokens_details.cache_write_tokens 0, total_tokens 0.74M
attempt usage rv2-r70-6-elixir-2-r0-weak-old-a1 openai (responses): input 1.44M, cached 0.55M, output 26.6k, reasoning 2.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.47M
attempt outcomes included: new: correct 4, incorrect 0, workflow failure 0, infrastructure 1, incomplete 0; old: correct 4, incorrect 0, workflow failure 0, infrastructure 1, incomplete 1; weak-new: correct 4, incorrect 0, workflow failure 0, infrastructure 1, incomplete 0; weak-old: correct 0, incorrect 0, workflow failure 4, infrastructure 0, incomplete 0
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 10427.1s, model 9893.2s, tools/checks 533.9s, requests 573
builder settings: new openai gpt-6.1-sol reasoning.effort=medium; old openai gpt-6.1-sol reasoning.effort=medium; weak-new openai gpt-6-luna reasoning.effort=low (not equivalent); weak-old openai gpt-6-luna reasoning.effort=low (not equivalent)
## CMP-3 Counts and exposure
planned 16, started 20, scored 16, incorrect 0, infrastructure 3, incomplete 1
variant old differs from new in:
  plan.enabled: false -> true
  review.context: kogen_reviewer -> kogen_reviewer_fd0cdcfb
  review.effect: stop -> builder_repair
  review.tools: fix -> read_only
  verify.continue: stop_at_first -> run_all
variant weak-new differs from new in:
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
variant weak-old differs from new in:
  plan.enabled: false -> true
  review.context: kogen_reviewer -> kogen_reviewer_fd0cdcfb
  review.effect: stop -> builder_repair
  review.tools: fix -> read_only
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  roles.builder: openai gpt-6.1-sol medium -> openai gpt-6-luna low
  verify.continue: stop_at_first -> run_all
C03: exercised in 6 of 6 old attempts
review.effect: not exercised
C09: exercised in 6 of 6 old attempts
P01: exercised in 6 of 6 old attempts
V07: exercised in 6 of 6 old attempts
roles.builder.effort: exercised in 5 of 5 weak-new attempts
roles.builder.model: exercised in 5 of 5 weak-new attempts
C03: exercised in 4 of 4 weak-old attempts
review.effect: not exercised
C09: exercised in 4 of 4 weak-old attempts
P01: exercised in 4 of 4 weak-old attempts
V07: exercised in 4 of 4 weak-old attempts
roles.builder.effort: exercised in 4 of 4 weak-old attempts
roles.builder.model: exercised in 4 of 4 weak-old attempts
first position per task: r70-1-go new 0, old 0, weak-new 0, weak-old 1 (1 repetitions, 4 variants)
first position per task: r70-4-elixir-2 new 0, old 0, weak-new 0, weak-old 1 (1 repetitions, 4 variants)
first position per task: r70-4-go new 1, old 0, weak-new 0, weak-old 0 (1 repetitions, 4 variants)
first position per task: r70-6-elixir-2 new 1, old 0, weak-new 0, weak-old 0 (1 repetitions, 4 variants)
new: not the Kogen profile (differs in stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
old: not the Kogen profile (differs in plan.enabled, review.context, review.effect, review.tools, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds, verify.continue)
weak-new: not the Kogen profile (differs in roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds)
weak-old: not the Kogen profile (differs in plan.enabled, review.context, review.effect, review.tools, roles.builder.effort, roles.builder.model, stop.max_command_seconds, stop.max_repairs, stop.max_wall_seconds, verify.continue)
experimental stop: every variant has stop.max_repairs = 6, stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
new: build.helper_context = lab_helper (extension)
new: build.helper_prompt = lab:helper (extension)
new: build.subagents_output = 4096 (extension)
new: build.subagents_turns = 10 (extension)
new: plan.context = kogen_planner (extension)
new: plan.prompt = lab:plan (extension)
new: repair.context = packet,diff,check_results,review_findings (extension)
new: repair.roles = builder (extension)
new: review.timing = every_green (extension)
new: shape.critique_prompt = lab:critique (extension)
new: shape.critique_rounds = 1 (extension)
new: shape.helper_context = lab_helper (extension)
new: shape.helper_prompt = lab:helper (extension)
new: shape.subagents_output = 4096 (extension)
new: shape.subagents_turns = 10 (extension)
old: build.helper_context = lab_helper (extension)
old: build.helper_prompt = lab:helper (extension)
old: build.subagents_output = 4096 (extension)
old: build.subagents_turns = 10 (extension)
old: plan.context = kogen_planner (extension)
old: plan.enabled = true (extension)
old: plan.prompt = lab:plan (extension)
old: repair.context = packet,diff,check_results,review_findings (extension)
old: repair.roles = builder (extension)
old: review.timing = every_green (extension)
old: shape.critique_prompt = lab:critique (extension)
old: shape.critique_rounds = 1 (extension)
old: shape.helper_context = lab_helper (extension)
old: shape.helper_prompt = lab:helper (extension)
old: shape.subagents_output = 4096 (extension)
old: shape.subagents_turns = 10 (extension)
weak-new: build.helper_context = lab_helper (extension)
weak-new: build.helper_prompt = lab:helper (extension)
weak-new: build.subagents_output = 4096 (extension)
weak-new: build.subagents_turns = 10 (extension)
weak-new: plan.context = kogen_planner (extension)
weak-new: plan.prompt = lab:plan (extension)
weak-new: repair.context = packet,diff,check_results,review_findings (extension)
weak-new: repair.roles = builder (extension)
weak-new: review.timing = every_green (extension)
weak-new: shape.critique_prompt = lab:critique (extension)
weak-new: shape.critique_rounds = 1 (extension)
weak-new: shape.helper_context = lab_helper (extension)
weak-new: shape.helper_prompt = lab:helper (extension)
weak-new: shape.subagents_output = 4096 (extension)
weak-new: shape.subagents_turns = 10 (extension)
weak-old: build.helper_context = lab_helper (extension)
weak-old: build.helper_prompt = lab:helper (extension)
weak-old: build.subagents_output = 4096 (extension)
weak-old: build.subagents_turns = 10 (extension)
weak-old: plan.context = kogen_planner (extension)
weak-old: plan.enabled = true (extension)
weak-old: plan.prompt = lab:plan (extension)
weak-old: repair.context = packet,diff,check_results,review_findings (extension)
weak-old: repair.roles = builder (extension)
weak-old: review.timing = every_green (extension)
weak-old: shape.critique_prompt = lab:critique (extension)
weak-old: shape.critique_rounds = 1 (extension)
weak-old: shape.helper_context = lab_helper (extension)
weak-old: shape.helper_prompt = lab:helper (extension)
weak-old: shape.subagents_output = 4096 (extension)
weak-old: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
