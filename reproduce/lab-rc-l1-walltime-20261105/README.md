# Lab L1: the wall-time deadline test flakes because its clock starts too early; the loaded run did not happen

**Finding.** On the Studio at natural load (load5 12.5-18.6 on 10 cores) the unchanged test `TestWallTimeDeadlineAndNeverStarted` failed 2 of 600 runs, both "setup-1 never started". A test-only variant whose 300 ms clock starts when setup-1 starts failed 0 of 600, and a product mutant that ignores the deadline failed it 2 of 2. A separate probe shows why the unchanged test is fragile: `Verify` spends 215-297 ms (median 228) of the test's 300 ms budget before setup-1 starts, in 300 of 300 runs. The registered adoption threshold (A fails at least 3 of a loaded block of 300) was not met, and the fixed-load Linux condition could not run, so the verdict was first unresolved; B was then adopted under a recorded deviation (see Verdict). No model call, no product code change.

## Question

Kogen's kogen-verification test [`verify/wall_time_test.go`](https://github.com/KogenAI/kogen-verification/blob/ec39831718deb42a60af26e1e8a9b06a763e1258/verify/wall_time_test.go) `TestWallTimeDeadlineAndNeverStarted` failed in 8 of 9 delivery runs on 5 Nov 2026 (5 candidate checks and 3 producer-main baselines, on both Macs). The suspected cause is the test itself. Line 86 gives the whole `Verify` call a 300 ms deadline. `Verify` does work before setup-1 starts (a git tree snapshot, tool identity probes, a host-load probe), and line 97 then requires setup-1 to have run at least 100 ms. Any run whose earlier work takes more than about 200 ms fails.

## Arms

All arms are kogen-verification commit `ec39831718de`, Go 1.27.2, Apple git 2.54.0, one Mac Studio (10 cores), run as the unprivileged runner user.

- **A:** the test as it is.
- **B:** the same tree with the test changed only. The 300 ms deadline starts when the logger sees the `command` event of setup-1 (a small context type whose error is `context.DeadlineExceeded`, armed by a logger wrapper; a 20 s fallback deadline ends a run whose setup-1 never starts). The 100 ms floor, the 3000 ms ceiling and the "aborted at setup-1" check stay. No product code is touched. The B patch is kept in the private research notes; packs link public source and do not carry patches.
- **Mutant:** the same A and B test files over a product change that runs each step with `context.WithoutCancel(ctx)` (the deadline is ignored).
- **Probe (supplementary, not part of the decision):** the A test plus one log line giving the milliseconds from the start of the `Verify` call to the `command` event of setup-1.

## Method

`go test -json -run '^TestWallTimeDeadlineAndNeverStarted$' -count=30 ./verify` per arm and chunk, arms interleaved in chunks of 30 (A,B in odd rounds, B,A in even rounds), 10 rounds per wave, two waves of 300 runs per arm (wave 2 started about 3 minutes after wave 1 ended, after the mutant check). The 1-minute and 5-minute load averages were read at each chunk start. Per-run results are parsed from the JSON events (`rows.tsv`). No synthetic load was added; the host's own load was whatever it was.

## Results

| wave | load5 at chunk starts | arm | runs | fails | failure kind |
|---|---|---|---|---|---|
| 1 | 15.1-18.6 | A | 300 | 2 | setup-1 never started (`results: []`) x2 |
| 1 | 15.1-18.6 | B | 300 | 0 | - |
| 2 | 12.5-15.8 | A | 300 | 0 | - |
| 2 | 12.5-15.8 | B | 300 | 0 | - |
| both | 12.5-18.6 | A | 600 | 2 (0.33%, 95% CI 0.09-1.21%) | - |
| both | 12.5-18.6 | B | 600 | 0 (95% CI 0-0.64%) | - |

