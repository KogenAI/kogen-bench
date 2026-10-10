# Kogen Core

Status: contract for the minimal core.

## 1. Purpose and scope

Kogen is a coding agent provided as a `kogen` executable for macOS and Linux: it shapes a caller's request into an Intent, waits for
caller approval, runs one bounded Build, checks its exact candidate, and lands only verified work. The first core uses
ChatGPT only; the command statuses are listed in §3.

Kogen aims to make cheap models produce successful, high-quality
changes; that is a product goal, not a performance guarantee established by this contract.

Where this contract leaves a detail OPEN, the expected values in the scored conformance cases are normative for this race.

## 2. Terms

- **Intent:** Record of a requested change, retaining the verbatim request and shaped requirements and acceptance.
  The first core runs one Build per Intent.
- **Shaper:** Kogen's own ChatGPT-backed role that shapes an Intent. It cannot approve it.
- **Approval:** Caller authorization bound to the exact Intent and acceptance bytes. Changing those bytes invalidates
  that approval.
- **Build:** One bounded, isolated attempt to implement an approved Intent in a private workspace. The initial core
  starts one Build at a time.
- **Candidate:** The exact workspace tree produced by a Build and presented to checks and landing. A Candidate that has
  not passed the required checks is unverified.
- **Check / gate:** A configured deterministic command or approved acceptance check whose result is recorded against the
  candidate tree.
- **Landing:** Applying the verified candidate to the project as one ordinary Git commit.
- **Reserved command:** A command in the CLI contract which the first core does not implement; its name and behavior
  do not change.

## 3. CLI

The command tree below is the CLI contract. This core implements commands marked implemented and reserves commands
marked reserved, with their stated names and behavior unchanged.

```text
kogen init
kogen update
kogen status [<slug>] [--watch] [--json]
kogen intent shape <slug> <request> [--json] [--no-color]
kogen intent approve <slug> [<hash>] [--by <name>]
kogen intent remove <slug> [--force]
kogen queue start [--detach]
kogen queue stop
kogen provider list
kogen provider login chatgpt [--as <label>]
kogen provider logout chatgpt [--as <label>]
kogen provider use chatgpt [--as <label>] [--project <checkout>]
kogen version
kogen help [<command> [<subcommand>]]
```

