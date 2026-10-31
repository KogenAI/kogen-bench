# delivery-path-timing

Where the wall-clock time of Kogen builds and shaping sessions goes, read from logs that were already recorded (no model call, nothing run again). Two large pieces of time are not model time: the **check commands** (startup baseline plus verification) take 36% of build wall time in the benchmark cells and 72% of wall time in 15 real delivery builds, and the **slowest 4% of shaping requests** (those taking 180 s or more) hold 39% of all shaping request time. Review repair, builder prompt growth and builds that start with a failing baseline show little headroom. Verdict: **unresolved** (descriptive; it ranks where a speed-up could matter and decides which candidate changes to test or skip, and it tests no change). Finished 31 October 2026.

## What was measured

4,389 Kogen cells (shaping or build sessions; cells of other agents are excluded) that started between 22 and 31 October 2026, on one Mac desktop, one laptop, two Linux hosts, plus 15 real delivery builds and 15 delivery shapings on a MacBook. They span many Kogen builds, tasks and loads, so they are not one baseline. 1,470 are "real builds": not seeded, with at least one builder request or one external-tool round. Seeded review and verification replay cells (1,311) are reported separately. Delivery builds use an external coding tool as the builder, which Kogen's log does not break into requests, so their builder request time shows as 0%, which means "not logged", not "free".

For every cell the logs give the length of each phase (startup, build, verifying, review, committing; for shaping: setup, preparation, model, probe, readiness), the outcome, and counts such as command runs and review rounds. For the 39,869 model requests they give input, cached and output tokens and the request time. The pack's `data/cells.jsonl.gz` and `data/reqs.jsonl.gz` hold exactly these fields. Host names became a class (`mac-desktop`, `laptop`, `linux-a`, `linux-b`, `macbook-delivery`), task and run names became numbers, and start times were cut to the date. Commands, paths, model names, token counts per account and output text are not included.

## Where the headroom is

Ordered by the wall time that would go away if the item went to zero. These are upper bounds and the items overlap.

| # | Item | Upper bound | What the data shows | Reading |
| --- | --- | --- | --- | --- |
| 1 | **Check commands: startup baseline and verification** | Startup 26.8 h (13%) + verifying 46.0 h (23%) = 36% of the 201.7 h of real-build wall time in the benchmark cells; 72% of wall time in the 15 delivery builds (startup 38% + verifying 34%; medians 2,647 s and 1,345 s) | Of it: a re-run of an unchanged tree's check, counted strictly (no file write and no builder shell call in between), is 12.6 h (6.3% of wall; 9.3% on one Linux host, 4.3% in delivery, 5 of 15 delivery builds, up to 2,378 s in one). Commands that run longer than 300 s: 97 commands in 35 cells = 23.6 h, 15.5 h of it beyond 300 s (Go 10.4 h, test 7.5 h, format 2.1 h). Delivery Go tests of 1,000 to 3,000 s and format of 500 to 1,000 s look like machine contention or cold caches; the logs have no load data, so this is not proven | Largest item. Worth a screen of reusing checks of unchanged trees, and of the long-command tail, after checking contention first. |
| 2 | **Shaping model tail** | 42.2 h (39%) of the 108.3 h of shaping request time sits in 479 requests of 180 s or longer (113, 160, 140 and 66 on the four benchmark hosts; 46, 84, 66 and 29 of them at 300 s or longer) | Shaping model time is 48% to 94% of the shaping session by host. The 90th-percentile shaping request is 142 s on the Mac desktop | A budget screen is worth running only with controls, because these are high-effort reasoning calls: 180 s or more is not a stall by itself. |
| 3 | **Builds that do not land** | 110 builds (7%) hold 30% of real-build wall time, about 60 h. Timeouts alone: 22 builds, 21.5 h. Others: no progress 23, failing checks 29, invalid response 17, context budget 6 | A stop rule only saves the time after the point where it would fire, and a wrong stop loses a success | Stop-early rules apply to the 22 timeout builds. |
| 4 | **Shaping sessions that do not finish `ok`** | 361 sessions (23%) hold 19% of shaping wall time, about 31 h: refused 210, questions pending 124, timeout 16, memory cap 22 | | The lever is task coverage and ambiguity (refused, questions pending), not timing; only the 16 timeouts are a time item. |
| 5 | **Review** | Review phase 29.4 h = 20% of wall, but the **repair part is only 4.9 h (3.3%)**: 445 of 1,208 builds have a review round with findings, and median wall is 190 s with findings against 174 s without | | The cost is the first review pass, not the repair. A speed-up of review has little headroom; a review change has to win on defects caught. |
| 6 | **Prompt growth and caching** | Uncached input tokens: review 117 M, shaping 82 M, build 56 M (of 557 M, 312 M and 655 M input; cached 79%, 74%, 92%). The builder's prompt grows by only **1.4k tokens per round** (90th percentile 2.6k): first request 18.8k, last request 32.4k (medians over 122 cells with four or more rounds; builder rounds median 10, 90th percentile 42) | The builder's prompt is 92% to 97% cached from round 2 on | Little headroom in shortening the builder's history. Unexplored: the reviewer's first request (about 20k tokens, 75% cached) and shaping (74% cached). Only the ten longest builds (48 to 134 rounds, 3 to 5 M input tokens each) show growth that matters. |
| 7 | **Baseline already failing at start** | 4 of 1,470 real builds (0.3%); 29 more in seeded replay cells, by design | | No natural headroom; a mode that tolerates a failing baseline has nothing to act on. |
| 8 | **Very large review (more than 150 parts)** | 0 cells; the largest review had 119 parts (10 cells at 100 or more) | | Trigger absent from existing logs: unmeasured, not disproved. |
| 9 | **Slow provider requests in build and review** | 28 of about 28,000 requests took 180 s or longer (build 8, review 20), 5 took 300 s or longer | | No headroom for build and review; only shaping has a tail (item 2). |

