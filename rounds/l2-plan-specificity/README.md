# L2 plan specificity × builder strength

## Status

**VALID**

### Why not VALID
- None: the README documents a pre-result registration, execution under its rule, reconciled denominators, recomputable results, matched conditions, and retained evidence.


STATUS: **VALID**

Data completeness: **78/78** current assigned cells have latest exact-cell official rows and are included as VALID. The separate historical Luna-max no-plan baseline contains 32 valid official rows.

Pre-registered: **yes**, 7 October 2026, before the first scored cell; Amendment 1 was recorded before rep 2.
Label: **DESCRIPTIVE**
Question: Does a more specific plan help a weaker builder more?
n: **78 assigned cells**: 72 factorial cells (6 variants × 3 plan levels × 2 builders × 2 reps) plus 6 Luna-low no-plan cells.
Headline: **Luna-low steps vs criteria: 3 steps-only wins, 1 criteria-only win, 8 ties; net +2/12, below the preregistered +3 adoption threshold. Do not adopt steps for cheap builders; report descriptively.**
Configuration: Six fixed R70 task variants; three frozen plan levels; Luna-low and Luna-max builders; two reps per planned condition. Eighteen plans were generated once with Luna-max. Direct Codex builder CLI 0.160.0; 3,600-second cap and zero retries; planner CLI 0.160.1; Python 3.14.7. Elixir/Rust ran on kogen-bench-eu; Go/TypeScript-Bun ran on kogen-bench-us. Runner tree SHA-256: `3a6638ea3d6967f03770478039bf1f32e522ab393c32feb5df85d1b923e1ca19`; wrapper SHA-256: `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`. Mac Studio remained reserved.
Limit: Pilot on 18 frozen plans, one plan per task × level; plan content and specificity are inseparable. The observed one-sided sign test is p=5/16=0.3125 over four discordant pairs; even the minimal +3 screen case has p=1/8=0.125. Low-vs-max results and the historical no-plan baseline are descriptive only; there is no interaction estimator. Confirmation needs independent plans on new tasks and contemporaneous no-plan arms.
Sources: [pre-registration](DESIGN.md); [decision rule](DECISION-RULE.md); [results](RESULTS.md); [official cell data](data/official_cells.csv); [planner receipts](data/planner_usage.csv); [historical no-plan baseline](data/historical_no_plan_max.csv); [reproducer](../../reproduce/l2-plan-specificity.py).

## Lifecycle counts

| Lifecycle count | Count | Scope |
|---|---:|---|
| Planned | 78 | All assigned cells |
| Started | 78 | All gate and bulk cells |
| Finished | 78 | All completed runs |
| Officially graded | 78 | Latest official row per exact cell ID |
| ITT denominator | 78 | All assigned cells |

<!-- L2-CSV-SUMMARY:BEGIN -->
- Lifecycle counts: planned 78 / started 78 / finished 78 / graded 78 / ITT 78.
- Headline: Luna-low steps vs criteria: 3 steps-only wins, 1 criteria-only win, 8 ties; net +2/12, below the preregistered +3 adoption threshold. Do not adopt steps for cheap builders; report descriptively.
- Luna-low descriptive full-pass rates: none 1/6; criteria 4/12; approach 4/12; steps 6/12.
- Luna-max descriptive full-pass rates: criteria 6/12; approach 7/12; steps 6/12; historical no-plan baseline 20/32.
- Sign-test caveat: observed one-sided exact p=5/16=0.3125 over 4 discordant pairs; the minimal +3 case (3 wins, 0 losses) gives p=1/8=0.125.
- Grading provenance: the final 2 EU rep-2 cells (`r70-4-elixir-fe2-l2criteria`, `r70-4-elixir-fe2-l2steps`) used grade_worker SHA 0e6f8aa0 instead of 73dc09af; the change was inventory-glob-only and scoring code was byte-identical.
<!-- L2-CSV-SUMMARY:END -->

## Reproduce

All exact task IDs are in the cell table in [RESULTS.md](RESULTS.md). The six base task IDs are `r70-2-elixir`, `r70-2-go`, `r70-7-rust`, `r70-4-elixir-fe2`, `r70-4-go-fe2`, and `r70-4-ts-bun-fe2`.

