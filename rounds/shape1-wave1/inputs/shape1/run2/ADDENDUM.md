# FIX-4 validated first-wave addendum

Recorded at 2026-10-09T19:31:24.270658+00:00.

Only EU c4-4 and US c4b-4 launch, each Go → Rust → TS/Bun, preserving seed 20261022. c4b-2 and c4b-5 are not launched: each has 2/5 Rust, 3/5 Go and 2/5 TS/Bun failing mutant validations; zero validator exclusions. Failed-task admission slots are permanently closed with explicit not-launched disposition latches, without consuming a model attempt.

The six cells use the earlier execution configuration and remain descriptive. The recorded setup was frozen before launch. Queue holds and releases checked the current queue hash.
