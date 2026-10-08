# 3. Shaping, approval and the Build

Constants live in [data/constants.json](data/constants.json); model ids are configuration (§2.3).

## 3.0 Rules
**Build invariants (decisions dated 5 Oct 2026).**
1. Doubt belongs in **shaping**, where a human or the calling agent can still decide.
2. A Build that has started **MUST finish**: no re-plan, no return to shaping.
3. A Build's only levers are **repair**, **fresh attempt**, **next rung**, **provider retry** and **best candidate**.
4. Success comes first; checks keep the Build in its lane rather than walling it in.

**Resolved calls (5 Oct).**
1. An Intent whose only failures are tests the auditor demoted **lands by default** (`build.land: green-or-advisory`; `green` opts out).
2. There is **no Intent without acceptance tests**: at least one change item (`no_change_item` lint error).
3. Feasibility concerns are shaping **warnings**, not an exit code.
4. A host that cannot confine **builds unconfined with a warning** (§5.3).

**Ends of a started Build.**

| Status | Meaning | Intent afterwards |
|---|---|---|
| `landed` | a landable candidate landed | landed |
| `failed` | no landable candidate; best candidate on `refs/kogen/parked/<run_id>` | failed (re-approve to retry) |
| `parked` | a landable candidate could not be landed (moved-base repairs or landing retries exhausted) | parked |
| `stopped` | stopped **without judging the Intent**: login, provider outage, setup failing twice, acceptance runner unavailable on the base, Kogen bug | stays queued; the drain stops |

## 3.1 The recipe: `ladder`
The default `build.recipe` is `ladder`. These names are accepted. Any ladder name may end in `+edge`.

| Name | What changes |
|---|---|
| `ladder` | four rungs below |
| `ladder-diverse` | the second rung is `sol-medium-raw` and receives no plan |
| `ladder-luna`, `ladder-sol-low`, `ladder-sol-medium`, `ladder-sol-high` | every rung uses that one builder model; rung names are `builder`, `fresh-2`, `fresh-3`, `raw-request` |
| `plan-shell` | one builder stage, no later rung. An environment failure fails the stage. |
| `staged` | adds a context stage before the plan and a review stage before commit |
| `direct`, `direct-escalate` | no plan stage. The builder gets `read`, `search`, `edit`, and `write` as well as `shell`. |
| `direct-shell`, `escalate-shell` | no plan stage. The builder is shell-only. |

`edit` replaces one exact unique `old_text` with `new_text`. `write` creates or replaces a file and refuses a file that already has more than 200 lines. An unknown recipe fails project load. The message contains `build.recipe must be one of` and the rejected value.

The default ladder:

| Rung | Name | Builder | Input |
|---|---|---|---|
| 1 | `builder` | `gpt-6-luna/max` | the plan |
| 2 | `sol-medium` | `gpt-6.1-sol/medium` | the plan |
| 3 | `sol-high` | `gpt-6.1-sol/high` | the plan |
| 4 | `raw-request` | `gpt-6.1-sol/high` | the Request and Acceptance only. This rung is experimental. |

- **One wall.** The Build wall is **60 min** (`3_600_000` ms), or `build.wall_minutes`. Each stage wall is the time remaining, capped at **30 min**. There is no separate 20/12/12 minute rung wall.
- **Plan.** It is made once, before the first rung. The planner is `gpt-6.1-sol/high`, with no tools and no model fallback. Its input is the Intent bytes and `git ls-files` (≤ 160,000 characters). The request wall is **900 s**. It answers with a first line `Difficulty: easy|hard` and then `## Acceptance criteria`, `## Technical approach`, `## Implementation steps`. `build.plan_max_words` defaults to **500** and must be an integer from **300** to **2000**. The project value wins over the machine value. Words are whitespace-separated. The wrapper text counts with the plan.
- **Hard.** The default is parallel. `Difficulty: hard` starts rung 1 and rung 2 together. A green member is the one that commits. If both are red, the ladder continues from the better member. `on_hard: skip_first` is not the default.
- **Easy.** Rungs run in order. A rung that is not landable escalates to the next one. Later rungs still receive the plan, except `raw-request`.
- **Repeats.** After rung 4, attempts cycle from rung index 2 (`sol-high`, then `raw-request`) as `sol-high-2`, `raw-request-2`, and so on, until the wall. `repeat_from` null ends after the last rung. That is not the default.
- **Fresh workspace.** Every rung starts from the build base. Every rung sees the Intent, the acceptance output on the base, and summaries of earlier rungs. It does not see their diffs.
- **Shell.** Ladder and other shell recipes give the builder `shell`, `finish`, and `tool_output` (§4.7).
- **Edge.** `+edge` or `build.edge_tests: true` generates tests from the Request and runs them before landing. A failure blocks landing. Two or more green parallel rungs each run the other's tests before selection.
- **Auditor role.** `gpt-6.1-sol/high` (§3.8.2).

