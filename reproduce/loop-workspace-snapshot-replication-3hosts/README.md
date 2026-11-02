# loop-workspace-snapshot-replication-3hosts

Does the [workspace snapshot screen](../loop-workspace-snapshot-166ec7f-eu/README.md) hold on two more hosts? **Yes on orientation, requests and hidden pass, and yes pooled on tokens; the Studio alone misses one rule by a hair.** Over 79 scored pairs on three hosts, requests that only list, search or read before the first edit fell 66.8% (190 to 63), and to 0 on all 65 runs of the 11 small tasks that got the snapshot. All requests fell 26% (599 to 444). Hidden pass was 74 of 79 on both arms, with no pair differing. Where the snapshot was sent, input tokens fell 11.8% and output tokens 6.2%. The named kogen-loop bundle (bounded shell wait plus this snapshot) stands.

Setup is the one of the first screen, repeated unchanged on two more hosts: standalone kogen-loop `166ec7f` plus `bcw.diff` (arm `base`), and the same plus `wmap.diff` (arm `wmap`), both with the lane-only `api-replay.diff` and `overlap3-nohook.diff`; the four patches are the ones published in [the first screen's pack](../loop-workspace-snapshot-166ec7f-eu/patches/SHA256SUMS), and are not copied here. 14 Go tasks (`tasks.txt`), two runs each, gpt-6.1-terra at high effort, the two runs of a pair side by side, starting arm alternating by pair. What the patch does is described in the first screen's README.

| Host | Pairs scored of 56 cells assigned | Notes |
| --- | ---: | --- |
| EU (Linux, bubblewrap) | 27 of 28 | the first screen; one base run ended on a provider error (HTTP 429), pair left out as registered |
| Laptop (Linux, 4 cores) | 28 of 28 | same sandbox and route as EU; not a timing host |
| Studio (macOS arm64, `sandbox-exec`) | 24 of 28 | stopped at its 3 h cap after one run took the full 3600 s deadline and the shared Studio had no free slot for 75 minutes; rep 2 of `csvq-go`, `task-tags-go`, `kogen-review-on-demand` and `kogen-review-retry` were not run, no replacement |

Not scored: 1 EU pair (provider error) and the 4 Studio pairs above, 5 of 84 assigned. Every other assigned pair is in `pairs.csv`. All three hosts used the ChatGPT seat login already present on that host; nothing was copied.

## Registered rules, per host and pooled

The three-host pooling rule was registered before the laptop and Studio runs started: simple sum of paired blocks with the same rules on the sums; host as a stratum; if one host says drop and another does not, the pooled number does not override and the result is a bounded confirmation, unless the disagreeing host's failure has a class (b-e) cause. Wall is never pooled. Rules per host: drop if look-around requests before the first edit fall under 50%; drop if hidden pass gets worse; drop if input or output tokens rise where the snapshot fires. The snapshot fired on the same 11 small tasks on all three hosts (first-request input larger by 1.6k to 5.2k tokens in every one of those runs, byte-identical on the 3 large repositories).

| Readout | EU (27 pairs) | Laptop (28) | Studio (24) | Pooled (79) |
| --- | ---: | ---: | ---: | ---: |
| Look-around requests before first edit, base to wmap | 66 to 24 (-64%) | 70 to 26 (-63%) | 54 to 13 (-76%) | 190 to 63 (-67%) |
| ...on the 11 small tasks | 44 to 0 | 43 to 0 | 39 to 0 | 126 to 0 |
| ...on the 3 large repositories (no snapshot) | 22 to 24 | 27 to 26 | 15 to 13 | 64 to 63 |
| All requests | 170 to 122 (-28%) | 200 to 140 (-30%) | 229 to 182 (-21%) | 599 to 444 (-26%) |
| Pairs with fewer / equal / more requests | 23 / 1 / 3 | 25 / 1 / 2 | 19 / 2 / 3 | 67 / 4 / 8 |
| Hidden pass, base / wmap | 25 / 25 | 26 / 26 | 23 / 23 | 74 / 74 of 79 |
| Pairs whose hidden result differs | 0 | 0 | 0 | 0 |
| Input tokens where the snapshot was sent | 442,201 to 344,488 (-22.1%) | 445,993 to 331,413 (-25.7%) | 849,231 to 856,920 (**+0.9%**) | 1,737,425 to 1,532,821 (-11.8%) |
| Output tokens where the snapshot was sent | 51,759 to 46,102 (-10.9%) | 50,367 to 47,220 (-6.2%) | 53,868 to 53,029 (-1.6%) | 155,994 to 146,351 (-6.2%) |
| List-price cost, all tasks (USD) | 1.47 to 1.30 | 1.82 to 1.50 | 1.55 to 1.34 | 4.84 to 4.15 |
| Rules met (orientation, pass, input, output) | all four | all four | three of four: input up 0.9% | all four |

`kogen-review-retry` fails in every run of both arms on all three hosts (its acceptance command needs runner variables the standalone sandbox leaves empty), so it is a common failure, not a difference. On the Studio its first `base` run ran to the 3600 s deadline and is scored as a fail, as is its `wmap` partner. Agent wall (not pooled; EU 2,254 s to 1,875 s, laptop 2,830 s to 2,316 s, Studio 5,346 s to 1,724 s, the last dominated by that one timeout) decides nothing.

## What decides the disposition

The Studio alone breaks the registered input rule: 7.7k tokens more (+0.9%) over 21 pairs on the 11 firing tasks. The registered rule says a host that says drop does not let the pooled number override it: the result is a bounded confirmation, unless that host's miss has a class (b-e) cause, that is, a cause outside the patched stage. The arithmetic, from the per-run files:

- **Per pair the sign is a coin flip.** Of the 21 Studio pairs, 12 used more input with the snapshot and 9 less (EU: 5 of 22 more; laptop: 2 of 22). Two pairs, `jobq-go` run 2 (+32.1k) and `argvsplit-go` run 2 (+15.7k), add +47.8k; the other 19 pairs sum to -40.1k.
- **The extra input is spent after the first edit, not on look-around.** The snapshot removed what it was meant to: look-around requests on firing tasks went 39 to 0 and requests went 169 to 120. But on the Studio every run, in both arms, spends several more rounds after its first edit than on Linux: 6.05 per run in `base` and 5.67 in `wmap`, against 2.4 to 3.1 on EU and the laptop. All 48 Studio runs (24 per arm) contain commands setting `TMPDIR` and `GOTMPDIR` (verify-and-retry rounds, such as `mkdir -p .cache/tmp && export TMPDIR=... && make`, then `env | grep -E 'TMP|GO'`, then the same again) that the macOS `sandbox-exec` host needs and the Linux sandbox does not: 0 of 112 Linux runs contain them. Each such round carries the whole conversation, snapshot included, so a host that adds about 3 rounds per run to both arms pays the snapshot's 3k first-request prefix on each and loses the saving from the two look-around requests.
- **So it is a host and verify-stage cause (class b-e), not the patched stage.** The patched stage (opening request, look-around) behaved identically on all hosts. This reading is model-free (request classes and command text from `events.jsonl` and `tool-items.jsonl`); it explains why the Studio's input is flat rather than lower, it does not show the snapshot saves input on the Studio. On the pooled sums it saves 11.8%.

**Disposition: named kogen-loop bundle** (joins the bounded shell wait), unchanged from the first screen. Pooled sums meet all four rules; the two Linux hosts meet all four; the Studio's one miss is attributed to its host rounds under the registered exception. If a reader counts the Studio's +0.9% as caused by the patched stage, the same rule would give a bounded confirmation of 2 more repetitions on one host, not a drop. Pass is untouched on all three.

## Limits

- Three hosts, but one task set and one model route: still 14 tasks. The hidden-pass guard has no power on its own (5 of 79 pairs fail, all the same task); it shows no sign of harm.
- Studio is partial (24 of 28 pairs), runs under `sandbox-exec` rather than a namespace sandbox, and shared the host with other work.
- The snapshot stays in the conversation for the whole session. On a host or task that needs many rounds after the first edit, it is paid on each of them (here: Studio input flat).
- Standalone kogen-loop sessions only. Kogen's builder builds its own first request and does not use this path.

## Rerun

```
python3 -I reproduce/loop-workspace-snapshot-replication-3hosts/pool_wmap.py /tmp/wmap-pool-out eu=reproduce/loop-workspace-snapshot-replication-3hosts/runs-eu.csv lm=reproduce/loop-workspace-snapshot-replication-3hosts/runs-laptop.csv st=reproduce/loop-workspace-snapshot-replication-3hosts/runs-studio.csv
```

This rebuilds `analysis.json` and `pairs.csv` from the per-run files `runs-eu.csv`, `runs-laptop.csv` and `runs-studio.csv`, and prints the per-host and pooled lines in `expected-output.txt`. `analyze_wmap.py <round dir> <out dir>` rebuilds a `runs-*.csv` from a round directory (`events.jsonl` and `tool-items.jsonl` per run). `registered.json` has the rules.

To repeat the runs: take kogen-loop `166ec7f`, apply `reproduce/loop-workspace-snapshot-166ec7f-eu/patches/api-replay.diff`, `overlap3-nohook.diff` and `bcw.diff` (arm `base`), and additionally `wmap.diff` with `patch -p1` (arm `wmap`); checksums in `reproduce/loop-workspace-snapshot-166ec7f-eu/patches/SHA256SUMS`. Run the 14 tasks in `tasks.txt` twice per arm with gpt-6.1-terra at high effort, both arms of a pair at the same time.
