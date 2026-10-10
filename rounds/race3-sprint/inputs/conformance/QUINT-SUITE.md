# Quint → executable conformance contract (IO schema 1)

The oracle is a seeded Quint trace. Replay drives the public `kogen` executable and observes its exit, streams,
Git state, and files. It must not call Rust lifecycle/replay functions, construct verified receipts, or substitute
an implementation-generated expected result. The existing ten abstract models are not yet executable conformance
models: module writers must add this interface. This document specifies the runner; step 0 does not implement it.

## Producer and artifacts

Import `kogen_io.* from "./kogen_io"`. Every runnable module exports `var lastStep: List[Step]`, `init`, `step`,
and `invariant`. The composed module has exactly one `lastStep`, collecting ordered effects from its submodules.
It also exports `var ioSeam: Seam`, initialized once for the trace. The library itself is pure, not a runnable model.

Each action assigns `lastStep'`, even a repeated invocation or stutter:

```quint
// Inside an action; the action also updates its lifecycle state.
lastStep' = [cliStep(command(["version"]), expectedVersion)]
// Non-CLI action: install a hook, move a base, kill a process, or advance time.
lastStep' = [setupStep(WriteFile({ path: "${repo}/.git/hooks/pre-commit",
  bytes: Utf8("#!/bin/sh\nexit 1\n"), mode: 493 }))]
// A pure transition produces no external effect.
lastStep' = []
```

`Step` is the discriminated union `Cli({cmd,expect}) | Setup({op,expect})`; **lastStep is always a list**,
including for one command. An init action may emit setup steps; the runner executes those too. `ioSeam` may not
change silently after init: environment changes belong in `Cmd.env`, clock changes in `AdvanceClock`, and barrier
arming in `WriteFile`. Multi-command actions emit the complete ordered list and the expectation after each command.

Each trace has a companion manifest (plain JSON, independently of runner language):

| Field | Required meaning |
|---|---|
| `io_schema` | `1`; reject any other version |
| `module`, `source_digest`, `sources` | Main module and SHA-256 of the sorted path/byte contents of its complete import closure |
| `quint_version`, `backend`, `seed`, `max_steps` | Pin `0.33.0`, `typescript`, decimal seed string, and generator bound |
| `last_step_var`, `seam_var` | Exact ITF state keys; normally `lastStep` and `ioSeam`, including namespace if emitted |
| `binary_digest`, `binary_version` | SHA-256 and `kogen version` from the tested binary, kept as actual metadata |
| `scripts`, `fixtures`, `fixture_sources` | Versioned provider scripts and replay-installed fixture byte blobs with content digests; fixture source maps are provenance-only `{path, sha256}` entries relative to `spec/` and their scripts are extracted into `scripts` |
| `requires` | Platform/tool capabilities and required implemented seams; no silent skip |
| `clause_ids`, `witnesses`, `profile` | Ownership IDs from MODULE-PLAN, generated witness names, and run profile |

A fixture digest covers templates **before** placeholder substitution. Record the resolved bindings, exact argv/env
overrides, setup operations, provider transcripts, outputs, Git observations, seed, and first failure state/step index.
Keep the original ITF and manifest. Exclude inherited secrets; fixtures use synthetic credentials. Files are temporary
artifacts, not additions to CORE's otherwise OPEN serialization contract.

## ITF decoding and order

Read `states` in stored array order, checking strictly increasing `#meta.index` when present. Read the configured
`last_step_var` from **every** state, including state 0. Do not deduplicate identical steps, diff against the preceding
state, or execute arbitrary other state fields. Missing lastStep, malformed records, undefined/cyclic ITF values,
unknown constructors, and empty/missing required manifest fields are malformed suite input, not binary failures.

Decode ITF values structurally: primitives; arrays for Lists; `{"#bigint":"143"}` for arbitrary-precision integers;
`{"#set":[...]}` for Sets; `{"#map":[[key,value],...]}` for Maps; `{"#tup":[...]}` for tuples; plain objects for
records; and `{"tag":"Cli","value":{...}}` for sum constructors. A nullary constructor such as `Missing` has a
unit payload (`{"#tup":[]}`), not JSON null. Reject duplicate map keys/set elements rather than hiding them. Do not
round big integers through floating point. These encodings are Quint 0.33's exported ITF, not executable JSON rows.