## 3.2 Shaping (`intent shape`)
### 3.2.1 Conversations
Shaping is a small ladder of its own.
- **Passes 1–3:** role `shaper`, in one conversation (the first pass plus up to 2 repairs).
- **Passes 4–6:** role `fallback_shaper` (`gpt-6.1-sol/high`), in a fresh conversation that also gets the last failure.
- **Limits:** 60 model turns per conversation; no wall limit; provider retries per §4.5.
- **Tools:** `read`, `search`, and `write`, with `write` restricted to the Intent and the acceptance source (≤ 200,000 bytes).
- **System prompt:** contains `You are Kogen Intent shaper.`
- **First message (exact):**
```
Slug: <slug>

Configured project domains: <sorted, comma-joined>. Use only these names in the Intent and Verify lines.

Effective gate paths: <`p1`, `p2`…>. Set `changes_gate: true` only when the task or planned changes require modifying one of these paths. Omit it for unrelated changes; running or inspecting checks alone does not count.

Task statement:
<request>

Write the Intent to `.kogen/intents/<slug>/intent.md` and its acceptance test to `<acceptance source path>`.
```
- **Layout** (settled v1.1, reference): gate paths are sorted by byte order; the request bytes follow `Task statement:\n` verbatim and are followed by `\n\n`, then the `Write the Intent …` line.
- **Fallback shaper** (passes 4–6) uses the same system prompt and marker; it is told apart by its model and its fresh conversation.
- **End of a pass.** A pass ends on a response with **no tool calls**. If a file is still missing at that point, Kogen answers `Both files must exist before you finish. Missing: <path>.` and the pass continues. This finish guard does not spend a repair.
### 3.2.2 Pre-steps
Validate the slug, load the project, delete stale shape artefacts, and run `setup` (sandboxed, cached by `HEAD^{tree}`). A setup failure exits 3.
### 3.2.3 Validation (each pass, in order)
1. **Normalise:**
   - `approach:` at the start of Notes (any case) becomes `Approach: `.
   - Notes of ≥ 8 words that start with an action verb get the `Approach: ` prefix.
   - Drop any `## Request` the model wrote, then append `\n` (if the bytes end with `\n`, else `\n\n`) + `## Request\n` + the request bytes.
2. **Parse and lint.** Errors → candidate `intent_parse_failed` / `intent_lint_failed`.
   - **Style** findings are sent back as a repair that does **not** count against the pass budget, at most 2 times per conversation; anything left over becomes a `lint_<rule>` warning.
3. **Gate declaration.** If the Notes or the test name an effective gate path without `changes_gate: true` → `undeclared_gate_path`.
4. **Format** the written files with the formatter argv. A missing formatter is a warning only: the progress line `shaper pass=<n> role=<role> warning formatter_unavailable` (settled v1.1; a progress line, so §1.1 allows it).
5. **Acceptance checks.** Stage the test at its candidate path and run `acceptance_checks`:
   - red → candidate repair;
   - 126/127 → exit 3;
   - the tree must be unchanged → otherwise `tree_mutated`.
6. **Red on base and reclassification.** Run the tests on the checkout.
   - `test keep` items with a failed row become `test`; `test` items whose rows all pass become `test keep`. Each direction gets one `shape_reclassified` warning, and the file is rewritten.
   - At least one `test` item must then be fully red, else candidate `all_items_keep`.
   - Any other base rule violation → candidate repair.
