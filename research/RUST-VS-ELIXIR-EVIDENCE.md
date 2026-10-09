# Rust vs Elixir: what our runs showed

Rust passed more often than Elixir in every comparison we ran, except two extra pairs from the last re-run, which were tied. No single round proves the difference statistically: the samples are small and two recent rounds were invalidated. We chose Rust for the Kogen core.

| Run | What was compared | Rust passed | Elixir passed | Status | Round page |
|---|---|---:|---:|---|---|
| Original comparison | Tasks 1, 3, 4 and 6, run separately for each language | 8 of 10 | 2 of 10 | Limited evidence: incomplete list of attempts, no test plan recorded in advance | [Round page](https://bench.kogen.dev/rounds/r70/) |
| Extension | Tasks 2, 5 and 7, run separately for each language | 5 of 6 | 4 of 6 | Valid, but the sample is small | [Round page](https://bench.kogen.dev/rounds/r70-rve-ext/) |
| Re-run with corrected task setup | Task 4 only, run separately for each language | 3 of 3 | 0 of 3 | Limited evidence: the corrected setup's own control checks did not pass | [Round page](https://bench.kogen.dev/rounds/r70-rve-rerun/) |
| First paired run, 9 Oct | Tasks 1, 5 and 7; each pair tested both languages on the same machine; 6 pairs counted before the run stopped | 1 of 6 | 0 of 6 | Invalid: two task prompts differed from their originals |  |
| Paired re-run, 9 Oct | Tasks 1, 5 and 7; each pair tested both languages on the same machine; first 9 pairs | 8 of 9 | 3 of 9 | Invalid under the advance test plan: a rule for checking the run flagged harmless text in tool output. These counts are the official test results. |  |
| Paired re-run, extra pairs | 2 more pairs finished after that run stopped | 1 of 2 | 1 of 2 | Additional results outside the planned comparison |  |
| Spot check, 9 Oct | Tasks 5 and 7, one attempt per language | 2 of 2 | 1 of 2 | Limited evidence from a small follow-up check |  |

The original comparison and its later audit page describe the same 20 attempts and are counted once.

Raw records for the three 9 October runs are not yet published.

## Why Elixir failed

In the paired re-run, Elixir failed four times at the project's own checks for formatting, code quality and type errors (including Credo and Dialyzer), and in each case the coding agent had not run those checks itself. When the agent did run them, Elixir got past them every time. Rust's agent also skipped its checks twice, and Rust's formatting and code-quality checks (rustfmt and Clippy) let the code through. The comparison therefore includes differences in the languages’ checking tools. Four other Elixir failures across the paired re-run and the spot check each missed exactly one hidden test—a test the agent could not see.

## Limits

- small samples, a few to ten attempts per language per run;
- one model (gpt-6-luna at maximum effort);
- some runs weren't paired, and two recent ones were invalidated;
- the task sets differ between runs, so their results are not combined.

## Decision

Rust is the language for the Kogen core; Elixir is not in further rounds.
