# h2h30-sub-route-tokens

On the ChatGPT subscription route, 24 Go tasks, `gpt-6.1-terra` at medium and at high effort, both tools passed 24/24. Loop used about 40% of Codex's equivalent tokens per pass (38.9% at medium, 42.2% at high), and it used fewer on every one of the 24 tasks at both efforts. Its median wall time was 25–30% longer, but this pairing is route-confounded, so the wall result is not a tool comparison. Verdict: **yes** (the token result), 30 October 2026.

## What was measured

One run per task, tool and effort: 24 tasks × 4 tools = 96 runs, all on one Linux host with one run at a time. Within each task the runs alternated: loop medium, Codex medium, loop high, Codex high. Hidden tests graded each final tree. All 96 runs finished, with complete usage records and no infrastructure failures.

Comparisons pair the same model and effort only: loop medium with Codex medium, and loop high with Codex high.

- **Pass:** the hidden suite passed on the final tree (`passed` = 1).
- **Equivalent tokens per pass:** (uncached input + 0.1 × cached input + 4 × output) summed over runs, divided by passes. There are no USD figures because neither tool's usage on this route is priced.
- **Wall:** the whole run, in seconds (`wall_s`); `agent_wall_s` is the agent process alone.
- **Sign tests:** two-sided exact binomial tests over the 24 tasks, ties dropped, one repetition each. They are descriptive only.

**Route confound.** Both tools used the same ChatGPT account, but by different routes. Loop, on its ChatGPT login, calls the public API host with its own OAuth client; Codex calls the ChatGPT Codex backend. During this period loop's measured output rate was lower than Codex's (finding `loop-sub-route-throughput`; see also [loop-sub-route-honest-probe](../loop-sub-route-honest-probe/)). A later same-host test saw both routes at about the same rate (see [`superseding-same-host-test`](../loop-sub-route-throughput/superseding-same-host-test/)), and the cause of the earlier gap was not found, so the earlier rates are not quoted here. The wall gap may therefore mix tool and route and is not a tool comparison. Token counts are much less affected by the route, but they are still not a comparison on the same API key.

## Tasks

24 Go tasks, listed in [tasks.txt](tasks.txt); each task is at `tasks/<task-id>/`.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop (`loop-default`) | kogen-loop commit `b8a4046`, built for linux/amd64 with Go 1.27.3 (binary SHA-256 `20ff81d9d5cc77c1e2aa8dd0008cc6268d9a9a3b358a3aa2efd6836a69ce1238`) | `gpt-6.1-terra` | medium, high | ChatGPT login (public API host, loop's own OAuth client) | none |
| Codex CLI | 0.165.0, x86_64-unknown-linux-musl (binary SHA-256 `b8a11fedf24b2dfb59a70c9e52b030f9a508dcd49cd2dd0d41956f4c785156b8`) | `gpt-6.1-terra` | medium, high | ChatGPT login (ChatGPT Codex backend) | none |

Harness: the bare-agent runner `lanes_bare.py` (SHA-256 `9744637db945c7d897918a970524087586c21e5323394bc8bf0edc417448c99a`), with a deadline of 3,600 s per run and Gherkin intent form.

## Rerun

```sh
python3 lanes/bare/lanes_bare.py batch reproduce/h2h30-sub-route-tokens/batch.json --tasks tasks --run-dir "$RUN" --slots 1
```

[batch.json](batch.json) is the measured specification, with only the home and binary paths made generic: put a loop binary at `~/bin/kogen-loop` with its ChatGPT login under `~/kogen-home`, and Codex 0.165.0 at `~/bin/codex` with its ChatGPT login under `~/codex-home`. You need Linux, Bubblewrap (`bwrap`), Go and a ChatGPT plan; run from the repository root. Then `python3 lanes/bare/lanes_bare.py summary "$RUN"` lists the per-run rows. Route speeds vary with time and account, so wall times will not repeat exactly.

## Reproduce the numbers

```sh
python3 reproduce/h2h30-sub-route-tokens/analyze.py | diff - reproduce/h2h30-sub-route-tokens/expected-output.txt
```

Verified 30 October 2026: this reproduces every published number exactly, including the medians, means, equivalent and uncached tokens per pass, input and output totals, median paired deltas and sign-test counts. Halves are rounded up, as in the published table. The script prints p-values to two significant figures (0.00028, 0.0015, 1.2e-07, 3.6e-05, 0.023); the published text rounds the same values to 0.0003, 0.0015, 1.2e-7, <0.0001 and 0.023.

## Expected outputs

[expected-output.txt](expected-output.txt) contains:

| Effort | Loop eq. tokens/pass | Codex eq. tokens/pass | Loop/Codex | Loop lower on | Wall median loop / Codex | Median paired wall delta | Wall task wins loop/Codex |
| --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| medium | 32,697 | 84,035 | 38.9% | 24/24 tasks (p=1.2e-7) | 81.16 / 66.91 s | +29.5% (+17.4 s) | 3/21 (p=0.0003) |
| high | 40,747 | 96,476 | 42.2% | 24/24 tasks (p=1.2e-7) | 101.37 / 77.79 s | +24.7% (+17.4 s) | 4/20 (p=0.0015) |

Uncached input per pass, loop vs Codex: 15,493 vs 34,826 at medium (loop lower on 22/2 tasks) and 19,849 vs 34,157 at high (18/6). The median per-task equivalent-token delta is −58.7% at medium and −60.2% at high. Mean wall per run: loop 97.8 s vs Codex 78.1 s at medium, and 110.5 s vs 93.3 s at high.

## Cost

There are no dollar figures: both tools ran on a ChatGPT plan, and the usage is not priced. A rerun uses 96 runs of plan quota (about 2.5 hours of summed run wall time at one run at a time; the measured batch took 2 h 47 min).

## Limits

- The routes differ, so this is not a comparison on the same API key, and the wall result says nothing about the tool alone.
- There is one repetition per task, so the sign tests are descriptive only.
- The two tools count `requests` in different units, given in `request_unit`: loop counts logical model requests and Codex counts completed CLI turns.
- One Codex-high run (`r70-7-go`) carries a harness leak flag: one private-path reference appears in its own log. The source report gives 0 leaks for the round. The run passed, and dropping it does not change any direction.
