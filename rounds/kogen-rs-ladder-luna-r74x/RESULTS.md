# Kogen-RS tier-1 results

STATUS: **VALID**

Label: DESCRIPTIVE. Cohort complete: 18 planned IDs have reported outcomes. Three XDG-1 attempt-1 records are reported invalid and replaced by same-ID attempt-2 reruns.

The primary outcome is reported official full-suite pass, intention-to-treat (ITT), over the 18 planned cell IDs. Kogen-RS has source-reported **16/18** passes and **2/18** failures. The recovered internal R74 Codex Luna-max rows show **9/18** passes for the same six task IDs and reps 1–3; see [the recovered rows](../l0-reconcile/data/r74-graded-subset.csv). All 18 outcomes match by task, arm, and rep, but these rows are not joined to the canonical official export. R74 remains **WITHDRAWN**; 9/18 is historical context, not exact official receipts.

## Source evidence disclosure

All per-cell values, execution and hash assertions, XDG-1 and DEV-1 incident details, and identity-audit findings in this document are source-reported and not independently reproducible from the public snapshot. The named lane records are absent from that snapshot: official grade ledgers (`grades/tier1-grades.jsonl` and `grades/tier1-invalid.jsonl`), manifests, usage/report/request records, recipe, runner manifest, and exclusion/incident receipts. Arithmetic consistency in the published tables does not verify extraction or source provenance.

## Cohort and accounting

The Kogen-RS cohort used six tasks × three reps, the `ladder-luna` recipe, builder gpt-6-luna/max, Sol/high shaper, planner, auditor, reviewer and context roles, Luna/max rung roles, no fallback, the default prompt, a 4,800-second timeout, and sequential jobs.

For each Kogen-RS cell, wall time is reported as coming from its manifest, request count from `requests.jsonl`, and token counters from `usage.json`/`report.json`. Total tokens = uncached input + cached input + output. Weighted cache share = cached input / (uncached input + cached input). Reasoning is shown separately and is already part of output; cache-write is excluded from total and was reported as 0 in each attempt. Invalid attempt-1 token data are retained as reported and excluded from cohort totals.

Source-reported XDG-1 details: the three syn-06 attempt-1 runs were **invalid: harness env defect** because setup children did not receive the configured XDG cache location, attempted blocked GitHub release downloads, and stopped during setup. Their attempt-2 reruns retain the same cell IDs and supply the three counted outcomes. The other 15 cell IDs use attempt 1.

Source-reported DEV-1 details: a concurrent US grading window overlapped the final approximately 214 seconds of syn-31 rep 3, causing CPU contention. The cell completed and its reported official FAIL remains in ITT. Its wall time is flagged below and included in the reported sum.

## Source-reported Kogen-RS per-cell values

