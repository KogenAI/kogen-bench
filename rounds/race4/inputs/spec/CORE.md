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
| `kogen provider use chatgpt [--as <label>] [--project <checkout>]` | **implemented** — Choose the default account, or one project's account. Choices live in `$HOME/.kogen/accounts.yaml` on this machine, never in a repo. | — |
| `kogen version` | **implemented** — Prints `kogen <version> (<short-commit> <UTC-commit-date>)` when Git metadata is available, or `kogen <version> (built <UTC-build-date>)` otherwise. The build date uses `SOURCE_DATE_EPOCH` when set and the UTC build time otherwise; an invalid value or one resolving to the Unix epoch is an error. Never print a zero commit or the Unix epoch date. | — |
| `kogen help [<command> [<subcommand>]]` | **implemented** — Lists commands; run `kogen <command>` to see its subcommands and options. | — |

The CLI contract's argument forms and output conventions are fixed. There are no model/effort flags, and the vocabulary is “Build.” Human results go to stdout and progress goes to stderr. Shape `--json` emits one `v:1` result envelope and no progress or other stdout lines. `--no-color` and `NO_COLOR` suppress color; progress is rendered only when stderr is a TTY.
Exit codes are fixed: 0 done; 1 ran but the result is no (including failed Build, hash mismatch or red check); 2 usage;
3 environment; 4 provider; 5 decision needed (advisory to an authorized caller); 70 Kogen bug; 143 SIGTERM.

Provider login prompts only when stdin and stderr are terminals. The suggested label is normalized from the email local part to the account-label rules, falls back to `chatgpt` when empty, and gets a numeric suffix when already used. A typed new label must also be valid and unused. Replacing a saved label always requires a second explicit confirmation; declining or canceling leaves its credential and profile unchanged. When prompting is unavailable, the decision message names both commands needed to keep and select the new login, and returns exit 5. The OAuth credential already obtained is saved directly under the chosen label; Kogen does not sign in again to save it.


#### G1: CORE §3 and §4.2 — Questions-only shaping

A Shaper response consisting only of branching questions returns exit **5** (decision needed). In human output, print the questions to stdout in their returned order, one per line, with no Intent-success card or approval instruction. Do not create an Intent, acceptance source, or approval package for that response. This rule replaces both conflicting questions-only rows and the statements that questions-only exits are unscored in CORE's OUTCOMES section. In the greeting fixture the entire stdout is `Choose the greeting language?` followed by a newline.

File, stdin, and inline request transports retain exactly the caller's request bytes. An inline request is the caller's single original argument under §3; it is not silently replaced with stdin and is never forwarded as content in child argv.

#### G2: CORE §§3 and 4.1 — Init validation, output and warning

An invalid existing config returns exit 3, leaves the config, ignore file, index,
HEAD and refs unchanged, and emits no success warning. Its stdout diagnostic
starts with `environment/project_config_invalid: <absolute-config-path>`.
When the error is an unknown key, its detail contains the literal token
`unknown key` and identifies the mapping and offending key. The model's neutral
form is ``<mapping-path> has unknown key `<key>` ``. Other diagnostic layout is OPEN
and the visible case expectations are normative. The scored missing-field form
is ``checks[1] is missing required key `argv` ``. The scored malformed-row forms are
`checks[1].argv must be a non-empty list of strings` and
`checks[1].timeout_ms must be a positive integer`, in that order. Diagnostic
indices in these forms are 1-based. These diagnostic cases leave stderr empty.

Successful init output and warning follow the single §4.1 Init contract below (G6). A valid existing config is never rediscovered or rewritten, including after project marker files change.

#### G3: CORE §3 — `status --json` schema and comparison boundary

Each successful non-watch overview JSON Lines row MUST validate against
`spec/schemas/status-row.schema.json`. A known slug's single JSON object MUST
validate against `spec/schemas/status-detail.schema.json`, including when its
command exits 1 because the Intent is not Landed. These checked-in JSON Schemas
are normative: they specify required keys, types, nullability, and state-dependent
constraints. Every object allows additional properties. Implementations MAY
include additional report data; consumers MUST NOT require implementation-private
fields or reject an otherwise valid row because of extra properties.

Detail includes the same public Intent fields as an overview Intent row, plus
`approval`, `candidate`, `verdict`, `checks`, and `stage_times`. `approval` is null
when no current approval exists; otherwise `approval_sha256` identifies the exact
approved bytes and `by` identifies the caller, or is null if unavailable. No
private approval-record version or serialization is part of this output contract.
`candidate` is null until a candidate is recorded; otherwise its `tree` and `commit`
identify that exact candidate. A check row contains `name`, `status`
(`green`, `red`, or `could-not-check`), `tree`, and `evidence_complete`; the tree is
the one actually checked. Incomplete evidence cannot report a green check.
`verdict` is the latest Build's result or null before a result exists.

