# Bare harness

`lanes_bare.py` runs one coding agent on one task with nothing around it, then grades the final tree with the lanes grader (`../grade/`), the same way a Kogen cell is graded. Tools (`--arm`): `loop` (kogen-loop), `codex` (Codex CLI `exec`), `claude` (Claude Code `-p`), `pi`, `opencode`, `kogen`. Each cell gets a fresh git workspace from the task's base, the task prompt, its tool's shipped default instructions, and an environment with tokens and routing variables removed; the hidden suite stays outside the workspace. A cell writes `result.json` (outcome, tokens, cost, wall), the agent's event stream, `final.diff` and `final-tree.tar`, then `evaluation.json`.

Release hashes and which finding used which copy: `../RELEASES.md`.

## Settings

| variable | default | what |
|---|---|---|
| `LANES_DIR` | this repo's `lanes/` | lanes package and grader the harness imports |
| `LANES_PRIVATE` | `~/lanes-work` | private work dir: agent sign-ins for pi/opencode, live-batch markers, `lanes.env` |
| `LANES_ENV` | `$LANES_PRIVATE/lanes.env` | sourced by `lanes-bare.sh` (PATH, toolchain, `KOGEN_LANES_HOME`) |
| `CLAUDE_BIN`, `CODEX_BIN` | on PATH | tool binaries |

Paths in a batch file go through `~` expansion only.

## Commands

One cell:

```sh
sh lanes/bare/lanes-bare.sh cell --tasks tasks --task <task-id> --arm codex --model gpt-6.1-terra --effort high \
  --codex-bin "$(command -v codex)" --codex-home ~/codex-home-bench --run-dir runs/one
```

A batch (h2h-30 layout: `examples/h2h-30.json`, 24 tasks × 2 tools × 2 efforts, one rep, one slot):

```sh
sh lanes/bare/lanes-bare.sh batch lanes/bare/examples/h2h-30.json --tasks tasks --run-dir runs/h2h-30 --slots 1
```

`paired.py`, `pubmetrics.py` and `pubagg.py` turn a batch's run dir into the task-paired comparison and the per-run rows used on the site; `paired.py` refuses rounds that are incomplete or lack the harness attestation.

## shelltail

`shelltail/lanes_bare_ts.py` is the copy that ran the shelltail rounds: an older `lanes_bare.py` (`67a1c527…`, where kogen-loop got a one-line instruction instead of its shipped default) that also writes each event's arrival time to `events-arrival.jsonl`. It ran on macOS with Codex CLI 0.166.0 and kogen-loop `b8a4046`, both at high effort. `run-shelltail.sh` runs a one-task dry batch first and starts the hard and broad batches only if both dry cells were graded:

```sh
cd lanes/bare/shelltail && sh run-shelltail.sh
```

## Offline check

`test/batch-fake.json` runs two fake Codex binaries (one copies the task reference, one does nothing) through a batch: no model calls. It needs `LANES_TASKS` set to a tasks dir holding `bytefmt-go`.
