# loop-workspace-snapshot-166ec7f-eu

Can kogen-loop skip the requests it spends looking around a small repository before its first edit, by handing the model the repository listing and its small files up front? **Yes, in this screen. On 14 tasks over two runs each, requests that only list, search or read before the first edit fell 64% (66 to 24 over 27 complete pairs), and to 0 on all 22 runs of the 11 small tasks. All requests fell 28% (170 to 122). No pair changed its hidden result. Where the snapshot was sent, input tokens fell 22% and output tokens 11%.** It is a screen (27 complete pairs; one pair lost to a provider error on the unchanged side), not a confirmation.

Setup:
- **Arm `base`:** standalone kogen-loop `166ec7f` plus `patches/bcw.diff`, the bounded shell wait from [loop-bounded-shell-wait-166ec7f-eu2](../loop-bounded-shell-wait-166ec7f-eu2/README.md), which is going into the loop. Built binary sha256 `222bcdf817090389df3057a1a58238d37215b37729c36e3489d968ba58a64238`.
- **Arm `wmap`:** the same plus `patches/wmap.diff` (binary `e6ed9a28d75f3c69098787496dc62e261ed3aee84507558f3cc91899cbbe95a6`).
- Both arms carry the two lane-only patches of the earlier loop rounds (`patches/api-replay.diff`, `patches/overlap3-nohook.diff`).

The patch changes only the first request of a session. After the unchanged task text, it adds a second user message with:
- a one-line header;
- exactly what `list_files` returns;
- for every listed file of up to 4096 bytes, exactly what `read_file` returns.

Larger, binary or unreadable files are listed only. If the listing has more than 64 paths, or the listing and shown files together exceed 32,768 bytes, nothing is added and the session opens as before. There is no option. Reads go through the loop's own root containment. A FIFO or special file is never read, and the snapshot is taken once per session, so a retried first round sees the same view.

Tasks: the 14 Go tasks of [loop-fixes-9e90bf5-vs-pin-1a3eb18-eu2](../loop-fixes-9e90bf5-vs-pin-1a3eb18-eu2/README.md), two runs each, gpt-6.1-terra at high effort. The two runs of a (task, run) pair ran side by side on one 2-core server, and the starting arm alternated by pair.

## Why this lever, and why it is not an earlier refuted map

Before any run, the earlier loop round's own logs showed 38 of 222 requests on these tasks were look-around-only before the first edit. They came in two shapes:
- **11 small tasks** (14 to 17 files): the model lists the folder, then reads nearly every file in one batch, then edits. The snapshot replaces exactly those two requests. With the 4096-byte cap it shows about what the model read anyway (for example 5.3 KB shown against 5.0 KB read). The only files it leaves out are the two the model never opened: a 37 KB `package-lock.json` and a 7 KB test runner.
- **3 large repositories** (1,100 to 5,300 files): the model searches and reads parts of files. The patch does nothing there.

