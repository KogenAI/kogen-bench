# Same-key confirmation extension

Runs kogen-loop and Codex CLI on the same OpenAI API key, through one local gateway, on a Linux host. Used by the EU same-key rounds (medium, high, wide, replay and the write-check short test). Release hashes: `../RELEASES.md`.

- `confirmation_ext.py` patches `../bare/lanes_bare.py` at import (`install(h)`); it changes no loop source. It starts a gateway on `127.0.0.1` per cell that forwards each tool's Responses requests to `OPENAI_UPSTREAM` with the key, caps `max_output_tokens`, serializes requests, and writes `route-receipts.jsonl` (model, usage, list price and an upper bound of the charge per request) and `route-summary.json`. Admission is checked before each cell only (`admit_cell`): spend so far plus a conservative estimate must stay under the round cap; an admitted cell is never stopped for budget. Tools run in bubblewrap (user, PID, IPC and UTS namespaces) with only the workspace and read-only toolchains; shells they start get a further namespace without network. A boundary probe records what the tool could read.
- `run_confirmation.py freeze|cell --index N` freezes `protocol.json` (task order, tools, model, effort, hashes of tasks, cache, grader, loop source and binaries) and runs one cell including grading.
- `run_replay13.py amend|login|cell|cleanup|spend [--index N]` resumes a frozen round with a measured per-cell estimate and, before each admission, a one-request credit probe on the same key and upstream (`max_output_tokens` 16, counted in spend); a quota or billing error stops admission.

## Settings

| variable | default |
|---|---|
| `LANES_CONFIRM_DIR` | `~/lanes-work/confirmation-eu-replay-20261030` (the round dir) |
| `CODEX_BIN_DIR` | `~/.codex/packages/standalone/releases/0.165.0-x86_64-unknown-linux-musl/bin` |
| `LANES_GOROOT`, `LANES_NODEROOT` | mise installs of Go 1.27.2 and Node 24.21.0 under `~/.local/share/mise/installs` |
| `OPENAI_UPSTREAM` | `https://api.openai.com/v1/responses` |
| `LANES_HOST_LOCK` | `/run/kogen-host-lock.d/expires` (expiry of the host lease; bounds a cell's deadline, never raises it) |
| `LANES_UID` | unset (when set, `run_replay13.py` refuses to run as another uid) |
| `KOGEN_LANES_HOME` | `~/.cache/kogen-lanes` |

The round dir holds `harness/lanes_bare.py` (this repo's `../bare/`), `grader/` (a lanes tree), `tasks/`, `bin/` (the kogen-loop builds: unpatched `loop-b8a4046` and the patched ones from `../patches/loop/`), `source/kogen-loop`, `cache-snapshot/`, and the two sign-ins, each made with its tool's own login command reading the key from stdin: `login-codex/` (`codex login --with-api-key`) and `login-loop/.kogen/credentials/openai-compatible.json`. Only the gateway reads them; no credential is mounted into a tool's namespace.

## Command

```sh
cd "$LANES_CONFIRM_DIR" && python3 run_confirmation.py freeze && \
  for i in $(seq 0 23); do python3 run_confirmation.py cell --index $i || break; done
```
