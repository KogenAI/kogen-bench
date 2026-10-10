# Rust vs Elixir: what our runs showed

Rust passed more often than Elixir in these small recorded samples. The two 9 October registered comparisons are INVALID, and the spot check is DESCRIPTIVE, so these results do not establish a causal language effect. We chose Rust for the Kogen core.

| Run | What was compared | Rust passed | Elixir passed | Status | Round page |
|---|---|---:|---:|---|---|
| Original comparison | Tasks 1, 3, 4 and 6, run separately for each language | 8 of 10 | 2 of 10 | Limited evidence: incomplete list of attempts, no test plan recorded in advance | [Round page](https://bench.kogen.dev/rounds/r70/) |
| Extension | Tasks 2, 5 and 7, run separately for each language | 5 of 6 | 4 of 6 | Valid, but the sample is small | [Round page](https://bench.kogen.dev/rounds/r70-rve-ext/) |
| Re-run with corrected task setup | Task 4 only, run separately for each language | 3 of 3 | 0 of 3 | Limited evidence: the corrected setup's own control checks did not pass | [Round page](https://bench.kogen.dev/rounds/r70-rve-rerun/) |
| First paired run, 9 Oct | Tasks 1, 5 and 7; descriptive peek after six complete pairs | 1 of 6 | 0 of 6 | INVALID: prompts for tasks 5 and 7 differed from their recorded originals; all 17 completed cells are listed on the round page | [Round page](https://bench.kogen.dev/rounds/r70-rve2/) |
| Paired re-run, 9 Oct | Tasks 1, 5 and 7; registered interim after 9 pairs | 8 of 9 | 3 of 9 | INVALID under the registered audit rule; these are official grades, while the registered interim score was Rust 7/9 and Elixir 0/9 | [Round page](https://bench.kogen.dev/rounds/r70-rve3/) |
| Paired re-run, after-stop cells | 2 more pairs finished after the interim stop | 1 of 2 | 1 of 2 | Descriptive cells outside the registered interim | [Round page](https://bench.kogen.dev/rounds/r70-rve3/) |
| Spot check, 9 Oct | Tasks 5 and 7, one attempt per language | 2 of 2 | 1 of 2 | DESCRIPTIVE: small, unregistered follow-up | [Round page](https://bench.kogen.dev/rounds/r70-spot1/) |

The original comparison and its later audit page describe the same 20 attempts and are counted once.

Per-cell records and result tables are available from the three round pages above.

## Limits on diagnosing Elixir failures

The rve3 interim and spot1 round pages retain official outcomes and explain the limits of stage-probe evidence. The Elixir stage labels from spot1 were withdrawn because the probe did not reproduce the grading environment. The invalid rve2 prompt mismatch and rve3 audit rule prevent treating the paired results as a clean language comparison.

## Limits

- small samples, a few to ten attempts per language per run;
- one model (gpt-6-luna at maximum effort);
- some runs weren't paired, and two recent ones were invalidated;
- the task sets differ between runs, so their results are not combined.

## Decision

Rust is the language for the Kogen core; Elixir is not in further rounds.
