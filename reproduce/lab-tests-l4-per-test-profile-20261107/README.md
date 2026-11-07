# Six of nine Kogen test suites exceed their proposed time budgets on a quiet 4-core host; a few waiting tests cause most of it

Finding `lab-tests-l4-per-test-profile-20261107`. A model-free Lab (no model call), step 1 of Lab L4 of the K-TESTS-ACCEPTANCE-FIRST request. It follows `lab-tests-l4-critical-path-20261105`, which could not price the budgets because no per-test durations had been recorded.

## Question

For each Kogen repository, on a quiet 4-core Linux host with a cold test cache: how long does the suite take, how is the time spread over tests, and how parallel is it? Budgets proposed by the request: kogen 60 s, kogen-build 60 s, kogen-shaping 45 s, kogen-loop 10 s, every other component 20 s.

## Method

One exclusive host lock, nothing else running. For each repo: shallow clone of the default branch, a fresh Go build and module cache, `go test -json -count=1 ./...` once (kogen from its `cli/` module, where its `go.mod` lives). From the JSON events: longest package wall, per-test seconds, tests over 1 s and over 5 s, the slowest 20 tests, the sum of package walls over the longest (a parallelism ratio) and failed tests. Package wall = the longest package, because packages run in parallel.

## Result (`data/summary.json` has every number)

| Repo | longest package (s) | budget (s) | tests | over 5 s | slowest test (s) | failed |
|---|---|---|---|---|---|---|
| kogen | 210.5 | 60 | 370 | 10 | 131.2 | 0 |
| kogen-build | 87.6 | 60 | 1209 | 9 | 61.9 | 0 |
| kogen-coordinator | 36.4 | 20 | 841 | 1 | 10.0 | 0 |
| kogen-loop | 19.3 | 10 | 1853 | 9 | 7.1 | 0 |
| kogen-executor | 25.3 | 20 | 593 | 1 | 6.2 | 0 |
| kogen-setup | 22.5 | 20 | 689 | 0 | 4.2 | 0 |
| kogen-review | 2.6 | 20 | 269 | 0 | 0.6 | 0 |
| kogen-shaping | 34.7 | 45 | 758 | 4 | 15.2 | 85 |
| kogen-verification | 63.8 | 20 | 558 | 0 | 3.8 | 2 |

- Six repos pass every test and exceed their budget: kogen, kogen-build, kogen-coordinator, kogen-loop, kogen-executor and kogen-setup (marginally). kogen-review is within budget.
- The waiting tests are few. In kogen two approve-deadline tests take 131 s and 121 s and a packaging-isolation test 38 s; in kogen-build two lineup-review tests take 62 s each and one retry test 41 s; in kogen-coordinator one fallback test takes 10 s. Moving a test out of the fast tier lowers the wall only if no other package is as long: the previous step found these tests already run in parallel, so each repo's wall is set by its longest package, which these tests dominate in kogen (210.5 s) and kogen-build (87.6 s).
- kogen-loop is bounded by parallelism: its package walls sum to 55 s (ratio 2.9) yet the longest package is 19 s, over the 10 s budget with no test over 7.1 s.
- kogen-shaping and kogen-verification are not judgeable: their failures here come from missing test tooling (the real Cucumber is not installed in a fresh clone; the tests stop with "run npm ci ... or set the Cucumber path"), so their walls are not clean. A clean clone of those two repos does not pass without that extra step.

## Verdict

unresolved: six of nine repos are above budget with the cause named per repo; two repos need a rerun with the test tooling installed before they can be judged.

## Rerun

1. On a quiet 4-core Linux host with Go installed, run `scripts/run.sh <empty output dir>` (clones the repos at their default branch heads; the heads at this run are in `replay.json` inputs).
2. Run `python3 -I scripts/profile.py <output dir>/json > summary.json` and compare with `data/summary.json`. Wall times vary with the host; the ranking of slowest tests and the pass/fail counts should match.
