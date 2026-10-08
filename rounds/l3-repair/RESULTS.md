# L3 results

STATUS: **DESCRIPTIVE** — the registered three-rescue threshold failed and preservation is unmeasured.

Release label: DESCRIPTIVE — raw captures not retained; results verified against official grades

All reported outcomes and aggregates below are recomputed from [data/cells.csv](data/cells.csv) by [reproduce/l3_repair.py](reproduce/l3_repair.py).

<!-- BEGIN L3 GENERATED RESULTS -->

## Matched pair results

| Task ID | Exact arm | Original cell ID | Original tests | Repair cell ID | Outcome | Repair tests | wall_s | Uncached | Cached | Output | Total tokens |
| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `r70-2-elixir-l3r31` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-2-elixir__r31` | 24/25 | `codex__gpt-6-luna__max__default__r70-2-elixir-l3r31__r1` | PASS | 25/25 | 1435.708 | 145,573 | 4,334,848 | 71,901 | 4,552,322 |
| `r70-2-elixir-l3r33` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-2-elixir__r33` | 21/25 | `codex__gpt-6-luna__max__default__r70-2-elixir-l3r33__r1` | FAIL | 21/25 | 2753.349 | 384,209 | 9,389,568 | 113,206 | 9,886,983 |
| `r70-2-go-l3r32` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-2-go__r32` | 21/25 | `codex__gpt-6-luna__max__default__r70-2-go-l3r32__r1` | FAIL | 21/25 | 1020.239 | 121,775 | 2,307,072 | 50,768 | 2,479,615 |
| `r70-5-go-l3r1` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-5-go__r1` | 23/24 | `codex__gpt-6-luna__max__default__r70-5-go-l3r1__r1` | FAIL | 23/24 | 489.475 | 76,408 | 503,808 | 24,511 | 604,727 |
| `r70-5-go-l3r32` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-5-go__r32` | 23/24 | `codex__gpt-6-luna__max__default__r70-5-go-l3r32__r1` | PASS | 24/24 | 232.210 | 72,800 | 931,584 | 23,072 | 1,027,456 |
| `r70-7-rust-l3r31` | Arm A → Arm B | `codex__gpt-6-luna__max__default__r70-7-rust__r31` | 23/24 | `codex__gpt-6-luna__max__default__r70-7-rust-l3r31__r1` | FAIL | 23/24 | 471.463 | 80,040 | 409,600 | 24,696 | 514,336 |
| **Total** | — | — | — | — | **2/6 rescues** | — | **6402.444** | **880,805** | **17,876,480** | **308,154** | **19,065,439** |

## Independent base pass rates

Each rate uses the same task and stack's other official reps, excluding that pair's original cell; invalidated rows and reps at or above 700 are excluded.

- `r70-2-elixir-l3r31` / original `codex__gpt-6-luna__max__default__r70-2-elixir__r31`: **1/2** across 2 other official reps.
- `r70-2-elixir-l3r33` / original `codex__gpt-6-luna__max__default__r70-2-elixir__r33`: **1/2** across 2 other official reps.
- `r70-2-go-l3r32` / original `codex__gpt-6-luna__max__default__r70-2-go__r32`: **2/2** across 2 other official reps.
- `r70-5-go-l3r1` / original `codex__gpt-6-luna__max__default__r70-5-go__r1`: **5/6** across 6 other official reps.
- `r70-5-go-l3r32` / original `codex__gpt-6-luna__max__default__r70-5-go__r32`: **5/6** across 6 other official reps.
- `r70-7-rust-l3r31` / original `codex__gpt-6-luna__max__default__r70-7-rust__r31`: **5/5** across 5 other official reps.

## Decision

Rescues: **2/6**. The preregistered threshold is **at least 3/6**; it was not met, so repair-with-verification remains budget-limited.
Per-test no-regression requirement: **UNVERIFIABLE**; per-test grade results are not present in this public bundle. Aggregate pass counts are a separate diagnostic and cannot establish that every previously passed check was preserved.
Aggregate count diagnostic: **PASS**; these counts do not determine the no-regression condition.
Token definition: uncached input + cached input + output; total is their sum.

## Process log

- **Admission controls, initial attempt:** Invalid: reference controls passed, while no-op controls were infrastructure-invalid because deployed variant skeletons lacked repository history.
- **Control deployment correction:** The lane-local deployer was corrected to preserve repository history; stray prepared skeletons were archived, hosts cleaned and redeployed, and variant base archives verified.
- **Admission controls, retry:** Valid: every reference passed and each no-op reproduced its paired original pass count.
- **Initial scored-cell launch attempt:** Voided before any model call after a runner workdir error.
- **Task-record deployment correction:** Task records were corrected to point to each variant skeleton; the host variants were redeployed.
- **Official release and grading sequence:** Official grades were returned through the MacBook-driven official grade window (route r70-macbook-window-v1); the first repair received its clean grade before the next release gate.

<!-- END L3 GENERATED RESULTS -->