7. **Requirement ledger and coverage (core).**
   - One request to role `auditor` (system prompt contains `You are Kogen's requirement auditor.`). It lists every atomic constraint of the Request, mapped to an item id or `untestable: <reason>`. Reply: `{"rows":[{"constraint","maps_to"}]}`, the shape of `ledger.json` (settled v1.1).
   - Kogen then checks that every number, backticked identifier and quoted string in the Request appears in some ledger row, and that every row maps to an existing item.
   - Gaps → one repair (`candidate/coverage_gap`, listing them). Gaps still there after it become `coverage_gap` warnings. The ledger and the audit run in every pass that reaches step 7 (settled v1.1).
   - The ledger is saved to `ledger.json`.
8. **Shaping test audit (core).**
   - One request to role `auditor` (`You are Kogen's acceptance test auditor.`). Input: the Request, the Intent, the test source, and each item's base output.
   - Output: `{"items":[{"id","verdict":"valid|over_strict|infeasible","citation","reason"}]}`.
   - Non-valid items with a valid citation (§3.8.2) → one repair asking for a test that follows the Request. Verdicts still non-valid after it become `audit_<verdict>` warnings. A non-valid verdict without a valid citation gets no repair but still becomes an `audit_<verdict>` warning (concerns are warnings, resolved call 3; settled v1.1).
9. **Restore** the staged path.

The ledger and the shaping audit run once the earlier steps pass. Their repairs count against the pass budget.
### 3.2.4 Repair message (exact)
```
Validation failed. Repair the generated files in this conversation. The required paths and their current state are:
- `<path>`: present on disk. Keep it in place; change it only if the failure below requires a correction.
- `<path>`: missing or unreadable. Write it during this repair pass at this exact path.
Both exact paths must exist after this pass. Every missing path must be written now. Do not delete required files. The available tools can read, search, and write files; they cannot remove them. Preserve present content unless the failure below requires a focused correction.

Exact failure output:

<class>/<reason>: <detail>
```
### 3.2.5 Results
- **Valid** → exit 0. `shape-warnings.json` is written; nothing is committed.
- **Pass budget used up** → exit 1: `candidate/<reason>: Shaper repair limit reached for <reason> after <n> pass(es) and <m> model call(s).` followed by the last failure.
- **Turn limit** → `candidate/shape_turn_limit: Shaper exhausted its turn limit.`, exit 1.
### 3.2.6 Concerns and progress
- **Concerns.** The text of each pass's final response is scanned for a `Concerns:` line followed by `- <concern>` lines. Each distinct concern (exact text) becomes a `feasibility_concern` warning with empty `item_ids`. Concerns never fail shaping.
- **stderr progress:** `shaper pass=<n> role=<role> <event>`, where `<event>` is `started` · `complete turns=<t>` · `validation_failed reason=<r>` · `style_repair` · `fallback_started` · `validation_passed` · `warning <code>`.
### 3.2.7 Witness path (target contract; pending measurement)
This mode is enabled by `shaping.proof: witness`, which is not the default. It becomes the default only when the shaping-guarantee adopt rule passes (research/shaping-guarantee §5: post-approval failures fall, end-to-end non-inferior, yield ≥ 95 %).
- **Witness Build.** After validation, shaping runs a witness Build: the ladder's R1 (with R2 on `hard`), the real gate, and the real sandbox, in a throwaway workspace from the approved base, with no audit demotion.
- **Red witness.** Each failing assertion goes to the auditor (`TEST-WRONG` → repair the test and re-run; `WITNESS-WRONG` → keep the test, repair the witness; `UNDECIDED` → `feasibility_concern`). This is limited to `shaping.witness_rounds` (default 2). The adjudication is one tool-less request with the test-auditor marker; reply `{"items":[{"id","verdict":"TEST-WRONG|WITNESS-WRONG|UNDECIDED","citation","reason"}]}` (settled v1.1).
- **Feasibility.** `PROVEN` = a green witness with no open verdict. `PROVEN with concerns` = green, with concerns. Anything else is `UNPROVEN`.
- **Approval.** `intent approve` refuses `UNPROVEN` (`intent/unproven`, exit 1). The approval binds the witness commit and its diff hash (§2.5.1).
- **Build.** Step B3 (§3.4) re-verifies the witness on the build base with no model call and lands it if it is `green`. Otherwise the ladder runs as usual. In this mode the Build never demotes tests.

