incomplete: 19 of 24 cells scored
Question: repeat-screen-1: with Kogen b2c9876b defaults on the harder tasks and two repetitions, does a Sol-medium reviewer-fixer or turning the planner on change correctness, wrong submissions, tokens or time against the defaults?
Hypothesis: exploratory: Sol medium matches Sol high at lower cost (fixer-model-1, review-fix-1); the planner changes little (planner-direct-1/2)
Purpose: development
Objective: correctness
Rule: descriptive
Decision: none yet (19 of 24 cells scored)
## CMP-1 Correctness
| variant         | correct | incorrect | workflow failure | infrastructure | incomplete | correct rate | false success | regressions |
|-----------------|---------|-----------|------------------|----------------|------------|--------------|---------------|-------------|
| defaults        | 6       | 0         | 0                | 0              | 0          | 100%         | 0 of 6        | 0           |
| reviewer-medium | 7       | 0         | 0                | 0              | 0          | 100%         | 0 of 7        | 0           |
| planner-on      | 6       | 0         | 0                | 0              | 2          | 100%         | 0 of 6        | 0           |
false success: 0 of 6 claims (defaults)
false success: 0 of 7 claims (reviewer-medium)
false success: 0 of 6 claims (planner-on)
shaping outcomes:
defaults: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
reviewer-medium: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
planner-on: supplied artifacts (gherkin): representation or builder behavior with supplied artifacts; shaping is not measured
## Per-task outcomes
| task           | variant         | correct | incorrect | workflow failure | infrastructure | incomplete |
|----------------|-----------------|---------|-----------|------------------|----------------|------------|
| r70-1-go       | defaults        | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| r70-1-go       | planner-on      | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | defaults        | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| r70-4-elixir-2 | planner-on      | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | defaults        | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | reviewer-medium | 2       | 0         | 0                | 0              | 0          |
| r70-4-go       | planner-on      | 2       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | defaults        | 0       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | reviewer-medium | 1       | 0         | 0                | 0              | 0          |
| r70-6-elixir-2 | planner-on      | 0       | 0         | 0                | 0              | 2          |
## CMP-2 Resources
per stage: wall, model, tools/checks, requests
| variant         | stage      | wall    | model   | tools/checks | requests |
|-----------------|------------|---------|---------|--------------|----------|
| defaults        | shape      | 0ms     | 0ms     | 0ms          | 0        |
| defaults        | plan       | 0ms     | 0ms     | 0ms          | 0        |
| defaults        | build      | 1883.1s | 1803.1s | 80s          | 47       |
| defaults        | verify     | 21.4s   | 0ms     | 21.4s        | 0        |
| defaults        | review     | 3150.4s | 3150.4s | 0ms          | 65       |
| defaults        | commit     | 0ms     | 0ms     | 0ms          | 0        |
| defaults        | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| defaults        | assessment | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | shape      | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | plan       | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | build      | 2717.8s | 2652.2s | 65.7s        | 63       |
| reviewer-medium | verify     | 18.5s   | 0ms     | 18.5s        | 0        |
| reviewer-medium | review     | 2173.8s | 2173.8s | 0ms          | 42       |
| reviewer-medium | commit     | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| reviewer-medium | assessment | 0ms     | 0ms     | 0ms          | 0        |
| planner-on      | shape      | 0ms     | 0ms     | 0ms          | 0        |
| planner-on      | plan       | 382.7s  | 382.7s  | 0ms          | 8        |
| planner-on      | build      | 3087.9s | 2994.5s | 93.5s        | 70       |
| planner-on      | verify     | 20.5s   | 0ms     | 20.5s        | 0        |
| planner-on      | review     | 2938.1s | 2938.1s | 0ms          | 57       |
| planner-on      | commit     | 0ms     | 0ms     | 0ms          | 0        |
| planner-on      | evaluate   | 0ms     | 0ms     | 0ms          | 0        |
| planner-on      | assessment | 0ms     | 0ms     | 0ms          | 0        |
per attempt: includes failed, interrupted, infrastructure and incomplete attempts; repair, review, question and incomplete-response counts included
| attempt                                  | outcome    | wall    | model   | tools/checks | requests | repairs | reviews | questions | incomplete responses |
|------------------------------------------|------------|---------|---------|--------------|----------|---------|---------|-----------|----------------------|
| cf1-r70-1-go-r0-defaults-a1              | correct    | 776.2s  | 746.8s  | 29.5s        | 16       | 0       | 1       | 0         | 0                    |
| cf1-r70-1-go-r0-planner-on-a1            | correct    | 1150.2s | 1124.2s | 26s          | 24       | 0       | 1       | 0         | 0                    |
| cf1-r70-1-go-r0-reviewer-medium-a1       | correct    | 687.7s  | 662.9s  | 24.8s        | 16       | 0       | 1       | 0         | 0                    |
| cf1-r70-1-go-r1-defaults-a1              | correct    | 1309.2s | 1287s   | 22.1s        | 27       | 0       | 1       | 0         | 0                    |
| cf1-r70-1-go-r1-planner-on-a1            | correct    | 1426.3s | 1389.7s | 36.6s        | 27       | 0       | 1       | 0         | 0                    |
| cf1-r70-1-go-r1-reviewer-medium-a1       | correct    | 638s    | 623.6s  | 14.3s        | 15       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r0-defaults-a1        | correct    | 866.9s  | 839s    | 28s          | 18       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r0-planner-on-a1      | correct    | 596.5s  | 574.6s  | 21.9s        | 15       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r0-reviewer-medium-a1 | correct    | 486.8s  | 468.7s  | 18.1s        | 10       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r1-defaults-a1        | correct    | 685.3s  | 659.4s  | 25.9s        | 16       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r1-planner-on-a1      | correct    | 819.1s  | 795.3s  | 23.8s        | 18       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-elixir-2-r1-reviewer-medium-a1 | correct    | 922.8s  | 899.4s  | 23.4s        | 17       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-go-r0-defaults-a1              | correct    | 521.2s  | 508.4s  | 12.8s        | 14       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-go-r0-planner-on-a1            | correct    | 755.6s  | 740.2s  | 15.4s        | 17       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-go-r0-reviewer-medium-a1       | correct    | 798.1s  | 785s    | 13.1s        | 16       | 0       | 2       | 0         | 0                    |
| cf1-r70-4-go-r1-defaults-a1              | correct    | 930.5s  | 912.9s  | 17.6s        | 21       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-go-r1-planner-on-a1            | correct    | 804.1s  | 787.5s  | 16.5s        | 17       | 0       | 1       | 0         | 0                    |
| cf1-r70-4-go-r1-reviewer-medium-a1       | correct    | 662.2s  | 647.8s  | 14.4s        | 16       | 0       | 2       | 0         | 0                    |
| cf1-r70-6-elixir-2-r0-planner-on-a1      | incomplete | 272.6s  | 268.4s  | 4.2s         | 5        | 0       | 0       | 0         | 0                    |
| cf1-r70-6-elixir-2-r0-reviewer-medium-a1 | correct    | 754.2s  | 738.5s  | 15.7s        | 15       | 0       | 1       | 0         | 0                    |
| cf1-r70-6-elixir-2-r1-planner-on-a1      | incomplete | 648.4s  | 635.2s  | 13.2s        | 12       | 0       | 0       | 0         | 0                    |
native usage by variant and provider (wire format kept separate):
defaults openai: input 1.83M, cached 0.11M, output 82.6k, reasoning 39.5k, input_tokens_details.cache_write_tokens 0, total_tokens 1.92M
planner-on openai: input 2.05M, cached 0.21M, output 87.6k, reasoning 34.7k, input_tokens_details.cache_write_tokens 0, total_tokens 2.14M
reviewer-medium openai: input 1.30M, cached 0.16M, output 44.5k, reasoning 12.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.35M
native usage by stage and provider:
stage build defaults openai (responses): input 0.44M, cached 0.11M, output 20.8k, reasoning 3.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.46M
stage build planner-on openai (responses): input 0.73M, cached 0.19M, output 34.6k, reasoning 4.4k, input_tokens_details.cache_write_tokens 0, total_tokens 0.77M
stage build reviewer-medium openai (responses): input 0.63M, cached 0.14M, output 28.4k, reasoning 4.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.66M
stage plan planner-on openai (responses): input 37.6k, cached 0, output 3.1k, reasoning 0, input_tokens_details.cache_write_tokens 0, total_tokens 40.7k
stage review defaults openai (responses): input 1.39M, cached 0, output 61.9k, reasoning 35.8k, input_tokens_details.cache_write_tokens 0, total_tokens 1.46M
stage review planner-on openai (responses): input 1.29M, cached 17.4k, output 49.8k, reasoning 30.3k, input_tokens_details.cache_write_tokens 0, total_tokens 1.34M
stage review reviewer-medium openai (responses): input 0.68M, cached 20.7k, output 16.2k, reasoning 7.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.69M
native usage by attempt and provider:
attempt usage cf1-r70-1-go-r0-defaults-a1 openai (responses): input 0.29M, cached 16.9k, output 17.0k, reasoning 7.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.30M
attempt usage cf1-r70-1-go-r0-planner-on-a1 openai (responses): input 0.38M, cached 64.6k, output 16.3k, reasoning 6.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.40M
attempt usage cf1-r70-1-go-r0-reviewer-medium-a1 openai (responses): input 0.23M, cached 48.9k, output 10.1k, reasoning 2.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.24M
attempt usage cf1-r70-1-go-r1-defaults-a1 openai (responses): input 0.61M, cached 40.7k, output 28.4k, reasoning 16.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.64M
attempt usage cf1-r70-1-go-r1-planner-on-a1 openai (responses): input 0.61M, cached 46.8k, output 27.6k, reasoning 14.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.63M
attempt usage cf1-r70-1-go-r1-reviewer-medium-a1 openai (responses): input 0.21M, cached 16.9k, output 8.7k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage cf1-r70-4-elixir-2-r0-defaults-a1 openai (responses): input 0.27M, cached 5.1k, output 10.2k, reasoning 4.7k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage cf1-r70-4-elixir-2-r0-planner-on-a1 openai (responses): input 0.19M, cached 5.1k, output 8.8k, reasoning 3.3k, input_tokens_details.cache_write_tokens 0, total_tokens 0.20M
attempt usage cf1-r70-4-elixir-2-r0-reviewer-medium-a1 openai (responses): input 96.0k, cached 5.1k, output 3.9k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 99.8k
attempt usage cf1-r70-4-elixir-2-r1-defaults-a1 openai (responses): input 0.22M, cached 10.2k, output 8.1k, reasoning 3.1k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage cf1-r70-4-elixir-2-r1-planner-on-a1 openai (responses): input 0.27M, cached 32.8k, output 9.7k, reasoning 3.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.28M
attempt usage cf1-r70-4-elixir-2-r1-reviewer-medium-a1 openai (responses): input 0.21M, cached 27.6k, output 6.0k, reasoning 2.2k, input_tokens_details.cache_write_tokens 0, total_tokens 0.22M
attempt usage cf1-r70-4-go-r0-defaults-a1 openai (responses): input 0.17M, cached 15.0k, output 7.2k, reasoning 2.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cf1-r70-4-go-r0-planner-on-a1 openai (responses): input 0.24M, cached 15.0k, output 9.7k, reasoning 2.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.25M
attempt usage cf1-r70-4-go-r0-reviewer-medium-a1 openai (responses): input 0.19M, cached 25.0k, output 5.9k, reasoning 1.5k, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cf1-r70-4-go-r1-defaults-a1 openai (responses): input 0.28M, cached 25.0k, output 11.7k, reasoning 4.9k, input_tokens_details.cache_write_tokens 0, total_tokens 0.29M
attempt usage cf1-r70-4-go-r1-planner-on-a1 openai (responses): input 0.22M, cached 0, output 9.5k, reasoning 3.6k, input_tokens_details.cache_write_tokens 0, total_tokens 0.23M
attempt usage cf1-r70-4-go-r1-reviewer-medium-a1 openai (responses): input 0.18M, cached 30.0k, output 5.5k, reasoning 1.8k, input_tokens_details.cache_write_tokens 0, total_tokens 0.18M
attempt usage cf1-r70-6-elixir-2-r0-planner-on-a1 openai (responses): input 37.7k, cached 12.0k, output 704, reasoning 23, input_tokens_details.cache_write_tokens 0, total_tokens 38.4k
attempt usage cf1-r70-6-elixir-2-r0-reviewer-medium-a1 openai (responses): input 0.18M, cached 6.0k, output 4.5k, reasoning 531, input_tokens_details.cache_write_tokens 0, total_tokens 0.19M
attempt usage cf1-r70-6-elixir-2-r1-planner-on-a1 openai (responses): input 0.12M, cached 33.4k, output 5.3k, reasoning 162, input_tokens_details.cache_write_tokens 0, total_tokens 0.12M
attempt outcomes included: defaults: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; reviewer-medium: correct 7, incorrect 0, workflow failure 0, infrastructure 0, incomplete 0; planner-on: correct 6, incorrect 0, workflow failure 0, infrastructure 0, incomplete 2
preparation: none
qualification: unavailable (not recorded in frozen manifest)
overall: measured attempts plus preparation and qualification; wall 16512s, model 16094.7s, tools/checks 417.3s, requests 352
builder settings: defaults openai gpt-6.1-sol reasoning.effort=medium; reviewer-medium openai gpt-6.1-sol reasoning.effort=medium; planner-on openai gpt-6.1-sol reasoning.effort=medium
## CMP-3 Counts and exposure
planned 24, started 21, scored 19, incorrect 0, infrastructure 0, incomplete 2
variant reviewer-medium differs from defaults in:
  roles.reviewer: openai gpt-6.1-sol high -> openai gpt-6.1-sol medium