| Host | Task | Rep (attempt) | Reported official outcome | Wall s | Requests | Uncached | Cached | Output | Total | Reasoning | Weighted cache share |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| US | elx-07-cli-stats | 1 (attempt 1) | PASS | 1090.218 | 58 | 128936 | 703744 | 53972 | 886652 | 20074 | 84.5155% |
| US | elx-07-cli-stats | 2 (attempt 1) | PASS | 802.277 | 53 | 161776 | 577152 | 56973 | 795901 | 24320 | 78.1067% |
| US | elx-07-cli-stats | 3 (attempt 1) | FAIL | 743.054 | 49 | 139586 | 510976 | 46668 | 697230 | 15649 | 78.5438% |
| EU | elx-12-retry-api-deprecation | 1 (attempt 1) | PASS | 1060.214 | 66 | 148992 | 642432 | 52251 | 843675 | 20555 | 81.1742% |
| EU | elx-12-retry-api-deprecation | 2 (attempt 1) | PASS | 1089.409 | 72 | 177398 | 664704 | 49119 | 891221 | 21630 | 78.9339% |
| EU | elx-12-retry-api-deprecation | 3 (attempt 1) | PASS | 1036.205 | 67 | 149784 | 691840 | 51534 | 893158 | 21315 | 82.2030% |
| US | elx-port-board-publish-unpublish-public-boundary | 1 (attempt 1) | PASS | 769.547 | 65 | 106855 | 589568 | 28390 | 724813 | 10665 | 84.6566% |
| US | elx-port-board-publish-unpublish-public-boundary | 2 (attempt 1) | PASS | 510.621 | 42 | 72890 | 270720 | 13676 | 357286 | 5407 | 78.7870% |
| US | elx-port-board-publish-unpublish-public-boundary | 3 (attempt 1) | PASS | 859.744 | 72 | 128173 | 680576 | 33479 | 842228 | 15826 | 84.1517% |
| EU | syn-06-migration-ticket-numbers | 1 (attempt 1) | invalid: harness env defect | 606.161 | 40 | 61013 | 429696 | 23632 | 514341 | 6358 | 87.5664% |
| EU | syn-06-migration-ticket-numbers | 1 (attempt 2) | PASS | 958.731 | 75 | 166387 | 995968 | 43534 | 1205889 | 14676 | 85.6854% |
| EU | syn-06-migration-ticket-numbers | 2 (attempt 1) | invalid: harness env defect | 546.258 | 38 | 54419 | 367872 | 17551 | 439842 | 5381 | 87.1134% |
| EU | syn-06-migration-ticket-numbers | 2 (attempt 2) | PASS | 970.182 | 77 | 195689 | 994304 | 43008 | 1233001 | 18116 | 83.5554% |
| EU | syn-06-migration-ticket-numbers | 3 (attempt 1) | invalid: harness env defect | 767.722 | 45 | 68778 | 577536 | 30766 | 677080 | 7340 | 89.3584% |
| EU | syn-06-migration-ticket-numbers | 3 (attempt 2) | PASS | 1156.755 | 113 | 211701 | 1807872 | 54771 | 2074344 | 17328 | 89.5175% |
| US | syn-20-email-invite-flow | 1 (attempt 1) | PASS | 1215.110 | 88 | 235824 | 1553152 | 64253 | 1853229 | 27900 | 86.8179% |
| US | syn-20-email-invite-flow | 2 (attempt 1) | PASS | 1106.346 | 80 | 166836 | 1278464 | 54984 | 1500284 | 23759 | 88.4567% |
| US | syn-20-email-invite-flow | 3 (attempt 1) | PASS | 1307.677 | 81 | 246735 | 1310080 | 63685 | 1620500 | 23632 | 84.1513% |
| US | syn-31-inbound-email-webhook | 1 (attempt 1) | PASS | 1443.851 | 137 | 248439 | 3015936 | 75417 | 3339792 | 31824 | 92.3894% |
| US | syn-31-inbound-email-webhook | 2 (attempt 1) | PASS | 1145.198 | 91 | 224719 | 1603328 | 60371 | 1888418 | 28739 | 87.7072% |
| US | syn-31-inbound-email-webhook | 3 (attempt 1)† | FAIL | 1669.496 | 106 | 259429 | 1824384 | 80210 | 2164023 | 29624 | 87.5503% |

† Source-reported wall time includes the DEV-1 contention window; outcome remains in ITT.

## Kogen-RS per-task and overall totals

These source-reported totals include the 18 counted attempts only; the three invalid attempts above are excluded. Wall time is the sum of reported cell wall seconds. Reasoning is reported separately, not added to total. In the outcome column, the numerator is reported official full-suite passes and the denominator is counted cells. The new arm is not represented in `results/cells.jsonl`; the source-reported fractions are not joined to that export.

| Task | Exact arm | Reported official outcome / cells | Wall s | Requests | Uncached | Cached | Output | Total | Reasoning | Weighted cache share |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| elx-07-cli-stats | `kogen-rs-ladder-luna-r74x` | 2/3 | 2635.549 | 160 | 430298 | 1791872 | 157613 | 2379783 | 60043 | 80.6361% |
| elx-12-retry-api-deprecation | `kogen-rs-ladder-luna-r74x` | 3/3 | 3185.828 | 205 | 476174 | 1998976 | 152904 | 2628054 | 63500 | 80.7618% |
| elx-port-board-publish-unpublish-public-boundary | `kogen-rs-ladder-luna-r74x` | 3/3 | 2139.912 | 179 | 307918 | 1540864 | 75545 | 1924327 | 31898 | 83.3448% |
| syn-06-migration-ticket-numbers | `kogen-rs-ladder-luna-r74x` | 3/3 | 3085.668 | 265 | 573777 | 3798144 | 141313 | 4513234 | 50120 | 86.8759% |
| syn-20-email-invite-flow | `kogen-rs-ladder-luna-r74x` | 3/3 | 3629.133 | 249 | 649395 | 4141696 | 182922 | 4974013 | 75291 | 86.4458% |
| syn-31-inbound-email-webhook | `kogen-rs-ladder-luna-r74x` | 2/3 | 4258.545 | 334 | 732587 | 6443648 | 215998 | 7392233 | 90187 | 89.7915% |
| **Overall** | `kogen-rs-ladder-luna-r74x` | **16/18** | **18934.635** | **1392** | **3170149** | **19715200** | **926295** | **23811644** | **371039** | **86.1477%** |

