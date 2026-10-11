# Race 4 decision rule

Complete-spec race on suite-v3. Frozen inputs SHA: 1a04b9dbd7337a6f. The freeze fills this value, N=88 scored cases and TARGET=71; target = ceil(0.80 × N_scored), from COUNTS.txt. Whether this race is descriptive or registered is the project lead call before the freeze.

Wave A starts on both hosts at the same epoch. Wave B starts 5 minutes after wave A's 60-minute cap ends. Each host runs Rust, Go, TypeScript on Bun, Gleam and Elixir with the same harness, kit, gpt-6.1-sol / high and soft 2-core build/test caps. Each wave has a 60-minute cap.

Every 10 seconds, each arm's watcher reads its own brief-command result file. Only an inventory containing every scored case ID, with at least 71/88 scored passes, triggers an immediate TARGET-arm snapshot, STOP-arm and a timestamp/pass-count/result-SHA receipt. Partial runs never trigger. Normal 5-minute snapshots continue until that arm stops. Watcher counts save time; official scores come from later scoring.

Primary: official wall time to 71/88, at the first qualifying 5-minute or TARGET-arm snapshot. FINAL at the cap is the last timed checkpoint. Arms that miss the target rank after those that reach it, by official scored count at FINAL. Report stall-adjusted time alongside raw time, subtracting logged quota/rate-limit waits as before. Secondary: FINAL /N_total and /88, sampled scores, time to 75/90/100 percent where observed, turns, tokens, tokens-to-target (cumulative input, cached input, output, reasoning output and total tokens at the official target snapshot, or FINAL if not reached; reported only and not deciding), CPU, command/model-wait time, stalls, implementation size, tests, audit flags and available efficiency measurements. Binary-search sampling does not supply a complete score curve.

Scoring is after the wave, at most three arm-snapshots concurrently per host, runner --jobs 2 each. SCORE_CONCURRENCY defaults to 3 and may be set to 1 or 2; a shared host slot pool also limits simultaneous wave drivers. Keep the 60-second invocation limits, kg-wrap process groups and cwd sweeps, with one untimed version warm-up (at most 900 seconds) per raw scoring. First score all FINALs over all cases, reporting /N_total and scored /88. Then use exact scored IDs from runner list minus SPEC-BUG-CASES for time-to-target: binary search the snapshots, check S−5, and verify earlier checkpoints when scores regress.

Every scored snapshot whose FIRST scored-case count is within target±3 (inclusive) is scored a SECOND time, including FINAL. For that snapshot and that arm, a case passes officially only if it passes in BOTH raw scorings. The combined per-case count is the official snapshot score used for time-to-target and cap ranking; a flip does not remove passes from other snapshots or other arms. Snapshots outside the band use their first result. Record both raw scorings, per-case combined results and combined scores, and publish flip differences. The race 3 sprint showed 49↔50 flips on timing-sensitive cases (foreground queue land, failing pre-commit hook, the absolute build budget, status watch) under five-way concurrent scoring; this motivates the second scoring and the lower concurrency. No live scoring; watcher inspection is not scoring. Scoring uses scored cases only, except the disclosed FINAL /N_total runs.

Invalidates the whole round: changes to the frozen rule, suite, briefs, kit or harness; lock/isolation failure allowing other runs' code, implementations or hidden suites; wrong model/effort in more than one arm; different harness versions between waves; a host failure stopping a run for more than 10 minutes.

Invalidates one arm in one run (counts as not reached): any receipt using a model/effort other than gpt-6.1-sol / high; an audit flag for a real model-provider call, or for reads of $HOME/.codex*, $HOME/Library, iCloud, other implementations, other arms or $HOME/Areas (package installs and web reads are allowed and only logged), or changes to spec/, conformance/ or TARGET.md (hash checked); FINAL unscorable for a harness reason. Missing model/effort receipts are audit failures. Locks and the audit remain required.

Disclose quota/rate-limit stalls, soft CPU cap bursts, arm-specific flakiness, warm-up time, any clean-copy regrade differences, Studio efficiency cores and the network-on sandbox guarded by audit. No agent dry cell, Astra pre-review or reference/witness implementation. Satisfiability rests on suite checks and the published exclusions; the race shows what is reachable. No winner aggregation beyond these metrics is registered here.

## Internet and package installs

Agents may install packages using their ecosystem's package manager and read
documentation on the web as a developer normally would. Calls to real model
providers remain forbidden; the suite uses a local fake. The agent's own Codex
client traffic is not visible to the command audit and is not flagged.

Each arm receives its own writable caches inside its repository, seeded with
copies of the prefetched kit caches. Cargo, Go, Mix/Hex, Bun, XDG and npm caches
are private; no arm shares writable caches with another. Agent environments
remove offline switches and restore Go's normal package proxy and checksum service.

Scoring and warm-up run offline using dead HTTP/HTTPS/ALL proxies at
`http://127.0.0.1:9`, with `NO_PROXY=127.0.0.1,localhost` for the local fake, and
Cargo, Go, Hex and npm offline switches. The harness exec wrapper reapplies these
settings after the conformance runner's environment filtering. GOFLAGS is unset;
build-cache variables are removed from the implementation environment and the
deliverable is prebuilt. macOS offers no unprivileged hard network block:
this policy is enforced by proxies and offline flags, not a kernel network deny.

Every runtime dependency must be vendored, bundled or cached inside repository
content retained in snapshots, which include build output. The snapshot mechanism
excludes `.kitcache/`, so implementations must not depend on that build cache at
runtime or on paths back to the original arm or kit.

The command audit logs observed network accesses and package installs per arm in
`out/network-<arm>.log`; those accesses are permitted. Command-policy flags apply
only to real provider calls and reads outside the arm of `$HOME/.codex*`, `$HOME/Library`,
iCloud, `$HOME/Areas`, other arms or other races. Existing frozen-input, snapshot and
model/effort receipt integrity checks remain in force. This is a static event-log
audit, not packet capture; it cannot observe hidden traffic inside arbitrary
programs or the agent's Codex client.

Supervisor smoke (after final inputs are frozen):
`./smoke-race4.sh`. Preview with `./smoke-race4.sh --dry-run`.
The smoke prepares fresh arms, installs one package per ecosystem, builds native
stubs that use the installed package, snapshots them, and verifies each warm-up
and the suite's version case through the offline `score-arm.sh` path. Smoke runs
are isolated under this harness and retained for review; no models are launched.