| Command | First-core behavior | Unresolved details |
|---|---|---|
| `kogen init` | **implemented** — Bare invocation initializes the current Git working tree: create `.kogen/project.yaml`, ignore `.kogen/local/`, detect the documented default checks, and make one commit containing both tracked paths. Print selected checks and the created commit's short SHA and subject, plus the checked-out branch or detached-HEAD state. Detection reads files only and never runs project checks. A valid config already present is a no-op; an invalid one is an error. | Exact diagnostics outside a Git repo: OPEN. |
| `kogen update` | **reserved** | — |
| `kogen status [<slug>] [--watch] [--json]` | **implemented** — Text is the human view: show queue, every non-Landed Intent, and at most five most recently Landed Intents; groups include Building / Queued / Blocked / Failed / Parked / Interrupted / Drafts / Landed. Overview rows show wait/failure reason and latest Build ID/status when available, including queued, draft, and landed rows; Landed rows retain the SHA. Status shows preserved recovery locations and expiry times. Slug detail includes stage times, candidate diff and journal paths. Non-watch overview `--json` is versioned JSON Lines: one `schema:1,type:queue` row (`state,pid,queued,next`), then `schema:1,type:intent` rows in board order (`slug,status,queue_position,reason,build_id,build_status,stage,elapsed_ms,landed_sha,priority,blocks_on,journal,candidate_diff,recovery`; status is building/queued/blocked/failed/parked/interrupted/draft/landed), then `schema:1,type:agent` rows (`id,role,build,status,elapsed_ms,activity,events`). `recovery` is an array of unverified preserved locations, expiry times and expired flags. Missing values are `null`; queue positions are 1-based. `stage` is the latest nonempty `stage` from `model_stage` or `rung` from `rung_started`, and is populated only for Building Intents; unrelated events and terminal or reapproved queued Builds do not supply it. Slug `--json` is one detailed object with `schema:1,type:intent_detail`, including the recovery array. `--watch` is text-only: render immediately, poll every 2 seconds, emit only changed frames, and return when the queue is stopped and no Build or agent is active. Overview returns 0; slug returns 0 if Landed and 1 otherwise; unknown slug returns 2. Ordinary status returns 0 unless inspection fails. | — |
| `kogen intent shape <slug> <request> [--json] [--no-color]` | **implemented** — A request argument equal to `-` reads stdin. Otherwise, resolve it against the invocation directory (unless absolute); a readable regular file is read as a path, and every other value is verbatim inline request text. Thus `-` always means stdin, readable files take precedence over inline text, and missing, unreadable, or non-file path-like values are inline text. Use `--` before inline text that begins with a dash. Do not copy inline text into child-process arguments; Kogen adds no process-list exposure beyond the caller's original argv value. Block until the ChatGPT Shaper returns the shaped Intent or branching questions; print paths, warnings and the approve command. On a TTY, stderr shows one updating progress line with phase, elapsed time, started model-call count and repair count/reason; otherwise emit no progress. `NO_COLOR` and `--no-color` disable color. `--json` suppresses progress and prints exactly one versioned result envelope to stdout on success or failure. | — |
| `kogen intent approve <slug> [<hash>] [--by <name>]` | **implemented** — Without a hash, show the review card with the Intent hash and exact approval command, then return advisory status 5. With a matching prefix of at least 6 hex characters, record caller approval; do not start the queue. | — |
| `kogen intent remove <slug> [--force]` | **implemented** — Removes the Intent files and its approval in one commit. An Intent in a running Build can't be removed. `--force` confirms removing an approved (queued), failed or parked Intent. | — |
| `kogen queue start [--detach]` | **implemented** — Explicitly start the approved queue. The foreground form runs bounded Builds serially, one at a time, until empty or stopped; checks and landing are part of each Build. `--detach` starts the approved queue in the background. | — |
| `kogen queue stop` | **implemented** — Asks the running queue to stop after its current Build. | — |
| `kogen provider list` | **implemented** — Lists saved accounts, whether each is signed in, and the default. | — |
| `kogen provider login chatgpt [--as <label>]` | **implemented** — Sign in with a ChatGPT account under the selected label; defaults to `default`. If the completed login's subject differs from the saved credential, a TTY offers to save it under a new, validated label suggested from the email's local part, or replace the selected label after a separate confirmation. Saving under a new label uses the completed OAuth credential and leaves the old label unchanged. Without a TTY, do not prompt or change saved state; print the exact `login --as` command for the suggested label and the matching `provider use --as` command, then exit 5 (decision needed). Invalid or occupied new labels leave saved credentials unchanged. Never print credential or token contents. | — |
| `kogen provider logout chatgpt [--as <label>]` | **implemented** — Sign out of only the selected ChatGPT account; defaults to `default`. | — |
| `kogen provider use chatgpt [--as <label>] [--project <checkout>]` | **implemented** — Choose the default account, or one project's account. Choices live in `~/.kogen/accounts.yaml` on this machine, never in a repo. | — |
| `kogen version` | **implemented** — Prints `kogen <version> (<short-commit> <UTC-commit-date>)` when Git metadata is available, or `kogen <version> (built <UTC-build-date>)` otherwise. The build date uses `SOURCE_DATE_EPOCH` when set and the UTC build time otherwise; an invalid value or one resolving to the Unix epoch is an error. Never print a zero commit or the Unix epoch date. | — |
| `kogen help [<command> [<subcommand>]]` | **implemented** — Lists commands; run `kogen <command>` to see its subcommands and options. | — |

The CLI contract's argument forms and output conventions are fixed. There are no model/effort flags, and the vocabulary is “Build.” Human results go to stdout and progress goes to stderr. Shape `--json` emits one `v:1` result envelope and no progress or other stdout lines. `--no-color` and `NO_COLOR` suppress color; progress is rendered only when stderr is a TTY.
Exit codes are fixed: 0 done; 1 ran but the result is no (including failed Build, hash mismatch or red check); 2 usage;
3 environment; 4 provider; 5 decision needed (advisory to an authorized caller); 70 Kogen bug; 143 SIGTERM.

Provider login prompts only when stdin and stderr are terminals. The suggested label is normalized from the email local part to the account-label rules, falls back to `chatgpt` when empty, and gets a numeric suffix when already used. A typed new label must also be valid and unused. Replacing a saved label always requires a second explicit confirmation; declining or canceling leaves its credential and profile unchanged. When prompting is unavailable, the decision message names both commands needed to keep and select the new login, and returns exit 5. The OAuth credential already obtained is saved directly under the chosen label; Kogen does not sign in again to save it.

## 4. Lifecycle

### 4.1 Init

Bare `kogen init` creates `.kogen/project.yaml` as strict-subset YAML. The required
`name` is a string and `checks` is a list that may be empty; each check has a unique string `name`, a non-empty
`argv` list of strings (never a shell string), and a positive integer `timeout_ms`. Unknown keys at any level and
duplicate keys are errors; optional settings are accepted only when specified by this contract. The default name is
`project`; init writes the checks detected below, or `checks: []` when no supported marker is present. A valid
config already present makes init a no-op; an invalid one is an error.

Init adds the
`.gitignore` rule `.kogen/local/`. That directory is reserved for machine-local files; init ignores it. Init never
ignores `.kogen/`, which contains tracked project config and Intent data. If `.gitignore` exists, init preserves its
content and ensures the final effective rules ignore `.kogen/local/`. Credentials and workspaces live under the user's
home directory. Init stages exactly `.kogen/project.yaml` and `.gitignore`, then makes one commit containing both.
It detects checks from repository-root files without running project commands. Each generated check has a descriptive
unique name, a command argv vector, and `timeout_ms: 600000`. Init lists the selected checks or reports that none
were detected. A valid config already present is not rediscovered or rewritten. If the init commit fails,
init reports the failure and exits nonzero.

