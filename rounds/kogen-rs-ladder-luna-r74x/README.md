# Kogen-RS R74 sandbox comparison

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING, DECISION_RULE_NOT_APPLIED. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

### Why not VALID
- **DECISION_RULE_NOT_APPLIED:** DECISION-RULE.md requires an incomplete comparison when exact official comparator rows are unavailable; the rule remains unapplied.
- **PRE_REGISTRATION_UNPROVEN:** No pre-registered rule predating the first result is established.
- **RAW_EVIDENCE_MISSING:** The reported grade rows and invalid-attempt records are not retained in the round files.


STATUS: **DESCRIPTIVE** — 18 planned IDs have source-reported outcomes.

Registration: the design was recorded 2026-10-07; registration/amendment timing is operator-reported. See the dated [Registration amendment](DECISION-RULE.md#registration-amendment-2026-10-08).
Label: DESCRIPTIVE, with the original operational preference rule retained.
Arm: `kogen-rs-ladder-luna-r74x`.
Question: On six task IDs, how do the source-reported Kogen-RS results compare with recovered internal R74 Codex Luna-max rows for historical context?
n: 18 planned cell IDs (six tasks × three reps); the recovered R74 rows are not joined to the canonical official export.

## Evidence disclosure

Per-cell outcomes and metrics, execution and hash assertions, XDG-1 and DEV-1 incident details, and the identity audit are source-reported and not independently reproducible from the public snapshot. The named lane records are absent from this snapshot: official grade ledgers, manifests, usage/report/request records, recipe, runner manifest, and exclusion/incident receipts. The tables' arithmetic does not verify their extraction or source provenance.

All 18 Codex outcomes match by task, arm, and rep in the [recovered internal R74 rows](../l0-reconcile/data/r74-graded-subset.csv). Those rows are not joined to the canonical official export; R74 remains **WITHDRAWN**. The 9/18 count is historical context, not a set of exact official receipts.

## Release evidence disclosure

Strict release-checklist compliance is not established for this descriptive exception: Standard run records and public smoke/strict-validation receipts are not present in the snapshot. See [MEASURED.md](MEASURED.md) for the evidence gap.

| Source-reported lifecycle count | Count |
| --- | ---: |
| Planned cell IDs | 18 |
| Started cell IDs | 18 |
| Finished cell IDs | 18 |
| Officially graded cell IDs | 18 |
| ITT denominator | 18 |

Headline: Source-reported Kogen-RS results show 16/18 official full-suite passes; recovered internal R74 rows show 9/18. These are descriptive counts. Task base commits, public prompts, host assignment and timeout are reported to match; grader-script identity and the R74 task-setup hash are not verifiable. The matched preference rule is not adjudicated.
Configuration: `ladder-luna`; gpt-6-luna/max builder; gpt-6.1-sol/high shaper, fallback shaper, planner, auditor, reviewer and context; gpt-6-luna/max rung roles; no fallback; default prompt; 4,800-second cap; sequential jobs. The source-reported runner adapter used Kogen-RS commit `851dd0eed5b78709e35ff7da8533cb02dda12026`; its binary SHA-256 begins `607dd9be` (reported built once on US and copied to EU).
Accounting: total tokens = uncached input + cached input + output; weighted cache share = cached / (uncached + cached). Reasoning is reported separately.
Limit: Task base commits, public prompts, host assignment and timeout are reported to match. Grader-script identity and the R74 task-setup hash remain unverifiable, so the matched preference rule is not adjudicated. Three source-reported XDG-1 attempt-1 records are invalid harness attempts and replaced by same-ID attempt-2 runs. Syn-31 rep 3 remains in ITT; its wall time includes a source-reported concurrent grading window.
See [results](RESULTS.md) and the [predeclared decision rule](DECISION-RULE.md).

## Reproduce

Source-reported execution details and hashes below are not independently reproducible from the public snapshot.

Kogen commit: executed pin `851dd0eed5b78709e35ff7da8533cb02dda12026` (binary SHA-256 begins `607dd9be`; source-reported as built once on US and copied to EU). The registered pin and operator-recorded timeline are in the [Registration amendment](DECISION-RULE.md#registration-amendment-2026-10-08).

Harness commit: no separate harness Git commit is recorded. The run used the R74 `bench.py` runner (SHA-256 `4533c5ad901a585fecc92dc1ce05c86ba1958d5f5a370d58051162c75671e1`) and the `kogen-rs-runner` lane. The lane `SHA256SUMS` manifest is SHA-256 `4064b253a861c3884feb228a10979ae6028369173cb655fed02f168faeb69412`; the post-XDG-1 `run_kogen_rs_cell.py` is SHA-256 `66d2b3861b4e09181f93f92fa83f848a643fb607a72497f3c7a81ead4d620290`.

Model and effort: builder `gpt-6-luna`/`max`; shaper, fallback shaper, planner, auditor, reviewer and context `gpt-6.1-sol`/`high`; rung2 and rung3 `gpt-6-luna`/`max`, as mapped in `RECIPE.json`.

Task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-board-publish-unpublish-public-boundary`, `syn-06-migration-ticket-numbers`, `syn-20-email-invite-flow`, and `syn-31-inbound-email-webhook`.

Historical execution command: from the lane directory, each run used the matching host/task spec and cell selector:

```sh
python3 bench-rs.py run specs/<host-task>.json --only '<cell-selector>' --timeout 4800 --retries 0 --jobs 1 --no-gate --no-status-pause --cleanup
```

`--no-gate` was used for runner parity because no sealed release directory was available; the lane's admission and sandbox checks were separate.

Raw records: the operator source-reports official grade rows in `grades/tier1-grades.jsonl`, three invalid XDG-1 attempt-1 rows in `grades/tier1-invalid.jsonl`, and same-ID syn-06 attempt-2 rows supplying the counted outcomes. The grade ledgers, per-cell manifests, reports, requests, usage, recipe, runner manifest, and exclusion/incident receipts are not in the public snapshot. The source-reported execution used `--cleanup`, which removed the `.kogen` run directories.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/kogen-rs-ladder-luna-r74x.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 12 rows (ungraded 12); overall pass rate is n/a among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 12 missing published metadata). Missing counters remain unknown, not zero.
This round also has 12 raw-only or non-public rows; they are kept separate from the published-export denominator.