variant planner-on differs from defaults in:
  plan.enabled: false -> true
roles.reviewer.effort: exercised in 7 of 7 reviewer-medium attempts
P01: exercised in 8 of 8 planner-on attempts
first position per task: r70-1-go defaults 1, reviewer-medium 1, planner-on 0 (2 repetitions, 3 variants)
first position per task: r70-4-elixir-2 defaults 1, reviewer-medium 0, planner-on 1 (2 repetitions, 3 variants)
first position per task: r70-4-go defaults 0, reviewer-medium 1, planner-on 1 (2 repetitions, 3 variants)
first position per task: r70-6-elixir-2 defaults 0, reviewer-medium 1, planner-on 1 (2 repetitions, 3 variants)
defaults: not the Kogen profile (differs in build.subagents_guidance, build.subagents_required, shape.subagents_guidance, shape.subagents_required, stop.max_command_seconds, stop.max_wall_seconds, verify.continue, verify.environment)
reviewer-medium: not the Kogen profile (differs in build.subagents_guidance, build.subagents_required, roles.reviewer.effort, shape.subagents_guidance, shape.subagents_required, stop.max_command_seconds, stop.max_wall_seconds, verify.continue, verify.environment)
planner-on: not the Kogen profile (differs in build.subagents_guidance, build.subagents_required, plan.enabled, shape.subagents_guidance, shape.subagents_required, stop.max_command_seconds, stop.max_wall_seconds, verify.continue, verify.environment)
experimental stop: every variant has stop.max_wall_seconds = 3600, stop.max_command_seconds = 900; no variant matches the Kogen profile configuration
defaults: build.helper_context = lab_helper (extension)
defaults: build.helper_prompt = lab:helper (extension)
defaults: build.subagents_output = 4096 (extension)
defaults: build.subagents_turns = 10 (extension)
defaults: plan.context = kogen_planner (extension)
defaults: plan.prompt = lab:plan (extension)
defaults: repair.context = packet,diff,check_results,review_findings (extension)
defaults: repair.roles = builder (extension)
defaults: review.timing = every_green (extension)
defaults: shape.critique_prompt = lab:critique (extension)
defaults: shape.critique_rounds = 1 (extension)
defaults: shape.helper_context = lab_helper (extension)
defaults: shape.helper_prompt = lab:helper (extension)
defaults: shape.subagents_output = 4096 (extension)
defaults: shape.subagents_turns = 10 (extension)
reviewer-medium: build.helper_context = lab_helper (extension)
reviewer-medium: build.helper_prompt = lab:helper (extension)
reviewer-medium: build.subagents_output = 4096 (extension)
reviewer-medium: build.subagents_turns = 10 (extension)
reviewer-medium: plan.context = kogen_planner (extension)
reviewer-medium: plan.prompt = lab:plan (extension)
reviewer-medium: repair.context = packet,diff,check_results,review_findings (extension)
reviewer-medium: repair.roles = builder (extension)
reviewer-medium: review.timing = every_green (extension)
reviewer-medium: shape.critique_prompt = lab:critique (extension)
reviewer-medium: shape.critique_rounds = 1 (extension)
reviewer-medium: shape.helper_context = lab_helper (extension)
reviewer-medium: shape.helper_prompt = lab:helper (extension)
reviewer-medium: shape.subagents_output = 4096 (extension)
reviewer-medium: shape.subagents_turns = 10 (extension)
planner-on: build.helper_context = lab_helper (extension)
planner-on: build.helper_prompt = lab:helper (extension)
planner-on: build.subagents_output = 4096 (extension)
planner-on: build.subagents_turns = 10 (extension)
planner-on: plan.context = kogen_planner (extension)
planner-on: plan.enabled = true (extension)
planner-on: plan.prompt = lab:plan (extension)
planner-on: repair.context = packet,diff,check_results,review_findings (extension)
planner-on: repair.roles = builder (extension)
planner-on: review.timing = every_green (extension)
planner-on: shape.critique_prompt = lab:critique (extension)
planner-on: shape.critique_rounds = 1 (extension)
planner-on: shape.helper_context = lab_helper (extension)
planner-on: shape.helper_prompt = lab:helper (extension)
planner-on: shape.subagents_output = 4096 (extension)
planner-on: shape.subagents_turns = 10 (extension)
limit: a process that leaves its process group and its workspace is not found by cleanup (TOOL-6)
limit: candidates cannot use sandbox-exec on seatbelt hosts; network access is not restricted; the boundary is proven for ordinary commands, not against a determined adversary