**Non-normative check-discovery examples:** A `Makefile` with an exact `check`
target takes priority and selects only `make check`. Otherwise, `mix.exs` selects `mix format --check-formatted`,
`mix compile --warnings-as-errors`, and `mix test`; it also selects `mix credo --strict` only when `mix.exs` contains
a Credo dependency tuple. `Cargo.toml` selects `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and
`cargo test`. If both stack markers exist and there is no Makefile check target, both sets are selected in
Elixir-then-Rust order. When no Makefile check target exists, init says so and lists the selected stack checks, or
reports that none were detected.

Init's Git operations target the working tree containing the invocation directory, including from a subdirectory or
linked worktree, regardless of inherited Git repository-routing environment variables. It commits on the currently
checked-out branch or advances detached HEAD; successful output includes the short commit SHA and subject and names
that branch or detached-HEAD state.

Init warns that Kogen does not read `AGENTS.md` or `CLAUDE.md`; the files are not banned from the project.

If the repository has no commits, the init commit subject is exactly `Initial commit`; if it already has history, the
subject is `Initialize Kogen project`.

### 4.2 Shape

Kogen's own Shaper uses ChatGPT to turn caller input into an Intent; the caller supplies the task through a file,
stdin, or inline text under §3's exact argument precedence. Inline text remains exactly the single argv value supplied
by the caller and is not forwarded in child-process arguments. Use a file or stdin when the
request should not appear in the caller's process listing. Shaping resolves UX and DX choices, explores relevant
branches, and may leave a few purely technical choices for the Builder. It blocks until it returns an Intent or
questions. Thoroughness does not guarantee Build success.

The Shaper must produce acceptance criteria sufficient to check the requested change. Shaping ends with a result or
branching questions; it never approves. The Shaper resolves UX/DX branches rather than handing those choices to the
Builder. Kogen does not treat repository `AGENTS.md` or `CLAUDE.md` as instructions.

**Non-normative acceptance-adapter examples:** Unless `.kogen/project.yaml` sets `acceptance.adapter`, Kogen selects
Cargo when the project root has `Cargo.toml`,
ExUnit when it has `mix.exs`, and criteria-only acceptance otherwise. An explicit `exunit` adapter is honored only when
the root has `mix.exs`, so projects without that Elixir marker never require `elixir`, `mix` or `erl`. Other explicit
adapters override detection.

**Non-normative Cargo adapter example:** During shaping, the Cargo adapter writes one Rust integration test to
`.kogen/local/acceptance/<slug>.rs`. Each Acceptance id maps to a `#[test]` function named `acceptance_a<n>`, such as
`acceptance_a1`. It stages the source temporarily as
`tests/<slug>.rs` and runs `cargo test --offline --test <slug> --message-format=json`; when `Cargo.lock` exists it
also passes `--locked`. The Shaper writes ordinary integration tests that call the crate's public API directly; it
does not runtime-compile probes, discover rlibs, or use build tricks. A base compile failure is the expected red only
when every primary compiler error is an unresolved item (E0425, E0432, or E0433) in the staged acceptance test;
other base compile errors fail shaping validation. Cargo's target directory is private run state at
`run/reports/cargo-target`, writable under the Build sandbox on macOS and Linux. Configured Cargo checks use the same
private target directory; this keeps Cargo artifacts outside the workspace tree check. An automatically generated
lockfile is removed, and the user's `Cargo.toml` is never edited.

During shaping, incomplete base evidence is an environment problem and cannot reclassify an Acceptance item as red.
Approval copies an executable acceptance source from
`.kogen/local/acceptance/` into the immutable approval package at `.kogen/acceptance/`; the Build installs only its
candidate copy. Shaping ledgers and warnings live under `.kogen/local/intents/<slug>/`, which init ignores. Approval
reads these local artifacts, carries a matching ledger into the immutable approval package, and leaves warning files
local. Criteria-only acceptance keeps the Intent's Acceptance and Verify sections, writes and runs no acceptance
source, and reports once that no acceptance runner exists. Approval and the gate require at least one configured
project check for criteria-only acceptance.

Before acceptance validation, the Shaper runs the selected project formatter only on an acceptance source it
successfully wrote during this shaping run, and uses the formatted bytes as the source of record. A configured
`format` command is passed the generated path, or
has that path appended when it has no `{path}` placeholder. Formatting never targets the Intent Markdown or files the
Shaper did not write. A missing formatter or any non-parse formatter failure is an environment error. Its report names
the command argv, exit code, generated file, and first 12 output lines. A formatter parse error is a content failure the
Shaper may repair once; a second parse error fails shaping without another formatter-driven repair.

**Non-normative formatter examples:** Cargo uses `rustfmt` with the Cargo edition, ExUnit uses `mix format`,
and Rails uses the formatter selected from the Gemfile.

