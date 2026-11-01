# b1-base-qualification-go-eu2

Kogen's newer build (commit 6a65bf3e, the base that carries the delivered stream-timing, shell-hang, invalid-UTF-8 shell output, Retry-After, request-budget, clock-wait and review-resume fixes, with the Loop library re-pinned to 1a3eb18) did not do worse than the previous build (3e759e88) on 13 Go tasks. **Hidden checks passed on 9 of 13 tasks with the newer build and 8 of 13 with the previous one**: two tasks gained, one lost, net +1, which is inside the run-to-run noise of this setup. Verdict: **unresolved** as a performance claim; the newer build is adopted as the baseline for later experiments because no regression beyond noise was shown. Finished 1 November 2026.

## What was run

Two release builds of Kogen on one Hetzner Linux host, one trial per task per arm, cells interleaved, no patch in either arm, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, the same 13 Go tasks for both arms. The runs on this host were not overlapped, so wall times are comparable.

| Arm | Kogen commit | Loop library pin | Linux release sha256 |
| --- | --- | --- | --- |
| b0 | 3e759e88 | 8a2fcdae | 265272a6659e26c636eb177acec1acdc472f25345877da874072a80e12c2e392 |
| b1 | 6a65bf3e | 1a3eb18f | 94fcd65f8b203bcd604c62c4e8cb2f4d87c0a6cd4ce77f66db381c592c9ba1b4 |

The two builds differ in many code paths (142 files, about 9,700 lines added; 89 of the files under `cli/`), by design: this run measures the delivered fixes together, so it cannot say which one changed a result.

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 8/13 | 3769 | 4251084 | 219 |
| b1 | 9/13 | 3652 | 5679995 | 248 |

Wall, tokens and requests are summed per cell and **include cells that ended build_blocked, review_blocked or unavailable**. Pairs that differ on the hidden result: G04 and G12 fail on the previous build (G04 review_blocked, G12 build_blocked) and pass on the newer; G02 passes on the previous build and fails on the newer (landed, two hidden checks about invalid operators and syntax-error ordering failed). Outcomes: previous build landed 9, build_blocked 1, review_blocked 2, unavailable 1; newer build landed 11, build_blocked 1, review_blocked 1.

The extra tokens and requests of the newer build come mostly from one task: G08 used 45 requests and about 2.6 million input tokens against 25 requests and 1.3 million for the previous build, and both ended review_blocked. Without that task the request counts are 203 and 194. Wall time of that task rose from 559 s to 775 s.

## Limits

- One trial per task per arm on one host; the previous build alone flips on about 18 to 27 percent of tasks between identical repeated runs on this host, so three flips are not a difference.
- Hidden-check results only; intent validity and acceptance separation are not scored. The model has no listed price, so cost is token counts (input plus output as recorded per cell).
- Tasks are named G01 to G13 in the order of the experiment; names and hidden suites are not included.

## Reproduce the numbers

```sh
python3 -I reproduce/b1-base-qualification-go-eu2/report.py reproduce/b1-base-qualification-go-eu2/data b1-base-qualification-go-eu2 b1 | diff - reproduce/b1-base-qualification-go-eu2/expected-output.txt
```

`report.py` uses only the standard library. `data/b1-base-qualification-go-eu2_cells.tsv` has one row per cell.

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen release builds of commit 3e759e88 and commit 6a65bf3e (no patch in either), the same 13 Go tasks, and a ChatGPT login.
