# Race 3 — "each language at its best" (plan for Almir's go)

**Question:** which language is best for building Kogen, judged fairly, honestly and transparently, by time to a near-complete implementation of the spec, plus cost and quality metrics.

## Format (Almir's decisions, updated ~11:20Z)

- **Four runs in two waves.** Wave 1: run A on the MacBook and run B on the Mac Studio, started at the same epoch. Wave 2: both hosts again, started at the same epoch 10 minutes after wave 1's cap. Every language runs once on each host per wave, so host differences cancel.
- **Arms:** Rust, Go, TypeScript on Bun, Gleam (Erlang/BEAM), Elixir. One continuing Codex session each (`gpt-6.1-sol`, reasoning effort high), auto-continued until the cap; turn boundaries are logged.
- **Account:** every arm on both hosts uses the shared Codex account (MacBook `~/.codex`; Studio `~/.codex-almir`), so 10 concurrent sessions share one account. Throttling is recorded: each quota or rate-limit refusal is logged per arm, the arm waits 60 s and resumes, and times are reported both raw and with stall waits removed. Quota resets are Almir's alone; the guard only alerts main (HEALTH-EVENT.md) at 85 % and on each arm's first refusal.
- **Clock:** a 3-hour cap per wave. No live scoring and no plateau stop (both dropped by decision): every arm runs the full cap unless its session exits by itself (the exit time is recorded).
- **Checkpoints:** an instant APFS snapshot every **5 minutes**, with prebuilt output (including Rust `target/`); copy times are logged. If the no-model harness smoke shows a copy over 20 s, the interval falls back to 10 minutes and main is told. Nothing else runs during a race.
- **Scoring:** after wave 2 stops, every snapshot of all four runs is scored, one arm-snapshot at a time. The config is the race 2 scorer (kg-wrap process groups, per-case cwd sweep, jobs 4, 60 s per invocation) **plus a warm-up** (double score first results within TARGET±3 (47–53/56) and FINAL, judge flakiness per arm): one untimed (≤ 900 s) `./kogen version` per arm per snapshot before scoring, so compile time already spent on the race clock isn't charged again inside a 60 s case. Disclosed as a difference from races 2/2s/2s2; a later supplement re-scores those FINALs with the warm-up.
- **Suite:** the frozen patched race 3 suite (sha 2eeacf689c103dc3, 144 cases). The headline is time to **TARGET/N (50/56)** (the 56 scored cases outside the frozen 88-case exclusion list, given to every arm as TARGET.md), read from the 5-minute snapshots; /144 is also reported.

## Equal resources

- **CPU:** each arm is capped at 2 cores' worth of parallelism (**soft caps**: macOS has no core pinning; on the Studio, 10 of its cores include 2 efficiency cores; a 10-second per-arm CPU and load sampler records whether the caps held) (CARGO_BUILD_JOBS=2, GOMAXPROCS=2 with `go -p=2`, Erlang `+S 2:2` for Gleam and Elixir, RAYON/UV thread pools 2); 5 × 2 = 10 of 12 cores. The agents run their own suite at `--jobs 2`. macOS has no hard CPU partition, so these are equal caps, not a guarantee; a 10-second per-arm CPU and load sampler records whether they held.
- **Aids ("as I would use it"):** every general aid each ecosystem offers, pre-installed and offline (see the kit's KIT.md):
  - Rust: rustfmt, clippy, rust-analyzer, cargo-nextest (JUnit; stable JSON test output doesn't exist);
  - Go: gofmt, go vet, golangci-lint, goimports, gofumpt, gopls, gotestsum;
  - TS: tsc strict, Biome, bun test;
  - Gleam: compiler checks, `gleam format`, `gleam docs`, LSP, plus a community linter if it works offline;
  - Elixir: `mix format`, warnings-as-errors, Credo strict, usage_rules.
- **Guidance:** the same AGENTS.md structure per language (toolchain, offline docs, check → format → lint → test commands, conventions, a best-practices section of the same 9 parts, offline rules), plus `docs/STACK-GUIDE.md`. For Elixir that's elixir.menu itself; for the others, an equivalent written by our researchers to the same 5 sections, with sources.
- **Libraries:** an equal offline cache of each ecosystem's most popular general-purpose libraries (JSON, YAML/TOML, CLI args, HTTP client, test helpers), chosen by popularity, not by Kogen's needs (LIBS.md). They're pre-fetched and pre-compiled in each template; the agent may use or remove them.
- **Caches:** every arm gets PRIVATE copy-on-write caches inside its own repo, so no writable cache is shared between arms. Toolchains and dependencies are pre-warmed equally before the clock.
- **No Kogen-specific help:** nothing in any kit picks libraries or hints for Kogen's use case.

## Isolation and honesty

- **Locks:** for the race, every other Kogen implementation, clone, race directory (including earlier arms' code), the export archive, `~/.kogen` and the Quint CLI are made unreadable (chmod 000) and restored exactly afterwards. A post-race check verifies that no directory is left at mode 000.
- **Audit:** every agent command is scanned for downloads/installs and reads of `~/.codex*`, `~/Library`, iCloud or `~/Areas`.
- **Disclosure:** the machine's `~/.codex` history contains earlier Kogen transcripts. The sandbox can't stop an agent reading its own CODEX_HOME, so the audit is the guard.
- **Sandbox:** workspace-write with network on (sandbox requirement); the brief forbids any download, and the audit checks it.
- **Machine:** no other heavy jobs during the race (main has told benchmarks).

## Metrics per arm (reported with the result)

- score curve /144 and /56 at every snapshot;
- time to 75 % / 90 % / 100 % of the 56 scored cases (42, 51, 56) and to the TARGET/N (50/56) target (finish time);
- wall time; agent turns;
- input, cached, output and reasoning tokens;
- CPU time (per-turn `time -l`, plus the sampler);
- model-wait time vs command time (build/test/lint wall time from timestamped command events), and CPU-seconds, so compile cost is visible separately while still on the clock;
- quota/rate-limit stalls per arm (count and times), and times with stalls removed;
- build-output size; lines of code; test definitions;
- audit flags.

## Known suite effects (for the review)

Equal for all arms: the suite tests the `kogen` binary's black-box behaviour. Possibly unequal:
1. 16 cases pass only if the implementation forwards RUSTUP_HOME/CARGO_HOME to its project checks (a behaviour choice).
2. First-invocation builds; addressed by the warm-up.
3. A per-case temporary HOME; dependencies are vendored in-repo.

## Before the go

1. The kit passes its offline probe on both hosts.
2. The pass-2 kit is identical on both hosts (checksums) and its probe passes on both.
3. A no-model harness smoke per host (no agent dry cell; snapshot copy times measured).
4. Disk check: 2 waves × 5 arms fit (MacBook 114 GiB free, Studio 260 GiB).
5. No Astra pre-review, by Almir's speed call; publish suite-lint, contradiction and exclusion evidence.
6. Almir's go.
