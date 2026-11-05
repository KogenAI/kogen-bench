# Lab L1 on Linux: the wall-time deadline test does not fail, and its pre-setup work is 4x shorter than on the Mac

**Finding.** This is the Linux condition of [Lab L1](../lab-rc-l1-walltime-20261105/README.md), run after that finding was published. On a 4-core Linux server, the unchanged kogen-verification test `TestWallTimeDeadlineAndNeverStarted` passed 600 of 600 runs: 300 on the quiet host (load5 0.07-0.39) and 300 under a fixed background build load (load5 3.35-5.00). The variant whose 300 ms clock starts at setup-1 also passed 600 of 600. A probe shows why: on this host `Verify` spends 23-77 ms before setup-1 starts (median 59 quiet, 40 loaded), against 215-297 ms on the Mac in Lab L1. So the test's budget is tight only where the pre-setup work is slow, which in these runs is the Mac. By the registered rule the Linux reproduction failed and the adoption question was left to the combined evidence; B was then adopted under a recorded deviation (see Verdict). No model call, no product code change.

## Arms

All arms are kogen-verification commit [`ec39831718de`](https://github.com/KogenAI/kogen-verification/tree/ec39831718deb42a60af26e1e8a9b06a763e1258), Go 1.27.3, one 4-core Linux server, run as an unprivileged user under an exclusive host lock.

- **A:** the test as it is.
- **B:** the same tree with the test changed only, exactly as in Lab L1: the 300 ms deadline starts when the logger sees the `command` event of setup-1 (a small context type whose error is `context.DeadlineExceeded`, armed by a logger wrapper; a 20 s fallback deadline ends a run whose setup-1 never starts). The 100 ms floor, the 3000 ms ceiling and the "aborted at setup-1" check stay.
- **Probe:** the A test plus one log line giving the milliseconds from the start of the `Verify` call to the `command` event of setup-1.

## Method

- **Quiet:** after load5 fell below 1, `go test -json -run '^TestWallTimeDeadlineAndNeverStarted$' -count=30 ./verify` per arm and chunk, arms interleaved (A,B in odd rounds, B,A in even rounds), 10 rounds, so 300 runs per arm. Then 300 probe runs.
- **Fixed load:** a `go test -count=1 ./...` of kogen-build at [`956b151a6564`](https://github.com/KogenAI/kogen-build/tree/956b151a6564) looping in the background, started 240 s before the first chunk; then the same 10 rounds of interleaved chunks and 300 probe runs. Load5 was 3.35-5.00 at the chunk starts, about 1x the cores, below the 2-3x the registration aimed for: one build loop on this host did not reach more.
- Load averages were read at each chunk start (`chunks-linux.tsv`). Per-run results are parsed from the JSON events (`rows.tsv`), with Lab L1's `report.py`.

## Results

| condition | load5 at chunk starts | arm | runs | fails |
|---|---|---|---|---|
| quiet | 0.07-0.39 | A | 300 | 0 |
| quiet | 0.07-0.39 | B | 300 | 0 |
| fixed load | 3.35-5.00 | A | 300 | 0 |
| fixed load | 3.35-5.00 | B | 300 | 0 |

| probe | runs | time before setup-1 starts | over 100 ms | over 200 ms |
|---|---|---|---|---|
| quiet (load5 under 1) | 300 | 23-65 ms, median 59 | 0 | 0 |
| fixed load (load5 3.8-5.0) | 300 | 25-77 ms, median 40 | 0 | 0 |
| Mac in Lab L1 (load5 15.5-17.9) | 300 | 215-297 ms, median 228 | 300 | 300 |

- With 23-77 ms spent before setup-1, the unchanged test has over 200 ms of headroom on this host, quiet or loaded. A failure needs the pre-setup work to approach 300 ms, which only the Mac runs did.
- The Linux run therefore cannot prove or refute B by failures. It does show that A's failures are not a property of the test alone: they depend on how long the host takes before setup-1.

## Verdict: yes (adopted under a recorded deviation, with [Lab L1](../lab-rc-l1-walltime-20261105/README.md))

- **Deviation, recorded at adoption.** The registered load arm (A fails at least 3 of 300 under fixed load) was replaced by the natural record of the failing land checks: 8 of 9 runs of this test failed on the two Macs at load5 22-113 while land checks ran. Synthetic CPU load on the Macs is not allowed, and the Linux leg cannot reproduce (its pre-setup work is about 4x shorter). That record, the measured mechanism (215-297 ms of the 300 ms budget spent before setup-1 on the Mac), B failing 0 of 1,200 runs across both legs, and the deadline-ignoring mutant still failing B were judged enough to adopt B. The deviation is stated here so the result is not read as meeting the registered threshold.
- **Result:** B is adopted. kogen-verification's test is to start its 300 ms clock when setup-1 starts, with a fallback deadline for a setup-1 that never starts; no product code changes.

As first published (unresolved):

- Registered rule: adopt B if B fails 0 of 600 and A fails at least 3 of 300 under load; if A never fails, the reproduction failed. On Linux A failed 0 of 600 (quiet and loaded), so the Linux reproduction failed, as registered. B failed 0 of 600 here and 0 of 600 on the Mac.
- Combined with Lab L1, the evidence points at the Mac's pre-setup cost (about 4x Linux at a fraction of the load) eating the test's fixed 300 ms budget. A loaded Mac condition was not run: synthetic load on the Macs is not allowed.

## Rerun

1. On a 4-core Linux host with `go`, `git` and `python3`, in an empty directory holding `chunks.sh` and `run-linux.sh`: `bash run-linux.sh setup` clones the two trees at the commits above. Make the B change in `kv-b` and the probe line in `kv-p` as described under Arms, then `bash run-linux.sh` runs both conditions and the probes.
2. `python3 -I ../lab-rc-l1-walltime-20261105/report.py out-quiet out-load --write <dir>` writes `rows.tsv` and `summary.md`.
3. `grep -o 'prework_ms=[0-9]*' probe-quiet.out probe-load.out` gives the probe values (`probe-prework-linux.tsv`).

Files: `rows.tsv` (1,200 runs), `chunks-linux.tsv` (chunk start, load5, load1, exit code), `summary.md`, `probe-prework-linux.tsv` (600 probe runs), `replay.json`, `chunks.sh`, `run-linux.sh`.
