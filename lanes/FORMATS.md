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
| `lanes[].settings.models` | object | role → `"provider/model effort"`; `.kogen/project.yaml` gets `<role>: {model: <part after the first "/">, effort: <last word>}` (bare id, as Kogen takes ChatGPT ids: `config.ex` l.19-21) for prefix `openai/` or `chatgpt/`, and `{model: …, effort: …, provider: <prefix>}` for any other prefix (e.g. `supergrok/grok-4.7 high`, `opencode-go/…`), only for roles set. The `provider` key exists from Kogen main 65640c6; b45ba32b lanes must use `openai/`. Kogen's own config validation decides which providers and models are valid; unset roles keep Kogen's defaults (`config.ex` l.254-268). |
| `tasks[]` | strings | task ids, unique, at least one |
| `reps` | integer | ≥ 1 |
| `deadline_s` | number | > 0, per cell |
| `cost_cap_usd` | number | finite, > 0; required to run cells (`lanes-run`, `lanes-cell` refuse without it); the soft cap, see Cost cap |
| `hosts[]` | strings | host names only |
| `decision_rule` | object | has a string `kind` (L6 defines the kinds) |

### Climb experiments

`"kind": "climb"` marks a hill-climbing round (others: no `kind`). Extra fields, all required, validated by `experiment.py`:

| field | type | rule |
|---|---|---|
| `lanes[]` | objects | exactly two, named `baseline` and `candidate`, same `sha`; they differ by one patch (different `patch`, same `settings`) or by exactly one `settings` entry (same `patch`), never both |
| `split.train`, `split.test` | strings | non-empty, unique task ids, disjoint; together exactly `tasks` |
| `min_effect` | number | greater than 0, at most 1: the smallest pass-rate difference worth acting on |
| `noise_ref` | string | path to a noise record (written by `lanes-noise`; only its shape is checked here) |
| `round` | integer | ≥ 1 |
| `parent` | string or null | previous round's `id`; null exactly in round 1 |
| `decision_rule.kind` | string | `keep_revert` (and only climb experiments may use it) |
| `decision_rule.improves` | object, optional | `{"test": "task_sign", "max_p": p}` with 0 < p < 1: a split improves only if its pass-rate difference exceeds `min_effect` and the exact one-sided sign test over tasks gives p ≤ `max_p`, instead of a Hoeffding interval above zero (`DECISION-RULES.md`). Absent: the Hoeffding rule, report unchanged. With it the verdict adds `sign` (per split `k`, `n`, `p`) and its `params` is `{"improves": ...}` |

`report.json` of a climb run adds `climb`: per split (`train`, `test`) both lanes' `{correct, n, rate, ci}` (Wilson 95%), `unit` (`task`), `tasks`, `pairs`, `candidate_better`, `baseline_better`, `tied`, `difference` (the pass-rate difference: mean over tasks of each task's mean rep difference), `difference_exact` (the same, a decimal or `n/d`), `difference_ci` (Hoeffding 95% over tasks), `pair_difference`; `plumbing` (one row per excluded cell: `cell`, `lane`, `split`, `category`, `outcome`, which is null for test cells), `plumbing_counts`, and `train_failures` (cells of the train split that failed on the task, for the next round; test failures are never listed). Every lane also carries `pass_rate_ci`, `first_green_pass_rate_ci`, `plumbing` counts and `witness_failures_test` (climb: a count; the lane's `outcomes`, `classes`, `plumbing` and `witness_failures` then cover train cells only, and its rates leave plumbing out).

## Cost cap

`cost_cap_usd` is the **soft cap**; the **hard cap** is 1.25 × `cost_cap_usd`. Both come from `experiment.json` (so `PLAN.json` carries the cap) and are enforced in `lanes/lanes/costguard.py`, which every entry point uses. A run dir whose `experiment.json` has no `cost_cap_usd` (an older run) gets no new cell from `lanes-run` or `lanes-cell`; the error says to add the field and run `lanes-plan` again.

**Spend estimate** of a run dir: finished cells' `totals.cost_usd` (a null one is re-read from the cell's saved logs), plus the spend so far of running cells parsed with `usage.py` from their live Kogen run log and shaping events, plus the **ledger**. A running cell leaves `live.json` in its cell dir (its workspace); a cell that stopped without `result.json` leaves `spent.json`. Spend is never forgotten: before a cell dir is thrown away (a retry, `--force`), its spend is appended to `cost-ledger.jsonl` in the run dir (`{cell, usd}` per line) and counted from then on; a remote attempt that was killed has its `spent.json` fetched into the ledger before the remote dir is removed (the last polled value is the floor).
- no price row for the model (or no price cost_calc can give): the request's tokens at the highest input, cached-input and output rate in `reproduce/price-table-v1.json`;
- unknown usage (a null counter, or a build request whose four counters are all 0): an allowance of 100,000 input and 20,000 output tokens at those rates (about $2), above the largest request seen in real logs (53,940 uncached input tokens). It is an allowance, not a proven bound.

