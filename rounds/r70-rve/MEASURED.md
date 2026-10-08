# Measurement contract: original R70 RvE cohort

Question: what official hidden-suite full-pass outcomes were recorded for Rust, Elixir, Go, and TypeScript/Bun on tasks 1, 3, 4, and 6?

Primary metric: official full pass per exact cell ID. Own checks are secondary. These are release and audit requirements; they do not make the historical comparison confirmatory.

| Phase count | n | Definition |
|---|---:|---|
| Planned scored IDs | 40 | Original selected cohort. |
| Identified scored IDs | 40 | Unique `r70-original-rve` rows in `results/test-counts.jsonl`. |
| Official grades | 40 | Latest official outcome rows for those IDs. |
| ITT | Unresolved | Five extra ungraded deliveries are reported without public IDs or an auditable exclusion join. |

Task IDs, model, and requested effort are stated in [README.md](README.md). The outcome ledger carries official pass/fail labels and test fractions. Resource records are limited to Rust and Elixir in the cost/time ledger. Host comparisons are not pooled for timing.

The exact historical runner invocation and full per-cell harness revision are unavailable. The reproduction script recalculates exported outcomes; it does not recreate the original executions.