For state i, execute `lastStep[j]` sequentially and compare its Expect before j+1. The state is the model state
**after** these effects. Pure actions use `[]`; ordinary actions must never retain the previous lastStep value.
The runner does not infer commands from abstract state differences. A model nondeterministically choosing a scenario,
slug, request, base move, check fixture or provider result must emit the selected concrete operands/script reference
in lastStep. Never reroll a pick during replay. Preconditions must ensure that the emitted setup is physically possible;
an unsatisfied fixture precondition is a model/runner error. OS-generated values use typed captures below.

## Fresh environment and command execution

Allocate one fresh trace directory with `home/`, `repo/`, `tmp/`, `bin/`, `control/` and `fixtures/`. Reuse it across
steps of that trace; never across traces. Bind `${home}`, `${repo}`, `${tmp}`, `${bin}`, `${control}`, `${fixtures}`,
`${kogen}` (absolute tested executable). With a local fixture server, also bind `${provider}` and `${auth}` to its
complete Responses endpoint and OpenID discovery base. Endpoints use loopback only. Generation/typechecking need no
server or network; replay of provider traces uses the local fake HTTP server, never hosted endpoints.

Initialize an **unborn** Git repository on branch `main`, empty worktree, configured identity `Kogen Suite
<kogen-suite@example.invalid>`. Set `HOME`, `TMPDIR`, `XDG_CONFIG_HOME`, `LC_ALL=C`, `TZ=UTC`, `NO_COLOR=1`,
`TERM=dumb`, `GIT_CONFIG_NOSYSTEM=1`, and a temporary `GIT_CONFIG_GLOBAL`; use no inherited KOGEN variables,
Git command/config/identity overrides, credential tokens, signing settings or user's config. **Implementation
environment:** the legacy and Gherkin runners pass the inherited host `PATH`; the Quint runner prepends its fixture
`bin/` directory to that PATH (unless a trace `Cmd.env` explicitly sets `PATH`, in which case that exact value is
used). All three pass through `RUSTUP_HOME`, `CARGO_HOME`, `GOROOT`, and `GOTOOLCHAIN` when set by the runner. If
`RUSTUP_HOME` or `CARGO_HOME` is unset, the runner uses `$HOME/.rustup` or `$HOME/.cargo` when that directory exists.
The toolchain passthrough does not copy host credentials or host `KOGEN_*` values. The baseline config disables
signing, sets the identity and disables external pagers; an emitted Git setup can replace these choices. No initial commit or automatic
`kogen init`: the init trace must observe its own first commit. Existing-history scenarios emit ordinary Git setup
commits. Build/workspace, checkout, hooksPath, Cargo/Elixir and synthetic child fixtures are installed by emitted
steps. Track any escaped fixture children for teardown.

Compile initial `ioSeam` to CORE's Test seam: decimal `timeScalePermille / 1000`; file credential store; synthetic
injected auth or no auth; default, scripted, or intentionally invalid endpoint; optional frozen wall-clock file;
optional barrier directory. `InjectedAuth` creates the documented JSON with a synthetic JWT payload `exp`, not a
saved login. A default hosted endpoint is permitted only in a trace guaranteed to make zero provider requests;
otherwise require a scripted endpoint. Test owned logins through the local OpenID fixture with AUTH_PATH unset.
The fake OpenID fixture signs its ID tokens against its advertised JWKS and preserves normal nonce/state/PKCE and
issuer validation. Capture the flushed authorization URL and use the PATH browser shim; it may not launch a real
browser. OAuth traces are serialized because the current callback port is 1455; bind failure is a fixture failure.

For `Cli`, execute `${kogen}` with `cmd.argv` **excluding** the executable itself, including an empty argv for bare
usage. Pass each string as one argv element, no shell expansion. Resolve cwd, feed exact stdin bytes and close stdin,
then apply `SetEnv`/`UnsetEnv` overrides to the baseline. Overrides last for that process and descendants, not subsequent
commands. `Utf8` encodes the substituted string as UTF-8; `Octets` encodes literal integers 0..255, without substitution.
No request bytes are inserted into argv. Preserve stdout and stderr separately, drain both concurrently and do not
assume an ordering between them. Process full logs are observed via named files, not merged CLI streams.

`Foreground` waits for termination and drains streams before comparison. `Background(handle)` starts and registers
the actual child PID, returns immediately and requires exit/stdout/JSON expectations to be Unobserved at launch;
stream class/text must also be unobserved. Its files/Git may be compared only after a modeled barrier establishes
quiescence. Subsequent `AwaitOutput`, `ProviderGate`, or `AwaitBarrier` establishes readiness; `AwaitExit` observes
the complete accumulated streams and exit. A detached queue's launcher is still a foreground CLI: capture its daemon
PID from documented status, and signal only that captured trace-owned process. Status watch runs with a background
handle so the trace can advance the environment and later await its result.

