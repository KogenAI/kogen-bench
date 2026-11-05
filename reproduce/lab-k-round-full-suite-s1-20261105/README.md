# Changed-first checks in build rounds: the targeted form is not cheap enough, so no cells were run

**Finding.** Stage 1 of the round-suite Lab asked whether a build round could run a heavy check in a targeted form (only the tests that belong to the changed files) and run the full suite once on the final tree. The model-free gate timed the targeted form against the full `mix test` on the frozen start trees of the four slow-suite tasks. The targeted form cost at most half the full suite on 2 of the 4 tasks (documentation-lookup-evidence 0.02, opencode-go-subscription 0.23). On prompt-cache-reuse-and-usage it cost 0.69 of the full suite, and on shaping-technical-discovery no test maps to the changed files, so the targeted form would check nothing. The gate needed 3 of 4. Arm A2 has no proven headroom on these tasks, no seat or API cell was run, and the row closes as measured.

## Question
Stage 0 (lab-slow-checks-rerun-s0-20261105) left one arm open: A2 changed-first. Its saving is bounded by the targeted run's cost `f` as a share of the full run (median verify-wall saving 52% / 41% / 29% at f = 0.1 / 0.3 / 0.5), so the Stage 1 bar (median verify wall down 25% and at least 3 min) is reachable only if `f` is at most about 0.5. Registered gate (Studio Lab lever lab-round-suite-reuse-s0-20261105): continue to the 16 cells (A0 vs A2) only if `f <= 0.5` on at least 3 of the 4 tasks; otherwise stop and publish the negative result.

## Method
Model-free, no seat, no API key. One host (the Studio, as the research runner user), one run at a time, MIX_ENV=test, Elixir 1.20.4 / OTP 29, the frozen `start` tree of each of the four tasks (documentation-lookup-evidence, opencode-go-subscription, prompt-cache-reuse-and-usage, shaping-technical-discovery), dependencies fetched and compiled before timing.

- Full suite: `mix test` with no arguments.
- Targeted form, fixed before the first timing: take the lib files the task's landed solution changed (the reference diff, a stand-in for "the files a typical fix touches"). The wide form runs every test file that mirrors a changed file by name or mentions a module defined in a changed file. The narrow form runs only the mirror-named test files. `data/targets.json` lists both sets.
- Fallback rule: when no test maps to the change, the targeted form falls back to the full suite (ratio 1.0). Running nothing is not a cheaper check.
- The primary form is wide (the safer to use as a repair signal). The gate verdict is the same for the narrow form.

## Results
| task | full `mix test` | wide targeted | f (wide) | narrow targeted | f (narrow) |
|---|---|---|---|---|---|
| documentation-lookup-evidence | 854 s | 18 s (1 file) | 0.02 | none maps (falls back) | 1.00 |
| opencode-go-subscription | 803 s | 187 s (14 files) | 0.23 | 2 s (6 files) | 0.00 |
| prompt-cache-reuse-and-usage | 441 s | 306 s (4 files) | 0.69 | 2 s (2 files) | 0.01 |
| shaping-technical-discovery | 1,087 s | none maps (falls back) | 1.00 | none maps (falls back) | 1.00 |

Tasks with f at most 0.5: 2 of 4 (wide), 2 of 4 (narrow); gate needs 3. **Verdict: A2 no headroom, stop before any cell.**

- Counting a form that maps to no test as free (f = 0) would give 3 of 4, but that form verifies nothing in the non-final rounds, so the builder gets no repair signal from it; Stage 0 found the red output was used to repair after 24 of 24 non-final slow-check failures.
- On the lead task (prompt-cache-reuse-and-usage) the wide form still takes 306 of 441 s because it includes the slowest integration files. The narrow form is fast (2 s) but only exercises two mirror-named files.
- The mapping needs a Build to know which tests belong to a change. Three of the four tasks have a module referenced by tests under different file names, and one has no test at all for the changed modules.

## Limits
- The host was heavily loaded during the timings (one-minute load 16 to 150, see `data/gate.tsv`), so absolute seconds are noisy; the ratios that decide the gate are far from 0.5 except prompt-cache-reuse-and-usage (0.69, both runs at load 16-17).
- The scratch trees are not git repositories, so every full run had failing tests (10, 7, 9 and 78 failures; the 78 on shaping-technical-discovery include timeouts under load). Failing full runs may be slower than green ones, which would raise the true ratios, not lower them.
- The tasks' own configured `test` check is already a hand-picked regression list, not the whole suite; the Stage 0 Elixir Builds (`mix test` 469-974 s) are the population the lever targets.
- The escape rate (green targeted, red full) was not measured; with the gate failed it is not needed for the verdict.
- One run per form per task; no repetition.

## What this decides
- A2 is not taken to cells: the 16-cell plan (about $160, A0 vs A2, st, seats) is not run and no REQUEST is filed.
- k-round-full-suite closes as measured: A1 and A3 had no headroom in Stage 0, and A2 fails the cost gate in Stage 1 on these tasks.
- Reopen only if a per-change test mapping exists that is cheap on the large integration files (not file-name matching), or a different, slower task set is chosen.

## Rerun
```
cd reproduce/lab-k-round-full-suite-s1-20261105
python3 -I report.py data/gate.tsv data/targets.json data/results.json
```
`data/gate.tsv` has one line per timed run (task, run label, exit code, seconds, one-minute load); `data/targets.json` the changed lib files and the test sets of both forms; `data/results.json` is the script's output and holds the numbers above. The task trees are the frozen start commits of the Studio repository (see the kogen repository on GitHub, commits 70506bb for prompt-cache-reuse-and-usage and the matching start commits of the other three tasks); no source is copied into the pack.
