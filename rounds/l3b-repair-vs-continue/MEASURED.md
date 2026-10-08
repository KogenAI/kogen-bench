# L3b: measured results

STATUS: **DESCRIPTIVE** — observed result for eight selected failures; the published per-test evidence recomputes the no-regression condition.

Label: VALID for the registered rule — raw captures not retained; results verified against official grades

The eight selected original failures and all 24 officially scored cells are published as aggregate fields in data/original-failures.csv and data/scored-cells.csv. The 24-row table, rescues, token totals, and rule result are recomputed by reproduce/l3b_repair_vs_continue.py from those files.

## Decision rule

- Rescues: **REPAIR 3/8; CONTINUE 1/8; RESTART 2/8**.
- Pre-registered criterion: REPAIR − CONTINUE = **2**, meeting the threshold of **≥2**.
- Per-test comparison: available for all 8 REPAIR cells; **no REPAIR regression**, recomputed from the public pass/fail sets.
- Result: **observed KEEP for these eight selected failures**. RESTART comparisons are secondary and descriptive.

The label stays DESCRIPTIVE because n=8, deviation [DEV-1](README.md#deviation-dev-1) is described on the round page, and the strict-validation exception was declared before the bulk release in [MISSING.md](MISSING.md) (timing operator-reported). The strict run-record omissions remain documented there; no missing value is estimated.

## Token and wall accounting

The token definition is uncached input + cached input + output. The aggregate inputs use those components from official grade rows. Wall time is the recorded runner wall time; grade-window time is excluded.

### Scored attempts

| Arm | Cells | Uncached input | Cached input | Output | Total tokens | Wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| REPAIR | 8 | 796,472 | 16,684,800 | 288,379 | 17,769,651 | 3,227.436 |
| CONTINUE | 8 | 288,227 | 2,626,048 | 118,358 | 3,032,633 | 1,512.299 |
| RESTART | 8 | 451,463 | 5,742,848 | 200,515 | 6,394,826 | 2,288.914 |

### Original failures as sunk cost

The eight selected original failures contribute the same source cost to each matched-arm view:

| Uncached input | Cached input | Output | Total tokens | Wall seconds |
| ---: | ---: | ---: | ---: | ---: |
| 581,584 | 10,938,112 | 280,318 | 11,800,014 | 5,044.201 |

### Matched-arm all-in view

Each row adds the same eight matched original failures to that arm's attempt usage and wall time. The source cost is counted once in the overall experiment total.

| Arm | Uncached input | Cached input | Output | All-in total tokens | All-in wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| REPAIR | 1,378,056 | 27,622,912 | 568,697 | 29,569,665 | 8,271.637 |
| CONTINUE | 869,811 | 13,564,160 | 398,676 | 14,832,647 | 6,556.500 |
| RESTART | 1,033,047 | 16,680,960 | 480,833 | 18,194,840 | 7,333.115 |

Overall scored attempts: **27,197,110 tokens; 7,028.649 seconds**. Including the source cost once: **38,997,124 tokens; 12,072.850 seconds**.

## Recalculation evidence

The public reproducer and inputs are [reproduce/l3b_repair_vs_continue.py](reproduce/l3b_repair_vs_continue.py), [data/scored-cells.csv](data/scored-cells.csv), [data/original-failures.csv](data/original-failures.csv), and [data/per-test-results.json](data/per-test-results.json). The pass/fail sets reproduce the per-test no-regression check. The pinned source checker was `levers/lanes-2026-10-07/l3b/l3b_rule_check.py`, SHA-256 17ebe3ef4a67bd09c83c8a8568505e8c3e42ea31981afc80ae7bcdc5c046d4a2.
