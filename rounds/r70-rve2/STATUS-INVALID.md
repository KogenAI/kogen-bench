# rve2: INVALID (task-definition confound), recorded 2026-10-09 ~09:14Z

Decision by maintainers. Every cell is kept and will be packaged later as a disclosed INVALID round.

- **Cause.** The published kit (a855b22 / d8c0f59) has prompt.md files for r70-5 and r70-7 that differ from each task's recorded prompt_sha256_original:
  - r70-5-rust f7e3e38e vs 6a593a6a; r70-5-elixir f2f3586b vs 9905736a;
  - r70-7-rust 6d49c8a5 vs 27eb953b; r70-7-elixir 18082d43 vs 10d81ef5.
- **Evidence** (hashes only): the same failing-test set repeats within each task, across arms and hosts (task 7 a54b7e2e29 in 4/4 cells; task 5 d4c076d11e in 4 cells and b592913b84 in 2). Task 1, with matching prompts, passes. The references pass in the identical grade sandbox.
- **Stop.** ROUND-STOP was set on both hosts at ~09:12Z. The running cells finish (EU p06-elixir finished 09:11:20Z; US p10-rust is running), and no new cells start.
- **Descriptive peek before the stop** (owner request, PEEKS.log): 6 pairs complete, Rust 1/6, Elixir 0/6.
- **Successor:** rve3 with the verified original prompts restored in the kit, and a prompt-hash preflight before any cell.
