# Harness releases

The code that produced each published finding, pinned by hash. A finding's `reproduce/<finding-id>/README.md` names one release below and the exact command.

Each file was copied from the host that ran it. Files that named a host, a private path or an account were changed only to read those values from environment variables, with documented defaults. `releases/sanitized-files.tsv` lists every changed file with the sha256 of the original (the hash recorded in run manifests and protocols) and of the published copy. Unchanged files keep their original hash.

## Lanes (Kogen runs)

| release | used by | base commit | changes since the base |
|---|---|---|---|
| `preflight5-20261030` | Kogen runs started from 30 Oct, after the preflight5 queue entry went live | `11d9739c15be871c6ecb97719bf9cd80a49c4a75` | uncommitted, all shipped here: priced and unpriced cost totals (`usage.totals`: `priced_usd`, `unpriced_stages`, `cost_complete`; costguard and export fall back or publish no cost when a total is partial), task deferral after two timeouts (`lanes/timeoutguard.py`, `LANES_TIMEOUT_LEDGER`), a stable grader binary path behind a file lock, a spend ledger per key name in `ops/day-runner.sh` |
| `preflight3-20261030` | Kogen runs started 30 Oct between 06:55 UTC and the preflight5 switch | `8a9ecbf7c64e964405676ebd1852ca0191944570` (branch `fix/defer-approval-timeouts`; the queue entry first pinned `e9d1fbbb`) | the same grader-lock change in `lanes/grading.py` |
| `7a0e22ad` (28 Oct) | runs before 30 Oct | `7a0e22ad` | none: this was the `lanes/` tree published before this release |

`lanes/`, `bin/`, `tests/` and `grade/` in this directory are `preflight5-20261030`. What it adds over 28 Oct:

- **npm cache** (`lanes/node_modules.py`, `bin/lanes-stage`): locked npm dependencies are staged once into `LANES_NPM_CACHE` (default: `node-cache` beside the repo) and reused.
- **Approval deferral** (`lanes/approval.py`, `lanes/carry.py`, `bin/lanes-carry`): a preflight approval that times out defers its task, keeps it in the plan and is retried by the next unit; the report marks the run incomplete instead of dropping the task.
- **Refusal logs**: a refused approval keeps its full output.
- **Approval reuse** (`lanes/approvecache.py`, `LANES_APPROVAL_CACHE`): a successful approval is reused only when every input hashes the same (Kogen sha, patch and artifact hashes, Node, the environment Kogen inherits, the harness code); a real refusal blocks reuse for that key. Unset, nothing changes.
- **Priced and unpriced totals** and **timeout deferral**, as in the table.

To get `preflight3-20261030`: `patch -R -p1 -d lanes < lanes/releases/preflight3-to-preflight5.diff` (Python and tests only; in `ops/` preflight3 lacks the timeout ledger and the key-name spend ledger, and its entry script pinned the preflight3 tree). File hashes of both releases, as run: `releases/preflight5-20261030.sha256` and `releases/preflight3-20261030.sha256` (`ops/` excluded: its originals name host paths; their hashes are in `releases/sanitized-files.tsv`).

`ops/` holds the queue scripts that drove the runs: `run-queued-entry.sh` pins new units to a release, `run-queued.sh <cg|cc|cgr|ccr> <id> <tasks dir> <slots> <cell estimate>` prepares and runs one experiment under a per-day spend guard (`day-runner.sh` for Anthropic keys, `day-runner-v3.sh` for ChatGPT with a weekly guard). Command, from the repo root:

```sh
LANES_RELEASE=$PWD/lanes LANES_P=$HOME/lanes-work lanes/ops/run-queued-entry.sh cg <experiment-id> tasks 1 0.3
```

`LANES_P` is the private work dir (experiments at `$LANES_P/<id>/experiment.json`, run dirs at `$LANES_P/runs/<id>`); `LANES_KH`/`CHATGPT_KH` is the Kogen home holding the provider sign-in (default `~/kogen-home`). Without the queue, the same run is `lanes-plan`, `lanes-preflight`, `lanes-run`, `lanes-grade`, `lanes-report` (README.md).

Tests: `sh lanes/test.sh` (Python 3.11+, Go, git). For this release, `tests.test_usage`, `test_approval_reuse`, `test_timeout_deferral`, `test_node_modules`, `test_approval_deferrals`, `test_costguard`, `test_report` and `test_preflight` (117 tests) passed on 30 Oct with Python 3.13 on macOS; the full `test.sh` (Go grader builds) was not rerun for this release.