### 3.2.8 Assumption recheck
Optional frontmatter `assumptions` and `shared_contracts` are lists of `{name, path, contains}`. `contains` is a short observable sentence, not a hash of the whole file. Approval checks each `path` on the base and requires `contains` to be present. Before a Build, every `blocks_on` slug must have landed on that branch. A match records `shaping_rechecked`. A missing or changed predicate records `shaping_stale` and the Build does not start. Status keeps that explanation. Edits elsewhere in the file do not stale the predicate. An Intent with no predicates skips this check. No new shaping pass runs after the Build has started.

## 3.3 Approval checks
These run in the checkout and its scratch run dir:
1. Setup.
2. Every configured check once, giving a **baseline** row per check: status `green|red|unavailable|timeout|mutating`, exit status, and finding identities.
3. Each acceptance check on the staged test. A red check refuses approval (exit 1); 126/127 → exit 3.
4. Remove the staged file.

The baseline is cached by (base tree, setup, checks, child env), so the card call and the hash call run the checks only once. Red baseline checks warn and never block.

## 3.4 Build orchestration
The drain runs these steps in order. Events in brackets are required in this order; a test asserts them as a subsequence.

| Step | Action | Events | Next |
|---|---|---|---|
| B0 | Load the approval (invalid → `controller/approval_invalid`, stopped). If the target branch ≠ the drain's base → `skipped`. Take the claim (held by a live run → drain stops `environment/build_already_claimed`). | — | B1 |
| B1 | Run dir, `run.json`; sandbox probe (§5.3) | `started`, [`sandbox_unavailable`] | B2 |
| B2 | Build base = origin tip. If it moved: record it, then run every check once there and merge into the baseline. | [`base_moved_at_start`] | B3 or B4 |
| B3 | Witness mode only: apply the witness commit on the build base and verify it. `green` → B9; else B4. | `verification` | |
| B4 | Plan (§3.1). A stale assumption (§3.2.8) stops before this step. | `plan`, `model_stage` | B5. Hard starts the first two rungs together. |
| B5 | Rung Rn: fresh workspace, setup (failure retried once, then stopped `environment/setup_failed`), install Intent and test, base acceptance (first rung only; runner unavailable → stopped `environment/tool_missing`), then develop/verify/repair (§3.5). The auditor runs inside a red acceptance-only rung (§3.8.2). | `rung_started`, [`base_acceptance`], `model_stage`…, `verification`…, [`repair`…], [`acceptance_demoted`], `rung_finished` | B7 |
| B6 | Re-score Rn after demotions made inside the rung. | — | B7 |
| B7 | Rn landable → B9. A next rung exists and budget is left → B5. Else → B8. | — | |
| B8 | Select the best candidate across rungs (§3.8.3) and record its verdict | `selection` | B10 (`failed`) |
| B9 | Commit, moved-base handling, landing (§3.9) | `commit_result`, `landing_prepared`, [`landing_retry`…] | B10 (`landed` or `parked`) |
| B10 | Push the best candidate to `refs/kogen/parked/<run_id>` unless landed; destroy all workspaces; release the claim | `finished` | — |

- **Budget.** B4–B6 spend the Build budget (`build.budget_ms`, default 60 min). Provider waits (§4.5) pause the clock.
- **Budget runs out.** The in-flight stage is cancelled, the current tree is verified and snapshotted, and the Build goes to B7 with no next rung. Diffs are never discarded.
- **Landing.** B9's model repairs use a separate landing allowance (10 min); its deterministic steps are not time-limited.
- **Stopping.** A stop condition (§3.0) at any step goes straight to B10 with status `stopped`. Rung snapshots already made stay on their refs.
- **Before a Build starts.** Nothing refuses it except B0. A moved base, base-red checks, and items already green on a moved base are absorbed (§3.7).