`stage_times` lists recorded stage timings in event order. Each entry contains
`stage` and `wall_ms`, with null representing unavailable information; an available
`rung` is a string. Times are nonnegative integer milliseconds. Timings, check
results, candidate identity, journal and diff paths remain associated with their
Build after it terminates. Reapproval changes the current approval and can return
an Intent to Queued while retaining its latest Build and that Build's detail.
Only Building Intents expose a current `stage` and `elapsed_ms`; other states
report null for both. Reapproval does not make the retained Build active again.

Recovery entries follow the shared recovery-entry schema in §3 (G7), equally in overview and detail. Preserved recovery is always unverified.

Conformance validates the whole actual row against its schema before comparing
the scenario's specified JSON pointers. Specified scalar values and nulls must
match, specified object pointers must denote objects, and specified arrays must
have the stated lengths. Unspecified properties are allowed at every object
level. Row counts and the existing queue/Intent/agent ordering rules remain
checked. Captured identifiers and paths must agree wherever reused; no Build ID
format, executable basename, transport headers, cache accounting, sandbox name,
or implementation language is required by these schemas.

#### G4: CORE §3 and §4.2 — questions-only shaping

A shape command that returns branching questions without a shaped Intent exits 5
(decision needed). It prints the returned questions and creates neither a shaped
Intent nor an acceptance source, approval package, or project commit. A successful
shaped Intent still exits 0. This applies to text and JSON modes.

#### G4: CORE §3, §5 and §6 — queue identity and portable process witnesses

The `pid` in the `status --json` queue row is the PID of the process that owns the
queue, including when that process is a VM runtime or is launched by a wrapper.
A detached queue owner and its children inherit the invocation's TMPDIR. The
conformance runner obtains a queue-owner PID only from that public CLI result,
checks the unique trace TMPDIR and OS process-start time, captures the resulting
identity, and rechecks it immediately before signalling. It never requires a
particular executable name, path, implementation language, or launcher PID.

For Quint process traces the runner reserves `${queueOwner.pid}` from a successful
`status --json` queue row. This is a runner binding, not another Kogen command or
JSON field. Numeric process-group IDs read from diagnostic files are observations,
not authority to signal a process. Fixture descendants use a runner-owned stop
file for teardown instead of granting signal authority to file-supplied PIDs.

When `KOGEN_TEST_BARRIER_DIR` is set, the process conformance seam also supports
`before-builder`, after workspace creation and before the first Builder request.
It uses the same ticket, arrival metadata, release, cancellation and bounded-wait
protocol as the other §6 barriers. This seam does not change checks or deadlines.

For supervised Builder shell calls under that seam, supply these environment
variables to the child before execution:

- `KOGEN_PROCESS_RUN_PATH`: the private directory containing this run's diagnostics.
- `KOGEN_PROCESS_LOG_PATH`: the rolling stdout/stderr log for this child.
- `KOGEN_PROCESS_WRITER_PATH`: the child's durable ownership registration file,
  created before the child runs and nonempty while it is owned.
- `KOGEN_PROCESS_CUSTODY_PATH`: the child's durable cleanup-result file.
- `KOGEN_PROCESS_GROUP_ID`: the positive decimal process-group identifier recorded
  in that cleanup result.

The paths may use any private layout; scripts must use the supplied paths, never
infer them from an executable or shell-script path. Cleanup writes one JSON object
plus a newline to the custody path, with exactly `group` (the integer group ID) and
`confirmed` (boolean). Confirmed cleanup removes the ownership registration;
unconfirmed cleanup retains its exact bytes. Persist the output captured so far
in the log before bounded return. A parent's unexpected death still invokes this
custody protocol. An escaped descendant that keeps a pipe open must produce a
bounded unconfirmed result and prevent publication; report an environment failure
(exit 3) when cleanup is unconfirmed without absolute Build deadline expiry.
These diagnostic fields are an OPEN layout refinement visible to every arm;
process-control mechanisms and helper languages remain unrestricted.

#### G5: CORE §3 — Help and argument parsing

No arguments and `help` both print top-level help to stdout and exit 0. Top-level
help lists every implemented command form in the §3 command tree, including
`intent shape`, `intent approve`, `intent remove`, `queue start`, `queue stop`,
and all four `provider` commands. Each form has the literal display prefix
`kogen `, and provider login, logout and use identify `chatgpt`. Help also lists
`kogen update` and labels it reserved and unavailable in the first core.
The display name is always `kogen`, independently of the executable's actual
filename, path, launcher, implementation language or build system.

Bare `intent`, `queue`, and `provider` print their group help and exit 0.
`help <command>` and `help <command> <subcommand>` print the corresponding page
and exit 0; in particular, `help update` succeeds. Help is available without
project initialization, authentication, or a valid project configuration. Help
and usage errors do not modify project files, the index, HEAD or Kogen refs.

For this race, exact help text and line layout are fixed by `cli.helpPages` in
`spec/quint/cli.qnt` and its expanded stdout expectations in the eight scored
CLI traces. This is a public text convention; it does not require a particular
argument-parser library. Help must describe the current contract: shape accepts
a file, stdin or inline text and advertises `--json` and `--no-color`; init
detects checks without running them; status uses versioned JSON and polls watch
every two seconds. Descriptions do not add lifecycle requirements beyond CORE.