Kogen commit: the task-specific commit map below lists every base commit used by the current cells; the first linked commit is [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975).
Harness commit: not recorded as a Git commit. Runner tree SHA-256: `3a6638ea3d6967f03770478039bf1f32e522ab393c32feb5df85d1b923e1ca19`; wrapper SHA-256: `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`.
Model and effort: direct Codex `gpt-6-luna` at low and max for builders; `gpt-6-luna` at max for plan generation. Builder CLI `codex-cli 0.160.0`; planner CLI `codex-cli 0.160.1`; Python `3.14.7`.
Task IDs: six base task IDs above and 18 plan-bearing task IDs in the commit map.
Command: plan generation used the command template below; scored dispatches used the four gate/bulk commands below; official grading used the operator-run MacBook route `r70-macbook-window-v1`. Analysis command: `python3 reproduce/l2-plan-specificity.py`.
Raw records: sanitized official rows and planner receipts are included in the data files below; latest row per exact cell ID is used.

Plan-generation command template (run from each public input directory):

```sh
codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox read-only --model gpt-6-luna -c model_reasoning_effort="max" --cd <public-input-dir> --json --output-last-message <plan.md> -
```

Scored dispatch commands (run from the L2 lane directory):

```sh
python3 dispatch.py us gate
python3 dispatch.py eu gate
python3 dispatch.py us bulk
python3 dispatch.py eu bulk
```

Data files: `rounds/l2-plan-specificity/data/official_cells.csv`, `rounds/l2-plan-specificity/data/planner_usage.csv`, and `rounds/l2-plan-specificity/data/historical_no_plan_max.csv`. The standard-library reproducer recomputes the result page and checks the summary and commit map in this README.

