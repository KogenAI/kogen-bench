# Race 3 decision rule (frozen before the go; sha256 recorded)

Registered kogen-bench round. This file is frozen before the start. Its SHA-256 is sent to main and shown to Almir before the go, and any change after the freeze voids the round.

## Runs

Four runs: wave 1 = MacBook run A + Mac Studio run B, wave 2 = MacBook run C + Mac Studio run D. Each run has five arms (Rust, Go, TypeScript on Bun, Gleam, Elixir) with an identical setup per PLAN. Cap: 3 hours per run.

## Primary metric

**Time to TARGET/N (50/56)**, per arm per run: the elapsed time from the run's start to the first 5-minute snapshot whose official score passes ≥ 50 of the 56 scored cases outside the frozen 88-case exclusion list. The time is **stall-adjusted**: minutes spent waiting after quota or rate-limit refusals (logged per arm) are subtracted. The raw time is always reported next to it.

- An arm that doesn't reach TARGET/N (50/56) within the cap has no time. It ranks **after** every arm that reached the target, and among such arms by score/56 at the FINAL snapshot.
- Per language, the primary value is the **median over its 4 runs**. A run without a time counts as "not reached", which ranks below any time. The median then uses that ordering: e.g. 2 times and 2 not-reached put the median between the slower time and "not reached".

## Winner

The winner is the language with the best primary value **and** the best primary in at least **3 of the 4 runs**. Otherwise the result is **"no decisive winner"**, stated as such, with the full table. If no language reaches TARGET/N (50/56) in at least 2 runs, the round reports "target not reached" and ranks by median score/56 at FINAL. The same ≥ 3 of 4 rule applies; otherwise "no decisive winner".

## Secondary metrics (reported; they do not decide)

- the score curve /144 and /56 at every snapshot;
- time to 75 %, 90 % and 100 % of the 56 scored cases;
- wall time; agent turns;
- input, cached, output and reasoning tokens;
- estimated quota points;
- CPU-seconds; model-wait vs command time;
- stalls (count and time);
- cold and incremental start-to-ready time; own test-suite time;
- artifact size; startup median; median invocation runtime; peak RSS;
- lint findings; LOC; test definitions;
- the blind maintainability review (reported separately);
- audit flags.

## Scoring

All scoring runs after wave 2, one arm-snapshot at a time, on an idle machine. The scorer:
- uses the frozen suite (sha 2eeacf689c103dc3);
- runs kg-wrap process groups, a per-case cwd sweep, jobs 4, and 60 s per invocation;
- does one untimed warm-up `./kogen version` (≤ 900 s) per arm per snapshot.

Every snapshot whose first scored result is within TARGET±3 (47–53/56), plus every FINAL, is scored **twice**. Compare per-case statuses. Flakiness is judged **per arm**: a case that flips for an arm counts as a fail only for that arm at every snapshot in that run; other arms retain their own results. Publish all raw results and the arm-specific flaky list. One clean-copy regrade per arm (a FINAL copied without build output) is compared with the official FINAL. A difference is disclosed, and the official FINAL score stands.

## Disclosures (Almir's speed call)

- No agent dry cell; run a no-model harness smoke per host instead.
- No Astra pre-review.
- No reference or witness implementations.
- Satisfiability rests on the spec-lint, the contradiction check and the published exclusion list; the race itself shows what is reachable.
- The spec v2 patch was a wording and suite patch of the v1 spec, not a full rewrite.
- Races 1, 2, 2s and 2s2 used the unpatched Rust-worded spec.

## CPU cap

Each arm gets **2** cores' worth of build and test parallelism (soft caps, identical for every arm and both hosts). This is the registered soft cap; the no-model smoke per host checks the harness before the freeze.

## Invalidation

**Voids the whole round:**
- any change to this file, the suite, the briefs, the kit or the harness after the freeze;
- a lock or isolation failure that let an arm read another run's code, any Kogen implementation, or hidden suites;
- a different model or effort than `gpt-6.1-sol` / `high` used by more than one arm;
- the two waves not using the same harness version;
- a host failure that stops a run for more than 10 minutes.

**Voids one arm in one run** (that run counts as "not reached" for that language):
- a model or effort other than `gpt-6.1-sol` / `high` in any turn receipt of that arm;
- an audit flag showing a download or install, network fetch, read of `~/.codex*`, `~/Library`, iCloud, another implementation or `~/Areas`, or a modification of `spec/`, `conformance/` or `TARGET.md` (checked by hash);
- a FINAL snapshot that can't be scored for a harness reason (not the arm's own code).

**Disclosed only** (doesn't void):
- quota or rate-limit stalls (handled by stall adjustment);
- soft CPU caps exceeded in bursts (sampler data published);
- flaky cases (handled above);
- clean-copy regrade differences;
- scorer warm-up time;
- efficiency cores on the Studio;
- network-on sandbox (guarded by the audit).

## Pre-declared analysis

The results page follows RESULTS-OUTLINE.md, written before the race. Nothing is added, dropped or re-weighted after seeing the data.
