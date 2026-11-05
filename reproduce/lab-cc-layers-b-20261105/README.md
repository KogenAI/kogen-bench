# lab-cc-layers-b-20261105

On the same model, effort, prompt, server and API key, is kogen-loop faster and lighter than Claude Code, and how much of the gap is Claude Code's own layers? **kogen-loop finished faster than every Claude Code setup: 0.80x the agent wall time of Claude Code configured exactly as Kogen runs it (97.5% CI 0.76-0.85, faster in 21 of 23 paired blocks) and 0.88x the wall of a lean Claude Code (0.84-0.92, 21 of 23).** It used 0.64x and 0.85x the uncached-equivalent tokens and list cost, and about 2-3 fewer model requests per task. It passed 21 of 24 tasks, against 20 of 23 and 22 of 23. Its three failures are two csvq-go repetitions and one splitter-go repetition. Stage B of Lab cc-layers-1 is descriptive: no product change follows from it directly.

## Setup

- **Tasks:** 12 Go tasks (`tasks.txt`; each has its task directory in `tasks/`), 2 repetitions each, giving 24 blocks.
- **Block order:** one block holds the four arms of one (task, repetition). Cells ran one at a time on one 4-core Linux server, with the arm order rotated per block. Every arm got the same prompt (the bare harness's `build_prompt`: request, acceptance scenarios, checks and rules).
- **Model and route:** claude-sonnet-5-5 at medium effort in every cell. Every cell used the same Anthropic API key.
- **Deadline:** 3600 s.
- **Grading:** cells were graded by the harness's own checks.
- **Server load:** no delivery job overlapped any counted cell; the runner sampled every 10 s.

| Arm | Client | What differs |
| --- | --- | --- |
| `loop` | kogen-loop `e5054c8` (the shipped default of the earlier head-to-head rounds), provider anthropic | its shipped default instructions (`patches/loop-instructions.txt`) |
| `claude-kexec` | Claude Code 2.1.312 | the exact arguments Kogen's executor passes for a build round: appended executor constraints (`patches/constraints.txt`), the build submission schema, the executor's tool settings, a fresh config dir, background tasks, auto-memory and updates off, Kogen's own pre/post tool hook |
| `claude-lean` | Claude Code 2.1.312 | same, but the constraints replace the system prompt (`--system-prompt`), tools limited to Bash, Read, Write, Edit, Glob, Grep, git instructions off |
| `claude-c2` | Claude Code 2.1.312 | `claude-lean` with kogen-loop's instructions as the system prompt instead of the constraints |

The arms are defined in `patches/claude-arms.diff`, which applies to `lanes/bare/lanes_bare.py`. Checksums are in `patches/SHA256SUMS`. Credentials reach Claude Code only on an inherited file descriptor, never through arguments, environment values or files.

## Results

| Arm | Cells | Passed | Checks passed | Median agent wall | Mean requests | List cost | Cost per pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `loop` | 24 | 21 | 2075/2098 | 36.8 s | 5.7 | $2.32 | $0.110 |
| `claude-kexec` | 23 | 20 | 1335/2091 | 45.4 s | 8.4 | $3.27 | $0.163 |
| `claude-lean` | 23 | 22 | 2084/2091 | 42.6 s | 8.0 | $2.55 | $0.116 |
| `claude-c2` | 24 | 24 | 2098/2098 | 44.5 s | 8.6 | $2.87 | $0.120 |

Paired over the blocks that hold both arms (geometric means; normal CI on per-block log ratios; exact two-sided sign test):

| Pair | Kind | Agent wall | Faster in | Sign p | Tokens | Requests per task |
| --- | --- | --- | --- | --- | --- | --- |
| loop / claude-kexec | primary, 97.5% CI | 0.804 [0.758, 0.853] | 21/23 | 0.0001 | 0.644 [0.606, 0.684] | -2.7 |
| loop / claude-lean | primary, 97.5% CI | 0.877 [0.836, 0.920] | 21/23 | 0.0001 | 0.853 [0.819, 0.889] | -2.2 |
| claude-kexec / claude-lean | secondary, 95% CI | 1.090 [1.047, 1.135] | 5/23 | 0.011 | 1.326 [1.271, 1.384] | +0.4 |
| claude-c2 / claude-lean | secondary, 95% CI | 1.016 [0.964, 1.071] | 9/23 | 0.40 | 1.027 [0.962, 1.097] | +0.7 |
| loop / claude-c2 | secondary, 95% CI | 0.859 [0.807, 0.914] | 20/24 | 0.0015 | 0.826 [0.774, 0.881] | -2.9 |

- **Tokens:** "tokens" means uncached-equivalent tokens: uncached input (including cache writes), plus 0.1 x cache reads, plus 5 x output. With one model on one key, this tracks list cost one to one.
- **Multiplicity:** both primary sign tests stay below 0.001 after the Holm adjustment over the two primaries.
- **Claude Code's own layers:** on this route, Kogen's executor arguments cost Claude Code about 9% wall and 33% tokens against the lean setup (`claude-kexec` / `claude-lean`).
- **Gap left:** kogen-loop is still 12% faster and 15% lighter than the lean setup. So most of the gap to Claude Code as Kogen runs it is not those layers alone.
- **One system prompt:** with kogen-loop's instructions, Claude Code (`claude-c2`) was no slower and no heavier than with the executor constraints. It passed 23 of the 23 shared blocks, against `claude-lean`'s 22.

Failed cells:
- csvq-go r1 failed in `loop`, `claude-kexec` and `claude-lean`, at 0 of 7 checks.
- csvq-go r2 failed in `loop` only, at 0 of 7.
- splitter-go r2 failed in `loop`, at 0 of 9.
- patchapply-go r2 failed in `claude-kexec`, at 0 of 9.
- task-tags-go r2 failed in `claude-kexec`, at 160 of 900.

## Limits

- **Missing block:** the run stopped at its own registered spend cap for the API key ($11.50; $11.0 spent) before the last block's `claude-kexec` and `claude-lean` cells. That leaves 94 of 96 cells and 23 paired blocks for the pairs involving those arms. The registered sizing needed 22.
- **Scope:**
  - One model at one effort.
  - One server.
  - Twelve small Go tasks.
  - Claude Code 2.1.312 only.
- **Pass counts:** too few failures to compare pass rates. kogen-loop's two csvq-go failures are a task-level weakness worth a look, not a measured difference.
- **What was measured:** agent wall time, from agent start to exit, excluding setup and grading. Not end-to-end Kogen Builds.
- **Missing comparisons:** Stage A (the same Claude Code arms on subscription seats) and the Codex leg have not finished and are not part of this finding.
- **Raw files:** the raw per-cell logs stay in the private round directory. `data/cells.tsv` holds every number used here.

## Rerun

```
python3 reproduce/lab-cc-layers-b-20261105/report.py
```

`report.py` rebuilds every table above from `data/cells.tsv`; the expected output is in `expected-output.txt`.

To repeat the runs:
1. Apply `patches/claude-arms.diff` to `lanes/bare/lanes_bare.py`, and put `constraints.txt` and `loop-instructions.txt` next to it.
2. Run one cell per (task, repetition, arm) with these flags:
   - all arms: `lanes_bare.py cell --tasks <tasks dir> --task <id> --arm <arm> --rep <r> --model claude-sonnet-5-5 --effort medium`;
   - the `loop` arm adds `--loop-bin <kogen-loop e5054c8> --provider anthropic`;
   - the Claude Code arms add `--claude-bin <Claude Code 2.1.312> --kogen-hook-bin <Kogen release> --claude-route api`.
3. Run the four arms of a block one after the other, with the order rotated per block.