## 3.5 The rung machine
A pure step function `step(state, event) → (state, effects)` is recommended. Only the journal is observed.

| State | Event | Next |
|---|---|---|
| develop | done claim | verify |
| develop | turn cap (60) or rung wall | verify the current tree; rung ends `turn_cap` / `wall_cap` |
| develop | 4th protected restore | rung ends `protected_restore_limit` |
| verify | result `green` | rung ends `green` |
| verify | result `red` | progress check, then `repair` |
| develop | after a repair, the tree equals the pre-repair tree | rung ends `unchanged` |
| any | budget out | verify; rung ends `budget` |
| any | provider failure after §4.5 | rung ends `provider/<class>`, or stopped for login and outage |

**Repairs.** The ladder allows **6** repairs in a rung. The **count** of a red verification = distinct identities in non-excused red checks + non-excused red checks without identities + failing undemoted items. A count that is not strictly lower than the previous red count ends the rung as `no_progress`. When the red result has no count, the second such repair ends the rung the same way. `repair_cap` is the name when the 6 are spent. On `plan-shell`, an environment failure fails the stage. On the ladder, `check_unavailable` is fed back as a repair, and `protected_restore_limit` escalates.

## 3.6 Developer messages
- **System prompt.** It contains `You are Kogen's builder.` and says:
  - implement the approved Intent;
  - Intent and test files are read-only;
  - `## Request` is context, and the Acceptance section is the gate;
  - the plan is advice;
  - add no dependencies the Intent does not ask for;
  - ignore AGENTS.md and CLAUDE.md;
  - call `finish` alone with `{}` when the implementation and the targeted checks are done. Text alone does not finish the Build.
- **First user message:**
```
Approved Intent:
<intent bytes>

Acceptance on the base:
<per item: A<n> (<test|test keep>): <passed|failed> — first 5 lines of its output>

<"Implementation plan:\n<plan>" | "No implementation plan was supplied.">

Earlier attempts:                                 ← from the second rung on
<per rung: R<n> <model>: <end reason>; ≤ 5 lines of ≤ 180 chars of its last failures>

Repairs available: <repairs_left>. Begin work in the supplied worktree.
```
- **Completion.** The only completion is tool `finish` alone with `{}` (§4.7). A text-only reply is progress. Kogen appends: `Continue the entire approved Intent with the next useful tool call. Brief progress text does not finish the Build; call finish alone with {} when implementation and targeted verification are complete.`
- **Empty finish.** The first `finish` with no implementation change gets `Kogen found no changed files. Make the requested change before claiming done.` The second empty `finish` runs the gate anyway.
- **Protected files.** After each tool batch the restorer runs (§3.9.4). Each restored path appends `You changed <path>; acceptance tests and the Intent are read-only and have been restored. Make the implementation satisfy them.`
- **Turn budget note.** It is one appended user item, not a change to `instructions` (§4.9.2). The text is `System note: <N> turns remain. Run the targeted tests now and finish the smallest complete change.`
- **Repair message.** `Kogen's controller reported this failure. Continue the same session and fix it:\n\n<feedback>` (§3.7.3).

## 3.7 Verification and base-relative checks
### 3.7.1 Composition
A verification of the workspace tree:
1. Every `fix` command, once. A non-zero exit is a red finding `fix/<name>`.
2. Every `check`, in order, each with its own `timeout_ms`.
3. The acceptance tests.

The tree after step 1 is the verified tree T, and receipts bind to T. Steps 2 and 3 must not change T. An excused mutating check's writes are reverted.
### 3.7.2 Status of each check, and excusing
| Status | When |
|---|---|
| `unavailable` | exit 126/127, executable not found, no exit status, or the adapter's `unavailable` signal |
| `timeout` | deadline reached |
| `mutating` | T changed |
| `red` | any other non-zero exit |
| `green` | exit 0, T unchanged |

A check is **excused** when its baseline status is not `green`, its current status equals the baseline status, and either:
- both sides have identities and the current set ⊆ the baseline set; or
- they do not, and the exit status is the same.

