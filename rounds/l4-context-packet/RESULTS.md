# L4 deterministic context packet results

STATUS: **DESCRIPTIVE** (see the round README: post-result amendment, non-interleaved controls)

The primary comparison follows Amendment 1: packet and contemporaneous no-packet controls are paired by variant and seed. Each cell is the latest official aggregate grade row for its exact cell ID, from the MacBook grading route.

## Paired outcomes

| Source variant | Seed | Packet cell | No-packet control | Pair |
| --- | ---: | --- | --- | --- |
| `r70-2-go` | 1 | PASS 25/25 | PASS 25/25 | both pass |
| `r70-2-go` | 2 | PASS 25/25 | FAIL 21/25 | rescue |
| `r70-2-go` | 3 | PASS 25/25 | PASS 25/25 | both pass |
| `r70-2-elixir` | 1 | PASS 25/25 | FAIL 21/25 | rescue |
| `r70-2-elixir` | 2 | PASS 25/25 | FAIL 21/25 | rescue |
| `r70-2-elixir` | 3 | PASS 25/25 | PASS 25/25 | both pass |
| `r70-4-elixir-fe2` | 1 | FAIL 17/18 | FAIL 17/18 | both fail |
| `r70-4-elixir-fe2` | 2 | FAIL 17/18 | FAIL 17/18 | both fail |
| `r70-4-elixir-fe2` | 3 | FAIL 17/18 | FAIL 17/18 | both fail |
| `r70-7-rust` | 1 | PASS 24/24 | FAIL 23/24 | rescue |
| `r70-7-rust` | 2 | PASS 24/24 | FAIL 23/24 | rescue |
| `r70-7-rust` | 3 | PASS 24/24 | FAIL 23/24 | rescue |

## Pass counts, test counts, and tokens

A full pass is an official `pass` outcome. Mean `tests_passed` is the arithmetic mean across the three cells in that variant and arm. One cell's total tokens are uncached input + cached input + output; total is the sum. Tokens per pass is all tokens consumed by every cell in that arm divided by its full-pass count, so failed-cell tokens remain in the numerator.

| Source variant | Arm | Successful cells | Mean tests_passed | Total tokens | Tokens per successful cell |
| --- | --- | ---: | ---: | ---: | ---: |
| `r70-2-go` | packet | 3/3 | 25.00 | 1,922,619 | 640,873 |
| `r70-2-go` | control | 2/3 | 23.67 | 1,320,610 | 660,305 |
| `r70-2-elixir` | packet | 3/3 | 25.00 | 24,525,211 | 8,175,070.3 |
| `r70-2-elixir` | control | 1/3 | 22.33 | 27,080,262 | 27,080,262 |
| `r70-4-elixir-fe2` | packet | 0/3 | 17.00 | 3,043,793 | — (0 passes) |
| `r70-4-elixir-fe2` | control | 0/3 | 17.00 | 3,256,526 | — (0 passes) |
| `r70-7-rust` | packet | 3/3 | 24.00 | 1,053,801 | 351,267 |
| `r70-7-rust` | control | 0/3 | 23.00 | 928,201 | — (0 passes) |
| All variants | packet | 9/12 | 22.75 | 30,545,424 | 3,393,936 |
| All variants | control | 3/12 | 21.50 | 32,585,599 | 10,861,866.3 |

## Historical baselines (context only)

These are the registered historical Luna-max cells. Amendment 1 makes the contemporaneous paired controls the decision basis; the historical baseline is shown only as context.

| Source variant | Historical successes | Eligible cells |
| --- | ---: | ---: |
| `r70-2-go` | 3/4 | 4 |
| `r70-2-elixir` | 2/4 | 4 |
| `r70-4-elixir-fe2` | 0/5 | 5 |
| `r70-7-rust` | 6/7 | 7 |

## Decision and protocol notes

The net packet-minus-control change is **+6 full passes**. There are **6 paired rescues** and **0 paired losses**. Packet pass counts are no lower than controls on **4/4 variants**. The regression rule did not fire; the worst mean `tests_passed` comparison is 17.00 packet versus 17.00 control on `r70-4-elixir-fe2` (difference 0.00).

**Verdict: KEEP** packets in specification sections 3.2 and 4.9, as a descriptive pilot. The result is based on four outcome-selected variants and three cells per arm per variant; the rule thresholds are coarse and support no general claim.

The EU controls followed the seeded order recorded for the lane. One EU control was launched while a grade-window drain was in progress; this delayed the window only and affected no result. The three US controls ran after their packet cells had finished and were **not interleaved**.

A separate confirmation round, `l4b-confirm`, is running on three new variants; it is not included here.