**Fails closed on real errors**: unreadable or unparsable usage (a log line that is not a JSON object, other than a last line still being written; counters that are not non-negative integers or cached > input; a malformed `result.json`, `spent.json` or ledger), no `cost_calc.py` or price table, or a crash of the guard stops the run. `lanes-cell` refuses to start (exit 2, "fails closed"); a running cell is aborted as `cost_cap` (`result.json` has `cost_error`); `lanes-run` claims no new cell and stops every cell.

**Exactly once**: a source that is gone because its attempt finished, was retired or was cleaned up is not an error. Every step that moves an attempt's spend from one record to the next holds the run dir's lock (`flock` on `.cost.lock` in the run dir) exclusively: a cell ending (`spent.json` written and `live.json` removed before its workspace is deleted; `result.json` is written while `live.json` still exists and is read first), `retire` (ledger line, then the cell dir removed) and every ledger append. `estimate` reads under the shared lock, so it sees each attempt in exactly one record. A source gone with no final record yet (a `live.json` whose workspace is gone, no `spent.json`) is retried, with the lock released, for 5 s (`RETRY_S`); then the guard fails closed. On the controller, an attempt's remote live spend and its ledger line change together under one lock (only cells still running keep a polled value).

**Soft cap**: `lanes-run` claims no new cell once the estimate is at or above the cap, and exits 3 when cells were left; `lanes-cell` exits 2 without starting when the estimate has reached it. Both print the spend and the cap and write `cost-stop.json` in the run dir (`{cap: soft|hard, spent_usd, at}`; a hard note is never replaced by a soft one; a new `lanes-run` clears it).

**Hard cap**: while a cell runs, a watcher thread in `lanes-cell` (every `LANES_COST_WATCH_S` seconds, default 0.5) kills the cell's own process group as soon as the run dir's estimate reaches the hard cap. The cell is recorded with outcome `cost_cap` (also the killed command's stage outcome); the report counts it as plumbing, not a task failure (class `incomplete`, plumbing category `cost_cap`, also a key of a climb report's `plumbing_counts`). `lanes-run` writes the note, stops claiming, gives local cells 3 s to stop themselves, then stops every cell it started, and exits 3.

**Remote hosts**: `Host.prepare` copies `reproduce/cost_calc.py` and the price table to the host (`<root>/reproduce/`). While a remote cell runs, the controller polls `python3 -m lanes.costguard cells <remote run dir>` over ssh every second and adds each cell's live spend (the larger of the local and the polled value) to its own estimate, so the soft and hard caps cover cells on every host. Three polls in a row that fail stop the run (fail closed). Every remote host is polled. A remote `lanes-cell` also guards its own host's cells.