Shaping requests at most `shaping.repair_limit` model repairs per command (default 2, configurable from 0 through 5
in `.kogen/project.yaml`). Every scheduled repair records its reason in the Shape journal and progress output.

### 4.3 Approve

Approval is a separate caller action after shaping and before queue start. It binds the exact Intent and, when present,
the exact acceptance source bytes. Criteria-only approvals record no acceptance path or bytes. Any bound byte change
requires approval again. Approval records the caller's identity; the Shaper cannot approve.

### 4.4 Build

Queue start runs one bounded Build in an isolated workspace under `~/.kogen/workspaces/`. The user’s project checkout
remains separate; isolation must work for any project type. Content must not be passed in process command-line arguments.
The first core has one Builder, no parallel Builds, ladder, escalation, plan stage, auditor, additional automatic repair
strategies, or setup-cache control. Provider overload retries remain on the configured Builder model and stop when the
bounded request budget is exhausted. Within the single bounded Build, the Builder may fix its own failing checks; at landing it may
resolve its own rebase conflict. These are bounded parts of that Build and landing flow, not extra retries, repair
ladders, or escalation.

A Build may edit the candidate, but may not alter the approved Intent or its acceptance. One monotonic Build deadline,
60 minutes by default and configurable per project with `build.budget_ms` or `build.wall_minutes`, covers every Build
stage through landing integration. The Builder stage defaults to 30 minutes as one stage-wide cap; generic children
default to 120 seconds, acceptance to 600 seconds, and configured checks require explicit `timeout_ms`. Provider
requests, retry waits, and supervised children are clipped to their remaining absolute Build or Builder-stage time.
Landing receives no fresh allowance; expiry prevents landing.

Only observable process-control effects are normative (no descendant survives a stop by more than 5 s); the mechanism
text below is guidance, and a helper executable is allowed.

On expiry or cancellation, Kogen sends TERM to each registered child process group, then KILL after a bounded grace.
Only ESRCH confirms that a group is absent; permission and other probe failures remain unconfirmed and prevent
landing. Controller commands and Build children use bounded reaping and output-reader waits; an open pipe or leader
that remains after the cleanup deadline returns unconfirmed cleanup with the log persisted so far. The parent-death
watcher writes a durable confirmed/unconfirmed custody result; it retains its ownership registration when cleanup
cannot be verified. An escaped descendant retaining a pipe forces an unconfirmed bounded return.
Group signalling and probing depend on Unix process-group facilities; unsupported hosts
report process supervision as unavailable. On hosts where process-group probes are denied, cleanup cannot be
confirmed and landing is blocked.

Returned process output is a 16 KiB tail; full process logs have a configurable byte cap through
`build.log_limit_bytes`, 10 MiB by default. The rolling log is updated while the process runs and records stdout and
stderr in observed drain order. On overflow, Kogen keeps a rolling tail and marks the log as truncated without stopping
the child. Linux applies a non-raisable address-space soft and hard limit capped by current host soft and hard limits and reports
setup through a close-on-exec pipe. Other hosts record memory limits as unenforced. Configure the optional limit with
`build.memory_limit_bytes`; no memory limit is configured by default.

### 4.5 Check

Run configured checks and acceptance against the exact candidate tree and retain their results. Checks are controller-run
and cannot be changed by the Builder. Missing, malformed, incomplete, or zero-test evidence is could-not-check: its
Acceptance item status remains distinct from `fail`, it blocks landing, and it is not a code or test failure. A known
failing test or a compiler error with a valid primary span is red. Criteria-only acceptance runs the configured checks without installing or invoking an
acceptance source; those checks must be configured and non-blocking for a verified receipt. Nothing unverified lands.
Init selects these defaults only when creating a missing config; later changes to the configured check list are
explicit project configuration. A valid config already present is not rediscovered or adopted.

Red requires an individually identified failing test or a compiler error with a valid primary span. If test failure
evidence cannot identify the individual failed tests, it is red but cannot be excused by a baseline. Could-not-check
(including timeout, missing or malformed evidence, resolver failure and zero collected tests) blocks landing, cannot
be excused, and is not a code finding. Pass requires exit 0 and complete evidence. Compiler finding identity uses
file, code and normalized diagnostic message, with available source text as added context; it omits line and column.
This conservative identity can fail to excuse a relocated error when its message changes, which blocks safely.
Commands without an evidence adapter retain generic exit-based classification. Check evidence retains both configured
and effective argv. A log that cannot be read completely blocks green and baseline excusing.

