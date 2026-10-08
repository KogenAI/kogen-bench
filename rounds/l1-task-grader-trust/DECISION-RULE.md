# L1 decision rule — task and grader trust

The design was recorded on 7 October 2026, before any scored cell. L1 is a model-free control audit; operator-run official control grades are recorded in the public receipt. No scored model cells were launched.

## Units and controls

The eight task variants are r70-2-elixir, r70-2-go, r70-4-rust, r70-4-elixir-fe2, r70-4-go-fe2, r70-4-ts-bun-fe2, r70-5-go, and r70-7-rust. The original cohort staged two small reference mutants and one valid alternative per variant. Two replacement mutants are recorded in a separate cohort for r70-4-elixir-fe2 and r70-4-go-fe2 after their second original mutants failed at build. The replacement behavior class is rebase-success outcome misclassification. Their patch SHA-256 values and behavior class are published in the control manifest.

## Admission and outcome rule

Reference-pass and noop-fail admission controls must be recorded for each variant on its assigned host before control grading where coverage is missing. Recorded coverage and the two required new US admission commands are in RESULTS.md and README.md.

The intended official outcomes are: each behavioral mutant compiles and fails on the seeded behavioral defect, and each valid alternative passes. A behavioral-mutant pass is evidence that the grader did not detect that seeded prompt violation. A build-failure mutant does not show that the grader detects its intended behavioral defect. An alternative failure is evidence of a possible over-strict gate. Report the official outcomes per control and do not infer beyond these seeded examples. Original build-failure mutants r711/r714 are retained and labelled build rejections; graded replacements r720/r719 supersede them for the behavioral-mutant criterion.

No token totals are measured for this model-free lane. Any future token reporting must use uncached, cached, and output tokens, with total equal to their sum. Before releasing any scored benchmark cells, complete every item in the release checklist, including one real cell per arm through the actual sandbox and official grading.

Use status labels VALID, CONFOUNDED, INVALID, INTERIM, WITHDRAWN, or NOT-RUN. Current status is VALID: 21 original controls were graded for seven admitted variants, three staged task-4 Rust controls were withdrawn before grading, and two replacements were officially graded. Fourteen behavioral mutant detections now cover the seven admitted variants (two per variant), alongside seven passing alternatives. The original r711/r714 build rejections remain recorded and are superseded by r720/r719 for the criterion. No scored model cells were launched.


## Addendum: L1-EU (7 Oct 2026)

The L1-EU extension applies the same control criteria to two EU Elixir variants. Admission requires two reference PASS controls, two no-op FAIL controls, two behavioral-mutant FAIL controls, and one alternative PASS. Task 6's reference/no-op pair passed, but both prompt-length mutants passed; the suite therefore failed to detect those seeded limits and `r70-6-elixir` is NOT ADMITTED. Task 7's prior R70 reference/no-op pair passed its admission gate; mutants r733/r734 failed 23/24 each and alternative r735 passed, so `r70-7-elixir` is ADMITTED.

The L1-EU audit itself is VALID and model-free. It does not change the original seven-variant result. `l4b-confirm-eu` remains NOT-RUN because only one variant was admitted and its baseline was 5/6; no cells were spent. Any future scored release still requires every item in the release checklist, including one officially graded real sandbox cell per arm.