`report.json` has `cost`: `{cost_cap_usd, hard_cap_usd, spent_usd, lanes: {lane: usd}, cost_cap_cells, not_started, stopped}`; `stopped` is `hard` when any cell ended `cost_cap` (a remote cell's own note stays on its host), else `soft` or `hard` from `cost-stop.json`, else null; `not_started` counts planned cells with no cell dir. `report.md` has the section "Spend vs cost cap".

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

- `result.json`: `{cell, lane, phase, exit_code, outcome, started, ended, wall_s, kogen_version, node: {path, version} | null (the Node of an unpacked release's `node-path`), final_tree, pass_trees: [], intent_hash, host, stages, totals}`; `stages` and `totals` are described under Stage records.
- `run-log/`: copy of Kogen's run folder. `final-tree.tar`: `git archive` of the final tree. `intent/`: the Intent (shape and e2e).
- `evaluation.json`: added by the grader (L4).

## Stage records (`result.json` `stages`, `totals`)

`lanes/lanes/usage.py` (`parse_run_log(events, commands, table=None, shape_events=None)`) builds them from two sources: the build run log (`events`) and the shaping events (`shape_events`: `.kogen/local/shaping/<slug>/events.ndjson`, which `kogen intent shape` writes; `shape.ex` l.11, `shape_evidence.ex` l.59–90). **L3 copies the shaping events file into the cell** (next to `run-log/`) for every cell that ran `shape`. Every phase records them, shape-only cells too, because identical Intents still differ in cost and speed. `commands` is one entry per Kogen command the cell ran, `{stage, started, ended, wall_s, exit_code, timed_out?}`, measured by the harness, so each command's wall time exists even when the log is silent.

`stages[]`, in command order, each `{stage, started, ended, wall_s, exit_code, outcome, requests, models, input_tokens, cached_input_tokens, output_tokens, reasoning_tokens, cost_usd, cost_reason, missing}`:

- `stage`: `shape`, `approve` or `build` (command level; `shape` sums the `provider_call` events of the shaping events, one request each, model = `effective_model`, usage `{input, cached, output, reasoning}` with nulls kept as null, `wall_ms`; `started`/`ended` are ISO-8601 UTC, `wall_s` seconds, `exit_code` the command's), then one inner record per request role the log names `verify`, `review`, `repair`. An inner record has the tokens, cost and the summed request `wall_ms` of that role; `started`, `ended`, `exit_code` and `outcome` are null and listed in `missing`. A request belongs to exactly one record: `build` holds every request not in an inner role.
- `outcome`: `timeout` when the command hit its deadline; for `build` the last log `outcome` event (`landed`, `build_blocked`, ...), `no_outcome` when a failed build logged none; otherwise `ok` or `exit_<code>` (`approve` exit 5 with a card counts as `ok`: it printed the card).
- Tokens are sums over the stage's requests (`reasoning_tokens` is a subset of `output_tokens`). A request with a null counter (shaping events when the provider sent no usage; build logs of a future Kogen) makes the stage's sum null. A build request whose four counters are all 0 is flagged, not priced (see the R2 gaps): `usage_zero_is_unknown` in `missing`, `cost_usd` null. `approve` makes no request: zero tokens, cost 0.
- `cost_usd`: sum of `reproduce/cost_calc.py` over the requests (model id as logged, else the part after `/`); null with `cost_reason` when usage is missing or a model has no price. When cost_calc prices a model from a third-party rate it returns an estimate: `cost_usd` keeps the value and `cost_reason` is cost_calc's status (`declared_estimate`), so an estimate is never reported as exact. Totals join the reasons.
- `missing`: names of the null fields the log could not supply. Nothing is invented.

`totals`: `{requests, models, input_tokens, cached_input_tokens, output_tokens, reasoning_tokens, wall_s, cost_usd, cost_reason, missing}`. Counters and cost sum all records (null when any is null); `wall_s` sums command-level stages only, since inner records overlap them.

**R2 gaps** (what b45ba32b's log cannot supply, so these fields are null and listed in `missing`):
- Build `request` events log `ChatGPT.usage/1`, which turns every missing counter into 0 (`chatgpt.ex` l.651–661): a request whose provider sent no usage looks like a request with zero tokens, and the log cannot tell 0 from unknown. The harness therefore flags a build request with all four counters 0 (`usage_zero_is_unknown`, cost null) and R2 would add a null or a flag. Only the shaping events (`known_usage`) carry null counters.
- The shaping events file is not a run log: it has no outcome and its events are not in the build log, so the harness reads it separately (above).
- No stage start/end events: `started`, `ended` and `exit_code` come from the harness, and inner stages have none.
  Inner stages other than `review` are named only if a request role says so; `repair` and `verify` appear only then.
- No per-request start time in the build log (only `at` at the end and `wall_ms`).
- Build outcome beyond the last `outcome` event, and distinct exit codes per outcome, as listed under Not in b45ba32b.

## PLAN.json

Written by `python3 -m lanes.plan_hashes <experiment.json> --tasks <dir> --lock lanes.lock.json --out PLAN.json` before any cell runs, and committed to kogen-bench before the run. It holds only hashes for private material:

```
{experiment: <experiment.json>,
 hashes: {tasks: {<id>: {task, tree, hidden_tests, task_toml, request, intents: {<form>: sha}}},
          lanes: {<name>: {patch, settings}}},
 lock: {sha256, artifacts: {<lane>: artifact_sha256}}}
```

`task` is the whole task folder (so `reference/` and `wrong/` are covered too), `tree` the `start/` tree, `hidden_tests` the `evaluator/` folder, `intents.<form>` each `supplied/<form>/`, `patch` the patch file (null without one), `settings` the sha256 of the lane's settings as sorted compact JSON. Folder hashes are `common.sha256_tree`; file hashes `common.sha256_file`.

`PLAN.json` omits the experiment's `hosts` (host names never go into the public repo). `plan_hashes` exits 2 with a message, writing nothing, when a task folder, its `start/` or `evaluator/` is missing, when a build or e2e experiment's `intent_form` has no `supplied/<form>/`, when `request.md` is missing for a `shape` or `e2e` experiment (it is optional otherwise, hash null), when the lock is not a list of entries with `name` and `artifact_sha256`, or when a lane has no lock entry.

### Publication marker

Only at publication time, `lanes-export --publish-private` adds `"publication": {"closed": true, "closed_at": "<UTC>", "files": {"<path relative to the round>": "<sha256>"}}` to the round's `PLAN.json`; `hashes` and everything written before the run stay untouched. `files` lists every file under `reproduce/tasks/<task>/evaluator/` (hidden tests included). The export refuses, publishing nothing, when a published `evaluator/` folder no longer hashes to the task's pre-run `hidden_tests`. A re-run keeps the first `closed_at`. The release validator reads this marker (`reproduce/VALIDATION.md`). Adding it changes the file hash of `PLAN.json`; the export therefore rewrites each `records.jsonl` `manifest_sha256` that named the earlier `PLAN.json` to the published file hash.