<!-- L2-COMMIT-MAP:BEGIN -->
| Task ID | Plan level | Kogen commit | Plan SHA-256 |
|---|---|---|---|
| `r70-2-elixir` | none | [`470ba65c1d3c19191a2190a032cd9ebf24e71975`](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) | — |
| `r70-2-elixir-l2approach` | approach | [`0c6f95804e901912ba40c256105c49650dade6bd`](https://github.com/KogenAI/kogen-ex/commit/0c6f95804e901912ba40c256105c49650dade6bd) | 4986e20ea03a06466030cd3e40a613a34f6fd7f541d4fb92e103439ea2505f2f |
| `r70-2-elixir-l2criteria` | criteria | [`2c6ee03a749151a28aa0e908de4f1474017b411f`](https://github.com/KogenAI/kogen-ex/commit/2c6ee03a749151a28aa0e908de4f1474017b411f) | e3f054f0bf8335d286581ea716825cb540e31d6333a78935e759feab3ccd1e2d |
| `r70-2-elixir-l2steps` | steps | [`0cabbafd45cf324219747a2fa97968ae262ab8b2`](https://github.com/KogenAI/kogen-ex/commit/0cabbafd45cf324219747a2fa97968ae262ab8b2) | 75b11ce37398535be44d17272c0dbcf55fa7791f93863f4f7bd603df82250a46 |
| `r70-2-go` | none | [`13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82`](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) | — |
| `r70-2-go-l2approach` | approach | [`1db582020ff97c48c854feee9b4588161323cef4`](https://github.com/KogenAI/kogen-ex/commit/1db582020ff97c48c854feee9b4588161323cef4) | 707ff42bb366fad3e83a1c9ba929f7ad15613195e06c078c6678c05e81affcd6 |
| `r70-2-go-l2criteria` | criteria | [`48672b705c40c6232023a63a697f44e12fd7a7d0`](https://github.com/KogenAI/kogen-ex/commit/48672b705c40c6232023a63a697f44e12fd7a7d0) | 92799bbf4b92d915b52b4b3b787dab9bb659380eb196998c41955887fd19e511 |
| `r70-2-go-l2steps` | steps | [`d08c7c9d38b87416c47fb648f472d7524d1ff9d0`](https://github.com/KogenAI/kogen-ex/commit/d08c7c9d38b87416c47fb648f472d7524d1ff9d0) | 9f7dfe458cf2d0e7ce83747a8a1f6bd657f23b467c5173ef5e4c656448ebdf87 |
| `r70-4-elixir-fe2` | none | [`5ccd0bf1e816e2b2f5b2694861f8596402409f52`](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | — |
| `r70-4-elixir-fe2-l2approach` | approach | [`f9a5948042d525d20729f9346770ca185bcecb9d`](https://github.com/KogenAI/kogen-ex/commit/f9a5948042d525d20729f9346770ca185bcecb9d) | c8963e6d6421b153ce56a9c1389ab1af5fb0c434413d14505dda63c143fc207d |
| `r70-4-elixir-fe2-l2criteria` | criteria | [`634d71701ded3a7e4f698650e5bb9fea71fce589`](https://github.com/KogenAI/kogen-ex/commit/634d71701ded3a7e4f698650e5bb9fea71fce589) | 950ac4033b51b7cdffc9b7f4cf1e161d984acf84c83cc7f3949a43b773be6497 |
| `r70-4-elixir-fe2-l2steps` | steps | [`3d1e48fab23a0e2b01fa5051cc1c31a2f8611052`](https://github.com/KogenAI/kogen-ex/commit/3d1e48fab23a0e2b01fa5051cc1c31a2f8611052) | 2515e7b8cec8a619dd955401c2b74a9aa9ed3c68a0b450aa1068b43f4f83eadc |
| `r70-4-go-fe2` | none | [`21d21a2f420a387c921f998e5b4d16efc8f80904`](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) | — |
| `r70-4-go-fe2-l2approach` | approach | [`9c2f20f38404d4cc5906268c5b68357e11902c97`](https://github.com/KogenAI/kogen-ex/commit/9c2f20f38404d4cc5906268c5b68357e11902c97) | dd12e95f67c0388c51a1626bc0d46f1850face51b0209a279624a0baf0013cb5 |
| `r70-4-go-fe2-l2criteria` | criteria | [`1524f0aeb36233c80dd86e635a550dc2b8762995`](https://github.com/KogenAI/kogen-ex/commit/1524f0aeb36233c80dd86e635a550dc2b8762995) | 90f4b65162e54d422cb26bd5c2890eb13224d92d60678e5ff95f11c75e6d1d80 |
| `r70-4-go-fe2-l2steps` | steps | [`9c40d5ead25b9bda63c12fb4919c836d12c415ec`](https://github.com/KogenAI/kogen-ex/commit/9c40d5ead25b9bda63c12fb4919c836d12c415ec) | 104853e7dc867ae0e2e41c7c3abc095d97b1d5398a27da4c590fd94da793ab6f |
| `r70-4-ts-bun-fe2` | none | [`cc3a831a167020538c4ca2ad90185606a2e4ad6a`](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) | — |
| `r70-4-ts-bun-fe2-l2approach` | approach | [`de4007f44b3115aa79c94bf62c09067d839ef7ec`](https://github.com/KogenAI/kogen-ex/commit/de4007f44b3115aa79c94bf62c09067d839ef7ec) | ddb365943f53b51f148cad60d5c4679d3dba69d398cf63e7b9ddbd8c79dc24b1 |
| `r70-4-ts-bun-fe2-l2criteria` | criteria | [`c977e8ea8ce3cd817a87fb32c005cf65a2e7c718`](https://github.com/KogenAI/kogen-ex/commit/c977e8ea8ce3cd817a87fb32c005cf65a2e7c718) | e0c0149b8a6c11a0ff745ae7218dade16ae9ea58420a392a3d17ee680e7e2a41 |
| `r70-4-ts-bun-fe2-l2steps` | steps | [`2dbbffb9759ff1372ff1087951c3332aafd57bf4`](https://github.com/KogenAI/kogen-ex/commit/2dbbffb9759ff1372ff1087951c3332aafd57bf4) | b19f9b6e352b9ab3e099ab510eddd14cd6743c0d2765d99df43282d9bba71ce8 |
| `r70-7-rust` | none | [`111a0c776ae6d93f6e7fccd3fc694d5f4fa26838`](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) | — |
| `r70-7-rust-l2approach` | approach | [`7eb195d8474713c66fcd3173b064d801876c367e`](https://github.com/KogenAI/kogen-ex/commit/7eb195d8474713c66fcd3173b064d801876c367e) | d14c4377010fd3ccb8e5688528d2d36454821e0db9f559dd41d301cc527e2e50 |
| `r70-7-rust-l2criteria` | criteria | [`538de74aefb8bd061438a00da684aeec2b3e8a5b`](https://github.com/KogenAI/kogen-ex/commit/538de74aefb8bd061438a00da684aeec2b3e8a5b) | 6415b150f9a16886a7328d4d847228c5335e5cb26c39d590276f12e3b182eef2 |
| `r70-7-rust-l2steps` | steps | [`c70927abbf58f038226c0f83a24da9edae0c00d0`](https://github.com/KogenAI/kogen-ex/commit/c70927abbf58f038226c0f83a24da9edae0c00d0) | 53ae845814f28c4758e3ddf7d2f7c0fee434b7e490c69b1964afc1d6f6b7c7e5 |

Historical Luna-max no-plan baseline commits:

| Task ID | Official cell IDs | Kogen commit |
|---|---|---|
| `r70-2-elixir` | `codex__gpt-6-luna__max__default__r70-2-elixir__r31`, `codex__gpt-6-luna__max__default__r70-2-elixir__r32`, `codex__gpt-6-luna__max__default__r70-2-elixir__r33`, `codex__gpt-6-luna__max__default__r70-2-elixir__r910` | [`470ba65c1d3c19191a2190a032cd9ebf24e71975`](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) |
| `r70-2-go` | `codex__gpt-6-luna__max__default__r70-2-go__r31`, `codex__gpt-6-luna__max__default__r70-2-go__r32`, `codex__gpt-6-luna__max__default__r70-2-go__r33`, `codex__gpt-6-luna__max__default__r70-2-go__r911` | [`13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82`](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) |
| `r70-4-elixir-fe2` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10`, `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13`, `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9` | [`5ccd0bf1e816e2b2f5b2694861f8596402409f52`](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) |
| `r70-4-elixir-fe2` | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r909`, `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r910` | [`a43dbb032d795157c5a93976947637502b30fece`](https://github.com/KogenAI/kogen-ex/commit/a43dbb032d795157c5a93976947637502b30fece) |
| `r70-4-go-fe2` | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r10`, `codex__gpt-6-luna__max__default__r70-4-go-fe2__r13`, `codex__gpt-6-luna__max__default__r70-4-go-fe2__r9` | [`21d21a2f420a387c921f998e5b4d16efc8f80904`](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) |
| `r70-4-go-fe2` | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r820`, `codex__gpt-6-luna__max__default__r70-4-go-fe2__r823`, `codex__gpt-6-luna__max__default__r70-4-go-fe2__r919` | [`748ebe3a3bc03a112dab83e785159654e0709f9e`](https://github.com/KogenAI/kogen-ex/commit/748ebe3a3bc03a112dab83e785159654e0709f9e) |
| `r70-4-ts-bun-fe2` | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819`, `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r920`, `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r923` | [`880afb00474fe33e9cf38a6d70016ddcd4e38e81`](https://github.com/KogenAI/kogen-ex/commit/880afb00474fe33e9cf38a6d70016ddcd4e38e81) |
| `r70-4-ts-bun-fe2` | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r10`, `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r13`, `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9` | [`cc3a831a167020538c4ca2ad90185606a2e4ad6a`](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) |
| `r70-7-rust` | `codex__gpt-6-luna__max__default__r70-7-rust__r1`, `codex__gpt-6-luna__max__default__r70-7-rust__r2`, `codex__gpt-6-luna__max__default__r70-7-rust__r3`, `codex__gpt-6-luna__max__default__r70-7-rust__r31`, `codex__gpt-6-luna__max__default__r70-7-rust__r32`, `codex__gpt-6-luna__max__default__r70-7-rust__r33`, `codex__gpt-6-luna__max__default__r70-7-rust__r905` | [`111a0c776ae6d93f6e7fccd3fc694d5f4fa26838`](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) |
<!-- L2-COMMIT-MAP:END -->
