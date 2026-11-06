# Launch path decides XProtect scan cost on macOS: detached Go tests are scanned, attached ones are not

Finding id: `lab-xprotect-launch-path-20261106`. Comparison: kogen-shaping-and-builds. Model-free: no model call, no seat tokens.
Verdict: **yes**. A Go test started the way delivery starts Builds (over ssh with nohup, reparented to launchd) cost 1.35 to 1.39 s of XprotectService CPU per run at a 10-package scale; the same command attached to an ssh session cost 0.00 s in all runs.

## Question
During a delivery Build on a macOS build host, the XProtect service used about 40 percent CPU while the Build ran `go test ./...`. The Build's process tree ran from launchd (parent pid 1), not from an ssh session. Does the way a Go test is started change what the scanner spends, and by how much?

## Arms
- **detached (as Builds):** over ssh, `nohup sh script </dev/null &`, so the job is reparented to launchd the moment the ssh session ends.
- **attached:** `ssh host sh script` in the foreground; the process stays a child of the ssh session. Attached with a pty (`ssh -tt`) was tried at one package and read the same.
- **reused binary, detached:** `go test -c` once to a stable path, then run that binary detached.
- **launchctl submit** was tried and left no result file; no data.
All arms ran as an unprivileged user on the same host, without sudo, with a warm build cache, with `-count=1` and a different `-ldflags -X` value per run, so each run links new test binaries.

## Workload and metric
Stage 1: one package (kogen-loop [268327e](https://github.com/KogenAI/kogen-loop/tree/268327e7f9503310dd9834f17f283effa17a2c09), `./tools`, about 8 s). Stage 2: `./...` of the same tree (10 packages, 7 with tests, about 14 s). Metric: cumulative CPU time (`ps` time) of XprotectService, XProtectBridgeService and syspolicyd, as the difference from before the launch to stable after the run (sampled every 3 s until under 0.02 s per sample, twice). Also wall seconds, wired memory (`vm_stat`) and `kern.num_vnodes`. Each run started only on a quiet host (no build, no other `go test`, the build host's heavy lock free), polled every 20 s during a stage 2 run. Idle windows: 6 windows (5 before stage 1, 1 before stage 2), 0.00 s each.

## Results
Stage 2, `./...`, 3 runs per arm, interleaved:
| arm | XprotectService CPU-s per run | bridge CPU-s | syspolicyd CPU-s | wall s |
|---|---|---|---|---|
| detached | 1.39, 1.35, 1.37 | 0.29, 0.25, 0.36 | 0.65, 0.53, 0.74 | 16.52, 14.37, 14.22 |
| attached | 0.00, 0.00, 0.00 | 0.00, 0.00, 0.00 | 0.02, 0.00, 0.01 | 13.37, 13.25, 13.56 |

Stage 1, one package, 2 runs per arm: detached 0.17 and 0.15 s; attached 0.00 and 0.00 s; attached with a pty 0.00 and 0.00 s; reused binary detached 0.00 and 0.16 s (not clearly different from detached).
- **Registered rule** (written before stage 2): attached median at most 10 percent of the detached median, with non-overlapping ranges. Attached median 0.00 s against detached 1.37 s: met.
- **Scale:** about 0.2 s of XprotectService CPU per freshly linked test binary, which is about 10 percent of one core during a 14 s run of 7 binaries; detached also took about 8 percent more wall time. A Build's `go test ./...` over a larger repo for minutes reaches the 40 percent observed by the same mechanism; that scale was not run here.
- **Memory (observation, no cause claimed):** the host was rebooted before the lab began. Within about 35 minutes of Builds, `kern.num_vnodes` went from about 120,000 to its maximum, 263,168, and stayed there. Wired memory went from about 2 GB to about 4 GB in the same window and was not released. It did not move with the lab's own runs.

## Limits
Two stages with n of 2 and 3 per arm on one host and one repository; a whole Build was not run; attachment does not cover a Build whose controlling ssh session drops; Linux has no such scanner. The reboot before the lab means all runs are post-boot. The `launchctl submit` arm produced no data.

## Rerun
On a macOS host with go 1.27.2, an unprivileged user, and no other build running:
1. Clone kogen-loop at 268327e7 into a scratch directory and warm the build cache (`go test -count=1 ./...` once).
2. Edit the `HOST`, `XP` and the go path at the top of `drive-stage2.py` for your host (the `ssh` calls expect a host alias), then run `python3 -I drive-stage2.py`. It writes the per-run rows; `rows.tsv` here is its output joined with stage 1 (`drive-stage1.py`).