`timeoutMs` is a **real** runner safety bound, not a Kogen logical budget. Timeout is a suite failure with persisted
output; it must not be treated as the expected Kogen expiry. A signal exit is represented as `128 + signal number`
(thus TERM=143), whether reported directly by the OS or by Kogen. Unconfirmed teardown is a suite failure.

## Setup operations

| Constructor | Runner operation and output subject for Expect |
|---|---|
| `GitCommand(Exec)` | Require `executable == "git"`; execute real Git with exact argv/stdin/env/cwd, capture streams and exit. No shell. This includes initial commits, config, branch moves, refs, worktrees and checkout. |
| `WriteFile` | Resolve a path within the trace, create parents, atomically replace regular file with exact bytes and Unix mode (e.g. 493=0755). Used for config, request, check executable, hooks, user edits and `.arm` files. |
| `DeletePath` | Remove the named trace path (a symlink itself, without following it); absent is success. No implicit Git staging. |
| `SendSignal` | Resolve handle or a typed captured PID, verify trace ownership/start identity, send named TERM/KILL/INT to that process or its original group. Never signal arbitrary numeric literals or reused PIDs. |
| `AdvanceClock(ms)` | Require nonnegative delta and clock capability; atomically add it to `now_ms` in the CORE seam file. Never alter the system clock or run snapshots. |
| `WaitRealMs(ms)` | Wait the nonnegative number of real milliseconds. No multiplier, no logical-clock advance. Use only for explicitly modeled elapsed-time tests. |
| `AwaitExit` | Bounded wait for a registered background handle, then compare its complete exit/streams; retain handle identity until teardown. |
| `AwaitOutput` | Wait until its named stdout/stderr buffer matches the pattern, compare Expect against the prefix through that match; exit is Unobserved. This does not consume/reset the eventual full output. |
| `ProviderGate` | Script id and gate label select a fake-server checkpoint; operation `await` waits for an arrival, `release` allows its response to proceed. Unexpected labels/operations fail. |
| `AwaitBarrier` | Wait for next unconsumed arrival at point, capture `ticket` under the supplied binding name and metadata as `<name>.run_id`, `.workspace`, `.expected_base`, `.ordinal`, `.point`; timeout is failure. |
| `ReleaseBarrier` | Resolve the previously captured ticket and atomically create its release file. The `.arm` stays armed until explicitly deleted; repeated turns create new tickets. |
| `Inspect` | Take Git/file observations without invoking status or causing reconciliation. |

Non-process setup operations have synthetic exit 0 and empty streams on successful execution; setup failure is a
fixture failure, not an expected CLI error. `Setup.expect` can check the resulting Git and files. `Inspect` never
implicitly runs `kogen status`; reconciliation is a separate emitted CLI call. A request made before a crash may
remain at a provider gate: teardown releases or aborts those requests explicitly.

## Comparing Expect

All enabled observations must hold. `Unobserved` means no assertion; `Observe([])`/`Observe("")` means exactly
empty. `Missing` nested within an enabled ref/HEAD observation asserts absence; it is not a wildcard. `noExpectation`
is for setup and deliberate partial observations; conformance CLI completion must observe an exit and at least the
outputs/Git/files required by its owned clauses. Do not use ignored fields to conceal a known divergence.