Command routing consumes separate argv words. A single word such as
`intent shape` is not a route. Unknown commands or subcommands, undeclared or
command-inapplicable options, missing or extra operands, missing option values,
and values attached to boolean options are usage errors (exit 2). Unknown
providers are usage errors; the first core supports only `chatgpt`.
`status --watch --json` is a usage error. These errors precede project inspection
or authentication, including when `--json` occurs in an invalid invocation.

The allowed options and operand counts are exactly the §3 command forms.
Within a routed command, options may precede or follow operands. Value options
accept both `--name value` and `--name=value`; repeated value options use the last
value. Boolean options take no value. `--` ends option parsing, after which all
words are operands. A value option immediately followed by `--`, or by end of
argv, lacks a value. Otherwise its next word is its value. An attached empty
account label is invalid. No implicit `--help`, `-h`, or `--version` aliases are
required; the fixed grammar rejects these undeclared options.

For multiple errors within a known route, select the first encountered error
within the first applicable class in this order: value attached to a boolean
option; unknown option; known option disallowed on this command; missing option
value; missing operand; extra operand; incompatible watch/JSON flags; unknown
provider. Scan left to right within a class. Usage output is one diagnostic line,
one blank line, then the relevant help page, all on stdout; stderr is empty.
Exact diagnostic spelling is the public expectation in the CLI case files.

Intent slugs use 3–48 lowercase ASCII letters, digits and single dashes, with no
leading, trailing or consecutive dash. Account labels use 1–64 ASCII letters,
digits, dots, underscores or dashes; the first character cannot be a dot,
underscore or dash. Approval prefixes contain 6–64 hex characters and compare
case-insensitively. Invalid operands exit 2 before repository lookup. A valid
but nonmatching approval prefix exits 1. The cases' exact validation text is
normative for this race, regardless of parser or runtime.

An empty stdin request (`intent shape <slug> -`) exits 2 with the public
`intent/request_unavailable` diagnostic. A nonexistent path argument is inline
request text, as already specified in §3; it must not produce a missing-file
usage error. With no usable selected credentials it reaches authentication and
exits 4 with the provider-login diagnostic, leaving Intent state unchanged.

Other CLI human-output spelling and line layout asserted by these eight cases
are normative OPEN presentation choices for the race. Captures represent
runtime values, not hard-coded hashes, ports, process IDs, durations or paths.
The command forms and canonical display name are independent of executable
discovery and toolchains.

#### G5: CORE §3 and §8 — Reserved update

`update` with no operands or options exits 2 and prints exactly
`kogen: reserved: update is not implemented` as one stdout line, with empty
stderr. It does not inspect or mutate project or credential state and does not
make a provider request. Its help page exits 0 and says
`Reserved; unavailable in the first core.` Invalid operands or options use the
ordinary usage-error convention above. `update` is the only reserved command.

#### G5: CORE §3, §4.1 and §7 — Init output

When no supported project marker exists, init writes the minimal configuration bytes `name: project\nchecks: []\n` and, when absent, `.gitignore` bytes `.kogen/local/\n`. Human output and warning follow the single §4.1 Init contract below (G6). Invalid configuration exits 3 without changing files, index, HEAD or refs.

#### G5: CORE §3 and §7 — Expected removal failures

When a user's pre-commit hook rejects an Intent-removal commit, removal exits 1,
keeps the Intent and approval, and restores its own changes to the worktree and
index. It must not publish a removal commit. Hook rejection is an expected
negative result, never exit 70.

If the approval ref changes concurrently before removal publication, removal
also exits 1 without publishing a partial removal. It preserves the Intent,
HEAD and index, and leaves the concurrent writer's ref value intact. It must
neither delete a replacement approval nor restore the stale approval over that
writer. Exit 70 remains reserved for an internal Kogen bug.

#### G5: CORE §3 and §5 — Public journal and machine-local fixtures

The race journal layout is
`$HOME/.kogen/workspaces/<project-id>/runs/<build-id>/`, matching the status
model. Project IDs are implementation-chosen stable filename-safe identifiers;
the suite captures them. JSON and text status identify the same journal
directory. A present candidate diff is `candidate.diff` in that directory,
and agent event streams are `agents/<agent-id>/events.jsonl`. Verification
observers read the journal advertised by this layout, rather than a
repository-local alternative. They still check durable verification against
the published candidate tree. The layout is language-independent.

When the file credential-store seam is selected, the public credential JSON
fields and account-choice YAML exercised by the CLI cases and their embedded
`observe.py` fixture are the race's serialization convention. JSON object key
order is immaterial; credential-file digests capture the implementation's own
bytes and compare them only to ensure another account is unchanged. Saved
subject, token, expiry and scopes must reflect the completed fixture login;
credentials and account choices remain machine-local. The exact account-choice
YAML in the observer is an OPEN text-layout choice shared with every arm.

