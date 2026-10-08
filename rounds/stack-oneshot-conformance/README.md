# One-shot stack conformance

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of CONDITIONS_MISMATCH, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because original implementation worktrees, conformance result bundles, and host environments are not included; the round cites the retained source reports and result paths but cannot be replayed from this repository.
## Required reproduction metadata

- Question: after the same planned Kogen build process, how much of the executable conformance suite did each language implementation pass before post-build integration rounds?
- Planned process: Sol-high plan, Luna-max package workers, then gates. The observation point is the planned build snapshot, before later integration rounds.
STATUS: **DESCRIPTIVE** — historical snapshots, not a controlled language comparison: suite versions, spec revisions, hosts, and gate timing differ.
- Unit: conformance cases, counted pass, fail, or skip by the suite runner. These runs do not have official scored cells, official grades, or an ITT denominator.
- Kogen commit: Rust `6fde1ed7ae576b281c487f718a38ee86521b90f1`; Go historical I8 `d7e7880` and Linux `d368d2796eb77eb79b8c4ad5ee55e131f63e3c8b`; TypeScript `38297e6139e36dde63777ed5c41c5b7ea9b42c0d`. The Go historical SHA is recorded as `d7e7880` in the I8 evidence; the full SHA is not retained here.
- Harness commit: no single shared harness commit is recorded. The Rust report identifies conformance commit `c1907685e52b9ba965f540b6cc162b489d4f4334`; the Linux run identifies suite version `v1.3+5a570f9` in its JSONL metadata.
- Model and effort: Sol-high planner and Luna-max package workers, as specified by the experiment design. Per-run provider model revisions are not recorded in these conformance artifacts.
- Task IDs: not applicable as official scored Build tasks. Conformance suite case IDs are in the cited source reports and Linux JSONL files.
- Historical execution command: the Linux command rows are retained in `commands.tsv` in the results directory. The original Rust and Go I8 command environments are described in their source reports; a single cross-stack command was not recorded.
- Raw records: Linux `results.jsonl`, `commands.tsv`, `run.log`, and `OPERATOR.log` are outside this repository; the Rust and macOS Go source reports are also external. No historical model execution is replayable from this repository.

## Results

Source-reported case outcomes:

- Rust `kogen-rs`, KRS-INT1, merge `6fde1ed` (7 Oct, 03:25 EAT): 76 passed / 196 cases (38.8%); 120 failed and no skips were reported. This was the first conformance check after all planned packages, before later integration rounds.
- Go `kogen-go`, `d7e7880`, plan end I8, historical macOS v1.2: 61 passed / 236 cases (25.8%); 175 failed, with no skips or errors reported.
- Go `kogen-go`, `d368d27`, Linux v1.3 suite: 76 passed, 196 failed, and 6 skipped of 278 cases (27.3% passed). The JSONL has 278 case rows plus one metadata row.
- TypeScript `kogen-ts`, `38297e6`, Linux v1.3 suite: 90 passed, 148 failed, and 6 skipped in 244 case rows before the run stopped. The JSONL has 245 total rows including its metadata row; the plan was unfinished and gates I3–I7 remained open.

**Lifecycle accounting across the four snapshots** (conformance cases, not scored cells):

| Population | N |
| --- | ---: |
| Planned suite cases across snapshots | 988 |
| Started suite cases across snapshots | 954 |
| Finished suite cases with a runner outcome | 954 |
| Officially graded cells | 0 |
| ITT denominator for official scored cells | 0 |

The aggregate suite counts are sums across the four snapshots above: 196 + 236 + 278 + 278 planned, and 196 + 236 + 278 + 244 started and finished. The TypeScript six skips are included among its 244 runner outcomes. This accounting does not treat conformance cases as official graded cells.

Rust's initial pass fraction was the highest of the one-shot snapshots with recorded outcomes: 76/196 (38.8%) versus TypeScript's partial 90/244 (36.9%), Go Linux's 76/278 (27.3%), and Go's historical 61/236 (25.8%). These fractions describe different suites and execution conditions and should not be read as a matched estimate.

