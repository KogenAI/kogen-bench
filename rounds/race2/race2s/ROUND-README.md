# Race 2-SOL (10 Oct 2026)

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

Same as race 2 (frozen generated suite, 144 cases, inputs sha 784e6599908f2eeb; same harness, shim-free env, snapshots T+10..50 + FINAL, locks, audit), except the agent model: **gpt-6.1-sol, reasoning effort high** (race 2 used gpt-6-luna max). Arms: Gleam, Rust, Go, TypeScript (Bun); 1 hour, concurrent. Start 05:25:14Z.

**Fairness — Quint connectors:** no arm has a Quint connector available. Checked before launch: the Rust crate cache, Go module cache, Bun/npm caches and Gleam/Hex caches contain no Quint/ITF connector packages; the quint-connect-go checkout and the Quint CLI are locked (unreadable) for the race. None is needed: the suite is black-box (it drives `./kogen` and replays pre-generated traces). Arms have sandbox network access but the brief forbids downloads and installs, and the post-race audit flags any download/install command.

The language implementations ran concurrently on one MacBook. [The round overview](../README.md#reproduction) gives the model, duration, setup and scoring commands for this run. Implementation code and checkpoint snapshots remain private; reproduce with your own implementation.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