The clock fixture follows §6's existing seam: it supplies JSON
`{"now_ms":2000000000000}`, never a bare decimal file. The suite's Python
observer and Git setup commands are runner fixtures, not dependencies that
Kogen itself must be implemented with or invoke.

#### G7: CORE §3, `status`: one recovery-entry schema

The `recovery` arrays in overview Intent rows and slug-detail JSON use the same
schema. Each element requires the following keys; object-key order is not
significant and additional properties are allowed under the status schemas. An empty array means no recovery was preserved for the reported
Build. This schema describes evidence, never an approval or a check receipt.

| Key | JSON type and meaning |
|---|---|
| `workspace` | String: absolute path of the source Build workspace, retained after cleanup. |
| `base` | String: Git commit ID of that workspace's recorded base. |
| `tree` | String: Git tree ID of the complete preserved candidate tree. |
| `ref` | String for ref preservation; otherwise `null`. |
| `commit` | String: preservation commit ID when `ref` is a string; otherwise `null`. |
| `archive` | `null` for ref preservation; otherwise an object requiring `path`, `manifest`, `sha256` (all strings). The paths are absolute, and `sha256` is the lowercase SHA-256 of the archive bytes. |
| `verification` | The string `unverified`, including after expiry. |
| `preserved_at_ms` | Nonnegative integer Unix milliseconds when evidence was first preserved. |
| `expires_at_ms` | Nonnegative integer Unix milliseconds: `preserved_at_ms + recovery_retention_days * 86400000`, using the setting read at first preservation. |
| `expired` | Boolean: true only after deletion and its durable journal record succeed. |
| `expired_at_ms` | `null` until expiry is recorded; then integer Unix milliseconds of that deletion, at least `expires_at_ms`. This key is always present. |

Exactly one of `ref` and `archive` is non-null. Historical entries retain all
location, commit, tree and time fields after deletion; only `expired` and
`expired_at_ms` change. Configuration changes never alter a recorded expiry.

For text watch, render the final changed frame before returning when the queue
is stopped and no Build or agent remains. Text layout remains **OPEN**; the
running, failed/interrupted and recovery-location/expiry examples exercised by
these cases are visible in their `stdoutLines` expectations.

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


#### G1: CORE §4.1 — Generic command acceptance configuration

The optional `acceptance` map accepts `adapter: command`, a required nonempty `argv` vector of strings, and an optional positive integer `timeout_ms` (default 600000). These are the only command-adapter keys. Explicit selection works in every project type and overrides project-marker detection. Launch the vector directly, without treating it as a shell command string or modifying it based on the executable's name.

Each literal `{path}` occurrence in an argv element is replaced with the acceptance source's absolute path. If no element contains `{path}`, append the absolute path as one additional element. Preserve argument boundaries and order. The source contents are never arguments. Resolve the program and relative paths under the ordinary command rules and run the command with the checked project/workspace as its current directory.

#### G2: CORE §4.1 — Complete project configuration schema

`.kogen/project.yaml` is one strict-subset YAML mapping. The table below is the
complete schema; keys not listed here are errors, including keys inside optional
mappings. Every mapping key is a string and duplicate keys are errors, including
inside an unknown subtree. YAML booleans, numbers and null are not strings;
quoting a scalar makes it a string. Empty strings are allowed where the type is
`string`. Missing optional mappings behave as empty mappings.

| Key | Type and constraints | Default when omitted |
| --- | --- | --- |
| `name` | Required string | No default when loading; init writes `project` |
| `checks` | Required list of check mappings; may be empty | No default when loading; init writes detected checks or `[]` |
| `format` | List of nonempty strings, representing argv; `[]` disables formatting | Absent: no project override of the selected formatter |
| `acceptance` | Mapping containing only the six keys below | `{}` |
| `hooks` | Mapping containing only `repair_limit` (integer 0–5, default 1) | `{}` |
| `shaping` | Mapping containing only `repair_limit` | `{}` |
| `build` | Mapping containing only the four keys below | `{}` |
| `recovery_retention_days` | Positive integer | `14` |

Each check mapping contains exactly the required keys `name` (string), `argv`
(nonempty list of strings), and `timeout_ms` (positive integer). Check names must
be unique within `checks`. A check's argv elements may be empty strings; the list
itself must contain at least one element. There is no implicit check timeout.
Config validation never executes these commands.

| Acceptance key | Type | Default when omitted |
| --- | --- | --- |
| `adapter` | String naming the acceptance adapter | Absent: automatic adapter selection under §4.2 |
| `ext` | String overriding the generated acceptance source's extension | Absent: no override of the selected adapter's extension |
| `candidate_dir` | String overriding the source's candidate directory | Absent: no override of the selected adapter's directory |
| `argv` | Required nonempty list of strings when `adapter: command`; allowed only for that adapter | No default |
| `run` | List of nonempty strings representing acceptance argv; may be `[]` | Absent: no override of the selected adapter's command; `[]` disables that command |
| `timeout_ms` | Positive integer | `600000` |