## Bare harness (`bare/`)

`bare/lanes_bare.py` runs one coding agent on a task with no Kogen around it (kogen-loop, Codex CLI, Claude Code, Pi, opencode), then grades the final tree with this directory's grader. The head-to-head findings use it.

| variant | used by | file | original sha256 |
|---|---|---|---|
| default instructions (29 Oct 17:09) | h2h-30 (both tools at medium and high, 24 tasks, Linux); the EU same-key confirmations (`confirm-eu/`) | `bare/lanes_bare.py` | `9744637db945c7d897918a970524087586c21e5323394bc8bf0edc417448c99a` |
| timestamped events, older base | shelltail (macOS) | `bare/shelltail/lanes_bare_ts.py` | `e2100d02dfe58b4f5328a1615dac7dacedfb5d51314953d9e2a1ef7c0896fac7` |

h2h-30 imported the lanes modules of the 28 Oct tree (`7a0e22ad`: `cell.py` `0f01df2b…`, `grading.py` `eb78d0a4…`, `usage.py` `a5bbe19f…`, as its run manifest records); to rerun it exactly, set `LANES_DIR` to a checkout of `lanes/` from before this release.

The shelltail copy is `lanes_bare.py` `67a1c527db1ab28b0495f2a027787018bc0e7088e76cf82e69e415fc8ecef96e` (before 29 Oct 17:09: kogen-loop still got the one-line instruction "You are a coding agent working in the supplied repository." instead of its shipped default) plus one change: each agent event line is also written to `events-arrival.jsonl` with its arrival time. See `bare/README.md`.

## Same-key EU extension (`confirm-eu/`)

`confirm-eu/confirmation_ext.py` wraps `bare/lanes_bare.py` (`9744637d…`) for runs where both tools use the same OpenAI API key — a local gateway forwards each tool's Responses requests to the one upstream with the key, records each request's usage and list price, and enforces a measured spend guard (a cell is admitted only if spend so far plus a conservative estimate stays under the round cap; an admitted cell is never cut). Tool shells run in nested bubblewrap namespaces without network. `run_confirmation.py` is the round driver; `run_replay13.py` resumes a round with a measured estimate and a one-request credit (quota) probe before each admission. Original hashes: extension `19c9755dd572750afd94f39d78b4d29dc8ec933377e77c3c7fc7fa1a79df7249`, driver `ff5bab0d0cb4a8f064f3abf8e7b51a72185c48a863f0d9d3f2bcbdf55faf86ab`, replay13 `0b4c06b14a57a8b47c6174b9252f1d0d1ad93a40ac64654ba33e3eef68647e31`. See `confirm-eu/README.md`.

## Loop patches (`patches/loop/`)

Applied with `patch -p1` to kogen-loop at `b8a4046`; `patches/loop/SHA256SUMS` lists them.

| patch | sha256 | tool name in findings | built binary sha256 (linux x86_64) |
|---|---|---|---|
| `api-replay.diff` | `440f72fd1b31befbe07f88da7abe19485883b0664e626be143b73abe0985899e` | Replay patch (native Responses with encrypted reasoning replayed) | `586f0314107a42736636bf30a69b3afa3eb31319de9fe837394a586046444eae` |
| `highwall-write-check.diff` | `ce4fc7acb5f23afb9d7cd06a0ac2e7705647e92fd0ee014fa5f2112ba4cca654` | kogen-loop with write-check patch | `7c1af4b2851ed6885e1e7393b3707f5a10a179cd9f3124e0413133d574a7dae5` |

Unpatched kogen-loop `b8a4046` built `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817` (EU runs), `20ff81d9d5cc77c1e2aa8dd0008cc6268d9a9a3b358a3aa2efd6836a69ce1238` (h2h-30) and `ca916aaf90ebc3c87e9c9750466086eb2358608aae683078b3b5d52a45b73568` (shelltail, macOS arm64). Patches for unpublished results (overlap, batch/exec) are not shipped.

## Tools

| tool | version | where |
|---|---|---|
| Codex CLI | 0.165.0 (x86_64-unknown-linux-musl), binary `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5` | h2h-30, EU runs |
| Codex CLI | 0.166.0 (aarch64-apple-darwin) | shelltail |
| model | `gpt-6.1-terra`, effort medium or high as each finding states | all of the above |
| Go / Node (EU runs) | 1.27.2 / 24.21.0 | read-only in the tool namespace |