| Field | Comparison |
|---|---|
| `exitCode` | Exact integer after signal conversion, never an allowed-code set. `exitCodes` lists CORE's set; exit 130 remains a known divergence. |
| `stdoutLines` | Concatenate each Line's fragments without separators, substitute bindings, then compare ordered normalized lines exactly. Decode UTF-8 strictly, convert CRLF to LF, remove one final LF, split on LF. Empty byte output gives []; additional blank lines, spaces and ordering remain significant. Do not trim, sort, wrap, erase progress lines or globally scrub hashes/times. ANSI output is unexpected under the baseline. |
| `stderr.text` | Same normalization for `ExactLines`; `Pattern` uses the portable regex subset below over normalized full text (join lines with LF); `IgnoreText` asserts nothing. |
| `stderr.class` | `empty` requires zero bytes. `warning` requires nonempty lines beginning `kogen: warning:` and exit 0. `usage`, `environment`, `provider`, `decision`, `bug`, `sigterm`, `no` require nonempty stderr and the corresponding `exitClass`; `other` requires nonempty stderr. Class checks never replace an enabled text check. Use Unobserved when a diagnostic class is not fixed by CORE. |
| `jsonRows` | Parse each stdout line as one JSON value. Reject blank/non-JSON lines and duplicate object keys. Compare row count/order and the complete flattened shapes/atoms. Key order/JSON whitespace are immaterial; array order and numeric/string/null/absent distinctions are material. A single detailed object is one row. Pretty multi-line JSON is not JSONL. |
| `statusRows` | The same parsed stdout, additionally restricted to schema 1 status rows: overview begins with exactly one queue row, then board-order intent rows, then agents; detail is exactly one intent_detail object. Compare exact keys, types, values, ordering, nulls, recovery arrays and 1-based queue positions. If both JSON fields are enabled, both must match. No hidden status call. |
| `git` | Inspect the Cmd cwd repository (or GitCommand cwd; otherwise `${repo}`), using read-only Git commands and no optional locks. `branches` keys are full refs/heads names; `kogenRefs` keys full refs/kogen names. Resolve ref/HEAD values to full object ids. `complete=false` checks named entries only; true requires precisely the non-Missing listed refs in that namespace. HEAD may be unborn (Missing); symbolicHead is the exact ref or Missing for detached HEAD. headTree and indexTree are Git tree identities; derive the index tree in an isolated copied index, never change the real index. Subject is HEAD's first message line; trailers are the ordered Git-parsed trailer list, including duplicates; changedPaths is the set of paths in HEAD versus its first parent (empty tree for a root), with both sides of renames. Compare parents in stored order and author/committer name/email exactly when enabled. Never inspect or assert signed-or-not. |
| `files` | Check each named path with lstat; absence, exact UTF-8/octet bytes, SHA-256 of complete raw bytes, or exact symlink target as requested. No newline normalization for files; hash tokens capture/reuse. Reject directories where a file is expected. Additional unnamed paths are unobserved; use Git changedPaths to assert a commit touches exactly its permitted paths. |
| `jsonFiles` | Named UTF-8 JSONL files (one object per line, a single JSON object counts as one row); parse and compare complete ordered rows just like jsonRows. Useful for required recovery journal events. No private snapshot synthesis. |
| `timings` | Named real integer measurements, compared with JInt or integer JSymbol only: `elapsed_ms` for this command/setup operation; `stdout_first_ms` / `stderr_first_ms` for first nonempty stream arrival; `output_match_ms` for the end of an AwaitOutput match; `exit_ms` for actual termination. Arrival/exit times are milliseconds since trace start on the runner's monotonic clock. A missing event fails an enabled observation. Capture then use relations for immediate watch output, bounded return or successive changed frames; never divide these by TIME_SCALE. |
| `relations` | Resolve both scalar expressions/tokens and check Same/Different typed equality, inclusive IntRange, exact IntDelta (later−earlier), or IntAtLeastDelta. Numeric relations use integers, not string lexicographic order or timing tolerances invented by the runner. |

An enabled Git field unavailable for an unborn repository (subject/tree/parents) is an invalid expectation, except
the explicitly Optional head fields. Observe additional worktrees through explicit GitCommand observations and
absolute named file paths. Never obtain a tree by staging user edits into the user's index.

Portable patterns use literals, character classes/ranges, groups, alternation, `.`, `*`, `+`, `?`, `{m,n}`, `^`/`$`
and escaped literal punctuation. Match a whole text (`^...$` is implicit), with dot excluding LF; use `[\s\S]` for
multiline text. No backreferences, lookaround, Unicode categories or engine-specific flags. Pattern `${name}` reuse
is regex-escaped. Captures in regex are ordinary groups only; binding captures use the explicit token grammar below.

## Placeholders, captures, and reuse

Binding tokens use `${name}`. Reserved baseline bindings above and captures are trace-local and immutable. Names
match `[A-Za-z][A-Za-z0-9_.-]*`. Literal `${` is written `$${`; perform a single substitution pass. Unbound reuse
is an input error. Match captures **only in expectations**, never in commands/setup inputs:

```text
${capture:landed:oid}       full lowercase Git id, 40 or 64 hex characters
${capture:approval:hex}    nonempty lowercase hex (approval domain controls its length)
${capture:build:id}        nonempty identifier [A-Za-z0-9_.:-]+
${capture:queuePid:pid}    positive integer; command ownership separately verified
${capture:expiry:ms}       nonnegative integer timestamp/duration
${capture:log:path}        absolute path inside this trace directory
${landed}                 exact reuse of the captured typed value
${prefix:approval:6}       first 6 characters of a previously bound string
```

