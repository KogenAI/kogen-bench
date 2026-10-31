# Hard-task harness overlay (`lanes/hk/`)

The hard-task packs (`reproduce/ccs3-lm-hard-tasks`, `ccs2-mb-hard-tasks`, `cco-mb-hard-tasks`, `hk3-lm-hard-tasks`, `hk3-mb-hard-tasks`, `hk4-lm-hard-tasks`) compare Kogen with an agent run on its own. The published `lanes/` runs Kogen's side. The agent-on-its-own side and the grading of a final tree against the task's public scenarios were added to the harness by a small overlay. It is published here so that everything but the task kits can be rerun.

| file | what it is |
|---|---|
| `adapter_codex.py`, `adapter_claude.py` | the alone-arm driver for Codex CLI and for Claude Code (`hk_adapter.py` in the snapshot). Each wraps `bare/lanes_bare.py`, refuses to start unless the experiment's `hk_study` matches `HK_STUDY`, and checks the model, effort and fixed binary path against the experiment file. Only the study id is a placeholder. |
| `gocache.py` | stages one Go build cache per task so every setup starts from the same cache; the runs used it. |
| `apply_overlay.py` | copies `lanes/` into a new directory, installs the adapter and `gocache.py`, and edits `cell.py`, `costguard.py`, `grading.py`, `report.py` and `approvecache.py` (alone-arm dispatch, spend of alone cells, grading from the public scenarios, "not evaluated" shape class, the Go cache). Every edit fails if its anchor is missing. |

```sh
python3 lanes/hk/apply_overlay.py --study hardplan3-20261030 --arm codex --out "$SUPPORT"
HK_STUDY=hardplan3-20261030 "$SUPPORT/source/lanes/bin/lanes-run" "$RUN" --tasks "$TASKS" --hosts hosts.json
```

`--study` is the experiment file's `hk_study` value and `--arm` is `claude` for the Claude Code packs. `hosts.json` for the Claude Code arm also names `claude_bin` (the fixed Claude Code release path, equal to `hk_claude_bin` in the experiment) and `kogen_token_home` (the sign-in directory). The experiment files in the packs carry placeholders for these paths.

The overlay was built on the `preflight5-20261030` lanes release. The published `lanes/` also holds the timeout ledger, which the run snapshots did not have; it applies the same way, and no result in a pack depends on it. Checked 31 October 2026: applied to the published tree, the overlay reproduces the run snapshot's edits to `cell.py`, `grading.py` and the adapter exactly, and the snapshot's other differences are the timeout ledger and comments. The overlay itself was not rerun on a model.

Withheld: the task kits (start trees, hidden tests and public scenarios of the hard tasks) stay private until the Kogen hill-climb ends; no date is set. Publishing them would let the climb fit the tests. The task names and counts are in each pack's `tasks.txt`.
