# Slow checks re-run on an unchanged tree: replay of 137 stored Builds

**Finding.** Re-running a slow green check on a tree that has not changed is a real but small cost: in 101 stored Kogen Builds a check of 60 s or more repeated on an identical tree in 12 Builds, for 7,407 s, 2.75% of total Build wall (mean 73 s per Build, 5.3% of the median Build wall; bootstrap 95% interval 2.7-8.7%; the median Build saves nothing). Every repeat is the pass that re-verifies a tree the review had just approved. The fix is already in Kogen: kogen-build [b9990a3](https://github.com/KogenAI/kogen-build/commit/b9990a3d090306d79e28ac0d858ba47c8f3b0ed4) (3 Nov 2026) keeps a per-Build check ledger keyed by check, command, tree and environment and reuses a green result. The queued request for an opt-in Verify reuse would duplicate it, so it is not built. Whether the same reuse across restarted Builds pays is open and cannot be measured from stored logs.

## Question
The request asked for opt-in reuse of a check that was green on an identical tree, command and run identity (checks of 60 s or more, every third reuse re-executes, a red result never reused), and for a wider run identity. Decision rule registered before the replay (Studio Lab lever lab-round-suite-reuse-s0-20261105): build the reuse only if reuse inside one run (U0) or with a green baseline reused across restarts (U1) saves at least 5% of median Build wall over at least 40 Builds.

## Method
Model-free replay; no cell, seat or API key. Corpus: 251 stored run logs of Kogen Builds, 22-31 Oct 2026. 101 raw delivery logs (MacBook 57, Studio 32, laptop 12) carry command, command_result, pass, review and commit events, with the git tree digest on review and commit events; 36 further delivery Builds are rows of a 30 Oct profile without tree digests (used only for the baseline replay); 114 climb-cell logs are Go kits whose longest check is 47 s. A pass counts as the same tree as an earlier pass when its review digest is equal, or when no builder tool call and no fixer ran between the two. U0 counts a check of at least the threshold that exited 0 on an earlier identical tree and counts every third such reuse as a re-execution. U1 reuses a green baseline check when an earlier Build of the same slug started at the same head with the same command. Run identity was not logged by any of these Builds (0 identity events in 251 logs), so the identity-widening part (U2) cannot be measured.

## Results
| replay | Builds | Builds with a hit | seconds saved | share of total wall | mean per Build vs median Build wall |
|---|---|---|---|---|---|
| U0, checks >= 60 s | 101 | 12 | 7,407 | 2.75% | 73 s = 5.3% of 1,376 s |
| U0, >= 120 s | 101 | 12 | 7,280 | 2.71% | 5.2% |
| U0, >= 300 s | 101 | 12 | 6,318 | 2.35% | 4.6% |
| U1, baseline >= 60 s | 137 | 18 | 11,000 | 3.59% | 80 s = 8.4% of 951 s |
| U1, baseline >= 300 s | 137 | 17 | 9,959 | 3.25% | 7.6% |

- All 26 identical-tree consecutive passes are a re-verify of a tree the review had approved. The every-third re-execution never fired in U0.
- In 2 of the 20 U0 reuses the stored re-run was red on a tree that had been green: one Build whose `go test -race` ran 606-609 s and failed at the 10-minute package timeout. Reuse would have reported green there. The shipped ledger has no every-third re-execution.
- U1 uses a surrogate key (slug, start head, command); the logs hold no toolchain or environment identity, and an earlier replay found mixed outcomes in 3 of 133 same-key groups. U1 is not proven.
- Median per-Build saving is 0 s in both replays: 12 of 101 and 18 of 137 Builds benefit.

## What this decides
- U0: already shipped, so the opt-in Verify reuse is not built; the queued row closes as superseded by b9990a3. The shipped ledger records only status-0 executions and keys on the toolchain found on PATH, the variables and the files named in the command.
- U1: open. It needs at least 40 Builds that carry check_reuse and identity events; none are stored, so a new Lab row would first collect them.
- Limits: tree equality is inferred from review digests and from the absence of builder activity; the logs predate run-identity logging and the b9990a3 ledger; the Builds are Kogen's own (Go and Studio Elixir), not AoR task cells.

## Rerun
```
cd reproduce/lab-slow-checks-rerun-s0-20261105
python3 -I report.py data/builds.json data/results.json
```
`data/builds.json` is the reduced table (one record per Build: source, slug, start head, span, outcome, per-pass check names, class, command hash, seconds, exit, tree digest, review verdict and the builder activity between passes). The raw run logs are kept out of the pack. `data/results.json` is the script's output and holds the numbers above, plus the companion slow-check cadence tables.
Source: the code in question is [kogen-build build/checkreuse.go at b9990a3](https://github.com/KogenAI/kogen-build/blob/b9990a3d090306d79e28ac0d858ba47c8f3b0ed4/build/checkreuse.go).