`JSymbol("${capture:expiry:ms}")` matches a JSON integer and binds that integer; it must not match a JSON string.
`JString` may embed string captures/reuse; `JInt` matches the literal integer. `JDecimal` is a canonical exact decimal
number, not a float; normalize JSON numeric spellings to an exact rational value, preserving integer versus fractional
values. A fractional value cannot match JInt. `JSymbol` contains exactly one typed token/reuse and adopts its JSON
scalar type. Paths/ids/hashes are strings; pid/ms are integers. In string contexts those integers render in decimal.

The first capture occurrence binds; subsequent occurrences of that capture name must equal it and keep its type.
Match non-placeholder text literally. Reject ambiguous adjacent variable-length captures without a delimiter; a
failed comparison never updates the live binding table. Compare a step using a tentative table, then commit all
bindings only if **every** enabled field and relation passes. Evaluate fields in the order in Expect above, maps in
lexicographic key order, JSON atoms in lexicographic Pointer order, lists in order; references must be captured earlier
in that traversal or in an earlier step. Step-local relations run last. Map/path keys can reuse earlier bindings but
cannot introduce captures. Never bind different model identities to one concrete identity unless equality is intended;
emit Different relations where required. Time captures are not unrestricted wildcards: emit IntRange/delta relations
or clock-controlled literal values for timing/retention clauses. Relation operands are literal strings, signed
decimal integers, or the binding/prefix tokens above; they are not an expression language. Int relations require
integer literals/bindings. All equality remains typed.

For each JsonRow flatten a parsed JSON value: objects records every object Pointer, arrays maps every array Pointer
to length, atoms maps every scalar Pointer to a typed atom. Root Pointer is `""`; `/` and `~` in member names escape
as `~1` and `~0`; array indices are canonical decimal. Compare all three domains exactly. This preserves null versus
missing, nested recovery/events, empty objects/arrays, and full key sets without recursive Quint types. A model may
not omit a container to gain partial matching. Arbitrary unknown JSON keys require an explicit schema decision,
not a runner filter. Opaque OPEN formats can be checked via specified semantic projections or named file effects.

## Provider scripts and nondeterminism

`providerScript: Present(id)` selects an immutable, manifest-digested fake-provider scenario. Route this command's
complete KOGEN_PROVIDER_URL to the local `/scripts/<escaped-id>/responses`; the fixture owns a FIFO request cursor per
id for this trace. Concurrent commands use distinct ids. Missing means no provider interaction expected from that
command, except a explicitly inherited scripted seam endpoint; each manifest states the intended request count.
An explicit conflicting SetEnv URL is rejected unless testing an invalid URL. Script cursors never silently reset.

A script is a sequence of request predicates and responses: required model/effort, role/tool permissions and input
fields; HTTP status/headers; exact Responses/SSE chunks or malformed bytes; disconnect/empty stream; gate label or
real delay; and optional tool-call results followed by subsequent response turns. Tool calls ask Kogen to perform
ordinary edits/check commands through its own dispatcher; the fake server cannot write the candidate directly or
claim verification. Capture request-generated thread/response ids if needed. Predicates and expected request count
are assertions; wrong model/role, unexpected/extra request or unconsumed required turn fails the trace. Gate arrival
is an out-of-band runner observation of its own server, not a new Kogen API. Keep script records/transcripts as plain
JSON plus byte blobs; language choice for the server is free. OPEN wire fields are compared only where CORE fixes
semantics. New scripted results must come from new Quint choices, not hand-edited ITF or expected output.

The version-1 script envelope in `manifest.scripts[id]` is `{schema:1,digest,turns,min_requests,max_requests}`;
`digest` covers the envelope excluding itself. A turn is:

```json
{
  "request": {
    "method": "POST",
    "headers": {"content-type": "application/json"},
    "equals": {"/model": "gpt-6-luna", "/reasoning/effort": "max"},
    "present": ["/input"]
  },
  "response": {
    "status": 200,
    "headers": {"content-type": "text/event-stream"},
    "chunks": [{"bytes": {"utf8": "<fixture SSE bytes>"}, "gate": "reply-1", "delay_ms": 0}],
    "disconnect": false
  }
}
```

