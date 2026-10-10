# Kogen black-box conformance runner

The runner drives the public `kogen` executable and compares process output,
JSON rows, files, Git state and timings. It supports the original JSON smoke
cases and Quint 0.33 ITF traces. Quint traces are replayed from each state's
`lastStep` list using the contract in [`QUINT-SUITE.md`](QUINT-SUITE.md) and
the shared types in [`kogen_io.qnt`](kogen_io.qnt); the runner does not call
Kogen's internal Rust lifecycle code.

## Run it

Run these commands from the race directory with your own implementation; implementation source and binaries are not published here.

```sh
suite/bin/kogen-conformance list
suite/bin/kogen-conformance run --kogen /path/to/kogen
suite/bin/kogen-conformance run --kogen /path/to/kogen --case 'smoke.*' --jobs 4 -v --out results.jsonl
suite/bin/kogen-conformance run --kogen /path/to/kogen --timeout 60
suite/bin/kogen-conformance run --kogen /path/to/kogen --workdir /tmp/scorer-a
suite/bin/kogen-conformance summary results.jsonl
```

Generate seeded traces from the `suite/` workspace root:

```sh
suite/bin/kogen-conformance gen --model spec/quint/init.qnt \
  --seed 12000000 --traces 8 --steps 40 --out cases/quint/init/
suite/bin/kogen-conformance run --kogen /path/to/kogen --case 'quint.init.*' -v
```

`gen` invokes the pinned Quint 0.33.0 TypeScript backend at
`../quint-cli/quint.sh`, one trace per increasing seed. It writes a
`trace-N.itf.json` file and a companion `trace-N.manifest.json` for each seed.
The manifest records the import-closure source digest, command line, binary
version and digest, scripts and fixture digests, required capabilities,
clause IDs, witnesses and profile. Optional `--clause ID`, `--witness NAME`,
`--script ID=FILE.json` and `--fixture NAME=FILE` arguments attach the
corresponding metadata and byte fixtures.

`run` discovers JSON cases, ITF traces and executable Gherkin scenarios under
`features-src/` (and any `.feature` files under `cases/`). Each scenario is a
separate case with an ID such as `feature.04-lifecycle.init-creates-the-exact-bare-config-and-initial-history-commit`.
Its result includes the scenario's `@quint:` and `@core:` tags. The shared,
language-neutral step executor implements the complete vocabulary in
[`features-src/STEPS.md`](features-src/STEPS.md); named Responses and OpenID
fixtures are defined in [`features-src/FAKES.md`](features-src/FAKES.md). Use
`--case` to select either a scenario ID or a filename glob.

Every Kogen invocation has its own session/process group. The default hard
bound is 60 seconds; `--timeout SECONDS` sets a different maximum, and shorter
case or trace timeouts remain in force. The runner terminates each invocation's
process group on completion or timeout. After each case it also uses
`lsof -t -a -d cwd +D <case-dir>` to terminate any remaining process whose cwd
is inside that case, including detached children in new sessions. It rescans
at 0.3 and 1.0 seconds before removing the case directory, then sweeps the
whole run root at shutdown. `--workdir DIR` chooses the temporary root for
case, feature, Quint trace, and runtime version metadata directories; it
defaults to `/tmp`. Use a separate root for each concurrent scorer. Killed
processes are reported as teardown notes without changing case status.

Each Quint trace gets a fresh temporary HOME, unborn
Git repository and `home/`, `repo/`, `tmp/`, `bin/`, `control/` and `fixtures/`
directories. Its fake Responses server binds to loopback only. A trace that
requires an unavailable seam or capability is reported as `blocked`, with its
clause IDs; it is never treated as a pass.

Failures include the trace ID, state and step, concrete action, expected and
actual values, and a replay command with the seed. Results retain command
argv/environment, streams, observations, captures, provider transcript,
binary metadata and the first failing state/step. `--keep` retains the
per-trace sandbox for inspection.

The runner exits 0 only when every selected case passes. JSON cases use
`kc2-case-*` sandboxes; Gherkin scenarios use `kc2-feature-*`; Quint traces use
`kc2-quint-*` under the selected workdir. Git has a
local identity, signing is disabled, and global/system configuration is
isolated. Sandboxes are removed when each case ends; `--keep` preserves them.
Cases default to `KOGEN_TIME_SCALE=0.01`; the CLI can set a different default
and an individual case can override it. `--jobs` runs isolated cases
concurrently.

The standard library is the only Python dependency. Git and `sh` are available
to cases through the host PATH.

### Implementation environment