## Recovered internal R74 Codex Luna-max rows

These recovered internal rows report R74 Codex gpt-6-luna/max outcomes for these task IDs, reps 1–3, totaling **9/18** passes. All 18 outcomes match the L0 CSV by task, arm, and rep, but the rows are not joined to the canonical official export. R74 remains **WITHDRAWN**, and this comparison is historical context only. Token fields below are the values in the recovered rows; reasoning is shown separately.

| Host | Task | Rep | Reported outcome | Input (as stored) | Cached (as stored) | Output | Reasoning |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| US | elx-07-cli-stats | 1 | FAIL | 103184 | 873216 | 18759 | 10732 |
| US | elx-07-cli-stats | 2 | FAIL | 54504 | 342784 | 13019 | 7720 |
| US | elx-07-cli-stats | 3 | PASS | 43777 | 555776 | 12845 | 7929 |
| EU | elx-12-retry-api-deprecation | 1 | FAIL | 34404 | 245248 | 10039 | 6325 |
| EU | elx-12-retry-api-deprecation | 2 | PASS | 33956 | 304128 | 11895 | 7434 |
| EU | elx-12-retry-api-deprecation | 3 | FAIL | 38388 | 262656 | 10822 | 6968 |
| US | elx-port-board-publish-unpublish-public-boundary | 1 | FAIL | 42559 | 179712 | 6542 | 4290 |
| US | elx-port-board-publish-unpublish-public-boundary | 2 | FAIL | 26577 | 173824 | 4753 | 2764 |
| US | elx-port-board-publish-unpublish-public-boundary | 3 | FAIL | 33143 | 355584 | 9088 | 5854 |
| EU | syn-06-migration-ticket-numbers | 1 | PASS | 77634 | 1603072 | 14218 | 9068 |
| EU | syn-06-migration-ticket-numbers | 2 | PASS | 61906 | 1371904 | 13176 | 8207 |
| EU | syn-06-migration-ticket-numbers | 3 | PASS | 81827 | 1537280 | 20678 | 15503 |
| US | syn-20-email-invite-flow | 1 | FAIL | 81660 | 981504 | 19931 | 13615 |
| US | syn-20-email-invite-flow | 2 | PASS | 50538 | 581632 | 14335 | 8859 |
| US | syn-20-email-invite-flow | 3 | PASS | 78889 | 977408 | 19113 | 12593 |
| US | syn-31-inbound-email-webhook | 1 | FAIL | 73725 | 1366016 | 21908 | 14610 |
| US | syn-31-inbound-email-webhook | 2 | PASS | 78871 | 1457664 | 27555 | 19393 |
| US | syn-31-inbound-email-webhook | 3 | PASS | 77448 | 1263616 | 26888 | 19994 |

### R74 recovered internal per-task and overall rows

| Task | Exact arm | Reported outcome / cells | Input (stored sum) | Cached sum | Output sum | Reasoning sum |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-07-cli-stats | `codex-luna-max` | 1/3 | 201465 | 1771776 | 44623 | 26381 |
| elx-12-retry-api-deprecation | `codex-luna-max` | 1/3 | 106748 | 812032 | 32756 | 20727 |
| elx-port-board-publish-unpublish-public-boundary | `codex-luna-max` | 0/3 | 102279 | 709120 | 20383 | 12908 |
| syn-06-migration-ticket-numbers | `codex-luna-max` | 3/3 | 221367 | 4512256 | 48072 | 32778 |
| syn-20-email-invite-flow | `codex-luna-max` | 2/3 | 211087 | 2540544 | 53379 | 35067 |
| syn-31-inbound-email-webhook | `codex-luna-max` | 2/3 | 230044 | 4087296 | 76351 | 53997 |
| **Overall** | `codex-luna-max` | **9/18** | **1072990** | **14433024** | **275564** | **181858** |

R74 records do not verify whether the stored input counter already includes cached input; the stored input values are smaller than cached values, conflicting with the documented conversion. Therefore uncached input, normalized total tokens, and weighted cache share are **not verifiable from records** and are not calculated. Cache-write is also not carried in these R74 rows.

## Source-reported identity audit: R74 Codex records versus Kogen-RS