**Non-normative compiler/check-adapter examples:** Cargo exit 101 without a primary-span compiler error or completed
test summary is could-not-check at both base and candidate. For `cargo test`, `cargo clippy`, `cargo build`,
`cargo check` and `rustc`, classify from command-specific evidence.
Cargo argv parsing handles global options, `+toolchain`, the subcommand, validated `--message-format` values and
`--`. Malformed Cargo commands block instead of being repaired. The
controller adds or normalizes Cargo's `--message-format=json` option before Cargo's `--` separator, preserving
arguments after that separator. Supported Cargo modes are
JSON output (which the controller requests) with validated `build-finished` records; text-only output is unavailable.
Cargo test also requires every test summary to parse, every observed test target to complete, and at least one
collected test, counting passed, failed, ignored and measured tests but excluding filtered-out tests. The Cargo
acceptance adapter uses this evidence and maps named `acceptance_a<n>` cases to Acceptance ids. A target
with zero collected tests is could-not-check. Test identity includes the Cargo executable target and libtest name;
absent or ambiguous target association blocks baseline excusing.
Warnings do not make an otherwise complete Clippy run red. Direct `rustc` has no Cargo completion record: the controller
requests JSON diagnostics; text
diagnostics are also recognized for compatibility. It passes only when the controller observes a successful process
exit for an invocation naming a Rust source input and requesting compilation; help, version and other non-compiling
invocations are unavailable.

Project-specific timing thresholds and static-analysis suites are not imposed by this core; they may be configured as
checks for a target project.

### 4.6 Land

Use compare-and-swap (CAS) to land the verified candidate. Detect a moved base before publication and after a lost CAS;
fetch the new tip, rebase in the Build's workspace, and rerun checks against the resulting exact tree. A moved-base
integration turn is one Builder repair followed by that gate rerun. A Build may use at most four such turns across all
base movements. After four turns without a landable result, park the candidate and stop. A lost CAS removes the stale
incoming candidate and retries only after rebasing on the new tip, within the same turn cap and Build deadline.

Immediately before creating the commit, recheck that the tree still matches the checked candidate; create it with
ordinary `git commit` using the user's identity and trusted user Git configuration. When the target branch is checked
out in a worktree, publish with `git merge --ff-only` there so Git advances the branch, index, and worktree together,
preserving non-conflicting user edits and unrelated untracked files. An untracked Kogen Intent draft at the landed
path is removed only when its bytes equal the landed file. An acceptance draft under `.kogen/acceptance/` is
removed only when a same-named file in the landed tree has identical bytes. If local changes prevent the
fast-forward, detach that worktree at its previous commit before publishing the branch by CAS; this keeps its HEAD
and index on the old tree. The warning prints a tested recovery command that stashes tracked and untracked changes,
then switches to the landed branch. When the target branch is not checked out, update it by CAS against the expected
base.
The commit runs the user's configured Git hooks, including hooks selected by `core.hooksPath` or stored in the
project's `.git/hooks`. If a hook fails, landing fails, its output is returned to the Build, and the target ref remains
unchanged.

A failed check, missing receipt, changed candidate, or lost CAS must not result in landing. This core
makes no parallel or crash-resume promise.

## 5. Files and state

- `.kogen/` is created by init and contains project config and Intent state. `.kogen/local/` holds ignored shaping
  scratch, including acceptance sources and per-Intent ledgers and warnings; init ignores it. Exact directory tree
  and filenames beyond the paths specified in §4.2 are **OPEN**.
- Init commits `.kogen/project.yaml` and the `.gitignore` change. Credentials never belong in project config.
- Intents remain with the project and retain the verbatim request. Exact serialization and state-transition format are
  **OPEN**.
- Keep enough local state to show Intent/approval/Build/check/landing outcomes through `status`.
- Reconciliation marks a dead Build failed (`crashed`) or interrupted (`interrupted`), unless its landing candidate
  is already reachable from the recorded target branch. A changed, unverified workspace tree is preserved as a
  hook-free internal commit at `refs/kogen/candidates/<run-id>/recovery-<workspace>` using the user's Git identity and
  configuration; use the run archive fallback if ref publication fails. Unchanged workspaces need no preservation.
- Recovery refs and archive files expire after `recovery_retention_days` in `.kogen/project.yaml` (default 14 days).
  Read the setting when recovery is first preserved and persist its expiry time. Reconciliation, including the pass
  run by `status`, removes expired refs and archives and records each deletion in the run journal. Status displays
  each preserved location and its expiry time. Preserved recovery remains unverified; it cannot be approved, queued,
  landed, or resumed. Landing requires a fresh approved Build and its checks.
- Event format beyond the required recovery lifecycle and shaping-repair records is **OPEN**.
- User logins, global default, and project account selections live in `~/.kogen/accounts.yaml` on this machine. The
  project selection takes precedence over the global default. Never put provider account choices or login secrets in
  the repository.
- Build workspaces live under `~/.kogen/workspaces/`.
- Process content is transported without command-line arguments.
- Commits follow the user's git configuration.

## 6. Provider

ChatGPT is the only provider in the first core. The Shaper is Kogen's own role, not a delegated external shaper. No
provider fallback is part of this cut.