A configured adapter name with no supported adapter selects criteria-only
acceptance. The schema does not require any implementation language's toolchain.
Adapter source layout and automatic selection remain OPEN where §4.2 does not
specify them; applicable conformance fixtures supply their concrete values.

`shaping.repair_limit` is an integer from 0 through 5, default 2. No other shaping
settings are accepted.

| Build key | Type and constraints | Default when omitted |
| --- | --- | --- |
| `budget_ms` | Positive integer | `wall_minutes * 60000` if specified, otherwise `3600000` |
| `wall_minutes` | Positive integer | `60`; ignored for deadline selection when `budget_ms` is present |
| `log_limit_bytes` | Positive integer, at least 12 | `10485760` |
| `memory_limit_bytes` | Positive integer | Absent: no project memory limit |

For these configuration fields, a positive integer is a whole YAML number from
1 through 2^53−1 = 9007199254740991 inclusive. Booleans, quoted numbers, floating-point
numbers, zero, negatives and larger numbers are invalid. This bound is exactly
representable in every implementation language without arbitrary-precision arithmetic.

In particular, `base`, `domains`, `acceptance_checks`, `protected_paths`,
`gate_paths`, `setup`, `fix`, `env`, `sandbox`, `shaping.web_search`, `build.roles`,
`build.tool_result_tokens` and `build.model_generation_tokens` are unknown keys.
Credentials and account selection are not project configuration keys.

#### G4: CORE §4.1, §4.6 and §7 — bounded hook repairs

Project config accepts optional `hooks: {repair_limit: N}`, where N is an integer
from 0 through 5; the default is 1. This is a maximum number of hook-repair Builder
turns per Build, counted across all landing attempts independently of the four
moved-base integration turns.

When a user's commit hook rejects a candidate, return its output to the Builder.
If hook repairs remain and the original Build deadline has not expired, request
one Builder repair turn with that output in its context. A turn ends when the
Builder finishes or returns a terminal assistant response; it may make tool calls
within that turn. Consume one hook repair even when the Builder proposes no edit.
Rerun the candidate gate and ordinary commit hooks before any publication. Do not
edit, skip, or disable the rejecting hook to make landing succeed.

If the hook rejects again after the configured number of repair turns, stop the
Build with exit 1, make its hook error available to the caller, and leave the target
ref unchanged. With limit 0, the first rejection stops immediately. Deadline expiry
or a failed candidate gate stops without scheduling another hook repair. Hook
repairs retain the same Build, Builder role, model, and absolute deadline.

The always-rejecting conformance fixture uses the default limit 1. Its first two
provider responses edit and finish the initial candidate; its third response
finishes the sole repair turn without changing it. Exactly three requests are
required. The recheck passes, the hook rejects again, and the command exits 1.

#### G4: CORE §4.1 and §4.5 — minimal smoke configuration

The shape/approve/queue/land smoke fixture uses criteria-only acceptance and a
project config consisting of `name`, `checks` and optional `build.budget_ms`.
It requires no domains table, model-role overrides, sandbox setting, acceptance
adapter, or language/toolchain marker. Its configured shell check and final
file-content assertion apply equally to every implementation language.

#### G6: CORE §4.1 Init — config, preservation, and human output

When no supported check marker is present, the generated `.kogen/project.yaml`
MUST contain exactly these UTF-8 bytes, including the final LF:

```yaml
name: project
checks: []
```

Init MUST preserve every existing byte of `.gitignore`. If its final effective
rules already ignore `.kogen/local/`, init MUST leave those bytes unchanged.
Otherwise it MUST append `.kogen/local/` followed by LF, first appending a
separator LF if the existing nonempty file has no final LF. An absent file is
created with exactly `.kogen/local/` followed by LF. A later negation of an
earlier ignore rule requires appending the effective rule again.

Init MUST preserve unrelated worktree files and the original staged content of
unrelated index entries. Those entries MUST NOT enter the init commit. Existing
`AGENTS.md` and `CLAUDE.md` files MUST remain byte-for-byte unchanged; init MUST
NOT create either file when absent.

After successfully creating the init commit, stdout MUST consist of the following
LF-terminated lines, in this order:

1. `Initialized Kogen project.`
2. `Checks: none` when the generated checks list is empty; otherwise `Checks:`
   followed by one line per selected check, in config order, with exactly two
   leading spaces followed by that check's name.
3. `Commit: <short-sha> <subject>` where `<short-sha>` is the first eight lowercase
   hexadecimal digits of the actual created commit ID, and `<subject>` is
   `Initial commit` when there was no prior history, or `Initialize Kogen project`
   when there was history.
4. `Branch: <name>` using the checked-out branch's short name, or
   `Branch: (detached HEAD)` when HEAD is detached.

The placeholders above describe values; angle brackets are not printed. These
fields contain no implementation executable name or implementation toolchain.
Init discovers checks by reading repository files; it MUST NOT execute them.

A valid existing config is a filesystem and Git no-op: exit 0, no new commit,
no config or ignore-file rewrite, and stdout exactly
`Kogen is already initialized.` followed by LF.

