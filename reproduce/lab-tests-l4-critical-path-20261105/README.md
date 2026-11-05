# The tests request's time budgets cannot be priced from the recorded logs: 9 of 15 repo-by-host rows are above budget and only kogen's packaging and builds (81 s) have a recorded cost

Finding `lab-tests-l4-critical-path-20261105`. A model-free Lab (no model call, no suite run, 5 Nov 2026), step 0 of Lab L4 of the K-TESTS-ACCEPTANCE-FIRST request. The Studio record `lab-tests-l4-critical-path-20261105` was registered before the projection and holds the fixed rule. (The raw suite medians of the earlier build-speed analysis were already known when the rule was written.)

## Question

The request sets time budgets for each repo's whole configured verification: kogen 60 s, kogen-loop 10 s, kogen-build 60 s, kogen-shaping 45 s, every other component 20 s, cold test cache, on a 4-core Linux host and a MacBook, quiet. Can its section 4 (tiers, package once, parallel by default) and the section 6 delete/rewrite lists reach them? Step 0 uses recorded data only.

## Inputs (window 3 Nov 09Z to 5 Nov 09Z)

- `data/suite_walls.json`: wall seconds of every recorded `go-test` command per repo and host class, from the heavy-lock logs (median, p90, runs, failures). Host classes: `macbook`, `mac-studio`, `linux-a` (a Linux server), `linux-2core`.
- `data/adoption_steps.json`: step seconds (`go`, `acceptance`, `setup`, `build`) of the kogen adoptions of the window.
- `data/package_times.json`: package-level `ok <pkg> <s>` seconds from adoption and land logs.
- `data/static_counts.json`: tests and `t.Parallel()` calls per repo at the main snapshots the request names.

No per-test durations exist in the window (no `go test -json` or `-v` output was kept; only suite wall, package lines and the `running tests` dump of timed-out runs).

## Fixed rule

Projected path = recorded median wall minus priced savings. A saving is priced only if it is packaging charged once ((8-1) x the recorded `setup` step), builds charged once ((12-1) x the recorded `build` step), or a REL/DEL test with a recorded or stated duration that is not `t.Parallel()`. Every FAST, REW and MOVE item without a recorded duration removes 0 s. Yes: every measured repo within budget on the MacBook and the Linux server. No: a retained item exceeds a budget on its own. Unresolved: otherwise, each repo above budget a named gap.

## Result (seconds; `data/l4.json` has every row)

| Repo | budget | MacBook median | Linux server median | priced savings | gap (MacBook / Linux) | tests / `t.Parallel()` calls |
|---|---|---|---|---|---|---|
| kogen | 60 | 252 | none recorded | 81 | 110 / - | 746 / 661 |
| kogen-build | 60 | 331 | 235 (p90 605) | 0 | 271 / 175 | 517 / 476 |
| kogen-shaping | 45 | 120 | 216 (p90 609) | 0 | 76 / 172 | 503 / 15 |
| kogen-loop | 10 | none recorded | 80 (2-core server: 806, 7 of 7 runs failed) | 0 | - / 70 | 568 / 644 |
| kogen-verification | 20 | none recorded | 42 | 0 | - / 22 | 222 / 0 |
| kogen-coordinator | 20 | 27 | 8 | 0 | 7 / 0 | 351 / 1 |
| kogen-setup | 20 | 48 | 11 | 0 | 28 / 0 | 171 / 2 |
| kogen-executor | 20 | 17 | 18 | 0 | 0 / 0 | 258 / 125 |
| kogen-review | 20 | 8 | 7 | 0 | 0 / 0 | 158 / 46 |

Of 15 repo-by-host rows on the two budget classes, 6 are within budget today and 9 are above it.

- **The named real waits are already parallel.** The two approve-deadline tests (130 s and 120 s) call `t.Parallel()`, and kogen has 661 such calls in 746 tests, kogen-build 476 in 517. Moving them to the release tier lowers the floor of the `kogen` package (measured median 273 s) but removes nothing from a suite whose wall is work divided by cores; the same holds for the 47 s scenario under `cucumber --parallel 4`. The gap in these two repos is CPU work, which only deleting or shrinking tests removes, and the logs cannot price it.
- **Non-parallel repos** (shaping 15 of 503, verification 0 of 222, coordinator 1 of 351, setup 2 of 171). If every test became parallel and scaled perfectly on 4 cores, the floor is the wall over 4: shaping 54 s on the Linux server (above 45) and 30 s on the MacBook; verification 10.5 s; setup 12 s and coordinator 7 s on the MacBook. This assumes CPU-bound tests.
- **kogen's whole configured verification** also has the offline acceptance step (273 s median in adoption variants, 85 s in the final window with 3 runs). The request's budget wording does not say which of the 267 offline scenarios are fast tier and its list removes only one 47 s scenario from them, so the acceptance step alone is above 60 s unless the fast tier is a small named subset.
- **kogen-loop** on the 2-core Linux host failed every recorded run at about 806 s, the process-death hang the request's section 5 targets, so its 10 s budget cannot be measured there before that fix.

## Verdict

**Unresolved.** No row above budget is shown reachable and none is shown unreachable; no retained item is above a budget on its own, so the verdict is not `no`.

## Step 1

One per-test `go test -json` profile per repo, cold cache, 1 repetition, on a quiet 4-core Linux host and the MacBook: about 45 minutes per host class (nine suites, sum of medians about 15 minutes plus cold compiles), about 1.5 host-hours in total. The request must also name the fast-tier scenarios.

## Limits

- Medians include whatever load the hosts had (the heavy lock serialises Go suites per host, not other work). The MacBook row of kogen-shaping has 4 runs and kogen-executor 3.
- Packaging and build savings use the recorded `setup` and `build` step medians as the unit cost, which is an upper estimate for packaging (the setup step also runs dependency installs).
- The 2-core Linux server and the Mac Studio are reported for context; the verdict uses the MacBook and the 4-core-class Linux server only.

## Rerun

Offline, from the published data, no model call:

```
python3 -I report.py data
```

It recomputes `data/l4.json` with `l4_model.py`, prints the table and checks every count against `replay.json`. `extract/heavy_suites.py` and `extract/extract_inputs.py` produced `data/` from the heavy-lock logs, the adoption records and the land logs; those inputs hold internal run names, so only their extract is shipped. Sources are public: https://github.com/KogenAI/kogen, https://github.com/KogenAI/kogen-build and the other kogen-* repositories at the main snapshots in `data/static_counts.json`.
