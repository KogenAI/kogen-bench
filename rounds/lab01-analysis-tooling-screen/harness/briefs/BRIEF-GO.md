Using only `inputs/`, produce `out/` (UTF-8, comma-delimited, exact header order, a header row, no index column):

1. `tables.csv`: `language,condition,studio_final,macbook_final,median,spread,median_minus_A`. Exactly 8 rows keyed by (language ∈ {Elixir, Go}, condition ∈ {A, B, C, D}).
   - The final score is `accepted_deviation_final`.
   - median = the mean of the two host finals; spread = |studio − macbook|; median_minus_A = median − (A's median for that language).
   - median_minus_A is empty for A and only for A.
2. `bootstrap.csv`: `language,condition,stat,lo,hi`. Exactly 14 rows.
   - `stat=median` (8 rows): 95% percentile bootstrap interval of the median of the two host finals; resample the two hosts with replacement, 10,000 resamples.
   - `stat=paired_diff_vs_A` (6 rows, B/C/D): resample host pairs together; the statistic is the mean over the resampled hosts of (condition final − A final on the same host).
   - Record the seed and quantile method in the README.
3. `token_cost.csv`: `language,condition,host,total_tokens,final,tokens_per_case`. Exactly 16 rows; host ∈ {studio, macbook}.
   - total_tokens = `tokens.tsv` `total`.
   - tokens_per_case = total_tokens / final, rounded to the nearest integer with ties to even.
4. `plot_data.csv`: `language,condition,host,final,total_tokens_millions`. Exactly the 16 points plotted, with total_tokens_millions = total_tokens / 1,000,000.
5. `token_cost.png` or `token_cost.svg`:
   - 16 points; x = final score (/106), y = total tokens (millions);
   - both axes labelled with units;
   - condition and language visibly encoded, with legends.
6. `README.md`: the rerun command (`./run.sh`), seed, quantile method, and tool and library versions.

Commit everything (including `out/`) to the workspace repo before finishing.

Your stack: Write a plain Go program in a Go module (`go.mod` and `go.sum`) and have `run.sh` invoke it with `go run` or `go build`.

Use only the files in inputs/ and public package registries.
