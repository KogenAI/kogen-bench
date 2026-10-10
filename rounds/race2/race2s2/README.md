**Experimental benchmark spec, not Kogen's released core.**

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

Race race2s2: specification (spec/: Quint models + Gherkin scenarios) and generated conformance suite (suite/, frozen; inputs tree SHA-256 prefix 784e6599908f2eeb) exactly as raced. See ../HARNESS.md.

## Machine-load disclosure

During this run the MacBook was heavily loaded (load up to 159 on 12 cores). Two sources: the race's own checkpoint scoring, and unrelated publishing jobs (benchmark-publication checks) that ran on the same machine from the start of the run until about 07:08 UTC. Both slowed all agents during the bursts. FINAL was scored after the stop.

At 07:07Z during T+30 checkpoint scoring, load was 159.3/106.2/71.8 on 12 cores and swap was 2.35/3 GB; top CPU users were the two publication-check jobs at about 96% each, the race's scoring sweeps, and the arms' compilers. At 07:37Z after the race, load was 4.6/24.8/51.8. The score effect is not measurable from these data: load slows agents but cannot change how a given snapshot scores except through the 60-second per-case timeout; FINAL was scored after the stop on a quiet machine. See [`LOAD-NOTES.txt`](LOAD-NOTES.txt).

The language implementations ran concurrently on one MacBook. [The round overview](../README.md#reproduction) gives the model, duration, setup and scoring commands for this run. Implementation code and checkpoint snapshots remain private; reproduce with your own implementation.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
