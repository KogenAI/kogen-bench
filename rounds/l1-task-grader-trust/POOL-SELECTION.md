# L1 pool-selection context

STATUS: **VALID** — contextual source-pool summaries, separate from the exact L1 control-grade ledger.

# L1 results — task and grader trust

STATUS: **VALID**: all L1 controls graded on 7 October 2026 (windows 10:24–10:33Z).

## POOL-L2 — headroom variants

The full-suite counts below are source-specific summaries from `POOLS.json`; this table is not an official per-cell outcome table in the L1 round export.

| Task | Stack | Host | Luna-max full-suite successes (of attempts) | Failure cells |
| --- | --- | --- | ---: | --- |
| r70-2-elixir | elixir | kogen-bench-eu | 1 of 3 | codex__gpt-6-luna__max__default__r70-2-elixir__r31, codex__gpt-6-luna__max__default__r70-2-elixir__r33 |
| r70-2-go | go | kogen-bench-us | 2 of 3 | codex__gpt-6-luna__max__default__r70-2-go__r32 |
| r70-4-rust | rust | kogen-bench-eu | 1 of 3 | codex__gpt-6-luna__max__default__r70-4-rust__r10, codex__gpt-6-luna__max__default__r70-4-rust__r13 |
| r70-4-elixir-fe2 | elixir | kogen-bench-eu | 0 of 3 | codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10, codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13, codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9 |
| r70-4-go-fe2 | go | kogen-bench-us | 1 of 2 | codex__gpt-6-luna__max__default__r70-4-go-fe2__r820 |
| r70-4-ts-bun-fe2 | ts-bun | kogen-bench-us | 2 of 4 | codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819, codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9 |

## POOL-L3 — contestant failures with applied patch

All 12 selected cells had make_check=true and cause=hidden_tests_failed. Each is classified as visible checks pass but hidden behavior missing. Eleven rows explicitly record contestant_patch_applied=true; r70-4-rust rep 10 is the legacy row with a patch artifact in inventory but no explicit applied flag, and its grader SHA is absent from the 6 October invalidation record. No selected case supports a possible-over-strict-gate classification from public prompt text and own-check status.

| Cell ID | Task | Failing tests | Classification |
| --- | --- | ---: | --- |
| codex__gpt-6-luna__max__default__r70-2-elixir__r31 | r70-2-elixir | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-2-elixir__r33 | r70-2-elixir | 4 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-2-go__r32 | r70-2-go | 4 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9 | r70-4-elixir-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r10 | r70-4-elixir-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r13 | r70-4-elixir-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-go-fe2__r820 | r70-4-go-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r9 | r70-4-ts-bun-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r819 | r70-4-ts-bun-fe2 | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-5-go__r32 | r70-5-go | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-7-rust__r31 | r70-7-rust | 1 | visible checks pass but hidden behavior missing |
| codex__gpt-6-luna__max__default__r70-4-rust__r10 | r70-4-rust | 2 | visible checks pass but hidden behavior missing |

## POOL-L4 — reference-changed files opened

Transcript review was read-only. This page records only the count of changed reference files the transcript showed as opened.

| Cell ID | Task | Host | Changed files opened |
| --- | --- | --- | ---: |
| codex__gpt-6-luna__max__default__r70-2-elixir__r33 | r70-2-elixir | kogen-bench-eu | 2 |
| codex__gpt-6-luna__max__default__r70-2-go__r32 | r70-2-go | kogen-bench-us | 2 |
| codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r9 | r70-4-elixir-fe2 | kogen-bench-eu | 3 |
| codex__gpt-6-luna__max__default__r70-7-rust__r31 | r70-7-rust | kogen-bench-eu | 1 |

## POOL-L5 — hard variants with Luna-max failures

The six POOL-L2 variants also form POOL-L5; every variant has at least one Luna-max failure. Failure IDs and pass rates are listed above.

## Admission-control coverage

| Variant | Assigned host | Recorded reference/noop evidence | Decision |
| --- | --- | --- | --- |
| r70-2-elixir | EU | EU: 2 reference PASS, 2 noop FAIL | Covered |
| r70-2-go | US | EU: 2 reference PASS, 2 noop FAIL | New US window needed |
| r70-4-rust | EU | EU: 2 reference PASS, 2 noop FAIL | Covered |
| r70-4-elixir-fe2 | EU | EU: 1 reference PASS, 1 noop FAIL; additional reference-core-fixed-frontend failed | Covered for reference/noop |
| r70-4-go-fe2 | US | US reference controls INVALID and noops FAIL; EU: one reference PASS/noop FAIL pair | New US window needed |
| r70-4-ts-bun-fe2 | US | US: 1 reference PASS, 1 noop FAIL; second reference INVALID | Covered for reference/noop |
| r70-5-go | US | EU: 2 reference PASS, 2 noop FAIL | New US window needed |
| r70-7-rust | EU | EU: 2 reference PASS, 2 noop FAIL | Covered |
