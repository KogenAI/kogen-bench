# L4b-CONFIRM design

STATUS: **INTERIM — PREPARATION ONLY; no scored cells released, launched, or graded**

Sanitized publication copy of the frozen design source dated 7 October 2026. Original-source SHA-256: `94d0158342fd83188e5a49d3aed538bda401cd96f5335b2992a24e5342634ebc`. The published-byte SHA-256 is recorded in `DESIGN.sha256` and `RELEASE-STATE.json`.

This is a new round (`l4b-confirm`), not an L4 amendment. The pre-registered cohort, order, fairness conditions, and decision rule are frozen in this file before any scored cell.

## Question

On three L1-admitted variants unused by L4, does a frozen public-only context packet improve official full-suite results versus a contemporaneous no-packet control?

## Variants and arms

The L1 ledger marks `r70-4-go-fe2`, `r70-4-ts-bun-fe2`, and `r70-5-go` VALID. These are the only valid L1-admitted variants not used by L4. `r70-4-rust` is WITHDRAWN and is not added.

- **Packet:** `r70-4-go-fe2-l4pk`, `r70-4-ts-bun-fe2-l4pk`, and `r70-5-go-l4pk`; each public prompt appends its frozen packet to the corresponding source prompt. Each skeleton is based on the source base plus one empty child commit with the identical skeleton tree. Child commit creation and `task.json.base_sha` update are builder/operator-owned and remain pending; no scored cell may run before those hashes are recorded.
- **Control:** the unchanged source tasks `r70-4-go-fe2`, `r70-4-ts-bun-fe2`, and `r70-5-go` with no packet.
- Source bases:
- `r70-4-go-fe2` source base: https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904 (packet variant `r70-4-go-fe2-l4pk` child commit pending builder/operator).
- `r70-4-ts-bun-fe2` source base: https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a (packet variant `r70-4-ts-bun-fe2-l4pk` child commit pending builder/operator).
- `r70-5-go` source base: https://github.com/KogenAI/kogen-ex/commit/e0b4a2478a17a924fcecb965b2941ca3396f49d6 (packet variant `r70-5-go-l4pk` child commit pending builder/operator).

The packet is capped at 2,000 tokens, uses only the source task's public prompt, public skeleton, and public interfaces, and cites factual notes to exact source lines. Packet hashes, source-file hashes, and author receipts are in `PACKETS.json` and `packets/`.

## Cohort and configuration

The planned cohort is 18 cells: 3 variants × 2 arms × 3 paired seeds. Each arm has n=3 per variant; 9 cells per arm. The budget ceiling is 36 Luna-max cells; this round plans 18 and has no automatic expansion.

Model and harness: direct Codex, `gpt-6-luna` at `max`; worker Codex CLI `0.160.0`; Python `3.14.7`; timeout 3,600 seconds; zero retries. All six task IDs run on `kogen-bench-us`, sequentially one cell at a time, through the same runner, sandbox, task environment, and official operator grade route. The only treatment difference is the appended packet. The dispatcher shares the host cap of 3 with active `lanes-2026-10-07` cells and honors lane, R70, and ROOT STOP files.

Seeds 1, 2, and 3 map to unused reps 61, 62, and 63 respectively. `rep-check.json` records checks against local public grade/data ledgers and `COMPLETE.json` cell IDs on both benchmark hosts; no matching rep 61–63 was found for any source or packet task.

One token definition applies: uncached input, cached input, and output; total tokens equal their sum. No alternate token accounting is used.

## Frozen interleaved order

The canonical pre-shuffle list is variant order (`r70-4-go-fe2`, `r70-4-ts-bun-fe2`, `r70-5-go`), packet then control within each variant, and seeds 1, 2, 3 within each arm. One `random.Random(20261008).shuffle` produced the following order, also stored in `ORDER.json` and `PICKS.json`.

Execution follows this recorded order in two stages. The first seven cells are the shortest prefix that includes at least one packet and one control cell for each source variant; they run sequentially as the exact-arm sandbox smoke cohort. The remaining eleven cells run in order only after the operator records official grades for the smoke cohort and completes the full release checklist. This preserves the preregistered order and the checklist gate.

| Order | Cell ID | Variant | Arm | Seed | Rep |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r63` | r70-4-go-fe2 | control | 3 | 63 |
| 2 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r62` | r70-5-go | packet | 2 | 62 |
| 3 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r63` | r70-4-ts-bun-fe2 | control | 3 | 63 |
| 4 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r62` | r70-4-ts-bun-fe2 | packet | 2 | 62 |
| 5 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r63` | r70-4-ts-bun-fe2 | packet | 3 | 63 |
| 6 | `codex__gpt-6-luna__max__default__r70-5-go__r63` | r70-5-go | control | 3 | 63 |
| 7 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r61` | r70-4-go-fe2 | packet | 1 | 61 |
| 8 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r61` | r70-4-ts-bun-fe2 | packet | 1 | 61 |
| 9 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r62` | r70-4-ts-bun-fe2 | control | 2 | 62 |
| 10 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r61` | r70-5-go | packet | 1 | 61 |
| 11 | `codex__gpt-6-luna__max__default__r70-5-go__r61` | r70-5-go | control | 1 | 61 |
| 12 | `codex__gpt-6-luna__max__default__r70-5-go__r62` | r70-5-go | control | 2 | 62 |
| 13 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r62` | r70-4-go-fe2 | control | 2 | 62 |
| 14 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r63` | r70-4-go-fe2 | packet | 3 | 63 |
| 15 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r61` | r70-4-go-fe2 | control | 1 | 61 |
| 16 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r63` | r70-5-go | packet | 3 | 63 |
| 17 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r62` | r70-4-go-fe2 | packet | 2 | 62 |
| 18 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r61` | r70-4-ts-bun-fe2 | control | 1 | 61 |

## Outcome and fairness rules

The primary outcome is an official full-suite pass. For each variant v, P_v is packet passes out of 3 and C_v is control passes out of 3. Report per-variant values and the sum Σ_v(P_v − C_v).

**CONFIRM** only if Σ_v(P_v − C_v) ≥ +2 across the three variants and no variant's packet mean `tests_passed` is more than 1 below its control mean. Otherwise report **NOT CONFIRMED**. Report a rescue for each seed where control fails and packet passes; report a loss for the reverse. Pair strictly by variant and seed. Timeouts remain failures. Exclude a cell only for a proven environment or adapter fault, with its evidence and disposition recorded.

No hidden-suite text, grader output, failure names, or reference content enters packet authorship or public reporting. Report outcomes and test counts only.

## Release state

This is preparation only. `STOP` remains present and release gates remain false except the frozen design receipt. No scored cells or admission controls have been launched or graded. Before any bulk release, satisfy every item in `levers/RELEASE-CHECKLIST.md`, including one exact packet/control sandbox cell per variant through the official operator grading route. Shared grading infrastructure remains untouched; the lane carries a proposed grade-worker glob patch only.