The core uses the ChatGPT provider path for its Shaper and Builder. ChatGPT-plan logins call the ChatGPT backend
Responses endpoint (`https://chatgpt.com/backend-api/codex/responses`) with the account ID from the login's ID token;
injected credentials use the same backend route. The Builder uses
`gpt-6-luna` at maximum effort; shaping uses `gpt-6.1-sol` at high effort. There is one Builder and no separate plan
stage or model ladder. Provider overloads retry within the bounded request budget without changing the configured model.

### Test seam

Black-box conformance uses the ordinary executable, a temporary `HOME`, and a temporary Git project. Test inputs do
not bypass approval, checks, deadlines, custody, hooks, or publication. The provider endpoint is abstract in Quint.

- `KOGEN_PROVIDER_URL` overrides the **complete Responses endpoint URL**, not a base to which Kogen appends a path,
  for both injected and owned ChatGPT credentials. It accepts an absolute HTTP or HTTPS URL with a host; an invalid
  URL is a provider error. Unset, the endpoint remains `https://chatgpt.com/backend-api/codex/responses`.
- `KOGEN_AUTH_PATH` selects an injected-auth JSON file, reread before each provider request, instead of saved request
  credentials. Its minimum format is `{"tokens":{"access_token":"header.payload.signature","account_id":"acct-test"}}`.
  Both strings must be nonempty. `payload` is unpadded base64url JSON containing integer `exp` (Unix seconds), strictly
  later than the current wall clock. This injected adapter decodes expiry without verifying the signature; it is not
  an owned login and does not make `provider login` succeed or add a saved account. Invalid, missing, or expired
  injected auth is a provider error. Injected credentials do not refresh after a 401.
- `KOGEN_CREDENTIAL_STORE=file` selects private JSON credentials under
  `$HOME/.kogen/credentials/chatgpt-<label>.json`, avoiding the macOS Keychain; account choices remain in
  `$HOME/.kogen/accounts.yaml`. It changes storage only, not authentication or account selection.
- `KOGEN_AUTH_URL` overrides the OpenID discovery base (Kogen appends `/.well-known/openid-configuration`) for login,
  refresh and revocation. Discovery must still declare issuer `https://auth.openai.com`; endpoint HTTP is allowed
  with this override. The runner supplies a local OpenID fixture and a temporary `open`/`xdg-open` executable on
  `PATH` to follow the printed authorization URL; normal callback/state/PKCE/JWT validation still runs.
- `KOGEN_TIME_SCALE` accepts a positive finite decimal multiplier (suite default `1`). It scales provider request
  timeouts/retry waits, the Builder's stage/request budget, shell-tool default timeout, landing retry waits, and
  authentication wait/lock windows, to at least 1 ms. It does **not** advance the wall clock, scale recovery retention,
  configured check timeouts, the controller's absolute Build budget, or the 2-second status-watch poll. Use a small
  positive `build.budget_ms` and explicit check `timeout_ms` to exercise absolute expiry; no zero-scale semantics are
  promised. A suite must not infer elapsed logical time by dividing arbitrary timestamps by this multiplier.
- `KOGEN_TEST_CLOCK_PATH` selects a runner-owned JSON file `{"now_ms":<nonnegative integer>}`. Kogen rereads it for
  its persisted wall timestamps, recovery preservation/expiry and credential expiry (`now_ms / 1000`, rounded down).
  The runner atomically replaces it to advance time, including in already running processes. It does not replace
  monotonic Build/process deadlines or OS process-start identity. Unset, use the real wall clock; unreadable or
  malformed clock data is an environment error. The suite never edits recovery records to simulate expiry.
- `KOGEN_TEST_BARRIER_DIR` selects a runner-owned directory for three optional pause points:
  `before-candidate-recheck` (before the workspace comparison preceding an ordinary landing commit),
  `before-publication` (after validating the expected base, immediately before the branch publication operation),
  and `after-cas-loss` (after deleting the stale incoming ref, before reading/rebasing onto the replacement tip).
  Only a point with `<point>.arm` present pauses. Kogen atomically writes `arrivals/<ticket>.json` containing
  `point,ticket,run_id,workspace,expected_base,ordinal` (ordinal is 1-based per point and Build), then waits for
  `releases/<ticket>`. Tickets are unique safe filenames. Deadlines continue running; waits are bounded by the
  remaining Build deadline and 30 real seconds, and expiry/cancellation blocks publication. Release resumes normal
  validation; it never supplies a receipt or forces a CAS result. Unset, these points have no effect.

The clock and barrier variables are required test seams. [SEAM-GAPS.md](SEAM-GAPS.md) discusses the seams.
[QUINT-SUITE.md](QUINT-SUITE.md) defines the trace encoding, fixture protocol and observation comparisons.

## 7. Commits and hooks

The trusted origin configuration supplies landing commit settings; the Build workspace cannot override them. Landing
commits run in the Build worktree with the user's own Git identity and Git configuration. Init uses its separate
ordinary `git commit` path. If the repository has no
commits, init's subject is exactly `Initial commit`; if it has history, init's subject is `Initialize Kogen project`.
Successful init output prints that commit's short SHA and subject plus the current branch or detached-HEAD state.
Signing is not required by Kogen: Git invokes the configured signer only when the applicable user configuration enables
signing.

