# rve2 results

**STATUS: INVALID.** The prompt mismatch on tasks 5 and 7 compromises the registered comparison. Every available outcome below is descriptive and must not be used as a valid Rust–Elixir comparison.

The launcher stopped after the mismatch was identified. The descriptive peek recorded six complete pairs at that point: Rust 1/6, Elixir 0/6. Later cells that finished before the stop remain individually listed below; the peek is not a tally of the full set. `rc` and wall time come from the filtered launcher START/END lines. Test totals and outcomes are official per-cell fields.

| Cell | Task | Exact arm label | pass_ outcome | Tests | Failures + errors | Tests ran | Launcher rc | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rve2-eu-p02-elixir | r70-7-elixir | elixir | pass_=false | 24 | 1 | yes | 1 | 330 |
| rve2-eu-p02-rust | r70-7-rust | rust | pass_=false | 24 | 1 | yes | 129 | 160 |
| rve2-eu-p04-elixir | r70-5-elixir | elixir | pass_=false | 24 | 1 | yes | 1 | 501 |
| rve2-eu-p04-rust | r70-5-rust | rust | pass_=false | 24 | 2 | yes | 1 | 290 |
| rve2-eu-p05-elixir | r70-1-elixir | elixir | pass_=false | 25 | 1 | yes | 1 | 941 |
| rve2-eu-p05-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 360 |
| rve2-eu-p06-elixir | r70-1-elixir | elixir | pass_=true | 25 | 0 | yes | 0 | 720 |
| rve2-eu-p06-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 270 |
| rve2-us-p01-elixir | r70-5-elixir | elixir | pass_=false | 24 | 2 | yes | 1 | 521 |
| rve2-us-p01-rust | r70-5-rust | rust | pass_=false | 24 | 1 | yes | 1 | 220 |
| rve2-us-p03-elixir | r70-5-elixir | elixir | pass_=false | 24 | 1 | yes | 1 | 480 |
| rve2-us-p03-rust | r70-5-rust | rust | pass_=false | 24 | 1 | yes | 1 | 210 |
| rve2-us-p07-elixir | r70-7-elixir | elixir | pass_=false | 24 | 1 | yes | 1 | 430 |
| rve2-us-p07-rust | r70-7-rust | rust | pass_=false | 24 | 1 | yes | 1 | 160 |
| rve2-us-p08-elixir | r70-1-elixir | elixir | pass_=false | 25 | 1 | yes | 1 | 1061 |
| rve2-us-p08-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 370 |
| rve2-us-p10-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 260 |

## Corrected audit

The corrected per-cell count export is [`audit-corrected.jsonl`](pulled-all/audit-corrected.jsonl). It covers all 17 available cells across both hosts; 0 cells were flagged. The registered round is still INVALID because of the task prompt mismatch.