Every successful init invocation, including the valid-config no-op, MUST emit
exactly the following UTF-8 warning line on stderr, followed by LF, regardless
of whether either named file exists:

```text
kogen: warning: Kogen does not read AGENTS.md or CLAUDE.md.
```

The literal `kogen:` prefix is a product diagnostic label, independent of the
filename or path used to launch an implementation.

The files remain allowed in the project. This warning reports Kogen's treatment
of them; their presence or absence does not cause an error.

#### G6: CORE §4.1 Init and §7 Commits and hooks — init failure

Init's user-visible commit MUST run the user's Git hooks. If a hook rejects the
commit before HEAD advances, init MUST return exit code **3**, report the failure
with the rejecting hook's diagnostic output on stderr, leave HEAD unchanged
(including an unborn HEAD), and roll back its changes to `.kogen/project.yaml`
and `.gitignore`, restoring their original bytes or their original absence.
It MUST restore the original staged content of the index and preserve unrelated
worktree bytes. Init MUST NOT retry the commit while bypassing the hook.

If the commit has already succeeded and subsequent index reconciliation fails,
init MUST return exit code **3** and report that failure; it MUST retain the
created commit and its config/ignore files rather than roll back published
history.

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


#### G1: CORE §4.2 — Opaque command acceptance and shaping

For the command adapter, the Shaper writes `.kogen/local/acceptance/<slug>.txt`. This source is opaque bytes owned by the supplied command; Kogen neither parses its test identifiers nor rewrites, normalizes, or formats it. No implicit or configured formatter is applied to command-adapter acceptance. This is the command-adapter exception to §4.2's formatter rule. Preserve all bytes, including line endings and trailing blank lines, as the source of record.

Run the configured acceptance argv on that local source during shaping. A completed command with exit 0 is green; an ordinary nonzero exit is valid red base evidence for a new `test` requirement and does not by itself prevent shaping. Missing source, unavailable process, timeout, or incomplete capture is an environment failure, never expected red. Requirements marked `test keep` must pass on the base. Shaping does not modify project files, metadata or lockfiles, does not manufacture a missing lockfile, and does not install a permanent acceptance package. It cannot approve.

The Intent Markdown written by the Shaper is retained, followed by a blank line, `## Request`, a newline, and the original request bytes. In the G1 fixtures, the provider writes Markdown ending in one newline; Kogen appends `\n## Request\n` and then the request. No summarization of the provider's Notes or normalization of the original Request is permitted.

### 4.3 Approve

Approval is a separate caller action after shaping and before queue start. It binds the exact Intent and, when present,
the exact acceptance source bytes. Criteria-only approvals record no acceptance path or bytes. Any bound byte change
requires approval again. Approval records the caller's identity; the Shaper cannot approve.


#### G1: CORE §4.3 and §5 — Exact approval and the package layout

Command-adapter approval binds the current Intent bytes, source presence, and every source byte. Editing or deleting either bound file makes the approval stale. A stale Intent is draft and cannot dispatch. Reapproval requires a fresh matching hash and records the current caller without starting the queue. A matching hash prefix has at least six hexadecimal digits; a shorter prefix returns 2, and a syntactically valid nonmatching prefix returns 1. The approval digest is SHA-256 over an unambiguous binding of both byte strings and source presence; its serialization remains OPEN, and cases capture the displayed digest rather than computing it.

The approval package is a Git tree reachable at `refs/kogen/intents/<slug>`. It contains `.kogen/intents/<slug>/intent.md`, `.kogen/intents/<slug>/approval.json`, `.kogen/acceptance/<slug>.txt` when a command source exists, and `.kogen/intents/<slug>/ledger.json` only when a local ledger matches the exact current binding. Store the Intent, source, and promoted ledger verbatim: their Git blob IDs equal those of their local files. Its commit records `Kogen-Approved-By` and `Kogen-Approved-Hash` trailers with the approving caller and displayed full digest. The approval JSON's internal representation remains OPEN. Warnings stay in `.kogen/local/intents/<slug>/shape-warnings.json` with their existing bytes, and are never promoted. Editing files must not mutate an existing immutable package.

The human review card's line order, labels, spacing, blank lines, baseline warning and next-command text are the visible templates `intent::reviewExpectation` and `approve::reapprovalCard`, also materialized in the G1 case files. These templates fix this OPEN presentation detail for every implementation. Dynamic digests and base IDs are captured, and an executable may be installed under any filename; displayed instructions use the canonical CLI name `kogen`.

For a stale greeting Intent, human slug status returns 1 and prints `greet: draft; review it with kogen intent approve greet` followed by a newline. Starting an empty queue returns 0 with `queue: nothing to build`; stopping a stopped queue returns 0 with `queue: not running`, each followed by a newline.

#### G2: CORE §§4.3 and 4.6 — Landing fixtures without extra config keys

When approval is created from a checkout on a branch, that branch and its current
commit identify the approved base and landing target. No `base` configuration
key is required or accepted. Approval's review card names that branch and commit.
Moving the branch after approval does not change the recorded target; landing
uses §4.6's moved-base and CAS rules.