The legacy and Gherkin runners pass the runner's inherited `PATH` to Kogen. The
Quint runner puts the trace's `bin/` directory first, followed by that inherited
`PATH`, so fixture shims work while language tools such as Cargo, Go, Bun,
Elixir, Mix and Node remain available. A trace `Cmd.env` that sets `PATH` uses
that exact value. All runners pass through `RUSTUP_HOME`, `CARGO_HOME`,
`GOROOT` and `GOTOOLCHAIN` when set. If the Rust home variables are unset, an
existing `$HOME/.rustup` or `$HOME/.cargo` is used. This passthrough does not
copy host credentials or host `KOGEN_*` variables.

## JSON case format

Each `cases/**/*.json` file contains one case:

```json
{
  "id": "example.trace-001",
  "title": "A short human-readable description",
  "files": {"README.md": "fixture bytes as UTF-8 text\n"},
  "initial_commit": true,
  "time_scale": 0.01,
  "env": {"CASE_FLAG": "enabled"},
  "provider": {
    "script": [
      {"expect": {"role": "shaper"}, "tool_calls": [
        {"name": "write", "arguments": {"path": "out.txt", "content": "hello"}}
      ]},
      {"assistant_text": "Done."}
    ]
  },
  "steps": [
    {
      "argv": ["version"],
      "stdin": "optional input bytes",
      "env": {"STEP_FLAG": "value"},
      "timeout_s": 30,
      "expect": {"exit": 0, "stdout": {"regex": "version"}},
      "observe": {
        "head": {"sha": "{{capture:hash:commit}}", "subject": "{{capture:subject|.+}}"},
        "files": {"out.txt": {"equals": "hello"}},
        "status_json": true,
        "status_rows": [{"type": "queue", "state": "stopped"}]
      }
    }
  ]
}
```

`files` seeds checkout files. `initial_commit` records them before the first
step. Each step launches `kogen <argv...>` in the checkout. `stdin` is UTF-8;
`stdin_b64` is available for arbitrary bytes. Step environment overrides case
environment. `${SANDBOX}`, `${HOME}`, `${TMPDIR}`, `${CHECKOUT}`, `${AUTH_PATH}`
and `${FAKE_URL}` expand to per-case values. Exit, stdout and stderr are
captured for every step.

`observe.git` reports all branch heads and refs. `observe.head` reports the
current SHA, branch, subject, full body, parsed trailers and changed paths of
the latest commit. `observe.files` reads named project-relative files.
`observe.status_json: true` runs `kogen status --json` after the step when the
step itself did not run that command; parsed JSON Lines appear as
`observe.status_rows`. `observe.provider_requests` and
`observe.provider_oauth` expose the fake server's complete request logs.

Object expectations are recursive subsets. Arrays compare their expected
prefix, which allows a trace to check selected status rows or request fields
without pinning volatile additions. String expectations are exact unless
wrapped in an operator such as `{"contains":"..."}` or `{"regex":"..."}`.
Captures persist across all steps in a case:

- `{{capture:hash:name}}` captures a 7 to 64 digit hexadecimal hash.
- `{{capture:time:name}}` captures an integer timestamp or ISO-like time.
- `{{capture:id:name}}` captures an identifier.
- `{{capture:name|regular-expression}}` captures a custom match.
- `{{name}}` reuses a prior capture.

The fake provider accepts `assistant_text` / `final_text`, a list of Responses
`tool_calls`, and a `usage` object. Tool calls use the actual function names and
JSON arguments Kogen receives, so `read`, `search` and `write` operate through
Kogen's normal tool dispatcher. It emits `response.output_item.done` and
`response.completed` SSE events and records each request for assertions.

Scripted error values are `401`, `429` / `usage_limit`, `5xx` / `503`,
`malformed_sse`, `slow` / `slow_stream`, and `usage_limit_sse`. For a refresh
case, set `"auth":"owned"`: the sandbox gets a file-backed owned credential,
the fake answers the OpenID discovery, refresh-token and JWKS requests, and a
401 causes Kogen's normal refresh-and-replay path. The default `auth` is
`injected`, backed by the per-case `KOGEN_AUTH_PATH` file.

At the end of a case, each scripted provider response must have been consumed
and every request must have matched its script step unless
`provider.allow_unconsumed` or `provider_allow_unconsumed` is true. A step can
also assert request fields using `provider.script[].expect`; the full request log is
always included in the JSONL result.

## Current core seam

The current core already reads `KOGEN_PROVIDER_URL` for both injected and owned
Responses clients. The fake is pointed at `<loopback>/v1/responses`; there is
no pending endpoint override request to the core. Auth injection uses
`KOGEN_AUTH_PATH`, the credential store is forced to `file`, and time scaling
uses `KOGEN_TIME_SCALE`.

## Results

Each results file is JSON Lines: one metadata record followed by a record for
each case. The `summary` command reads this file independently of the
implementation executable.
