# Formats

The contract every lane package follows. All JSON is written with sorted keys and a trailing newline (`common.write_json`).

## Kogen (what the harness relies on)

Studied at Kogen `b45ba32b` (read-only). Paths are in the Kogen repo.

- **CLI** (`cli/main.go`: `parse` l.97–190, `main` l.222–284): `kogen version` (also `--version`), `kogen init`, `kogen intent shape <slug> <request-file|->`, `kogen intent approve <slug> [<hash>]`, `kogen intent build <slug>`; `shape`, `approve` (also `--by <name>`) and `build` take `--project <dir>` (default: the current directory, which must be a git work tree); `init` and `version` take **no options** (`init --project X` exits 2 with `unknown option '--project'`) and `init` always runs in the cwd (`cli/main.go` l.77–90, 272–273). Slug: 3–48 chars, lowercase letters, digits, dashes (`cli/main.go` l.95, 241–246). `<hash>` is 6–64 lowercase hex.
- **Output**: results and errors go to stdout; errors are one line `<class>/<reason>: <detail>` (`lib/kogen/error.ex` l.1–15); progress goes to stderr (`docs/configuration.md` l.36).
- **Exit codes**: 0 success; 1 refusal or failed build (`Error` default, `build.ex` l.592, 827, 852, 932, 1009); 2 usage or invalid input (`main.go` l.225, 243; `approve.ex` "approval_identity_unavailable"); 3 environment (`build.ex` l.33, 896; `main.go` l.230); 5 `approve` without a hash printed the review card (`approve.ex` l.154); 70 internal error (`lib/kogen/main.ex` l.51); 129/130/143 signals (`main.ex` l.57–59). Build outcomes beyond "landed" are named only in the run log, not in the exit code.
- **Version**: `kogen <sha8> (<date>)` or `kogen dev+<hash8> (<date>, uncommitted source)` (`lib/kogen.ex` l.7–10).
- **`kogen init`** (`lib/kogen/init.ex` l.20–60, 83, 154ff; `README.md` l.48–60): needs a git identity (`Git.identity!`, l.20). On a repo with commits it makes **one shaping-model request** (`ChatGPT.require_login!`, detection of the project's commands), so its `commands` can differ between cells and it costs a model call; it then writes `.kogen/project.yaml` and `.gitignore` (adds `.kogen/local/`) and commits both as `Add Kogen configuration`. On a repo that already commits `.kogen/project.yaml` it only prints `Kogen is already initialized in <root>` and exits 0. On a repo without commits it writes a template and commits it. **The harness should ship a fixed, committed `project.yaml` (and `.gitignore`) with each task or lane and not run `init` per cell**; that avoids the model call and the variation.
- **Project config**: `.kogen/project.yaml` (`docs/configuration.md` l.19–22, 32): `version: 1`, `commands:` (setup, fix, checks, acceptance), `protect:`, then `models:` with `shape`, `build`, `review` (also `read`, `probe`, `draft`), each `{model: <name>, effort: <effort>}`. No command takes model flags. A lane's `"provider/model effort"` string maps to one such line (the provider part is not in the file at `b45ba32b`; the harness writes `model: <provider/model>` unless L2 finds Kogen wants the bare name).
- **Intent**: `.kogen/intents/<slug>/` with `intent.md`, `acceptance.feature`, optional `model.qnt` and the step files it names (`lib/kogen/intent.ex` l.1–26). `shape` writes it uncommitted; the Intent folder must be committed or untracked-but-present at build.
- **Approval**: `kogen intent approve <slug>` prints the card with `SHA-256: <hash>` and exits 5; `approve <slug> <hash-prefix>` writes `.kogen/local/approvals/<slug>.json` `{slug, sha256, approver, approved_at}` (`approve.ex` l.60–100, `intent.ex` l.353) and exits 0. Needs git `user.name`/`user.email` or `--by`. The approval is deleted when the build lands (`build.ex` l.940).
- **Run log**: `.kogen/local/runs/<id>/` (`lib/kogen/run.ex` l.1–25) with `log.jsonl` (one JSON object per line, each with `at` ISO-8601 UTC and `event`), `result.json`, `review-<n>.json`, `checkpoint.json`. Events: `start` {slug, start_head, approved}; `request` {role, model, effort, usage (the provider's usage map as Kogen has it; Kogen counts input, cached, output, reasoning), wall_ms} (`build.ex` l.1128); `tool_call`; `command` / `command_result` {name, status, output}; `pass` {pass, green, failing, not_run, files_changed_while_checks_ran} (`build.ex` l.734); `review` {review, attempt, pass, tree, verdict, findings} (`review.ex` l.135); `commit` {tree} (`build.ex` l.875); `builder_blocker`; `resume`; `outcome` {outcome, commit?, provider_failure?} (`build.ex` l.944, 1068). `result.json`: {slug, build, outcome, start_head, passes, reviews, repairs, usage, model_active_ms, ...} (`build.ex` l.1082). A landed build is one commit on HEAD.
- **Not in b45ba32b** (what the design's R1–R5 would add): tree hashes on `pass` events (only `review.tree` and `commit.tree` name trees); per-stage start and end times (only `at` per event and `wall_ms` per request); unknown per-request usage is not marked; building from a supplied, already-approved Intent without shape; `version` reporting a dirty-tree hash for patched builds; distinct exit codes per outcome (timeout, blocked, provider failure). Until then the harness derives pass trees from `review`/`commit` events and outcomes from the last `outcome` event.

`lanes/tests/fake-kogen` follows the lines above and nothing more.

## experiment.json

Written and committed before any run; validated by `lanes/lanes/experiment.py` (error names the field; entry points exit 2).

| field | type | rule |
|---|---|---|
| `id` | string | letters, digits, `.` `_` `-`; names the run dir |
| `phase` | string | `shape` \| `build` \| `e2e` |
| `intent_form` | string | `gherkin` \| `gherkin-lean` \| `gherkin-quint` \| `prose`; required when `phase` is `build` (the folder `supplied/<form>/` to build from), ignored for `shape` and `e2e` |
| `kogen.repo` | string | URL or path of the Kogen repository |
| `lanes[]` | objects | at least one; unique `name` |
| `lanes[].name` | string | as `id` |
| `lanes[].sha` | string | 40 lowercase hex, a Kogen commit |
| `lanes[].patch` | string or null | path relative to the experiment file, no `..` |
| `lanes[].settings.models` | object | role → `"provider/model effort"`, applied to `.kogen/project.yaml` |
| `tasks[]` | strings | task ids, unique, at least one |
| `reps` | integer | ≥ 1 |
| `deadline_s` | number | > 0, per cell |
| `hosts[]` | strings | host names only |
| `decision_rule` | object | has a string `kind` (L6 defines the kinds) |

## Task folder (private)

Lab layout, e.g. `$LAB_NEXT/spec/examples/tasks/rate-go`; schemas `spec/schema/task.json` and `evaluate.json`. Outside the repo; the harness takes its path from a flag or `KOGEN_LANES_TASKS`. `lanes/tests/fixtures/task-mini` is a tiny Go task valid against both schemas.

- `task.toml` (`task.json`): required `name` (l.4), `split` (`development` | `confirmation`, l.8), `language` (l.16), `requires` (list, l.20), `test_globs` (list, l.55), `regression_tests` (list, l.59); optional `env`, `setup` (list), `fix` (list), `protect` (list), `[[check]]` {`name`, `run`} (both required, l.36), `[acceptance]` {`run`, `steps_dir`}.
- `start/` — the starting tree (the work tree's first commit); includes the acceptance steps folder (`features/steps/`).
- `reference/` — a correct solution, files copied over `start/` (the fake Kogen's `correct` mode).
- `wrong/<name>/` — known-wrong solutions copied over `start/`; the grader must fail them.
- `evaluator/` (`evaluate.json`): `evaluate.toml` with required `overlay` (`evaluate.json` l.7; folder under `evaluator/` laid over the tree, normally `files`) and `[[command]]` (at least one, l.11) each with required `name`, `run`, `adapter` (`go_test_json` | `exunit_lab` | `lab_jsonl`), `results` (file the command writes via `$LAB_RESULTS`) and `timeout_seconds` (int ≥ 1); optional `setup` (list) and `[expected]` {`requested`, `regression`} (lists of test ids). Hidden tests live in `overlay`.
- `request.md` — the shape brief (`shape` and `e2e`).
- `supplied/<form>/` — the frozen approved Intent, one folder per Intent form: `intent.md`, `acceptance.feature` and the step files the Intent's `Acceptance:` list names (e.g. `features/steps/…`); `gherkin-lean` adds `model.lean`, `gherkin-quint` adds `model.qnt`; `prose` has only `intent.md`. Forms: `gherkin`, `gherkin-lean`, `gherkin-quint`, `prose` (`$LAB_NEXT/spec/examples/tasks/rate-go/supplied/`, `EQUIVALENCE.md`; chosen in the Lab by `shape.supplied`, `spec/schema/config.json` l.740–749). A `build` experiment names the form in `intent_form`.

## lanes.lock.json (from L2)

`[{name, sha, patch_sha256, artifact_sha256, kogen_version}]`, one entry per lane; `patch_sha256` is null without a patch.

## plan.jsonl (from L5)

One cell per line: `{cell, task, rep, lane, order}`; `cell` is `<task>/r<rep>/<lane>`.

## Run directory

`$KOGEN_LANES_HOME/runs/<experiment id>/` (`KOGEN_LANES_HOME` defaults to `~/.cache/kogen-lanes`):

```
experiment.json  lanes.lock.json  plan.jsonl
cells/<task>/r<rep>/<lane>/
  result.json  run-log/  final-tree.tar  intent/  stdout.txt  stderr.txt  evaluation.json
```

- `result.json`: `{cell, lane, phase, exit_code, outcome, started, ended, wall_s, kogen_version, final_tree, pass_trees: [], intent_hash, host}`.
- `run-log/`: copy of Kogen's run folder. `final-tree.tar`: `git archive` of the final tree. `intent/`: the Intent (shape and e2e).
- `evaluation.json`: added by the grader (L4).
