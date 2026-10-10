**Experimental benchmark spec, not Kogen's released core.**

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

Race race2b: specification (spec/: Quint models + Gherkin scenarios) and generated conformance suite (suite/, frozen; inputs tree SHA-256 prefix 784e6599908f2eeb) exactly as raced. See ../HARNESS.md.


The first launch at 05:07:48 UTC was aborted after about one minute for all arms because setup made the Gleam template unreadable before it was copied. The relaunch began at 05:08:40 UTC and was stopped by the operator at 05:24:00 UTC, after 15 minutes 20 seconds. Only the ten-minute checkpoint scores survive; there is no final score. Race 2C was cancelled by the same order before it was built.

The language implementations ran concurrently on one MacBook. [The round overview](../README.md#reproduction) gives the model, duration, setup and scoring commands for this run. Implementation code and checkpoint snapshots remain private; reproduce with your own implementation.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