Commits that become user-visible history—landing commits and any commit pushed as branch history—MUST run the user's
Git hooks. If a hook fails, landing stops with the hook output available to the Build repair path, and nothing bypasses
the hook. Internal ref commits (approval, claim and preservation records under `refs/kogen/*`, never pushed as branch
history) MAY skip hooks while following the same trusted Git configuration and user identity. Internal temporary
repositories disable hook phases explicitly.

The first-core landing is one commit. Use a normal subject and only the `Kogen-Intent: <slug>` trailer; do not add AI
attribution. Whether that trailer also appears on init's setup commit is **OPEN**.

## 8. Out of scope

The following are not first-core controls: providers other than ChatGPT; check adoption after init; update; parallel
Builds; multi-domain scheduling; crash resume; cache replay; experimental harnesses; and Linux parity beyond the stated
macOS/Linux target.

Builder ladders and repair strategies, setup cache, context packets, generated edge tests, extra shaping audits,
model escalation, plan stages, automatic retries, and candidate ranking do not decide core behavior or landing eligibility.

Only `kogen update` remains reserved in the CLI contract; `kogen queue start --detach` is implemented.

## 9. OPEN

Each item names an unresolved implementation decision. Open implementation details do not widen the cut.

- **OPEN — Process wrapper:** What supervision mechanism implements the observable effects required in §4.4?
- **OPEN — Build crash:** What additional crash-recovery behavior is required beyond preserving and expiring an unverified Candidate? No crash-resume behavior is promised meanwhile.
- **OPEN — Provider mapping:** How does the ChatGPT model setting map to the provider API and authentication flow beyond the specified ChatGPT backend Responses route for ChatGPT-plan logins?


## OUTCOMES

The questions-only exit code is unscored in race 3.

The table fixes command outcomes. Status names refer to the lifecycle or diagnostic category;
where a case does not inspect a status row or text, that limitation is stated. A required
text token is a literal substring, not a requirement to reproduce the entire diagnostic.

| Situation | Exit code | Status | Required text token |
|---|---:|---|---|
| Absolute Build deadline expires | 1 | `failed` (Build model; status row not asserted) | None asserted |
| Candidate is tampered with before the final recheck | 1 | `failed` (landing model; status row not asserted) | None asserted |
| Invalid project config | 3 | `environment/project_config_invalid`; no Intent status asserted | `environment/project_config_invalid` on stdout in diagnostic cases |
| Could-not-check because a check times out | 1 | `blocked` (Intent); check result `could-not-check` | `could-not-check` on stdout |
| Questions-only shape, Quint fixture (unscored) (unscored) | 5 | `questions`; no Intent or acceptance source | `Choose the greeting language?` on stdout |
| Questions-only shape, Gherkin fixture (unscored) (unscored) | 0 | Questions only; no Intent or acceptance source | `tone` on stdout |
| User pre-commit hook rejects landing | 1 | `failed` (landing model; status row not asserted) | `landing-hook-denied` on stderr in the Quint hook case; no text asserted by the Gherkin case |

Sources: `conformance/cases/quint/build/trace-20271011.itf.json` (deadline),
`conformance/cases/quint/landing/trace-20273013.itf.json` (tampering),
`conformance/cases/quint/config/trace-20264016.itf.json`, `trace-20264017.itf.json`
and `trace-20264047.itf.json` (invalid-config diagnostics),
`conformance/cases/quint/shape/trace-20269010.itf.json` (questions), and
`conformance/cases/quint/landing/trace-20273011.itf.json` (hook).
The source Gherkin scenarios in `conformance/features-src/04-lifecycle.feature`
supply the timeout status/token and the conflicting questions exit;
`conformance/features-src/07-commits.feature` supplies hook exit 1.

The questions-only exit expectations conflict (5 versus 0); neither value is a resolved
universal rule. Other invalid-config cases assert exit 3 without asserting diagnostic text.
All three Build/landing failures above leave the target unpublished; timeout cannot land.


## WIRE

Conformance checks only `/model` and `/reasoning/effort` in requests; instructions, prompts and other request fields are implementation-defined.

The following is the mechanically extracted fake-provider wire vocabulary, not an exact
request template. Legacy fixture predicates for instructions, inputs, tools and
`parallel_tool_calls` do not expand the request comparison boundary above.

### HTTP and requests

- Method: `POST`, JSON body. `KOGEN_PROVIDER_URL` is the complete endpoint URL;
  scripted endpoints end in `/scripts/<escaped-id>/responses`. The smoke case records
  `/v1/responses`; the fake also accepts `/backend-api/codex/responses` and any path
  ending in `/responses`.
- Literal role defaults: Shaper `{"model":"gpt-6.1-sol","reasoning":{"effort":"high"}}`;
  Builder `{"model":"gpt-6-luna","reasoning":{"effort":"max"}}`. The effort literal
  is `max`, not `maximum`.
