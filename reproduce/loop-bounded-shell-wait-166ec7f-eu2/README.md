# loop-bounded-shell-wait-166ec7f-eu2

Does kogen-loop save model requests if a new shell command waits up to 45 seconds to finish before it hands back a handle? **Yes, in this screen: on the two hard Kogen review tasks, requests that only fetch a shell result fell from 16 to 0, all requests fell 30% (70 to 49, fewer in 5 of 5 complete pairs), and wall time fell 24% (792 s to 604 s). No pair changed its hidden result.** It is a screen (6 paired runs, one of them lost to a provider error on the unpatched side), on two tasks. It is not a confirmation.

Setup: arm `main` = standalone kogen-loop main `166ec7f` (sha256 of the built binary `6c55ea46246e703e6972ff345e17240ef53cd4ff1afa41f5a755d48a0e7ca7cb`). Arm `bcw` = the same plus `patches/bcw.diff` (`67cb0e5eef413c274ff097988d5338be4ce1b112b49e87200e0f467583b079ef`). Both get the same two lane-only patches as the earlier loop rounds (`patches/api-replay.diff`, `patches/overlap3-nohook.diff`). The patch changes one bound: a new shell command now waits up to 45 s for completion instead of 1 s. A command that finishes in time returns its exit status and output in the same tool response. A longer one returns a handle as before, and fetching a handle still waits up to 30 s. Cancellation and the round deadline still end the wait at once and stop the command; waiting never kills a command. The model-facing shell description says "A new command waits up to 45 seconds". Tasks: `kogen-review-on-demand` and `kogen-review-retry` (the hard-kit set of [l3-stop-at-green-hard-kits](../l3-stop-at-green-hard-kits/README.md)), 3 repetitions. Model gpt-6.1-terra at high effort, as in that round. The two runs of a (task, repetition) ran side by side on one 4-core server (eu2), and the starting arm alternated by block. 45 s was picked before the runs from the measured command times: it covers 83% of the commands that yielded a handle on loop main in the earlier round (45 of 54) and 94% of the longer commands timed exactly on these tasks; the tasks' test and acceptance runs take 38–41 s.

| Registered readout (5 complete pairs) | `main` | `bcw` | Result |
| --- | ---: | ---: | --- |
| Requests that only fetch a shell result | 16 | 0 | -100% (rule: fall by at least 50%, at most 1 of 6 pairs higher): met, 0 of 6 higher |
| Requests | 70 | 49 | -30%, fewer in 5 of 5 pairs (rule: pooled fall and at least 4 lower): met |
| Pair passing on `main` and failing on `bcw` | | 0 | guard held: on-demand 3/3 both, review-retry 0/3 both |
| Agent wall | 792 s | 604 s | -24% (guard: not above +15%): held |