This is a format example, not a valid green SSE fixture. `equals` uses JSON Pointers and complete literal native
JSON values after binding substitution; `present` checks existence (null still exists). Request header names are
case-insensitive and named values exact after optional surrounding HTTP whitespace; extra headers/JSON fields are
unobserved. Scripts must name model/effort and any role/tool/input assertions needed for their clause; optional
wire metadata is not globally scrubbed. Byte blobs use exactly one `utf8` string or `octets` integer list; chunks
are written in order. Gate is null or a unique label, and pauses before writing that chunk until released; delay is
nonnegative real ms after release. `disconnect=true` aborts the connection after these chunks; otherwise finish
the response normally. `min_requests` and `max_requests` are explicit integers with
`0 <= min_requests <= max_requests <= turns.length`. A request consumes its turn on arrival, even if Kogen later
cancels it; count all attempts. At trace end, require the count within bounds. An unexpected request/predicate
mismatch fails the trace and responds with a bounded error rather than hanging. ProviderGate await observes the
arrival at its chunk gate. Abort remaining gated connections during teardown. The analogous OpenID fixture uses
literal discovery/JWKS/token/revocation responses and validates dynamic state/nonce/PKCE against the captured
authorization request; it must not replace those checks with a fake successful `provider login` output.

Retries, scheduler timing, randomized provider retry jitter and OS ids may differ within the modeled bounds. Make
semantic choices deterministic through the script; capture ids, and assert time bounds instead of fixed real
timestamps. Use provider gates for in-flight Build/crash/setup, and the documented barriers for precise Git races.
If a required seam/capability is absent, report `blocked(seam-or-capability)` with clause IDs, never `passed` or a
real-sleep substitute for a 14-day expiry. Expected implementation divergences are reported as named failures
(or separately inventoried expected failures); they may not change the contract oracle to match today's binary.

## Seeds, counts, and coverage

Pin the TypeScript backend to avoid dependence on a downloaded evaluator or thread scheduling. Generate exactly
one ITF per seed, with `--max-samples=1 --n-traces=1`; different traces are separate runs, not multiple samples from
an unspecified PRNG stream. With main module `init` and seed 1000000, the invocation is:

```sh
../../quint-cli/quint.sh run spec/quint/init.qnt --main init --backend typescript \
  --seed 1000000 --max-samples 1 --n-traces 1 --max-steps 40 \
  --invariant invariant --out-itf /tmp/kogen-init-1000000.itf.json
```

Runnable module indices are fixed: cli=1, git=2, process=3, config=4, intent=5, shape=6, approve=7, build=8,
check=9, landing=10, queue=11, init=12, status=13, recovery=14, kogen=15. IO has no trace count. For module m,
seed j is `1000000*m+j`. The example command's seed is illustrative; the init profile uses 12000000+j.

- Fast profile: j=0..7 (8 traces per runnable module), maximum 40 transitions, scale 1 unless explicitly modeled.
- Full profile: j=0..127 (128 traces per runnable module), maximum 200 transitions. Include platform-specific
  process/check fixtures on macOS and Linux separately; missing host coverage remains visible.
- Maintain a checked-in seed/witness manifest per clause. Each normative clause must have at least one observable
  positive witness; each stated error/guard must also have a negative witness. Composition witnesses must include
  approval invalidation, exact-tree check binding, four moved-base turns/park, failed hooks, lost CAS, crash
  preservation and expiry, and watch/recovery observations. Seed count alone never establishes coverage.

Use additional increasing j=128..4095 only to discover missing witnesses, then retain the selected seeds explicitly
in the manifest and replay them in both profiles. No time-derived seeds, cherry-picking to remove failures, hidden
filtering of uninteresting traces, or handcrafted conformance scenarios. Record all generation failures/deadlocks;
an intentional terminal state stutters with lastStep=[] until the bound. Reject an all-empty trace as conformance
coverage. A failed model invariant is a specification failure before replay. Stop replay at the first mismatch,
retain artifacts, and optionally shrink by regenerating a shorter seeded trace with valid preconditions. Never
delete arbitrary setup steps to claim a minimized valid trace. A profile is complete only when requested trace
counts, clause witnesses, required seams, and all enabled comparisons succeed.

## Runner cleanup options

`kogen-conformance run --workdir DIR` sets the root for case, feature, Quint
trace, and runtime version metadata temporary directories (default `/tmp`).
Use a separate workdir for each concurrent scorer. Case teardown scans cwd
owners before deleting the case directory, rescans after 0.3 and 1.0 seconds,
and kills process groups as well as individual PIDs. A final scan covers the
whole workdir; processes killed there are recorded as teardown notes and do
not change case pass/fail status.
