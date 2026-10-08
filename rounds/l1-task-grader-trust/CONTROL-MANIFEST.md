# L1 control manifest — prep snapshot (superseded by RESULTS.md)

Preparation snapshot from 7 October 2026, superseded by RESULTS.md for grading outcomes. Current round status: VALID (complete); 24 original controls were staged, 21 graded, and 3 withdrawn, with 2 replacement mutants separately graded. The snapshot records original host-side patch-application checks. These are controls, not model cells.

| Host | Task | Kind | Cell ID | Patch SHA-256 | Apply check |
| --- | --- | --- | --- | --- | --- |
| kogen-bench-eu | r70-2-elixir | mutant1 | `codex__gpt-6-luna__max__default__r70-2-elixir__r701` | `e2924a672c3b06d0e1e1f052d78902d7cd3f5fd956231f66772f44559db47fe6` | PASS |
| kogen-bench-eu | r70-2-elixir | mutant2 | `codex__gpt-6-luna__max__default__r70-2-elixir__r702` | `22c0689248a5e16d1c9a94caca31d82202d4fc0fb02e8d8ebac11a2af8df9f1b` | PASS |
| kogen-bench-eu | r70-2-elixir | alternative | `codex__gpt-6-luna__max__default__r70-2-elixir__r703` | `60e05f57f6920fb43ba38f3e65dc1fcee89f8ae81341b9400d177b6a223f24df` | PASS |
| kogen-bench-us | r70-2-go | mutant1 | `codex__gpt-6-luna__max__default__r70-2-go__r704` | `7e3ad89f06bf5cab5419bdef3eb73f82cef93249afa7253dff4d751067fe70d2` | PASS |
| kogen-bench-us | r70-2-go | mutant2 | `codex__gpt-6-luna__max__default__r70-2-go__r705` | `1a214e3c2c8bf45583c235140b57c07899648d5d8b5fda139fbdcdaadee53a32` | PASS |
| kogen-bench-us | r70-2-go | alternative | `codex__gpt-6-luna__max__default__r70-2-go__r706` | `cd2964a47af8dcbff7c775f02a78ceb04ab9995e6c5d8b479bc94a8b4baaff51` | PASS |
| kogen-bench-eu | r70-4-rust | mutant1 | `codex__gpt-6-luna__max__default__r70-4-rust__r707` | `838a62452037550f4fb920ac532d225c694bf671e3eca1a0e0047d85f4428714` | PASS |
| kogen-bench-eu | r70-4-rust | mutant2 | `codex__gpt-6-luna__max__default__r70-4-rust__r708` | `57693ee80cad479c9d8b5f13694c085253190044a0fe647d62b90e6dd7f4bd81` | PASS |
| kogen-bench-eu | r70-4-rust | alternative | `codex__gpt-6-luna__max__default__r70-4-rust__r709` | `7430efaa80edc9c1fd53de6e34e87a7d1a967ddcb8f5725f9ac6509f1d5f441f` | PASS |
| kogen-bench-eu | r70-4-elixir-fe2 | mutant1 | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r710` | `fab8fc34420f318db41078f4717d4d645a0842925cb1d4215fcca13f9a8e25ea` | PASS |
| kogen-bench-eu | r70-4-elixir-fe2 | mutant2 — build rejection; superseded by r720 for criterion | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r711` | `2e152e5d16db1a65d9a33c30c34f5d1a95c0b7ce903d7c5c39e634a6d0abd9c5` | PASS |
| kogen-bench-eu | r70-4-elixir-fe2 | alternative | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r712` | `3d3b37a84c1c571fb79d249e73a090918a0053d29328597425b58e6e73580ceb` | PASS |
| kogen-bench-us | r70-4-go-fe2 | mutant1 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r713` | `fc5366419456d78161915e6da07d207087c9f211b10ada26b21a4a727a3700d0` | PASS |
| kogen-bench-us | r70-4-go-fe2 | mutant2 — build rejection; superseded by r719 for criterion | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r714` | `a1d332dee0902c2f8d37b8f144f1f4d481563c885e5342edbde7572a4d2e4198` | PASS |
| kogen-bench-us | r70-4-go-fe2 | alternative | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r715` | `95aaffdddaa1eedfd1ab86dde7589b85a9dc048b5243abb7889c7a9272fa7ac5` | PASS |
| kogen-bench-us | r70-4-ts-bun-fe2 | mutant1 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r716` | `c0605ffb24313287746128b148ae88c30b811600446ad95657466ce46f80c522` | PASS |
| kogen-bench-us | r70-4-ts-bun-fe2 | mutant2 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r717` | `28eafedfe080f65b6762d2a2db1502bc8157d3701f340813c3aebc54f9d09283` | PASS |
| kogen-bench-us | r70-4-ts-bun-fe2 | alternative | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r718` | `37d8ba7e88d39962f7fb9235d6d65abd18e995a19b1218b302b9086256273e52` | PASS |
| kogen-bench-us | r70-5-go | mutant1 | `codex__gpt-6-luna__max__default__r70-5-go__r719` | `b3289b778942a8c34e1a94ff59bf620b50809dce3c76d2976c8b931cf1b9b50f` | PASS |
| kogen-bench-us | r70-5-go | mutant2 | `codex__gpt-6-luna__max__default__r70-5-go__r720` | `42ea657ad7bf6dab8b9fab6268fb45e2e67259056f8337355910a53c8f4bf57a` | PASS |
| kogen-bench-us | r70-5-go | alternative | `codex__gpt-6-luna__max__default__r70-5-go__r721` | `c236a7655240bbe02110a1c7c5ad9ebcae269f1dd5200d25c4693f268dc1edac` | PASS |
| kogen-bench-eu | r70-7-rust | mutant1 | `codex__gpt-6-luna__max__default__r70-7-rust__r722` | `7ef849eb0701bdcd2ce69ba8bcf847e74ae5d795c470fa5de735dbbf3f805afa` | PASS |
| kogen-bench-eu | r70-7-rust | mutant2 | `codex__gpt-6-luna__max__default__r70-7-rust__r723` | `e6848318158115994466cd64ae9dc675686fa2977bfaf7c3f2ac1e28407ca885` | PASS |
| kogen-bench-eu | r70-7-rust | alternative | `codex__gpt-6-luna__max__default__r70-7-rust__r724` | `9034a7c304e08c194383516c22152d317894005ff54b9cb4c92cf61af0cbeb71` | PASS |


## Withdrawn before grading

These three staged controls were not graded because the original task-4 Rust variant was removed from all pools before scoring after its recorded failures were attributed to the front-end exit-code trap:

- codex__gpt-6-luna__max__default__r70-4-rust__r707 (mutant 1)
- codex__gpt-6-luna__max__default__r70-4-rust__r708 (mutant 2)
- codex__gpt-6-luna__max__default__r70-4-rust__r709 (alternative)

The matching data/controls.csv rows are marked WITHDRAWN and have no grade, grader SHA, or grade-window timestamp.

## Replacement mutants — 7 October 2026

These two replacements address original build rejections r711/r714. Their behavior class is rebase-success outcome misclassification. Original receipts are unchanged; replacements r719/r720 failed behaviorally with 16/18 tests passing and make_check true. They supersede the original build rejections for the two-behavior-mutant criterion. Public mutant details are limited to patch SHA-256 and behavior class.

| Host | Task | Cell ID | Kind | Patch SHA-256 | Behavior class | Official grade | Grade window |
| --- | --- | --- | --- | --- | --- | --- | --- |
| kogen-bench-us | r70-4-go-fe2 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r719` | mutant replacement | `71ad31d37bdf1745dbf6a39efa8c1dbf6ab138f7432ef4c017c03c51a25fd1fc` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T14:55:34Z |
| kogen-bench-eu | r70-4-elixir-fe2 | `codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r720` | mutant replacement | `f95c4624becd7edd205d1b62b801dd7ac1207255bcd7afd0c012b98e19321fc7` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T16:40:48Z |

Operator grade-window commands are listed in README.md. No scored model cells were launched.
