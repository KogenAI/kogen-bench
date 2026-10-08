# L5 — direct Sol-medium comparators

Pre-registered: yes for the four prospective new cells; frozen 7 October 2026 before any new L5 scored cell. The 12 reused official cells are historical observations from the earlier Sol replication and predate this L5 design.

## Question and label

Does direct Codex `gpt-6.1-sol` at MEDIUM solve the selected hard tasks on which direct Luna-max has official failures, and at what token cost per pass?

Label: **DESCRIPTIVE (H45)**. This round reports task-level outcomes and token use. It has no threshold, ranking rule, or decision beyond descriptive reporting. The table is the frozen direct comparator for the Kogen ladder lane.

## Arms and configuration

- Sol arm: direct Codex, `gpt-6.1-sol`, MEDIUM, default prompt, Codex harness, 3,600-second cap, zero retries.
- Luna comparator: existing direct Codex `gpt-6-luna`, MAX, default prompt, official grades reused from the L5 pool; no Luna cells are rerun.
- The six exact task variants are `r70-2-elixir`, `r70-2-go`, `r70-7-rust`, `r70-4-elixir-fe2`, `r70-4-go-fe2`, and `r70-4-ts-bun-fe2`. All six are in the L1 VALID admitted set.
- Rust and Elixir are assigned to kogen-bench-eu; Go and TS-Bun are assigned to kogen-bench-us. This assignment applies to new cells. Reused cells retain their recorded hosts.

## Reuse audit and exact IDs

Every equivalent official Sol-medium cell found on the six exact task IDs is counted. The 12 cells below have official grades, the same task base, direct Codex harness wrapper SHA-256 `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`, CLI `codex-cli 0.160.0`, a 3,600-second timeout, and zero retries.

- `r70-2-go`: `codex__gpt-6.1-sol__medium__default__r70-2-go__r1`, `codex__gpt-6.1-sol__medium__default__r70-2-go__r2`, `codex__gpt-6.1-sol__medium__default__r70-2-go__r3`.
- `r70-7-rust`: `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1`, `codex__gpt-6.1-sol__medium__default__r70-7-rust__r2`, `codex__gpt-6.1-sol__medium__default__r70-7-rust__r3`.
- `r70-4-go-fe2`: `codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r1`, `codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r2`, `codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r3`.
- `r70-4-ts-bun-fe2`: `codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r1`, `codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r2`, `codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r3`.

The official Sol replication cell data and R70 grades contain no equivalent Sol-medium cell on `r70-2-elixir` or `r70-4-elixir-fe2`; the public R70-RvE extension pages contain no exact-task Sol rows. No existing equivalent cell is excluded.

The proposal specified two reps per task. Reuse-first requires every equivalent official cell to count, so four tasks have three reused reps each. The other two tasks have no equivalent Sol cell and receive two new reps each. The frozen Sol population is therefore 16 cells: 12 reused plus 4 new, rather than the proposal's approximate 12.

## New cells and host assignment

The exact new IDs use the unused rep range 901–902. Local public grade ledgers and both worker result trees had no exact ID at freeze time.

| Task | Stack | Host | New direct Sol IDs |
|---|---|---|---|
| `r70-2-elixir` | Elixir | kogen-bench-eu | `codex__gpt-6.1-sol__medium__default__r70-2-elixir__r901`, `codex__gpt-6.1-sol__medium__default__r70-2-elixir__r902` |
| `r70-4-elixir-fe2` | Elixir | kogen-bench-eu | `codex__gpt-6.1-sol__medium__default__r70-4-elixir-fe2__r901`, `codex__gpt-6.1-sol__medium__default__r70-4-elixir-fe2__r902` |

The US pick list is empty because its Go and TS-Bun tasks already have equivalent official Sol-medium cells. The dispatcher runs one new cell at a time per host and reads SOURCE tasks.

## Primary descriptive table

Report one row per task: direct Sol-medium pass count/rate and n; the pre-existing Luna-max pass count/rate and n; and Sol tokens per pass split into uncached input, cached input, and output. Tokens per pass are the componentwise sums across all Sol attempts on that task divided by Sol passes. If there are no passes, report tokens per pass as undefined. Include failed attempts in the token numerator.

| Task | Sol-medium current rows | Luna-max baseline | Sol tokens per pass: uncached / cached / output (total) |
|---|---:|---:|---:|
| `r70-2-elixir` | pending; 2 new cells | 1/3 | pending |
| `r70-2-go` | 3/3 | 2/3 | 25,221.7 / 185,642.7 / 7,862.7 (218,727) |
| `r70-7-rust` | 3/3 | 5/6 | 15,679 / 88,064 / 7,032.7 (110,775.7) |
| `r70-4-elixir-fe2` | pending; 2 new cells | 0/3 | pending |
| `r70-4-go-fe2` | 2/3 | 1/2 | 30,968.5 / 224,896 / 11,787 (267,651.5) |
| `r70-4-ts-bun-fe2` | 0/3 | 2/4 | undefined (0 passes) |

## Token definition

For Codex records, uncached input is `usage.input`, cached input is `usage.cached_input`, and output is `usage.output`. Total tokens equal uncached + cached + output. Reasoning is not added separately because it is included in output accounting. Cost per pass uses all official Sol attempts in the task's numerator, including failures, divided by official Sol passes.

## Limits

This is a selected six-task descriptive comparison, not a general model ranking or causal estimate. The reused Sol outcomes were available before L5 registration; the prospective design covers the four new cells and descriptive aggregation only. Per-task n varies because all equivalent official cells are retained. Reused R70 cells were not randomized with the new pair. Two of the three reused `r70-7-rust` observations ran on US although new Rust cells are assigned EU. The Luna baseline has unequal n by task. No Sol result is available yet for either Elixir task; those cells are NOT-RUN at freeze.