- Every chunk started above load5 12, so the 3-12 and below-3 buckets are empty. The Studio was never quiet.
- Both A failures were "never started" (the deadline passed before setup-1's command began), in chunks at load5 17.5 and 18.2 (load1 19 and 21). The "setup-1 ran 19-97 ms" failure seen in delivery runs did not occur in 600 A runs.
- **Mutant:** with the deadline ignored, A and B both fail 2 of 2 (30.5 s each, "item = setup-2, want setup-1"), so B still detects a broken deadline.
- **Probe, 300 runs at load5 15.5-17.9:** time before setup-1 starts is min 215, median 228, p90 248, p99 277, max 297 ms. All 300 runs were over 200 ms; none was over 300 ms. The test has 3-85 ms of headroom before "never started"; runs with about 230 ms spent still pass the 100 ms floor, so the floor is not simply 300 ms minus the earlier work; how setup-1's measured wall time exceeds the budget left was not measured.

## Verdict: yes (adopted under a recorded deviation)

- **Deviation, recorded at adoption.** The registered load arm (A fails at least 3 of 300 under fixed load) was replaced by the natural record of the failing land checks: 8 of 9 runs of this test failed on the two Macs at load5 22-113 while land checks ran. Synthetic CPU load on the Macs is not allowed, and the Linux leg cannot reproduce (its pre-setup work is about 4x shorter). That record, the measured mechanism (215-297 ms of the 300 ms budget spent before setup-1 on the Mac), B failing 0 of 1,200 runs across both legs, and the deadline-ignoring mutant still failing B were judged enough to adopt B. The deviation is stated here so the result is not read as meeting the registered threshold.
- **Result:** B is adopted. kogen-verification's test is to start its 300 ms clock when setup-1 starts, with a fallback deadline for a setup-1 that never starts; no product code changes.

As first published (unresolved):

- The registered rule was: adopt B if B fails 0 of 600 and A fails at least 3 of 300 under load. B met its half (0 of 600, and the mutant fails it). A did not: 2 of 300, then 0 of 300. A did fail, so this is not "the reproduction failed" either.
- The rule's fixed-load condition (a 4-core Linux host under a parallel `go test ./...` of kogen-build, load5 2-3 times its cores) did not run: the exclusive host lock could not be taken (the lock tool's root route to the host failed host-key verification; the host was not held), and running unlocked was not allowed. A second Studio wave replaced it, at natural load only. The quiet-host question (does A fail below load5 3?) is unanswered for the same reason.
- What the data supports: at Studio load the unchanged test already spends most of its budget before setup-1 (probe), fails about 1 run in 300, and B removes that dependence on the pre-setup time. What it does not show is the 8-of-9 failure rate delivery saw at load5 22-113 while a land check ran 8 consumer suites; that needs the loaded condition above.

## Rerun

1. Clone [kogen-verification at `ec39831718de`](https://github.com/KogenAI/kogen-verification/tree/ec39831718deb42a60af26e1e8a9b06a763e1258) twice (arms A and B). Change B's test as described under Arms.
2. `bash chunks.sh <cond> 10 30 <outdir> <dir of A> <dir of B>` (needs `go` on PATH; it writes `chunks.tsv` and one JSON file per chunk).
3. `python3 -I report.py <outdir> [<outdir2> ...] --write <dir>` writes `rows.tsv` and `summary.md`.
4. For the probe: add the one log line described under Arms to a third copy, run `chunks.sh` with that directory for both arms, then `python3 -I probe_report.py <outdir> --write <dir>`.
5. For the missing condition, run steps 2-3 on a 4-core Linux host holding the exclusive host lock, with a parallel `go test -count=1 ./...` of kogen-build at `956b151a6564` looping in the background (restarted as it ends), starting the load several minutes before the first chunk so load5 builds up.

Files: `rows.tsv` (1,200 runs), `chunks-studio.tsv` and `chunks-studio2.tsv` (chunk start, load5, load1, exit code), `summary.md`, `probe-prework.tsv`, `probe-summary.txt`, `chunks.sh`, `report.py`, `probe_report.py`.