| Task | R74 task base commit | Kogen-RS task base commit (per-cell post-setup `base_commit` in parentheses) | Host assignment (R74 / Kogen-RS) | Public prompt SHA-256 | Task-setup SHA-256 (Kogen-RS; R74) | Timeout (R74 / Kogen-RS, s) |
| --- | --- | --- | --- | --- | --- | ---: |
| elx-07-cli-stats | `adb5cbc11e33143bcc0153dc966f1f2ee8846d7d` | `adb5cbc11e33143bcc0153dc966f1f2ee8846d7d` (same; post-setup `cb186af625d2`) | US / US | `f31dba1ebdf2958d7eb7af1ae26e4483a2023ef04f4579df4631479aec2f88e7` (same) | `df639a954b6f1aebfda2a22d763c6bd6e5b5f9f4e287c2c97ba26a6da2334455`; R74 not verifiable from records | 4800 / 4800 |
| elx-12-retry-api-deprecation | `adb5cbc11e33143bcc0153dc966f1f2ee8846d7d` | `adb5cbc11e33143bcc0153dc966f1f2ee8846d7d` (same; post-setup `365648c7ea67`) | EU / EU | `d044a33f4318a08d594f51e63b05c7a21a51f0c142c0972f78df6193131943d1` (same) | `df639a954b6f1aebfda2a22d763c6bd6e5b5f9f4e287c2c97ba26a6da2334455`; R74 not verifiable from records | 4800 / 4800 |
| elx-port-board-publish-unpublish-public-boundary | `9082caa0a17b18c670475a08ef68d417edc0afc6` | `9082caa0a17b18c670475a08ef68d417edc0afc6` (same; post-setup `e633e4c33344`) | US / US | `6ac0dd5c8a0a3d0f8d268ab4508252eb87b65cee1ea627cb0253230469c1b578` (same) | `4756b9372b38be8ce6bc96900578625408bd28baaf15d011f1fcd94be2e21d0b`; R74 not verifiable from records | 4800 / 4800 |
| syn-06-migration-ticket-numbers | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` (same; post-setup `97ab832391bd`) | EU / EU | `1b0906a68da1c191e6397557eda0a2d66ef4e2b7cc059b21ac4b89a6230d725d` (same) | `4756b9372b38be8ce6bc96900578625408bd28baaf15d011f1fcd94be2e21d0b`; R74 not verifiable from records | 4800 / 4800 |
| syn-20-email-invite-flow | `43b6cdcd44bf08d6cd2d2edebdb24c36356513c1` | `43b6cdcd44bf08d6cd2d2edebdb24c36356513c1` (same; post-setup `8c9fbc385acc`) | US / US | `db7585985b61b103d079479d79f1b1e6a439a32049f2d07a39755089c2b08abf` (same) | `4756b9372b38be8ce6bc96900578625408bd28baaf15d011f1fcd94be2e21d0b`; R74 not verifiable from records | 4800 / 4800 |
| syn-31-inbound-email-webhook | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` | `f8b30351614c1b4ad22b28c6bd21b13598fe8a5e` (same; post-setup `31d1b25e645c`) | US / US | `5a4aa8969bcb709d839b7d4c498436ea1706e8673be4f13f84b3e58cc8db1860` (same) | `4756b9372b38be8ce6bc96900578625408bd28baaf15d011f1fcd94be2e21d0b`; R74 not verifiable from records | 4800 / 4800 |

Public prompt SHA-256, host assignment, timeout (4,800 seconds), and task base commits are reported to match on all six tasks. Matching initial task bases does not establish identical post-setup task versions: the lane's per-cell `base_commit` is reported as the post-setup project commit. The Kogen-RS task-setup hashes are source-reported; the R74 setup-command hash is not verifiable from the public snapshot.

The R74 Codex rows are source-reported as dated 2026-10-06; Kogen-RS cells as run 2026-10-07–08. R74 run records identify the MacBook `poll.py` route and report SHA-256 `ffd9173ef9375b58cbe4264aa52e1738ee82babbb826e2ad43aa9505c9c55a7a`; the R74 decision-rule record lists a different `poll.py` SHA-256 (`8d721b07ba5beaf80ba70e7acb6b15f8c94afef6f2223a408b0056947cc27ae2`) and no semantic grader version. For tier-1, the operator reports one-shot grading through `grade_cell.sh`, the Studio wrapper for `poll.py` (`night_grade v2 / mac-private-v2`). The grader-script identity remains unreconciled. R74 venue records are source-reported as Studio for 15 cells and MacBook for 3.

Task base commits, public prompts, host assignment and timeout are reported to match. Grader-script identity and the R74 setup-command hash remain unverifiable; the matched preference rule stays unapplied.

## Evidence

The lane records listed above, R74 run records, and Codex pool are not present in the public snapshot. The linked L0 CSV provides recovered internal R74 rows only; no hidden-suite details are included.
