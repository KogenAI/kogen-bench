# b1-base-qualification-go-pooled

Three repetitions of the newer Kogen build (6a65bf3e) against the previous one (3e759e88) on the same 13 Go tasks, pooled: **hidden checks passed on 28 of 39 task runs with the newer build and 27 of 39 with the previous one**. Three pairs gained, two lost, net +1. Of the five differing pairs, three trace to a defect written while the task was being shaped (on the previous build's side) and two to a request that leaves a case open (on the newer build's side); none is a build or review failure that the logs attribute to either build's own code. Verdict: **unresolved** as a performance claim; there is no regression and no gain beyond noise, and the newer build stays the baseline for later experiments. Finished 1 November 2026.

This is a new publication: it adds two repetitions on a Linux laptop host to the single Hetzner repetition already published as `b1-base-qualification-go-eu2`, and attributes every differing pair by stage. Two more repetitions on the Mac Studio host were still running when this was written and will be published as a separate finding.

## What was run

Two release builds of Kogen, no patch in either arm, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, the same 13 Go tasks, one trial per task per arm, cells interleaved.

| Arm | Kogen commit | Loop library pin | Hosts |
| --- | --- | --- | --- |
| b0 | 3e759e88 | 8a2fcdae | e1: Hetzner Linux host; l1 and l2: Linux laptop host |
| b1 | 6a65bf3e | 1a3eb18f | same cells, same hosts |

The builds differ in many code paths (142 files, about 9,700 lines added), by design: this measures the delivered fixes together. Repetitions e1, l1 and l2 ran on different hosts, so wall times are compared inside a repetition only.

## Result

| Repetition | b0 hidden pass | b1 hidden pass | Pairs that differ (b1 wins, losses) |
| --- | --- | --- | --- |
| e1 (Hetzner) | 8/13 | 9/13 | 3 (2, 1) |
| l1 (laptop) | 9/13 | 9/13 | 2 (1, 1) |
| l2 (laptop) | 10/13 | 10/13 | 0 |
| all | 27/39 | 28/39 | 5 (3, 2) |

Per task over the three repetitions (b0 / b1): G01 3/3, G02 2/0, G03 3/3, G04 2/3, G05 0/0, G06 2/2, G07 3/3, G08 0/0, G09 3/3, G10 2/3, G11 3/3, G12 2/3, G13 2/2. G05 and G08 fail in both arms in every repetition. G02 is the only task where the newer build did worse.

Wall, tokens and requests are summed per cell and **include cells that ended refused, build_blocked, review_blocked or unavailable**. Over all 39 pairs: wall 9751 s (b0) and 11160 s (b1), requests 596 and 698, tokens 9.9 million and 14.7 million. Most of the difference is G08 (the newer build used up to 49 requests and about 1100 s on it, ending review_blocked, where the previous one refused after seven requests). Without G08: wall 9094 s and 9175 s, requests 557 and 597, tokens 8.3 million and 8.9 million.

## Why the five pairs differ (read from the cell logs, no model run)

Classes: (a) the stage a patch changed, (b) shaping or approval, including acceptance written at shaping time, (c) review, (d) infrastructure, (e) unclear or an open request. Because the two builds differ everywhere, class (a) cannot be isolated here; the classes show where each pair came apart.

| Pair | Failing arm | Stage | Class | Cause |
| --- | --- | --- | --- | --- |
| e1 G04 | previous | review | b | Review blocked on a protected acceptance step, written at shaping time, that raised the default step timeout from 5 s to 120 s |
| e1 G12 | previous | build | b | The first acceptance scenario gives plain text where a hex line is required and expects a frame, contradicting the approved odd-length-hex rule |
| e1 G02 | newer | hidden checks | e | Landed after green verification; hidden checks on invalid operators and syntax-error order failed; the Intent encodes one reading of an end-of-input case the request leaves open |
| l1 G10 | previous | shaping | b | Refused: the Intent was not ready, acceptance steps for the layout error messages were undefined |
| l1 G02 | newer | hidden checks | e | Landed; the same syntax-error-order check failed |

Pairs that fail in both arms or stop on the provider (e1 G06, l1 G13) do not change the count. In l2 nothing differs, but G02 on the newer build stopped at build because its acceptance scenario expected byte position 9 for a character that is the eighth byte of its input (checked with a hex dump); the previous build landed that task and failed the same syntax-order hidden check as the newer build did in e1 and l1. So G02 fails on both builds through one shared check, in different ways.

Counted this way: of 5 differing pairs, 3 are class b on the previous build's side, 2 are class e on the newer build's side, 0 are build or review defects of either build.

## Noise

The identical-build repetition on the Hetzner host (previous build against itself) flips 3 of 13 pairs (23%), all class b (published as its own A/A finding). The 5 flips in 37 usable pairs here (14%) are not more than that. At a flip rate of about 20%, a 9-to-1 split of differing pairs (two-sided sign test p about 0.02) needs about 10 differing pairs, so about 50 pairs, or four repetitions, per comparison; three repetitions are enough only to show a large effect.

## Limits

- One trial per task per arm per repetition; two host types; hidden-check results only (intent validity and acceptance separation are not scored). The model has no listed price, so cost is token counts (input plus output as recorded).
- G02 on the newer build failed in all three repetitions; two of them are class e on an open request, but the hidden check was not rerun here, so a newer-build effect on that one task is not excluded.
- Tasks are named G01 to G13 in experiment order; names and hidden suites are not included.

## Reproduce the numbers

```sh
python3 -I reproduce/b1-base-qualification-go-pooled/report.py reproduce/b1-base-qualification-go-pooled/data b1-base-qualification-go-pooled | diff - reproduce/b1-base-qualification-go-pooled/expected-output.txt
```

`report.py` uses only the standard library. `data/b1-base-qualification-go-pooled_cells.tsv` has one row per cell; `data/b1-base-qualification-go-pooled_pairs_attribution.tsv` lists the differing pairs with their cause.

## Rerun

The tables rerun from `data/`. To run the cells again you need Kogen release builds of commit 3e759e88 and commit 6a65bf3e (no patch in either), the same 13 Go tasks, and a ChatGPT login.
