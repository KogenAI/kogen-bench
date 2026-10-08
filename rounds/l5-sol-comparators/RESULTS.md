# L5 results — final descriptive record

STATUS: **DESCRIPTIVE**

<!-- L5-RESULTS:BEGIN -->
Outcomes use the latest official grade row for each exact cell ID.
Population: 16 Sol observations (12 reused + 4 new); 21 Luna-max POOL-L5 observations.

The arm labels below identify direct Codex `gpt-6.1-sol` at medium and direct Codex `gpt-6-luna` at max.

### `r70-2-elixir`

- Sol-medium official full pass: **2/2 (100%)**; tokens per pass (uncached / cached / output / total): 52,816 / 529,472 / 15,767 / 598,055.
- Luna-max official full pass: **1/3 (33.3%)**; tokens per pass (uncached / cached / output / total): 696,484 / 21,394,176 / 295,879 / 22,386,539.
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-2-elixir__r31`; `codex__gpt-6-luna__max__default__r70-2-elixir__r33`.
- Sol-medium pass cell IDs on this task variant: `codex__gpt-6.1-sol__medium__default__r70-2-elixir__r901`; `codex__gpt-6.1-sol__medium__default__r70-2-elixir__r902`.

### `r70-2-go`

- Sol-medium official full pass: **3/3 (100%)**; tokens per pass (uncached / cached / output / total): 25,221.7 / 185,642.7 / 7,862.7 / 218,727.
- Luna-max official full pass: **2/3 (66.7%)**; tokens per pass (uncached / cached / output / total): 86,891 / 1,045,248 / 44,274 / 1,176,413.
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-2-go__r32`.
- Sol-medium pass cell IDs on this task variant: `codex__gpt-6.1-sol__medium__default__r70-2-go__r1`; `codex__gpt-6.1-sol__medium__default__r70-2-go__r2`; `codex__gpt-6.1-sol__medium__default__r70-2-go__r3`.

### `r70-7-rust`

- Sol-medium official full pass: **3/3 (100%)**; tokens per pass (uncached / cached / output / total): 15,679 / 88,064 / 7,032.7 / 110,775.7.
- Luna-max official full pass: **5/6 (83.3%)**; tokens per pass (uncached / cached / output / total): 63,173.8 / 473,292.8 / 20,395.8 / 556,862.4.
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-7-rust__r31`.
- Sol-medium pass cell IDs on this task variant: `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1`; `codex__gpt-6.1-sol__medium__default__r70-7-rust__r2`; `codex__gpt-6.1-sol__medium__default__r70-7-rust__r3`.

### `r70-4-elixir-fe2`

- Sol-medium official full pass: **1/2 (50%)**; tokens per pass (uncached / cached / output / total): 78,874 / 731,264 / 18,831 / 828,969.
- Luna-max official full pass: **0/3 (0%)**; tokens per pass (uncached / cached / output / total): undefined (0 passes).
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10`; `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13`; `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9`.
- Sol-medium pass cell IDs on this task variant: `codex__gpt-6.1-sol__medium__default__r70-4-elixir-fe2__r902`.

### `r70-4-go-fe2`

- Sol-medium official full pass: **2/3 (66.7%)**; tokens per pass (uncached / cached / output / total): 30,968.5 / 224,896 / 11,787 / 267,651.5.
- Luna-max official full pass: **1/2 (50%)**; tokens per pass (uncached / cached / output / total): 74,166 / 662,272 / 35,900 / 772,338.
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-4-go-fe2__r820`.
- Sol-medium pass cell IDs on this task variant: `codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r1`; `codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r3`.

### `r70-4-ts-bun-fe2`

- Sol-medium official full pass: **0/3 (0%)**; tokens per pass (uncached / cached / output / total): undefined (0 passes).
- Luna-max official full pass: **2/4 (50%)**; tokens per pass (uncached / cached / output / total): 101,863 / 1,042,688 / 53,486.5 / 1,198,037.5.
- Luna-max failure cell IDs: `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819`; `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9`.
- Sol-medium pass cell IDs on this task variant: none.

Token figures are per task and per official pass. Each cell total is uncached input + cached input + output; per-pass costs sum every attempt, including failures, then divide by passes. Values are rounded to one decimal when needed; separately rounded components can differ slightly from the displayed total. A zero-pass arm has undefined tokens per pass.

These are task-variant-level observations across separate cells; the Sol pass IDs are not paired to individual Luna failure IDs.
<!-- L5-RESULTS:END -->

Limit: the reused Sol observations came from another round under the same configuration, and task-level sample sizes are small and unequal. The outcomes are descriptive; they do not establish a general model ranking or causal effect.

Source rows: [Sol-medium official cells](data/sol-cells.csv), [Luna-max POOL-L5 official cells](data/luna-baseline.csv), and [new Sol cells](data/new-cells.csv). The [decision rule](DECISION-RULE.md) defines pass and token accounting.
