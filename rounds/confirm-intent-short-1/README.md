# Short intent on a fresh specification

A descriptive confirmation screen on one new private specification in Go and Elixir. The round is approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

## Question and scope

On a fresh specification whose acceptance scenarios cover all requirements checked by hidden tests, is a short intent correct in at least as many paired blocks as full prose, with no more wrong submissions or wrong first-green builds?

The task specifications remain private. This page reports the public task IDs and the per-test outcome IDs exported with them; it does not reproduce the task prose, acceptance scenarios, hidden-test code, or reference implementations.

## What each arm received

The full arm received the complete prose specification plus an extended Gherkin acceptance feature and its step definitions. The short arm received an Intent frame containing a title, purpose, command-line synopsis, and option names, plus the same extended feature and steps. The two arms used identical acceptance scenarios for each task, and the feature coverage was checked against every requirement exercised by hidden tests.

A rescue means review changes a tree that failed one or more hidden tests into a tree that passes them all. The reviewer approved all 12 trees unchanged, so each submission was its first green build and no rescue occurred.

## Fixed rule

CONFIRMED requires short to be correct in at least as many blocks as full, with no more wrong submissions and no more wrong first-green builds, across at least five usable blocks. REJECTED applies if short is correct in fewer blocks or has more wrong submissions or wrong first-green builds. UNRESOLVED applies when fewer than five usable blocks are available.

## Results

A paired block is one task and repetition run with both full and short. A first-green build is the first code snapshot that passed the workflow's verification checks; hidden tests determine whether it was correct.

The run scored 12 of 12 attempts and had six usable pairs of attempts, each comparing full and short on the same task and repetition: two task IDs, three repetitions, and both arms. There were no wrong submissions, builder stops, provider refusals, repairs, or wrong first-green builds.

| Arm | Correct blocks | Wrong submissions | Wrong first-green builds | Reviewer edits | Builder input tokens | Reviewer input tokens | Total input tokens | Sum of review-stage durations (Lab bundle) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Full prose | 6 of 6 | 0 | 0 | 0 | 0.45M | 0.61M | 1.06M | 538.9 s |
| Short intent | 6 of 6 | 0 | 0 | 0 | 0.39M | 0.48M | 0.87M | 410.4 s |

**CONFIRMED.** Short was correct in as many usable blocks as full (6 of 6), with no more wrong submissions and no more wrong first-green builds; the run had at least five usable blocks.

| Task ID | Full correct submissions | Short correct submissions |
| --- | ---: | ---: |
| subnet-ex | 3 of 3 | 3 of 3 |
| subnet-go | 3 of 3 | 3 of 3 |

### Public test outcomes

The outcomes below list repetitions 0, 1, and 2 in that order. State strings come directly from the exported public ID maps.

| Task ID | Public test ID | Full outcomes | Short outcomes |
| --- | --- | --- | --- |
| subnet-ex | test_hidden:test_address_lexical_and_range_errors_are_exact | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_address_validation_precedes_prefix_validation | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_argument_errors_and_precedence | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_ascii_check_precedes_all_row_parsing | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_cidr_shape_error_is_exact | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_comments_must_start_in_first_column | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_crlf_final_cr_and_physical_line_numbers | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_default_retains_duplicate_canonical_subnets | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_default_text_empty_and_dash_json | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_file_path_uses_same_output_as_stdin | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_first_bad_physical_line_wins_without_partial_output | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_format_text_and_unique_work_in_either_order | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_help_exact_and_does_not_read_input | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_json_has_exact_key_order_and_aggregate_values | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_missing_file_reports_exact_read_error | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_prefix_lexical_and_range_errors_are_exact | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_text_sorts_and_canonicalizes_host_bits | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_thirty_one_and_thirty_two_prefix_hosts_are_usable | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_thirty_prefix_hosts_exclude_network_and_broadcast | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_unique_keeps_one_canonical_network_prefix_pair | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_unique_still_validates_later_duplicate_lines | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_unknown_options_and_help_with_extra_argument | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_unrecognized_option_is_checked_before_later_path_count | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_value_option_consumes_flag_like_token | passed / passed / passed | passed / passed / passed |
| subnet-ex | test_hidden:test_zero_prefix_and_decimal_output_bounds | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_address_lexical_and_range_errors_are_exact | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_address_validation_precedes_prefix_validation | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_argument_errors_and_precedence | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_ascii_check_precedes_all_row_parsing | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_cidr_shape_error_is_exact | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_comments_must_start_in_first_column | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_crlf_final_cr_and_physical_line_numbers | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_default_retains_duplicate_canonical_subnets | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_default_text_empty_and_dash_json | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_file_path_uses_same_output_as_stdin | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_first_bad_physical_line_wins_without_partial_output | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_format_text_and_unique_work_in_either_order | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_help_exact_and_does_not_read_input | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_json_has_exact_key_order_and_aggregate_values | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_missing_file_reports_exact_read_error | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_prefix_lexical_and_range_errors_are_exact | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_text_sorts_and_canonicalizes_host_bits | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_thirty_one_and_thirty_two_prefix_hosts_are_usable | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_thirty_prefix_hosts_exclude_network_and_broadcast | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_unique_keeps_one_canonical_network_prefix_pair | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_unique_still_validates_later_duplicate_lines | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_unknown_options_and_help_with_extra_argument | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_unrecognized_option_is_checked_before_later_path_count | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_value_option_consumes_flag_like_token | passed / passed / passed | passed / passed / passed |
| subnet-go | test_hidden:test_zero_prefix_and_decimal_output_bounds | passed / passed / passed | passed / passed / passed |

All 12 exported attempts were correct, with every listed public ID in the passed state for all three repetitions in each arm. The short arm used 18% less input (0.87M versus 1.06M). Together with the development screen, the short arm was correct in 14 of 14 attempts against 14 of 14 for full, across six task IDs and two languages, at 18–19% lower input.

## Limits

This is one fresh specification represented in two languages and six paired blocks. It supports the fixed comparison on this sample and did not test weaker builders or less fully specified work. The extended feature needed 24 more scenarios than the standard one (41 in total), so shorter prose moved detail into the scenarios.

## Required reproduction metadata

The frozen settings, resolved configurations, attempt records, and exported public ID states are in the public bundle. The task materials remain private. Lab outcomes are descriptive; no official benchmark grade was assigned. Standard 1.2 records, measured fields, declared gaps, and missing-field data are included with the round.

## Metadata

Round date: 2026-10-21
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — fresh-task confirmation, approximate execution, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Lab build: 3bf295ef
Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b
Model and effort: the default builder and reviewer settings.
Task IDs: subnet-ex and subnet-go.
Harness commit: not recorded as a public Git commit; the execution build is identified above.
Command: the experiment was run and exported in Lab before publication.
Raw records: records.jsonl and the public bundle preserve attempt outcomes and configuration.
The run scored 12 of 12 attempts, with six usable pairs of attempts, each comparing full and short on the same task and repetition, and used 1.93M input tokens of the 5M budget.
All 12 review trees were approved unchanged and were the first green builds.
The public bundle retains the frozen configuration, attempt outcomes, and public ID states.

## What's missing and why
- `circumstances.cap_end` (12 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (12 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (12 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (12 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (12 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (12 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (12 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (12 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (12 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (12 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (12 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (12 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (12 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (12 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (12 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (12 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (12 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (12 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (12 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (12 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (12 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (12 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (12 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `provenance.ledger_sha256` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (12 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (12 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (12 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (12 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (12 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (12 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (12 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.gate` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (12 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (12 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
