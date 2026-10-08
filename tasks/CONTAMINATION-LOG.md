# Task-suite contamination log

Dated record of every known exposure of hidden-suite material outside the official grading pipeline. Each affected task in the catalogue carries a matching `exposures` entry in its `task.json`, so later rounds can avoid those tasks or keep them knowingly. This log records the scope and recipients without listing test names. L3b now separately publishes the per-test outcomes it needs to recompute its registered decision rule.

<a id="2026-10-08--failed-test-names-in-an-operator-codex-job"></a>

## 2026-10-08 — failed-test names in an operator Codex job

- **What:** hidden-suite failed-test **names** only: 20 distinct names. No test source, assertion text, grader code, reference solution or sealed file was exposed.
- **Which suites:** four r70 hidden suites, each shared by every stack of its task (same suite digest across stacks):

  | Task | Suite digest (prefix) | Distinct names exposed | Rows the names came from |
  | --- | --- | ---: | --- |
  | r70-2 | `5ca6ad5c8f26` | 4 | L3b grade rows for r70-2-go (RESTART, CONTINUE, REPAIR variants) and r70-2-elixir REPAIR |
  | r70-4 | `6136eb268b80` | 1 | L3b grade rows for r70-4-elixir-fe2 (all arms) |
  | r70-5 | `754d878d4e17` | 14 | L3b grade rows for r70-5-go RESTART and CONTINUE, plus two admission no-op rows |
  | r70-7 | `20f6ee33ae5b` | 1 | L3b grade row for r70-7-rust RESTART |

- **How:** an operator documentation job ran 2026-10-08 05:51:38–06:22:34Z through the Codex CLI on OpenAI's `gpt-6-luna` model at max effort. It was inspecting private lane records, and two of its inspection commands printed whole rows from the L3b `grades.jsonl`, including the `failed_test_names` field. The names entered that job's model context and so reached the model provider (OpenAI). The job reported the exposure itself, and none of its outputs contain the names.
- **Chronology:** all 24 L3b contestant executions had finished by 05:47:42Z, before the job began. The last 14 L3b official grades finished at 06:06:26Z, inside the job's interval. The retained job log has no per-command timestamps, so whether the printing commands came before or after that grading is not established. Grading applies each fixed patch to the hidden suite and takes no input from the job.
- **Who saw them:** that one non-contestant operator job and its model provider. No contestant cell, agent session, Kogen run or benchmark sandbox had access to them (operator-reported). The documented L3b cohort's executions predate the exposure, as above. Any later round that uses these suites must treat them as exposed.
- **Catalogue marking:** all 20 catalogue tasks `r70-{2,4,5,7}-{elixir,gleam,go,rust,ts-bun}` carry `exposures[]` with `kind: hidden-test-names-to-operator-job` and date `2026-10-08`. Derived variants (fe2, l2*, l3*, l4pk) share these suites and inherit the marking.
- **Guard since:** grade rows, grade windows, run records and manifests are inspected only through the lane helper `levers/lib/safe_rows.py`. It replaces `failed_test_names`, `failing`, `tail`, test stdout/stderr and failure summaries at any depth before printing. The operator job wrapper's standing preamble now forbids printing those files directly (HIDDEN-SUITE RULE). A follow-up job run under the guard had zero hidden values in its log.

<a id="2026-10-08--grade-rows-in-a-zig-task-author-job"></a>

## 2026-10-08: raw grade rows in a Zig task-author job

- **What:** raw official grade rows, which can contain `failed_test_names` and output tails. No test source, grader code, reference solution or sealed file beyond what the job already held was exposed through these rows.
- **Which suite:** the r70-1 hidden suite (shared by every stack of task 1). Rows came from `levers/r70/grades.jsonl` and `r70-rve/official-rve-grades.jsonl`, for r70-1-rust cells and lang-sol-replication cells.
- **How:** on 2026-10-08, during the Zig vs Rust round (rz1), the task-author job `zig-author-1` (Codex CLI, gpt-6-luna max, writing the r70-1-zig variant) ran grep over those grade files, and the matching rows entered its model context and reached the model provider (OpenAI). The other seven author jobs' logs show only prompt-text matches.
- **Who saw them:** that one non-contestant author job, which already had declared access to task 1's sealed suite by design (authoring a variant requires it), and its model provider. No contestant cell, agent session, Kogen run or benchmark sandbox had access to them.
- **Effect:** rz1's pre-registration declares author exposure to the task suites. Contestant cells never see grade rows, so rz1's held-out status for contestants is unchanged. Any later round that uses r70-1 as a held-out task must treat its suite as exposed.
- **Catalogue marking:** the r70-1 tasks should carry `exposures[]` with `kind: grade-rows-to-author-job` and date `2026-10-08`. Pending: added in the next catalogue update.
- **Guard:** author and operator jobs inspect grade files only through `levers/lib/safe_rows.py`. The author-job prompts get the same HIDDEN-SUITE RULE preamble as operator jobs.