Two earlier findings refuted repository maps: the [static repository map in the first request](../../categories/mechanism-profiles.md#static-repository-map-in-the-first-request-no) (e1-static-repo-map) and the request-retrieval map (idea-f-request-retrieval). Those maps tried to predict which files of a large task would change, covering 54-57% against a 70% gate, and added input. This lever predicts nothing, so it does not revive them. It leaves large repositories alone, and on small ones it sends what the model would read anyway.

## Registered rules and results

Registered before any run, over the 27 complete pairs. The snapshot was sent on the 11 small tasks:

| Readout | `base` | `wmap` | Rule and result |
| --- | ---: | ---: | --- |
| Look-around-only requests before the first edit | 66 | 24 | -64% (drop if under 50%): met |
| (11 small tasks, 22 pairs) | 44 | 0 | every `wmap` run edited in its first request |
| (3 large repositories, 5 pairs, no snapshot) | 22 | 24 | unchanged, as expected |
| All requests | 170 | 122 | -28%, fewer in 23 of 28 pairs (the 4 higher pairs are all large repositories) |
| Hidden pass | 25 of 27 | 25 of 27 | no pair differs (drop if worse): held |
| Input tokens where the snapshot was sent | 442,201 | 344,488 | -22% (drop if higher): held |
| Output tokens where the snapshot was sent | 51,759 | 46,102 | -11% (drop if higher): held |

Also measured:
- **Agent wall:** 2,254 s vs 1,875 s (-17%). The large repositories, where nothing changed, also show -16%, so wall on this shared 2-core server is noisy and is not claimed.
- **List-price cost:** $1.47 vs $1.30.

**The patch fired where it should.** On all 22 small-task `wmap` runs the first request carried 1.6k to 5.2k more input tokens, and none of them listed or read files before editing. On the large repositories the first request was byte-for-byte the same size in both arms.

**Lost pair.** `kogen-review-on-demand` run 1 is left out. Its `base` run ended when the provider answered HTTP 429 ("client disconnected before delivery") three times. That is provider-side, on the unchanged arm, and as registered there is no replacement. Counting it, look-around requests are 72 vs 28 (-61%) and both arms still pass the same pairs. `kogen-review-retry` fails in every run of both arms, as in every earlier loop round on that task (task-side: its acceptance command needs runner variables the standalone sandbox leaves empty).

## Route, tests

- **Route:** this server holds no OpenAI API login, and logins may not be copied to bench servers. The round's gateway sent every request to the Responses endpoint with the ChatGPT seat login already on the server, read only by the gateway outside the agent's sandbox. Every response reported gpt-6.1-terra at high effort. Absolute numbers are not comparable with API-key rounds; both arms share the route.
- **Loop tests, on Linux in the round itself before any run:**
  - the patches apply cleanly; `gofmt` and `go vet` are clean;
  - the new tests pass, as do `go test ./loop ./tools ./api` on the `wmap` tree.
  - New tests cover: the snapshot equals the tools' own output, including empty files and names Git quotes; binary, oversized, ignored, outside-symlink and FIFO files are not shown; the size and path limits; no snapshot without both tools or outside a repository; the snapshot as the second opening message only; a retried first round keeps the same snapshot.
- **Review:** an independent code review by a different model asked for five fixes (bounded reads, exact empty output, counting the numbered output, quoted names, a stable retry). All were made before the runs, and its re-check passed.

## Limits

- **A screen, not a confirmation:** 14 tasks, two runs each, one pair lost.
- **Small repositories only.** It acts only on repositories with at most 64 listed files and 32 KiB shown. Here those are the 11 small tasks; on large repositories, where look-around is targeted search, it does nothing.
- **Snapshot cost.** The snapshot stays in the conversation (and in any condensed history) for the whole session, so a task with many requests pays for it on each one. Here that was cheaper than the reads it replaced.
- **Standalone kogen-loop sessions only.** Kogen's builder builds its own first request and does not use this path, so this result says nothing about Kogen. A Kogen-level version would need its own screen.

The raw per-run files stay in the private round directory. `runs.csv`, `analysis.json` and `registered.json` hold every number used here.

## Rerun

```
python3 reproduce/loop-workspace-snapshot-166ec7f-eu/summarize.py reproduce/loop-workspace-snapshot-166ec7f-eu/runs.csv
```

`summarize.py` rebuilds the per-pair table and the registered totals above from `runs.csv` (expected output in `expected-output.txt`). `analyze_wmap.py <round dir> <out dir>` rebuilds `runs.csv` (as `cells.csv`) and `analysis.json` from the round directory. It reads each run's `events.jsonl` (a response and the tool calls that follow it) and `tool-items.jsonl` (the call arguments).

To repeat the runs:
1. Take kogen-loop `166ec7f` and apply `patches/api-replay.diff`, `patches/overlap3-nohook.diff` and `patches/bcw.diff` (arm `base`). Additionally apply `patches/wmap.diff` with `patch -p1` (arm `wmap`). Checksums are in `patches/SHA256SUMS`.
2. Run the 14 tasks in `tasks.txt` twice per arm with gpt-6.1-terra at high effort, both arms of a pair at the same time.