- Other fields represented in fixtures: `instructions` (string), `input` (conversation
  array; predicates address `/input/1/content/0/text` and `/input/5/content/0/text`),
  `tools` (tool definitions), `stream:true` (smoke case), `parallel_tool_calls:false`,
  and `tool_choice:{"type":"allowed_tools","mode":"auto","tools":[...]}`.
  Allowed-tool entries use `{"type":"function","name":"<tool>"}`. These fields
  illustrate the fixture representation; exact prompts, ordering and tool-definition
  JSON are implementation-defined.

### Tools and arguments

Tool calls in fake responses have `type:"function_call"`, a string `call_id`, string
`name`, and `arguments` containing a JSON-encoded string. Dispatch the decoded arguments
and include the actual tool result in the next provider turn.

| Role | Tool name | Argument object exercised by the scripts |
|---|---|---|
| Shaper | `write` | `{"path":string,"content":string}`; both fields supplied |
| Shaper | `read` | Listed as permitted; no call or argument schema supplied |
| Shaper | `search` | Listed as permitted; no call or argument schema supplied |
| Builder | `shell` | `{"cmd":string}`; `cmd` supplied |
| Builder | `finish` | `{}` |
| Builder | `tool_output` | Listed as permitted by Quint; no call or argument schema supplied |

These are observed argument shapes. The extracted sources do not supply formal
`parameters` schemas, optional fields, or additional-property rules. Gherkin Builder
fixtures require `shell` and `finish`; Quint builders also list `tool_output`.

### Headers and identity

- Request header in script manifests: `Content-Type: application/json`.
  The smoke case observes `Authorization: Bearer kogen-fake-access-old`, then
  `Authorization: Bearer kogen-fake-access` after owned credential refresh.
- Injected auth supplies `tokens.access_token` and `tokens.account_id`; FAKES uses
  account `acct-test`. Saved-login fixtures distinguish `acct-default` and
  `acct-research`. The research-account check looks for `acct-research` in request
  headers (or its distinct synthetic access token); it does not pin an account-header
  name. No account-header spelling is defined in the extracted scripts/manifests.
- The signed ID-token claim for the account is
  `claims["https://api.openai.com/auth"]["chatgpt_account_id"]`
  (JSON Pointer `/https:~1~1api.openai.com~1auth/chatgpt_account_id`).
  OIDC fixtures also include `iss`, `sub`, `aud`, `iat`, `exp`, `email` and `nonce`;
  their issuer is `https://auth.openai.com`. Normal signature, issuer, expiry,
  state, nonce and PKCE validation still apply.
- Successful response header: `Content-Type: text/event-stream`. The fake's generated
  streams also send `Cache-Control: no-cache` and `Connection: close`.

### SSE and Shaper output

Frames are `event: <type>\ndata: <JSON>\n\n`; HTTP chunks need not align with frames.
Quint scripts emit `response.completed`; the generated smoke/Gherkin streams also emit
`response.output_item.done` before completion:

| Event type | JSON payload fields |
|---|---|
| `response.output_item.done` | `type`, `item` (one output item) |
| `response.completed` | `type`, `response:{id,status:"completed",output:[...]}`; `model`, `object` and `usage` occur in some fixtures |

Output items are either `function_call` as above (sometimes with `status:"completed"`),
or `{"type":"message","role":"assistant","content":[{"type":"output_text","text":string}]}`.
Generated message items additionally carry `id`, `status:"completed"` and
`annotations:[]`. Usage fields are `input_tokens`, `output_tokens`, optional
`input_tokens_details.cached_tokens`, `output_tokens_details.reasoning_tokens` and
`total_tokens`; some completions omit usage entirely. Malformed-SSE fixtures deliberately
send invalid JSON and are not successful completions.

The Shaper does not return a dedicated JSON Intent object in these scripts. It writes
`.kogen/intents/<slug>/intent.md` through `write`, optionally writes an acceptance source
under `.kogen/local/acceptance/`, then returns assistant text. The Intent content is
Markdown with YAML frontmatter `title` (string), `size` (`small` in the fixtures),
`domains` (string list), a brief, and `## Acceptance`, `## Verify`, `## Notes` sections.
Acceptance uses `- A1: ...`; Verify maps that ID with `- A1: test domain=app`; Notes
starts with `Approach:`. Criteria-only fixtures write no acceptance source. Questions-only
fixtures return assistant `output_text` with a branching question and make no Intent or
acceptance-source write. Neither payload approves an Intent.

Extraction sources: `spec/features/FAKES.md`, `spec/quint/intent.qnt`'s `fixtureTurn`
and script builders, decoded `scripts` in `conformance/cases/**/*.manifest.json`,
`conformance/cases/04-shape-approve-queue-land.json`, and the fake/script builders in
`conformance/kogen_conformance/fake_provider.py` and `gherkin_runner.py`.
