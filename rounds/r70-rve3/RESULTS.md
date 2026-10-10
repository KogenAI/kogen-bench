# rve3 results

**STATUS: INVALID under the registered interim rule.** The registered audit flagged 7 cells, exceeding its limit of 2. The interim result remains the registered result; the corrected audit and official grades below are post hoc context.

## Registered interim

The registered interim covered pairs 1–9 (18 official cells) and returned INVALID, with 7 flagged cells and no missing or ungraded cells. See [INTERIM-RESULT.json](INTERIM-RESULT.json), [registered audit counts](audit.json), and [status record](STATUS-INVALID.md). Its interim pair tally was Rust 7/9 and Elixir 0/9 after flagged cells were scored zero under the registered rule. This is not an official grade pass rate.

## Official outcomes for pairs 1–9

The official grades show Rust 8/9 and Elixir 3/9 full passes. The `tests_ran` split is 15/18 cells with tests run and 3/18 without tests run. Among the test-running failures, 4 cells failed after the test stage; the remaining 3 failures were before tests ran. This stage split is descriptive.

| Cell | Task | Exact arm label | pass_ outcome | Tests | Failures + errors | Tests ran | Launcher rc | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rve3-eu-p03-elixir | r70-1-elixir | elixir | pass_=false | 25 | 1 | yes | 1 | 911 |
| rve3-eu-p03-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 310 |
| rve3-eu-p05-elixir | r70-7-elixir | elixir | pass_=true | 24 | 0 | yes | 0 | 340 |
| rve3-eu-p05-rust | r70-7-rust | rust | pass_=true | 24 | 0 | yes | 0 | 190 |
| rve3-eu-p06-elixir | r70-5-elixir | elixir | pass_=false | — | 0 | no | 1 | 260 |
| rve3-eu-p06-rust | r70-5-rust | rust | pass_=false | 24 | 2 | yes | 1 | 250 |
| rve3-eu-p08-elixir | r70-5-elixir | elixir | pass_=true | 24 | 0 | yes | 0 | 431 |
| rve3-eu-p08-rust | r70-5-rust | rust | pass_=true | 24 | 0 | yes | 0 | 170 |
| rve3-eu-p09-elixir | r70-1-elixir | elixir | pass_=false | 25 | 1 | yes | 1 | 710 |
| rve3-eu-p09-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 311 |
| rve3-us-p01-elixir | r70-5-elixir | elixir | pass_=false | 24 | 1 | yes | 1 | 450 |
| rve3-us-p01-rust | r70-5-rust | rust | pass_=true | 24 | 0 | yes | 0 | 260 |
| rve3-us-p02-elixir | r70-7-elixir | elixir | pass_=false | — | 0 | no | 1 | 220 |
| rve3-us-p02-rust | r70-7-rust | rust | pass_=true | 24 | 0 | yes | 0 | 140 |
| rve3-us-p04-elixir | r70-7-elixir | elixir | pass_=false | — | 0 | no | 1 | 290 |
| rve3-us-p04-rust | r70-7-rust | rust | pass_=true | 24 | 0 | yes | 0 | 171 |
| rve3-us-p07-elixir | r70-1-elixir | elixir | pass_=true | 25 | 0 | yes | 0 | 1000 |
| rve3-us-p07-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 350 |

## Cells that finished after the stop

Pairs 10–11 are outside the registered interim and are descriptive. Outcomes by pair: pair 10 had no passes; pair 11 had both passes.

| Cell | Task | Exact arm label | pass_ outcome | Tests | Failures + errors | Tests ran | Launcher rc | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rve3-eu-p10-elixir | r70-7-elixir | elixir | pass_=false | — | 0 | no | 1 | 230 |
| rve3-eu-p10-rust | r70-7-rust | rust | pass_=false | 24 | 1 | yes | 1 | 170 |
| rve3-us-p11-elixir | r70-1-elixir | elixir | pass_=true | 25 | 0 | yes | 0 | 1191 |
| rve3-us-p11-rust | r70-1-rust | rust | pass_=true | 25 | 0 | yes | 0 | 200 |

## Dry cells

The two unscored dry cells passed their checks and are not part of the scored denominator.

| Cell | Task | Exact arm label | pass_ outcome | Tests | Failures + errors | Tests ran | Launcher rc | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rve3-dry-eu | r70-5-rust | rust | pass_=true | 24 | 0 | yes | — | — |
| rve3-dry-us | r70-7-elixir | elixir | pass_=true | 24 | 0 | yes | — | — |

## Corrected audit context

The corrected audit re-counts the 18 registered cells as 0/18 flagged. This is post hoc and does not change the INVALID status under the registered audit. Corrected per-cell counts for all 24 available cells, including both dry cells and pairs 10–11, are in [`audit-corrected.jsonl`](pulled-all/audit-corrected.jsonl).
