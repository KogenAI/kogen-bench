**Experimental benchmark spec, not Kogen's released core.**

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

Race race2: specification (spec/: Quint models + Gherkin scenarios) and generated conformance suite (suite/, frozen; inputs tree SHA-256 prefix 784e6599908f2eeb) exactly as raced. See ../HARNESS.md.


Case-level result files retain final outcomes (T+10 for the aborted bundle); checkpoint scores for every saved stage remain in `scores.tsv`.

The language implementations ran concurrently on one MacBook. [The round overview](../README.md#reproduction) gives the model, duration, setup and scoring commands for this run. Implementation code and checkpoint snapshots remain private; reproduce with your own implementation.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