An excused check never blocks `green`. It is recorded as `excused` and listed as a warning in the feedback and the report. A same-seed flake retry runs once. If that retry passes, up to **two** tests that also fail on the base are excused. The evidence (retry, base result, excused ids) is stored on the run. If the evidence cannot be stored, the check stays red. A non-excused check that is not `green` makes the verification **red**. On the ladder an unavailable tool is repair feedback (§3.5). The messages are:
- unavailable now but not on the base: `<argv0> is not available, but it ran on the base`;
- timeout: `timed out after <s> s` plus the tail;
- mutating: the changed paths.

A verification is **green** when every non-excused check is green and every undemoted acceptance item passes.
### 3.7.3 Feedback
1. Up to 10 findings per tool and 20 in total, each `path:line:col: error: [tool/rule] symbol: message` (message ≤ 200 characters), followed by `… <N> more <tool> findings`.
2. `raw log: <path>` for each failing command.
3. `raw tail (first failed step <name>):` with its last 8 lines (≤ 600 characters). The temp dir is written as `$TMPDIR` and the home dir as `$HOME`.
4. One line per failing undemoted item: `acceptance <id>: <status>`.
5. Excused checks: `Base-red warning: check "<name>" still has only findings recorded at approval.`
6. A last line: `gate: <E> errors, <W> warnings (<tool counts>); checks <name>=<status>, …; acceptance <passed>/<total>`.

The full finding list is also written to `gate-findings-<id>.json` in the run dir. Dialyzer output is shortened before the builder sees it. The file keeps the full text. Landing details never reach the model.

### 3.7.4 Advice that does not change the gate
These may be shown to the builder or on status. None of them changes pass, fail, or land.
- **Check proposals.** Repeated gate text can become a stored proposal. Status lists it as `candidate checks (caller approval required): <paths>`. A later run records whether the proposal was adopted. Adopting it is a human edit of project config, not an automatic gate change.
- **Quality advice.** Elixir source notes, duplicated functions, a bounded mutation of changed lines, reach of the change, and tests that copy implementation text are advice beside the gate.
- **Mutation advice** on a red gate uses cache epoch `mutation-advice` (§4.9.1). It is appended. It is not a verdict.
- **Scratch tests.** Tests the builder wrote outside the acceptance file run as warnings. They do not count as acceptance items.

## 3.8 Verdict, audit, selection
### 3.8.1 Verdicts
| Verdict | Non-excused checks | Undemoted items | Demoted items | Lands with `green-or-advisory` (default) / `green` |
|---|---|---|---|---|
| `green` | all green | all pass | all pass | yes / yes |
| `green-with-advisory-tests` | all green | all pass | ≥ 1 fails | yes / no |
| `unverified` | anything else | | | no / no |
| `none` | no verified tree | | | no / no |

A candidate is **landable** only if, on top of the table, ≥ 1 undemoted **change** item passes. The auditor can therefore never vote a candidate in alone. A verified tree whose implementation diff is empty but which is `green` lands as an Intent-and-test-only commit (the work was already on a moved base).
### 3.8.2 Build auditor
- **When.** Inside the rung, before repair, when the gate is red only because acceptance items failed.
- **Request.** Role `auditor` (test-auditor marker, §4.8.2), one request with no tools. Input: the failing ids, the verbatim Request, the test source, the failure output, and the candidate diff. The diff clip is **60,000** characters.
- **Output.** `{"items":[{"id","verdict":"valid|over_strict|contradicts","reason"}]}`.
- **Demotion.** `over_strict` and `contradicts` demote the item for the rest of the Build. There is no citation field. A missing or garbled item stays `valid` and is not demoted. `valid` means the test matches the Request, so the candidate is wrong.
- **Scope.** The rung is re-scored after demotion. The auditor is disabled in witness mode. Journal events are `acceptance_demoted` and `acceptance_upheld`.
### 3.8.3 Selector
**Candidates** are the rung snapshots. Rank them by, in order:
1. most passing undemoted items;
2. fewest blocking findings (the §3.5 count);
3. smallest implementation diff (added + removed lines);
4. earliest rung.