Short reading: the time is in the checks and in shaping, not in the builder's model time, review repair or the builder's prompt growth.

## Delivery builds

Section 5 of `expected-output.txt` lists the 15 real delivery builds with their phase times. Median wall time is 7,054 s (90th percentile 11,654 s). Startup plus verifying is about 72% of wall time, the builder or external tool 25%, review nearly nothing (reviews are mostly absent or stubbed in these runs). Only 3 of 15 landed; 3 ended in a failed commit and 1 in a protocol error, and each still carries its full check time, so failed delivery builds waste check time too. "(none logged)" means the run had no outcome event: still running or interrupted when copied.

## Limits

- Byte counts of tool results are as logged and the log cuts results (mean 150 to 220 bytes per call), so they rank contributors but understate real prompt growth. Request size is logged for only 625 requests. The split of a prompt into system text, history and tool output is not logged. A full request replay would need the stored request bodies.
- The benchmark cells are research runs on warmed caches; delivery builds ran on a loaded MacBook. A difference between host classes is not a hardware effect alone: Kogen version, tasks and load also differ.
- Phase lengths overlap (review runs inside the build phase), so they are not added. On the Mac desktop most builds lack phase times (older Kogen), so its phase shares are unlogged for 90% of wall time and its numbers come from the result file instead.
- The strict repeat count includes Kogen's required re-check of the final candidate, which must stay; it is headroom only where a receipt could prove the tree and environment identical.
- Replay estimates are bounds, not proof that any change would help.

## Reproduce the numbers

```sh
python3 -I reproduce/delivery-path-timing/report.py reproduce/delivery-path-timing/data | diff - reproduce/delivery-path-timing/expected-output.txt
```

`report.py` uses only the Python standard library and prints every table and every number in the sections above (section 1 phase tables, 2 trigger counts, 3 request and prompt tables, 4 headroom arithmetic, 5 delivery builds). To restrict to cells started on or after a date, set `FPH_SINCE=2026-10-29`; the shares keep the same shape and the medians are somewhat higher. The 108.3 h and 42.2 h of shaping request time in item 2 are the sums of shaping requests in `data/reqs.jsonl.gz` (all, and those of 180 s or more).

## Rerun

The tables rerun from the data files in this directory with the command above. The extraction step that produced `data/` reads Kogen's own run logs, which hold task text, commands and output and are kept out of this repository; the data files hold only the extracted numbers.