After subsequent integration rounds, Rust reached 231/236 in INT6, about ten hours after INT1, and later passed 278/278 on the final v1.3 suite. Those are later outcomes and are not part of the one-shot comparison. In the related Sol-medium language replication, the reported outcomes were Rust 18/20, Go 18/20, and TS-Bun 15/18; see [that round's status and limits](../lang-sol-replication/README.md).

## Why the numbers aren't perfectly comparable

- The suite versions differ: Rust's v1.1 plus v1.2 suite had 196 cases at the time; Go's historical run used v1.2 with 236 cases; the Linux Go and TypeScript runs used the v1.3 suite with 278 planned cases.
- Rust was built against spec v1.2. Go and TypeScript were built against v1.3-draft.
- Rust's 76/196 comes from its first integration worker (KRS-INT1), which also had a mandate to fix failures; the report doesn't record whether the figure was taken before or after those fixes.
- The Go and TypeScript plans told workers to read the Rust code and started from an already-corrected suite, while Rust's early runs met suite defects later corrected (most of its first 145 v1.3 reds were suite or fake-provider defects).
- TypeScript had 64 of its 66 planned packages merged and gates I0–I2 accepted at the snapshot.
- The TypeScript run is partial, stopped at 244 case rows, and its plan was unfinished with gates I3–I7 open.
- Go and TypeScript plans could consult the Rust implementation; Rust's plan did not have that reference.
- Rust's INT1 check was on macOS; the Go and TypeScript v1.3 run was on Linux. Go's earlier 61/236 result was also on macOS.
- Go and TypeScript gates included fix rounds before the recorded snapshot. Rust's INT1 was its first conformance check after the planned packages.
- Suite sizes and profiles changed, so raw pass counts and pass fractions answer different questions across these runs. The Go macOS v1.2 result and Linux v1.3 results are separate snapshots, not a single Go trajectory.

## Finding

Rust conformed most after the one-shot build by pass fraction among the recorded snapshots, and it is the only stack that is top or tied-top on every measure recorded here, including the later integration results and the related Sol-medium replication. The evidence is descriptive and does not establish a general language effect. Kogen continues in Rust.

## Source records

- Rust INT1: `careful-rebuild/build/LOG.md`, around line 211, records the KRS-INT1 check and result. The merged implementation commit is [`6fde1ed7ae576b281c487f718a38ee86521b90f1`](https://github.com/KogenAI/kogen-rs/commit/6fde1ed7ae576b281c487f718a38ee86521b90f1). The companion `kogen-rs/docs/INTEGRATION-1.md` report contains the 76/196 profile totals, commands, and integration context. The careful-rebuild log is outside this repository.
- Go macOS v1.2: `docs/work/I8-release-comparison-admission.evidence.md` in the Studio Go checkout, section “Commands and results,” reports 61/236 historical cases and identifies the run as v1.2. This file is outside this repository.
- Go and TypeScript Linux v1.3: `/tmp/claude-501/linux-batch/conformance3/results-eu/go/results.jsonl` and `/tmp/claude-501/linux-batch/conformance3/results-eu/ts/results.jsonl`; each JSONL metadata row records the Linux platform, v1.3 suite version, spec revision, and implementation binary hash. The Go file has 278 case outcomes (76/196/6). The TypeScript file has 244 case outcomes before termination (90/148/6). `commands.tsv`, `run.log`, and `OPERATOR.log` in that results directory record the commands and execution order. The run artifacts are not included in this repository.
- Go Shape and plan status: the Linux results include Shape failures; `internal/app/foundation.go:109` in Go commit `d368d27` identifies the unwired Shape route. The real-task smoke failed at Shape in both attempts (2/2 failed). The I8 source above documents the earlier Go milestone; these are component/run observations, not release acceptance.
- Later Rust integration results: `/tmp/claude-501/cx/logs/KRS-INT6.last.md` reports 231 pass / 0 fail / 5 login-skipped of 236. The final v1.3 278/278 result is recorded in the Rust release-gate journal at `levers/OPERATOR-JOURNAL.md` (5:11Z entry). These are later results, not INT1 evidence.
- Related Sol-medium replication: [lang-sol-replication](../lang-sol-replication/README.md), including its stated host, cohort, and registration limits.

Reproduction of model execution is unavailable from this bundle because the original run artifacts and environments are not bundled. The case totals above were checked against the retained source rows and reports; this page records their source-reported results.
