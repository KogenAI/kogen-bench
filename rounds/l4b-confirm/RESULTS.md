# L4b US results

STATUS: **VALID** — the US part of the round is complete. All 18 scored cells were officially graded through `r70-macbook-window-v1`; all remain in the intention-to-treat denominator, with no exclusions.

**Decision: NOT CONFIRMED** under the pre-registered rule. The packet and control arms each passed 6/9 cells, so Σ(P−C)=0, below the required +2. The observed paired outcomes were two rescues and two losses. Per-variant mean `tests_passed` was equal between packet and control, so there was no test-count regression in this cohort.

The ceiling-risk concern from high Luna-max baselines was recorded before scored cells in a dated [preparation receipt](reproduce/CEILING-RISK-RECEIPT.md) on 7 October 2026. Contemporaneous controls passed 6/9. L4's KEEP came from low-baseline variants; this confirmation cohort tested a different baseline regime. The result is no-confirmation, not evidence against the packet. With n=3 per arm per variant, one model, and one host, it supports no general claim beyond these cells.

The smoke prefix stalled for about 25 minutes at the US disk floor. It received official grades before the remaining cells were released, according to the published operator chronology. The public snapshot has no Standard 1.2 run records for the 18 IDs, no strict-validation receipt for the seven-cell smoke prefix before the remaining cells were released, and no strict-validation receipt for all 18 cells before analysis. Strict checklist completion is not established; see [MEASURED.md](MEASURED.md). The EU extension `l4b-confirm-eu` is **NOT-RUN**: only task 7 was admitted, its baseline was 5/6, and no cells were spent. There is no EU scored result.

The marked block below is generated and checked by the standard-library [reproducer](reproduce/reproduce_us.py) from [cells.csv](data/cells.csv) and the frozen [ORDER.json](reproduce/ORDER.json).

<!-- R70-L4B-US:BEGIN -->

## Per-variant outcomes

| Variant | Packet full passes | Control full passes | Packet mean tests_passed | Control mean tests_passed | P−C |
| --- | ---: | ---: | ---: | ---: | ---: |
| `r70-4-go-fe2` | 3/3 | 3/3 | 18.00 | 18.00 | 0 |
| `r70-4-ts-bun-fe2` | 1/3 | 1/3 | 17.33 | 17.33 | 0 |
| `r70-5-go` | 2/3 | 2/3 | 23.67 | 23.67 | 0 |
| **Total** | **6/9** | **6/9** | — | — | **0** |

**Decision: NOT CONFIRMED** under the pre-registered rule (required Σ(P−C) ≥ +2; observed Σ(P−C) = 0).
Paired outcomes: **2 rescues** and **2 losses**.

## Paired outcomes by variant and seed

| Variant | Seed (rep) | Packet outcome (`tests_passed`) | Control outcome (`tests_passed`) | Pair result |
| --- | ---: | --- | --- | --- |
| `r70-4-go-fe2` | 1 (r61) | PASS (18/18) | PASS (18/18) | same |
| `r70-4-go-fe2` | 2 (r62) | PASS (18/18) | PASS (18/18) | same |
| `r70-4-go-fe2` | 3 (r63) | PASS (18/18) | PASS (18/18) | same |
| `r70-4-ts-bun-fe2` | 1 (r61) | FAIL (17/18) | FAIL (17/18) | same |
| `r70-4-ts-bun-fe2` | 2 (r62) | PASS (18/18) | FAIL (17/18) | rescue |
| `r70-4-ts-bun-fe2` | 3 (r63) | FAIL (17/18) | PASS (18/18) | loss |
| `r70-5-go` | 1 (r61) | PASS (24/24) | PASS (24/24) | same |
| `r70-5-go` | 2 (r62) | PASS (24/24) | FAIL (23/24) | rescue |
| `r70-5-go` | 3 (r63) | FAIL (23/24) | PASS (24/24) | loss |

## Token use per official full pass

Numerator is total usage across all nine cells in that arm, including failed cells; denominator is official full passes. One token definition applies: uncached input + cached input + output = total.

| Arm | Full passes | Uncached input / pass | Cached input / pass | Output / pass | Total / pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| packet | 6/9 | 70,861.5 | 625,066.7 | 31,642.3 | 727,570.5 |
| control | 6/9 | 63,870.2 | 661,077.3 | 30,814.0 | 755,761.5 |

All-cell token sums (packet): uncached 425,169; cached 3,750,400; output 189,854; total 4,365,423.

All-cell token sums (control): uncached 383,221; cached 3,966,464; output 184,884; total 4,534,569.

## Frozen seeded interleaved order and official outcomes

| Order | Cell ID | Variant | Arm | Seed | Rep | Outcome | tests_passed |
| ---: | --- | --- | --- | ---: | ---: | --- | ---: |
| 1 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r63` | `r70-4-go-fe2` | control | 3 | 63 | PASS | 18/18 |
| 2 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r62` | `r70-5-go` | packet | 2 | 62 | PASS | 24/24 |
| 3 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r63` | `r70-4-ts-bun-fe2` | control | 3 | 63 | PASS | 18/18 |
| 4 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r62` | `r70-4-ts-bun-fe2` | packet | 2 | 62 | PASS | 18/18 |
| 5 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r63` | `r70-4-ts-bun-fe2` | packet | 3 | 63 | FAIL | 17/18 |
| 6 | `codex__gpt-6-luna__max__default__r70-5-go__r63` | `r70-5-go` | control | 3 | 63 | PASS | 24/24 |
| 7 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r61` | `r70-4-go-fe2` | packet | 1 | 61 | PASS | 18/18 |
| 8 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2-l4pk__r61` | `r70-4-ts-bun-fe2` | packet | 1 | 61 | FAIL | 17/18 |
| 9 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r62` | `r70-4-ts-bun-fe2` | control | 2 | 62 | FAIL | 17/18 |
| 10 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r61` | `r70-5-go` | packet | 1 | 61 | PASS | 24/24 |
| 11 | `codex__gpt-6-luna__max__default__r70-5-go__r61` | `r70-5-go` | control | 1 | 61 | PASS | 24/24 |
| 12 | `codex__gpt-6-luna__max__default__r70-5-go__r62` | `r70-5-go` | control | 2 | 62 | FAIL | 23/24 |
| 13 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r62` | `r70-4-go-fe2` | control | 2 | 62 | PASS | 18/18 |
| 14 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r63` | `r70-4-go-fe2` | packet | 3 | 63 | PASS | 18/18 |
| 15 | `codex__gpt-6-luna__max__default__r70-4-go-fe2__r61` | `r70-4-go-fe2` | control | 1 | 61 | PASS | 18/18 |
| 16 | `codex__gpt-6-luna__max__default__r70-5-go-l4pk__r63` | `r70-5-go` | packet | 3 | 63 | FAIL | 23/24 |
| 17 | `codex__gpt-6-luna__max__default__r70-4-go-fe2-l4pk__r62` | `r70-4-go-fe2` | packet | 2 | 62 | PASS | 18/18 |
| 18 | `codex__gpt-6-luna__max__default__r70-4-ts-bun-fe2__r61` | `r70-4-ts-bun-fe2` | control | 1 | 61 | FAIL | 17/18 |

<!-- R70-L4B-US:END -->