The winner is emitted even if it is `unverified`. There is no model judge. When parallel rungs ran each other's tests (§3.1), those scores are part of the ranking.

## 3.9 Commit and landing
### 3.9.1 Commit
In the winning workspace:
1. Squash onto the build base: `reset --soft` if the builder committed, then `add -A`.
2. Commit with the §2.5.4 message; no hooks.
### 3.9.2 Moved base
1. Fetch the tip and rebase in the workspace.
2. Re-run the guard and a full verification.
3. A conflict or red result becomes a repair for the winning rung's builder, in the same conversation, naming the conflicting paths or the findings. These repairs use the landing allowance; their number is bounded by the allowance alone (settled v1.1). This matches research/executable-specs (landing.qnt after the 5 Oct fix): a moved base never parks a candidate by itself; only an impossible rebase or a red result after the repairs does.
4. Not landable afterwards → `parked`.
### 3.9.3 CAS
1. Record `landing_prepared` and set `run.json.landing`.
2. Refuse if `refs/heads/<base>.lock` exists, if HEAD's sole parent is not the expected parent, or if HEAD's tree is not the verified tree.
3. Push to `refs/kogen/incoming/<run_id>`.
4. Run `update-ref refs/heads/<base> <new> <expected>`.
5. Update every clean checked-out worktree of the base. A dirty one gets a `landing_warning` and the stderr line `land: warning: landed <sha> on <branch>; your checkout at <path> has local changes and was not updated; run \`git reset --keep <sha>\`, or merge it yourself`.
6. CAS-delete the incoming ref. A failure here is a `cleanup_failure` event, not a failed Build.

**Failure handling.**
- A present `.lock` or a lost CAS is **transient**: retry after 1 s, 2 s, 4 s (`landing_retry`), then follow the §3.9.2 path. If it still cannot land → `parked`.
- `not_fast_forward` and `tree_mismatch` are Kogen bugs → stopped `controller/*`.
### 3.9.4 Protection during a Build
- **Refusal.** `write`/`edit` (shaper only) refuse manifest paths with `ERROR: <rel> is approved and protected; change the implementation instead.`
- **Restorer.** After every tool batch it restores mismatching manifest paths (from the approval bytes or the build base), deletes paths that must stay absent, and deletes the acceptance source copy.
- **Guard.** It checks the manifest before each verification and before the commit; a mismatch is a red finding `protected/<path>`.
- **Scope.** Paths outside the Intent's domains are `scope_warning`s only.

## 3.10 Recovery
This runs before `status` and before each drain step. A run is **dead** when it is `running` and its owner pid is not alive, or the pid is alive with a different start time. For each dead run:
- If its `landing.candidate_commit` is on the base → `reconciled{landed}`.
- Else → `finished{failed, reason: interrupted}` when its last event is `interrupted`, otherwise `reason: crashed`.

In both cases, release the claim if owned and destroy its workspaces. Crashed and interrupted Builds leave the queue until re-approved (features/24).

## 3.11 Queue and drain
- **Queue.** It is computed from statuses (§2.11).
- **Lock.** `queue.pid` holds `<pid>\n`, created exclusively. A dead pid is taken over (2 attempts). Acquiring deletes `queue.stop`. Only the owner releases it.
- **Loop.**
  1. Recover, then derive statuses.
  2. If `queue.stop` exists → stop on request.
  3. Take the next queued approval (§2.11) not yet attempted in this drain. A blocked Intent is not taken.
  4. Print `building <slug>` and run the Build.
  5. Print the outcome line (§1.7.4).
- **After each Build.**
  - `landed`, `failed` and `parked` → continue with the next approval.
  - `stopped` → end the drain with that class's exit code; the Intent stays queued.
- A provider error that fails one Intent after its available rung/repair attempts is a `failed` Build; the drain continues. `stopped` for provider means a login, usage-limit, or outage condition that prevents the drain from doing useful work, not one recoverable request error (D20).
- **Provider outages never fail an Intent (§4.5).**
  - A usage limit waits for the reset with the budget paused.
  - A login failure stops the drain.
  - An outage longer than the outage window stops the drain.
