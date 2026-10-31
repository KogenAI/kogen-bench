# baseline-check-reuse-prototype

A model-free test of one idea for Kogen's delivery builds: when a build restarts on the same starting tree, **skip a baseline check (the test, format or compile command run before any change) if the identical check already passed**. A prototype was written, checked for wrong reuse, and replayed over recorded builds. Verdict: **unresolved**. The prototype is safe in every control tried, and the headroom is real but small: it would fire on about a third of baseline checks, and only four reuses reach 300 s (mean 41 s per reuse). Nothing was run with a model, and the effect on a real build was not measured. Finished 31 October 2026.

## The prototype

Off by default; it is switched on by setting one environment variable. A reuse needs every part of a key to match: the digest of the whole working tree (tracked, untracked and ignored files; build and cache directories are treated as outputs and skipped), the exact command, the version output of the toolchain (Go, Elixir, Erlang, Node, npm, Git), the dependency lockfile digests, an environment digest (secret values are hashed, never stored) and the kind of host (system, architecture, CPU). Rules:

- Only a pass (exit code 0) is stored.
- A key that has ever failed is **poisoned**: it is never reused, because a failure is evidence of a flaky or environment-caused check.
- A check that changed the tree is not stored.
- Any missing or oversized key field means a miss. Entries expire after 24 hours.
- Optionally, every Nth hit runs the check anyway as an audit.

Only the baseline step changes. Verification passes, the final gates, review and landing are untouched. The patch is in `patch/` (sha256 in `patch/a1-baseline-reuse.diff.sha256`): one hook in the baseline step, a new file with the key and store, and a new test file.

## Correctness gate: passed

The gate was written before the code: any control that hits when it must miss drops the idea. In the patch's own tests (Go, default timeout) **all passed**:

- Positive control: identical inputs hit, and the reused verdict equals a fresh run.
- 15 negative controls all miss: changed command, source file, config file, lockfile, a second lockfile, toolchain version, missing toolchain, a generated untracked file, an extra untracked input, a file added in or resized inside the dependency directory, a changed or added environment variable, a changed secret variable, a different host kind, a changed file mode, and an empty host.
- Prior failure is never reused (tried twice), expired entries miss, a check with tree side effects is not stored, and the strict mode sees build directories.
- An environment-caused red after a pass is not hidden: the audit run executes, sees the failure, and poisons the key; a later pass is not reused.
- A secret value does not appear in the store.

Not covered, and stated as a residual risk: an identical-key hit cannot see a fault outside the key (a service down, a port clash, machine load). Only the audit option and the poison rule bound it. The broader test suites of Kogen were not run; the patch is isolated.

## Replay over recorded builds

The input is the anonymised command log of 44 delivery builds from 30 October (`data/runs.json.gz`; task and tree names are counters, commands are digests). It holds 224 baseline executions (23,865 s), of which 91 (11,452 s) belong to restarted builds. The logs record no toolchain, environment or lockfile identity, so the replay uses a weaker key (starting tree id, check, task) and its numbers are **upper bounds**.

| Rule | Reuses | Share of baseline checks / of restart checks | Seconds skipped | Share of restart baseline seconds | Reuses of 300 s or more | Reuses where the real run had failed |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Any earlier pass (naive) | 82 | 36.6% / 90.1% | 7,059 | 61.6% | 10 | 5 (would hide a red) |
| Poison rule (prototype) | 76 | 33.9% / 83.5% | 3,094 | 27.0% | 4 | 0 |
| Poison rule plus 24 h age | 76 | 33.9% / 83.5% | 3,094 | 27.0% | 4 | 0 |

The poison rule halves the naive saving: the flaky and environment-affected test groups are correctly excluded. By check, the prototype's reuses are: Go tests 7 (2,297 s), cucumber 4 (577 s), spec 4 (185 s), format and compile 40 (about 31 s), the rest negligible.

## Against the registered bar

The card required at least 20% of restart baseline seconds, at least 300 s per reuse, 0 wrong reuses and 0 hidden reds. Safety: met (0 in all controls). Share of seconds: 27.0%, met only as an upper bound. Seconds per reuse: **not met** on average (41 s); only the 4 heavy reuses (Go tests, cucumber) reach it. Real savings will be lower than 3,094 s, because a full key misses more often than the weak key used here.

## Decision

Unresolved: safe, small headroom. Recommended next: either a **heavy-checks-only variant** (Go tests, cucumber and tests above about 60 s), or defer. Enabling change if pursued: record the toolchain, lockfile and environment identity of every check in the run logs, so the true fire rate can be measured on a few fresh builds of two trees.

## Rerun

```sh
python3 -I reproduce/baseline-check-reuse-prototype/replay.py reproduce/baseline-check-reuse-prototype/data > /tmp/out.txt
diff /tmp/out.txt reproduce/baseline-check-reuse-prototype/expected-output.txt
```

The control results above come from the patch's own tests; to rerun them, apply the patch to the Kogen source it was written against and run the Go tests whose names contain `Reuse` in the build package. The Kogen source it was written against is identified by the commit and content digest on the card (`card.md`).
