# Decision rule

DESCRIPTIVE ONLY (H45). There is no threshold, winner, stopping rule, or model-selection decision.

The prospective L5 design covers the new Sol-medium cells. Reused official Sol-medium observations predate the L5 design and are reported as historical comparator data. The Luna-max arm is the official POOL-L5 task baseline; no Luna cells are rerun.

For each task variant, report official full-pass outcomes and rates for direct Codex `gpt-6.1-sol` at medium and direct Codex `gpt-6-luna` at max. Use the latest official grade row for each exact cell ID. A failure remains in the denominator and in the token numerator.

For both arms, uncached input is `usage.input`, cached input is `usage.cached_input`, and output is `usage.output`. A cell's total tokens equal uncached input + cached input + output. Per-pass component costs sum the corresponding token counts across all task attempts, including failures, then divide by the number of official passes. If an arm has no pass on a task, its tokens per pass are undefined. The published display rounds to one decimal when needed.

List the Luna-max failure cell IDs for each task and indicate whether any Sol-medium cell passed on that same task variant. These are separate cells, not paired trials; the comparison does not establish that Sol would repair an individual Luna failure.

Do not pool the uneven task samples into a model ranking or infer causal differences. See the [frozen design](DESIGN.md) and [results](RESULTS.md).