Configured project checks apply directly to the candidate tree. A criteria-only
Intent may retain domain labels in its Intent and Verify text, but no `domains`
project mapping is required or accepted for running those checks. In the landing
fixtures here, the configured greeting check verifies `README.md`; hook,
signing, draft cleanup, fast-forward and lost-CAS assertions remain applicable.

### 4.4 Build

Queue start runs one bounded Build in an isolated workspace under `$HOME/.kogen/workspaces/`. The user’s project checkout
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


#### G4: CORE §4.4 and §3 — absolute Build deadline

Expiry of the absolute Build deadline is a failed Build and returns exit 1 from
foreground `queue start`, including expiry during a provider request, child process,
or test barrier. It cannot publish the candidate or change the target branch,
index, or checkout. Cleanup still runs within the process cleanup bound. Deadline
expiry is not an environment error (exit 3), and landing receives no new budget.
Diagnostic wording and the failed Build's status presentation remain OPEN.

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


#### G1: CORE §4.5 — Generic command gate

The controller runs both configured checks and command acceptance on the exact candidate tree, with the immutable approved source installed at `.kogen/acceptance/<slug>.txt` in that candidate. The Builder cannot change that source or the approved Intent. Acceptance passes exactly when its command completes with exit 0 and complete capture; an ordinary nonzero exit is red. A missing source, timeout, unavailable process (including exits 126/127), or incomplete capture is could-not-check. All required checks and acceptance must pass for a verified receipt and publication. A base-red command acceptance is never an excuse for candidate-red acceptance. A foreground queue that cannot verify its Build returns 1 and leaves the target branch unpublished.

A generic command may itself check identity/mapping validity inside its opaque source. The supplied portable fixture validates exactly one `A1: hello` record and the greeting output. Missing or duplicate records produce nonzero exits even when the greeting is otherwise correct; Kogen uses that exit and does not parse test-framework output. Success records and publishes the same tree that was checked. The fixture records its argv, bytes read, and result outside the candidate as observable evidence.

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
- User logins, global default, and project account selections live in `$HOME/.kogen/accounts.yaml` on this machine. The
  project selection takes precedence over the global default. Never put provider account choices or login secrets in
  the repository.
- Build workspaces live under `$HOME/.kogen/workspaces/`.
- Process content is transported without command-line arguments.
- Commits follow the user's git configuration.


#### G3: CORE §5 — OPEN fixture layout for the status agent observation

The rich status fixture exercises a waiting agent by writing its event log from
the scripted Build shell call. For this fixture's OPEN storage layout, the Build
workspace basename is `<build-id>-R1`, and its sibling path
`../runs/<build-id>/agents/<agent-id>/events.jsonl` stores agent events. The
fixture agent ID and event bytes are visible in `statusrec-fixtures.json`.
`agent_started` and `agent_waiting` records identify a `builder`; the waiting
record supplies status `waiting`, activity `provider reply`, and timestamp
`ts:1000` (Unix milliseconds). Overview must project that waiting agent while
the Build is active and stop reporting it as active after the Build terminates.
The reported paths follow §5’s shared public journal layout and are captured from output.

#### G7: CORE §5, Files and state: reconciliation and preservation

Reconcile only after the recorded owner is dead. If the recorded landing
candidate is reachable from the recorded target branch, mark that Build
`landed`, with no failure reason, and retain its landing SHA. Reachability from
another branch does not satisfy this condition; a missing recorded target also
does not satisfy it. Otherwise mark it `failed` with reason `crashed`, or
`interrupted` if cancellation was recorded. Recovery does not restart a Build
or confer approval, queue eligibility or verified evidence.

A Landed Build MUST NOT produce an unverified recovery artifact for its
published workspace tree. Once custody is confirmed, that workspace may be
cleaned without creating a recovery ref or archive. With uncertain custody,
retain the workspace for later cleanup. Reconciliation and preservation MUST
leave the origin checkout's HEAD, index and working files unchanged; recognizing
a candidate already published on the recorded target does not move them again.

For a changed workspace of a failed Build, preserve the complete candidate tree
before removing the workspace. Prefer the internal ref required by §5. The
preservation commit has the recorded base as its sole parent, uses the user's
trusted origin Git configuration and identity for both author and committer,
and has subject `Unverified recovery`. Skip preservation hooks; workspace-local
identity/configuration cannot override the trusted origin settings. Repeated
reconciliation does not create duplicate preservation records or artifacts.

If the local ref publication fails, including because the ref's `.lock` file
already exists, use the run archive fallback. Do not delete or overwrite a lock
owned by another writer, and do not treat a failed ref write as successful
preservation. Only after the fallback and preservation record are durable may
cleanup remove the workspace. If neither preservation mechanism succeeds,
retain the workspace. A fixture may hold the exact recovery ref lock to force
this outcome; no receive hook is involved in a local ref write.