Also measured (descriptive, same 5 pairs): output tokens 15,213 vs 12,928 (-15%), list-price cost $1.10 vs $0.86 (-22%), shell commands 44 vs 30, handles issued 15 vs 0, handle fetches 21 vs 0. In the `bcw` runs every shell command (41 of 41) returned in its own response. 18 of them took longer than 30 s (upper bound: the next request's start) and none needed a handle, so the patch did what it was built to do (`lever_fires.py`, `expected-lever-fires.txt`). One `main` run ended with a yielded command it never fetched; no `bcw` run did.

## The pairs

| Pair | Fetch-only requests | Requests | Wall s | Hidden pass |
| --- | --- | --- | --- | --- |
| on-demand r1 | 4 → 0 | 16 → 11 | 167 → 124 | pass / pass |
| on-demand r2 | 4 → 0 | 21 → 14 | 207 → 186 | pass / pass |
| on-demand r3 | 1 → 0 | 14 → 9 | 125 → 119 | pass / pass |
| review-retry r1 | 2 → 0 | 7 → 6 | 72 → 72 | fail / fail |
| review-retry r2 | 5 → 0 | 12 → 9 | 220 → 102 | fail / fail |
| review-retry r3 | 0 → 0 | 7 → 8 | 779 → 101 | fail / fail (censored) |

No pair differs in the hidden result, so there is nothing to attribute. `kogen-review-retry` fails in every run of both arms with the same 7 of 649 expected results, as in every earlier loop round on this task: its acceptance command needs runner variables that are empty in the standalone sandbox. So it can show request and wall changes but not a lost pass. Only the 3 on-demand pairs could show one, and they pass 3 of 3 on both sides.

The review-retry r3 pair is censored. On the `main` side, request 7's provider stream stopped after it had started, with no final response. The round's gateway then refused that run's further requests (its identity and usage gate: "returned effort mismatch" on a response with no final record), and the run ended as an agent error after 779 s. That is a provider-side failure on the unpatched arm. As registered there is no replacement, so the pair stays in the table and out of the pooled readouts. With it included, fetch-only requests are still 16 vs 0 and requests 77 vs 57.

## Route, grader, tests

- Route: this server holds no OpenAI API login, and logins may not be copied to bench servers. The round's gateway therefore sent every request to the same Responses endpoint with the ChatGPT seat login already on the server, read only by the gateway outside the agents' sandbox (the sandbox check confirms the agent cannot read it). Every response reported gpt-6.1-terra at high effort. Absolute numbers are not comparable with the l3 round, which used an API key; both arms here share the route.
- Grader: cells were graded by the grader copy the earlier loop rounds used. All 12 final trees were regraded model-free with the clean published lanes tree `7bf6990c` (`regrade.py`, `regrade-7bf6990c.json`). All 12 results and test counts are identical (on-demand 298 of 298, review-retry 642 of 649).
- Loop tests: on `166ec7f` + `bcw.diff` alone, `gofmt`, `go vet ./...` and `go build` are clean, and `go test ./...` passes except one CLI conformance test (`TestShellLifecycleDeadlineStartup/cli`). That test expects a 1 s yield before a 2 s round deadline; with the 45 s wait the deadline ends the wait instead, so it sees one request, not two. Its lifecycle checks (deadline error, shell and a signal-resistant child stopped) pass. The acceptance steps of the earlier polling fix (`l_shell_poll_cost.js`, parts of `l_shell_hang.js`) also encode the 1 s yield and would need restating. With the lane patches, both arms fail the same lane-patch tests. The patch adds tests for a completed result in the same response, the 45 s bound itself, cancellation and deadline during the wait, and a background child of a completed command being stopped when the round returns.

## Limits

Two tasks, three repetitions, one pair censored: a screen, not a confirmation. Only the on-demand task could show a lost pass. The wall gain comes partly from fewer model requests and partly from the review-retry r2 pair; wall on one server with both arms side by side is comparable, but n is small. Within one model response, a shell call now holds later calls of that response for up to 45 s; no run here showed a cost from that. The patch changes the model-facing tool description, so Kogen, which ships this loop, should be checked at its own level before delivery. The raw per-run files stay in the private round directory; `runs.csv` and `analysis.json` hold every number used here.

## Rerun

```
python3 reproduce/loop-bounded-shell-wait-166ec7f-eu2/summarize.py reproduce/loop-bounded-shell-wait-166ec7f-eu2/runs.csv
```

`summarize.py` rebuilds the tables above from `runs.csv` (expected output in `expected-output.txt`). `analyze_bcw.py <round dir> <out dir>` rebuilds `runs.csv` and `analysis.json` from the round directory. `lever_fires.py <round dir>` gives the per-arm command counts (`expected-lever-fires.txt`). `durations.py <rounds root> <out.csv>` gives the command-time table behind the 45 s choice. `regrade.py` regrades the final trees with the clean lanes tree. To repeat the runs: take kogen-loop `166ec7f`, build it with `patches/api-replay.diff` and `patches/overlap3-nohook.diff` (arm `main`) and additionally `patches/bcw.diff` (arm `bcw`); checksums are in `patches/SHA256SUMS`. Then run the two tasks three times per arm with gpt-6.1-terra at high effort, both arms of a repetition at the same time.
