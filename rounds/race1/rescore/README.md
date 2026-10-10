# Race 1 FINAL re-score supplement

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

Race 1 ran on a MacBook. Official-run per-case results were not preserved: the scorer deleted each working directory after recording the aggregate. The published supplement re-scores the four concurrent arms’ final code with the official-v2 settings; it is not the official run and may differ by ±1–5 cases. No Gleam re-score is preserved. Implementation code remains private. For setup and scoring commands, see [reproduction](../README.md#reproduction).

| Arm | Re-score passed | Cases | Case results |
| --- | ---: | ---: | --- |
| Rust | 89 | 283 | [`FINAL-rust.tsv`](FINAL-rust.tsv) |
| Go | 86 | 283 | [`FINAL-go.tsv`](FINAL-go.tsv) |
| TypeScript (Bun) | 149 | 283 | [`FINAL-ts.tsv`](FINAL-ts.tsv) |
| Elixir | 6 | 283 | [`FINAL-ex.tsv`](FINAL-ex.tsv) |

Scoring settings and the variance qualification are recorded in [`NOTE.txt`](NOTE.txt).

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