Expire evidence when `now_ms >= expires_at_ms`, including exactly at the
boundary. Ref expiry deletes the recovery ref. Archive expiry deletes both
archive and manifest. If deletion fails, retain the unexpired record and its
original expiry, record no successful deletion, and report an inspection error
(exit 3 from `status`). A later reconciliation retries deletion. A successful
retry records exactly one deletion; further status calls neither recreate the
artifact nor duplicate that record. Normal overview `status --json` returns 0
and emits no stderr when inspection succeeds.

#### G7: CORE §5, Files and state: public recovery inspection layout

For these recovery cases the following language-independent inspection layout
is fixed. A project's opaque `project-key` and a Build's opaque `run-id` are
learned from status, rather than computed by the suite. Workspaces are
`$HOME/.kogen/workspaces/<project-key>/<workspace>`, with `<workspace>` equal to
`<run-id>-R1` in the single-rung fixtures. A run's status `journal` path is
`$HOME/.kogen/workspaces/<project-key>/runs/<run-id>`.

That directory exposes UTF-8 JSON Lines in `events.jsonl`. A
`recovery_preserved` event includes the recovery-entry fields defined above at
preservation time. A `recovery_expired` event includes `workspace`, `ref`,
`archive`, the original `expires_at_ms`, and `deleted_at_ms`; its location
fields agree with the preservation record. Other event keys and events remain
**OPEN**. A read-only `run.json` inspection view exposes the terminal `status`
and `landing.candidate_commit` when a landing candidate was recorded; its
other keys remain **OPEN**. This view does not prescribe internal storage.

The archive fallback is a tar archive of the complete preserved Git tree,
including tracked file bytes and executable/symlink modes, with relative safe
paths and no duplicate file entries. Its path in these fixtures is
`<journal>/recovery-<workspace>-<tree>.tar`; the manifest is that path plus
`.json`. Archive encoding, compression and metadata timestamps are **OPEN**;
the suite captures the actual SHA-256 and compares it with the recorded hash.
The manifest is an object with exactly `schema`, `base`, `tree`, `sha256`,
`files`, and `reviewed_files`; `schema` is the integer 1. It contains a
`files` object and a `reviewed_files` object. `base`, `tree`, and `sha256` agree
with the recovery entry. `files` maps changed UTF-8 regular-file paths (relative to the recorded base)
to objects with the single key `text` containing the complete file text. For
these fixtures it has exactly the key `greeting.txt`.
`reviewed_files` is empty when the Build has no separately reviewed acceptance
files. These fixtures inspect `files["greeting.txt"].text == "hello\n"`; the
archive itself must reproduce the entire independently constructed tree.

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
[QUINT-SUITE.md](../../MISSING.md) defines the trace encoding, fixture protocol and observation comparisons.

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

Questions-only shaping exits 5 in every transport and output mode.

The table fixes command outcomes. Status names refer to the lifecycle or diagnostic category;
where a case does not inspect a status row or text, that limitation is stated. A required
text token is a literal substring, not a requirement to reproduce the entire diagnostic.

| Situation | Exit code | Status | Required text token |
|---|---:|---|---|
| Absolute Build deadline expires | 1 | `failed` (Build model; status row not asserted) | None asserted |
| Candidate is tampered with before the final recheck | 1 | `failed` (landing model; status row not asserted) | None asserted |
| Invalid project config | 3 | `environment/project_config_invalid`; no Intent status asserted | `environment/project_config_invalid` on stdout in diagnostic cases |
| Could-not-check because a check times out | 1 | `blocked` (Intent); check result `could-not-check` | `could-not-check` on stdout |
| Questions-only shape | 5 | Questions only; no Intent or acceptance source | Returned questions on stdout |
| User pre-commit hook rejects landing | 1 | `failed` (landing model; status row not asserted) | `landing-hook-denied` on stderr in the Quint hook case; no text asserted by the Gherkin case |

Sources: `conformance/cases/quint/build/trace-20271011.itf.json` (deadline),
`conformance/cases/quint/landing/trace-20273013.itf.json` (tampering),
`conformance/cases/quint/config/trace-20264016.itf.json`, `trace-20264017.itf.json`
and `trace-20264047.itf.json` (invalid-config diagnostics),
`conformance/cases/quint/shape/trace-20269010.itf.json` (questions), and
`conformance/cases/quint/landing/trace-20273011.itf.json` (hook).
The source Gherkin scenarios in `conformance/features-src/04-lifecycle.feature`
supply the timeout status/token and the exit-5 questions case;
`conformance/features-src/07-commits.feature` supplies hook exit 1.

The questions-only exit code is 5. Other invalid-config cases assert exit 3 without asserting diagnostic text.
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

#### G1: CORE §6 Test seam / WIRE — Portable fixture assertions

Provider fixture requests assert only the prescribed model and reasoning effort, not a particular implementation's prompts, tool-array ordering, headers, or private serialization. The existing WIRE tool argument and SSE output contracts still apply. Generic command fixtures are declared as bytes and SHA-256 digests in each case manifest and installed by the runner; no language-specific host tool or wrapper is required. The POSIX-shell fixture is invoked through the configured interpreter argv, so its installed executable bit is immaterial.
